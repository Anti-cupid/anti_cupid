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
from tqdm import tqdm

if __name__ == "__main__":
    print("data_crawling...")
    args = get_args()
    yaml_data = read_yaml(args.yaml)
    

    data_lengths = []
    total_data_length = 0

    for i in tqdm(range(yaml_data['search_year_range'])):
        params = yaml_data['param']

        #####################################
        # # get response info as beautifulSoup object.
        ###################################
        soup = get_soup(yaml_data['crawling_url'] + "/search", params=params, headers=yaml_data['header'], proxy=True)
        
        # data
        save_output = []
        save_path = "../../data"
        save_filename = f"data_{str(params['period_from'])}.json"
        next_page = True
        page = 1

        while next_page:
            params['page'] = page
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
                
                judge_soup = get_soup(temp, params=None, headers=yaml_data['header'], proxy=True)
                data = get_judgement_content(judge_soup)
                
                data[2]['link'] = temp
                save_output.append(data[2])

            # ########################
            # # get next page link postfix
            # ########################
            next_page = get_next_page_postfix(soup)
            if next_page:
                page += 1
            else:
                next_page = False
        print("last page : ", page)
        print("{} data lenth : {}".format(params['period_from'], len(save_output)))
        
        data_lengths.append((params['period_from'], len(save_output)))
        total_data_length += len(save_output)
        
        with open(os.path.join(save_path, save_filename),'w', encoding='utf8') as f:
            json.dump(save_output,f,indent=4, ensure_ascii=False)

        params['period_from'] -= 1
        params['period_to'] -= 1
    


    ###### print saved data length logs
    for i in data_lengths:
        print("{} data length : {}".format(i[0], i[1]))
    print("total length : {}".format(total_data_length))
            
   