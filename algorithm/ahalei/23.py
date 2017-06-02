#!usr/bin/env python3
#-*-coding: utf-8-*-

'''
23.已知正整数a0,a1,b0,b1，设某未知正整数x满足： 
1、 x和a0的最大公约数是a1； 
2、 x和b0的最小公倍数是b1。 
求出满足条件的正整数x。这样的x并不唯一，甚至可能不存在。因此考虑如何求解满足条件的x的个数。 
例如：a0=41，a1=1，b0=96，b1=288，那么x可以是9、18、36、72、144、288，共有6 个。
请问：当a0=8085，a1=105，b0=1532，b1=11099340的是时候，x有多少种可能？
'''

def gcd(n1, n2):
    '''The greatest common divisor func.'''
    return gcd(n2, n1 % n2) if n1 % n2 > 0 else n2

def lcm(n1, n2):
    '''The lowest common multiple func.'''
    return n1 * n2 // gcd(n1, n2)

def main(a0, a1, b0, b1):
    ls = []
    for x in range(1, b1+1):
        if gcd(x, a0) == a1 and lcm(x, b0) == b1:
            ls.append(x)
    return set(ls)
