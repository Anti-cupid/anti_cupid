"""
This code for https://casenote.kr/ url search crawling.
If you want crawling other url, you have to analysis url's script where you want.
"""
import yaml
import requests as req
import argparse
from bs4 import BeautifulSoup

def read_yaml(yaml_path):
    with open(yaml_path) as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
    return yaml_data

def get_args():
    parser = argparse.ArgumentParser(description='Data crawling for specific URL.')
    parser.add_argument('--yaml', default='./yaml/data_crawling.yaml')
    args = parser.parse_args()
    return args

if __name__=="__main__":
    print("data_crawling...")
    args = get_args()
    print(args)
    yaml_data = read_yaml(args.yaml)
    print(yaml_data)
    # print("https://casenote.kr/search/?q=2024.%208&sort=0&case=0%2C1%2C2%2C3%2C4&period=4&period_from=2024&period_to=2024&oc=1%2C2%2C3")
    # https://casenote.kr/search/?q=%EC%9D%B4%ED%98%BC&exclusion=&sort=0&period=4&period_from=2024&period_to=2024
    # https://casenote.kr/search/?q=2024&sort=0&period=0&partial=0&page=1
    url = yaml_data['crawling_url']
    print(url)
    params = {
        "q" :yaml_data["q"],
        "sort" :0,
        "period" :yaml_data["period"],
        "period_from" :yaml_data["period_from"],
        "period_to" :yaml_data["period_from"],
        "page" :yaml_data["page"],

    }
    headers= {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'}
    response = req.get(url, params=params, headers=headers)
    # response = req.get("https://naver.com", headers=headers)
    print(response.status_code)
    # url = url+"/?"\
    #     "q="+yaml_data["q"]+\
    #     "&sort=0"+ \
    #     "&period=4" + \
    #     "&period_from="+str(yaml_data["period_from"])+\
    #     "&period_to="+str(yaml_data["period_from"])+\
    #     "&page="+str(yaml_data["page"])
    print(url)

