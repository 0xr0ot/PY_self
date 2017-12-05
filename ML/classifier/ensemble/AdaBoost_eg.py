# coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, cross_validation, ensemble


def load_data_regression():
    diabetes = datasets.load_diabetes()
    return cross_validation.train_test_split(diabetes.data,diabetes.target,test_size=0.25,random_state=0)

def load_data_classification():
    digits = datasets.load_digits()
    return cross_validation.train_test_split(digits.data,digits.target,test_size=0.25,random_state=0)


def test_AdaBoostClassifier(*data):
    X_train,X_test,y_train,y_test = data
    clf = ensemble.AdaBoostClassifier(learning_rate=0.05)
    clf.fit(X_train,y_train)

    # plt:
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    estimators_num = len(clf.estimators_)
    X = range(1,estimators_num+1)
    ax.plot(list(X),list(clf.staged_score(X_train,y_train)),label='Training_score')
    ax.plot(list(X),list(clf.staged_score(X_test,y_test)),label='Testing_score')
    ax.set_xlabel('estimator_num')
    ax.set_ylabel('score')
    ax.legend(loc='best')
    ax.set_title('AdaBoostClassifier')
    plt.show()

def run():
    X_train,X_test,y_train,y_test = load_data_classification()
    test_AdaBoostClassifier(X_train,X_test,y_train,y_test)


if __name__ == '__main__':
    run()
    
