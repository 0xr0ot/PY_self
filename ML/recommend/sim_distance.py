#!usr/bin/env python3
#-*-coding: utf-8-*-


def sim_distance(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys()) ## shared items.
            
    if not si:
        return 0
    
    sum_of_squares = sum(pow(prefs[p1][item]-prefs[p2][item], 2) for item in si)
    return 1/(1+sqrt(sum_of_squares))
    
####END####
