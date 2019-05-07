import os
import sys


def m_main():  # 对于视频的处理
    # ====================import openpose=========================================
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release')
        # 一定要注意是 build目录下的python而不是openpose根目录下的
        # 如果一直报错可以将绝对路径加入 path环境变量中去。
        # 或者将绝对路径引进来 F:\\OPENPOSE\\openpose\\build\\python\\openpose\\Release
        #
        sys.path.append("F:\\OPENPOSE\\openpose\\build\\python\\openpose\\Release")
        import pyopenpose as op

    except ImportError as e:
        print('Error: Did you enable `BUILD_PYTHON`')
        raise e

    # =============================参数args 设置====================================

    params = dict()
    params["model_folder"] = "F:\\OPENPOSE\\openpose\\models\\"
    params["number_people_max"] = 1  # 只检测一个人
    params["camera_resolution"] = "640x360"
    # params["disable_blending"] = True  #此处可以控制是否显示背景或者是只显示骨骼图
    params["render_threshold"] = 0.001


    opWrapper = op.WrapperPython(3)
    opWrapper.configure(params)
    opWrapper.execute()



if __name__ == '__main__':
    m_main()
