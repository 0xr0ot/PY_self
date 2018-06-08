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
