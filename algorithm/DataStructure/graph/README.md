![](https://i.imgur.com/WnX6H20.png)

# *Welcome to [graph](https://en.wikipedia.org/wiki/Graph_(abstract_data_type)) of python !* #

## *图的定义* ##

```python
定义：
图由两个集合组成： 一个由'顶点（vertex）'构成的'有穷非空'集合，和一个由'边（edge）'构成的'有穷允空'集合。

图的分类：
1.有向图
2.无向图
3.边无权值的图
4.边有权值的图

接口：
1.添加顶点
2.删除顶点
3.获得所有顶点
4.添加一条边
5.删除一条边
6.获得所有边
7.判断图是否为空

实现：
1.使用list,set,dict实现图
# 邻接列表（矩阵），邻接集合，邻接加权字典
2.networkx库

应用：
1.图的遍历算法（广度优先bfs[Breadth-first search](少换乘，边数总和最低)、深度优先dfs[Depth-first search]）
2.最小生成树算法（prim算法）
3.最短路径算法（dijkstra算法(路程最短，边权值总和最低)）
4.拓扑排序算法（topsort算法）

```

## *1.图创建的几种形式* ##

```python
# coding=utf-8

'''
a ------- b
|      -  | -
|    -    |    c
|  -      |  -
e ------- d
'''
from pprint import pprint as ppt


'邻接矩阵：'
N = 5
a,b,c,d,e = range(N)
G = [[0] *N for _ in range(N)]

def addEdge(G,v1,v2):
    # 无向图加边
    G[v1][v2] = G[v2][v1] = 1

addEdge(G,a,b)
addEdge(G,a,e)
addEdge(G,b,c)
addEdge(G,b,d)
addEdge(G,b,e)
addEdge(G,c,d)
addEdge(G,d,e)

ppt(G)  # 邻接矩阵，存储无效内容过多


'邻接集合：'
G2 = [{b,e},{c,d,e},{b,d},{b,c,e},{a,b,d}]  # 只存储相应邻接点的集合
print(G2[a])

'邻接加权字典：'
G3 = [{b:1,e:2},{c:3,d:4,e:5},{b:6,d:7},{b:8,c:9,e:10},{a:11,b:12,d:13}]
# {邻接点：边权值}

```

## *2.深度优先VS广度优先(边数最少)* ##

```python
# coding=utf-8

G = [
    {1,2,3},    # 0
    {0,4,6},    # 1
    {0,3},      # 2
    {0,2,4},    # 3
    {1,3,5,6},  # 4
    {4,7},      # 5
    {1,4},      # 6
    {5},        # 7
]

# 深度优先，递归版本
def dfs(G,v,visited=set()):
    print(v)
    visited.add(v)
    for i in G[v]:
        if i not in visited:
            dfs(G,i,visited)

# 深度优先，迭代版本
def dfsIter(G,v):
    visited = set()
    s = [v]
    while s:
        u = s.pop()
        if u not in visited:
            print(u)
            visited.add(u)
            s.extend(G[u])


# 广度优先，类似树的层序遍历
from collections import deque

def bfs(G,v):
    q = deque([v])
    visited = {v}

    while q:
        u = q.popleft()
        print(u)

        for w in G[u]:
            if w not in visited:
                q.append(w)
                visited.add(w)


if __name__ == '__main__':
    # dfs(G,0)
    # dfsIter(G,0)
    bfs(G,0)
```

## *3.最小生成树prim算法* ##

```python
# coding=utf-8

import heapq

G = [
    {1:28, 5:10},           # 0  #{邻接点：边权值}
    {0:28, 2:16, 6:14},     # 1
    {1:16, 3:12},           # 2
    {2:12, 4:22, 6:18},     # 3
    {3:22, 5:75, 6:24},     # 4
    {0:10, 4:75},           # 5
    {1:14, 3:18, 4:24},     # 6
    # {}  # 无邻接边，是非全连接的图 raise exception
]

def prim(G,begin=0):
    edges,res = [],[]
    s = {begin}

    for _ in range(len(G)-1):
        for k,v in G[begin].items():
            heapq.heappush(edges,(v,begin,k))  # 利用堆的从小到大的排序作用
        # print([(x[1],x[2]) for x in edges])
        while edges:
            v,p,q = heapq.heappop(edges)  # 推出左边排序最小的元素
            if q not in s:
                s.add(q)
                res.append(((p,q),v))
                begin = q
                break
        else:
            raise Exception('Not connected graph!')
    return res


if __name__ == '__main__':
    print(prim(G))
    print(sum(x[1] for x in prim(G)))

```

## *4.最短路径算法(边权值总和最低)* ##

```python
# coding=utf-8
'最短路径算法之dijkstra'

import heapq

a,b,c,d,e,f = range(6)
# 邻接加权字典
G = {
    a: {b: 2, c: 1, d: 4, f: 10},
    b: {a: 2, c: 4, e: 3},
    c: {a: 1, b: 4, d: 2, f: 8},
    d: {a: 4, c: 2, e: 1},
    e: {b: 3, d: 1, f: 7},
    f: {a:10, c: 8, e: 7},
}

def dijkstra(G,begin):
    # D = dict(), d[c], ...
    inf = float('inf')
    D = {x: inf for x in G}
    D[begin] = 0
    P = {}
    S = {begin}
    Q = []

    x = begin
    for _ in range(len(G)-1):
        for k,v in G[x].items():
            d = D[x] + G[k][x]
            if D[k] > d:
                D[k] = d
                P[k] = x
                heapq.heappush(Q,(d,k))
        while Q:
            _,x = heapq.heappop(Q)
            if x not in S:
                S.add(x)
                break
        else:
            break
    return (D,P)


if __name__ == '__main__':
    print(dijkstra(G,a))

```

## *5.拓扑排序算法* ##
![](https://i.imgur.com/axgLzRr.jpg)
```python
# coding=utf-8
'''
1：高等数学
2：程序设计
3：离散数学 (1,2) #离散数学课程内容依赖于 高等数学 和 程序设计。
4：数据结构 (2,3)
5：算法分析 (2)
6：编译技术 (4,5)
7：操作系统 (4,9)
8：普通物理 (1)
9：计算机原理 (8)

问：怎样合理排课？
'''

# 有向图：
G = {
    'C1': ['C3','C8'], # C1指向C3和C8，C3和C8依赖于C1.
    'C2': ['C3','C4','C5'],
    'C3': ['C4'],
    'C4': ['C6','C7'],
    'C5': ['C6'],
    'C6': [],
    'C7': [],
    'C8': ['C9'],
    # 'C9': ['C7'],
    'C9': ['C7','C8'], #添加回环，死锁
}

def topsort(G):
    indegree = {k:0 for k in G} #图论之入度
    for v in G.values():
        for k in v:
            indegree[k] += 1
    L = [k for k in G if indegree[k] == 0]

    for i,_ in enumerate(L):
        for k in G[L[i]]:
            indegree[k] -= 1
            if indegree[k] == 0:
                L.append(k)
    return L if len(L) == len(G) else None #如果图中有回环，则返回None。


if __name__ == '__main__':
    print(topsort(G))

```
