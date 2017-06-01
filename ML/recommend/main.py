#!usr/bin/env python3
#-*-coding: utf-8-*-

from math import sqrt


def transform(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            
            result[item][person] = prefs[person][item] ## transform
    return result


def sim_distance(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys()) ## shared items.
            
    if not si:
        return 0
    
    sum_of_squares = sum(pow(prefs[p1][item]-prefs[p2][item], 2) for item in si)
    return 1/(1+sqrt(sum_of_squares))



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
    return num/den
               

def sim_jaccard(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys()) ##
    if not si:
        return 0
    sum_si = sum([(prefs[p1][it] * prefs[p1][it]) for it in si])
    
    sum1 = sum([pow(v, 2) for v in prefs[p1].values()])
    sum2 = sum([pow(v, 2) for v in prefs[p2].values()])
    
    return sum_si/(sum1+sum2-sum_si)


def sim_cos(prefs, p1, p2):
    si = set(prefs[p1].keys()) & set(prefs[p2].keys())
    if not si:
        return 0
    
    sum_si = sum([(prefs[p1][it] * prefs[p1][it]) for it in si])
    
    sum1 = sum([pow(v, 2) for v in prefs[p1].values()])
    sum2 = sum([pow(v, 2) for v in prefs[p2].values()])
    return sum_si/sqrt(sum1*sum2)

   
def top_matches(prefs, person, n=10, similarity=sim_pearson):
    ## return rank_list of all scores.
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommend(prefs, person, similarity=sim_pearson):
    ## return other recommend_list of the person.
    totals = {}
    sim_sums = {}
    
    for other in prefs:
        if other == person:
            continue
        
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue

        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim

                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    ranks = [(total/sim_sums[item], item) for item,total in totals.items()]
    ranks.sort()
    ranks.reverse()
    return ranks


def calc_sim_items(prefs, n=10):
    result = {}
    item_prefs = transform(prefs)
    i = 0
    for item in item_prefs:
        i += 1
        if i % 100 == 0:
            print('{0}/{1}'.format(i, len(item_prefs)))
        scores = top_matches(item_prefs, item, n=n, similarity=sim_distance) ## sim_distance
        result[item] = scores
    return result
            

def get_recommend_items(prefs, item_match, user):
    user_ratings = prefs[user]
    item_match = calc_sim_items(prefs)
    scores = {}
    total_sim = {}

    for (item, rating) in user_ratings.items():
        for (similarity, it) in item_match[item]:
            if it in user_ratings:
                continue
            scores.setdefault(it, 0)
            scores[it] += similarity * rating

            total_sim.setdefault(it, 0)
            total_sim[it] += similarity

    ranks = [(score/total_sim[item], item) for item,score in scores.items()]
    ranks.sort()
    ranks.reverse()
    return ranks

####END####
