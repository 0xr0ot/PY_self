# coding=utf-8

import torch
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt

x = torch.unsqueeze(torch.linspace(-1,1,100),dim=1) # 一维([torch.FloatTensor of size 100]) 转 二维(torch.FloatTensor of size 100x1)
y = x.pow(2) + 0.2*torch.rand(x.size())
x,y = Variable(x),Variable(y)

# plt.scatter(x,y)
# plt.show()

####################################################################################################################
# method1:
class Net(torch.nn.Module):
    def __init__(self,n_feature,n_hidden,n_output): # 输入层，隐藏层，输出层
        super(Net,self).__init__()
        self.hidden = torch.nn.Linear(n_feature,n_hidden)
        self.predict = torch.nn.Linear(n_hidden,n_output)

    def forward(self, x): # 前向传递
        x = F.relu(self.hidden(x)) # 激励函数relu
        x = self.predict(x)
        return x

net1 = Net(1,10,1) # 输入层，隐藏层，输出层
#######################################################
# method2: # 顺序容器
net2 = torch.nn.Sequential(
    torch.nn.Linear(2,10),
    torch.nn.ReLU(),
    torch.nn.Linear(10,2),
)

####################################################################################################################


optimizer = torch.optim.SGD(net1.parameters(),lr=0.5) # 优化：随机梯度下降
loss_func = torch.nn.MSELoss() # 损失函数： regression --> MSELoss; classification --> CrossEntropyLoss

plt.ion()
for i in range(100):
    prediction = net1(x)
    loss = loss_func(prediction,y)
    optimizer.zero_grad() # Clears the gradients
    loss.backward()
    optimizer.step()

    #plot:
    if i % 5 == 0:
        plt.cla()
        plt.scatter(x.data.numpy(),y.data.numpy())
        plt.plot(x.data.numpy(),prediction.data.numpy(),'r-',lw=5)
        plt.text(0.5,0,'Loss=%.4f' % loss.data[0],fontdict={'size': 20, 'color': 'red'})
        plt.pause(0.1)

plt.ioff()
plt.show()

# save model:
torch.save(net1,'net1_entire.pkl') # 保存整个模型
torch.save(net1.state_dict(),'net1_state.pkl') # 只保存模型状态参数,无骨架的血肉

# load model:
def load_entireModel():
    return torch.load('net1_entire.pkl')

def load_paramModel():
    net = torch.nn.Sequential(
        torch.nn.Linear(2,10),
        torch.nn.ReLU(),
        torch.nn.Linear(10,2),
    )
    return net.load_state_dict(torch.load('net1_state'))

