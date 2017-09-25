#coding:utf-8

import json
import datetime
import requests
import pymysql
from pprint import pprint as ppt


class Baidu(object):

    def __init__(self, siteId, username, password, token):
        self.siteId = siteId
        self.username = username
        self.password = password
        self.token = token


    def getresult(self, start_date, end_date, method, metrics, **kw):
        base_url = "https://api.baidu.com/json/tongji/v1/ReportService/getData"
        body = {"header": {"account_type": 1, 
                           "password": self.password, 
                           "token": self.token,
                           "username": self.username},
                "body": {"siteId": self.siteId, 
                         "method": method, 
                         "start_date": start_date,
                         "end_date": end_date, 
                         "metrics": metrics}}
        for key in kw:
            body['body'][key] = kw[key]
        data = bytes(json.dumps(body), 'utf8')
        res = requests.post(base_url, data)
        return res.text


    def save_data(self,dt):
        sql = ("INSERT INTO tb_xxx "
               "(site_name,site,siteid,PV,UV,IP_count,bounce_ratio,avg_visit_time,deadline)"
               "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(
                siteid[sid][1],siteid[sid][0],sid,dt[0],dt[1],dt[2],dt[3],dt[4],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        cur.execute(sql)
        conn.commit()
        return 'Save successfully!\r\n {0}'.format(dt)


if __name__ == '__main__':
    base_url = "https://api.baidu.com/json/tongji/v1/ReportService/getData"

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)#TODO
    yest,td = str(yesterday).replace("-", ""),str(today).replace("-", "")

    siteid = {
        xxx: ['xx.xxx.com','xxWEBxx']
    }

    conn = pymysql.connect(host='xxx.xx.xx.xx',
                                 port=33066,
                                 user='xxx_user',
                                 password='xxxx',
                                 database='db_xxx',
                                 charset='utf8mb4')
                                 #cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS tb_xxx "
        "(site_name varchar(10),site varchar(15),siteid int,PV int,UV int,IP_count int,"
        "bounce_ratio float,avg_visit_time int,deadline timestamp);"
    )

    for sid in siteid.keys():
        bd = Baidu(sid, "USERNAME", "PASSWORD", "TOKEN")#TODO
        result = bd.getresult(yest, td, "overview/getTimeTrendRpt", "pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time")
        result = json.loads(result)
        data = result["body"]["data"][0]["result"]["items"][1][0]
        ppt(data)
        bd.save_data(data)
    cur.close()
    conn.close()
    print('All session & db_connection closed.')
