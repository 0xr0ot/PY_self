import time
import datetime

##method_1:
def get_timestamp():
    time_f = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_p = time.strptime(time_f, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_p))
    return time_stamp #返回10位

##method_2:
time_stamp = int(1000 * time.time())#返回13位

##opposite：
timeStamp = 1499245099
def trans_timestamp(tsp): #参数为10位
    ##datetime.datetime.utcfromtimestamp(tsp)## utc: +8 hours.in China not need.
    see_time = datetime.datetime.fromtimestamp(tsp).strftime("%Y-%m-%d %H:%M:%S")
    return see_time


#TEST:
print(time_stamp)
print(trans_timestamp(time_stamp))#13位会报错

print(get_timestamp())
print(trans_timestamp(get_timestamp()))#10位正常，返回：2017-11-06 11:44:16
