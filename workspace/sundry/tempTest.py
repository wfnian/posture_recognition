import matplotlib.pyplot as plt
import numpy as np

ax = []  # 保存图1数据
ay = []
bx = []  # 保存图2数据
by = []
num = 0  # 计数
plt.ion()  # 开启一个画图的窗口进入交互模式，用于实时更新数据
# plt.rcParams['savefig.dpi'] = 200 #图片像素
# plt.rcParams['figure.dpi'] = 200 #分辨率
plt.rcParams['figure.figsize'] = (8, 3)  # 图像显示大小
plt.rcParams['font.sans-serif'] = ['SimHei']  # 防止中文标签乱码，还有通过导入字体文件的方法
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['lines.linewidth'] = 0.5  # 设置曲线线条宽度
while num < 40:
    plt.clf()  # 清除刷新前的图表，防止数据量过大消耗内存
    plt.suptitle("总标题", fontsize=5)  # 添加总标题，并设置文字大小
    g1 = np.random.random()  # 生成随机数画图
    # 图表1
    ax.append(num)  # 追加x坐标值
    ay.append(g1)  # 追加y坐标值
    agraphic = plt.subplot(1, 2, 1)
    agraphic.set_title('子图表标题1')  # 添加子标题
    plt.plot(ax, ay, 'g-')  # 等于agraghic.plot(ax,ay,'g-')
    # 图表2
    bx.append(num)
    by.append(g1)
    bgraghic = plt.subplot(1, 2, 2)
    bgraghic.set_title('子图表标题2')
    plt.plot(bx, by, 'r.')

    plt.pause(0.1)  # 设置暂停时间，太快图表无法正常显示
    if num == 15:
        plt.savefig('picture.png', dpi=300)  # 设置保存图片的分辨率
        # break
    num = num + 1

plt.ioff()  # 关闭画图的窗口，即关闭交互模式
plt.show()  # 显示图片，防止闪退
