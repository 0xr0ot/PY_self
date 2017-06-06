import pymysql

def connDB(data):
    conn = pymysql.connect(host='localhost',user='root',passwd='#######',db='xxxx',)
    cur = conn.cursor() ##游标
    cur.execute('create database if not exists test;')
    cur.close() ##关游标
    conn.commit()
    conn.close() ##关数据库
