# coding=utf-8

import torch
from torch.autograd import Variable


tensor = torch.FloatTensor([[1,2],[3,4]])
var = Variable(tensor,requires_grad=True)

t_out = torch.mean(tensor**2)
v_out = torch.mean(var**2)

v_out.backward()
print(var.grad)
print(var)
print(var.data)
print(var.data.numpy())
