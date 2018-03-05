'''
基数排序(radix sort)属于"分配式排序"(distribution sort)，又称"桶子法"(bucket sort)或bin sort，顾名思义，它是透过键值的部份资讯，将要排序的元素
分配至某些"桶"中，藉以达到排序的作用，基数排序法是属于稳定性的排序，其时间复杂度为O (nlog(r)m)，其中r为所采取的基数，而m为堆数，在某些时候，基数排序法
的效率高于其它的稳定性排序法。

时间效率:设待排序列为n个记录，d个关键码，关键码的取值范围为radix，则进行链式基数排序的时间复杂度为O(d(n+radix))，其中，一趟分配时间复杂度为O(n)，一
趟收集时间复杂度为O(radix)，共进行d趟分配和收集。 空间效率:需要2*radix个指向队列的辅助空间，以及用于静态链表的n个指针。
'''

def radix_sort(L,base=10): # bucket_sort
    def list_to_bucket(L,base,iteration):
        bucket = [[] for _ in range(base)]
        for num in L:
            digit = (num // (base ** iteration)) % base # 最低位优先(Least Significant Digit first)法，简称LSD法
            bucket[digit].append(num)
        # print(bucket)
        return bucket

    def bucket_to_list(bucket):
        nums = []
        for bkt in bucket:
            for e in bkt:
                nums.append(e)
        return nums

    it = 0
    while base ** it <= max(L):
        L = bucket_to_list(list_to_bucket(L,base,it))
        it += 1
    return L
