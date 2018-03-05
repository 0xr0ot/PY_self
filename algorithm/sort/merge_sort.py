from heapq import merge

def merge_sort(L):
    if len(L) > 1:
        middle = len(L) // 2
        left = merge_sort(L[:middle])
        right = merge_sort(L[middle:])
        return list(merge(left,right))
    return L
