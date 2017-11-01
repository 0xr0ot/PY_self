#coding:utf-8

import os
import time
import json
import requests
import certifi
import pymysql
from hashlib import md5


class HuoShan:
    def __init__(self):
        self.host = 'https://www.huoshan.com/share/hot_videos/?'
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)'}
        self.pool = set()

    def get_data(self, offset=0, count=400):
        url = self.host + 'offset={0}&count={1}'.format(offset, count)
        res = requests.get(url, headers=self.headers, verify=certifi.where())
        data = res.json()
        for dt in data['data']:
            if dt['video']['url_list'][0] not in self.pool:
                self.pool.add(dt['video']['url_list'][0])
                if dt['author']['gender'] == 1:
                    gender = 'Male'
                elif dt['author']['gender'] == 2:
                    gender = 'Female'
                else:
                    gender = 'Unknown'
                yield {
                    'key_id': 'HS_'+str(dt['create_time'] *1000)+'_'+dt['author']['id_str'],
                    'platform' : 'Huoshan',
                    'nickname': dt['author']['nickname'],
                    'author_id': dt['author']['id_str'],
                    'gender': gender,
                    'charm': dt['author']['fan_ticket_count'],
                    'level': dt['author']['level'],
                    'signature': dt['author']['signature'],
                    'city': dt['author']['city'],
                    'location': dt['location'],
                    'video_title': dt['text'],
                    'duration': dt['video']['duration'],
                    'video_height': dt['video']['height'],
                    'video_width': dt['video']['width'],
                    'avatar_large': dt['author']['avatar_large']['url_list'][0],
                    'avatar_medium': dt['author']['avatar_medium']['url_list'][0],
                    'avatar_thumb': dt['author']['avatar_thumb']['url_list'][0],
                    'video_cover': dt['video']['cover']['url_list'][0],
                    'video_url': 'http://hotsoon.snssdk.com/hotsoon/item/video/_playback/?video_id={}&line=0'
                                 '&watermark=0&app_id=1112'.format(dt['video']['uri']),
                    'video_ctime': str(dt['create_time'] * 1000),
                    'crawl_time': str(int(time.time()*1000))
                }


class KuaiShou:
    def __init__(self):
        self.url = 'http://api.gifshow.com/rest/n/feed/hot?mod=LeMobile(Le%20X820)&lon=116.306112&country_code=CN' \
                   '&did=ANDROID_38a52b90ecd7b381&app=0&net=WIFI&oc=LETV&ud=700775043&c=LETV&sys=ANDROID_6.0.1' \
                   '&appver=5.3.3.5055&ftt=&language=zh-cn&iuid=&lat=39.977848&ver=5.3'
        self.headers = {
            'X-REQUESTID': '726472818',
            'User-Agent': 'kwai-android',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-cn',
            'Host': 'api.gifshow.com',
            'Accept-Encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        self.param_data = {
            'type': 7,
            'page': 1,
            'coldStart': 'true',
            'count': 20,
            'pv': 'false',
            'id': 49,
            'refreshTimes': 0,
            'pcursor': '',
            '__NStokensig': '939307b1facd7f367a4a470d40da980185b236886cd2cf8fdd67b97e593e10d3',
            'token': '5107308e59704cc29ff6d9963eebb295-700775043',
            'client_key': '3c2cd3f3',
            'os': 'android',
            'sig': 'c613c8bccf6956cf295f0ba3fc6f24dd'
        }

    def get_data(self):
        res = requests.post(self.url, headers=self.headers, data=self.param_data)
        data = res.json()
        for dt in data['feeds']:
            if dt.get('main_mv_urls'):
                if dt['user_sex'] == 'F':
                    gender = 'Female'
                elif dt['user_sex'] == 'M':
                    gender = 'Male'
                else:
                    gender = 'Unknown'
                yield {
                    'key_id': 'KS_'+str(dt['timestamp'])+'_'+str(dt['user_id']),
                    'platform': 'Kuaishou',
                    'nickname': dt['user_name'],
                    'author_id': str(dt['user_id']),
                    'gender': gender,
                    'charm': dt['like_count'],
                    'level': '',
                    'signature': '',
                    'city': '',
                    'location': '',
                    'video_title': dt['caption'],
                    'duration': '',
                    'video_height': dt['ext_params']['h'],
                    'video_width': dt['ext_params']['w'],
                    'avatar_large': '',
                    'avatar_medium': dt['headurls'][0]['url'],
                    'avatar_thumb': '',
                    'video_cover': dt['cover_thumbnail_urls'][0]['url'],
                    'video_url': dt['main_mv_urls'][0]['url'],
                    'video_ctime': str(dt['timestamp']),
                    'crawl_time': str(int(time.time() *1000))
                }


class Inke:
    def __init__(self):
        self.url = 'http://116.211.167.106/api/feeds_tab/recommends?cc=TG36001&lc=3ef688bc40198108&mtxid=d0ee0728222e&devi=862177031894002&sid=20MCQVnazERp6Yi2qe5usEeRgCAqmni19dG9c9sMqkm0AIIqjOWF&osversion=android_23&cv=IK5.0.10_Android&imei=862177031894002&proto=7&conn=wifi&ua=LeMobileLeX820&logid=262%2C269%2C209%2C234%2C236&uid=603554151&icc=&vv=1.0.3-201610121413.android&aid=38a52b90ecd7b381&smid=DudQ1IMizexZyWmy%2BHaN%2FKqGra2unALU9UUbCI11dLHyfwsb32iUYsUO4FsHQCAYpC2hYmV1CccKe9E375uhA9yQ&imsi=&mtid=bdba779f457452c613f93fa8060d46e8&latitude=200&video_topic_disable=0&start=10&longitude=200&limit=30'
        self.headers = {
            'Host': '116.211.167.106',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.5.0'
        }

    def get_data(self):
        res = requests.get(self.url, headers=self.headers)
        data = res.json()
        for dt in data['feeds']:
            if dt['gender'] == 0:
                gender = 'Female'
            elif dt['gender'] == 1:
                gender = 'Male'
            else:
                gender = 'Unknown'
            content = json.loads(dt['content'])
            yield {
                'key_id': 'IK_' + dt['ctime']+ '_'+ str(dt['uid']),
                'platform': 'Inke',
                'nickname': dt['nickname'],
                'author_id': str(dt['uid']),
                'gender': gender,
                'charm': int(dt['likeCount']),
                'level': int(dt['level']),
                'signature': '',
                'city': '',
                'location': dt['location'],
                'video_title': dt['title'] or dt['topicName'],
                'duration': '',
                'video_height': '',
                'video_width': '',
                'avatar_large': '',
                'avatar_medium': dt['portrait'],
                'avatar_thumb': '',
                'video_cover': content['scale_url'],
                'video_url': content['mp4_url'],
                'video_ctime': dt['ctime'],
                'crawl_time': str(int(time.time() * 1000))
            }


class Save:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)'}
        self.conn = pymysql.connect(host='xxx.xx.xx.xxx',
                                    port=3306x,
                                    user='xxxx',
                                    password='xxxx',
                                    database='xxx',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.create_aql = '''
                                    CREATE TABLE IF NOT EXISTS xxx.small_video
                            (
                                  key_id VARCHAR(32) NOT NULL PRIMARY KEY
                                , platform VARCHAR(8) NOT NULL
                                , nickname VARCHAR(16) NULL
                                , author_id VARCHAR(16) NOT NULL
                                , gender VARCHAR(8) NOT NULL
                                , charm INT NULL
                                , level INT NULL
                                , signature VARCHAR(256) NULL
                                , city VARCHAR(8) NULL
                                , location VARCHAR(8) NULL
                                , video_title VARCHAR(256) NULL
                                , duration DECIMAL(5,3) NULL
                                , video_height INT NULL
                                , video_width INT NULL
                                , avatar_large VARCHAR(256) NULL
                                , avatar_medium VARCHAR(256) NOT NULL
                                , avatar_thumb VARCHAR(256) NULL
                                , video_cover VARCHAR(256) NOT NULL
                                , video_url VARCHAR(256) NOT NULL
                                , video_ctime VARCHAR(16) NULL
                                , crawl_time VARCHAR(16) NOT NULL
                            );'''
        self.cur.execute(self.create_aql)

    def link_to_content(self,link):
        res = requests.get(link,headers=self.headers)
        return res.content

    def save_mp4_local(self,content):
        target = os.getcwd() #TODO
        file_path = '{0}/{1}.{2}'.format(target, md5(content).hexdigest(), 'mp4')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(content)
                f.close()

    def save_info_db(self,dt):
        sql = ('''INSERT INTO xyl.small_video 
                  (key_id,platform,nickname,author_id,gender,charm,level,signature,city,location,
                   video_title,duration,video_height,video_width,avatar_large,avatar_medium,avatar_thumb,
                   video_cover,video_url,video_ctime,crawl_time)
                  VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}',
                   '{15}','{16}','{17}','{18}','{19}','{20}');'''.format(
            dt['key_id'],dt['platform'],dt['nickname'],dt['author_id'],dt['gender'],dt['charm'],dt['level'],dt['signature'],
            dt['city'],dt['location'],dt['video_title'],dt['duration'],dt['video_height'],dt['video_width'],dt['avatar_large'],
            dt['avatar_medium'],dt['avatar_thumb'],dt['video_cover'],dt['video_url'],dt['video_ctime'],dt['crawl_time'])
        )
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except pymysql.IntegrityError as e:
            print(e)
        return 'Save successfully!\r\n {0}'.format(dt)


if __name__ == '__main__':
    sv = Save()
    HS = HuoShan()
    KS = KuaiShou()
    IK = Inke()

    for i in range(100):
        print(i)
        time.sleep(1)
        data = HS.get_data(i,1000)
        for dt in data:
            print(sv.save_info_db(dt))

    for i in range(10):
        time.sleep(1)
        data = KS.get_data()
        for dt in data:
            print(sv.save_info_db(dt))

    for i in range(10):
        time.sleep(1)
        data = IK.get_data()
        for dt in data:
            print(sv.save_info_db(dt))
