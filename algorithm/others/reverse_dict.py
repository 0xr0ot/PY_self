# coding=utf-8

dt = {'a':{'b':{'c':{'d':'e'}}}}

def reverse_dt(dt:dict):
    pool = []
    while 1:
        p1 = [x for x in dt.items()]
        if p1[0][0]:
            pool.append(p1[0][0])
        if not isinstance(p1[0][1],dict):
            pool.append(p1[0][1])
            break
        dt = p1[0][1]

    new1,new2 = dict(),dict()
    new1[pool[1]] = pool[0]
    for i,k in enumerate(pool):
        if i >1:
            new2[k] = new1
            if i == len(pool)-1:
                break
            new1,new2 = new2,dict()
    return new2

print(reverse_dt(dt))

#dt = {'a':{'b':{'c':{'d':'e'}}}}
#>>>{'e': {'d': {'c': {'b': 'a'}}}}
