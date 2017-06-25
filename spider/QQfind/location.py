# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 00:51:51 2017

@author: Ulion_Tse
"""

import requests
import json

def main(url):
    headers = {
        'Host': 's.url.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.59 QQ/8.6.18804.201 Safari/537.36',
        'Referer': 'http://find.qq.com/index.html?version=1&im_version=5497&width=910&height=610&search_target=0',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-us,en'    
        }
    
    res = requests.get(url, headers=headers)
    html = res.text
    html = html[12:-3]+'}'
    data = json.loads(html)
    return data

if __name__ == '__main__':
    url = 'http://s.url.cn/qqfind/js/location.js'
    print(main(url))
