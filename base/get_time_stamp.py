import time
import datetime

##method_1:
def get_time_stamp():
    time_f = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_p = time.strptime(time_f, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_p))
    return time_stamp

if __name__ == '__main__':
    get_time_stamp()

##method_2:
time_stamp = int(time.time())

##opposite：
timeStamp = 1499245099
def trans_timestamp(tsp):
    see_time = datetime.datetime.utcfromtimestamp(tsp).strftime("%Y-%m-%d %H:%M:%S")## utc: 8 hours.
    return see_time
