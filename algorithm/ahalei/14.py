#!usr/bin/env python3
#-*-coding: utf-8-*-

'''
14.请将1~9这9个阿拉伯数字分别填入9个□中。每个数字只能使用一次。使得等式成立。 
□□□+□□□=□□□ 
例如173+286=459就是一个合理的组合，请问一共所有少种合理的组合？ 
注意：173+286=459 与 286+173=459 是同一种组合！
'''

def is_same(num_1, num_2, freq):
    ''' Judge the elements of two numbers whether they are same or not!
        Different method of find same element  ---->ahalei_15
    '''
    for i in range(freq):
        for j in range(freq):
            if str(num_1)[i] == str(num_2)[j]:
                return True
            elif i != j and str(num_1)[i] == str(num_1)[j]:
                return True
            elif i != j and str(num_2)[i] == str(num_2)[j]:
                return True
                
def has_zero(num):
    ''' Judge var_number whether it has 0 or not!
    '''
    for k in str(num):
        if k == str(0):
            return True 
        ##else <------Be careful!
		
def main():
    size = 0
    for a in range(100, 1000):
        for b in range(100, 1000):
            if (is_same(a, b, 3) is True) or (has_zero(a) is True) or (has_zero(b) is True):
                continue
            else:
                for c in range(100, 1000):
                    if (is_same(a, c, 3) is True) or (is_same(b, c, 3) is True) or (has_zero(c) is True):
                        continue
                    elif a+b == c:
                        size += 1
                        print('{0}={1}+{2}...............size is {3}'.format(c, a, b, size))
    r = size/2
    return r
