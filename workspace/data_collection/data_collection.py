import math
import os
import sys

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow

from data_collection_window import *

picSN = 10

# ====================import openpose=========================================
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    sys.path.append(dir_path + '/../python/openpose/Release')
    # 一定要注意是 build目录下的python而不是openpose根目录下的
    # 如果一直报错可以将绝对路径加入 path环境变量中去。
    # 或者将绝对路径引进来 F:\\OPENPOSE\\openpose\\build\\python\\openpose\\Release
    # 或是如下添加绝对路径
    sys.path.append("F:\\OPENPOSE\\openpose\\build\\python\\openpose\\Release")
    # 此句和上句同理 两者只要一者起效便可
    import pyopenpose as op

except ImportError as e:
    print('Did you enable `BUILD_PYTHON`')
    raise e
# =============================参数args 设置====================================
# 详细参考flags.hpp 文件
params = dict()
params["model_folder"] = "F:\\OPENPOSE\\openpose\\models"
# 根据实际情况路径做相应改变
params["number_people_max"] = 1  # 只检测一个人
params["camera_resolution"] = "640x360"
params["disable_blending"] = False
params["render_threshold"] = 0.001


# ==============================================================================

class Video:
    def __init__(self, capture):
        self.capture = capture

    def captureFrame(self):
        """
        capture frame and return captured frame
        """
        ret, readFrame = self.capture.read()
        return readFrame

    def captureNextFrame(self):
        """
        capture frame and reverse RBG BGR and return opencv image
        """
        ret, readFrame = self.capture.read()
        if ret:
            self.currentFrame = cv2.cvtColor(readFrame, cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        """     
        converts frame to format suitable for QtGui            
        """
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame, width, height, QtGui.QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            print("Convert error")
            return None


class mWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mWindow, self).__init__()
        self.setupUi(self)
        self._timer1 = QTimer(self)
        self._timer1.timeout.connect(self.showCapture)
        self.video = Video(cv2.VideoCapture(0))
        self._timer1.start(30)  # 每隔多长时间
        self.pushButton.clicked.connect(self.savePic)
        self.picPaths = "0"

    def showCapture(self):
        try:
            self.video.captureNextFrame()
            self.label.setPixmap(self.video.convertFrame())

        except TypeError:
            print("No frame")

    def savePic(self):
        self.video.captureNextFrame()
        frame = self.video.convertFrame()
        self.label_2.setPixmap(frame)
        # self.label_2.setScaledContents(False)  # 设置图片自适应窗口

        self.capturedFrame = self.video.captureFrame()
        pose = self.lineEdit.text()

        global picSN
        picSN += 1
        pictureName = str(picSN) + '_' + pose + ".jpg"

        self.picPaths = "../dataset/pic_background/" + pictureName
        cv2.imwrite(self.picPaths, self.capturedFrame)
        print('captured')
        try:

            self.processPic()
        except:
            print("线程错误")

    def processPic(self):
        # ============================= 启动openPose ===================================

        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()
        datum = op.Datum()

        datum.cvInputData = cv2.imread(self.picPaths)  # 输入
        opWrapper.emplaceAndPop([datum])  # 输出
        keyPoints = datum.poseKeypoints.tolist()

        dstPicPath = "../dataset/marked_pic/p_" + self.picPaths.split('/')[-1]  # 处理后的图片
        cv2.imwrite(dstPicPath, datum.cvOutputData)
        # ============================= 写骨骼数据文件 ===================================
        with open("../dataset/bone_dataSet.data", "a+") as dataSet:
            dataSet.writelines(
                str(self.pointDistance(keyPoints[0]) + self.pointAngle(keyPoints[0]) + [int(self.lineEdit.text())]))
            dataSet.write("\n")
        # ============================= 写骨骼图片文件 ===================================
        bone_img = datum.cvOutputData
        height, width, channel = bone_img.shape
        pixmap = QPixmap.fromImage(QImage(
            bone_img.data, width, height, 3 * width, QImage.Format_RGB888).rgbSwapped())
        self.label_3.setPixmap(pixmap)
        # ============================= label3 显示图片 ==================================

    def pointDistance(self, keyPoint):
        """
        :param keyPoint:
        :return:list
        :distance:
        """
        distance0 = (keyPoint[4][0] - keyPoint[9][0]) ** 2 + \
                    (keyPoint[4][1] - keyPoint[9][1]) ** 2
        distance1 = (keyPoint[7][0] - keyPoint[12][0]) ** 2 + \
                    (keyPoint[7][1] - keyPoint[12][1]) ** 2
        distance2 = (keyPoint[2][0] - keyPoint[4][0]) ** 2 + \
                    (keyPoint[2][1] - keyPoint[4][1]) ** 2
        distance3 = (keyPoint[5][0] - keyPoint[7][0]) ** 2 + \
                    (keyPoint[5][1] - keyPoint[7][1]) ** 2
        distance4 = (keyPoint[0][0] - keyPoint[4][0]) ** 2 + \
                    (keyPoint[0][1] - keyPoint[4][1]) ** 2
        distance5 = (keyPoint[0][0] - keyPoint[7][0]) ** 2 + \
                    (keyPoint[0][1] - keyPoint[7][1]) ** 2
        distance6 = (keyPoint[4][0] - keyPoint[10][0]) ** 2 + \
                    (keyPoint[4][1] - keyPoint[10][1]) ** 2
        distance7 = (keyPoint[7][0] - keyPoint[13][0]) ** 2 + \
                    (keyPoint[7][1] - keyPoint[13][1]) ** 2
        distance8 = (keyPoint[4][0] - keyPoint[7][0]) ** 2 + \
                    (keyPoint[4][1] - keyPoint[7][1]) ** 2
        distance9 = (keyPoint[11][0] - keyPoint[14][0]) ** 2 + \
                    (keyPoint[11][1] - keyPoint[14][1]) ** 2
        distance10 = (keyPoint[10][0] - keyPoint[13][0]
                      ) ** 2 + (keyPoint[10][1] - keyPoint[13][1]) ** 2
        distance11 = (keyPoint[6][0] - keyPoint[10][0]
                      ) ** 2 + (keyPoint[6][1] - keyPoint[10][1]) ** 2
        distance12 = (keyPoint[3][0] - keyPoint[13][0]
                      ) ** 2 + (keyPoint[3][1] - keyPoint[13][1]) ** 2
        distance13 = (keyPoint[4][0] - keyPoint[23][0]
                      ) ** 2 + (keyPoint[4][1] - keyPoint[23][1]) ** 2
        distance14 = (keyPoint[7][0] - keyPoint[20][0]
                      ) ** 2 + (keyPoint[7][1] - keyPoint[20][1]) ** 2

        return [distance0, distance1, distance2, distance3, distance4, distance5, distance6, distance7,
                distance8, distance9, distance10, distance11, distance12, distance13, distance14]

    def pointAngle(self, keyPoint):
        angle0 = self.myAngle(keyPoint[2], keyPoint[3], keyPoint[4])
        angle1 = self.myAngle(keyPoint[5], keyPoint[6], keyPoint[7])
        angle2 = self.myAngle(keyPoint[9], keyPoint[10], keyPoint[11])
        angle3 = self.myAngle(keyPoint[12], keyPoint[13], keyPoint[14])
        angle4 = self.myAngle(keyPoint[3], keyPoint[2], keyPoint[1])
        angle5 = self.myAngle(keyPoint[6], keyPoint[5], keyPoint[1])
        angle6 = self.myAngle(keyPoint[10], keyPoint[8], keyPoint[13])
        angle7 = self.myAngle(keyPoint[7], keyPoint[12], keyPoint[13])
        angle8 = self.myAngle(keyPoint[4], keyPoint[9], keyPoint[10])
        angle9 = self.myAngle(keyPoint[4], keyPoint[0], keyPoint[7])
        angle10 = self.myAngle(keyPoint[4], keyPoint[8], keyPoint[7])
        angle11 = self.myAngle(keyPoint[1], keyPoint[8], keyPoint[13])
        angle12 = self.myAngle(keyPoint[1], keyPoint[8], keyPoint[10])
        angle13 = self.myAngle(keyPoint[4], keyPoint[1], keyPoint[8])
        angle14 = self.myAngle(keyPoint[7], keyPoint[1], keyPoint[8])

        return [angle0, angle1, angle2, angle3, angle4, angle5, angle6, angle7,
                angle8, angle9, angle10, angle11, angle12, angle13, angle14]

    def myAngle(self, A, B, C):
        c = math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
        a = math.sqrt((B[0] - C[0]) ** 2 + (B[1] - C[1]) ** 2)
        b = math.sqrt((A[0] - C[0]) ** 2 + (A[1] - C[1]) ** 2)
        if 2 * a * c != 0:
            return (a ** 2 + c ** 2 - b ** 2) / (2 * a * c)
        return 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwin = mWindow()
    mwin.show()
    sys.exit(app.exec_())
