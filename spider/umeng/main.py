#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urllib.request
import http.cookiejar 
import urllib.parse

#import pyquery
import re
import json

import datetime
import pymysql

import sys

class Umeng:
    def __init__(self,cookie=''): 
        #连接数据库
        # self.conn=pymysql.connect(host='localhost',user='root', passwd='7511',port=3306, db='qxiu_py')
        # self.cur = self.conn.cursor()
        # self.cur.execute('CREATE TABLE IF NOT EXISTS umeng ( \
        #         logtime date not null,  \
        #         term varchar(8) not null, \
        #         key_tag varchar(64) not null, \
        #         key_value double not null default 0, \
        #         primary key(logtime,term,key_tag)) ')
        # self.sql = "replace into umeng(logtime,term, key_tag, key_value) values(%s,%s, %s, %s)"
        #构造抓取所需参数
        self.stats={'new':'installations','ret':'retentions'} 
        self.appkeys={'ad':'5d2f30f8ccb04265d30e3b35','ios':'4b86b089ccb0426578bd4b35'}
        webCookie = http.cookiejar.CookieJar() # 初始化一个CookieJar来处理Cookie 
        self.openner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(webCookie)) 
        self.start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d") 
        self.end_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 
        
    def __getToken(self):
        #用于获取登录页面的token信息
        url='http://i.umeng.com/'
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'i.umeng.com',
            'Upgrade-Insecure-Requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
        }
        req=urllib.request.Request(url=url,headers=headers)
        html=self.openner.open(req).read().decode()
        matchObj = re.search(r'token: \'(\w+)\',',html,re.M|re.I|re.S)
        return(matchObj.group(1))

    def login(self):
        #用于登录
        token=self.__getToken()
        url='http://i.umeng.com/login/ajax_do'
        headers={
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive', 
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'i.umeng.com',
            'origin':'http://i.umeng.com',
            'referer':'http://i.umeng.com/',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
            'x-requested-with':'XMLHttpRequest'
        }
        datas={
            'token':token,
            'username':'qiqimobile@17guagua.com',
            'password':'QJkj2016fhiier',
            'sig':'',
            'sessionid':'',
            'website':'umengplus',
            'app_id':'',
            'url':''
        }
        data = urllib.parse.urlencode(datas).encode('utf-8')
        req=urllib.request.Request(url=url,data=data,headers=headers)
        response=self.openner.open(req)
        
    def getData(self,appkey,stat):
        #抓取数据
        url= 'http://mobile.umeng.com/apps/' + self.appkeys[appkey] \
        + '/reports/load_table_data?page=1&per_page=1000&start_date=' + self.start_date \
        + '&end_date=' + self.end_date \
        + '&versions%5B%5D=&channels%5B%5D=&segments%5B%5D=&time_unit=daily&stats=' + self.stats[stat]
        headers={
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'mobile.umeng.com',
            'Referer':'http://mobile.umeng.com/apps/5d2f30f8ccb04265d30e3b35/reports/installation',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
            }
        req=urllib.request.Request(url=url,headers=headers)#创建请求对象
        response=self.openner.open(req)
        page=response.read().decode()#获取页面源代码
        data=json.loads(page)
        logtime=self.end_date
        term=appkey
        value=0
        if data.get('result') == 'success':
            tag=stat
            if(stat=='new'):
                value=data.get('stats')[0]['data']
            elif(stat=='ret'):
                value=data.get('stats')[-1]['retention_rate'][0]/100
        return (logtime,term,tag,value)
        
    # def insertdatas(self,needprint=False):
    #     #将抓取的数据插入数据库
    #     insdata=[]
    #     for appkey in self.appkeys:
    #         for stat in self.stats:
    #             data=self.getData(appkey,stat)
    #             insdata.append(data)
    #             if needprint:
    #                 print(data)
    #     self.cur.executemany(self.sql,insdata)
    #     self.conn.commit()
    #
    def getdatas(self):
        #将抓取的数据展示出来
        for appkey in self.appkeys:
            for stat in self.stats:
                data=self.getData(appkey,stat)
                print(data)


u=Umeng()
u.login()
#u.insertdatas()

###################################################################################################


#-*- coding:utf-8 -*-

import re
import time
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import psycopg2

session = requests.Session()

host = 'http://i.umeng.com/'
login_url = 'https://i.umeng.com/login/ajax_do'
visit_url = 'http://mobile.umeng.com/apps/'


def get_header(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'i.umeng.com',
        'Upgrade-Insecure-Requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
    }
    res = session.get(url=url, headers=headers)
    html = res.text
    tk = re.search(r'token: (.*?),', html)
    apk = re.search(r'appkey: (.*?),', html)
    sid = re.search(r'sessionid: (.*?),', html)
    return {
            'token': tk.group(1),
            'appkey': apk.group(1),
            'sessionid': sid.group(1)
    }

print(session.cookies.get_dict())
print(get_header(host))

def login(host,login_url):
    form_data = {
        'token': get_header(host)['token'],
        'username': 'qiqimobile@17guagua.com',
        'password': 'QJkj2016fhiier',
        'sig': '',
        'sessionid': '', #get_header(host)['sessionid']
        'website': 'umengplus',
        'app_id': '', #get_header(host)['appkey']
        'url': ''
        }
    headers = {
        'accept':'*/*',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.8',
        'content-length':'111',
        'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
        'origin':'https://i.umeng.com',
        'referer':'https://i.umeng.com/?',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        'x-requested-with':'XMLHttpRequest'
        }
    res = session.post(login_url,data=urlencode(form_data),headers=headers)
    return res.text

print(login(host,login_url))
session.close()









params = {
    'token':'1e92418bd5d721bc8fd3cba55fafab94',
    'username':'qiqimobile@17guagua.com',
    'password':'QJkj2016fhiier',
    'sig':'',
    'sessionid':'',
    'website':'umengplus',
    'app_id':'',
    'url':''
    }





time.sleep(1)
s1 = session.post(login_url, data=params, headers=headers)
print(s1.cookies.get_dict())
print(s1)
time.sleep(0.7)
s2 = session.get(visit_url, headers=headers)
print(s2)
##print(s2.text)



