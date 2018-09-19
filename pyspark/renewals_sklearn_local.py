# coding=utf-8
# uliontse

from __future__ import division # must first column.
import datetime
import numpy as np
import pandas as pd
import pickle
from pyspark import SparkContext,HiveContext
import lightgbm as lgb
from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,roc_auc_score


try:
    sc = SparkContext()
    spark = HiveContext(sc)
except:
    spark = HiveContext(sc)


path = '/home/xxx/xxx/'

spark_df1 = spark.sql('select * from temp.xxx_feature').select('*')
data = spark_df1.toPandas()
print(data.shape)

spark_df2 = spark.sql('select * from temp.xxx_feature_20180801')
data2 = spark_df2.toPandas()
print(data2.shape)

spark_df3 = spark.sql('select * from temp.xxx_feature_20180815')
data3 = spark_df3.toPandas()
print(data3.shape)
################## feature_choice ###################################################################################

def getDuring(now_date,n=0):
    try:
        today = datetime.datetime.strptime(now_date,'%Y-%m-%d')
    except:
        today = datetime.datetime.strptime(now_date, '%Y/%m/%d')
    oneday = datetime.timedelta(days=n)
    n_day = (today + oneday).day
    if n_day in range(1,11):
        return 1
    elif n_day in range(11,21):
        return 2
    else:
        return 3


def clear_data(data):
    ##drop:
    drop_pool = ['lm_stu_cancel_cnt','near_stu_cancel_distance','gift_gr13_hours','gift_gr15_hours','first_new_distance',
                 'first_subjoin_distance']
    data.drop(drop_pool,axis=1,inplace=True)
    data = data[data['age'] > 2] #删除年龄异常
    data = data[data['age'] < 17] #删除年龄异常
    data = data[data['left_hours'] >= 0] #删除异常值，剩余课时为负
    data = data[data['level_sequence'].notnull()] #删除异常值，没有定级

    data = data[data['register_distance'].notnull()] #删除异常值，没有注册时间
    data = data[data['register_distance'] > 0]

    data = data[data['entry_distance'].notnull()] #删除还没上过主修课的人
    data = data[data['entry_distance'] > 0]

    data = data[data['paid_success_cnt'].notnull()] #删除从未付费或退费了的人
    data = data[data['paid_success_cnt'] > 0] #同上


    ##fillna:
    data['city_level'] = data['city_level'].fillna(8)
    data[['info_length','lp_change_cnt']] = data[['info_length','lp_change_cnt']].fillna(0)
    # data['l6m_hw_avg_score'] = data['l6m_hw_avg_score'].fillna(0)
    # data['l6m_hw_avg_time'] = data['l6m_hw_avg_time'].fillna(1e8)

    # data['l6m_avg_bad_rating'] = data['l6m_avg_bad_rating'].fillna(data['l6m_avg_bad_rating'].median())

    for x in list(data.columns):
        if 'cnt' in x or 'hours' in x:
            data[x] = data[x].fillna(0)
        # if 'distance' in x:
        #     data[x] = data[x].fillna(2000)

    data['all_paid_hours'] = data['paid_new_hours'] + data['paid_subjoin_hours'] + data['paid_renew_hours']
    data = data[data['all_paid_hours'] > 0]

    data['register2new_distance'] = data['register_distance'] - data['last_new_distance']
    data['new2entry_distance'] = data['last_new_distance'] - data['entry_distance']

    data['renew_during'] = data['point_36_date'].apply(lambda x: getDuring(x,11)) #avg(datediff(point_renew_date,point_36_date))

    data['f2l_paid_distance'] = data['first_paid_distance'] - data['last_paid_distance']
    data['f2l_paid_avg_distance'] = data['f2l_paid_distance'] / data['paid_success_cnt']

    data['new2subjoin_distance'] = data['last_new_distance'] - data['last_subjoin_distance']
    data['subjoin2renew_distance'] = data['last_subjoin_distance'] / data['first_renew_distance']

    data['l6m_hm_avg_efficiency'] = data['l6m_hw_avg_score'] / data['l6m_hw_avg_time']

    data['all_gift_hours'] = data['gift_positive_hours'] + data['gift_negative_hours']
    data['gift_positive_percent'] = data['gift_positive_hours'] / (data['all_gift_hours'] +1)
    data['gift_negative_percent'] = data['gift_negative_hours'] / (data['all_gift_hours'] +1)
    data['gift_PN_rate'] = (data['gift_positive_hours'] +1) / (data['gift_negative_hours'] +1)

    data['left_hours_percent_paid'] = data['left_hours'] / data['all_paid_hours']
    data['left_hours_percent_all'] = data['left_hours'] / (data['all_paid_hours'] + data['all_gift_hours'])
    data['left_hours_percent_last_paid'] = data['left_hours'] / data['last_paid_hours']
    data['lpd2n_noconsume_class_cnt'] = (data['lastpaid2now_class2_hours'] - data['lastpaid2now_class1_hours']) / data['last_paid_distance']

    data['lpd2n_abs_diff_left_hours'] = np.abs(data['last_left_hours'] - data['left_hours'])
    data['lpd2n_isless_left_hours'] = np.where(data['last_left_hours'] > data['left_hours'],1,0)

    data['lpd2n_day_class_hours'] = (data['last_paid_hours'] + data['last_left_hours']) / data['last_paid_distance']
    data['will_zero_hours_distance'] = data['left_hours'] / ((data['lastpaid2now_class1_hours']+1) / data['last_paid_distance']) #课消效率相同

    for x in ['gift_gr1_hours']:
        if 'hours' in x and 'avg' not in x:
            data['avg_day_' + x] = data[x] / data['entry_distance']
            data.pop(x)
        else:
            pass

    #drop:
    data.pop('register_distance')
    data.pop('lastpaid2now_class2_hours')
    data.pop('student_type')

    data.drop(['point_36_date','student_id'],axis=1,inplace=True) #TODO
    print(data.shape)
    return data

data = clear_data(data)
data2 = clear_data(data2)
data3 = clear_data(data3)
######################### train_model ################################################################################
# df = data
# df = shuffle(df,random_state=1234)
# df_y0 = df[df['y'] == 0]
# df_y1 = df[df['y'] == 1]
# print(len(df_y0),len(df_y1))
#
# test = pd.concat([df_y0[:int(len(df_y0)*0.2)], df_y1[:int(len(df_y1)*0.2)]])
# y_test = test.pop('y')
# x_test = test
#
# ##train_data:
# train = pd.concat([df_y0[int(len(df_y0)*0.2):], df_y1[int(len(df_y1)*0.2):]])
# y_train = train.pop('y')
# x_train = train
y_train = data.pop('y')
x_train = data

y_val = data2.pop('y')
x_val = data2

y_test = data3.pop('y')
x_test = data3
# x1_train,x2_train,y1_train,y2_train= train_test_split(x_train,y_train,test_size=0.2,random_state=1234)
model = lgb.LGBMClassifier(
    max_depth=6,
    num_leaves=36,
    learning_rate=0.03,
    n_estimators=1000,
    min_child_samples=80,
    subsample=1,
    reg_lambda=0.03
)
model.fit(
    x_train,
    y_train,
    eval_set=[(x_train,y_train),(x_val,y_val)],
    eval_names=('fit', 'val'),
    eval_metric='auc',
    early_stopping_rounds=150
)

y2_pred = model.predict(x_val, num_iteration=model.best_iteration_)
print(confusion_matrix(y_val, y2_pred))

y3_pred = model.predict(x_test, num_iteration=model.best_iteration_)
print(confusion_matrix(y_val, y3_pred))

######################## predict ############################################################################################
#with open(path+'xxx_renew_model.pkl', 'wb') as f:
#    pickle.dump(model, f)

# bst = model.booster_
# bst.save_model(path+'xxx_renew_model.model')
# print('save model finished.')

sc.stop()
print('End!')

