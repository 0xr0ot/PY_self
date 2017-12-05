# coding=utf-8
# author:uliontse

import re
import time
import random
import pymysql
import requests
from bs4 import BeautifulSoup
from pprint import pprint as ppt
from config import *


class Xhulu:
    def __init__(self):
        self.header = dict()
        self.tm = int(time.time())
        self.target_url = 'http://www.xiaohulu.com/Anchor/index.html'
        self.bang_pool = ['吸金指数','礼物价值','礼物人数']
        self.header['Host'] = 'www.xiaohulu.com'
        self.header['Refer'] = 'http://www.xiaohulu.com/'
        self.header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        self.header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.header['Accept-Encoding'] = 'gzip, deflate, sdch'
        self.header['Cookie'] = 'PHPSESSID=mmm760v9otil1qm4st72daj7s6; Hm_lvt_2772005b8bc0b193d080228322981977={0},{1}; ' \
                    'Hm_lpvt_2772005b8bc0b193d080228322981977={2}; Hm_lvt_1c358b33dfa30c89dd3a1927a5921793={3},' \
                    '{4}; Hm_lpvt_1c358b33dfa30c89dd3a1927a5921793={5}'.format(
                    self.tm-153427,self.tm-2376,self.tm-1,self.tm-153427,self.tm-2377,self.tm)

        self.conn = pymysql.connect(host='xxxx',
                                    port=33066,
                                    user='xxxx',
                                    password='xxxx',
                                    database='xxxx',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.create_sql = '''
                            CREATE TABLE IF NOT EXISTS xyl__Xhulu_v2
                                (
                                      plat VARCHAR(8) NOT NULL
                                    , bang VARCHAR(8) NOT NULL                                       
                                    , nm VARCHAR(96) NOT NULL 
                                    , rank VARCHAR(4) NOT NULL 
                                    , hsnum VARCHAR(10) NOT NULL 
                                    , logDate VARCHAR(10) NOT NULL
                                    , crawlTime INT(10) NOT NULL
                                    , info VARCHAR(256) NOT NULL 
                                    , img VARCHAR(256) NOT NULL 

                                );'''
        self.cur.execute(self.create_sql)

        self.ss = requests.Session()
        self.ss.headers.update(self.header)
        self.res = self.ss.get(self.target_url)
        self.soup = BeautifulSoup(self.res.text,'lxml')


    def end(self):
        self.ss.close()
        self.cur.close()
        self.conn.close()
        return


    def get_durTime(self):
        durs = self.soup.find_all('select',{'size': '1'})[0].find_all('option')
        dur_pool = dict()
        for dur in durs[1:]:
            dur_pool[dur.get_text()] = dur.attrs['value']
        return dur_pool

    def get_plat(self):
        plats = self.soup.find_all('select',{'class': 'on'})[0].find_all('option')
        plat_pool = dict()
        for plat in plats:
            plat_pool[plat.get_text().strip().replace(r'\r\n','')] = re.findall('plat=(.*?)&',plat.attrs['value'])[0]
        return plat_pool

    def get_data(self):
        for plat in self.get_plat().items():
            payload = {'plot': plat[1],'class': 'all','day': 'month','y': 1}
            headers = {'User-Agent': random.choice(UA_POOL)}
            res = requests.get(self.target_url,params=payload,headers=headers)
            soup = BeautifulSoup(res.text,'lxml')
    
            for i,bang in enumerate(self.bang_pool):
                gold = soup.find_all('div',{'class': 'fl'})[1].find_all('div',{'class': 'svtable'})[i] #吸金榜 #吸金指数
                for item in gold.find_all('table'):
                    data = {
                        'plat': plat[0],
                        'logDate': '2017-11',
                        'bang': bang,
                        'rank': item.span.get_text(),
                        'img': item.img.attrs['src'],
                        'name': item.h4.get_text(),
                        'info': item.p.get_text(),
                        'hsnum': item.find_all('td',{'class': 'hsnum'})[0].get_text().strip()
                    }
                    yield data


    def save(self,dt):
        save_sql = '''
                    INSERT INTO xyl__Xhulu_v2 
                        (plat,bang,nm,rank,hsnum,logDate,crawlTime,info,img) 
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');
                    '''.format(
                                dt['plat'],dt['bang'],dt['name'],dt['rank'],dt['hsnum'],dt['logDate'],
                                int(time.time()),dt['info'],dt['img']
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



if __name__ == '__main__':
    begin = time.time()
    xhl = Xhulu()
    saveNum = 0
    try:
        for data in xhl.get_data():
            print(data)
            saveNum += bg.save(data)
    finally:
        xhl.end()
        print('saveNum: ',saveNum)
        print('useTime: ', int(time.time()-begin))

    # ppt(bg.get_durTime())
    # ppt(bg.get_plat())
