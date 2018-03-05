def quick_sort(L):
    if len(L) < 2:
        return L
    else:
        q = L[0]
        less = quick_sort([elem for elem in L if elem < q])
        more = quick_sort([elem for elem in L if elem > q])
        return less + [q] * L.count(q) + more
