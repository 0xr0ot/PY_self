# coding=utf-8
# uliontse

import heapq


'最短路径算法之dijkstra'
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




