# coding=utf-8
# uliontse

'''
           A
    B            C
     D        E    F
            G     H  I

先序遍历：ABDCEGFHI
中序遍历：BDAGECHFI
后序遍历：DBGEHIFCA

'''

import time
from collections import deque,OrderedDict


class TreeNode:
    def __init__(self,data,left=None,right=None):
        self.data = data
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.data)

def createTree():
    A,B,C,D,E,F,G,H,I = [TreeNode(x) for x in 'ABCDEFGHI']
    A.left = B
    A.right = C
    B.right = D
    C.left = E
    C.right = F
    E.left = G
    F.left = H
    F.right = I
    # print(C.left.data)
    # print(C.right)
    return A

# 递归遍历
def preOrder(node):
    if node:
        print(node)
        preOrder(node.left)
        preOrder(node.right)

def inOrder(node):
    if node:
        inOrder(node.left)
        print(node)
        inOrder(node.right)

def postOrder(node):
    if node:
        postOrder(node.left)
        postOrder(node.right)
        print(node)

# 循环遍历
def preOrderIter(node):
    s = []

    while True:
        while node:
            print(node)
            s.append(node)
            node = node.left
        if not s:
            break
        node = s.pop().right # 回溯方法

# 层序遍历
def levelOrder(node):
    q = deque([node])
    while q:
        node = q.popleft()
        print(node,node.left,node.right)

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)

# 层序遍历，高级打印形式
def levelOrder2(node):
    q = [node]

    while q:
        dic = OrderedDict()
        for x in q:
            dic[x] = (x.left,x.right)
        print(dic)

        q.clear()
        for x in dic.keys():
            if x.left:
                q.append(x.left)
            if x.right:
                q.append(x.right)

# 递归方法：
def depth(node):
    if node:
        dl = depth(node.left)
        dr = depth(node.right)
        # print('dr: ',dr)
        # print('dl: ',dl)
        # return (dl,dr,)
        return max(dl,dr)+1
    return 0

# 循环方法：
def depth2(node):
    q = deque([(node,1)])
    while q:
        node,d = q.popleft()
        if node.left:
            q.append((node.left,d+1))
        if node.right:
            q.append((node.right,d+1))
    return d

# 拷贝二叉树：
def copyTree(node):
    if node:
        lt = copyTree(node.left)
        rt = copyTree(node.right)
        return TreeNode(node,lt,rt)
    return



if __name__ == '__main__':
    root = createTree()

    # preOrder(root)            #先序遍历，递归方法
    # inOrder(root)             #中序遍历，递归方法
    # postOrder(root)           #后序遍历，递归方法
    #
    # preOrderIter(root)        #先序遍历，循环回溯
    #
    # levelOrder(root)          #层序遍历，循环方法
    levelOrder2(root)           #层序遍历，高级打印
    #
    # print(depth(root))        #树的深度，递归方法
    # print(depth2(root))       #树的深度，循环方法
    #
    # newTree = copyTree(root)  #树的拷贝，递归方法
    # levelOrder(newTree)

