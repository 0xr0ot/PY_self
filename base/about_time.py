import time
import datetime

##method_1:
def get_timestamp():
    time_f = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_p = time.strptime(time_f, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_p))
    return time_stamp #返回10位

def to_timestamp(tt,length=10):
    return int(time.mktime(time.strptime(tt,'%Y-%m-%d %H:%M:%S')))*(10**(length-10))
# to_timestamp('2018-10-10 19:40:32')
# return: 1539171632

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


#########################################################################
from datetime import datetime,date,timedelta

week_now = datetime.today().weekday()
print(week_now)# return: [0,6]

def getDate(n,isPt=True):
    theday = date.today() + timedelta(days=n)
    if isPt:
        return theday.strftime('%Y%m%d')
    return theday.strftime('%Y-%m-%d')

