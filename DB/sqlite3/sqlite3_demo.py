# coding=utf-8

import sqlite3


cookiePath = r'C:\Users\xxxx\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxx.default\cookies.sqlite'
con = sqlite3.connect(cookiePath)
cur = con.cursor()
cur.execute('select host, path, isSecure, expiry, name, value from moz_cookies')

for item in cur.fetchall():
    print(item)
con.close()
