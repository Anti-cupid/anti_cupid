"""
Utils for html content
"""

import sys
import requests as req
from bs4 import BeautifulSoup



def get_soup(url:str, params:dict, headers:dict)->BeautifulSoup:
    response = req.get(url, params=params, headers=headers)

    if response.status_code ==200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print("Request Response Error Occured. Error code : ", response.status_code)
        sys.exit()
        


def get_links(soup:BeautifulSoup)->list:
    links = soup.findAll('a', 'casename')
    
    link_data = []
    for link in links:
        href = link.attrs['href']
        link_data.append(href)
    return link_data

def get_page_number(soup:BeautifulSoup)-> int:
    page = soup.find_all('div', 'cn-pagination')
    span = page[0].find_all('span')
    if '이전' in span[0]:
        del span[0]
    if '다음' in span[-1]:
        del span[-1]
    page_num = span[-1].text.replace("<span>", "")
    page_num = page_num.replace("</span>", "")
    page_num = int(page_num)
    return page_num