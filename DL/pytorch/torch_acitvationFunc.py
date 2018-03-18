# coding=utf-8

import numpy as np
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt


# make data
x = torch.linspace(-5,5,200)
x = Variable(x)
x_np = x.data.numpy()

y_relu = F.relu(x).data.numpy()
y_sigmoid = F.sigmoid(x).data.numpy()
y_tanh = F.tanh(x).data.numpy()
y_softplus = F.softplus(x).data.numpy()
y_softmax = F.softmax(x).data.numpy()


fig = plt.figure()

ax1 = fig.add_subplot(2,3,1)
ax1.plot(x_np,y_relu,c='red',label='relu')
ax1.set_ylim((-1,5))
ax1.legend(loc='best')

ax2 = fig.add_subplot(2,3,2)
ax2.plot(x_np,y_sigmoid,c='red',label='sigmoid')
ax2.set_ylim((-0.2,1.2))
ax2.legend(loc='best')

ax3 = fig.add_subplot(2,3,3)
ax3.plot(x_np,y_tanh,c='red',label='tanh')
ax3.set_ylim((-1.2,1.2))
ax3.legend(loc='best')

ax4 = fig.add_subplot(2,3,4)
ax4.plot(x_np,y_softplus,c='red',label='softplus')
ax4.set_ylim((-0.2,6))
ax4.legend(loc='best')

ax5 = fig.add_subplot(2,3,5)
ax5.plot(x_np,y_softmax,c='red',label='softmax')
ax5.set_ylim(-0.1,0.1)
ax5.legend(loc='best')

plt.show()
