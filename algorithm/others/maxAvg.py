# coding=utf-8

def maxAverage1(nums, k):
    '求列表中大于等于k个长度的子列表的最大平均值。'
    # O(n**2)
    r = []
    for n in range(k,len(nums)+1):
        for i in range(len(nums) - n + 1):
            r.append(sum(nums[i:i + n]) / n)
    print(r)
    return max(r)

    def maxAverage2(nums, k):
        # update `z`,`r1`.
        z = len(nums)
        r1 = sum(nums[:k])/k
        for n in range(k,z+1):
            for i in range(z - n + 1):
                r2 = sum(nums[i:i + n]) / n
                if r1 < r2: r1 = r2
        return r1

    
if __name__ == '__main__':
    print(maxAverage([-1,-2,-3,-100,-1,-50],4))
