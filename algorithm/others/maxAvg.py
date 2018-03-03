# coding=utf-8

def maxAverage(nums, k):
    '求列表中大于等于k个长度的子列表的最大平均值。'
    # O(n**2)
    r = []
    for n in range(k,len(nums)+1):
        for i in range(len(nums) - n + 1):
            r.append(sum(nums[i:i + n]) / n)
    print(r)
    return max(r)

if __name__ == '__main__':
    print(maxAverage([-1,-2,-3,-100,-1,-50],4))
