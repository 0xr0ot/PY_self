# coding=utf-8
# uliontse

def reverseList(L):
    i,j = 0,len(L)-1
    while i < j:
        L[i],L[j] = L[j],L[i]
        i,j = i+1,j-1
    return L
    
# 2
newList = reversed(L)
