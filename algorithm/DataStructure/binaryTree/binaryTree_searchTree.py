# coding=utf-8
# uliontse

from collections import OrderedDict


# 层序遍历，高级打印形式
def levelOrder2(node):
    q = [node]
    while q:
        dic = OrderedDict()
        for x in q:
            dic[x] = (x.left,x.right)

        print(dic)  # 层级输出节点
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