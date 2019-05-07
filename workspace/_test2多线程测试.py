import os
import sys
from multiprocessing import Pool,Process
import cv2
import threading
import _thread


def processPic(picPath):
    # ====================import openpose=========================================
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        sys.path.append(dir_path + '/../python/openpose/Release')
        import pyopenpose as op

    except ImportError as e:
        print('Did you enable `BUILD_PYTHON`')
        raise e
    # =============================参数args 设置====================================
    params = dict()
    params["model_folder"] = "F:\\OPENPOSE\\openpose\\models"
    params["number_people_max"] = 1  # 只检测一个人

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    datum = op.Datum()

    imageToProcess = cv2.imread(picPath)

    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop([datum])
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", datum.cvOutputData)
    cv2.waitKey(50)
    dstPicPath = "../../picture/marked_pic/p_" + picPath.split('/')[-1]
    # cv2.imwrite(dstPicPath, datum.cvOutputData)
    print("Sub  END")
    f = open("F:\\OPENPOSE\\openpose\\build\\workspace\\bone_dataSet.data", "w")
    f.write("fdsafsdfas")
    f.close()


if __name__ == '__main__':
    print("Main Start")
    # t = threading.Thread(target=processPic, args=("F:\\OPENPOSE\\sundry\\pic\\threep.jpg",))
    # t.start()
    try:
        p = Process(target=processPic, args=("F:\\OPENPOSE\\sundry\\pic\\threep.jpg",))
        p.start()
        #_thread.start_new_thread(processPic, ("F:\\OPENPOSE\\sundry\\pic\\threep.jpg",))
    except:
        print("ERR")

    # p = Pool(1)
    # p.apply_async(processPic, args=("F:\\OPENPOSE\\sundry\\pic\\threep.jpg",))
    # p.close()
    # p.join()
    print("Main END")

"""
多线程测试
"""