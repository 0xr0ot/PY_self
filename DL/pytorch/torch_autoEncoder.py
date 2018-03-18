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
EPOCH = 10


train_data = torchvision.datasets.MNIST(root='./mnist',train=True,transform=torchvision.transforms.ToTensor(),download=DOWNLOAD_MNIST)
train_loader = Data.DataLoader(dataset=train_data,batch_size=BATCH_SIZE,shuffle=True,num_workers=4)


class AutoEncoder(torch.nn.Module):
    def __init__(self):
        super(AutoEncoder, self).__init__()

        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(28 * 28, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128, 64),
            torch.nn.Tanh(),
            torch.nn.Linear(64, 12),
            torch.nn.Tanh(),
            torch.nn.Linear(12, 3),
            torch.nn.Tanh(),
        )

        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(3, 12),
            torch.nn.Tanh(),
            torch.nn.Linear(12, 64),
            torch.nn.Tanh(),
            torch.nn.Linear(64, 128),
            torch.nn.Tanh(),
            torch.nn.Linear(128, 28*28),
            torch.nn.Sigmoid(), # difference
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


auto_encoder = AutoEncoder()
optimizer = torch.optim.Adam(auto_encoder.parameters(),lr=LR)
loss_func = torch.nn.MSELoss()


def run():
    torch.multiprocessing.freeze_support()

    for epoch in range(EPOCH):
        for i, (batch_x,batch_y) in enumerate(train_loader):
            v_x,v_y = Variable(batch_x.view(-1,28*28)),Variable(batch_x.view(-1,28*28))
            # v_label = Variable(batch_y)

            decoded = auto_encoder(v_x)
            loss = loss_func(decoded,v_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if i % 100 == 0:
                print('epoch: {0}, loss: {1}'.format(epoch,loss.data.numpy()[0]))



if __name__ == '__main__':
    run()
