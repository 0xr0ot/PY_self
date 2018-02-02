#-*-coding: utf-8-*-

from math import sqrt

'''
Cosine Similarity:
余弦相似度用向量空间中两个向量夹角的余弦值作为衡量两个个体间差异的大小。
相比距离度量，余弦相似度更加注重两个向量在方向上的差异，而非距离或长度上。

余弦相似度更多的是从方向上区分差异，而对绝对的数值不敏感，
更多的用于使用用户对内容评分来区分用户兴趣的相似度和差异，
同时修正了用户间可能存在的度量标准不统一的问题（因为余弦相似度对绝对数值不敏感）。
'''


def sim_cos(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys())
    if not si:
        return 0
    
    sum_si = sum([(prefs[p1][it] * prefs[p2][it]) for it in si])
    
    sum1 = sum([pow(v, 2) for v in prefs[p1].values()])
    sum2 = sum([pow(v, 2) for v in prefs[p2].values()])
    
    r = sum_si/sqrt(sum1*sum2)
    return r
