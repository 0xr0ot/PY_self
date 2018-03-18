# coding=utf-8

import torch
from torch.autograd import Variable
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt


torch.manual_seed(1234)

DOWNLOAD_MNIST = False
BATCH_SIZE = 50
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

test_x = Variable(torch.unsqueeze(test_data.test_data,dim=1),volatile=True).type(torch.FloatTensor)[:2000] / 255
# unsqueeze(x,dim=1)增加维度 [2000x28x28] --> [2000x1x28x28]
test_y = test_data.test_labels[:2000]
# test_x: [torch.FloatTensor of size 2000x1x28x28]
# test_y: [torch.LongTensor of size 2000]


class CNN(torch.nn.Module):
    def __init__(self):
        super(CNN, self).__init__()

        self.conv1 = torch.nn.Sequential( # --> [1x28x28] height,length,width（或者 厚度，高度，宽度）
            torch.nn.Conv2d(      # http://pytorch.org/docs/0.3.1/nn.html#conv2d
                in_channels=1,    # 输入信号的通道
                out_channels=16,  # 卷积产生的通道
                kernel_size=5,    # 卷积核的尺寸
                stride=1,         # 卷积步长
                padding=2         # 输入的每一条边补充0的层数, padding = (kernel_size - stride)/2
            ), # --> [16x28x28]
            torch.nn.ReLU(), # --> [16x28x28]
            torch.nn.MaxPool2d(kernel_size=2), # --> [16x14x14]
        )
        self.conv2 = torch.nn.Sequential( # --> [16x14x14]
            torch.nn.Conv2d(16,32,5,1,2), # --> [32x14x14]
            torch.nn.ReLU(),              # --> [32x14x14]
            torch.nn.MaxPool2d(2)         # --> [32x7x7]
        )
        self.out = torch.nn.Linear(in_features=32*7*7,out_features=10) # ndim==2, 10个数字识别

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)        # --> [batch,32x7x7]
        x = x.view(x.size(0),-1) # --> [batch,32*7*7]
        output = self.out(x)
        return output

cnn = CNN()
optimizer = torch.optim.Adam(cnn.parameters(),lr=LR)
loss_func = torch.nn.CrossEntropyLoss()

def run():
    # torch.multiprocessing.freeze_support() # windows necessary: first define func, then include free_support.

    for epoch in range(EPOCH):
        for i,(batch_x,batch_y) in enumerate(train_loader):
            v_x,v_y = Variable(batch_x),Variable(batch_y)
            output = cnn(v_x)
            loss = loss_func(output,v_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if i % 50 == 0:
                test_output = cnn(test_x)
                pred_y = torch.max(test_output,1)[1].data.numpy().squeeze()
                accuracy = sum(pred_y == test_y) / test_y.size(0)
                print('Epoch: {0}, train_loss: {1}, test_accuracy: {2}'.format(epoch,round(loss.data[0],4),round(accuracy,4)))



if __name__ == '__main__':
    run()
    test_output1 = cnn(test_x[:10])
    pred_y1 = torch.max(test_output1, 1)[1].data.numpy().squeeze()
    print('predict number:', pred_y1)
    print('real number:', test_y[:10].numpy())


'''Output:
Epoch: 0, train_loss: 2.2878, test_accuracy: 0.241
Epoch: 0, train_loss: 0.4973, test_accuracy: 0.842
Epoch: 0, train_loss: 0.4481, test_accuracy: 0.885
Epoch: 0, train_loss: 0.2738, test_accuracy: 0.916
Epoch: 0, train_loss: 0.3487, test_accuracy: 0.9285
Epoch: 0, train_loss: 0.0845, test_accuracy: 0.94
Epoch: 0, train_loss: 0.0372, test_accuracy: 0.934
Epoch: 0, train_loss: 0.2374, test_accuracy: 0.9575
Epoch: 0, train_loss: 0.1344, test_accuracy: 0.9585
Epoch: 0, train_loss: 0.0783, test_accuracy: 0.951
Epoch: 0, train_loss: 0.0472, test_accuracy: 0.96
Epoch: 0, train_loss: 0.1768, test_accuracy: 0.9665
Epoch: 0, train_loss: 0.3601, test_accuracy: 0.9705
Epoch: 0, train_loss: 0.0317, test_accuracy: 0.9695
Epoch: 0, train_loss: 0.0625, test_accuracy: 0.973
Epoch: 0, train_loss: 0.0426, test_accuracy: 0.971
Epoch: 0, train_loss: 0.0895, test_accuracy: 0.9705
Epoch: 0, train_loss: 0.1431, test_accuracy: 0.9745
Epoch: 0, train_loss: 0.3359, test_accuracy: 0.964
Epoch: 0, train_loss: 0.0052, test_accuracy: 0.975
Epoch: 0, train_loss: 0.1834, test_accuracy: 0.9715
Epoch: 0, train_loss: 0.06, test_accuracy: 0.9775
Epoch: 0, train_loss: 0.0525, test_accuracy: 0.979
Epoch: 0, train_loss: 0.0998, test_accuracy: 0.9715
predict number: [7 2 1 0 4 1 4 9 5 9]
real number: [7 2 1 0 4 1 4 9 5 9]
'''
