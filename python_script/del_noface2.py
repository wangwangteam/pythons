#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/19 上午9:22
# @Author : zs
# @Site : 
# @File : del_noface.py
# @Software: PyCharm

from PIL import Image
import face_recognition
import os, shutil
import gc
import threading
import queue
import time


def pro_imgs(root_path):
    for image_path in os.listdir(root_path):
        imgs = os.path.join(root_path, image_path)
        for img in os.listdir(imgs):
            im = os.path.join(imgs, img)
            print('product: ', im)
            q.put(im)
# Load the jpg file into a numpy array
def clean(out_path):
    while not q.empty():
        i = q.get(timeout=10)
        print('get:', i)
        image = face_recognition.load_image_file(i)     #加载图像
        face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")  #检测图像
        print(threading.current_thread().name, i, "I found {} face(s) in this photograph.".format(len(face_locations)))   #检测结果
        if len(face_locations) == 0 or len(face_locations) > 1:
            os.remove(i)
            print('\033[0;31m未检测到人脸或人脸数量大于2，图像已删除！！！！！！！！！！！！！！！！！！！！！！！！！！！！！\033[0m')
        else:
            img_name = i.split('/')[-1]
            new_path = os.path.join(out_path, i.split('/')[-2])
            new_img = os.path.join(out_path, i.split('/')[-2], img_name)
            # print(new_path)
            os.makedirs(new_path, exist_ok=True)
            shutil.move(i, new_img)
            del img_name
            del new_path
        del image
        del face_locations
        gc.collect()


if __name__ == '__main__':
    root_path = '/home/linkdata/face_server/daiab/原始数据/硬盘数据/快手数据30000ID-20190812/ksID-30845'
    out_path = '/home/linkdata/face_server/daiab/原始数据/硬盘数据/快手数据30000ID-20190812'
    q = queue.Queue(1000)
    t = threading.Thread(target=pro_imgs, args=(root_path,), daemon=True)
    t.start()
    time.sleep(10)
    for j in range(40):
        v = threading.Thread(target=clean, args=(out_path,))
        v.start()