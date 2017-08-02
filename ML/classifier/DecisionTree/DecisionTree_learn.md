# *Welcome to [DecisionTree](https://en.wikipedia.org/wiki/Decision_tree) !*

| Team|[qxiu_BI](http://bi.qxiu.com/)|
| :---:  | :---:  |
| Author | ulion.tse|
| Date | 2017-08-02 |

## *一. 决策树在[sklearn](http://scikit-learn.org/stable/index.html)中的运用*
- #### *[DecisionTree](http://scikit-learn.org/stable/modules/tree.html)*
1. *Information：*
```python
'''
1. ID3（Iterative Dichotomiser 3）是由罗斯奎因兰（Ros Quinlan）于1986年开发的。该算法创建一个多路树，找到每个节点（即以贪婪的方式）分类特征，这将产生分类目标的最大信息增益。树生长到最大尺寸，然后通常应用修剪步骤，以提高树的概括性来看待数据的能力。
2. C4.5是ID3的后继者，并通过动态定义将连续属性值分割成一组离散的间隔的离散属性（基于数字变量），消除了特征必须是分类的限制。 C4.5将训练的树（即，ID3算法的输出）转换成if-then规则的集合。然后评估每个规则的这些准确性以确定应用它们的顺序。如果规则的准确性没有改善，则通过删除规则的前提条件来完成修剪。
3. C5.0是Quinlan根据专有许可证发布的最新版本。它使用更少的内存，并建立比C4.5更小的规则集，同时更准确。
4. CART（分类和回归树）与C4.5非常相似，但它不同之处在于它支持数值目标变量（回归），并且不计算规则集。 CART使用在每个节点产生最大信息增益的特征和阈值来构造二叉树。

@_@ scikit-learn使用CART算法的优化版本。
'''
```
2. *Example1:*
```python
import numpy as np
from sklearn.tree import DecisionTreeClassifier,ExtraTreeClassifier
from sklearn.datasets import load_iris

X = np.array([[-3,-3],[-2,-2],[-1,1],[1,-1],[2,2],[3,3]])#样本
y = np.array([0,0,0,1,1,1])#样本对应的标签

clf = DecisionTreeClassifier()#ExtraTreeClassifier
clf = clf.fit(X,y)

pred = clf.predict([0,0])
pred_proba = clf.predict_proba([0,0]) #测试集样本在各个类别上预测的概率，越接近1越好
```

```python
>>>print(pred)
[0]
>>>print(pred_proba)
[[1. 0.]]
```
- #### *[RandomForest](http://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees) & [ExtraTrees](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html#sklearn.ensemble.ExtraTreesClassifier)*
1. *Information:*
```python
'''
   随机森林（RandomForest）与极端随机树（ExtraTrees）有两点主要的区别：
1. 随机森林应用的是Bagging模型，而ET是使用所有的训练样本得到每棵决策树，也就是每棵决策树应用的是相同的全部训练样本；
2. 随机森林是在一个随机子集内得到最佳分叉属性，而ET是完全随机的得到分叉值，从而实现对决策树进行分叉的。
'''
```
2. *Example2:*

```python
from sklearn.ensemble import RandomForestClassifier,ExtraTreesClassifier
'...'
'用法同Example1，注意调参。'
```



- #### *[Ensemble](http://scikit-learn.org/stable/modules/ensemble.html)*
1. *Information:*
```python
'@_@ 决策树算法会因为样本发生一点点的改动，就会导致树结构的剧烈变化。可通过集成学习(sklearn.ensemble)的方法来改善。'
```
2. *Example3:*

```python
from sklearn.ensemble import AdaBoostClassifier,BaggingClassifier,GradientBoostingClassifier,VotingClassifier
'...'
'用法同Example1，注意调参。'
```

## *二. 决策树在R中的运用*

- *Example3:*
```R
setwd('H:')
library(tree)
library(party)
library(RWeka)
library(C50)
library(rpart)


#数据准备
head(iris)
set.seed(1234)
ind <- sample(c(1,2), nrow(iris), replace = T, prob = c(0.6,0.4))#样本模型
train_data <- iris[ind==1,]
test_data <- iris[ind==2,]

#决策树
#iris_model <- tree(Species ~ ., data = train_data)#cart
iris_model <- ctree(Species ~ ., data = train_data)#条件推断树
#iris_model <- J48(Species ~ ., data = train_data)#c4.5
#iris_model <- C5.0(Species ~ ., data = train_data)#c5.0
#iris_model <- rpart(Species ~ ., data = train_data)#cart_improve

#调参（model中）
#control = tree.control(nobs, mincut = 5, minsize = 10, mindev = 0.01)
#control = ctree_control(teststat = c("quad", "max"),
#                       testtype = c("Bonferroni", "MonteCarlo", "Univariate", "Teststatistic"),
#                       mincriterion = 0.95, minsplit = 20, minbucket = 7,
#                       stump = FALSE, nresample = 9999, maxsurrogate = 0,
#                       mtry = 0, savesplitstats = TRUE, maxdepth = 0, remove_weights = FALSE)
#control = Weka_control(R = TRUE, M = 5)
#control = rpart.control(minsplit = 20, minbucket = round(minsplit/3), cp = 0.01, 
#                        maxcompete = 4, maxsurrogate = 5, usesurrogate = 2, xval = 10,
#                        surrogatestyle = 0, maxdepth = 30, ...)

#预测
pred <- predict(iris_model, newdata = test_data)

#准确率
t <- table(pred, test_data$Species)
accuracy <- sum(diag(t))/sum(t)
print(t)
print(accuracy)

#作图
print(iris_model)
plot(iris_model)
text(iris_model, use.n = T)
#plot(iris_model, type='simple')
```

```R
>>> print(t)
            
pred         setosa versicolor virginica
  setosa         19          0         0
  versicolor      0         13         2
  virginica       0          0        17
>>> print(accuracy)
[1] 0.9607843
>>> print(iris_model)

	 Conditional inference tree with 4 terminal nodes

Response:  Species 
Inputs:  Sepal.Length, Sepal.Width, Petal.Length, Petal.Width 
Number of observations:  99 

1) Petal.Length <= 1.9; criterion = 1, statistic = 92.053
  2)*  weights = 31 
1) Petal.Length > 1.9
  3) Petal.Width <= 1.7; criterion = 1, statistic = 45.837
    4) Petal.Length <= 4.4; criterion = 0.973, statistic = 7.34
      5)*  weights = 20 
    4) Petal.Length > 4.4
      6)*  weights = 19 
  3) Petal.Width > 1.7
    7)*  weights = 29 
```

![iris_model](http://i.imgur.com/LNl9pVw.png)

## *三. 决策树算法总结*

- *特点：*

|算法 |支持模型|树结构|特征选择|连续值处理|缺失值处理|[剪枝](https://en.wikipedia.org/wiki/Pruning_(decision_trees))|
|:--:|:------:|:---:|:-----:|:-------:|:------:|:--:|
|[ID3](https://en.wikipedia.org/wiki/ID3_algorithm)|分类|多叉树|[信息增益](https://en.wikipedia.org/wiki/Information_gain_in_decision_trees)|不支持|不支持|不支持|
|[C4.5](https://en.wikipedia.org/wiki/C4.5_algorithm)|分类|多叉树|[信息增益比](https://en.wikipedia.org/wiki/Information_gain_ratio)|支持|支持|支持|
|[CART](https://en.wikipedia.org/wiki/Decision_tree_learning)|分类&回归|二叉树|[基尼系数](https://en.wikipedia.org/wiki/Gini_coefficient)&均方差|支持|支持|支持|

- *优点*
```python
1. 生成决策树很直观；
2. 基本不需要预处理，不需要提前归一化和处理缺失值；
3. 使用决策树的算法复杂度是O(log2 m)，m为样本数；
4. 可以处理多维度输出的分类问题；
5. 相比于神经网络之类的黑盒分类模型，决策树在逻辑上可以得到很好的解释；
6. 可以交叉验证的剪枝来选择模型，从而提高泛化能力；
7. 对于异常点，容错能力好，健壮性高。
```
- *缺点*
```python
1. 决策树算法非常容易过拟合，导致泛化能力不强。可通过设置节点最少样本数量和限制决策树深度来改进；
2. 决策树算法会因为样本发生一点点的改动，就会导致树结构的剧烈变化。可通过集成学习(sklearn.ensemble)的方法来改善；
3. 一些较复杂的关系，决策树很难学习，如‘异或’。可通过神经网络来解决；
4. 某些特征的样本比例过大，生成决策树容易偏向于这些特征。可通过调节样本权重来改善。
```
