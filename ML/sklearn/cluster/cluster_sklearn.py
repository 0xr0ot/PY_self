#-*-coding:utf-8-*-
"""
Created on Wed Jul 19 14:25:31 2017
@author: UlionTse
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import Birch,KMeans,MiniBatchKMeans,DBSCAN,SpectralClustering,ward_tree,AgglomerativeClustering,MeanShift,AffinityPropagation
from sklearn import metrics

# data ready.
X,y = make_blobs(n_samples=1000,n_features=2,centers=[[0,0],[0,2],[2,0],[1,1],[2,2]],cluster_std=[0.2,0.2,0.2,0.4,0.2],random_state=9)
plt.scatter(X[:,0],X[:,1],marker='o')
plt.show()

# needed attrs.
# attr_1 = KMeans(n_clusters=8)
# attr_2 = MiniBatchKMeans(n_clusters=8)
# attr_3 = Birch(n_clusters=3,threshold=0.5,branching_factor=50)
# attr_4 = ward_tree(X,n_clusters=None)
# attr_5 = AgglomerativeClustering(n_clusters=2,linkage='ward')
# attr_6 = DBSCAN(eps=0.5,leaf_size=30)
# attr_7 = MeanShift(bandwidth=None,seeds=None,min_bin_freq=1)
# attr_8 = SpectralClustering(n_clusters=8,n_init=10,gamma=1.0)
# attr_9 = AffinityPropagation(damping=0.5,max_iter=200,convergence_iter=15,affinity='euclidean')

def show_cluster(category):
    if category in cat_pool:
        for index, k in enumerate([2,3,4,5,6,7]):
            plt.subplot(2,3,index+1)
            y_pred = eval(category+'(n_clusters=k).fit_predict(X)')#TODO
            score = metrics.calinski_harabaz_score(X, y_pred)
            plt.scatter(X[:,0], X[:,1],c=y_pred)
            plt.text(.99, .01, ('k=%d,score: %.2f' % (k,score)),transform=plt.gca().transAxes, size=10,horizontalalignment='right')
        plt.show()
    else:
        print('category is spelled error!')
    return

if __name__ == '__main__':
    cat_pool = ['KMeans', 'MiniBatchKMeans','Birch', 'AgglomerativeClustering', 'SpectralClustering']
    show_cluster(cat_pool[1])#0~4
    ## 其他聚类算法因为参数不一致--"needed attrs"，不适用于一起对比调用，故需要单独调用使用。
    ## 之后我再完善一下，把R的也分享出来。
