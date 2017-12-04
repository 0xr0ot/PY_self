# coding=utf-8

from nltk.book import *

## 1.频率分布
f = FreqDist(text1) # 创建给定样本的频率分布
f.inc(text2) # 增加样本
r1 = f['monstrous'] # 计数给定样本出现的次数
r2 = f.freq('monstrous') # 给定样本的频率
r3 = f.N() # 样本总数
r4 = [w for w in f.keys()] # 以频率递减顺序排序的样本链表
r5 = f.max() # 数值最大的样本
f.tabulate() # 绘制频率分布表
f.plot() # 绘制频率分布图
f.plot(cumulative=True) # 绘制累积频率分布图

## 2.慈会比较运算符
sen,t = '7Basket','t'

sen.startswith(t)
sen.endswith(t)
if t in sen: print(True)
sen.islower()
sen.isupper()
sen.isalpha()
sen.isalnum()
sen.isdigit()
sen.istitle()

#TODO
