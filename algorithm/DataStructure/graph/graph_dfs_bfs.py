# coding=utf-8
# uliontse

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