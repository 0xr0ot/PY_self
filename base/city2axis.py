# coding=utf-8
# uliontse

import requests

def baiduMap(city):
    key = 'GjG3XAdmywz7CyETWqHwIuEC6ZExY6QT'
    url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak={}&address='.format(key) + city
    data = requests.get(url).json()
    return data

def googleMap(city):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city
    data = requests.get(url).json()
    return data


for city in ('上海','上海市','纽约','New York','Bixessarri','NULL',''):
    # print(baiduMap(city))
    print(googleMap(city))
    # 申请key
    # https://console.developers.google.com/apis/credentials?project=_
