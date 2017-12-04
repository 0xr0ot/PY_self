# coding=utf-8

from nltk.book import *


# 词语索引，return: matches 和上下文
r1 = text1.concordance('monstrous')

# 上下文的关键词
r2 = text1.similar('monstrous')

# 多词索引共同上下文
r3 = text2.common_contexts(['monstrous','very'])

# 词汇位置分布图
text4.dispersion_plot(['citizens','democracy','freedom','duties','America'])


# 词汇丰富度(lexical_diversity)
r5 = len(text3) / len(set(text3))

# 词频,词占比
r6 = text3.count('smote')
r7 = text5.count('lol')*100 / len(text5)

# 词频字典
f1 = FreqDist(text1)
v1 = f1.keys()
r8 = f1.get('whale')

# 累积频率图
f1.plot(50,cumulative=True)

# 只出现一次的词
r9 = f1.hapaxes()

# 词长度选择(细粒度选择,Fine-Grained)
V = set(text1)
r10 = set([w for w in V if len(w) > 15])

# 词长且词频
f2 = FreqDist(text5)
r11 = sorted([w for w in set(text5) if len(w) > 7 and f2[w] > 7])

# 双连词,搭配
text4.collocations()

# 过滤分字母元素
r12 = len(set([word.lower() for word in text1 if word.isalpha()]))

#TODO
