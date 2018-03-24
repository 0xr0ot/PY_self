# coding=utf-8

from collections import OrderedDict
from pyspark import SparkContext,SparkConf


sc = SparkContext(master='local',appName='project_1')


data1 = sc.parallelize([('Rose',28),('Walker',28),('Kane',24),('alli',21)]) # input: list
# data2 = sc.parallelize({('Rose',28),('Walker',28),('Kane',24),('alli',21)}) # input: set
# data3 = sc.parallelize((('Rose',28),('Walker',28),('Kane',24),('alli',21))) # input: tuple
# data4 = sc.parallelize(OrderedDict([('Rose',28),('Walker',28),('Kane',24),('alli',21)])) # input: dict
# print(data4.collect(),data4.collect()[0])
# print(type(data3.collect()),type(data4.collect())) # all --> <class 'list'> , dict return key_list.

# data5 = sc.parallelize(c=[('Rose',28),('Walker',28),('Kane',24),('alli',21)],numSlices=3) #分区为3
# print(data5.glom().collect())
##return: [[('Rose', 28)], [('Walker', 28)], [('Kane', 24), ('alli', 21)]]


data_file = sc.textFile('C:\\InPySpark\\words.txt')
print(data_file.collect())
##return: ['I love python.', 'I like pyspark.', 'I like pytorch.']
# print(type(data_file.collect())) # all --> <class 'list'>

# data_file_conv1 = data_file.map(lambda x: x if 'python' not in x else '') # 将整个文章当作list，以行分割处理
# print(data_file_conv1.collect())
##return: ['', 'I like pyspark.', 'I like pytorch.']
# print(data_file_conv1.take(2)) # Returns first 2 entries

# data_file_conv2 = data_file.flatMap(lambda x: x if 'python' in x else '') # 将一行当作一个list处理，之后将记录加入到一起
# print(data_file_conv2.collect())
##return: ['I', ' ', 'l', 'o', 'v', 'e', ' ', 'p', 'y', 't', 'h', 'o', 'n', '.']

# data_file_conv3 = data_file.filter(lambda x: x if 'python' not in x else '')
# print(data_file_conv3.collect())
##return: ['I like pyspark.', 'I like pytorch.']

# data_file_conv4 = data1.map(lambda x: x[1]).distinct()
# print(data_file_conv4.collect())
##return: [24, 28, 21]


# data_file_conv5 = data_file.sample(withReplacement=False,fraction=0.67,seed=1234)
# print(data_file_conv5.collect())
##return: ['I love python.', 'I like pytorch.']

# rdd1 = sc.parallelize([('a',1),('b',2),('c',3)])
# rdd2 = sc.parallelize([('a',1),('a',10),('b',20),('d',40)])
# rdd3 = rdd1.leftOuterJoin(rdd2)
# print(rdd3.collect())
##return: [('c', (3, None)), ('b', (2, 20)), ('a', (1, 1)), ('a', (1, 10))]

# rdd4 = rdd1.join(rdd2)
# print(rdd4.collect())
##return: [('b', (2, 20)), ('a', (1, 1)), ('a', (1, 10))]
# rdd5 = rdd1.intersection(rdd2)
# print(rdd5.collect())
##return: [('a', 1)]

# rdd2 = rdd2.repartition(5)
# print(rdd2.collect())
##return: [('a', 1), ('a', 10), ('b', 20), ('d', 40)]
# print(len(rdd2.glom().collect()))
##return: 5
# print(rdd2.glom().collect())
##return: [[], [('a', 1), ('a', 10), ('b', 20), ('d', 40)], [], [], []]

##################################################################################
rdd1 = sc.parallelize([('a',1),('b',2),('c',3)])
rdd2 = sc.parallelize([('a',1),('a',10),('b',20),('d',40)])

# r1 = rdd2.take(2)
# print(r1)
##return: [('a', 1), ('a', 10)]
# r2 = rdd2.takeOrdered(2)
# print(r2)
##return: [('a', 1), ('a', 10)]
# r3 = rdd2.takeSample(withReplacement=False,num=3,seed=1234)
# print(r3)
##return: [('a', 10), ('b', 20), ('a', 1)]

# r4 = rdd2.collect()
# print(r4)
##return: [('a', 1), ('a', 10), ('b', 20), ('d', 40)]

# data_reduce1 = sc.parallelize([1, 2, 0.5, 0.1, 5, 0.2], 1)
# data_reduce3 = sc.parallelize([1, 2, 0.5, 0.1, 5, 0.2], 3)
# work1 = data_reduce1.reduce(lambda x,y: x/y)
# print(work1) ##return: 10.0
# work3 = data_reduce3.reduce(lambda x,y: x/y)
# print(work3) ##return: 0.004
#
# work_key = rdd2.reduceByKey(lambda x,y: x+y)
# print(work_key.collect()) #return: [('a', 11), ('b', 20), ('d', 40)]


# print(len(rdd2.collect())) # 需要把数据集移动到驱动程序
##return: 4
# print(rdd2.count()) # 效率高
##return: 4
# print(rdd2.countByKey().items())
##return: dict_items([('b', 1), ('d', 1), ('a', 2)])


# rdd2.saveAsTextFile('rdd2_test.txt')
#
# def parseRow(row):
#     import re
#     pattern = re.compile(r"\(\'([a-z]+)\', ([0-9]+)\)") #正确匹配哟
#     row_split = pattern.split(row)
#     return (row_split[1], row_split[2])
#
# rdd2_test = sc.textFile('rdd2_test.txt').map(parseRow)
# print(rdd2_test.collect())

rdd2.foreach(lambda x: print(x))











sc.stop()

