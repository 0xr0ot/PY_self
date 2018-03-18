# coding=utf-8

import torch
import torch.utils.data as Data


BATCH_SIZE = 8

x = torch.linspace(1,20,20) # ndim==1
y = torch.linspace(20,1,20)

torch_dataset = Data.TensorDataset(data_tensor=x,target_tensor=y)
loader = Data.DataLoader(
    dataset=torch_dataset,
    batch_size=BATCH_SIZE,
    # shuffle=True,
    # num_workers=2
)

for epoch in range(3):
    for step, (batch_x,batch_y) in enumerate(loader):
        print('epoch: {0}, step: {1}, batch_x: {2}, batch_y: {3}'.format(epoch,step,batch_x.numpy(),batch_y.numpy()))


