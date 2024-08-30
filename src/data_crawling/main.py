"""
This code is designed for https://casenote.kr/ url search crawling.
If you want to data crawl other urls, you have to adjust url's script to where you want.
"""

from utils import *
from args import *
from yaml_util import *
import pprint
import json
import os

if __name__ == "__main__":
    print("data_crawling...")
    args = get_args()
    yaml_data = read_yaml(args.yaml)
    



    for i in range(yaml_data['search_year_range']):
        params = yaml_data['param']

        print("==============")
        print(params['period_from'])
        print(params['period_to'])

        #####################################
        # # get response info as beautifulSoup object.
        ###################################
        soup = get_soup(yaml_data['crawling_url'] + "/search", params=params, headers=yaml_data['header'], proxy=True)
        
        # ########################
        # # get list page number
        # ########################
        page_num = get_page_number(soup)
        print("page_num : ", page_num)
        
        # data
        save_output = []
        save_path = "../data"
        save_filename = f"divorce_data_{str(params['period_from'])}.json"
        for i in range(1, page_num+1):
            params['page'] = i
            soup = get_soup(yaml_data['crawling_url'] + "/search", params=params, headers=yaml_data['header'], proxy=True)
            # #################################
            # # get judge content links
            # #################################
            links_postfix = get_links(soup)


            # ########################
            # # get documents from each link
            # ########################

            for link in links_postfix:
                temp = yaml_data['crawling_url'] + link
                
                soup = get_soup(temp, params=None, headers=yaml_data['header'], proxy=True)
                data = get_judgement_content(soup)
                
                data[2]['link'] = temp
                save_output.append(data[2])
            
        with open(os.path.join(save_path, save_filename),'w', encoding='utf8') as f:
            json.dump(save_output,f,indent=4, ensure_ascii=False)

        params['period_from'] -= 1
        params['period_to'] -= 1






    # # print(yaml_data['search_year_range'])
    
    
    # # #################################
    # # # get judge content links
    # # #################################
    # links_postfix = get_links(soup)
    # print("links_postfix : ")
    # for i in links_postfix:
    #     print("\t", i)

    # # ########################
    # # # get list page number
    # # ########################
    # page_num = get_page_number(soup)
    # print("page_num : ", page_num)


    # # ########################
    # # # get documents from each link
    # # ########################
    # save_output = []

    # # page, year
    # for link in links_postfix:
    #     temp = yaml_data['crawling_url'] + link
        
    #     soup = get_soup(temp, params=None, headers=yaml_data['header'], proxy=True)
    #     data = get_judgement_content(soup)
        
    #     data[2]['link'] = temp
    #     save_output.append(data[2])
    
    # with open('resultfile.json','w', encoding='utf8') as f:
    #     json.dump(save_output,f,indent=4, ensure_ascii=False)
        