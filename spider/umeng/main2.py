#-*- coding:utf-8 -*-

import re
import time
import json
import requests
from urllib.parse import urlencode,unquote
from bs4 import BeautifulSoup
import psycopg2
from pprint import pprint as ppt


cookie = '	cn_1258498910_dplus=%7B%22distinct_id%22%3A%20%2215e4d3ecb4455-0cb460099f6418-40544130-100200-15e4d3ecb45411%22%2C%22sp%22%3A%20%7B%22%24recent_outside_referrer%22%3A%20%22%24direct%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201504534652%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201504534652%7D%2C%22initial_view_time%22%3A%20%221504532668%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; UM_distinctid=15e4d3ecb4455-0cb460099f6418-40544130-100200-15e4d3ecb45411; cna=9U00EvCHzRoCAW/EgMWqndlh; isg=AgkJZI7UtBW3h0jhRNj0oKNhGTWj_vyL1U0z-at9yvAv8iEE9qchWBZiSl0n; umengplus_name=qiqimobile%4017guagua.com; umplusuuid=a79b2a99103c8a1b57e0c8b8ac6b044d; umplusappid=umcenter; __ufrom=http://i.umeng.com/; um_lang=zh; umlid_53b3de6dfd98c5e92c000a4c=20170904; ummo_ss=BAh7CUkiGXdhcmRlbi51c2VyLnVzZXIua2V5BjoGRVRbCEkiCVVzZXIGOwBGWwZvOhNCU09OOjpPYmplY3RJZAY6CkBkYXRhWxFpWGkBs2kB3mlyaQH9aQGYaQHFaQHpaTFpAGkPaVFJIhlnRTJQSXFPMjkxV3FCRXlidUd3TAY7AFRJIg91bXBsdXN1dWlkBjsARiIlYTc5YjJhOTkxMDNjOGExYjU3ZTBjOGI4YWM2YjA0NGRJIhBfY3NyZl90b2tlbgY7AEZJIjFkS3Nxc0xDMy9FMnpGUVd3aEpQRnVWbEM2YklpN25nZHpZUjBMS2YrUzA4PQY7AEZJIg9zZXNzaW9uX2lkBjsAVEkiJTljNTQ4YjQxNDcyMDgwMzE0MjA5YTA5MWQzOTAwZDkxBjsARg%3D%3D--5d9755d33c35f0d7444e9bd95f3f13204e022a55; cn_a61627694930aa9c80cf_dplus=%7B%22distinct_id%22%3A%20%2215e4d3ecb4455-0cb460099f6418-40544130-100200-15e4d3ecb45411%22%2C%22sp%22%3A%20%7B%7D%2C%22initial_view_time%22%3A%20%221504532660%22%2C%22initial_referrer%22%3A%20%22http%3A%2F%2Fi.umeng.com%2Fuser%2Fproducts%22%2C%22initial_referrer_domain%22%3A%20%22i.umeng.com%22%7D; CNZZDATA1258498910=398535413-1504532660-http%253A%252F%252Fi.umeng.com%252F%7C1504532660; CNZZDATA1259864772=1308082701-1504533202-http%253A%252F%252Fmobile.umeng.com%252F%7C1504533202; cn_1259864772_dplus=%7B%22distinct_id%22%3A%20%2215e4d3ecb4455-0cb460099f6418-40544130-100200-15e4d3ecb45411%22%2C%22sp%22%3A%20%7B%22%E6%98%AF%E5%90%A6%E7%99%BB%E5%BD%95%22%3A%20true%2C%22USER%22%3A%20%22qiqimobile%4017guagua.com%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201504536718%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201504536718%7D%7D'


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
        'username': 'qqmobile@guagua.com',
        'password': 'QJkj2016fhiier7102',
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
    #ppt(res.text)
    csrf = re.search(r'<meta name="csrf-token" content="(.*?)"/>', res.text)
    return csrf.group(1)


def get_data(visit_url):
    headers = {
        'Host': 'mobile.umeng.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-CSRF-Token': get_csrf(csrf_url).replace(r'&#47;','/'), #'goWzlwdv+i1oBFDPmYDoPlE4AV3kekJ94P/xHHcavl4='
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://mobile.umeng.com/apps',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Cookie': cookie
    }
    params = {
        'page': 1,
        'per_page': 30,
        'type': 'all-apps-list',
        'show_all': 'false',
        'sort_metric': '',
        'order': ''
    }
    res = session.get(visit_url,params=params,headers=headers)
    return res.text


def main():
    ppt(get_tk(host))
    print(login(host, login_url))
    print(get_csrf(csrf_url))
    ppt(get_data(visit_url))
    

if __name__ == '__main__':
    host = 'http://i.umeng.com/'
    login_url = 'https://i.umeng.com/login/ajax_do'
    csrf_url = 'http://mobile.umeng.com/apps'
    visit_url = 'http://mobile.umeng.com/apps/get_apps_stats_details'
    #visit_url = 'http://mobile.umeng.com/apps/get_apps_stats_details?page=1&per_page=30&type=all-apps-list&show_all=false&sort_metric=&order='

    session = requests.Session()
    main()
    session.close()
