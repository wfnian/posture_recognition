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
    model = twentyclassification(30, 200, 300, 100, 23)
    model.load_state_dict(torch.load(
        "../model_pth/23classification_eigenvalue.pth", map_location='cpu'))
    predict = model(Variable(torch.Tensor([datas]).float())).detach().cpu().numpy().tolist()[0]
    predict = predict.index(max(predict))

    return predict


if __name__ == '__main__':
    start = time.clock()
    data = [18114.703243270982, 1337.2019510874525, 5006.928658325225, 4989.230273844674, 1854.1111520813429,
            10223.014867910475, 39836.62142227986, 10821.068440392846, 8365.860164288897, 6547.2375971945,
            1948.9061406599358, 15334.657250107266, 21385.5211898149, 77001.53299685242, 40382.594906986924,
            -0.0556522508659626, -0.5145220751468748, -
            0.7812298025557365, -0.900114476102391, 0.9611478908253382,
            0.3495203204957407, 0.826071285700574, -0.8430192651728674, -
            0.8334670851415399, 0.42622085027801004,
            0.9999864313797364, -0.8929040269180767, -0.9913461399742748, -0.18617720401433438, 0.9652206370433247]
    predict_result(data)

    end = time.clock()
    print(end - start)
