'''
梳排序(Comb sort)是一种由Wlodzimierz Dobosiewicz于1980年所发明的不稳定排序算法，并由Stephen Lacey和Richard Box于1991年四月号的Byte杂志中推广。梳排序是改良自泡沫排序和快速排序，其要旨在于消除乌龟，亦即在阵列尾部的小数值，这些数值是造成泡沫排序缓慢的主因。相对地，兔子，亦即在阵列前端的大数值，不影响泡沫排序的效能。

在泡沫排序中，只比较阵列中相邻的二项，即比较的二项的间距(Gap)是1，梳排序提出此间距其实可大于1，改自插入排序的希尔排序同样提出相同观点。梳排序中，开始时的间距设定为阵列长度，并在循环中以固定比率递减，通常递减率设定为1.3。在一次循环中，梳排序如同泡沫排序一样把阵列从首到尾扫描一次，比较及交换两项，不同的是两项的间距不固定于1。如果间距递减至1，梳排序假定输入阵列大致排序好，并以泡沫排序作最后检查及修正。
'''

def comb_sort(L):
    gap = len(L)
    swap = True
    while gap > 1 or swap:
        gap = max(1,int(gap / 1.25))
        swap = False
        for i in range(len(L)-gap):
            j = i + gap
            if L[i] > L[j]:
                L[i],L[j] = L[j],L[i]
                swap = True
    return L
