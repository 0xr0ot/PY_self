#!usr/bin/env python3

'''
10.可爱的小明特别喜欢爬楼梯，他有的时候一次爬一个台阶，有的时候一次爬两个台阶，有的时候一次爬三个台阶。如果这个楼梯有36个台阶，小明一共有多少种爬法呢？
'''
from functools import reduce

def factor(n):
    if n == 0 or n == 1:
        return 1
    else:
        r = reduce(lambda x,y: x*y, range(1, n+1))
        return r


def xiaoming(n):
    ls = []
    for a in range(n+1):
        for b in range(n+1):
            for c in range(n+1):
                if a+2*b+3*c == n:
                    r1 = factor(a+b+c) / (factor(a)*factor(b)*factor(c))
                    ls.append(r1)
	r2 = sum(ls)      
    return r2
