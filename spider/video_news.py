#coding:utf-8
#author:uliontse

import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

class BaiduNews:
    def __init__(self):
        self.host = 'http://news.baidu.com/ns?'
        self.tm = time.time()
        self.tm0 = int(self.tm*1000)
        self.tm1 = int(self.tm)
        self.headers = {
            'Host': 'news.baidu.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs=intitle%3A%28%E9%99%8C%E9%99%8C%29&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E9%99%8C%E9%99%8C',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cookie': 'BAIDUID=9C7D1834BF0ADA92C4F080B41C5E873E:FG=1; PSTM={0}; BIDUPSID=BE2B0CF40FCC2740442B2882F395DD5C; '
                      'LOCALGX=%u5317%u4EAC%7C%30%7C%u5317%u4EAC%7C%30; Hm_lvt_e9e114d958ea263de46e080563e254c4={1},{2}; '
                      'Hm_lpvt_e9e114d958ea263de46e080563e254c4={3}; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; '
                      'BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; WWW_ST={4}; BDRCVFR[uLXjBGr0i56]=mbxnW11j9Dfmh7GuZR8mvqV; '
                      'BD_CK_SAM=1; PSINO=1; BDSVRTM=143; H_PS_PSSID='.format(self.tm1-82207,self.tm1-81353,self.tm1-798,self.tm1-798,self.tm0)
        }

    def get_soup(self,keyword):
        param = {
            'ct':1,
            'rn':20,
            'ie':'utf-8',
            'bs':keyword,
            'rsv_bp':1,
            'sr':0,
            'cl':2,
            'f':8,
            'prevct':'no',
            'tn':'newstitle',
            'word':keyword
        }
        res = requests.get(self.host,params=urlencode(param),headers=self.headers)
        soup = BeautifulSoup(res.text,'lxml')
        return soup


    def get_links(self,soup):
        data = soup.find_all('h3', {'class': 'c-title'})
        for dt in data:
            yield {
                'Title': dt.find_all('a')[0].get_text(),
                'Link': dt.find_all('a')[0].attrs['href']
            }


    def get_origin(self,soup):
        item = soup.find_all('div',{'class': 'c-title-author'})
        org_public = []
        org_date = []
        for it in item:
            org = it.get_text().split('\xa0\xa0')
            org_public.append(org[0])
            org_date.append(org[1])
        org_dic = {'public': org_public, 'date': org_date}
        return org_dic

    def get_content(self,link):
        res = requests.get(link)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,'lxml')
        if 'id="main_content"' in res.text:
            contents = soup.find_all('div',{'id':'main_content'}) #凤凰网
        elif 'id="contentMain"' in res.text:
            contents = soup.find_all('div',{'id':'contentMain'}) #光明网
        else:
            return
        para = ''
        for content in contents[0].find_all('p'):
            para = para + '\n' +content.get_text()
        return {
            'content': para,
            'length': len(para.replace(' ',''))
        }




if __name__ == '__main__':
    news = BaiduNews()
    soup = news.get_soup('陌陌')
    #print(news.get_origin(soup))
    # for dt in news.get_links(soup):
    #     print(dt)
    link1 = 'http://e.gmw.cn/2017-11/16/content_26806647.htm'
    link2 = 'http://tech.ifeng.com/a/20171115/44761603_0.shtml'
    aa = news.get_content(link2)
    print(aa)
