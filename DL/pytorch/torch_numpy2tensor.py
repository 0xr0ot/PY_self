# coding=utf-8

import torch as t
import numpy as np


'1. tensor <--> numpy:'
np_data = np.arange(6).reshape((2,3))

np2t_data = t.from_numpy(np_data)
t2np_data = np2t_data.numpy()

## abs(),sin(),cos()
array1 = np.array([-1,-2,1,2])
tensor1 = t.from_numpy(array1)


'2. tensor:'
x1 = t.FloatTensor(5,3)
x2 = t.rand(5,3)

'3. add'
sum1 = x1 + x2
sum2 = t.add(x1,x2)

t.add(x1,x2,out=x2)
# print(sum1)
# print(sum2)
# print(x2)

print(t.cuda.is_available())


