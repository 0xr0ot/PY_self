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
    # O(n**2)
    z = len(nums)
    r1 = sum(nums[:k])/k
    for n in range(k,z+1):
        for i in range(z - n + 1):
            r2 = sum(nums[i:i + n]) / n
            if r1 < r2: r1 = r2
    return r1


def maxAverage(nums, k):
    # 求列表中大于等于k个长度的子列表的最大平均值。
    # O()
    def search(nums,k,mid):
        z = len(nums)
        m = 0
        s = [0] * (z+1)
        for i in range(1,z+1):
            s[i] = s[i-1] + nums[i-1] - mid
            if i >= k and s[i] >= m:
                return True
            if i >= k:
                m = min(m,s[i-k+1])
        return False

    high,low = 1e-20,-1e20
    z = len(nums)
    for i in range(z):
        if nums[i] > high:
            high = nums[i]
        if nums[i] < low:
            low = nums[i]

    while high - low >= 1e-6:
        mid = (high + low) / 2
        if search(nums,k,mid):
            low = mid
        else:
            high = mid
    return high

    
if __name__ == '__main__':
    print(maxAverage([-1,-2,-3,-100,-1,-50],4))
