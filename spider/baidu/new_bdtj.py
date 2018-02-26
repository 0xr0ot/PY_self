# coding=utf-8
# author:uliontse

import json
import arrow
import requests


class BDTJ:
    def __init__(self):
        self.get_siteID_url = 'https://api.baidu.com/json/tongji/v1/ReportService/getSiteList'
        self.get_data_url = 'https://api.baidu.com/json/tongji/v1/ReportService/getData'
        self.username = 'xxxx'
        self.password = 'xxxx'
        self.token = 'xxxxxxxxxx'
        self.form_data = {
            'header': {
                'account_type': 1,
                'username': self.username,
                'password': self.password,
                'token': self.token
            }
        }
        self.siteIDs = self.get_siteID()


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


if __name__ == '__main__':
    today = arrow.utcnow().shift().format('YYYYMMDD')
    yesterday = arrow.utcnow().shift(days=-1).format('YYYYMMDD')
    method = 'overview/getTimeTrendRpt'
    metrics = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time'
    bdtj = BDTJ()
    for siteID in bdtj.siteIDs.values():
        data = bdtj.get_data(siteID,yesterday,today,method,metrics)
        print(data)
