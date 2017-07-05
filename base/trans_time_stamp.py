import time
import datetime

##method_1:
def get_timestamp():
    time_f = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_p = time.strptime(time_f, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_p))
    return time_stamp

##method_2:
time_stamp = int(time.time())

##opposite：
timeStamp = 1499245099
def trans_timestamp(tsp):
    ##datetime.datetime.utcfromtimestamp(tsp)## utc: +8 hours.in China not need.
    see_time = datetime.datetime.fromtimestamp(tsp).strftime("%Y-%m-%d %H:%M:%S")
    return see_time
