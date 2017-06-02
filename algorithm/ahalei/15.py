#!usr/bin/env python3
# -*-coding: utf-8-*-

def is_same(num_1, num_2, freq_1, freq_2):
    ''' Judge the elements of two numbers whether they are same or not!
        Different method of finding same element. ---->ahalei_14
    '''
    def ls_alpha(num):
        ''' Prepare for finding same element.
        '''
        return list(str(num))
    for i in range(freq_1):
        for j in range(freq_2):
            if str(num_1)[i] == str(num_2)[j]:
                return True
            elif len(ls_alpha(num_1)) != len(list(set(ls_alpha(num_1)))):
                return True
            elif len(ls_alpha(num_2)) != len(list(set(ls_alpha(num_2)))):
                return True

def has_zero(num):
    ''' Judge var_number whether it has 0 or not!
    '''
    for k in str(num):
        if k == str(0):
            return True

def main():
    size = 0
    for a in range(10, 100):
        for b in range(100, 1000):
            if is_same(a, b, 2, 3) is True or has_zero(a) is True or has_zero(b) is True:
                continue
            else:
                for c in range(1000, 10000):
                    if is_same(a, c, 2, 4) is True or is_same(b, c, 3, 4) is True or has_zero(c) is True:
                        continue
            elif a*b == c:
                size += 1
                print('{0}={1}*{2}...............size is {3}'.format(c, a, b, size))
    return size
