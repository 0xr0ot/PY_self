#-*-coding:utf-8-*-
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import Birch,KMeans,MiniBatchKMeans,DBSCAN,SpectralClustering
from sklearn import metrics


X,y = make_blobs(n_samples=1000,n_features=2,centers=[[0,0],[0,2],[2,0],[1,1],[2,2]],cluster_std=[0.2,0.2,0.2,0.4,0.2],random_state=9)
plt.scatter(X[:,0],X[:,1],marker='o')
plt.show()


def show_cluster(category):
    if category in cat_pool:
        for index, k in enumerate([2,3,4,5,6,7]):
            plt.subplot(2,3,index+1)
            if category == 'DBSCAN':
                y_pred = eval(category + '().fit_predict(X)')
            else:
                y_pred = eval(category+'(n_clusters=k).fit_predict(X)')
            score = metrics.calinski_harabaz_score(X, y_pred)
            plt.scatter(X[:,0], X[:,1],c=y_pred)
            plt.text(.99, .01, ('k=%d,score: %.2f' % (k,score)),transform=plt.gca().transAxes, size=10,horizontalalignment='right')
        plt.show()
    else:
        print('category is spelled error!')
    return


if __name__ == '__main__':
    cat_pool = ['KMeans', 'MiniBatchKMeans', 'Birch', 'DBSCAN', 'SpectralClustering']
    show_cluster(cat_pool[4])
    ##DBSCAN-->TODO

