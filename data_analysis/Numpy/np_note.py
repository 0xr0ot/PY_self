# coding=utf-8

import array
import numpy as np

'1. 创建矩阵'

arr1 = [1,2,3] # 无限制
arr2 = array.array('i',[1,2,3]) # 类型限制，索引位置不同类型不能重新赋值，效率高
arr3 = np.array([1,2,3]) # 类型限制，索引位置不同类型不能重新赋值，效率高

print(type(arr2[0]),type(arr3[0]),arr3.dtype)
print('-'*50)

m1 = np.zeros(10)       # 一维数组，尽量不要这样写，默认类型为浮点数
m2 = np.zeros((1,10))   # 二维数组
print(m1.ndim,m2.ndim)  # 1,2
m3 = np.ones(shape=(10,1),dtype=int) # 默认类型为浮点数
m4 = np.full(shape=(10,1),fill_value=6,dtype=int)
print(m1.shape,m2.shape)
print('-'*50)

L1 = list(range(0,10,2))                    # [0, 2, 4, 6, 8]
L2 = np.arange(0.0,1.0,0.2)                 # array([ 0. ,  0.2,  0.4,  0.6,  0.8])
L3 = np.linspace(0,10,num=5,endpoint=False) # array([ 0. ,  0.2,  0.4,  0.6,  0.8]) # 均分数字序列（默认包含头尾）

np.random.seed(1234)
n1 = np.random.randint(4,8,size=(10,1)) # 范围内随机整数
n2 = np.random.random(size=(3,5))       # 0-1范围内浮点数
n3 = np.random.normal(0,1,(2,3))        # 均值为0，方差为1的正态分布
n4 = np.random.randn(2,3)               # 标准正态分布（均值为0，方差为1）


'2.基本操作'

a1 = np.arange(15).reshape(3,5)
a2 = np.arange(15).reshape(3,-1) # 3行即可，但必须能被size整除，不然报错
print(a1.ndim,a1.shape,a1.size)  # 维度，（行，列），长度（行乘以列）
print(a1[0][0] == a1[(0,0)])     # 推荐arr[(x,y,z)]
print(a1[:2,:3] != a1[:2][:3])   # a1[:2][:3] == a1[:2]
print(a1[::-1,::-1])             # 对行列都进行 逆序

a3 = a2.copy()  # a3 = a2, 对a3,a2的操作都会互相影响，所以必须用copy函数

a4 = np.concatenate([a1,a2])         # 上下拼接，行变长列不变，默认axis=0. sql_union
a5 = np.concatenate([a1,a2],axis=1)  # like function pandas.concat(). sql_join

a6 = np.full((3,3),3)
a7 = np.full((2,3),2)
a8 = np.full((3,2),1)
a9 = np.vstack([a6,a7])          # Stack arrays in sequence vertically (row wise).
a10= np.hstack([a6,a8])          # Stack arrays in sequence horizontally (column wise).


A1,A2 = np.split(a1,[2],axis=0)
high,low = np.vsplit(a1,[2])
left,right = np.hsplit(a1,[2])

X,y = np.hsplit(a1,[-1])         # 常用（属性，标签）分割

'3.矩阵运算'
print(a1 * 2, np.abs(a1), np.exp(a1), np.power(3,a1), np.log2(a1), np.log10(a1))

A = np.array([1,2,3,4]).reshape(2,2)
B = np.full((2,2),10)
print(A+B, A-B, A*B)  # shape须相同
print(np.dot(A,B))
print(A.T)

# broadcasting
V = np.array([1,2])
print(V+A, np.vstack([V] * A.shape[0]) + A, np.tile(V,(2,1)) + A)

invA = np.linalg.inv(A) # 逆矩阵，必须为方阵
print(np.dot(A,invA))

M = np.arange(6).reshape(2,3)
pinvM = np.linalg.pinv(M) # 伪逆矩阵，非方阵求逆. 奇异值分解（SVD）
print(np.dot(M,pinvM), M.dot(pinvM)) # M.dot(pinvM) 会改变M ???? 并没有
print(M)

'4.聚合操作'
print(np.sum(A), np.max(A), A.sum(), A.max())
print(np.sum(A,axis=0))
print(np.sum(A < 4), np.count_nonzero(A < 4))
print(np.prod(A), np.mean(A), np.median(A)) # np.prod() 连乘
print(np.percentile(A,q=50), np.median(A), np.percentile(A,q=25), np.percentile(A,q=75)) # 四分位数

xx = np.random.normal(0,1,size=int(1e+6))
print(np.mean(xx), np.std(xx))


'5.索引与排序'
row,col = [0,1,2],[1,2,3]
print(a1[row,col])
print(a1[row,[False,True,False,False,False]])


print(np.argmax(xx), np.argmin(xx)) # 最大值索引值

mm = np.arange(10)
np.random.shuffle(mm) # 随机打乱mm的顺序
# mm = array([5, 6, 3, 9, 8, 2, 4, 0, 7, 1])
print(np.sort(mm), mm.sort())
print(np.sort(A) == np.sort(A,axis=1)) # 默认为列排序
print(np.argsort(mm))
print(np.partition(mm,3), np.argpartition(mm,3)) # arg 索引值

L = [1,4,3,2,6,5]
print(sorted(L)) # L.sort()
print(sorted(range(len(L)),key=L.__getitem__))

# funcy index:
print(np.sum(A < 4), np.count_nonzero(A < 4))
print(np.any(A >=0), np.all(A >= 0))

print(np.sum(A % 2 == 0, axis=1))
print(np.count_nonzero(A % 2 == 0, axis=1))

# &: 位用算符； &&: 条件用算符
print(np.sum((A % 2 == 0) & (A > 2)))

print(A[A < 5], A[A % 2 == 0]) # return np.array.ndim == 1

