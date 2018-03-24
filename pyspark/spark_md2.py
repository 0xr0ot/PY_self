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

