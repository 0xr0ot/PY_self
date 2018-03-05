def insert_sort(L):
    for i in range(1,len(L)):
        x = L[i]
        j = i
        while j > 0 and L[j-1] > x:
            L[j] = L[j-1]
            j -= 1
        L[j] = x
    return L
	

def insert_sort_binSearch(L):
    for i in range(1,len(L)):
        key = L[i]
        low,up = 0,i
        while up > low:
            middle = (low + up) // 2 #binSearch
            if L[middle] < key:
                low = middle + 1
            else:
                up = middle
        # print(L[:low],[key],L[low:i], L[i+1:])
        L = L[:low] + [key] + L[low:i] + L[i+1:]
    return L


import bisect
def insert_sort_bisect(L):
    for i in range(1, len(L)):
        bisect.insort(L, L.pop(i), 0, i)
    return L
