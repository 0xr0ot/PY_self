# coding=utf-8
# uliontse

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

