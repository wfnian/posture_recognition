# -*- coding: utf-8 -*-
"""
@author: wfnian
"""

import torch
from torch import nn, optim
from torch.autograd import Variable
import matplotlib.pyplot as plt
import time
from tensorboardX import SummaryWriter

gpu = True


def retFloat(val):
    return float(val)


def getData():
    with open("../dataset/taichi/bone_dataSet.data", "r") as file:
        data = file.readlines()
    x, y = [], []
    for i in data:
        if i[0] != '#':
            temp = i[1:-2].split(',')
            x.append(temp[:-1])
            y.append(temp[-1])

    res_x = []
    for i in x:
        r = map(float, i)
        res_x.append(list(r))
    y = list(map(int, y))

    return res_x, y


""" x 的形状类似于
x = [[],
     []
     []
     []]
len(x[0]) = 30
len(x) = 170
y 的形状类似于：表示分类
y = [0,
     1,
     2,
     3,
     ...
     ]
len(y) = 170
"""


class twentyclassification(nn.Module):
    def __init__(self, in_dim, n_hidden_1, n_hidden_2, n_hidden_3, out_dim):
        super(twentyclassification, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(in_dim, n_hidden_1), nn.ReLU(True))
        self.layer2 = nn.Sequential(
            nn.Linear(n_hidden_1, n_hidden_2), nn.ReLU(True))
        self.layer3 = nn.Sequential(
            nn.Linear(n_hidden_2, n_hidden_3), nn.ReLU(True))
        self.layer4 = nn.Sequential(nn.Linear(n_hidden_3, out_dim))

    def forward(self, data):
        data = self.layer1(data)
        data = self.layer2(data)
        data = self.layer3(data)
        data = self.layer4(data)

        return data


def train_net():
    start = time.clock()
    _x, _y = getData()

    if gpu:  # torch.cuda.is_available():
        model = twentyclassification(30, 200, 300, 100, 23).cuda()
    else:
        model = twentyclassification(30, 200, 300, 100, 23)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.000001)

    plt_loss = []
    acc_ = []

    writer = SummaryWriter()

    for epoch in range(600):

        if gpu:  # torch.cuda.is_available():
            x_data = Variable(torch.tensor(_x)).cuda()
            target = Variable(torch.tensor(_y)).cuda()
        else:
            x_data = Variable(torch.tensor(_x))
            target = Variable(torch.tensor(_y))
        out = model(x_data)
        loss = criterion(out, target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # if epoch % 20 == 0:
        plt_loss.append(loss.item())
        if gpu:  # torch.cuda.is_available():
            vect = out.detach().cpu().numpy().tolist()
        else:
            vect = out.detach().numpy().tolist()
        acc = 0
        for i in range(len(vect)):
            if _y[i] == vect[i].index(max(vect[i])):
                acc = acc + 1
        acc = acc / len(vect)
        acc_.append(acc)
        writer.add_scalar('loss', loss, epoch)
        writer.add_scalar('acc', acc, epoch)

    plt.figure(10, figsize=(8, 3))
    plt.subplot(1, 2, 1)
    plt.title("network loss")
    plt.plot(list(range(len(plt_loss))), plt_loss, 'r')
    plt.subplot(1, 2, 2)
    plt.title("network acc")
    plt.plot(list(range(len(acc_))), acc_, 'g')
    # plt.show()
    plt.savefig('../sundry/train_loss_acc_eigenvalue.png')
    plt.close(10)

    end = time.clock()
    print("used " + str(end - start))

    model.eval().cuda()

    torch.save(model.state_dict(), "../model_pth/23classification_eigenvalue.pth")


if __name__ == '__main__':
    train_net()
