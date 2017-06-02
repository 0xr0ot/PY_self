#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
22.给你n根火柴棍，你可以拼出多少个形如“A+B=C”的等式？等式中的A、B、C是用火柴棍拼出的整数（若该数非零，则最高位不能是0）。用火柴棍拼数字0-9的拼法如图所示：
My_CSDN_Blog: http://blog.csdn.net/sinat_20174131/article/details/56847685
注意： 
1. 加号与等号各自需要两根火柴棍 
2. 如果A≠B，则A+B=C与B+A=C视为不同的等式（A、B、C>=0） 
3. n根火柴棍必须全部用上 
当n=14的时候，只能拼成2种不同的等式（2个等式为0+1=1和1+0=1。）

请问当n=20的时候，能拼成多少种不同的等式？
"""

dict_m = {2:[1], 3:[7], 4:[4], 5:[2, 3, 5], 6:[0, 6, 9], 7:[8]}

def sep(num):
    '''一个数分为两个数的和,且x，y满足2~8
    '''
    two = []
    for x in range(num+1):
        for y in range(num+1-x):
            if x in range(2, 8) and y in range(2, 8):
                if x+y == num:
                    ls = []
                    ls.append(x)
                    ls.append(y)
                    two.append(ls)                 
    return two

def m2v(m):#依赖sep函数
    '''2～8仍能进行分裂,成为一个十位数，故没有范围限制
    '''
    result = []
    for pv in sep(m):#遍历所有的两两火柴数量组合
        item1, item2 = pv
        for var1 in dict_m[item1]:
            if var1 != 0:#十位不能是零
                for var2 in dict_m[item2]:
                    value = 10 * var1 + var2
                    result.append(value)
    if m < 8: ##2～8不要遗漏个位数
        for x28 in dict_m[m]:
            result.append(x28)
    return list(set(result))

def match2count(number):
    count = 0
    for match1 in range(2, number-4+1-4):
        for match2 in range(2, number-4+1-match1-2):
            match3 = number -4 - match1 - match2
            for res1 in m2v(match1):
                for res2 in m2v(match2):
                    for res3 in m2v(match3):
                        if res1 + res2 == res3:
                            count += 1
                            print('{0}+{1}={2}......{3}'.format(res1, res2, res3, count))
    return count
