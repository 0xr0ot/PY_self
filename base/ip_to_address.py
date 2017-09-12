# import json
# from urllib.request import urlopen
#
# def get_country(ip_address):
#     response = urlopen("http://freegeoip.net/json/"+ ip_address).read().decode("utf-8")
#     response_json = json.loads(response)
#     return response_json
#
# IP_1 = "222.35.76.57"
# IP_2 = "111.201.37.159"
# IP_3 = "121.97.110.145"
# IP_4 = "60.205.112.186"
# print(get_country(IP_4))


import requests

def get_address(ip):
    host = 'http://freegeoip.net/json/'
    res = requests.get(host+ip)
    return res.json()
print(get_address('115.55.1.36'))

>>>
{'ip': '115.55.1.36', 'country_code': 'CN', 'country_name': 'China', 'region_code': '41', 'region_name': 'Henan', 'city': 'Zhengzhou', 'zip_code': '', 'time_zone': 'Asia/Shanghai', 'latitude': 34.6836, 'longitude': 113.5325, 'metro_code': 0}
