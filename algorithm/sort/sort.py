# coding=utf-8
# uliontse


def quickSort(L):
    if len(L) < 2:
        return L
    else:
        q = L[0]
        less = quickSort([elem for elem in L if elem < q])
        more = quickSort([elem for elem in L if elem > q])
        return less + [q] * L.count(q) + more
