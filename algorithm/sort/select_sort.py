def select_sort(L):
    for i,e in enumerate(L):
        mn = min(range(i,len(L)), key=L.__getitem__) # 获得`索引i`之后切片的最小值的`索引mn`。
        L[i],L[mn] = L[mn],e
    return L
