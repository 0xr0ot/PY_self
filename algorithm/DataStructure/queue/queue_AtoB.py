# coding=utf-8
# uliontse

'''
数字a只能通过[`-1`,`+1`,`*2`]这三种运算得到b，一般地，b>a，求最少运算步骤。
'''
from collections import deque

def a_to_b(a,b):
    q = deque([(a,0)])
    checked = {a}

    while True:
        print(q)
        print(checked)
        v,n = q.popleft()
        # if v == b:
        #     break
        for i,j in q: # 不等正确答案推到队列首部，即可得到答案。
            if i == b:
                return j
        if v < b:
            if v+1 not in checked:
                q.append((v+1,n+1))
                checked.add(v+1)
            if v*2 not in checked:
                q.append((v*2,n+1))
                checked.add(v*2)
        if v > 0:
            if v-1 not in checked:
                q.append((v-1,n+1))
                checked.add(v-1)
    # return n


if __name__ == '__main__':
    print(a_to_b(5,9))
