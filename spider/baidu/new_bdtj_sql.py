# coding=utf-8
# author:uliontse

import time
import json
import arrow
import pymysql
import requests


class BDTJ:
    def __init__(self,username,password,token):
        self.get_siteID_url = 'https://api.baidu.com/json/tongji/v1/ReportService/getSiteList'
        self.get_data_url = 'https://api.baidu.com/json/tongji/v1/ReportService/getData'
        self.username = username
        self.password = password
        self.token = token
        self.form_data = {
            'header': {
                'account_type': 1,
                'username': username,
                'password': password,
                'token': token
            }
        }
        self.siteIDs = self.get_siteID()
        self.conn = pymysql.connect(host='xxx.xx.xx.xx',
                                    port=33066,
                                    user='xxxx',
                                    password='xxxx',
                                    database='xxxx',
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.create_sql = '''
                            CREATE TABLE IF NOT EXISTS xyl__bdtj_v1
                                (
                                      site VARCHAR(16) NOT NULL 
                                    , siteID INT(8) NOT NULL 
                                    , PV INT(8) NOT NULL 
                                    , UV INT(8) NOT NULL 
                                    , ipCount INT(8) NOT NULL 
                                    , bounceRatio DECIMAL(5,2) NOT NULL 
                                    , avgVisitTime INT(5) NOT NULL 
                                    , deadline TIMESTAMP NOT NULL 
                                );'''
        self.cur.execute(self.create_sql)

    def get_siteID(self):
        dic = dict()
        res = requests.post(self.get_siteID_url,data=bytes(json.dumps(self.form_data),encoding='utf-8'))
        data = res.json()
        for dt in data['body']['data'][0]['list']:
            dic[dt.get('domain')] = dt.get('site_id')
        print(dic)
        return dic

    def get_data(self,siteID,start_date,end_date,method,metrics):
        self.form_data.update({
            'body': {
                'siteID': siteID,
                'start_date': start_date,
                'end_date': end_date,
                'method': method,
                'metrics': metrics
                }
        })
        res = requests.post(self.get_data_url,data=bytes(json.dumps(self.form_data),encoding='utf-8'))
        data = res.json()
        data = data["body"]["data"][0]["result"]["items"][1][0]
        return data

    def save_data(self,domain,siteID,dt):
        save_sql = '''
                    INSERT INTO xyl__bdtj_v1
                        (site,siteID,PV,UV,ipCount,bounceRatio,avgVisitTime,deadline) 
                    VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}');
                    '''.format(
                                domain,siteID,dt[0],dt[1],dt[2],dt[3],dt[4],
                                arrow.utcnow().to('local').shift().format('YYYY-MM-DD HH:mm:ss')
        )
        try:
            self.cur.execute(save_sql)
            self.conn.commit()
            print('Save successfully!\r\n{}'.format(dt))
            return 1
        except pymysql.IntegrityError as e1:
            print(e1)
            return 0
        except pymysql.err.ProgrammingError as e2:
            print(e2)
            return 0

    def save_end(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    username,password,token = ('xxxx','xxxx','xxxxxxxx') #TODO
    bdtj = BDTJ(username,password,token)

    today = arrow.utcnow().to('local').shift().format('YYYYMMDD')
    yesterday = arrow.utcnow().to('local').shift(days=-1).format('YYYYMMDD')
    method = 'overview/getTimeTrendRpt'
    metrics = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time'

    saveNum = 0
    begin = time.time()
    try:
        for domain,siteID in bdtj.siteIDs.items():
            data = bdtj.get_data(siteID,yesterday,today,method,metrics)
            saveNum += bdtj.save_data(domain,siteID,data)
    finally:
        bdtj.save_end()
        print('saveNum: ',saveNum)
        print('useTime: ',int(time.time()-begin))
