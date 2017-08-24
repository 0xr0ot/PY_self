#-*-coding:utf-8-*-

import time
import requests
from bs4 import BeautifulSoup
import psycopg2
#from all_vpnsite import *

ss = requests.Session()
ss.trust_env = False
host = 'http://www.xicidaili.com'
category = ['nt','nn','wn','wt','qq']


headers = {
    'Host': 'www.xicidaili.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Referer': 'http://www.xicidaili.com/nt/2',#TODO
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cookie': ('_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTRiZTUyMzBmNTg5OTM2YmJkMjUwNzI0YzA3MmZmYzhhBjsAVEkiEF9jc3JmX3Rva2VuBjs'
               'ARkkiMW41d1hVT2lRbmx6SG05QWZzTGhsQnJMKzY0S0swNE5zcURzWERORi9QSG89BjsARg%3D%3D--75202b4ab0931f7023c611e51d6b3726333b1c83; '
               'Hm_lvt_0cf76c77469e965d2957f0553e6ecf59={0}; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59={1}'.format(int(time.time()),int(time.time()))),#TODO
    'If-None-Match': 'W/"6d13de41dfc71909f4b7f53fb9ad09ea"'#TODO
    }

def get_soup(url):
    try:
        res = ss.get(url, headers=headers)
    except:
        res = ss.get(url, headers=headers, proxies={'http': '58.217.255.184:1080'})
    soup = BeautifulSoup(res.text,'lxml')
    return soup


def get_data(soup):
    items = soup.find_all('tr',{'class': ['odd','']})
    for item in items:
        it = item.find_all('td')
        try:
            country = it[0].img.attrs['alt']
            source_url = host + it[3].a.attrs['href']
        except AttributeError:
            country = None
            source_url = None
        data = {
            'complete_ip': it[1].get_text() +':'+ it[2].get_text(),
            'ip_address': it[1].get_text(),
            'port': it[2].get_text(),
            'country': country,
            'server_area': it[3].get_text().strip('\n'),
            'category': it[4].get_text(),
            'http_type': it[5].get_text(),
            'transfer_speed': it[6].div.attrs['title'],
            'response_time': it[7].div.attrs['title'],
            'network_operator': None,
            'survived_time': it[8].get_text(),
            'verify_datetime': it[9].get_text(),
            'source_url': source_url,
            'source_host': host
            }
        yield data

def save_psg(dt):
    try:
        sql = ("INSERT INTO xxx.ip_pool_xxx"
               "(complete_ip,ip_address,port,country,server_area,category,http_type,transfer_speed,response_time,"
               "network_operator,survived_time,verify_datetime,source_url,source_host)"
               "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}');".format(
                dt['complete_ip'],dt['ip_address'],dt['port'],dt['country'],dt['server_area'],dt['category'],dt['http_type'],
                dt['transfer_speed'],dt['response_time'],dt['network_operator'],dt['survived_time'],dt['verify_datetime'],dt['source_url'],dt['source_host']
            ))
        cur.execute(sql)
        conn.commit()
    except psycopg2.IntegrityError as e:
        print(e)
    return 'Save successfully!\r\n {0}'.format(dt)

def main(number):
    id_pool = set()
    for cat in category:
        for num in range(3,number):
            url = host + '/{0}/{1}'.format(cat,number)
            time.sleep(6)
            soup = get_soup(url)
            #print(soup)
            data = get_data(soup)
            for dt in data:
                if dt['complete_ip'] not in id_pool:
                    id_pool.add(dt['complete_ip'])
                    print(save_psg(dt))
        print(cat,'----',len(id_pool))
    ss.close()#TODO
    return 'func_main done!'


if __name__ == '__main__':
    conn = psycopg2.connect(database="db_xxxx", user="xxx", password="xxx", host="xxx.xx.xxx.xxx", port="5432")
    cur = conn.cursor()
    main(11)#TODO
    cur.close()
    conn.close()
    print('All end.')

#END
#TODO --> class

# pattern = re.compile('<tr class.*?>'+
#                      '<td class="country"><img src=.*?.png" alt="(.*?)"</td><td>(.*?)</td>'+
#                      '<td>(.*?)</td><td><.*?href="(.*?)">(.*?)</a></td>'+
#                      '<td.*?="country">(.*?)</td><td>(.*?)</td>'+
#                      '<td.*?="country"><.*?title="(.*?)".*?"bar">.*?</td><td.*?="country"><.*?title="(.*?)".*?"bar">.*?</td>'+
#                      '<td>(.*?)</td><td>(.*?)</td></tr>',re.S)
# items = re.findall(pattern,res.text)
# print(len(items))
