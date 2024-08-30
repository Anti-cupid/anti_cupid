"""
This code is designed for https://casenote.kr/ url search crawling.
If you want to data crawl other urls, you have to adjust url's script to where you want.
"""

from utils import *
from args import *
from yaml_util import *

if __name__ == "__main__":
    print("data_crawling...")
    args = get_args()
    yaml_data = read_yaml(args.yaml)
    
    #####################################
    # # get response info as beautifulSoup object.
    ###################################
    soup = get_soup(yaml_data['crawling_url'] + "/search", params=yaml_data['param'], headers=yaml_data['header'], proxy=True)
    
    # #################################
    # # get judge content links
    # #################################
    links_postfix = get_links(soup)
    print("links_postfix : ")
    for i in links_postfix:
        print("\t", i)

    # ########################
    # # get list page number
    # ########################
    page_num = get_page_number(soup)
    print("page_num : ", page_num)


    # ########################
    # # get documents from each link
    # ########################
    for link in links_postfix:
        # temp = yaml_data['crawling_url'] + link
        
        # test
        # temp = yaml_data['crawling_url'] + "/대법원/2012므2918"
        # temp = yaml_data['crawling_url'] + "/서울고등법원/2015르717"
        # temp = yaml_data['crawling_url'] + "/대법원/2011므1116"
        temp = yaml_data['crawling_url'] + "/대법원/83므20"
        # temp = yaml_data['crawling_url'] + "/부산가정법원/2014드단201540"
        
        
        # print(temp)
        soup = get_soup(temp, params=None, headers=yaml_data['header'], proxy=True)
        data = get_judgement_content(soup)
        
        
        for i in data[1]:
            print("==================")
            print(i.text)

        
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
        # for i in data[2]:
        #     print("==================")
        #     print(i.text.strip())
        
        # for i in data:
        #     print(i.text)
        
        break