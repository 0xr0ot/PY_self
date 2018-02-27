![](https://i.imgur.com/WnX6H20.png)

# *Welcome to [binary tree](https://en.wikipedia.org/wiki/Binary_tree) of python !* #

## *二叉树* ##

```python
定义：
二叉树是有限多个节点的集合，这个集合可能是
1.空集
2.由一个根节点，和两棵互不相交的、分别称之为左子树和右子树的二叉树组成。

操作：
1.创建
2.遍历（先序、中序、后序、层序）（递归、循环）
3.求二叉树的深度（递归、循环）
4.拷贝一棵二叉树
5.求N个节点的不同二叉树个数

应用：
二叉搜索树
1.插入
2.搜索
3.删除
```

## *1.创建，遍历，深度，拷贝* ##

```python
# coding=utf-8

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


def levelOrder(node):
    q = deque([node])
    while q:
        node = q.popleft()
        print(node,node.left,node.right)

        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)


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


def depth(node):
    if node:
        dl = depth(node.left)
        dr = depth(node.right)
        # print('dr: ',dr)
        # print('dl: ',dl)
        # return (dl,dr,)
        return max(dl,dr)+1
    return 0


def depth2(node):
    q = deque([(node,1)])
    while q:
        node,d = q.popleft()
        if node.left:
            q.append((node.left,d+1))
        if node.right:
            q.append((node.right,d+1))
    return d


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

```

## *2.求N个节点的不同二叉树个数* ##

```python
# coding=utf-8


# 递归方法
def count(n):
    # root: 1
    # left: k, 定义域：[0,n-1]
    # right: n-1-k
    if n:
        v = 0
        for i in range(n):
            v += count(i) * count(n-1-i)
        return v
    return 1  # if n == 0


# 利用缓存减小重复计算量
def count2(n):
    v = count2.cache.get(n,0)
    # get(...) method of builtins.dict instance
    # D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.

    if not v:
        for i in range(n):
            v += count2(i) * count2(n-1-i)
        count2.cache[n] = v
        return v
    return v
count2.cache = {0: 1}  #空二叉树的个数唯一


if __name__ == '__main__':
    print(count(5))
    print(count2(100))

```

## *3.插入、搜索、删除* ##

```python
# coding=utf-8

from collections import OrderedDict


# 层序遍历，高级打印
def levelOrder2(node):
    q = [node]
    while q:
        dic = OrderedDict()
        for x in q:
            dic[x] = (x.left,x.right)

        print(dic) # 层级输出节点
        q.clear()

        for x in dic.keys():
            if x.left:
                q.append(x.left)
            if x.right:
                q.append(x.right)

#################################################

class TreeNode:
    def __init__(self,data,left=None,right=None):
        self.data = data
        self.left = left
        self.right = right

    def __repr__(self):
        return str(self.data)

##################################################

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def search(self,k):
        node,_ = self._search(k)
        return node

    def _search(self,k):
        parent = None
        node = self.root
        while node and node.data != k:
            parent = node
            if k < node.data:
                node = node.left
            else:
                node = node.right
        return node,parent

    def insert(self,k):
        node,parent = self._search(k)
        if not node:
            node = TreeNode(k)
            if not parent:
                self.root = node
            elif k < parent.data:
                parent.left = node
            else:
                parent.right = node
        return  # if node:

    def delete(self,k):
        pass


if __name__ == '__main__':
    bsTree = BinarySearchTree()
    for i in [10,5,15,1,2,8,12]:
        bsTree.insert(i)
    # levelOrder2(bsTree.root)
    print(bsTree.search(15))

```
