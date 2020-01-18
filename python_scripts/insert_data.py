#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/23 上午9:38
# @Author : zs
# @Site : 
# @File : insert_data.py
# @Software: PyCharm

import os
import shutil
import random
import gc
import threading
import time
import queue


#生成要填充的数据队列
def prod_src(src):
    while True:
        for root, dirs, files in os.walk(src):
            for name in files:
                img = os.path.join(root, name)
                print(img)
                q.put(img)

#生成填充的目标路径队列
def prod_dst(dst):
        for root, dirs, files in os.walk(dst):
            for name in dirs:
                file = os.path.join(root, name)
                q2.put(file)

#成对的取数据和目标路径进行同步填充（n个数据：1个路径）
def insert_data(i):
    for j in range(len(os.listdir(i))):
        rd = random.randint(200, 230)
        while not q2.empty():
            dst_file = q2.get(timeout=10)
            j += 1
            print(threading.currentThread().getName(), '正在向%s插入数据！正在执行该线程的第%s个文件夹' % (dst_file, j))
            for k in range(rd):
                src_img = q.get()
                shutil.copy(src_img, dst_file)



if __name__ == '__main__':
    q = queue.Queue(4000)
    q2 = queue.Queue(20)
    src = '/media/zs/LinkData/1/1'
    dst = '/media/zs/LinkData/1/2'
    threads = []
    print('--------------准备生产原始数据-------------------')
    t1 = threading.Thread(target=prod_src, args=(src,), daemon=True)
    t1.start()
    time.sleep(20)
    print('--------------准备生产待插入目录-------------------')
    t2 = threading.Thread(target=prod_dst, args=(dst,))
    t2.start()
    # time.sleep(10)
    for i in range(20):
        t3 = threading.Thread(target=insert_data, args=(dst,))
        threads.append(t3)
    print('--------------准备开启插入线程-------------------')
    for thread in threads:
        thread.start()
    # thread.join()
        # print(thread.getName())
