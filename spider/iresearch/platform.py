# coding=utf-8
# author:uliontse

import re
import time
import datetime
import random
import pymysql
import requests
from bs4 import BeautifulSoup



class Plat:
    def __init__(self):
        self.target_url = 'http://www.iresearch.tv/research/platform/data'
        self.now = str(datetime.date.today())
        self.header = dict()
        self.header['Host'] = 'www.iresearch.tv'
        self.header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.header['Accept-Encoding'] = 'gzip, deflate, sdch'
        self.header['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6'
        self.header['DNT'] = '1'
        self.header['Upgrade-Insecure-Requests'] = '1'
        self.header['Referer'] = 'http://www.iresearch.tv/research/platform/data?day=30&page=2'
        self.header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                                    ' Chrome/55.0.2883.87 Safari/537.36'
        self.conn = pymysql.connect(host='xxxx',
                                    port=33066,
                                    user='xxxx',
                                    password='xxxx',
                                    database='xxxx',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.create_sql = '''
                            CREATE TABLE IF NOT EXISTS xyl__Iresearch_v4
                                (
                                      crawlTime VARCHAR(10) NOT NULL
                                    , plat VARCHAR(8) NOT NULL 
                                    , rank INT(4) NOT NULL 
                                    , month_anchor_Broadcast BIGINT NOT NULL 
                                    , month_fans_online BIGINT NOT NULL 
                                    , day_anchor_active BIGINT NOT NULL 
                                    , month_anchor_new BIGINT NOT NULL 
                                    , plat_detail VARCHAR(256) NULL 
                                    , ID VARCHAR(64) NOT NULL PRIMARY KEY
                                );'''
        self.cur.execute(self.create_sql)

        self.ss = requests.Session()
        self.ss.headers.update(self.header)


    def transNum(self,N):
        trans_pool = {'亿': 10 ** 8, '万': 10 ** 4, '千': 10 ** 3}
        for X in trans_pool.items():
            if X[0] in N:
                r = re.findall('(.*?)' + X[0], N)[0]
                return int(float(r) * X[1])
        return int(N)

    def get_data(self):
        for i in range(1,3):
            res = self.ss.get(self.target_url+'?day=30&page={}'.format(i))
            soup = BeautifulSoup(res.text,'lxml')
            item = soup.find_all('div',{'class': 'orderlist'})[0].find_all('ul')
            for it in item:
                data = {
                    'rank': int(it.find_all('li',{'class': 'ranking'})[0].get_text()),
                    'plat': it.find_all('li',{'class': 'plat'})[0].get_text(),
                    'month_anchor_Broadcast': self.transNum(it.find_all('li', {'class': 'broadcast-num'})[0].get_text()),
                    'month_fans_online': self.transNum(it.find_all('li', {'class': 'audience-num'})[0].get_text()),
                    'day_anchor_active': self.transNum(it.find_all('li', {'class': 'active-anchor'})[0].get_text()),
                    'month_anchor_new': self.transNum(it.find_all('li', {'class': 'new-anchor'})[0].get_text()),
                    'plat_detail': it.find_all('li',{'class': 'plat'})[0].a.attrs['href'],
                    'crawlTime': self.now
                }
                yield data

    def save_data(self,dt):
        save_sql = '''
                    INSERT INTO xyl__Iresearch_v4 
                        (ID,crawlTime,plat,rank,month_anchor_Broadcast,month_fans_online,day_anchor_active,
                        month_anchor_new,plat_detail) 
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');
                    '''.format(
            '_'.join([str(dt['rank']),dt['plat'],dt['crawlTime']]), dt['crawlTime'], dt['plat'], dt['rank'],
            dt['month_anchor_Broadcast'],
            dt['month_fans_online'],dt['day_anchor_active'],dt['month_anchor_new'],dt['plat_detail']
        )
        try:
            self.cur.execute(save_sql)
            self.conn.commit()
            print('Save successfully!\r\n')
            return 1
        except pymysql.IntegrityError as e1:
            print(e1)
            return 0
        except pymysql.err.ProgrammingError as e2:
            print(e2)
            return 0

    def end(self):
        self.ss.close()
        self.cur.close()
        self.conn.close()
        return


def run():
    begin = time.time()
    saveNum = 0
    plat = Plat()
    try:
        for data in plat.get_data():
            print(data)
            saveNum += plat.save_data(data)
    finally:
        plat.end()
        print('saveNum: ',saveNum)
        print('useTime: ',int(time.time())-begin)


if __name__ == '__main__':
    run()
