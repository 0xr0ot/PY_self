# coding=utf-8
# uliontse
# python2

from __future__ import division ## must first row
import sys
import datetime
from pyspark import SparkContext,HiveContext

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    sc = SparkContext()
    spark = HiveContext(sc)
except:
    spark = HiveContext(sc)

def getDate(n,isPt=True):
    today=datetime.date.today()
    oneday=datetime.timedelta(days=n)
    if isPt:
        return (today + oneday).strftime('%Y%m%d')
    return (today + oneday).strftime('%Y-%m-%d')

sql = '''
SELECT id,var1,var2,var3
FROM database_x.table_x
WHERE pt='{pt}'
'''.format(pt=getDate(-1))

df = spark.sql(sql).select('id','var1','var2','var3')
pf = df.toPandas()
lists = pf.values.tolist()

#TODO
