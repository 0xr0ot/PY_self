'''
希尔排序是一种插入排序算法，它出自D.L.Shell，因此而得名。Shell排序又称作缩小增量排序。Shell排序的执行时间依赖于增量序列。

先取一个小于n的整数d1作为第一个增量，把文件的全部记录分成d1个组。所有距离为dl的倍数的记录放在同一个组中。先在各组内进行直接插入排序;然后，取第二个增量
d2<d1重复上述的分组和排序，直至所取的增量dt=1(dt<dt-l<;…<d2<d1)，即所有记录放在同一组中进行直接插入排序为止。

该方法实质上是一种分组插入方法。
'''

def shell_sort(L):
    middle = len(L) // 2
    while middle:
        for i,e in enumerate(L):
            while i > middle and L[i-middle] > e:
                L[i] = L[i-middle]
                i -= e
            L[i] = e
        middle = 1 if middle == 2 else int(middle * 5/11) #
    return L
