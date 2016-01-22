# This program implements the different evaluation methods used for

import math

#########################################################################################

# Used to get relevance information from corpus'''
#
# GIVEN : file which contains relevance information
# RETURNS : This function extracts the contents of file and creates a dictionary of
#           relevance information . The structure of the dictionary is as follows
#
#    [quer_id] ----> [list of all relevant document_ids]

def build_relevance_info(relevance_file):
    relevance_info_dict = {}

    relevance_file_handle = open(relevance_file)
    for line in relevance_file_handle.readlines():
        text_tokens = line.split(" ")
        query_id = int(text_tokens[0].strip())
        doc_id = int(text_tokens[2].replace("CACM-", "").strip())
        if query_id in relevance_info_dict.keys():
            relevance_info_dict[query_id].append(doc_id)
        else:
            relevance_info_dict[query_id] = [doc_id]
    return relevance_info_dict


##########################################################################################

# This function extracts data from result_file into a dictionary .
#
# GIVEN : file which contains retrieved documents using BM25 scoring
# RETURNS : A dictionary which consists of query_id as key and list of retrieved documents
#           as values
#
# The structure of the dictionary is as follows
#
# [quer_id] ----> [list of all retrieved document_ids]


def build_result_info(result_file):
    result_info_dict = {}
    result_file_handle = open(result_file)

    for line in result_file_handle.readlines():
        line_tokens = line.split(" ")
        query_id = int(line_tokens[0].strip())
        if query_id == 1:
            query_id = 12
        elif query_id == 2:
            query_id = 13
        elif query_id == 3:
            query_id = 19

        doc_id = int(line_tokens[2])
        rank = int(line_tokens[3])
        score = float(line_tokens[4])

        if query_id in result_info_dict.keys():
            result_info_dict[query_id].append([doc_id, rank, score])
        else:
            result_info_dict[query_id] = [[doc_id, rank, score]]

    return result_info_dict


##########################################################################################
# Main function of the program
# This function calculates precision , recall , MAP , NDCG and precision@K for the result
# obtained from BM25 scoring method.
# The results are stored in results.txt

def main():
    relevance_file = "cacm.txt"
    result_list = "results.txt"
    precision_table = {}
    precision_at_20_table = {}

    print(
        " This module calculates precision , recall , precision@20 , MAP , NDCG for BM25 scores of HW3\n")

    # getting data from relevance file into dictionary
    relevance_info_dict = build_relevance_info(relevance_file)

    # getting data from result file into dictionary
    result_info_dict = build_result_info(result_list)
    query_id_keys = list(result_info_dict.keys())
    query_id_keys.sort()

    # Calculating precision , recall , MAP , ndcg , precision@20 for each query
    for query_id in query_id_keys:
        relevant_docs = 0
        total_docs_retrieved = 0
        precision = 0
        sum_p = 0
        count_p = 0
        recall = 0
        relevance_level = 0

        list_of_relevant_docs = relevance_info_dict[query_id]
        list_of_results = result_info_dict[query_id]

        count = 0

        idcg_count = len(relevance_info_dict[query_id])
        query_result_file_handle = open("result_for_query_" + str(query_id) + ".txt", "w")

        query_result_file_handle.writelines(
            "{0} {1} {2} {3} {4} {5} {6} \n".format("RANK".ljust(5),
                                                    "DOCUMENT-ID".ljust(15),
                                                    "BM25-SCORE".ljust(25),
                                                    "R".ljust(5),
                                                    "PRECISION".ljust(25),
                                                    "RECALL".ljust(25),
                                                    "NDCG"))
        #calculation for precision ,recall , map and ndcg begins here

        for result in list_of_results:
            rel1 = 0

            if result[0] in list_of_relevant_docs:
                relevant_docs += 1
                relevance_level = 1
            else:
                relevance_level = 0

            #calculating NDCG
            if count + 1 == 1:
                rel1 = relevance_level
                dcg = rel1
                idcg = 1
                idcg_count -= 1
            elif count + 1 == 2:
                dcg += (relevance_level / math.log(count + 1, 2))
                if idcg_count > 0:
                    idcg = 1 + (1 / math.log(count + 1, 2))
                    idcg_count -= 1
            else:
                dcg += (relevance_level / math.log(count + 1, 2))
                if idcg_count > 0:
                    idcg += (1 / math.log(count + 1, 2))
                    idcg_count -= 1

            total_docs_retrieved += 1

            #Calculating precision
            precision = relevant_docs / total_docs_retrieved
            if relevance_level == 1:
                sum_p += precision
                count_p = len(relevance_info_dict[query_id])

            #Calculating recall
            recall = relevant_docs / len(relevance_info_dict[query_id])

            #writing result to output file
            query_result_file_handle.writelines(
                "{0} {1} {2} {3} {4} {5} {6} \n".format(str(result[1]).ljust(5),
                                                        str(result[0]).ljust(15),
                                                        str(result[2]).ljust(25),
                                                        str(relevance_level).ljust(5),
                                                        str(precision).ljust(25),
                                                        str(recall).ljust(25),
                                                        str(dcg / idcg))
            )
            count += 1
            if count == 20:
                precision_at_20_table[query_id] = precision
        precision_table[query_id] = sum_p / count_p


    precision_at_20_file_handle = open("precision_at_20_values.txt", "w")
    query_id_list = list(precision_at_20_table.keys())

    precision_at_20_file_handle.writelines(
        "{0} {1}\n".format("Query Id".ljust(12), "Precision@20"))

    query_id_list.sort()

    for query_id in query_id_list:

        #Writing output to file

        precision_at_20_file_handle.writelines(
            "{0} {1}\n".format(str(query_id).ljust(12),
                               str(precision_at_20_table[query_id])))

        print("Query_id : " + str(query_id) + " Precision@20 : " + str(
            precision_at_20_table[query_id]))

    # Calculation for Mean Average Precision
    sum_of_precision = 0
    for precisions in precision_table.keys():
        sum_of_precision += precision_table[precisions]

    # Calculating mean average precision
    mean_average_precision = sum_of_precision / len(precision_table.keys())
    mean_precision_file_handle = open("mean_average_precision.txt", "w")
    mean_precision_file_handle.writelines(
        "Mean Average Precision is : {0}\n".format(str(mean_average_precision)))

    mean_precision_file_handle.close()
    print("Mean Average Precision is : " + str(mean_average_precision))

    #Closing the files
    precision_at_20_file_handle.close()
    mean_precision_file_handle.close()
    query_result_file_handle.close()


main()
