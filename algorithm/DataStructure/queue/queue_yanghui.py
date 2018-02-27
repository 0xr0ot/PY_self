# coding=utf-8
# uliontse

'''
杨辉三角：第0行为(a+b)**0的二项式所有系数，第1行为(a+b)**1的二项式所有系数，第k行为(a+b)**k的二项式所有系数。
       1
      1  1
     1  2  1
    1  3  3  1
'''
from collections import deque

def yanghui(k):
    # 0,1,2,...,k,...
    q = deque([1])

    for i in range(k):
        for _ in range(i):
            q.append(q.popleft() + q[0])
        q.append(1)
    return list(q)


if __name__ == '__main__':
    print(yanghui(0))
