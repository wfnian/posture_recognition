# Overview ![](https://camo.githubusercontent.com/2d21dcc74fc13272cce1a3b020085968fc269cf7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f70726f70657274792d706572736f6e616c2532307265706f7369746f72792d627269676874677265656e2e737667)

- ![](https://img.shields.io/badge/Author-%40wfnian%F0%9F%98%81-red.svg)
- Posture recognition based on common camera 基于普通摄像头的太极姿势识别(分类)
- 相关：[基于Kinect的姿态识别(分类)](https://github.com/wfnian/kinect/wiki)
- 若有需要和问题可提issues.

## 安装与使用
首先根据OpenPose WindowsAPI安装说明安装，调用方式为Python调用。  
[OpenPose GitHub地址](https://github.com/CMU-Perceptual-Computing-Lab/openpose)  
[Windows OpenPose安装说明](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md)

### 程序开发目录说明
> `git clone` 下来后`cmake`进行编译,其中要勾选`BUILD_PYTHON`进行编译才能被python调用。
> 
![](./sundry/dir.png)

workspace 程序开发目录详细说明

- workspace
  - OpenPose_python_Demo📁
  - runs📁
  - data_collection📁
  - dataset📁
    - taichi📁
      - marked_pic📁
        - p_2_0.jpg（最后一个下划线后面是类别，此处`0`是类别）
        - ...
      - marked_pictrain.txt📄


