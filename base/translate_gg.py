#!usr/bin/env python3
#-*-coding: utf-8-*-

import time
import json
import requests
from urllib.parse import quote
from urllib.parse import urlencode


def translate_gg(eng_txt):
    QQ = quote(eng_txt)
    url = ('https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md'+
            '&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&source=bh&ssel=0&tsel=0&kc=1&tk='+tk+'&q=' + QQ)
    headers = {'Accept': '*/*',
               'Accept-Language': 'zh-CN,zh;q=0.8',
               'accept-encoding': 'gzip, deflate, sdch, br',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
               'dnt': '1',
               'referer': 'https://translate.google.cn/',
               'x-client-data': 'CJK2yQEIprbJAQjEtskBCPqcygEIqZ3KAQ=='
               }

    session = requests.Session()
    r = session.get(url, headers=headers)
    js = json.loads(r.text)
    session.close()
    return js[0][0][0]

if __name__ == '__main__':
    result = translate_gg(eng_txt)
    print(result)
