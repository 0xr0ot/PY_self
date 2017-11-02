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
                    'keyId': 'HS_'+str(dt['create_time'] *1000)+'_'+dt['author']['id_str'],
                    'platform' : 'Huoshan',
                    'nickname': dt['author']['nickname'],
                    'authorId': dt['author']['id_str'],
                    'gender': gender,
                    'charm': dt['author']['fan_ticket_count'],
                    'authorLevel': dt['author']['level'],
                    'signature': dt['author']['signature'],
                    'city': dt['author']['city'],
                    'location': dt['location'],
                    'videoTitle': dt['text'],
                    'duration': dt['video']['duration'],
                    'videoHeight': dt['video']['height'],
                    'videoWidth': dt['video']['width'],
                    'avatarLarge': dt['author']['avatar_large']['url_list'][0],
                    'avatarMedium': dt['author']['avatar_medium']['url_list'][0],
                    'avatarThumb': dt['author']['avatar_thumb']['url_list'][0],
                    'videoCover': dt['video']['cover']['url_list'][0],
                    'videoUrl': 'http://hotsoon.snssdk.com/hotsoon/item/video/_playback/?video_id={}&line=0'
                                 '&watermark=0&app_id=1112'.format(dt['video']['uri']),
                    'videoCtime': str(dt['create_time'] * 1000),
                    'crawlTime': str(int(time.time()*1000))
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
                    'keyId': 'KS_'+str(dt['timestamp'])+'_'+str(dt['user_id']),
                    'platform': 'Kuaishou',
                    'nickname': dt['user_name'],
                    'authorId': str(dt['user_id']),
                    'gender': gender,
                    'charm': dt['like_count'],
                    'authorLevel': '',
                    'signature': '',
                    'city': '',
                    'location': '',
                    'videoTitle': dt['caption'],
                    'duration': '',
                    'videoHeight': dt['ext_params']['h'],
                    'videoWidth': dt['ext_params']['w'],
                    'avatarLarge': '',
                    'avatarMedium': dt['headurls'][0]['url'],
                    'avatarThumb': '',
                    'videoCover': dt['cover_thumbnail_urls'][0]['url'],
                    'videoUrl': dt['main_mv_urls'][0]['url'],
                    'videoCtime': str(dt['timestamp']),
                    'crawlTime': str(int(time.time() *1000))
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
                'keyId': 'IK_' + dt['ctime']+ '_'+ str(dt['uid']),
                'platform': 'Inke',
                'nickname': dt['nickname'],
                'authorId': str(dt['uid']),
                'gender': gender,
                'charm': int(dt['likeCount']),
                'authorLevel': int(dt['level']),
                'signature': '',
                'city': '',
                'location': dt['location'],
                'videoTitle': dt['title'] or dt['topicName'],
                'duration': '',
                'videoHeight': '',
                'videoWidth': '',
                'avatarLarge': '',
                'avatarMedium': dt['portrait'],
                'avatarThumb': '',
                'videoCover': content['scale_url'],
                'videoUrl': content['mp4_url'],
                'videoCtime': dt['ctime'],
                'crawlTime': str(int(time.time() * 1000))
            }


class Save:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)'}
        self.save_url = 'http://plugin.client.qxiu.com/video/cgi/thirdVideo/add'
        self.conn = pymysql.connect(host='xxx.xx.xx.xxx',
                                    port=3306x,
                                    user='xxxx',
                                    password='xxxx',
                                    database='xxx',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.create_sql = '''
                                    CREATE TABLE IF NOT EXISTS xxx.small_video
                            (
                                  keyId VARCHAR(32) NOT NULL PRIMARY KEY
                                , platform VARCHAR(8) NOT NULL
                                , nickname VARCHAR(16) NULL
                                , authorId VARCHAR(16) NOT NULL
                                , gender VARCHAR(8) NOT NULL
                                , charm INT NULL
                                , authorLevel INT NULL
                                , signature VARCHAR(256) NULL
                                , city VARCHAR(8) NULL
                                , location VARCHAR(8) NULL
                                , videoTitle VARCHAR(256) NULL
                                , duration FLOAT NULL
                                , videoHeight INT NULL
                                , videoWidth INT NULL
                                , avatarLarge VARCHAR(256) NULL
                                , avatarMedium VARCHAR(256) NOT NULL
                                , avatarThumb VARCHAR(256) NULL
                                , videoCover VARCHAR(256) NOT NULL
                                , videoUrl VARCHAR(256) NOT NULL
                                , videoCtime VARCHAR(16) NULL
                                , crawlTime VARCHAR(16) NOT NULL
                            );'''
        self.cur.execute(self.create_sql)
    
    def save_end(self):
        self.cur.close()
        self.conn.close()

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
        save_sql = ('''INSERT INTO xxx.small_video 
                  (keyId,platform,nickname,authorId,gender,charm,authorLevel,signature,city,location,
                   videoTitle,duration,videoHeight,videoWidth,avatarLarge,avatarMedium,avatarThumb,
                   videoCover,videoUrl,videoCtime,crawlTime)
                  VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}',
                   '{15}','{16}','{17}','{18}','{19}','{20}');'''.format(
            dt['keyId'],dt['platform'],dt['nickname'],dt['authorId'],dt['gender'],dt['charm'],dt['authorLevel'],dt['signature'],
            dt['city'],dt['location'],dt['videoTitle'],dt['duration'],dt['videoHeight'],dt['videoWidth'],dt['avatarLarge'],
            dt['avatarMedium'],dt['avatarThumb'],dt['videoCover'],dt['videoUrl'],dt['videoCtime'],dt['crawlTime'])
        )
        try:
            self.cur.execute(save_sql)
            self.conn.commit()
        except pymysql.IntegrityError as e:
            print(e)
        return 'Save successfully!\r\n {0}'.format(dt)

    def save_to_url(self,dt):
        res = requests.post(self.save_url,data=dt)
        return res


if __name__ == '__main__':
    sv = Save()
    HS = HuoShan()
    KS = KuaiShou()
    IK = Inke()

    for i in range(200):
        time.sleep(.3)
        data = HS.get_data(i)
        for dt in data:
            sv.save_to_url(dt)
            print(sv.save_info_db(dt))

    for i in range(10):
        time.sleep(.3)
        data = KS.get_data()
        for dt in data:
            sv.save_to_url(dt)
            print(sv.save_info_db(dt))

    for i in range(20):
        time.sleep(.3)
        data = IK.get_data()
        for dt in data:
            sv.save_to_url(dt)
            print(sv.save_info_db(dt))
            
    sv.save_end()
