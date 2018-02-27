# coding=utf-8
# uliontse


# 求n个节点的不同二叉树的组合个数
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