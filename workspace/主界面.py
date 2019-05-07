import os
import sys

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame

from build.workspace.Classification import *
from build.workspace.MainWindow_F import *
from build.workspace.data_process import *
from build.workspace.predict_res import *

# ====================import openpose=========================================
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    sys.path.append(dir_path + '/../python/openpose/Release')
    import pyopenpose as op

except ImportError as e:
    print('Did you enable `BUILD_PYTHON`')
    raise e
# =============================== 参数设置 =====================================

params = dict()
params["model_folder"] = "F:\\OPENPOSE\\openpose\\models"
params["number_people_max"] = 1  # 只检测一个人
params["camera_resolution"] = "640x360"
params["render_threshold"] = 0.01
# ============================= 启动openPose ==================================
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

pos = ["预备势", "起势", "左右野马分鬃", "白鹤亮翅", "左右搂膝拗步", "手挥琵琶",
       "左右倒卷肱", "左揽雀尾", "右拦雀尾", "单鞭", "云手", "高探马", "右蹬脚",
       "双峰贯耳", "转身左蹬脚", "左下式独立", "左下式独立", "左右穿梭", "海底针",
       "闪通臂", "转身搬拦捶", "如封似闭", "十字手"]


class Video:
    def __init__(self, capture):
        self.capture = capture
        self.currentFrame = None
        self.previousFrame = None

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
        """     converts frame to format suitable for QtGui            """
        try:
            height, width = self.currentFrame.shape[:2]
            img = QImage(self.currentFrame,
                         width,
                         height,
                         QtGui.QImage.Format_RGB888)
            img = QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except cv2.Error:
            return None


class mWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mWindow, self).__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.train_network)

        self._timer1 = QTimer(self)
        # self._timer1.timeout.connect(self.setProcessBarValue)
        self._timer1.start(30)  # 每隔多长时间

        self._timer2 = QTimer(self)
        self._timer2.timeout.connect(self.showCapture)
        self.video = Video(cv2.VideoCapture(0))
        self._timer2.start(10)  # 每隔多长时间

        self.label_2.setFrameStyle(QFrame.Panel | QFrame.Sunken)

    def train_network(self):

        train_net()
        self.label_2.setPixmap(QPixmap("F:\\openpose\\sundry\\train_loss_acc_pic.png"))

    def showCapture(self):
        try:

            frame = self.video.captureFrame()
            datum = op.Datum()
            datum.cvInputData = frame
            opWrapper.emplaceAndPop([datum])
            resPic = datum.cvOutputData
            # cv2.putText(resPic, "OpenPose", (25, 25),
            #             cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 222))

            pic = cv2.cvtColor(resPic, cv2.COLOR_BGR2RGB)
            pic = QImage(pic, pic.shape[1], pic.shape[0], QtGui.QImage.Format_RGB888)
            self.label_3.setPixmap(QPixmap.fromImage(pic))

            keyPoints = datum.poseKeypoints.tolist()
            self.label_4.setText(pos[predict_result(pointDistance(keyPoints[0]) +
                                                    pointAngle(keyPoints[0]))])

        except TypeError:
            print("No frame")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywin = mWindow()
    # mywin.setStyleSheet("#MainWindow{border-image:url(F:/OPENPOSE/sundry/icons/back.png);}")
    mywin.show()
    sys.exit(app.exec_())
