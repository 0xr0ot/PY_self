import csv
import pymysql
from qqwry import QQwry


def get_addr(ip):
    return q.lookup(ip)


def gen_data(path):
    with open(path,'r',encoding='utf-8') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            if get_addr(row['110.180.134.187']):
                yield row['20210013'],get_addr(row['110.180.134.187'])[0],get_addr(row['110.180.134.187'])[1]#csv without header, so...
            else:
                yield row['20210013'], '', ''


def save_data(L):
    # try:
    sql =  "INSERT INTO dbxxx.addr920 (userid,address,network) VALUES {0};".format(str(L)[1:-1])#point

    cur.execute(sql)
    conn.commit()
    return 'Save successfully!\r\n {0}'.format(len(L))
    # except:
    #     conn.rollback()
    #     return 'Save faild!\r\n {0}'.format(dt)



def main(i):
    L = []
    path = r'F:\ip\{0}_ip.csv'.format(i)
    for ind,dt in enumerate(gen_data(path)):
        if len(L) > 200000:
            print('Saving 20000 rows data...')
            print(len(L))
            save_data(L)
            L = []
        else:
            L.append(dt)
            print(ind, dt)


if __name__ == '__main__':
    q = QQwry()
    q.load_file('qqwry.dat')

    conn = pymysql.connect(host='xxx.xx.xx.xx',
                                 port=33066,
                                 user='dbxxx_user',
                                 password='xxxx',
                                 database='dbxxx',
                                 charset='utf8mb4')
                                 #cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS dbxxx.addr920 (userid int PRIMARY KEY,address text,network text);")
    try:
        main(2014)#TODO
    finally:
        cur.close()
        conn.close()
#END
