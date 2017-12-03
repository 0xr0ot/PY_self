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
