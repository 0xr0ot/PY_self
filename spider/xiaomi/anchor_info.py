#coding:utf-8

import time
import datetime
import requests
import json
import pymysql
from pprint import pprint as ppt


def get_data(url,anchor_id):
    headers = {
        'Host': 's.zb.mi.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Referer': 'http://live.mi.com/lang/cn/index.html?zuid=4269660&lid=4269660_{0}'.format(int(time.time())-10000),#TODO
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
    }
    params = {
        'callback': 'cb',
        'lid': str(anchor_id)+'_'+str(int(time.time())),#'4269660_1504861488',
        'zuid': anchor_id,#4269660,
        '_': int(1000 * time.time()),#1504866219226,
    }
    try:
        res = session.get(url,params=params,headers=headers)
        data = json.loads((res.text)[3:-1])
        info_data = data['data']['user']
    except:
        info_data = None
        print('data None.')
    return info_data


def save_data(dt,nick_name):
    #global pool
    #pool = []
    try:
        sql =  ("INSERT INTO db_xxx.xxx__xiaomi_anchor_info "
                "(anchor_id,nickname,gender,level,sign,certification,certificationType,badge,avator,deadline)"
                "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}');".format(
                dt['userId'],nick_name,dt['gender'],dt['level'],dt['sign'],dt['certification'],
                dt['certificationType'],dt['badge'],dt['avator'],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()
        #pool.append(dt['userId'])
    return 'Save successfully!\r\n {0}'.format(dt)


def main(begin,end):
    for anchor_id in range(begin,end):
        print('anchor_id: {0}'.format(anchor_id))
        data = get_data(url,anchor_id)
        if data:
            try:
                nick_byte = data['nickname'].encode()
                nick_name = nick_byte.decode('unicode_escape')
            except:
                nick_name = data['nickname']
            save_data(data,nick_name)
            ppt(data)


if __name__ == '__main__':
    url = 'http://s.zb.mi.com/get_liveinfo'
    begin,end = 1,50000000#11076

    conn = pymysql.connect(host='xxx.xx.xx.xx',
                                 port=3306x,
                                 user='xxx_user',
                                 password='xxxx',
                                 database='db_xxx',
                                 charset='utf8mb4')
                                 #cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS db_xxx.xxx__xiaomi_anchor_info "
        "(anchor_id INT PRIMARY KEY,nickname text,gender INT,level INT,sign text,certification text,certificationType INT,"
        "badge INT,avator text,deadline TIMESTAMP);")

    session = requests.Session()
    main(begin,end)#TODO
    session.close()
    cur.close()
    conn.close()
    print('All session & db_connection closed.')
    #print(pool)
