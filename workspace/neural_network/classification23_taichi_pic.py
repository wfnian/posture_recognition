import os

import torch
import torch.nn
import torch.optim
import matplotlib.pyplot as plt
from PIL import Image
from torch.autograd import Variable
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from tensorboardX import SummaryWriter

root = "../dataset/taichi/marked_pic"


def convert_to_img():
    files = None
    for _, _, files in os.walk(root):
        pass
    txt_file = open(root + 'train.txt', 'w')

    for file in files:
        img_path = root + '/' + file
        img_label = file.split('.')[0].split('_')[-1]
        txt_file.write(img_path + ' ' + img_label + '\n')


# convert_to_img()


# -----------------ready the dataset--------------------------
def default_loader(path):
    return Image.open(path).convert('RGB')


class MyDataset(Dataset):
    def __init__(self, txt, transform=None, target_transform=None, loader=default_loader):
        fh = open(txt, 'r')
        imgs = []
        for line in fh:
            line = line.strip('\n')
            line = line.rstrip()
            words = line.split()
            imgs.append((words[0], int(words[1])))
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = self.loader(fn)
        if self.transform is not None:
            img = self.transform(img)
        return img, label

    def __len__(self):
        return len(self.imgs)


# -----------------create the Net and training------------------------

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
            torch.nn.MaxPool2d(2)
        )
        self.conv3 = torch.nn.Sequential(
            torch.nn.Conv2d(64, 64, 3, 1, 1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2)
        )
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


def train_net_cnn():
    train_data = MyDataset(txt=root + 'train.txt', transform=transforms.ToTensor())
    train_loader = DataLoader(dataset=train_data, batch_size=16, shuffle=True)

    model = Net()
    print(model)
    model = model.cuda()
    optimizer = torch.optim.Adam(model.parameters())
    loss_func = torch.nn.CrossEntropyLoss()

    plt_loss = []
    plt_acc = []

    # writer = SummaryWriter()
    # tensorboardMark = True

    for epoch in range(10):
        print('epoch {}'.format(epoch + 1))
        train_loss = 0.
        train_acc = 0.
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = Variable(batch_x).cuda(), Variable(batch_y).cuda()

            # if tensorboardMark:
            #     tensorboardMark = False
            #     with SummaryWriter(comment="Net") as w:
            #         w.add_graph(model, (batch_x,))

            out = model(batch_x)
            loss = loss_func(out, batch_y)
            train_loss += loss.item()
            pred = torch.max(out, 1)[1]
            train_correct = (pred == batch_y).sum()
            train_acc += train_correct.item()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        plt_acc.append(train_acc / (len(train_data)))
        plt_loss.append(train_loss / (len(train_data)))

        # writer.add_scalar('loss', train_loss / (len(train_data)), epoch)
        # writer.add_scalar('acc', train_acc / (len(train_data)), epoch)

        print('Train Loss: {:.6f}, Acc: {:.6f}'.format(train_loss / len(train_data), train_acc / len(train_data)))

        model.eval()

    # ===================================== 绘图 ==================================
    plt.figure(12, figsize=(8, 3))
    plt.subplot(1, 2, 1)
    plt.title("network loss")
    plt.plot(plt_loss, 'r')
    plt.subplot(1, 2, 2)
    plt.title("network acc")
    plt.plot(plt_acc, 'g')
    plt.savefig('../sundry/train_loss_acc_pic.png')
    plt.close(12)
    # ===================================== 绘图 ==================================

    torch.save(model.state_dict(), "../model_pth/23classification_pic.pth")


if __name__ == '__main__':
    # convert_to_img() 处理图片 写入TXT
    train_net_cnn()
