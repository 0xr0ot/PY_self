#-*-coding:utf-8-*-

## make wanted blobs.
#import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
X, y = make_blobs(n_samples=2000,n_features=2,centers=[[0,0],[1,1],[0,2],[2,0],[2,2]],cluster_std=[0.2,0.4,0.2, 0.2, 0.2],random_state =9)
plt.scatter(X[:, 0], X[:, 1], marker='o')
plt.show()
######################################################################################################################

## if k = n_clusters=2.
from sklearn.cluster import KMeans
y_pred = KMeans(n_clusters=2, random_state=9).fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)
plt.show()

from sklearn import metrics
score = metrics.calinski_harabaz_score(X, y_pred) 
print(score)## More greater more good.
#####################################################################################################################

## KMeans.
from sklearn.cluster import KMeans
for index, k in enumerate((2,3,4,5,6,7,)):
    plt.subplot(2,3,index+1)
    y_pred = KMeans(n_clusters=k, random_state=9).fit_predict(X)
    score= metrics.calinski_harabaz_score(X, y_pred)  
    plt.scatter(X[:, 0], X[:, 1], c=y_pred)
    plt.text(.99, .01, ('k=%d, score: %.2f' % (k,score)),
                 transform=plt.gca().transAxes, size=10,
                 horizontalalignment='right')
plt.show()
#####################################################################################################################

## MiniBatchKMeans.
from sklearn.cluster import MiniBatchKMeans
for index, k in enumerate((2,3,4,5,)):
    plt.subplot(2,2,index+1)
    y_pred = MiniBatchKMeans(n_clusters=k, batch_size = 200, random_state=9).fit_predict(X)
    score = metrics.calinski_harabaz_score(X, y_pred)  
    plt.scatter(X[:, 0], X[:, 1], c=y_pred)
    plt.text(.99, .01, ('k=%d, score: %.2f' % (k,score)),
                 transform=plt.gca().transAxes, size=10,
                 horizontalalignment='right')
plt.show()
