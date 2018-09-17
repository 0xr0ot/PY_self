# coding=utf-8
# author=uliontse

from __future__ import division,print_function
import numpy as np
import pandas as pd
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,Column
import pyspark.sql.functions as fn

conf = SparkConf().setMaster("yarn-client").setAppName("renew_app")
conf.set("spark.executor.heartbeatInterval","3600s")
conf.set("spark.executor.cores",4)
conf.set("spark.python.worker.memory","16g")
conf.set("spark.executor.memory","4g")
conf.set("spark.driver.maxResultSize","16g")
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

sc = SparkContext(conf=conf,batchSize=0)
spark = SparkSession(sc)

df = pd.DataFrame({'a':[1,2,3,4],'b':[2,1,3,None],'c':[None,1,4,4],'y':[1,1,0,0]})
df = spark.createDataFrame(df)

#df['a'] is Column, df.select('a') is DataFrame.

data = data.filter(df['b'] > 0)
df = df.filter(df['b'].isNotNull())
df = df.filter(df.b != np.nan)

df = df.fillna({'b': 100})

df = df.withColumn('new_col', fn.lit(0))
df = df.withColumn('new_col', fn.abs(df['b']))
df = df.withColumn('new_col', df['a'] + df['b'])
df = df.withColumn('new_col',fn.when(df['b'] == 1, 1).otherwise(0))

df.agg(*[(1 - (fn.count(x)/fn.count('*'))) for x in df.columns]).show()
