#coding:utf-8

import requests
from bs4 import BeautifulSoup
from pprint import pprint as ppt

class XTHW:

    def __init__(self):
        self.url = 'http://bjxthw.360jlb.cn/m/rest/event/applier/list?activityId=77821&'
        self.gender_url = 'http://bjxthw.360jlb.cn/m/user?'
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)'}
        self.ss = requests.session()

    def get_list(self,offset):
        self.ss.headers.update(self.headers)
        res = self.ss.get(self.url + 'page=1&offset={}'.format(offset),headers=self.headers)
        return res.json()

    def get_gender(self,id):
        res =self.ss.get(self.gender_url + 'id={}'.format(id))
        soup = BeautifulSoup(res.text,'lxml')
        gender = soup.find('span', {'class': ['sex f28']})
        return gender.get_text()




if __name__ == '__main__':
    gender_list = []
    xthw = XTHW()

    for offset in [0,20]:
        data = xthw.get_list(offset)
        ppt(data)

        for dt in data['result']['list']:
            gender = xthw.get_gender(dt['id'])
            gender_list.append(gender)

    print(gender_list)
    print(len(gender_list))

    cnt = 0
    for i in gender_list:
        if i == '女':
            cnt +=1

    print(cnt)

    #ppt(data)
