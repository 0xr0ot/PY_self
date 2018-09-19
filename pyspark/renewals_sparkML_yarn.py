# coding=utf-8
# uliontse

from __future__ import division,print_function
import time
import datetime
import numpy as np
import pandas as pd
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,Column
import pyspark.sql.functions as fn
import pyspark.mllib.stat as st
import pyspark.ml.feature as ft
import pyspark.ml.classification as cl
from pyspark.ml import Pipeline
import pyspark.ml.tuning as tune
import pyspark.ml.evaluation as ev
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,roc_auc_score


begin_time = time.time()

conf = SparkConf().setMaster("yarn").setAppName("renew_app")
conf.set("spark.executor.heartbeatInterval",3600)
conf.set("spark.executor.cores",25)
conf.set("spark.python.worker.memory","1g")
conf.set("spark.executor.memory","16g")
conf.set("spark.executor.memoryOverhead",'2g')
conf.set("spark.driver.cores",8)
conf.set("spark.driver.memory",'16g')
conf.set("spark.driver.maxResultSize","16g")
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
conf.set("spark.sql.execution.arrow.enabled", "true")#toPandas best.

sc = SparkContext(conf=conf,batchSize=0)
spark = SparkSession(sc)

data = spark.sql('select * from bigdata_algorithm.xxx_renew_l6m').select('*')
print(data.count())
data.agg(fn.count('student_id').alias('stu_cnt'), fn.countDistinct('student_id').alias('stu_dis_cnt')).show()
print('negative_sample:',data.where('y==0').count())
print('positive_sample:',data.where('y==1').count())

#######################################################
def clear_spark_data(data):
    drop_pool = ['lm_stu_cancel_cnt','near_stu_cancel_distance','gift_gr13_hours','gift_gr15_hours','first_new_distance',
                 'first_subjoin_distance']
    for col in drop_pool:
        data = data.drop(col)
    data = data.filter(data['age'].between(2,18))
    data = data.filter(data['left_hours'] >= 0)
    data = data.filter(data['left_hours'].isNotNull())
    data = data.filter(data['left_hours'] != np.nan)

    data = data.filter(data['level_sequence'] >= 0)
    data = data.filter(data['level_sequence'].isNotNull())
    data = data.filter(data['level_sequence'] != np.nan)

    data = data.filter(data['register_distance'] > 0)
    data = data.filter(data['register_distance'].isNotNull())
    data = data.filter(data['register_distance'] != np.nan)

    data = data.filter(data['entry_distance'] > 0)
    data = data.filter(data['entry_distance'].isNotNull())
    data = data.filter(data['entry_distance'] != np.nan)

    data = data.filter(data['paid_success_cnt'] > 0)
    data = data.filter(data['paid_success_cnt'].isNotNull())
    data = data.filter(data['paid_success_cnt'] != np.nan)

    data = data.fillna({
        'city_level': 8,
        'info_length': 0,
        'l6m_hw_avg_score': 0,
        'l6m_hw_avg_time': 0,
        'l6m_avg_bad_rating': data.select('l6m_avg_bad_rating').toPandas().median()[0]
    })

    for x in data.columns:
        if 'cnt' in x or 'hours' in x:
            data = data.fillna({x: 0})
        elif 'distance' in x:
            data = data.fillna({x: 2000})
        else:
            pass

    data = data.withColumn('all_paid_hours', data['paid_new_hours'] + data['paid_subjoin_hours'] + data['paid_renew_hours'])
    data = data.filter(data['all_paid_hours'] > 0)
    data = data.filter(data['all_paid_hours'].isNotNull())
    data = data.filter(data['all_paid_hours'] != np.nan)

    data = data.withColumn('now_during', fn.when(fn.dayofmonth('point_36_date')<=10,1)\
                           .when(fn.dayofmonth('point_36_date')<=20,2)\
                           .otherwise(3))
    data = data.withColumn('will_renew_date', fn.date_add(data['point_36_date'],11))
    data = data.withColumn('renew_during', fn.when(fn.dayofmonth('will_renew_date')<=10,1)\
                           .when(fn.dayofmonth('will_renew_date')<=20,2)\
                           .otherwise(3))#avg(datediff(point_renew_date,point_36_date))
    data = data.drop('will_renew_date')

    data = data.withColumn('register2new_distance', data['register_distance'] - data['last_new_distance'])
    data = data.withColumn('new2entry_distance', data['last_new_distance'] - data['entry_distance'])
    # data = data.withColumn('new2subjoin_distance', data['last_new_distance'] - data['last_subjoin_distance'])#TODO
    # data = data.withColumn('subjoin2renew_distance', data['last_subjoin_distance'] - data['first_renew_distance'])#TODO
    data = data.drop('last_subjoin_distance')

    data = data.withColumn('f2l_paid_distance', data['first_paid_distance'] - data['last_paid_distance'])
    data = data.withColumn('f2l_paid_avg_distance', data['f2l_paid_distance'] / data['paid_success_cnt'])

    data = data.withColumn('all_gift_hours', data['gift_positive_hours'] + data['gift_negative_hours'])
    data = data.withColumn('gift_positive_percent', data['gift_positive_hours'] / (data['all_gift_hours'] +1))
    data = data.withColumn('gift_negative_percent', data['gift_negative_hours'] / (data['all_gift_hours'] +1))
    data = data.withColumn('gift_PN_rate', (data['gift_positive_hours'] +1) / (data['gift_negative_hours'] +1))
    data = data.withColumn('left_hours_percent_paid', data['left_hours'] / data['all_paid_hours'])
    data = data.withColumn('left_hours_percent_all', data['left_hours'] / (data['all_paid_hours'] + data['all_gift_hours']))
    data = data.withColumn('left_hours_percent_last_paid', data['left_hours'] / data['last_paid_hours'])
    data = data.withColumn('lpd2n_noconsume_class_cnt', (data['lastpaid2now_class2_hours'] - data['lastpaid2now_class1_hours']) / data['last_paid_distance'])
    data = data.withColumn('lpd2n_abs_diff_left_hours', fn.abs(data['last_left_hours'] - data['left_hours']))
    data = data.withColumn('lpd2n_isless_left_hours', fn.when(data['last_left_hours'] > data['left_hours'],1).otherwise(0))
    data = data.withColumn('lpd2n_day_class_hours', (data['last_paid_hours'] + data['last_left_hours']) / data['last_paid_distance'])
    data = data.withColumn('will_zero_hours_distance', data['left_hours'] / ((data['lastpaid2now_class1_hours']+1) / data['last_paid_distance']))
    data = data.withColumn('gift_gr1_hours_percent_entry_distance', data['gift_gr1_hours'] / data['entry_distance'])
    data = data.withColumn('student_type', fn.when(data['student_type']=='NORMAL',1).when(data['student_type']=='VIP',2)\
                           .when(data['student_type']=='KOL',3)\
                           .otherwise(0))

    data = data.drop('lastpaid2now_class2_hours')
    data = data.drop('point_36_date')
    return data

################## data_ready #############################
try:
    data = clear_spark_data(data)

    print(data.count())
    data.agg(fn.count('student_id').alias('stu_cnt'), fn.countDistinct('student_id').alias('stu_dis_cnt')).show()
    print('negative_sample:', data.where('y==0').count())
    print('positive_sample:', data.where('y==1').count())

    # stu_pool = data.select('student_id')
    data = data.drop('student_id')

    ## miss_value:
    # miss_pool = data.agg(*[(1 - (fn.count(x)/fn.count('*'))) for x in data.columns])
    # miss_pool.show()
    # miss_pool.toPandas().to_csv('/tmp/xieyulong/miss_{}.csv'.format(time.time()),index=False)

    ##static_variance:
    data_rdd = data.rdd.map(lambda row: [x for x in row])
    mllib_st = st.Statistics.colStats(data_rdd)
    for col,m,v in zip(data.columns,mllib_st.mean(),mllib_st.variance()):
        print('{0}: \t{1:.2f} \t{2:.2f}'.format(col,m,np.sqrt(v)))

    ##static_corr:

    ##train_model:
    fea_pool = data.columns
    fea_pool.remove('y')

    ##featuerCreator:
    featuerCreator = ft.VectorAssembler(inputCols=fea_pool,outputCol='features')

    ##weightCol:
    data = data.withColumn('weight',fn.when(data['y']==1,1.0).otherwise(0.02))

    train,test = data.randomSplit([0.7,0.3],seed=1234)#42
    lr_model = cl.LogisticRegression(
        # maxIter=10,
        # regParam=0.01,
        elasticNetParam=0,
        family='binomial',
        threshold=0.5,
        weightCol='weight',
        labelCol='y'
    )

    grid = tune.ParamGridBuilder()\
        .addGrid(lr_model.maxIter,[200,300,500,800])\
        .addGrid(lr_model.regParam,[0.001,0.002])\
        .build()

    evaluator = ev.BinaryClassificationEvaluator(
        rawPredictionCol='probability',
        labelCol='y'
    )

    cv = tune.CrossValidator(
        estimator=lr_model,
        estimatorParamMaps=grid,
        evaluator=evaluator,
        numFolds=3
    )

    ppline = Pipeline(stages=[featuerCreator])
    train_transfomer = ppline.fit(train)

    cv_model = cv.fit(train_transfomer.transform(train))
    test = train_transfomer.transform(test)
    results = cv_model.transform(test)
    print('predict_results_type:',type(results))
    print(evaluator.evaluate(results,{evaluator.metricName: 'areaUnderROC'}))
    print(evaluator.evaluate(results,{evaluator.metricName: 'areaUnderPR'}))

    best_param = [
        (
            [
                {key.name: paramValues} for key,paramValues in zip(params.keys(),params.values())
            ], metric
        ) for params, metric in zip(cv_model.getEstimatorParamMaps(),cv_model.avgMetrics)
    ]
    print(sorted(best_param,key=lambda x: x[1],reverse=True)[0])

    print('Begin to sklearn evaluate:')
    y_pred = results.select('prediction').toPandas()['prediction']
    y_prob = results.select('probability').toPandas()['probability']
    y_true = results.select('y').toPandas()['y']
    print(confusion_matrix(y_true,y_pred))
    print(classification_report(y_true,y_pred))

    # print(roc_auc_score(y_true,y_prob))
    print(accuracy_score(y_true,y_pred))

# lr_model = cl.GBTClassifier(
#     maxDepth=5,
#     maxIter=100,
#     stepSize=0.1,
#     maxBins=32,
#     labelCol='y',
#     maxMemoryInMB=1024
# )

# lr_model = cl.RandomForestClassifier(
#     labelCol="y",
#     maxDepth=5,
#     numTrees=20,
#     subsamplingRate=1.0,
#     minInfoGain=1.0,
#     maxMemoryInMB=1024,
#     cacheNodeIds=True,
#     seed=42
# )

# ppline = Pipeline(stages=[
#     featuerCreator,
#     lr_model
# ])
#
# model = ppline.fit(train)
# test_model = model.transform(test)
# evaluator = ev.BinaryClassificationEvaluator(
#     rawPredictionCol='features',
#     labelCol='y'
# )
#
# print(evaluator.evaluate(test_model,{evaluator.metricName: 'areaUnderROC'}))
# print(evaluator.evaluate(test_model,{evaluator.metricName: 'areaUnderPR'}))

finally:
    sc.stop()
    print('UseTime:', time.time() - begin_time)
