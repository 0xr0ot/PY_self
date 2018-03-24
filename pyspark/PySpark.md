![](https://i.imgur.com/WnX6H20.png)

# *Welcome to [pyspark](http://spark.apache.org/docs/latest/api/python/pyspark.html) !* #


| Author | ulion.tse|
| :---:  | :---:  |

## *一、初始化 [SparkContext(上下文，环境)]()* ##

```python
from pyspark import SparkContext,SparkConf

# method_1:
sc_1 = SparkContext(master='local',appName='project_1') 
...
sc_1.stop()

# method_2:
conf = SparkConf().setMaster('local').setAppName('project_2')
sc_2 = SparkContext(conf=conf)
...
sc_2.stop()
```

## *二、run* ##

```python
# run 'spark_test.py' in cmd(Treminal):
>bin/spark-submit Py_path/spark_test.py
```
## *三、RDD操作* ##

- 创建RDD

```python
# list,set,tuple,dict
data1 = sc.parallelize([('Rose',28),('Walker',28),('Kane',24),('alli',21)]) # input: list
data2 = sc.parallelize({('Rose',28),('Walker',28),('Kane',24),('alli',21)}) # input: set
data3 = sc.parallelize((('Rose',28),('Walker',28),('Kane',24),('alli',21))) # input: tuple
data4 = sc.parallelize(OrderedDict([('Rose',28),('Walker',28),('Kane',24),('alli',21)])) # input: dict
print(data4.collect())
print(type(data3.collect()),type(data4.collect())) # all --> <class 'list'> , dict return key_list.

data5 = sc.parallelize(c=[('Rose',28),('Walker',28),('Kane',24),('alli',21)],numSlices=3) #分区为3
print(data5.glom().collect())
##return: [[('Rose', 28)], [('Walker', 28)], [('Kane', 24), ('alli', 21)]]

# file
data_file = sc.textFile('C:\\InPySpark\\words.txt')
print(data_file.collect())
##return: ['I love python.', 'I like pyspark.', 'I like pytorch.']
print(type(data_file.collect())) # all --> <class 'list'>

```

- 转化操作

```python
## .map()
data_file_conv1 = data_file.map(lambda x: x if 'python' not in x else '') # 将整个文章当作list，以行分割处理
print(data_file_conv1.collect())
##return: ['', 'I like pyspark.', 'I like pytorch.']
# print(data_file_conv1.take(2)) # Returns first 2 entries

## .flatMap()
data_file_conv2 = data_file.flatMap(lambda x: x if 'python' not in x else '') # 将一行当作一个list处理，之后将记录加入到一起
print(data_file_conv2.collect())
##return: ['I', ' ', 'l', 'o', 'v', 'e', ' ', 'p', 'y', 't', 'h', 'o', 'n', '.']

## .filter()
data_file_conv3 = data_file.filter(lambda x: x if 'python' not in x else '')
print(data_file_conv3.collect())
##return: ['I like pyspark.', 'I like pytorch.']

## .distinct()
data_file_conv4 = data1.map(lambda x: x[1]).distinct()
print(data_file_conv4.collect())
##return: [24, 28, 21]

## .sample()
data_file_conv5 = data_file.sample(withReplacement=False,fraction=0.67,seed=1234)
print(data_file_conv5.collect())
##return: ['I love python.', 'I like pytorch.']

## .leftOuterJoin() # 高开销
rdd1 = sc.parallelize([('a',1),('b',2),('c',3)])
rdd2 = sc.parallelize([('a',1),('a',10),('b',20),('d',40)])
rdd3 = rdd1.leftOuterJoin(rdd2)
print(rdd3.collect())
##return: [('c', (3, None)), ('b', (2, 20)), ('a', (1, 1)), ('a', (1, 10))]

## .join()
rdd4 = rdd1.join(rdd2)
print(rdd4.collect())
##return: [('b', (2, 20)), ('a', (1, 1)), ('a', (1, 10))]

## .intersection() #返回相同的记录
rdd5 = rdd1.intersection(rdd2)
print(rdd5.collect())
##return: [('a', 1)]

## .repartition() #重新对数据集进行分区
rdd2 = rdd2.repartition(5)
print(rdd2.collect())
##return: [('a', 1), ('a', 10), ('b', 20), ('d', 40)]
print(len(rdd2.glom().collect()))
##return: 5
print(rdd2.glom().collect())
##return: [[], [('a', 1), ('a', 10), ('b', 20), ('d', 40)], [], [], []]

```
- 行动操作

```python
## .take(), .takeOrdered(), .takeSample()
r1 = rdd2.take(2)
print(r1)
##return: [('a', 1), ('a', 10)]
r2 = rdd2.takeOrdered(2)
print(r2)
##return: [('a', 1), ('a', 10)]
r3 = rdd2.takeSample(withReplacement=False,num=3,seed=1234)
print(r3)
##return: [('a', 10), ('b', 20), ('a', 1)]

## .collect() #元素返回给驱动程序
print(rdd2.collect())
##return: [('a', 1), ('a', 10), ('b', 20), ('d', 40)]


## .reduce(), .reduceByKey()
data_reduce1 = sc.parallelize([1, 2, 0.5, 0.1, 5, 0.2], 1)
data_reduce3 = sc.parallelize([1, 2, 0.5, 0.1, 5, 0.2], 3)

work1 = data_reduce1.reduce(lambda x,y: x/y)
print(work1) ##return: 10.0
work3 = data_reduce3.reduce(lambda x,y: x/y)
print(work3) ##return: 0.004

work_key = rdd2.reduceByKey(lambda x,y: x+y)
print(work_key.collect()) #return: [('a', 11), ('b', 20), ('d', 40)]


## .count(), .countByKey()
print(len(rdd2.collect())) # 需要把数据集移动到驱动程序
##return: 4
print(rdd2.count()) # 效率高
##return: 4
print(rdd2.countByKey().items())
##return: dict_items([('b', 1), ('d', 1), ('a', 2)])

## .saveAsTextFile()
rdd2.saveAsTextFile('rdd2_test.txt')

def parseRow(row):
    import re
    pattern = re.compile(r"\(\'([a-z]+)\', ([0-9]+)\)") #正确匹配哟
    row_split = pattern.split(row)
    return (row_split[1], row_split[2])

rdd2_test = sc.textFile('rdd2_test.txt').map(parseRow)
print(rdd2_test.collect())

## .foreach() #将数据保存到pyspark不支持的数据库中很有用
rdd2.foreach(lambda x: print(x))

```
## *四、DataFrame* ##

```python
# coding=utf-8

import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SparkSession,types


sc = SparkContext(master='local',appName='dataframe_test')
spark = SparkSession(sc)

str_rdd = sc.parallelize(['''{
    'id': '123',
    'name': 'Kane',
    'age': 19,
    'color': 'brown'
}''',
'''{
    'id': '234',
    'name': 'Rose',
    'age': 22,
    'color': 'green'
}''',
'''{
    'id': '345',
    'name': 'Walker',
    'age': 23,
    'color': 'blue'
}'''])

# print(str_rdd.collect())
json_rdd = spark.read.json(str_rdd)
# print(json_rdd.collect())
# print(type(json_rdd)) ##return: <class 'pyspark.sql.dataframe.DataFrame'>
# json_rdd.show()

df = pd.DataFrame({'a': [1,2,3],'b': ['apple','banana','melon'], 'c': [True,False,True]})
df_rdd1 = spark.createDataFrame(df)
# df_rdd1.show()
############################## NO ###############################################
# json_rdd.createOrReplaceGlobalTempView('test0_temp') # 创建临时表，本地貌似不行啊
# json_rdd.show()
#
# sql_rdd = spark.sql('select * from test0_temp') # 使用临时表进行查询，貌似不行啊
# print(sql_rdd.collect())
############################## NO ###############################################

json_rdd.printSchema() # 打印数据类型(模式)

rdd1 = sc.parallelize([(123,'Kane',19,'brown'),(234,'Rose',22,'green'),(345,'Walker',23,'blue')])

# 指定数据类型(模式)
schema = types.StructType([types.StructField('id',types.LongType(),True),
    types.StructField('name',types.StringType(),True),
    types.StructField('age',types.LongType(),True),
    types.StructField('color',types.StringType(),True),
])

df_rdd2 = spark.createDataFrame(rdd1,schema)
df_rdd2.printSchema()

# 获取age=22的id
df_rdd2.select('id','age').filter('age = 22').show()
df_rdd2.select(df_rdd2.id,df_rdd2.age).filter(df_rdd2.age==22).show()
spark.sql("select id,age from df_rdd2 where age = 22").show() # sql查询形式

# 获得color以字母b开头的name,color
df_rdd2.select('name','color').filter("color like 'b%'").show()
spark.sql("select name,color from df_rdd2 where color like 'b%'") # sql查询形式

# 查行数
spark.sql("select count(1) from df_rdd2").show() #本地临时表建立无效




sc.stop()

```
