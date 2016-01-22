# this program implements the page rank algorithm for set of nodes which represent the w
# web pages . the description of the problem can be found at
#
# http://www.ccs.neu.edu/course/cs6200f15/hw2.html
#

'''
This function calculates the page rank for the nodes in the graph . the information about
the graph is supplied through the input parameter 'filename'

GIVEN : A file which consists of information regarding graph
RETURNS : Page rank values for the nodes in graph
'''


def small_graph(file_name):
    # d is the PageRank damping/teleportation factor . we use d = 0.85
    d = 0.85

    # List of all initial nodes
    node_list = []

    # List of all sink nodes
    sink_node = []

    # outlink-info dictionary consists of outlink count for each node
    outlink_info = {}

    # node-info dictionary consists of node and list of inlinks to the node :
    node_info = {}

    # Dictionary of page-ranks of nodes at iteration 't'  : page_rank[node]=number
    page_rank_t = {}

    # Dictionary of page-ranks at iteration t+1 : page_rank[node] =number
    page_rank_after_t = {}

    # Opening file to store graph in memory
    file_handle = open(file_name, 'r')

    # Reading graph into memory
    for lists in file_handle.readlines():
        list_of_nodes = lists.strip('\n').split(' ')
        node_list.extend(list_of_nodes)
        node_info["".join(list_of_nodes[0])] = list(set(list_of_nodes[1:]))

    # Closing the file after reading graph into memory
    file_handle.close()

    # Eliminating duplicates from node_list
    node_list = list(set(node_list))

    # Calculating Outlink count for each node
    for node in node_list:
        list_of_outlinks = list(set(node_info.get(node, [])))
        for page in list_of_outlinks:
            if page not in outlink_info.keys():
                outlink_info[page] = 1
            else:
                outlink_info[page] += 1

    # Extracting list of keys from node_info dictionary .
    # This is used later to get sink nodes
    keys_list = node_info.keys()

    # Generating a list of sink nodes .
    sink_nodes = list(set(keys_list) - set(outlink_info.keys()))

    # Calculating initial page-rank and assigning it to all nodes
    N = len(node_list)

    # Assigning initial page_rank to all nodes
    for node in node_list:
        page_rank_t[node] = 1 / N

    # Initialising count to 1 . used to keep count of iterations in loop
    count = 1

    # Calculating Page Rank after  1, 10 and 100 iterations
    while count <= 100:
        sink_pr = 0

        # Calculating probability of sink nodes
        for node in sink_nodes:
            sink_pr += page_rank_after_t.get(node, 0)

        # Calculating page rank for a page
        for page in node_list:
            pr = (1 - d) / N

            # Distributing page-rank of sink nodes equally between all nodes
            pr += d * (sink_pr / N)

            # getting a list of inlinks for a particular page . This is used later to
            # calculate page_rank
            inlinks_list = node_info.get(page, [])

            # adding the contributing factor from each inlink page to the page rank
            for inlink in inlinks_list:
                pr += ((d * page_rank_t.get(inlink, 0)) / (outlink_info.get(inlink, 1)))

            page_rank_after_t[page] = pr

        page_rank_t = page_rank_after_t
        page_rank_after_t = {}
        sum_val = 0
        if count == 1 or count == 10 or count == 100:
            print("PAGE-RANK AFTER ITERATION " + str(count))
            for links in page_rank_t:
                sum_val = sum_val + page_rank_t[links]
                print(links + " : " + str(page_rank_t[links]))
            print(sum_val)

        count += 1



##########################################################################################
# The main function of the program which invokes page rank module.

# Given : This function takes no inputs
# Returns : Page rank of the nodes in graph after 1 , 10 ,100 iterations

def page_rank():
    file_name = input("Enter file path : ")
    small_graph(file_name)

#########################################################################################

# Calling main function
page_rank()
