#-*- coding:utf-8 -*-

import re
import time
import json
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import psycopg2
from pprint import pprint as ppt




def get_tk(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'i.umeng.com',
        'Upgrade-Insecure-Requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
    }
    res = session.get(url=url, headers=headers)
    html = res.text
    tk = re.search(r'token: (.*?),', html)
    apk = re.search(r'appkey: (.*?),', html)
    sid = re.search(r'sessionid: (.*?),', html)
    return {
            'token': tk.group(1),
            'appkey': apk.group(1),
            'sessionid': sid.group(1)
    }

#print(session.cookies.get_dict())
#print(get_tk(host))

def login(host,login_url):
    form_data = {
        'token': get_tk(host)['token'],
        'username': 'qiqimobile@17guagua.com',
        'password': 'QJkj2016fhiier',
        'sig': '',
        'sessionid': '', #get_tk(host)['sessionid']
        'website': 'umengplus',
        'app_id': '', #get_tk(host)['appkey']
        'url': ''
        }
    headers = {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'content-length':'111',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'origin':'https://i.umeng.com',
        'referer':'https://i.umeng.com/?',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'x-requested-with':'XMLHttpRequest'
        }
    res = session.post(login_url,data=urlencode(form_data),headers=headers)
    return res


def get_csrf(csrf_url):
    headers = {
        'Host': 'mobile.umeng.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0', #TODO
        'Upgrade-Insecure-Requests': '1', #TODO
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://mobile.umeng.com/analytics',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    res = session.get(csrf_url, headers=headers)
    ppt(res.text)
    csrf = re.search(r'<meta name="csrf-token" content="(.*?)"/>', res.text)
    return csrf.group(1)


def get_data(visit_url):
    headers = {
        'Host': 'mobile.umeng.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-CSRF-Token': 'goWzlwdv+i1oBFDPmYDoPlE4AV3kekJ94P/xHHcavl4=', #get_csrf(csrf_url)
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://mobile.umeng.com/apps',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    params = {
        'page': 1,
        'per_page': 30,
        'type': 'all-apps-list',
        'show_all': 'false',
        'sort_metric': '',
        'order': ''
    }

    res = session.get(visit_url, params=params, headers=headers)

    return res.text















#ids = soup.find_all()

def main():
    print(login(host, login_url))
    ppt(get_data(visit_url))
    print(get_csrf(csrf_url))



if __name__ == '__main__':
    host = 'http://i.umeng.com/'
    login_url = 'https://i.umeng.com/login/ajax_do'
    csrf_url = 'http://mobile.umeng.com/apps'
    visit_url = 'http://mobile.umeng.com/apps/get_apps_stats_details'

    session = requests.Session()
    main()
#    session.close()

    print(session.cookies.get_dict())

