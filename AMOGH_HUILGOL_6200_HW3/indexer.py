"""
    This module is used to create a inverted index file from the corpus. To run this
    program , the user has to provide 2 parameters through command line
    1) corpus-file : A file which contains document-ids and stem-words for that document
    2) output-file : The file where the inverted index will be stored

    This module needs to be called using following format

    python indexer.py corpus-file output-file

    In order for this program to work the corpus file must be in following format

    # document-id
    stem_word1 stem_word2 ........
    ..............................

    # document-id
    stem_word1 stem_word2 ........
    ..............................

    ..
    ..

    The output file will be in following format

    # stem-word
    document-id~count
       .
       .
       .
       .
    # stem-word
    document-id~count

"""


from sys import argv


def create_inverted_index(corpus_file_name, output_file_name):
    """ This module helps to build inverted index . the inverted index is built by reading
         entries from corpus_file_name that is supplied through command-line  .
         The inverted index is a dictionary in which stem words from index.out file are
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
    inverted_index = {}

    file_handle = open(corpus_file_name)
    file_text = file_handle.read()
    document_text = file_text.split("#")
    for document in document_text:
        document = document.replace('\n', ' ')
        stem_list = document.split(' ')
        stem_list = [x for x in stem_list if x != '']

        if len(stem_list) == 0:
            continue

        document_id = int(stem_list[0])
        stem_list = [x for x in stem_list if x.isdigit() is False]

        for stem_word in stem_list:
            if stem_word in inverted_index.keys():
                if document_id in inverted_index[stem_word].keys():
                    inverted_index[stem_word][document_id] += 1
                else:
                    inverted_index[stem_word][document_id] = 1

            else:
                inverted_index[stem_word] = {document_id: 1}



    file_output_handle = open(output_file_name, 'w')

    for words in inverted_index.keys():
        file_output_handle.write("# "+str(words)+"\n")

        for doc_id in inverted_index[words].keys():
            file_output_handle.write(str(doc_id)+"~"+str(inverted_index[words][doc_id])+"\n")

    file_output_handle.close()
    file_handle.close()


def build_inverted_index():
    script_name,index_file,output_file = argv
    create_inverted_index(index_file, output_file)

build_inverted_index()
