# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 20:31:15 2017
@author: Ulion_Tse
"""
import requests
import json
import re

def get_json(url):
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
    noqt_json = html[11:-2]
    return noqt_json

def trans_noq(noq_json):
    '''Expecting property name enclosed in double quotes.'''
    
    pattern1 = r',([0-9A-Z]+):'
    pattern2 = r':{([0-9a-z]+):'
    ff1 = set(re.findall(pattern1, noq_json))
    ff2 = set(re.findall(pattern2, noq_json))
    for i in ff1:
        noq_json = noq_json.replace(','+i+':', ',"'+i+'":')
    for j in ff2:
        noq_json = noq_json.replace(':{'+j+':', ':{"'+j+'":')
    noq_json = '{"1":' + noq_json[3:]
    return noq_json
    
def main(url):
    nq_json = get_json(url)
    trans_json = trans_noq(nq_json)
    data = json.loads(trans_json)
    return data

if __name__ == '__main__':
    url = 'http://s.url.cn/qqfind/js/location4.js'
    result = main(url)
    print(result)
