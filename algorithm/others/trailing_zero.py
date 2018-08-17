coding=utf-8

def naive_match(t,p):
    m,n = len(p),len(t)
    i,j = 0,0
    while i < m and j < n:
        if p[i] == t[j]:
            i,j = i+1, j+1
        else:
            i,j = 0, j-i+1
    if i == m:
        return j-i
    return -1



def trailingZeros(n):
    # write your code here, try to do it without arithmetic operators.
    m = 0
    while n:
        m += n // 5
        n //= 5
    return m

print(trailingZeros(30))



def factor(n):
    m = 1
    while n > 1:
        m *= n
        n -= 1
    return m

for x in range(10,101,10):
    print(factor(x))


def judgeChinese(word:str,punctuation_filter=True):
    English_punctuation = '''`~!@#$%^&*()_+-=[]\{}|;':",./<>?'''
    Chinese_punctuation = '''·~！@#￥%……&*（）——+-=【】、{}|；‘’：“”，。《》？'''
    n = 0
    for per_word in word:
        if u'\u4e00' <= per_word <= u'\u9fff':
            n += 1
        elif punctuation_filter is True:
            if per_word in Chinese_punctuation:
                n += 1
        else:
            if per_word in set(Chinese_punctuation + English_punctuation):
                n += 1
    return n == len(word)
