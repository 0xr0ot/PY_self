# coding=utf-8

import torch
import torch.utils.data as Data
# import torch.nn.functional as F
from torch.autograd import Variable
import matplotlib.pyplot as plt


torch.manual_seed(1234)

LR = 0.0005
BATCH_SIZE = 32
EPOCH = 12

x = torch.unsqueeze(torch.linspace(-1,1,1000),dim=1)
y = x.pow(2) + 0.2*torch.rand(x.size())

torch_dataset = Data.TensorDataset(data_tensor=x,target_tensor=y)
loader = Data.DataLoader(dataset=torch_dataset,batch_size=BATCH_SIZE,shuffle=True)

net = torch.nn.Sequential(
    torch.nn.Linear(1,20),
    torch.nn.ReLU(),
    torch.nn.Linear(20,1),
)


opt_SGD      = torch.optim.SGD(net.parameters(), lr=LR)
opt_Momentum = torch.optim.SGD(net.parameters(), lr=LR, momentum=0.9)
opt_RMSprop  = torch.optim.RMSprop(net.parameters(), lr=LR, alpha=0.99)
opt_Adam     = torch.optim.Adam(net.parameters(), lr=LR, betas=(0.9, 0.999))

optimizers = [opt_SGD, opt_Momentum, opt_RMSprop, opt_Adam]

loss_func = torch.nn.MSELoss()
loss_pool = [[], [], [], []]

for epoch in range(EPOCH):
    print('Epoch:', epoch)
    for step, (batch_x, batch_y) in enumerate(loader):
        v_x,v_y = Variable(batch_x),Variable(batch_y)

        for opt, loss_list in zip(optimizers, loss_pool):
            output = net(v_x)
            loss = loss_func(output, v_y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            loss_list.append(loss.data[0])

labels = ['SGD', 'Momentum', 'RMSprop', 'Adam']
for i, loss_v in enumerate(loss_pool):
    plt.plot(loss_v, label=labels[i])
plt.legend(loc='best')
plt.xlabel('Steps')
plt.ylabel('Loss')
plt.ylim((0, 0.2))
plt.show()


