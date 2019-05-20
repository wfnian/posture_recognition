import os
import sys


def m_main():  # 对于视频的处理
    # ====================import openpose=========================================
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
    params["camera_resolution"] = "640x360"
    # params["disable_blending"] = True  #此处可以控制是否显示背景或者是只显示骨骼图
    params["render_threshold"] = 0.001


    opWrapper = op.WrapperPython(3)
    opWrapper.configure(params)
    opWrapper.execute()



if __name__ == '__main__':
    m_main()
