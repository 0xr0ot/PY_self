# coding=utf-8
# uliontse

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



