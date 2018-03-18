# coding=utf-8

import torch
from torch.autograd import Variable
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt


torch.manual_seed(1234)

DOWNLOAD_MNIST = False
BATCH_SIZE = 64
LR = 0.001
EPOCH = 1


train_data = torchvision.datasets.MNIST(root='./mnist',train=True,transform=torchvision.transforms.ToTensor(),download=DOWNLOAD_MNIST)
test_data  = torchvision.datasets.MNIST(root='./mnist/',train=False)

# print(train_data.train_data.size())   # torch.Size([60000, 28, 28])
# print(train_data.train_labels.size()) # torch.Size([60000])
#
# plt.imshow(train_data.train_data[0].numpy(),cmap='gray') # Greens,Blues
# plt.title('{}'.format(train_data.train_labels[0]))
# plt.show()

train_loader = Data.DataLoader(dataset=train_data,batch_size=BATCH_SIZE,shuffle=True,num_workers=4)

test_x = Variable(test_data.test_data,volatile=True).type(torch.FloatTensor)[:2000] / 255 # unsqueeze(x,dim=1)增加维度 [2000x28x28] --> [2000x1x28x28]
test_y = test_data.test_labels[:2000]
# test_x: [torch.FloatTensor of size 2000x28x28]
# test_y: [torch.LongTensor of size 2000]
# print(test_x.size())
# print(test_y.size(0))

class RNN(torch.nn.Module):
    def __init__(self):
        super(RNN,self).__init__()

        self.rnn = torch.nn.LSTM(    # http://pytorch.org/docs/0.3.1/nn.html#lstm
            input_size=28,          # 输入x的特征数量
            hidden_size=64,          # 隐层的特征数量
            num_layers=1,            # RNN的层数
            batch_first=True         # 如果True的话，那么输入Tensor的shape应该是[batch_size, time_step, feature(input_size)],输出也是这样。
        )
        self.out = torch.nn.Linear(in_features=64,out_features=10) # 10个数字识别

    def forward(self, x):
        rnn_out,(h_state,c_state) = self.rnn(x,None) # hc: tensor containing the `hidden` and `cell` state(the last) for t=seq_len.
        out = self.out(rnn_out[:,-1,:]) # [batch_size, time_step, feature]
        return out


rnn = RNN()
optimizer = torch.optim.Adam(rnn.parameters(),lr=LR)
loss_func = torch.nn.CrossEntropyLoss()

def run():
    torch.multiprocessing.freeze_support() # windows necessary: first define func, then include free_support.

    for epoch in range(EPOCH):
        for i,(batch_x,batch_y) in enumerate(train_loader):
            v_x,v_y = Variable(batch_x.view(-1,28,28)),Variable(batch_y) # reshape x to [batch_size, time_step, feature]
            output = rnn(v_x)
            loss = loss_func(output,v_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if i % 50 == 0:
                test_output = rnn(test_x)
                pred_y = torch.max(test_output,1)[1].data.numpy().squeeze()
                accuracy = sum(pred_y == test_y) / test_y.size(0)
                print('Epoch: {0}, train_loss: {1}, test_accuracy: {2}'.format(epoch,round(loss.data[0],4),round(accuracy,4)))



if __name__ == '__main__':
    run()
    test_output1 = rnn(test_x[:10])
    pred_y1 = torch.max(test_output1, 1)[1].data.numpy().squeeze()
    print('predict number:', pred_y1)
    print('real number:', test_y[:10].numpy())


'''Output:
Epoch: 0, train_loss: 2.3097, test_accuracy: 0.1025
Epoch: 0, train_loss: 2.1418, test_accuracy: 0.2175
Epoch: 0, train_loss: 1.3926, test_accuracy: 0.5705
Epoch: 0, train_loss: 1.1341, test_accuracy: 0.708
Epoch: 0, train_loss: 0.5589, test_accuracy: 0.732
Epoch: 0, train_loss: 0.9454, test_accuracy: 0.757
Epoch: 0, train_loss: 0.4716, test_accuracy: 0.826
Epoch: 0, train_loss: 0.3214, test_accuracy: 0.8585
Epoch: 0, train_loss: 0.3306, test_accuracy: 0.8555
Epoch: 0, train_loss: 0.3215, test_accuracy: 0.8805
Epoch: 0, train_loss: 0.2029, test_accuracy: 0.879
Epoch: 0, train_loss: 0.1784, test_accuracy: 0.8995
Epoch: 0, train_loss: 0.2682, test_accuracy: 0.8755
Epoch: 0, train_loss: 0.2382, test_accuracy: 0.9025
Epoch: 0, train_loss: 0.2455, test_accuracy: 0.9065
Epoch: 0, train_loss: 0.1949, test_accuracy: 0.9035
Epoch: 0, train_loss: 0.1632, test_accuracy: 0.9185
Epoch: 0, train_loss: 0.3286, test_accuracy: 0.9095
Epoch: 0, train_loss: 0.1573, test_accuracy: 0.891
predict number: [7 2 1 0 4 1 4 9 6 9]
real number: [7 2 1 0 4 1 4 9 5 9]
'''
