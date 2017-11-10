#coding:utf-8
#author:uliontse

import time
import requests
from bs4 import BeautifulSoup
import pymysql
from pprint import pprint as ppt


class Begin:
    def __init__(self):
        self.header = dict()
        self.tm = int(time.time())
        self.target_url = 'http://www.xiaohulu.com/Anchor/index.html'
        self.header['Host'] = 'www.xiaohulu.com'
        self.header['Refer'] = 'http://www.xiaohulu.com/'
        self.header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        self.header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        self.header['Accept-Encoding'] = 'gzip, deflate, sdch'
        self.header['Cookie'] = 'PHPSESSID=mmm760v9otil1qm4st72daj7s6; Hm_lvt_2772005b8bc0b193d080228322981977={0},{1}; ' \
                    'Hm_lpvt_2772005b8bc0b193d080228322981977={2}; Hm_lvt_1c358b33dfa30c89dd3a1927a5921793={3},' \
                    '{4}; Hm_lpvt_1c358b33dfa30c89dd3a1927a5921793={5}'.format(
                    self.tm-153427,self.tm-2376,self.tm-1,self.tm-153427,self.tm-2377,self.tm)

        self.ss = requests.Session()
        self.ss.headers.update(self.header)
        self.res = self.ss.get(self.target_url)
        self.soup = BeautifulSoup(self.res.text,'lxml')


    def end(self):
        self.ss.close()
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
            plat_pool[plat.get_text().strip().replace(r'\r\n','')] = plat.attrs['value']
        return plat_pool




if __name__ == '__main__':
    bg = Begin()
    #ppt(bg.get_durTime())
    ppt(bg.get_plat())
