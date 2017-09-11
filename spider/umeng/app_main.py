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
        'username': 'qqmobile@guagua.com',
        'password': 'QJkj2016fhiier7102',
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
        'X-CSRF-Token': get_csrf(csrf_url).replace(r'&#47;','/'),  # 'goWzlwdv+i1oBFDPmYDoPlE4AV3kekJ94P/xHHcavl4='
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://mobile.umeng.com/apps',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Cookie': cookie_app
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
    #print(data['result'])
    return data['stats']


def save_app_data(dt):
    sql =  ("INSERT INTO db_xxx.xxx__umeng_app_yesterday "
            "(app_name,deadline,platform,active_yesterday,launch_yesterday,install_yesterday,install_all,"
            "sdk_version,sdk_tip,starred,app_id,game,report_path,host_url)"
            "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}');".format(
            dt['name'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            dt['platform'],dt['active_yesterday'],dt['launch_yesterday'],dt['install_yesterday'],dt['install_all'],
            dt['sdk_version'],dt['sdk_tip'],dt['starred'],dt['app_id'],dt['game'],dt['report_path'],csrf_url))

    cur.execute(sql)
    conn.commit()
    return 'Save successfully!\r\n {0}'.format(dt)


def main_app():
    ppt(get_tk(host))
    print(login(host, login_url))
    print(get_csrf(csrf_url))
    data = get_app_data(visit_url)
    for dt in data:
        save_app_data(dt)
        time.sleep(1)
        print(dt)
    print('Spider finished!')


if __name__ == '__main__':
    host = 'http://i.umeng.com/'
    login_url = 'https://i.umeng.com/login/ajax_do'
    csrf_url = 'http://mobile.umeng.com/apps'
    visit_url = 'http://mobile.umeng.com/apps/get_apps_stats_details'

    conn = pymysql.connect(host='xxx.xx.xx.xx',
                                 port=3306x,
                                 user='xxx_user',
                                 password='xxxx',
                                 database='db_xxx',
                                 charset='utf8mb4')
                                 #cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS db_xxx.xxx__umeng_app_yesterday "
        "(app_name text,deadline timestamp PRIMARY KEY,platform text,active_yesterday int,"
        "launch_yesterday int,install_yesterday int,install_all int,"
        "sdk_version text,sdk_tip text,starred text,app_id text,game text,report_path text,host_url text);")

    session = requests.Session()
    main_app()
    session.close()
    cur.close()
    conn.close()
    print('All session & db_connection closed.')
