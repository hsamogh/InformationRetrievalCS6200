""" This module implements the BM25 algorithm . In order to run this program , the user
    has  to supply 3 parameters through command-line
    1) index-file : the file which contains inverted index information
       The inverted index file must have following format :

       # stem-word
       document-id~count
       .
       .
       .
       .
       # stem-word
       document-id~count

    2) queries file : A file containing queries for which documents are to be ranked
    3) max-documents : maximum number of documents to be retrieved for each query

    The module can be called with following format

    python bm25.py index-file queries-file max-documents

    OUTPUT : The top ranked documents based on BM25 scores . The output is of the format

          Query-id Q0 Document-id Rank bm25-score system-name

    The string Q0 is a literal used by the standard TREC evaluation script.  We can use
    space-free token for your system_name. """


from sys import argv
import math
import operator

##########################################################################################

# Input : index file
# Output : dictionary containing inverted index and dictionary containing token count
#          i.e number of tokens in each document


def create_inverted_index(file_name):
    """ This module helps to build inverted index . the inverted index is built by reading
         entries from file_name
         The inverted index is a dictionary in which stem words from file_name file are
         the keys . each stem word is associated with list of tuples of format
         (document-id , count) . count refers to the number of times the stem word appears
         in the document . The index file is of the form :

         # stemmed_word
         document_id~count
         .
         .
         .


         The inverted index data structure is of the form :

       {stem_word} -> [(document_id1,count) (document_id2,count)....(document_idn, count)]
    """

    # Initialising all variables

    inverted_index = {}
    token_count_dict = {}
    file_handle = open(file_name)
    file_text = file_handle.read()

    # Each word in index file starts with '#' . document_text consists of list of stemmed
    # words along with document_ids and counts
    document_text = file_text.split("#")

    for document in document_text:
        document = document.replace('\n', ' ')
        stem_list = document.split(' ')
        stem_list = [x for x in stem_list if x != '']

        if len(stem_list) == 0:
            continue

        # Each element in document_text list will have stem_word as first element and the
        # document_id~count pairs from second . So we take first element as key and then
        # process rest of the list (i.e stem_list[1:]) to generate (document,count) pairs

        stem_word = stem_list[0]
        inverted_index[stem_word] = []
        stem_list = stem_list[1:]

        for token in stem_list:
            doc_id, count = token.split('~')
            doc_id = int(doc_id)
            count = int(count)
            inverted_index[stem_word].append((doc_id, count))
            if doc_id not in token_count_dict.keys():
                token_count_dict[doc_id] = count
            else:
                token_count_dict[doc_id] += count

    return inverted_index, token_count_dict


##########################################################################################

# This function is used to calculate value of avdl
#
# Input : token-count dictionary containing  document-id as key and number of tokens
#         present in the document as value
#
# output : avdl value

def calculate_average(list_of_values):
    return sum(list_of_values) / len(list_of_values)


##########################################################################################

# This function is used to calculate the value of K for each document
#
# Input : token-count dictionary containing  document-id as key and number of tokens
#         present in the document as value , value of k1 , value of b , value of avdl
#
# Output: dictionary containing K value for each document .
#         the structure of dictionary is as follows
#         {key->value} => {document_id->k-value}

def calculate_k(token_count_dict, k1, b, avdl):
    dictionary_of_k = {}
    for doc_id in token_count_dict:
        k = k1 * ((1 - b) + (b * (token_count_dict[doc_id] / avdl)))
        dictionary_of_k[doc_id] = k
    return dictionary_of_k


##########################################################################################

#  This function generates term-count dictionary for queries
#
# INPUT  : A list containing query terms
# OUTPUT : A dictionary containing of terms as keys and number of occurrences as values
#          The structure of the dictionary is as follows
#           {key -> value} => { query_term -> term_count}

def get_query_term_count_dictionary(term_list):
    query_term_count_dict = {}

    for term in term_list:
        if term in query_term_count_dict:
            query_term_count_dict[term] += 1
        else:
            query_term_count_dict[term] = 1

    return query_term_count_dict

##########################################################################################

# This function computes the bm25 score for the queries . the queries are to be supplied
# in a file and must be passed through command line . This function is the main function
# and invokes other functions
#
# INPUT : This function takes three inputs .
#         1) index-file
#         2) query-file
#         3) maximum number of document results
#
# Note : All the input parameters are to be supplied through command line
#
# OUTPUT : The top ranked documents based on BM25 scores . The output is of the format
#
#          Query-id Q0 Document-id Rank bm25-score system-name
#
# The string Q0 is a literal used by the standard TREC evaluation script.
# We can use space-free token for your system_name.


def bm25():

    # Initialising all variables
    k1 = 1.2
    k2 = 100
    b = 0.75
    system_name = "amogh"
    query_token = "Q0"

    # reading inputs to the function that are passed through command line
    script_name, index_file, query_file, max_count = argv

    # Creating inverted index dictionary and token-count dictionary
    (inverted_index, token_count_dict) = create_inverted_index(index_file)

    # N represents the total number of documents in the collection
    N = len(token_count_dict.keys())

    max_count = int(max_count)

    # calculating value of avdl
    avdl = calculate_average(token_count_dict.values())


    # calculating  value of K for each document
    dictionary_of_k = calculate_k(token_count_dict, k1, b, avdl)

    query_file_handle = open(query_file)
    query_id = 0

    for queries in query_file_handle.readlines():

        # Generating a new query_id
        query_id += 1

        # processing the query file to get list of words for each query
        query_term_list = queries.strip('\n').split(' ')
        query_term_list = [x for x in query_term_list if x != '']

        # Setting bm25 score to zero
        bm25_score = 0

        query_term_count_dict = get_query_term_count_dictionary(query_term_list)
        bm25_rank_dictionary = {}
        for term in query_term_list:

            # ni refers to the number of documents containing the term-i
            ni = len(inverted_index.get(term, []))

            # qfi refers to the number of times the term-i appears in query
            qfi = query_term_count_dict[term]

            # getting list of document-count pairs containing the term
            fi_list = inverted_index.get(term, [])

            # The doc_tuple is of form (document-id, count)
            for doc_tuple in fi_list:

                bm25_score = 0
                doc_id = doc_tuple[0]
                fi = doc_tuple[1]

                k = dictionary_of_k[doc_id]

                # Calculating bm25 score . bm25 score is calculated using 4 components
                a = (ni + 0.5) / (N - ni + 0.5)
                b = 2.2 * fi
                c = k + fi
                d = 101 * qfi
                e = 100 + qfi

                bm25_score = math.log((1 / a)) * (b / c) * (d / e)

                if doc_id in bm25_rank_dictionary.keys():
                    bm25_rank_dictionary[doc_id] += bm25_score
                else:
                    bm25_rank_dictionary[doc_id] = bm25_score

        # sorting the dictionary of documents containing bm25 scores in the decreasing
        # order of bm25 score
        sorted_x = sorted(bm25_rank_dictionary.items(), key=operator.itemgetter(1),
                          reverse=True)

        count = 0

        # printing result
        for element in sorted_x:
            count += 1
            print(str(query_id) + " " + query_token + " " + str(element[0]) + " " + str(
                count) + " " + str(element[1])+ " " + system_name)
            if count >= max_count:
                break

    query_file_handle.close()

bm25()
