# coding=utf-8
# uliontse

'''
迷宫找唯一通路问题。
可升级为找最短路径问题。

方法：
增加左右上下边界n+2,1为墙，0为通路
for...break...else...如果for遍历完没有break过，则执行else。本次实行回退重新选择通路
走过的路变成墙
'''

from pprint import pprint as ppt

def initMaze():
    maze = [[0] * 7 for x in range(5+2)]
    wall = [
        (1,3),
        (2,1),(2,5),
        (3,3),(3,4),
        (4,2),
        (5,4)
    ]

    for i in range(5+2):
        maze[i][0] = maze[i][-1] = 1
        maze[0][i] = maze[-1][i] = 1

    for i,k in wall:
        maze[i][k] = 1

    return maze
#ppt(initMaze())

def path(maze,begin,end):
    i,j = begin
    ei,ej = end

    s = [(i,j)]
    maze[i][j] = 1

    while s:
        i,j = s[-1]
        if (i,j) == (ei,ej):
            break
        for di,dj in [(0,1),(1,0),(-1,0),(0,-1)]:
            if maze[i+di][j+dj] == 0:
                maze[i+di][j+dj] = 1
                s.append((i+di,j+dj))
                print('a: ', s)
                break
        else:
            s.pop()
            print('b: ',s)
            ppt(maze)
    return s


if __name__ == '__main__':
    maze = initMaze()
    ppt(maze)
    print('result: ',path(maze,begin=(1,1),end=(5,5)))
