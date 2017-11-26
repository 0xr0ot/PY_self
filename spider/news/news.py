# coding:utf-8
# author:uliontse

import re
import time
import random
import pymysql
import requests
import jieba.analyse
from html import unescape
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from pprint import pprint as ppt
from .config import *


class News:
    def __init__(self):
        self.host = 'http://news.baidu.com/ns?'
        self.tm = time.time()
        self.tm0 = int(self.tm * 1000)
        self.tm1 = int(self.tm)
        self.headers = {
            'Host': 'news.baidu.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs=intitle%3A%28%E9%99%8C%E9%99%8C%29&rsv_bp=1'
                       '&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E9%99%8C%E9%99%8C',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cookie': 'BAIDUID=9C7D1834BF0ADA92C4F080B41C5E873E:FG=1; PSTM={0}; BIDUPSID=BE2B0CF40FCC2740442B2882F395DD5C; '
                      'LOCALGX=%u5317%u4EAC%7C%30%7C%u5317%u4EAC%7C%30; Hm_lvt_e9e114d958ea263de46e080563e254c4={1},{2}; '
                      'Hm_lpvt_e9e114d958ea263de46e080563e254c4={3}; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; '
                      'BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; WWW_ST={4}; BDRCVFR[uLXjBGr0i56]=mbxnW11j9Dfmh7GuZR8mvqV; '
                      'BD_CK_SAM=1; PSINO=1; BDSVRTM=143; H_PS_PSSID='.format(self.tm1 - 82207, self.tm1 - 81353,
                                                                              self.tm1 - 798, self.tm1 - 798, self.tm0)
        }
        # self.conn = pymysql.connect(host='xxxx',
        #                             port=33066,
        #                             user='xxxx',
        #                             password='xxxx',
        #                             database='xxxx',
        #                             charset='utf8mb4',
        #                             cursorclass=pymysql.cursors.DictCursor)
        # self.cur = self.conn.cursor()
        # self.create_sql = '''
        #                     CREATE TABLE IF NOT EXISTS qxiu_bi2.xyl__VideoNews_v1
        #                         (
        #                               title VARCHAR(64) NOT NULL PRIMARY KEY
        #                             , crawlTime INT(10) NOT NULL
        #                             , keyword VARCHAR(8) NOT NULL
        #                             , length INT(4) NOT NULL
        #                             , publish VARCHAR(32) NOT NULL
        #                             , pubDate VARCHAR(32) NOT NULL
        #                             , word_TF VARCHAR(64) NULL
        #                             , word_RANK VARCHAR(64) NULL
        #                             , emotion VARCHAR(8) NULL
        #                             , image VARCHAR(256) NULL
        #                             , video VARCHAR(64) NULL
        #                             , link VARCHAR(256) NOT NULL
        #                             , content TEXT NULL
        #                         );'''
        # self.cur.execute(self.create_sql)
        self.web = '<!DOCTYPE HTML><html><head><title></title></head><body> </body></html>'

    def get_baidu(self, keyword, page=0):
        if page == 0:
            # 'ct'=0: TimeOrder, 'ct'=1: FocusOrder; 'tn'='news' or 'newstitle'.
            param = {'ct': 0, 'rn': 20, 'ie': 'utf-8', 'cl': 2, 'tn': 'newstitle', 'word': keyword, 'bs': keyword,
                     'rsv_bp': 1, 'sr': 0, 'f': 8, 'prevct': 'no'}
        else:
            pageN = 20 * page
            param = {'ct': 0, 'rn': 20, 'ie': 'utf-8', 'cl': 2, 'tn': 'newstitle', 'word': 'intitle:(' + keyword + ')',
                     'bt': 0, 'et': 0, 'pn': pageN}
        res = requests.get(self.host, params=urlencode(param), headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')

        # get `title`,`link`.
        data = soup.find_all('h3', {'class': 'c-title'})
        tt_pool, lk_pool = [], []
        for dt in data:
            tt_pool.append(dt.find_all('a')[0].get_text())
            lk_pool.append(dt.find_all('a')[0].attrs['href'])

        # get `publish`,`pubDate`.
        item = soup.find_all('div', {'class': 'c-title-author'})
        org_publish, org_date = [], []
        for it in item:
            org = it.get_text().split('\xa0\xa0')  # space
            org_publish.append(org[0])
            org_date.append(org[1])
        dic = {'publish': org_publish, 'pubDate': org_date,'title': tt_pool, 'link': lk_pool}
        return dic

    def judge(self,only, html):
        if isinstance(only, list):
            for x in only:
                if x in html:
                    return True
            return False
        if only in html:
            return True

    def encode_bug(self,res):
        if res.encoding == 'ISO-8859-1':
            if 'charset="' in res.text:
                pattern = re.compile('charset="(.*?)"', re.S)
                res.encoding = re.findall(pattern, res.text)[0]
                return res.encoding
            elif (('charset=utf-8' in res.text) or ('charset=UTF-8' in res.text)):
                return 'utf-8'
            elif (('charset=gb2312' in res.text) or ('charset=GB2312' in res.text)):
                return 'gb2312'
            elif (('charset=GBK' in res.text) or ('charset=gbk' in res.text)):
                return 'GBK'
            elif (('charset=cp936' in res.text) or ('charset=CP936' in res.text)):
                return 'cp936'
            else:
                return 'utf-8'

    def get_content(self, link):
        time.sleep(0.7)
        UA = ['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11',
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5']
        UA.append(self.headers['User-Agent'])
        try:
            global res
            res = requests.get(link, headers={'User-Agent': random.choice(UA)})
            res.encoding = self.encode_bug(res)
            html = res.text
        except:
            html = self.web
        soup = BeautifulSoup(html, 'lxml')
        for parser in PARSE_POOL.keys():
            if (parser == 'articleInfo: {' and self.judge(PARSE_POOL[parser]['only'], html)):
                pattern = re.compile("content: '(.*?)'")
                contents = re.findall(pattern, html)[0]
                para = BeautifulSoup(unescape(contents), 'lxml').get_text()
                dic = {
                    'parser': PARSE_POOL[parser]['who'],
                    'encoding': res.encoding,
                    'para': para,
                    'length': len(para.replace('\n', '').replace(' ', ''))
                }
                return dic

            elif (parser == 'article') and (parser in html) and self.judge(PARSE_POOL[parser]['only'], html):
                contents = soup.find_all('article')
                para = contents[0].get_text()
                dic = {
                    'parser': PARSE_POOL[parser]['who'],
                    'encoding': res.encoding,
                    'para': para,
                    'length': len(para.replace('\n', '').replace(' ', ''))
                }
                return dic

            elif (parser in html) and (parser != 'article') and (parser != 'articleInfo: {') and self.judge(PARSE_POOL[parser]['only'], html):
                kk, vv = parser.split('=')[0], parser.split('=')[1][1:-1]
                if ' ' in vv:
                    vv = vv.split(' ')[PARSE_POOL[parser]['space']]
                if PARSE_POOL[parser].get('div'):
                    contents = soup.find_all(PARSE_POOL[parser]['div'], {kk: vv})
                else:
                    contents = soup.find_all('div', {kk: vv})
                if PARSE_POOL[parser].get('p'):
                    para = contents[0].get_text()
                else:
                    para = ''
                    for content in contents[0].find_all('p'):
                        para += content.get_text()
                para = para.replace('\u3000\u3000', '\n').replace('\xa0', '').replace('\t', '').replace('\r\n','\n')
                para = para.replace('\n\n', '\n').replace('\n \n', '\n').replace('   ', '').replace('\t\n', '')
                dic = {
                    'parser': PARSE_POOL[parser]['who'],
                    'encoding': res.encoding,
                    'para': para,
                    'length': len(para.replace('\n', '').replace(' ', ''))
                }
                return dic
        dic = {
            'parser': 'Unknown',
            'encoding': res.encoding,
            'para': '',
            'length': 0
        }
        return dic


    def gene_data(self, keyword, page):
        dic = self.get_baidu(keyword, page)
        con_pool, len_pool = [], []
        parse_pool,encode_pool = [],[]
        for link in dic['link']:
            para_dic = self.get_content(link)
            para = para_dic['para'].strip()
            con_pool.append(para)
            len_pool.append(para_dic['length'])
            parse_pool.append(para_dic['parser'])
            encode_pool.append(para_dic['encoding'])

        cont_dic = {'content': con_pool, 'length': len_pool, 'parser':parse_pool, 'encoding':encode_pool}
        dic.update(cont_dic)

        for i, j in enumerate(dic['link']):
            data = {
                'keyword': keyword,
                'title': dic['title'][i],
                'link': dic['link'][i],
                'pubDate': dic['pubDate'][i],
                'publish': dic['publish'][i],
                'length': dic['length'][i],
                'content': dic['content'][i],
                'parser': dic['parser'][i],
                'encoding': dic['encoding'][i]
            }
            yield data

    def save_data(self, dt):
        save_sql = '''
                    INSERT INTO qxiu_bi2.xyl__VideoNews_v1 
                        (title,crawlTime,keyword,length,publish,pubDate,word_TF,word_RANK,emotion,image,video,link,content) 
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}');
                    '''.format(
            dt['title'], int(time.time()), dt['keyword'], dt['length'], dt['publish'], dt['pubDate'], '', '', '', '','',
            dt['link'], dt['content']
        )
        try:
            self.cur.execute(save_sql)
            self.conn.commit()
        except pymysql.IntegrityError as e:
            print(e)
        return 'Save successfully!\r\n {0}'.format(dt)

    def save_end(self):
        self.cur.close()
        self.conn.close()

    # TODO nlp
    def ext(sentence, method='TF-IDF'):
        if method == 'TF-IDF':
            result = jieba.analyse.extract_tags(sentence, topK=10, allowPOS=('ns', 'n', 'vn', 'v'))
            return result
        if method == 'TextRank':
            result = jieba.analyse.textrank(sentence, topK=10, allowPOS=('ns', 'n', 'vn', 'v'))
            return result


if __name__ == '__main__':
    items = ['直播行业', '小视频', '短视频', '网红 直播', '小米直播', '全民直播', '陌陌', '映客', '花椒直播', '奇秀直播', '一直播', 'NOW直播',
             '六间房直播', '来疯', '千帆直播', '我秀直播', '繁星直播', '网易cc直播', '网易BoBo直播', '网易薄荷直播', '花样直播',
             'YY直播', 'live直播', 'vlive直播', 'KK直播', '梦想直播', '聚星直播', '新浪秀场','豆豆Live','人人直播',
             '美拍', '快手', '火山小视频', '抖音', '淘宝直播', '梨视频', '开眼视频', '秒拍', '映兔视频', 'V电影', '魔力盒',
             '快视频', '西瓜视频',
             '熊猫直播', '斗鱼直播', '虎牙直播', '企鹅直播', '企鹅电竞', '熊猫直播', '战旗直播', '狮吼直播', '触手直播', '龙珠直播']
    # 抱抱直播、嗨秀秀场、乐嗨秀场、么么直播、bilibili直播、九秀直播、

    news = News()
    try:
        for item in items:
            print(item * 10)
            data = news.gene_data(item, 0)
            for dt in data:
                ppt(dt)
                if (('怎么用' or '好用吗' or '直播：') in dt['title']) or dt['length']<500:
                    pass
                else:
                    #news.save_data(dt)
                    print('Saved!')
    finally:
        news.save_end()
