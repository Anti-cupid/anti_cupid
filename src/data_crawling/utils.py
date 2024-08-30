"""
Utils for html content
"""

import sys
import requests as req
from bs4 import BeautifulSoup


######################
## Get method request and response using request and BeautifulSoup
######################
def get_soup(url:str, params:dict, headers:dict, proxy:bool=False)->BeautifulSoup:
    
    if proxy:
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }
        if params is not None:
            response = req.get(url, params=params, headers=headers, verify=False, proxies=proxies)
        else:
            response = req.get(url, headers=headers, verify=False, proxies=proxies)
    else:
        if params is not None:
            response = req.get(url, params=params, headers=headers, verify=False)
        else:
            response = req.get(url, headers=headers, verify=False)

    if response.status_code ==200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print("Request Response Error Occured. Error code : ", response.status_code)
        sys.exit()




#######################
## Get link infos and page infos search list
#######################
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


#######################
## Get judgement content data 
#######################
def get_judgement_content(soup:BeautifulSoup)->tuple:
    title = soup.find('div', 'cn-case-title')

    # content_title = soup.find_all('p', 'title')
    # content_main = soup.find_all('p', 'main-sentence')

    content_title = soup.find_all('div', 'panel')
    # content_main = soup.find_all('div', 'summary')
    content_main = soup.find_all('div', 'cn-case-body')

    return (title, content_title, content_main)
    
    # content = soup.find_all('div', {'class':'cn-case-left fs3'})
    # return content