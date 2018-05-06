# coding=utf-8
# uliontse

import requests

def baiduMap(city):
    key = 'GjG3XAdmywz7CyETWqHxylwIuEC6ZExY6QT'
    url = 'http://api.map.baidu.com/geocoder/v2/?output=json&ak={}&address='.format(key) + city
    data = requests.get(url).json()
    return data

def googleMap(city):
    key = 'AIzaSyDdz0-XTlMqgvK6AxylaKOh45PcFJwoa08FKs'
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(city,key)
    data = requests.get(url).json()
    r = data.get('results')[0].get('formatted_address')
    return r

from mapq import Geo # edit unquote.
def mapQuest(city):
    key = 'IOonFXAQap2OXL5JWeyDtseOFhHZSV4jsYd'
    g = Geo(key)
    return g.latlng(city)

for city in ('上海','上海市','纽约','New York','Bixessarri','NULL',''):
    # print(baiduMap(city))
    print(googleMap(city))
    # 申请key
    # https://console.developers.google.com/apis/credentials?project=_
