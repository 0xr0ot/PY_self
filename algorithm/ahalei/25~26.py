#!usr/bin/env python3
#-*-coding: utf-8-*-

"""
克拉兹问题是一个简单有趣而又没有解决的数学问题。这个问题是由L. Collatz在1937年提出的。 
　　问题如下： 
　　（1）输入一个正整数n； 
　　（2）如果n=1则结束； 
　　（3）如果n是奇数，则n变为3n+1，否则n变为n/2； 
　　（4）转入第（2）步。 
举一个例子：n=13的时候，经历10步可以达到1。 
13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1 
25.请问10000以内，哪个数变为1需要转化的步骤多。 
26.请问1000000以内，哪个数变为1需要转化的步骤多。
"""

def v2k(v, dict0):
    '''v_max2k'''
    for k in dict0.keys():
        if dict0[k] == v: ##默认最大值时key唯一，不然list.append
            return k

def main(num):
    dict1 = {}
    for i in range(1, num+1):
        ii = i
        m = 0
        while i > 0:
            if i == 1:
                break
            if i > 1 and i % 2 == 0:
                i = i / 2
                m = m + 1
            elif i > 1 and i % 2 != 0:
                i = 3*i + 1
                m = m + 1
        dict1[ii] = m
    v_max = max([x for x in dict1.values()])
    return v2k(v_max, dict1)
