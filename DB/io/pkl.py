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
