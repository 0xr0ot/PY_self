#-*-coding:utf-8-*-

import numpy as np
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BaseDiscreteNB,BernoulliNB

#X = np.array([['程序员','手痛'],['程序员','头痛'],['数据员','头痛'],['数据员','胃痛'],['前台','胃痛'],['前台','手痛']])
#y = np.array(['骨折','脑震荡','没病','肠胃炎','肠胃炎','没病'])

'''
job		            perform		    pain	
programmer	1	    finger	3	    fracture	1
programmer	1	    head	1	    cold	    2
dmer	    2	    head	1	    no	        3
dmer	    2	    stomach	2	    stomachache	4
hr	        3	    stomach	2	    stomachache	4
hr	        3	    finger	3	    no	        3
'''

X = np.array([[1,3],[1,1],[2,1],[2,2],[3,2],[3,3]])
y = np.array([1,2,3,4,4,3])
test = np.array([[1,2],[2,3],[3,1]])

clf = GaussianNB()
clf.fit(X,y)
pred = clf.predict(test)

pred_proba = clf.predict_proba(test) #测试集样本在各个类别上预测的概率
pred_log_proba = clf.predict_log_proba(test)#测试集样本在各个类别上预测的概率的一个对数转化
print(pred)
print(pred_proba)
#print(pred_log_proba)


#attrs:
# attr_1 = GaussianNB(priors=None)
# attr_2 = MultinomialNB(alpha=1.0,fit_prior=True,class_prior=None)
# attr_3 = BernoulliNB(alpha=1.0,fit_prior=True,class_prior=None,binarize=0.0)
