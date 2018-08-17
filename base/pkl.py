# coding=utf-8

import pickle

svm_classifier = 'svm'

# save model:
with open('svm_model_iris.pkl', 'wb') as f:
    pickle.dump(svm_classifier, f)

# use model:
with open('svm_model_iris.pkl', 'rb') as f:
    model = pickle.load(f)
    print(model)

#########################################
import numpy as np
import pandas as pd


df =  pd.DataFrame(np.arange(24).reshape(4,6))
print(df)
df.to_pickle('df.pkl')
df2 = pd.read_pickle('df.pkl')
print(df2)
