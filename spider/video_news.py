#coding:utf-8
#author:uliontse

import re
import time
import requests
import pymysql
from html import unescape
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from pprint import pprint as ppt


class VideoNews:
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
            'Referer': 'http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs=intitle%3A%28%E9%99%8C%E9%99%8C%29&rsv_bp=1'
                       '&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E9%99%8C%E9%99%8C',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cookie': 'BAIDUID=9C7D1834BF0ADA92C4F080B41C5E873E:FG=1; PSTM={0}; BIDUPSID=BE2B0CF40FCC2740442B2882F395DD5C; '
                      'LOCALGX=%u5317%u4EAC%7C%30%7C%u5317%u4EAC%7C%30; Hm_lvt_e9e114d958ea263de46e080563e254c4={1},{2}; '
                      'Hm_lpvt_e9e114d958ea263de46e080563e254c4={3}; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; '
                      'BDRCVFR[C0p6oIjvx-c]=mk3SLVN4HKm; WWW_ST={4}; BDRCVFR[uLXjBGr0i56]=mbxnW11j9Dfmh7GuZR8mvqV; '
                      'BD_CK_SAM=1; PSINO=1; BDSVRTM=143; H_PS_PSSID='.format(self.tm1-82207,self.tm1-81353,self.tm1-798,self.tm1-798,self.tm0)
        }
        #TODO
        # self.conn = pymysql.connect(host='123.59.20.50',port=33066,user='qxiu_user',password='c9Lmb6Wu29RGX!c',
        #                             database='qxiu_bi2',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        # self.cur = self.conn.cursor()
        # self.create_sql = '''
        #                                 CREATE TABLE IF NOT EXISTS xyl__VideoNews
        #                         (
        #                               keyId VARCHAR(32) NOT NULL PRIMARY KEY
        #                             , crawlTime VARCHAR(16) NOT NULL
        #                         );'''
        # self.cur.execute(self.create_sql)

    # def save_end(self):
    #     self.cur.close()
    #     self.conn.close()


    def get_baidu_soup(self,keyword,page=0):
        if page == 0:
            # 'ct'=0: TimeOrder, 'ct'=1: FocusOrder; 'tn'='news' or 'newstitle'.
            param = {'ct':0, 'rn':20, 'ie':'utf-8', 'cl':2, 'tn':'newstitle', 'word':keyword, 'bs':keyword, 'rsv_bp':1,'sr':0, 'f':8, 'prevct':'no',}
        else:
            pageN = 20 * page
            param = {'ct':0, 'rn':20, 'ie':'utf-8', 'cl':2, 'tn':'newstitle', 'word':'intitle:('+keyword+')', 'bt':0, 'et':0, 'pn':pageN}
        res = requests.get(self.host,params=urlencode(param),headers=self.headers)
        soup = BeautifulSoup(res.text,'lxml')
        return soup


    def get_baidu_links(self,soup):
        data = soup.find_all('h3', {'class': 'c-title'})
        tt_pool, lk_pool = [],[]
        for dt in data:
            tt_pool.append(dt.find_all('a')[0].get_text())
            lk_pool.append(dt.find_all('a')[0].attrs['href'])
        return {'title': tt_pool, 'link': lk_pool}


    def get_baidu_origin(self,soup):
        item = soup.find_all('div',{'class': 'c-title-author'})
        org_public,org_date = [],[]
        for it in item:
            org = it.get_text().split('\xa0\xa0') #space
            org_public.append(org[0])
            org_date.append(org[1])
        org_dic = {'public': org_public, 'date': org_date}
        return org_dic


    def get_html(self,link):
        res = requests.get(link,headers={'User-Agent':self.headers['User-Agent']})
        if ' charset="' in res.text: #space
            pattern = re.compile('charset="(.*?)"',re.S)
            res.encoding = re.findall(pattern,res.text)[0]
        elif ('charset=utf-8' or 'charset=UTF-8') in res.text:
            res.encoding = 'utf-8'
        elif ('charset=gb2312' or 'charset=GB2312') in res.text:
            res.encoding = 'gb2312'
        elif (('charset=GBK' or 'charset=gbk') in res.text) or res.encoding=='ISO-8859-1':
            res.encoding = 'GBK'
        elif 'charset=cp936' in res.text:
            res.encoding = 'cp936'
        else:
            res.encoding = res.encoding
        print(res.encoding)
        html = res.text
        #print(html)
        return html


    def get_content(self,html):
        soup = BeautifulSoup(html, 'lxml')

        if ('id="main_content"' and 'ifengimg.com/ifeng/') in html:
            print('--ifeng--')
            contents = soup.find_all('div',{'id':'main_content'}) #凤凰网
            return contents[0].get_text()

        elif ('articleInfo: {' and 'www.toutiao.com/complain/') in html: #头条
            print('--toutiao--')
            pattern = re.compile("content: '(.*?)'")
            contents = re.findall(pattern,html)[0]
            normal_text = BeautifulSoup(unescape(contents),'lxml')
            return normal_text.get_text()

        elif ('id="js_content"' and 'res.wx.qq.com/mmbizwap/zh_CN') in html:
            print('--weixin--')
            contents = soup.find_all('div',{'id':'js_content'}) #微信公众号
            #print(contents)
            return contents[0].get_text()

        elif ('id="artibody"' and 'www.sina.com.cn') in html:
            print('--sina--')
            contents = soup.find_all('div',{"id":"artibody"}) #新浪
            return contents[0].get_text()

        elif ('class="article"' and 'sohu.com/tag/') in html:
            print('--sohu--')
            contents = soup.find_all('article',{'class':'article'}) #搜狐
            return contents[0].get_text()

        elif ('class="content"' and 'http://static.bjnews.com.cn/www/') in html:
            print('--bjnews--')
            contents = soup.find_all('div',{'class':'content'}) #新京报
            return contents[0].get_text()

        elif ('id=bd_article' and 'http://kc.look.360.cn')in html:
            print('--qihoo--')
            contents = soup.find_all('article') # 今日爆点(360)
            return contents[0].get_text()

        elif ('id="endText"' and 'http://help.163.com/') in html:
            print('--163NetEase--')
            contents = soup.find_all('div',{'id':'endText'}) #网易
            return contents[0].get_text()

        elif ('id="content-text"' and 'btime.com') in html:
            print('--btime--')
            contents = soup.find_all('div',{'id':'content-text'}) #北京时间
            return contents[0].get_text()[:-40]

        elif ('class="content"' and 'http://new.xiaohulu.com/') in html:
            print('--xiaohulu--')
            para = ''
            contents = soup.find_all('div',{'class':'content'}) #小葫芦
            for content in contents[0].find_all('p'):
                para += content.get_text()
            return para

        elif ('id="article_content' and 'static.huxiucdn.com/www/') in html:
            print('--huxiu--')
            contents = soup.find_all('div',{'class':'article-content-wrap'}) #虎嗅网
            return contents[0].get_text()

        elif ('class="article-cont"' and 'news.zol.com.cn/more') in html:
            print('--ZOL--')
            contents =soup.find_all('div',{'class':'article-cont'}) #中关村在线
            return contents[0].get_text()[:-200].replace('\xa0','')

        elif ('id="contentMain"' and 'http://en.gmw.cn/') in html:
            print('--gmw--')
            contents = soup.find_all('div',{'id':'contentMain'}) #光明网
            return contents[0].get_text()

        elif ('class="news-con"' and 'http://www.dzwww.com/map/') in html:
            print('--dzwww--')
            contents = soup.find_all('div',{'class':'news-con'}) #大众网
            return contents[0].get_text()

        elif ('id="content"' or 'http://m.itbear.com.cn' or 'http://www.newsgd.com/') in html:
            print('--southcn or ITBEAR--')
            contents = soup.find_all('div',{'id':'content'}) #南方网、ITBEAR
            return contents[0].get_text()
        #TODO
        else:
            print('--Unknown--')
            return ''


def run(keyword,page):
    news = VideoNews()
    soup = news.get_baidu_soup(keyword,page)
    link_dic = news.get_baidu_links(soup)
    org_dic = news.get_baidu_origin(soup)
    #ppt(link_dic)
    #ppt(org_dic)

    con_pool,len_pool = [],[]
    for link in link_dic['link']:
        html = news.get_html(link)
        para = news.get_content(html).strip()
        con_pool.append(para)
        len_pool.append(len(para.replace('\n','').replace(' ','')))
    cont_dic = {'content':con_pool, 'length':len_pool}
    #ppt(cont_dic)
    link_dic.update(org_dic)
    link_dic.update(cont_dic)
    return link_dic


#TODO

if __name__ == '__main__':
    zb = run('直播行业',0)
    for zz in zb.values():
        ppt(zz[0])


    # link1 = 'http://e.gmw.cn/2017-11/16/content_26806647.htm' #光明网
    # link2 = 'http://tech.ifeng.com/a/20171115/44761603_0.shtml' #凤凰网
    # link3 = 'http://news.sina.com.cn/o/2017-07-25/doc-ifyihrwk2265523.shtml' #新浪
    # link4 = 'http://www.sohu.com/a/203545097_115980' #搜狐
    # link5 = 'http://ent.southcn.com/8/2017-11/10/content_178757607.htm' #南方网
    # link6 = 'http://www.itbear.com.cn/html/2017-11/244423.html' #ITBEAR
    # link7 = 'http://www.dzwww.com/yule/zy/201711/t20171109_16633719.htm' #大众网
    # link8 = 'http://tech.163.com/17/1117/13/D3ER9D5E00099504.html' #NetEase
    # link9 = 'https://www.toutiao.com/a6489226045797958158/' #toutiao
    # link10= 'https://mp.weixin.qq.com/s?__biz=MjM5MDI1ODUyMA==&mid=2672939627&idx=1&sn=14d587f0ccf8bf459406e3de1b189504&' \
    #         'chksm=bce2f65c8b957f4a72acbccb0cba549898bb39a582a67265df5b502823e3a87e1fcb8202ca11&mpshare=1&scene=1&' \
    #         'srcid=1117YeA0NLTDwKLvHM9kcnmQ&pass_ticket=W%2FN7x5QMxuwmbIEiD9OZsm%2BZ0U181Ugx3dgWlUW1OEJiHDVyRt5%2F8L4tbKWACFja#rd' #weixin
    # link11= 'http://sh.qihoo.com/pc/detail?360newsdetail=1&_sign=searchdet&check=36788aab903e770a&sign=360_e39369d1&' \
    #         'url=http://www.yulefm.com/news/2017-10-31/145085.html' # 今日爆点(360)
    # link12= 'https://item.btime.com/wm/427iajh3vuq8goruch18qschtuo' #北京时间
    # link13= 'https://www.huxiu.com/article/222579.html' # 虎嗅网
    # link14= 'http://news.zol.com.cn/659/6590172.html' # 中关村在线
    # link15= 'http://new.xiaohulu.com/daily/2017/11/171633.shtml' #小葫芦
    # link16= 'https://news.qq.com/a/20170823/001218.htm' #腾讯新闻
    # link17= 'http://www.bjnews.com.cn/ent/2017/11/21/465153.html' #新京报
