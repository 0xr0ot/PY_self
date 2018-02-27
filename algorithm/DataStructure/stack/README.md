![](https://i.imgur.com/WnX6H20.png)

# *Welcome to [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) of python !* #

## *栈* ##

```python
定义：
栈是一个特殊的有序表，其插入和删除操作都在一端（栈顶）进行。
'LIFO: last input first output.'
L = list()
L = []

操作：
1.入栈： L.append()
2.出栈： L.pop()
3.是否空栈： not L
4.栈的长度： len(L)
5.栈顶元素： L[-1]

应用：
括号匹配、迷宫问题、后缀表达式求值、背包问题。

```

## *1、括号匹配* ##

```python
# coding=utf-8
'''判断括号是否完整'''

LEFT = ['(','[','{']
RIGHT = [')',']','}']

def match(expr):
    s = []

    for i in expr:
        if i in LEFT: s.append(i)
        elif i in RIGHT:
            if not s: return False
            elif not 1 <= ord(i) - ord(s[-1]) <= 2: return False
            s.pop()
    return not s


if __name__ == '__main__':
    print(match('(){}[][]'))
    # print([ord(x) for x in LEFT])
    # print([ord(y) for y in RIGHT])

```

## *2、迷宫问题* ##

```python
# coding=utf-8

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

```

## *3、后缀表达式* ##
```python
# coding=utf-8

operators = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: a/b
}

def postfixExpression(expr):
    s = []
    tokens = expr.split()

    for token in tokens:
        if token.isdigit():
            s.append(int(token))
        elif token in operators:
            f = operators[token]
            b = s.pop()
            a = s.pop()
            s.append(f(a,b))
    return s.pop()


if __name__ == '__main__':
    print(postfixExpression('2 3 4 * +'))

```

## *4、背包问题* ##

```python
# coding=utf-8
'''
问题：背包能放10kg的物品，现有重量为1,2,3,4,5,...kg的物品，求装满背包的所有解。
'''
def knapsack(total,L):
    s = []
    ss = []
    ind = 0

    while s or ind < len(L):
        while total > 0 and ind < len(L):
            if total >= L[ind]:
                s.append(ind)
                total -= L[ind]
            ind += 1

        if total == 0:
            ss.append(tuple([L[x] for x in s])) #s.pop()会影响ss,因为ss指向s而已。

        ind = s.pop()
        total += L[ind]
        ind += 1
    return ss


if __name__ == '__main__':
    print(knapsack(10,[1,8,4,3,5,2]))
    print(knapsack(10,[1,2,3,4,5,6,7,8,9]))
```
