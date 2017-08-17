## zeppelin

%pyspark

##读出、写入数据库配置
p1={"url":"jdbc:sqlserver://111.111.11.51:18991;DatabaseName=db_xxx","user": "xxxx", "password": "xxxx"}
p2={"url":"jdbc:mysql://192.168.1.50:33066/db_xxx","user": "xxxx", "password": "xxxx"}

j1 = spark.read\
    .format("jdbc") \
    .option("url", p1["url"]) \
    .option("user", p1["user"]) \
    .option("password", p1["password"])
    
j2 = (spark.read
    .format("jdbc")
    .option("url", p2["url"])
    .option("user", p2["user"])
    .option("password", p2["password"]))


##新建SQL语句及建立“来自外部”的spark内部临时表
goods1_sql='''(
                SELECT DISTINCT 
                      userid
                    , goods1
                    , goods2

                FROM db_xxx.dbo.tb_xxx
    )qwe1'''
##qwe1必写
goods_df = j1.option("dbtable",goods1_sql).load().createOrReplaceTempView("temp_goods1")


##聚合查询“来自内部”的spark临时表及写入另外数据库的xxxx表
final_sql = spark.sql('''

SELECT
      a.userid
    , b.goods1
    , c.goods2
FROM
    (
        temp_goods1 a
    LEFT JOIN 
        temp_goods2 b
    ON a.userid = b.userid
    )   
 
''')
final_sql.write.jdbc(p2["url"],"t_data_personas","append",p2)
#END
