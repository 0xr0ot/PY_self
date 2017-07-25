# *Welcome to [Naive Bayes classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier) !*
| Team|[qxiu_BI](http://bi.qxiu.com/)|
| ---  | ---  |
| Author | ulion.tse|
| Date | 2017-07-25 |

## *1.认识[贝叶斯](https://en.wikipedia.org/wiki/Bayesian)*：
- ##### 历史
贝叶斯学派很古老，但是从诞生到一百年前一直不是主流。主流是频率学派。频率学派的权威皮尔逊和费歇尔都对贝叶斯学派不屑一顾，但是贝叶斯学派硬是凭借在现代特定领域的出色应用表现为自己赢得了半壁江山。被频率学派攻击的主要是先验概率，一般来说先验概率就是我们对于数据所在领域的历史经验，但是这个经验常常难以量化或者模型化，于是贝叶斯学派大胆的假设先验分布的模型，比如[正态分布]((https://en.wikipedia.org/wiki/Normal_distribution))，[beta分布](https://en.wikipedia.org/wiki/Beta_distribution)等。这个假设一般没有特定的依据，因此一直被频率学派认为很荒谬。[<<<更多](https://www.zhihu.com/question/20587681)
- ##### 思想
贝叶斯学派的思想可以概括为[先验概率](https://en.wikipedia.org/wiki/Prior_probability)+数据=[后验概率](https://en.wikipedia.org/wiki/Posterior_probability)。也就是说我们在实际问题中需要得到的[后验概率](https://en.wikipedia.org/wiki/Posterior_probability)，可以通过[先验概率](https://en.wikipedia.org/wiki/Prior_probability)和数据一起综合得到。
- ##### 应用
比如`垃圾邮件分类`，`文本分类`。
- ##### 过程
开始-->输入测试集及样本特征-->计算出所有的K个条件概率-->得出最大的条件概率对应的类别-->结束

## *2.naive_bayes ----sklearn --python*

- #### *GaussianNB*
| name | apply | attrs |
|------|-------|-------|
| 先验为[高斯分布](https://en.wikipedia.org/wiki/Normal_distribution)的朴素贝叶斯 | 样本特征的分布大部分是`连续值` | `GaussianNB(priors=None)` |

- #### *MultinomialNB*
| name | apply | attrs |
|------|-------|-------|
| 先验为[多项式分布](https://en.wikipedia.org/wiki/Multinomial_distribution)的朴素贝叶斯 | 样本特征的分布大部分是`多元离散值` | `MultinomialNB(alpha=1.0,fit_prior=True,class_prior=None)` |

- #### *BernoulliNB*
| name | apply | attrs |
|------|-------|-------|
| 先验为[伯努利分布](https://en.wikipedia.org/wiki/Bernoulli_distribution)的朴素贝叶斯 | 样本特征的分布大部分是`二元离散值`或者很稀疏的`多元离散值` | `BernoulliNB(alpha=1.0,fit_prior=True,class_prior=None,binarize=0.0)` |


- *Talk is chep, show me code:*
```python
import numpy as np
from sklearn.naive_bayes import GaussianNB,MultinomialNB,BaseDiscreteNB,BernoulliNB

X = np.array([[-3,-3],[-2,-2],[-1,1],[1,-1],[2,2],[3,3]])#样本
y = np.array([0,0,0,1,1,1])#样本对应的标签

clf = GaussianNB()#选择模型
clf.fit(X,y)#监督学习
pred = clf.predict([0,0])#预测[0,0]的标签

pred_proba = clf.predict_proba([0,0]) #测试集样本在各个类别上预测的概率，越接近1越好
pred_log_proba = clf.predict_log_proba([0,0])#测试集样本在各个类别上预测的概率的一个对数转化
print(pred)
print(pred_proba)
print(pred_log_proba)
```

```python
>>>[0]#预测的标签结果
>>>[[ 0.5  0.5]]
>>>[[-0.69314718 -0.69314718]]
```

## *3.navie_bayes优缺点总结*
- #### Advantage
1. 朴素贝叶斯模型发源于古典数学理论，有稳定的分类效率。
2. 对小规模的数据表现很好，能个处理多分类任务，适合增量式训练，尤其是数据量超出内存时，我们可以一批批(chuncked)的去增量训练`clf.partial_fit(X,y)`。
3. 对缺失数据不太敏感，算法也比较简单，常用于文本分类。
- #### Disadvantage
1. 理论上，朴素贝叶斯模型与其他分类方法相比具有最小的误差率。但是实际上并非总是如此，这是因为朴素贝叶斯模型**假设属性之间相互独立**，这个假设在实际应用中往往是不成立的，在属性个数比较多或者属性之间相关性较大时，分类效果不好。
2. 需要知道先验概率，且先验概率很多时候取决于假设，假设的模型可以有很多种，因此在某些时候会由于假设的先验模型的原因导致预测效果不佳。
3. 由于通过先验和数据来决定后验的概率从而决定分类，所以人为分类决策存在一定的错误率。
4. 对输入数据的表达形式很敏感。
