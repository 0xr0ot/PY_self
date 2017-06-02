#!usr/bin/env python3
# -*-coding: utf-8-*-

'''
8.相差为2的两个质数称为孪生质数。例如3和5是一对孪生质数，41和43也是一对孪生质数。那么100～200之间共有多少对孪生质数呢？
'''

def func(m, n):
    if m >= 2 and m < n:
        a = [x for x in range(m, n) if not [y for y in range(2, x) if x % y == 0]] ##zhishu
        ls0 = []
        for i in range(len(a) - 1):
            if a[i+1] - a[i] == 2:
                tp0 = (a[i], a[i+1])
                ls0.append(tp0)
        return ls0
    print('Error')
    return None
