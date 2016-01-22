'''
Web crawler to crawl the Wikipedia pages .

The seed page is 'https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher'

The description of the problem is present in the following link

http://www.ccs.neu.edu/course/cs6200f15/hw1.html

@author : Amogh Huilgol

'''

#importing libraries for regular expressions and web requests
from bs4 import BeautifulSoup
import urllib.request 
import re
import time



########################################################################

#    This function crawls a link and extracts all the links in the web page . This function returns
#    list of links
#
# GIVEN : A link and key phrase . The key phrase is used only in case of focussed crawler
#         If the key phrase is blank , then a general web crawler is implemented.
#
# RETURNS : A list of links for a web page

def wiki_crawler(link , key_phrase=""):

    temp_links=[]
    source_code = urllib.request.urlopen(link).read()
    
    links_list =re.findall(r'<a href="/wiki/.*?"',str(source_code))
    for link in links_list:
        if(re.search(":",link) or link is "/wiki/Main_Page"):
            continue
        else:
            temp_links.append("https://en.wikipedia.org"+link[9:len(link)-1])
    #temp_links=list(set(temp_links))
    temp_links1=[]
    for link in temp_links:
        if(link not in temp_links1):
            temp_links1.append(link)
        
    return temp_links1

#########################################################################
#
#    This function checks if the key_phrase is present in the link . This function is used
#    only for focussed crawler.
#
#    GIVEN : A link of web page , the key phrase to be searched and the current depth of
#            search by web crawler
#
#    RETURNS : True if the key phrase is present in the link . false otherwise. If the web link
#             is the seed page , then the function returns true irrespective of whether the
#             key phrase is found
#
#

def check_key_phrase_match(link,key_phrase,depth):

    if ((key_phrase is "") or (depth==1)):
        return True
    else:
        source_code = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(source_code)
        [links.extract() for links in soup(['style', 'script', '[document]'])]
        text_content = soup.getText()
        if (text_content.lower().find(key_phrase.lower()) >= 0):
            return True
        else:
            return False
#########################################################################
   # This is the main function which is called when the program begins
   #
   # GIVEN : The function does not take any inputs
   # RETURNS : List of all links crawled.

def main_function():
   seed_url="https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    depth_list=[seed_url]
    result_list=[]
    depth=1
    temp_list=[]
    link_pool=[]
    KEY_WORD_PRESENT=True
    KEY_WORD_FOUND=False
    relevant_list=[]
    
    # Asking user for key_phrase preference
    answer=input("Do you want to enter key_phrase ?[y/n]")

    # Asking user to enter a key phrase if preference is 'y'
    if(answer.lower()[0] is 'y'):
        key_phrase= input("Enter a key phrase : ")
        print("KEY PHRASE ENTERED IS "+key_phrase)
    else :
        key_phrase=""
        print("CONTINUING WITHOUT A KEY PHRASE")

   #Checking to see if the user has entered only blanks as key_phrase     
    if( key_phrase.replace(" ","") is ""):
        key_phrase=""

    count=0
    #Crawling upto 5 levels begins
    while(depth<= 5):
        print("DEPTH "+ str(depth) + " CRAWLING STARTED ")
        for link in depth_list:
            temp_list=wiki_crawler(link,key_phrase)
            time.sleep(1)
            
            if(link not in result_list and key_phrase is ""):
                result_list.append(link)
                
            if(len(result_list)>=1000):
                break;
            
            for link in temp_list:
                
                if(link is not 'en.wikipedia.org/wiki/Main_Page' and link not in result_list and link not in link_pool):
                    count=count+1
                    if(check_key_phrase_match(link,key_phrase,depth+1)):
                        relevant_list.append(link)
                        link_pool.append(link)
                        if(key_phrase is not ""):
                           result_list.append(link)
                if(count>=1000 and key_phrase is not ""):
                    for link in depth_list:
                        if(link not in result_list):
                            result_list.append(link)
                    break;
        if(len(result_list)>=1000):
             break;
        if(count>=1000 and key_phrase is not ""):
             break;
        depth_list=link_pool
        link_pool=[]
    #Stopping at 1000 unique links
        if(len(result_list)>=1000):
            break
        depth+=1
    #Displaying the result
    for link in result_list:
        print(link)
        
#######################################################################################        
#Calling main function to start program
main_function()
    
