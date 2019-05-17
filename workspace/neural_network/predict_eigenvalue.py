# -*- coding: utf-8 -*-
"""
@author: wfnian
"""

import time

import torch
from torch import nn
from torch.autograd import Variable


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

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        return x


def predict_result(datas=None):
    """
    :param datas: list
    :return: int
    """
    if datas is None:
        datas = []
    model = twentyclassification(30, 200, 300, 100, 24)
    model.load_state_dict(torch.load(
        "../model_pth/23classification_eigenvalue.pth", map_location='cpu'))
    predict = model(Variable(torch.Tensor([datas]).float())).detach().cpu().numpy().tolist()[0]
    predict = predict.index(max(predict))

    return predict


if __name__ == '__main__':
    start = time.clock()
    data = [0.0, 163115.3545813507, 135018.25825455785, 12331.515849550487, 120673.87059219554, 6122.537879968295, 0.0,
            163115.3545813507, 163115.3545813507, 0.0, 0.0, 433081.6202105442, 163098.4398608161, 0.0,
            163115.3545813507, 0.4150879533697161, 0.9778420883296507, 0, 0, -0.8914324274471591, -0.2886839472216833,
            0, 0, 0, -0.6680837068163037, 0, 0, 0, 1.0, 0.5246781242226066]
    # print(predict_result(data))
    predict_result(data)

    end = time.clock()
    print(end - start)
