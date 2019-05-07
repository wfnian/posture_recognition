import torch
from torch import nn
from PIL import Image
from torchvision.transforms import transforms
from torch.autograd import Variable


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Sequential(
            torch.nn.Conv2d(3, 32, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2))
        self.conv2 = torch.nn.Sequential(
            torch.nn.Conv2d(32, 64, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2))
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2))
        self.dense = torch.nn.Sequential(
            torch.nn.Linear(64 * 60 * 80, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 23)
        )

    def forward(self, x):
        conv1_out = self.conv1(x)
        conv2_out = self.conv2(conv1_out)
        conv3_out = self.conv3(conv2_out)
        res = conv3_out.view(conv3_out.size(0), -1)
        out = self.dense(res)
        return out


model = Net()
print(model)
model.load_state_dict(torch.load("23classification_pic_2.pth", map_location='cpu'))

img = Image.open("E:\\dataset\\taichi\\taichi\\marked_pic\\p_89_11.jpg").convert('RGB')
pre = transforms.Compose([transforms.ToTensor()])(img)
pre = pre.unsqueeze(0)
pre = Variable(pre)

res = model(pre)[0].detach().numpy().tolist()

resClass = res.index(max(res))
