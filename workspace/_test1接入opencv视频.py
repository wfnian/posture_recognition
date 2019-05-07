import os
import sys

import cv2

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append(dir_path + '/../python/openpose/Release')
    import pyopenpose as op

except ImportError as e:
    print('Error: Did you enable `BUILD_PYTHON`')
    raise e

params = dict()
params["model_folder"] = "F:\\OPENPOSE\\openpose\\models"
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
    opWrapper.emplaceAndPop([datum])
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
