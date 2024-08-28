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
    soup = get_soup(yaml_data['crawling_url'], params=yaml_data['param'], headers=yaml_data['header'])
    
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