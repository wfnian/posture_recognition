import os
import sys
import argparse
import cv2


def m_main():
    # ====================import openpose=========================================
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:

        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../python/openpose/Release')
        import pyopenpose as op


    except ImportError as e:
        print(
            'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python '
            'script in the right folder?')
        raise e

    # =============================参数args 设置====================================
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default="F:\\OPENPOSE\\sundry\\pic\\side.jpg")
    # parser.add_argument("--video", default="F:\\OPENPOSE\\sundry\\twop.mp4",
    #                    help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")

    args = parser.parse_known_args()

    params = dict()
    params["model_folder"] = "F:\\OPENPOSE\\openpose\\models"
    # params["number_people_max"] = 1  # 只检测一个人
    params["video"] = ""
    # print(args)# (Namespace(image_path='F:\\OPENPOSE\\openpose\\images\\intrinsics\\dq.jpg'), [])
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1]) - 1:
            next_item = args[1][i + 1]
        else:
            next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-', '')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-', '')
            if key not in params: params[key] = next_item

    opWrapper = op.WrapperPython()
    print(params)
    print(args)

    opWrapper.configure(params)
    opWrapper.start()

    datum = op.Datum()

    imageToProcess = cv2.imread(args[0].image_dir)
    datum.cvInputData = imageToProcess
    opWrapper.emplaceAndPop([datum])
    print((datum.poseKeypoints.tolist())[0][0][0])
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    cv2.imshow("OpenPose 1.4.0 - Tutorial Python API", datum.cvOutputData)
    cv2.imwrite("F:\\OPENPOSE\\sundry\\pic\\mside.jpg", datum.cvOutputData)

    cv2.waitKey(500)


m_main()
