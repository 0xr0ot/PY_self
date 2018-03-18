# coding=utf-8

import torch
from torch.autograd import Variable
import numpy as np
import matplotlib.pyplot as plt

# use sin() predict cos()
torch.manual_seed(1234)

LR = 0.01 # suitable
TIME_STEP = 10
h_state = None


class RNN(torch.nn.Module):
    def __init__(self):
        super(RNN, self).__init__()

        self.rnn = torch.nn.RNN(
            input_size=1,
            hidden_size=32,
            num_layers=1,
            batch_first=True
        )
        self.out = torch.nn.Linear(32,1)

    def forward(self, x, h_state):
        # x: [batch_size, time_step, feature(input_size)]
        # h_state: [n_layers, batch_size, hidden_size]
        # rnn_out: [batch_size, time_step, output_size(now = hidden_size)]
        rnn_out,h_state = self.rnn(x,h_state)
        outs = []
        for time_step in range(rnn_out.size(1)):
            outs.append(self.out(rnn_out[:,time_step,:]))
        return (torch.stack(outs,dim=1),h_state)


rnn = RNN()
optimizer = torch.optim.Adam(rnn.parameters(),lr=LR)
loss_func = torch.nn.MSELoss()


for step in range(100):
    begin,end = step * np.pi, (step+1) * np.pi
    steps = np.linspace(begin,end,TIME_STEP,dtype=np.float32) # must: np.float32 <--> floatTensor, not np.float64
    x_np,y_np = np.sin(steps),np.cos(steps)

    v_x = Variable(torch.from_numpy(x_np[np.newaxis, :, np.newaxis]))
    v_y = Variable(torch.from_numpy(y_np[np.newaxis, :, np.newaxis]))

    prediction, h_state = rnn(v_x, h_state)
    h_state = Variable(h_state.data) # importance

    loss = loss_func(prediction,v_y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    plt.plot(steps, y_np.flatten(), 'r-')
    plt.plot(steps, prediction.data.numpy().flatten(), 'b-')
    plt.draw()
    plt.pause(0.05)

plt.ioff()
plt.show()
