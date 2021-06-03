import os
import sys

import cv2

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # sys.path.append(dir_path + '/../python/openpose/Release')
    # 一定要注意是 build目录下的python而不是openpose根目录下的
    # 如果一直报错可以将绝对路径加入 path环境变量中去。
    # 或者将绝对路径引进来 F:\\OPENPOSE\\openpose\\build\\python\\openpose\\Release
    # 或是如下添加绝对路径
    # sys.path.append("F:\\OPENPOSE\\openpose\\build\\python\\openpose\\Release")
    # 此句和上句同理 两者只要一者起效便可import openpose
    # import pyopenpose as op
    sys.path.append('/home/wfnian/OPENPOSE/openpose/build/python')
    from openpose import pyopenpose as op

except ImportError as e:
    print('Did you enable `BUILD_PYTHON`')
    raise e
# =============================== 参数设置 =====================================

params = dict()
params["model_folder"] = "/home/wfnian/OPENPOSE/openpose/models"
params["number_people_max"] = 1  # 只检测一个人
params["camera_resolution"] = "800x600"

opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
datum = op.Datum()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    datum.cvInputData = frame
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    resPic = datum.cvOutputData
    cv2.putText(resPic, "OpenPose", (25, 25),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (222, 222, 222))
    cv2.imshow("OpenPose", resPic)
    keyPoints = datum.poseKeypoints.tolist()
    c = cv2.waitKey(5)
    if c == 27:
        break
cap.release()

cv2.destroyWindow("OpenPose")

# 摄像头可用，基于视频的处理
