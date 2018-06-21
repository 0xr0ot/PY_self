# -*- coding:utf-8 -*-

import re
import time
import datetime
import json
import requests
import pymysql
from urllib.parse import urlencode
from pprint import pprint as ppt
from umeng_config import *


def get_tk(url):
    res = session.get(url=url, headers=headers_get_tk)
    html = res.text
    tk = re.search(r'token: (.*?),', html)
    apk = re.search(r'appkey: (.*?),', html)
    sid = re.search(r'sessionid: (.*?),', html)
    return {
        'token': tk.group(1),
        'appkey': apk.group(1),
        'sessionid': sid.group(1)
    }


def login(host, login_url):
    form_data = {
        'token': get_tk(host)['token'],
        'username': 'xxxx',
        'password': 'xxxx',
        'sig': '',
        'sessionid': '',  # get_tk(host)['sessionid']
        'website': 'umengplus',
        'app_id': '',  # get_tk(host)['appkey']
        'url': ''
    }
    res = session.post(login_url, data=urlencode(form_data), headers=headers_login)
    return res


def get_csrf(csrf_url):
    res = session.get(csrf_url, headers=headers_get_csrf)
    csrf = re.search(r'<meta name="csrf-token" content="(.*?)"/>', res.text)
    return csrf.group(1)


def get_app_data(visit_url):
    headers = {
        'Host': 'mobile.umeng.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-CSRF-Token': get_csrf(csrf_url).replace(r'&#47;', '/'),  # 'goWzlwdv+i1oBFDPmYDoPlE4AV3kekJ94P/xHHcavl4='
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://mobile.umeng.com/apps',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Cookie': cookie_app_0907
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
    data = json.loads(res.text)
    # print(data['result'])
    return data['stats']

#----------------------------------------above--------------------------------------
def get_channel_data(url):
    headers = {
        'Host': 'mobile.umeng.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-CSRF-Token': get_csrf(csrf_url).replace(r'&#47;','/'),  # 'goWzlwdv+i1oBFDPmYDoPlE4AV3kekJ94P/xHHcavl4='
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': re.search('(.*?)channels/',url).group(1),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Cookie': cookie_channel
    }
    params = {
        'page': 1,
        'per_page': 30,
        'date': 'yesterday',
        'stats': 'list',
        'groupid': ''
    }
    res = session.get(url,params=params,headers=headers)
    data = json.loads(res.text)
    ppt(data)
    if data['result'] == 'success':
        result = data['stats']
    else:
        print('页面无数据，等待1分钟后刷新~~~')
        time.sleep(60)
        res = session.get(url, params=params, headers=headers)
        data = json.loads(res.text)
        result =data['stats']
    return result

def appid_list(data):
    L = []
    for dt in data:
        L.append([dt['name'],dt['app_id']])
    return L

def save_channel_data(dt,app_it):
    sql =  ("INSERT INTO db_xxx.xxx__umeng_app_yesterday_channel "
            "(app_name,app_id,deadline,channel_name,secret_id,active_user,duration,launch,install,total_install,total_install_rate,channel_url)"
            "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}');".format(
            app_it[0],app_it[1],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dt['name'],dt['id'],dt['active_user'],dt['duration'],dt['launch'],dt['install'],
            dt['total_install'],dt['total_install_rate'],channel_url))

    cur.execute(sql)
    conn.commit()
    return 'Save successfully!\r\n {0}'.format(dt)


if __name__ == '__main__':
    host = 'http://i.umeng.com/'
    login_url = 'https://i.umeng.com/login/ajax_do'
    csrf_url = 'http://mobile.umeng.com/apps/'
    visit_url = 'http://mobile.umeng.com/apps/get_apps_stats_details/'

    conn = pymysql.connect(host='xxx.xx.xx.xx',
                                 port=3306x,
                                 user='xxx_user',
                                 password='xxxx',
                                 database='db_xxx',
                                 charset='utf8mb4')
                                 #cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS db_xxx.xxx__umeng_app_yesterday_channel "
        "(app_name text,app_id text,deadline timestamp,channel_name text,secret_id text,"
        "active_user int,duration text,launch int,install int,total_install int,"
        "total_install_rate float,channel_url text);")


    session = requests.Session()
    print(login(host, login_url))
    app_data = get_app_data(visit_url)
    for item in appid_list(app_data):
        ppt(item)
        channel_url = csrf_url + item[1] + '/channels/load_table_data?'
        channel_data = get_channel_data(channel_url)
        #ppt(channel_data)
        for dt in channel_data:
            ppt(dt)
            save_channel_data(dt,item)
        time.sleep(10)
    session.close()
    cur.close()
    conn.close()
    print('All session & db_connection closed.')
