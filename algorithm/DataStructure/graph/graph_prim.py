# coding=utf-8
# uliontse

import heapq

G = [
    {1:28, 5:10},           # 0  #{邻接点：边权值}
    {0:28, 2:16, 6:14},     # 1
    {1:16, 3:12},           # 2
    {2:12, 4:22, 6:18},     # 3
    {3:22, 5:75, 6:24},     # 4
    {0:10, 4:75},           # 5
    {1:14, 3:18, 4:24},     # 6
    {}  # 无邻接边，是非全连接的图 raise exception
]

def prim(G,begin=6):
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
