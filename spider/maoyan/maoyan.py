#!usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import json
import requests
from requests.exceptions import RequestException


def get_page(url):
    try:
        response = requests.get(url) # try...except...for this line.
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_page(html):
    
    ## Opposite to original html, html parsed has a few changes.
    ## Especialy pay attention to 'data-src'.
    
    pattern = re.compile('<dd>.*?class="board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?'
                         +'name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
            }


def write_file(content):
    with open('my_maoyao_result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close() # necessary
        

def main(offset):
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_page(url)
    for item in parse_page(html):
        print(item)
        write_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i*10)
