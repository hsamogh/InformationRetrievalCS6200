INFORMATION RETRIEVAL -ASSIGNMENT 1
******************************************************************************************

This assignment has been coded using python 3.4.2

There are two python programs for this assignment

a) page-rank.py : This program computes page-rank values for 1 , 10 ,100 iterations on sample graph

b) wt2g.py : This program computes page-rank , perplexity , convergence values , proportions of nodes with
             no inlinks and outlinks

In order to successfully run this code ,we need following libraries

a) math : This library is inbuilt in python compiler . However if it is not present , the steps to install 
          math library is present in the following location
          https://docs.python.org/3.2/install/

HOW TO  RUN THE PROGRAM
------------------------
*) page-rank.py
*******************************
to run the program use the command : python3.4 <filename>.py

Once the program runs , we are asked for input 

a) Enter file path : At this stage user has to enter the path where the file is present.

OUTPUT : The page-rank values for 1 , 10 and 100 iterations on graph is displayed on terminal


*) wt2g.py
********************************
to run the program use the command : python3.4 <filename>.py

Once the program runs , we are asked for input 

a) Enter file path : At this stage user has to enter the path where the file is present.

OUTPUT : the code generates 4 files

perplexity_values.txt   : This file consists of perplexity value for each round
top_50_by_inlinks.txt   : This file consists of top 50 documents retrieved based on number of inlinks
top_50_by_page_rank.txt : This file consists of top 50 documents retrieved based on page rank values
all_proportions.txt     : This file consists of three types of proportions
                          a) the proportion of pages with no in-links (sources)
                          b) the proportion of pages with no out-links (sinks)
                          c) the proportion of pages whose PageRank is less than their initial, uniform values.




