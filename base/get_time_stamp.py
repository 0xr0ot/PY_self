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
