def judgeChinese(word):
    n = 0
    for per_word in word:
        if u'\u4e00' <= per_word <= u'\u9fff':
            n += 1
    return n == len(word)
