# coding=utf-8
# uliontse

import requests

def getMap(city):
    key = 'GjG3XAdmywz7CyETWqHwIuEC6ZExY6QTxyl'
    url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak={}&address='.format(key) + city
    data = requests.get(url).json()
    # if data['status'] == 1:
    #     print('{0}: {1}'.format(city,data['msg']))
    #     return data
    return data
