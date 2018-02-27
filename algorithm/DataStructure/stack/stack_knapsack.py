# coding=utf-8
# uliontse

'''
问题：背包能放10kg的物品，现有重量为1,2,3,4,5,...kg的物品，求装满背包的所有解。
'''
def knapsack(total,L):
    s = []
    ss = []
    ind = 0

    while s or ind < len(L):
        while total > 0 and ind < len(L):
            if total >= L[ind]:
                s.append(ind)
                total -= L[ind]
            ind += 1

        if total == 0:
            ss.append(tuple([L[x] for x in s])) #s.pop()会影响ss,因为ss指向s而已。

        ind = s.pop()
        total += L[ind]
        ind += 1
    return ss


if __name__ == '__main__':
    print(knapsack(10,[1,8,4,3,5,2]))
    print(knapsack(10,[1,2,3,4,5,6,7,8,9]))
    
