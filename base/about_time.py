import time
from datetime import datetime,date,timedelta

##method_1:
def get_timestamp():
    time_f = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_p = time.strptime(time_f, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_p))
    return time_stamp #返回10位

def to_timestamp(tt,length=10):
    return int(time.mktime(time.strptime(tt,'%Y-%m-%d %H:%M:%S')))*(10**(length-10))
# to_timestamp('2018-10-10 19:40:32')
# return: 1539171632

#########################################################################
from datetime import datetime,date,timedelta

week_now = datetime.today().weekday()
print(week_now)# return: [0,6]

def getWeek(date,isPt=False):
    date_format = '%Y%m%d' if isPt else '%Y-%m-%d'
    return datetime.strptime(date,date_format).weekday() #[0,6] 0: Monday.

def getDate(n,isPt=False):
    the_day = date.today() + timedelta(days=n)
    date_format = '%Y%m%d' if isPt else '%Y-%m-%d'
    return the_day.strftime(date_format)

def getTime(timestamp):
    timestamp = int(timestamp/1000) if len(str(timestamp)) == 13 else timestamp
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
