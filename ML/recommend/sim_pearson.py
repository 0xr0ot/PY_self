#-*-coding: utf-8-*-

from math import sqrt


def sim_pearson(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys()) ## shared items.
    n = len(si)
    if n == 0:
        return 0
    
    ## sum of all prefs.
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    ## sum of power.
    sum1_pw = sum([pow(prefs[p1][it], 2) for it in si])
    sum2_pw = sum([pow(prefs[p2][it], 2) for it in si])
    
    ## sum of times.
    sum_tm = sum([prefs[p1][it]*prefs[p2][it] for it in si])
  
	## pearson value.
    num = sum_tm - (sum1*sum2)/n
    den = sqrt((sum1_pw-pow(sum1, 2)/n) * (sum2_pw-pow(sum2, 2)/n))

    if den == 0:
        return 0
    r = num/den
    return r
