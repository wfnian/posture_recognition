import os
import sys

import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow

from build.workspace.data_process import *
from build.workspace.predict_res import *
from build.workspace.testWindow import *

picSN = 0

# ====================import openpose=========================================
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    sys.path.append(dir_path + '/../python/openpose/Release')
    import pyopenpose as op

except ImportError as e:
    print('Did you enable `BUILD_PYTHON`')
    raise e
# ============================= 参数设置 ==================================

params = dict()
params["model_folder"] = "F:\\OPENPOSE\\openpose\\models"
params["number_people_max"] = 1  # 只检测一个人
params["camera_resolution"] = "640x360"
params["render_threshold"] = 0.01
# ============================= 启动openPose ==================================
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()


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
        self._timer1 = QTimer(self)
        self._timer1.timeout.connect(self.showCapture)
        self.video = Video(cv2.VideoCapture(0))
        self._timer1.start(10)  # 每隔多长时间
        self.pushButton.clicked.connect(self.savePic)
        self.picPaths = None

    def showCapture(self):
        try:
            self.video.captureNextFrame()
            self.label.setPixmap(self.video.convertFrame())
            frame = self.video.captureFrame()
            datum = op.Datum()
            datum.cvInputData = frame
            opWrapper.emplaceAndPop([datum])
            resPic = datum.cvOutputData
            cv2.putText(resPic, "OpenPose", (25, 25),
                        cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 222))

            pic = cv2.cvtColor(resPic, cv2.COLOR_BGR2RGB)
            pic = QImage(pic, pic.shape[1], pic.shape[0], QtGui.QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(pic))

            keyPoints = datum.poseKeypoints.tolist()
            self.label_4.setText(str(predict_result(pointDistance(keyPoints[0]) +
                                                    pointAngle(keyPoints[0]))))

        except TypeError:
            print("No frame")

    def savePic(self):
        self.video.captureNextFrame()
        frame = self.video.convertFrame()
        self.label_2.setPixmap(frame)
        self.label_2.setScaledContents(False)  # 设置图片自适应窗口

        capturedFrame = self.video.captureFrame()
        pose = self.lineEdit.text()
        global picSN

        picSN += 1
        pictureName = str(picSN) + '_' + pose + ".jpg"

        self.picPaths = "../../" + pictureName
        cv2.imwrite(self.picPaths, capturedFrame)
        print('captured')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwin = mWindow()
    mwin.show()
    sys.exit(app.exec_())
