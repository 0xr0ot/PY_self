#coding:utf-8
#author:uliontse

import re
import time
import requests
import pymysql
from html import unescape
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


    def get_index_soup(self,keyword):
        param = {'ct':1, 'rn':20, 'ie':'utf-8', 'bs':keyword, 'rsv_bp':1,'sr':0, 'cl':2, 'f':8, 'prevct':'no',
                 'tn':'newstitle', 'word':keyword}
        res = requests.get(self.host,params=urlencode(param),headers=self.headers)
        soup = BeautifulSoup(res.text,'lxml')
        return soup


    def get_index_links(self,soup):
        data = soup.find_all('h3', {'class': 'c-title'})
        for dt in data:
            yield {
                'Title': dt.find_all('a')[0].get_text(),
                'Link': dt.find_all('a')[0].attrs['href']
            }


    def get_index_origin(self,soup):
        item = soup.find_all('div',{'class': 'c-title-author'})
        org_public = []
        org_date = []
        for it in item:
            org = it.get_text().split('\xa0\xa0') #space
            org_public.append(org[0])
            org_date.append(org[1])
        org_dic = {'public': org_public, 'date': org_date}
        return org_dic


    def get_html(self,link):
        res = requests.get(link,headers={'User-Agent':self.headers['User-Agent']})
        if 'charset="' in res.text:
            pattern = re.compile('charset="(.*?)"',re.S)
            res.encoding = re.findall(pattern,res.text)[0]
        elif ('charset=gb2312' or 'charset=GB2312') in res.text:
            res.encoding = 'gb2312'
        elif ('charset=GBK' or 'charset=gbk') in res.text:
            res.encoding = 'gbk'
        elif 'charset=cp936' in res.text:
            res.encoding = 'cp936'
        else:
            res.encoding = 'utf-8'
        html = res.text
        #print(html)
        return html


    def parse_choose(self,html):
        soup = BeautifulSoup(html, 'lxml')

        if ('id="main_content"' and 'ifengimg.com/ifeng/') in html:
            print('ifeng')
            contents = soup.find_all('div',{'id':'main_content'}) #凤凰网
            return contents[0].get_text()

        elif ('articleInfo: {' in html) and ('&gt;&lt' in html): #头条
            print('toutiao')
            pattern = re.compile("content: '(.*?)'")
            contents = re.findall(pattern,html)[0]
            normal_text = BeautifulSoup(unescape(contents),'lxml')
            return normal_text.get_text()

        elif 'id="js_content"' in html:
            print('weixin')
            contents = soup.find_all('div',{'id':'js_content'}) #微信文章
            return contents[0].get_text()

        elif 'id="artibody"' in html:
            print('sina')
            contents = soup.find_all('div',{"id":"artibody"}) #新浪
            return contents[0].get_text()

        elif ('class="article"' and 'sohu.com/tag/') in html:
            print('sohu')
            contents = soup.find_all('article',{'class':'article'}) #搜狐
            return contents[0].get_text()

        elif ('id=bd_article' and '360_' and 'class=content')in html:
            print('qihoo')
            contents = soup.find_all('article') # 今日爆点(360)
            return contents[0].get_text()

        elif 'id="endText"' in html:
            print('163NetEase')
            contents = soup.find_all('div',{'id':'endText'}) #网易
            return contents[0].get_text()

        elif ('id="content-text"' and 'btime.com') in html:
            print('btime')
            contents = soup.find_all('div',{'id':'content-text'}) #北京时间
            return contents[0].get_text()[:-40]

        elif ('id="article_content' and 'static.huxiucdn.com/www/') in html:
            print('huxiu')
            contents = soup.find_all('div',{'class':'article-content-wrap'}) #虎嗅网
            return contents[0].get_text()

        elif ('class="article-cont"' and 'news.zol.com.cn/more') in html:
            print('ZOL')
            contents =soup.find_all('div',{'class':'article-cont'}) #中关村在线
            return contents[0].get_text()[:-200].replace('\xa0','')

        elif 'id="contentMain"' in html:
            print('gmw')
            contents = soup.find_all('div',{'id':'contentMain'}) #光明网
            return contents[0].get_text()

        elif 'id="content"' in html:
            print('southcn or ITBEAR')
            contents = soup.find_all('div',{'id':'content'}) #南方网、ITBEAR
            return contents[0].get_text()

        elif 'class="news-con"' in html:
            print('dzwww')
            contents = soup.find_all('div',{'class':'news-con'}) #大众网
            return contents[0].get_text()
        else:
            return ''


    def get_content(self,contents):
        para = contents
        return {
            'length': len(para.replace(' ', '')),
            'content': para
        }


def run():
    news = BaiduNews()
    #soup = news.get_index_soup('陌陌')
    html = news.get_html(link15)
    contents = news.parse_choose(html)
    aa = news.get_content(contents)
    print(aa)




if __name__ == '__main__':
    #print(news.get_index_origin(soup))
    # for dt in news.get_index_links(soup):
    #     print(dt)
    link1 = 'http://e.gmw.cn/2017-11/16/content_26806647.htm' #光明网
    link2 = 'http://tech.ifeng.com/a/20171115/44761603_0.shtml' #凤凰网
    link3 = 'http://news.sina.com.cn/o/2017-07-25/doc-ifyihrwk2265523.shtml' #新浪
    link4 = 'http://www.sohu.com/a/203545097_115980' #搜狐
    link5 = 'http://ent.southcn.com/8/2017-11/10/content_178757607.htm' #南方网
    link6 = 'http://www.itbear.com.cn/html/2017-11/244423.html' #ITBEAR
    link7 = 'http://www.dzwww.com/yule/zy/201711/t20171109_16633719.htm' #大众网
    link8 = 'http://tech.163.com/17/1117/13/D3ER9D5E00099504.html' #NetEase
    link9 = 'https://www.toutiao.com/a6489226045797958158/' #toutiao
    link10= 'https://mp.weixin.qq.com/s?__biz=MjM5MDI1ODUyMA==&mid=2672939627&idx=1&sn=14d587f0ccf8bf459406e3de1b189504&' \
            'chksm=bce2f65c8b957f4a72acbccb0cba549898bb39a582a67265df5b502823e3a87e1fcb8202ca11&mpshare=1&scene=1&' \
            'srcid=1117YeA0NLTDwKLvHM9kcnmQ&pass_ticket=W%2FN7x5QMxuwmbIEiD9OZsm%2BZ0U181Ugx3dgWlUW1OEJiHDVyRt5%2F8L4tbKWACFja#rd' #weixin
    link11= 'http://sh.qihoo.com/pc/detail?360newsdetail=1&_sign=searchdet&check=36788aab903e770a&sign=360_e39369d1&' \
            'url=http://www.yulefm.com/news/2017-10-31/145085.html' # 今日爆点(360)
    link12= 'https://item.btime.com/wm/427iajh3vuq8goruch18qschtuo' #北京时间
    link13= 'https://www.huxiu.com/article/222579.html' # 虎嗅网
    link14= 'http://news.zol.com.cn/659/6590172.html' # 中关村在线
    link15= 'http://news.zol.com.cn/666/6661050.html'

    run()
