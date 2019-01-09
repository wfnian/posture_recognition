import requests
import base64
import json
import cv2


def img2base(file_name):
    with open(file_name, 'rb') as fin:
        file_data = fin.read()
        base_data = base64.b64encode(file_data)

    return base_data


def post_pic():
    url = "https://api-cn.faceplusplus.com/humanbodypp/v1/skeleton"
    file_path = "f:\\pic\\sbn.jpg" #front.jpg"
    img1 = img2base(file_path)
    pic = cv2.imread(file_path, 1)


    post_data = {
        "api_key": "TRSyKP-3x634yVbb7Cz1tBKB2Jl0zB0z",
        "api_secret": "AsV0IfXXKIOUDx3PbZr30obeumB4ekZY",
        "image_base64": img1
    }
    back = requests.post(url, data=post_data)
    res = json.loads(back.text)
    print(res)

    joints = list(res['skeletons'][0]['landmark'].keys())
    l1 = res['skeletons'][0]['body_rectangle']['left']
    l2 = res['skeletons'][0]['body_rectangle']['top']
    for i in joints:
        cv2.circle(pic, (res['skeletons'][0]['landmark'][i]['x']+l1,
                         res['skeletons'][0]['landmark'][i]['y']+l2), 
                   8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
        cv2.putText(pic, "{}".format(i), ((res['skeletons'][0]['landmark'][i]['x']+l1,
                                           res['skeletons'][0]['landmark'][i]['y']+l2)),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 1)
    cv2.imshow("pic", pic)


    cv2.waitKey(0)


if __name__ == '__main__':
    post_pic()
