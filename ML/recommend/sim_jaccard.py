#-*-coding: utf-8-*-

'''
Jaccard:

主要用于计算符号度量或布尔值度量的个体间的相似度，因此无法衡量差异具体值的大小，只能获得“是否相同”这个结果，
所以Jaccard系数只关心个体间共同具有的特征是否一致这个问题。
'''

def sim_jaccard(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys())
    if not si:
        return 0
    sum_si = sum([(prefs[p1][it] * prefs[p1][it]) for it in si])
    
    sum1 = sum([pow(v, 2) for v in prefs[p1].values()])
    sum2 = sum([pow(v, 2) for v in prefs[p2].values()])
    
    r = sum_si/(sum1+sum2-sum_si) ## 交集除以并集
    return r
