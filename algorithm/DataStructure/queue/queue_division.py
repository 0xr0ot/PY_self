# coding=utf-8
# uliontse

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
