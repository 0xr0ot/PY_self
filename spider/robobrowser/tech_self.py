#!usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Tip1:    text = text.replace(r'\xa0', '')
    Tip2:    html.unscape(text)
'''

import re
from robobrowser import RoboBrowser


url = 'http://xxxx/xxxx/'
b = RoboBrowser(history=True)
b.open(url)

class_name = b.select('.headline h2')
class_desc = b.select('.tag-box')
class_time = b.select('h4')
teacher = b.select('.thumbnail-style h3')

qq = b.find(text = re.compile('QQ'))
qq_group = b.find(text = re.compile('\+selenium'))

info = {'class_name': class_name[0].text,
        'calss_desc': class_desc[0].text,
        'class_time': class_time[0].text,
        'teacher': teacher[0].text,
        'qq': qq,
        'qq_group': qq_group
    }

print(info)
#################################################################
'''
    methods: find_all & select (above)
'''
#页面上所有的a
all_links = b.find_all('a')  
for link in all_links:
    print(link.text)

# 页面上所有class是container的div
divs = b.find_all(class_='container')#class_
print(divs)

# limit 参数控制返回的元素个数

# 页面上前2个p
first_two_p = b.find_all('p', limit=2)
print(first_two_p)

# 如果第1个参数是列表则返回相匹配的集合

# 页面上所有的meta和title
print(b.find_all(['meta', 'img']))






