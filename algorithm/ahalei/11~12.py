#!usr/bin/env python3
'''
11.请在123456789中插入3个乘号，使得乘积最大？请问乘积最大是多少？ 
12.请在5483298756中插入3个乘号，使得乘积最大,请问乘积最大是多少？ 
'''

def INT(m, n):
	return int(num_str[m:n+1])
	
def times_max():
    ls = []
    num_str = input('Number is :')
    for m1 in range(len(num_str)-3):
        for m2 in range(m1+1, len(num_str)-2):
            for m3 in range(m2+1, len(num_str)-1):
                r1 = INT(0,m1) * INT(m1+1,m2) * INT(m2+1,m3) * INT(m3+1,len(num_str)-1)
                print('{0}={1}*{2}*{3}*{4}'.format(r1, INT(0,m1), INT(m1+1,m2), INT(m2+1,m3), INT(m3+1,len(num_str)-1)))
                ls.append(r1)
    r2 = max(ls)
    return r2
