#-*-coding: utf-8-*-

from math import sqrt


def sim_distance(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys()) ## shared items.
            
    if not si:
        return 0
    
    sum_of_squares = sum(pow(prefs[p1][item]-prefs[p2][item], 2) for item in si)
    r = 1/(1+sqrt(sum_of_squares))
    return r
