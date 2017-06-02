#!usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import requests
from lxml import etree

#session & headers
session = requests.Session()


url_1 = 'http://pythonscraping.com/pages/cookies/welcome.php' ## action url when logging web
url_2 = 'http://pythonscraping.com/pages/cookies/profile.php' ## url after logged in web

params = {'username': 'allen', 'password': 'password'}
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'           
           } ## mobile agent without AD.
time.sleep(0.01)
s1 = session.post(url_1, data=params)
##print(s1.cookies.get_dict())
time.sleep(0.01)
s2 = session.get(url_2, headers=headers)
##print(s2.text)
tree = etree.HTML(s2.text)
th = tree.xpath('//table/')[0]
print(th.text)
#########################################################################################################

##auth
from requests.auth import AuthBase, HTTPBasicAuth

url_3 = 'http://pythonscraping.com/pages/auth/login.php'
auth = HTTPBasicAuth('wangjianlong', 'password')
r = requests.post(url_3, auth = auth)
print(r.text)
###########################################################################################################


