## *公公偏头痛之“naiveBayes分类示例”* ##

- ##### 数据转化
```python
job		            perform		    pain	
programmer	1	    finger	3	    fracture	1
programmer	1	    head	1	    cold	2
dmer	    	2	    head	1	    no	        3
dmer	    	2	    stomach	2	    stomachache	4
hr	        3	    stomach	2	    stomachache	4
hr	        3	    finger	3	    no	        3
```


- ##### R实现
```R
library(e1071)
## data_ready.
train <- data.frame(job = c(1,1,2,2,3,3),
                    perform = c(3,1,1,2,2,3),
                    pain = as.factor(c(1,2,3,4,4,3)))

test  <- data.frame(job = c(1,2,3),
                    perform = c(2,3,1))
## model_predict.
model <- naiveBayes(train[,-3], train[,3])
pred <- predict(model, test)
```

```R
>>>print(pred)
[1] 4 3 3
Levels: 1 2 3 4
```


- ##### python实现
```python
import numpy as np
from sklearn.naive_bayes import GaussianNB

X = np.array([[1,3],[1,1],[2,1],[2,2],[3,2],[3,3]])
y = np.array([1,2,3,4,4,3])
test = np.array([[1,2],[2,3],[3,1]])

clf = GaussianNB()
clf.fit(X,y)
pred = clf.predict(test)
pred_proba = clf.predict_proba(test)
```

```python
>>>print(pred)
[4 3 3]
>>>print(pred_proba)
[[  0.00000000e+00   0.00000000e+00   2.58192223e-05   9.99974181e-01]
 [  0.00000000e+00   0.00000000e+00   1.00000000e+00   0.00000000e+00]
 [  0.00000000e+00   0.00000000e+00   1.00000000e+00   0.00000000e+00]]
```
