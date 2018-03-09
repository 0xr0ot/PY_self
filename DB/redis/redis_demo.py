# coding=utf-8

import redis

conn = redis.StrictRedis(host='localhost',port=6379,db=0,)
person = {
    'name': 'ulion',
    'age': 20,
    'sex': None
}
conn.hmset('person',person)
data = conn.hmget('person',person)

data = list(map(lambda x: x.decode(),data))
print(data) # unordered list

conn.connection_pool.disconnect()
