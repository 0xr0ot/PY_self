#-*-coding: utf-8-*-

from math import sqrt


def sim_cos(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys())
    if not si:
        return 0
    
    sum_si = sum([(prefs[p1][it] * prefs[p1][it]) for it in si])
    
    sum1 = sum([pow(v, 2) for v in prefs[p1].values()])
    sum2 = sum([pow(v, 2) for v in prefs[p2].values()])
    
    r = sum_si/sqrt(sum1*sum2)
    return r
