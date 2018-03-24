# codong=utf-8

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


digits = datasets.load_digits()
x_train,x_test,y_train,y_test = train_test_split(digits.data,digits.target,test_size=0.2,random_state=1234)
# print(x_train.shape) # (1437, 64)

def knn():
    knn_clf = KNeighborsClassifier()
    knn_clf.fit(x_train,y_train)
    return knn_clf.score(x_test,y_test)

def knn_pca_loop():
    for i in range(x_train.shape[1]):
        pca = PCA(n_components=i+1)
        pca.fit(x_train)
        # print(pca.explained_variance_ratio_)

        x_train_pca = pca.transform(x_train)
        x_test_pca = pca.transform(x_test)

        knn_clf = KNeighborsClassifier()
        knn_clf.fit(x_train_pca,y_train)
        yield knn_clf.score(x_test_pca,y_test)


def knn_pca_findMax():
    maxScore,num = 0,0
    for i in range(x_train.shape[1]):
        pca = PCA(n_components=i+1)
        pca.fit(x_train)
        # print(pca.explained_variance_ratio_)

        x_train_pca = pca.transform(x_train)
        x_test_pca = pca.transform(x_test)

        knn_clf = KNeighborsClassifier()
        knn_clf.fit(x_train_pca,y_train)
        score = knn_clf.score(x_test_pca,y_test)
        if score > maxScore:
            maxScore,num = score,i
    return (maxScore,num)


def knn_pca(rate):
    pca = PCA(rate)
    pca.fit(x_train)
    print(pca.n_components_)
    x_train_pca = pca.transform(x_train)
    x_test_pca = pca.transform(x_test)

    knn_clf = KNeighborsClassifier()
    knn_clf.fit(x_train_pca,y_train)
    return knn_clf.score(x_test_pca,y_test)


def knn_pca_n(n=2):
    pca = PCA(n_components=n)
    pca.fit(x_train)
    x_train_pca = pca.transform(x_train)
    x_test_pca = pca.transform(x_test)

    if n == 2:
        colors = ['gray','red','green','blue','yellow','brown','orange','black','pink','purple']
        for i in range(10):
            plt.scatter(x_train_pca[y_train==i,0],x_train_pca[y_train==i,1],alpha=0.8,color=colors[i])
        plt.show()

    knn_clf = KNeighborsClassifier()
    knn_clf.fit(x_train_pca,y_train)
    return knn_clf.score(x_test_pca,y_test)




if __name__ == '__main__':
    # print(knn())

    # for score in knn_pca_find():
    #     print(score)

    print(knn_pca_n())

    # print(knn_pca(0.9))

    print(knn_pca_findMax())
