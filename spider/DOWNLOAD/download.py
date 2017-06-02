#!usr/bin/env python3
#-*- coding: utf-8 -*-

import re
import time
import random
import requests
from config import *

class Download:

    def __init__(self):
        ip_html = requests.get('http://api.xicidaili.com/free2016.txt')
        self.iplist = re.findall(r'(.*?)\r\n', ip_html.text, re.S)  ##re.S匹配包括换行符
        
        self.user_agent_list = UA_list


    def get(self, url, timeout=None, proxy=None, num_retry=7):        
        ## get策略为：先本地ip＋模仿浏览器头，不然就代理ip＋模仿浏览器头，辅助为重试（应对对方服务器及网络问题）。
        ## timeout: eg:(6, 12)，但实际操作后，只要timeout不是None，就会报错。
        ## proxy: 但requests.get的固定参数为'proxies', eg: 'headers',不要弄错。
        
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent': UA}

        if proxy == None:
            try:
                return requests.get(url, timeout, headers=headers)
            except:
                if (num_retry - 4) > 0:
                    time.sleep(7)
                    print('获取网页出错，7s后将获取倒数第：', num_retry, '次!')
                    return self.get(url, timeout, num_retry-1)
                else:
                    print('开始使用代理!')
                    time.sleep(1)
                    IP = random.choice(self.iplist)
                    proxy = {'http': IP}
                    print('当前代理@是：', proxy)
                    return self.get(url, timeout, proxy)

        else: ##代理不为空
            try:
                return requests.get(url, timeout, headers=headers, proxies=proxy) ##proxies
            except:
                if num_retry > 0:
                    time.sleep(7)
                    IP = random.choice(self.iplist)
                    proxy = {'http': IP}
                    num_retry -= 1
                    print('正在更换代理，7s后将重新获取倒数第', num_retry, '次')
                    print('当前@@代理是：', proxy)                   
                    return requests.get(url, timeout, headers=headers, proxies=proxy) ##proxies
                else:
                    print('代理也无法使用了，开始转为本地ip抓起！tor！')
                    return self.get(url, timeout=None, proxy=None, num_retry=7)

       
download = Download()
