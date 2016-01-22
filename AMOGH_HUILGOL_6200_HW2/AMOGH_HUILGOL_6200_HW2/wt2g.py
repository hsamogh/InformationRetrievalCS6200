import math
import operator
import time

##########################################################################################
#   This function calculates the page rank for the nodes in the graph .
#   the information about the graph is supplied through the input parameter 'filename'
#
#
#  GIVEN : A file which consists of information regarding graph
#  RETURNS : Page rank values for the nodes in graph


def wt2g_page_rank(filename):

    st=time.time()
    # d is the PageRank damping/teleportation factor . we use d = 0.85
    d = 0.85

    # List of all initial nodes
    node_list = []

    # List of all sink nodes
    sink_node = []

    # outlink-info dictionary consists of outlink count for each node
    # outlink-info[node]=count
    outlink_info = {}

    # node-info dictionary consists of node and list of inlinks to the node :
    # node-info[Nodes] = list[Inlink-Nodes]
    node_info = {}

    # Dictionary of page-ranks of nodes at iteration 't'  : page_rank[node]=number
    page_rank_t = {}

    # Dictionary of page-ranks at iteration t+1 : page_rank[node] =number
    page_rank_after_t = {}

    # Opening file to store graph in memory
    file_handle = open(filename)

    # Reading graph in memory
    for lists in file_handle.readlines():
        list_of_nodes = lists.strip('\n').strip(' ').split(' ')
        node_list.extend(list_of_nodes)
        node_info["".join(list_of_nodes[0])] = list(set(list_of_nodes[1:]))
    node_list = list(set(node_list))

    # Closing the file after reading graph
    file_handle.close()

    # Generating a list of outlinks count for each page
    for node in node_list:
        list_of_outlinks = list(set(node_info.get(node, [])))
        for page in list_of_outlinks:
            if page not in outlink_info.keys():
                outlink_info[page] = 1
            else:
                outlink_info[page] += 1

    # Getting the list of keys from node_info dictionary . used later for getting list of
    # sink nodes
    keys_list = node_info.keys()
    sink_nodes = list(set(keys_list) - set(outlink_info.keys()))

    # Calculating initial page-rank and assigning it to all nodes
    N = len(node_list)

    # Assigning initial page-rank to all pages
    for node in node_list:
        page_rank_t[node] = 1 / N

    # Calculating default convergence at iteration 't'

    # convergence_count is used to check if four consecutive values less than 1 is
    # obtained
    convergence_count = 0

    # Convergence value after iteration t
    convergence_value_t = 0

    # Shannon Entropy at iteration 't'
    shannon_entropy_t = 0

    for node in page_rank_t:
        shannon_entropy_t += (page_rank_t[node] * math.log(page_rank_t[node], 2))
    convergence_value_t = 2 ** (shannon_entropy_t * -1)
    count=0
    while convergence_count != 4:
        count+=1
        sink_pr = 0

        # Calculating probability of sink nodes
        for node in sink_nodes:
            sink_pr = sink_pr + page_rank_t[node]

        for page in node_list:
            pr = (1 - d) / N
            pr += d * (sink_pr / N)
            inlinks_list = node_info.get(page, [])

            for inlink in inlinks_list:
                pr += ((d * page_rank_t[inlink]) / (outlink_info[inlink]))

            page_rank_after_t[page] = pr

        shannon_entropy_after_t = 0
        convergence_value_after_t = 0

        for node in page_rank_after_t:
            shannon_entropy_after_t += (
                page_rank_after_t[node] * math.log(page_rank_after_t[node], 2))

        convergence_value_after_t = 2 ** (shannon_entropy_after_t * -1)

        perplexity_file_handle= open('perplexity_values.txt','a')
        perplexity_file_handle.writelines('Convergence value at round {0} is {1} \n'.
                                          format(count, convergence_value_after_t))

        print('Convergence value at round {0} is {1}'.format(count,convergence_value_after_t))

        if (math.fabs(convergence_value_after_t - convergence_value_t)) < 1:
            convergence_count += 1
        else:
            convergence_count = 0

        page_rank_t = page_rank_after_t
        page_rank_after_t = {}
        convergence_value_t = convergence_value_after_t
        convergence_value_after_t = 0

    print('convergence reached after round {0} '.format(count))
    sorted_page_rank_docs = sorted(page_rank_t.items(), key=operator.itemgetter(1), reverse=True)

    top_50_pr_file_handle=open('top_50_by_page_rank.txt','a')
    top_50_pr_file_handle.writelines("TOP 50 DOCUMENTS BASED ON PAGE-RANK \n")
    top_50_pr_file_handle.writelines("*"*100 + "\n"*3)
    top_50_pr_file_handle.writelines("DOCUMENT-ID: PAGE RANK\n")
    for count in range(0,50):
        top_50_pr_file_handle.writelines(str(sorted_page_rank_docs[count][0])+" : "+str(sorted_page_rank_docs[count][1])+"\n")
    top_50_pr_file_handle.close()
    et=time.time();

    inlinks_count_list={}

    for node in node_list:
        inlinks_count_list[node] = len(node_info.get(node))

    sorted_by_inlinks = sorted(inlinks_count_list.items(),key=operator.itemgetter(1),reverse=True)
    top_50_inlinks_file_handle=open('top_50_by_inlinks.txt','a')
    top_50_inlinks_file_handle.writelines("TOP 50 DOCUMENTS BASED ON INLINKS \n")
    top_50_inlinks_file_handle.writelines("*"*100 + "\n"*3)
    top_50_inlinks_file_handle.writelines("DOCUMENT-ID : INLINK COUNT \n")
    for count in range(0,50):
        top_50_inlinks_file_handle.writelines(str(sorted_by_inlinks[count][0])+" : "+str(sorted_by_inlinks[count][1])+'\n')

    # Proportion of  inlinks
    proportion_file_handle = open('all_proportions.txt','a')

    inlink_zero_count=[x for x in node_info.keys() if not node_info[x] ]
    proportion_file_handle.writelines('Proportion of pages with no inlinks : '+str(len(inlink_zero_count)/N) + '\n')

    outlink_zero_count=len(sink_nodes)
    proportion_file_handle.writelines('Proportion of pages with no outlinks : '+str((outlink_zero_count)/N) + '\n')
    print(et-st)
    count = 0
    for node in page_rank_t :
        if page_rank_t[node]<(1/N):
            count+=1

    proportion_file_handle.writelines('Proportion of pages with page rank less than initial uniform value : '+str((count)/N) + '\n')




def page_rank():
    file_name = input("Enter file path : ")
    wt2g_page_rank(file_name)


page_rank()
