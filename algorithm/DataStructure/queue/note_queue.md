![](https://i.imgur.com/WnX6H20.png)

# *Welcome to [queue](https://en.wikipedia.org/wiki/Queue_(abstract_data_type)) of python !* #

## *（双端）队列* ##

```python
定义：
队列是一个特殊的有序表，其插入操作在表的一端进行，而删除操作在表的领一端进行。插入端为队尾，删除端为队首。
from collections import deque
q1 = deque([1,2,3])
q2 = deque([1,2,3],5)#容量为5.

操作：
1.入队： 
	q.append(4), q.appendleft(0)
	q.extend([4,5]), q.extendleft([-1,0])
2.出队： q.pop(), q.popleft()
3.清空队列： q.clear()
4.判断队列是否为空： not q
5.判断队列是否为满： q.maxlen == len(q)
6.当前队列的长度： len(q)
7.队列的容量： q.maxlen
8.统计队列内元素个数：
	q.count(1)
	from collections import Counter
	Counter(q)
9.队列倒序： q.reverse()
10.旋转（想象'队列头尾相接',末尾成为第一个元素，其他元素依次向后移动）：
	q.rotate(), q.rotate(1), q.rotate(-1), q.rotate(len(q))

应用：
二项式系数、划分无冲突子集、数字变换。

```

## *1、杨辉三角（二项式幂的系数）* ##

```python
# coding=utf-8

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

```

## *2、划分无冲突子集* ##

```python
# coding=utf-8

'''
对互相有攻击性的动物分笼，笼要尽可能的少。
'''

from collections import deque,Iterable
from pprint import pprint as ppt

def initM():
    attackGroup = {
        (0,5),(1,0),(1,4),(1,5),(1,7),(1,8),
        (3,4),(4,8),(5,2),(5,6),(6,2),(6,4),(8,3)
    }
    # 假设每个动物都有攻击对象或被攻击对象，都在attackGroup.
    # 现确定动物数量：
    def oneDim(L):
        for each in L:
            if not isinstance(each, Iterable):
                yield each
            else:
                yield from oneDim(each)
    N = len(set(oneDim(attackGroup)))
    M = [[0] * N for _ in range(N)]
    for i,j in attackGroup:
        M[i][j] = M[j][i] = 1
    return M


def division(M,n=None):
    if not n: n = len(M) #如果存在没有互相攻击的动物，那一般会给出动物数量
    res = []
    q = deque(range(n))
    pre = n

    while q:
        cur = q.popleft()
        if pre >= cur:
            res.append([])

        for i in res[-1]:
            if M[cur][i] == 1:
                q.append(cur)
                break
        else:
            res[-1].append(cur)
        pre = cur
    return res


if __name__ == '__main__':
    M = initM()
    ppt(M)
    print(division(M))

```

## *3、数字变换* ##

```python
# coding=utf-8

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
        if v > 0: # 任何时候都能进行减法运算
            if v-1 not in checked:
                q.append((v-1,n+1))
                checked.add(v-1)
    # return n


if __name__ == '__main__':
    print(a_to_b(5,9))

```