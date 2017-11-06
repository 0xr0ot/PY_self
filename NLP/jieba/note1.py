#coding:utf-8
#https://github.com/fxsjy/jieba

## 1.分词
import jieba

seg_list1 = jieba.cut("像计算机科学家一样思考")#精确模式
seg_list2 = jieba.cut("像计算机科学家一样思考",cut_all=True)#全模式
seg_list3 = jieba.cut_for_search("像计算机科学家一样思考")#搜索引擎模式

print(','.join(seg_list1))
print(','.join(seg_list2))
print(','.join(seg_list3))


## 2.词性标注
import jieba.posseg as pseg

words = pseg.cut("像计算机科学家一样思考")
for word,flag in words:
    print(word,flag)


## 3.Tokenize：返回词语在原文的起止位置
result = jieba.tokenize("像计算机科学家一样思考")
for tk in result:
    print("word {0}\t\t begin: {1}\t\t end: {2}".format(tk[0],tk[1],tk[2]))
    

## 4.关键词抽取
import jieba.analyse

sentences = '''《物演通论(第3版)》
    宇宙演运即造成物类衰变，生物进化就导致种系残弱，文明前行则促进入寰危机;精神增益是载体趋弱的反比变量，信息扩张是物演分化的边际效应，
知识拓展是背离本真的天然尺度;社会结构是自然实体结构的一脉延伸，文明现象是生物智质代偿的后续恶果，历史进步是人类自取祸殃的必由之路。
    上述观点无不与当前全人类的各种主流意识形态相左，也无不与当前全世界高度文明发展所致的危机形势(诸如环境污染、资源耗竭、生态破坏、气候异常、
大规模毁灭性武器泛滥以及恐怖主义争端激化等诡异现实)丝丝相扣。读罢此作，不能不令人掩卷长思。故，可视其为"人文存亡之道"的基础理论。
'''

### 4.1 TF-IDF
result1 = jieba.analyse.extract_tags(sentences,topK=5,withWeight=True,allowPOS=('ns', 'n', 'vn', 'v'))
print(result1)

### 4.2 TextRank
result2 = jieba.analyse.textrank(sentences,topK=5,withWeight=True,allowPOS=('ns', 'n', 'vn', 'v'))
print(result2)
