#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/12/3 下午7:13
# @Author : zs
# @Site : 
# @File : test.py
# @Software: PyCharm

import os
import shutil


def main(list):
    list.sort()
    a = max(int(list[0]), int(list[1]))
    b = min(int(list[0]), int(list[1]))
    for i in range(2, len(list)):
        if int(list[i]) > a:
            b = a
            a = int(list[i])
        elif int(list[i]) > b:
            b = int(list[i])
    return a, b


def onefile(list):
    list.sort()
    a = list[0]
    return a


if __name__ == '__main__':
    oldpath = '/home/zs/face_rec/test_out'
    # new_path = '/home/zs/face_rec/test'
    for i in os.listdir(oldpath):
        new_path = '/home/zs/face_rec/two_file'
        new_path = os.path.join(new_path, i)
        i = os.path.join(oldpath, i)
        dict = {}
        for j in os.listdir(i):
            j = os.path.join(i, j)
            dict.update({len(os.listdir(j)): j})
        print(dict)

    # dict = {'12': '/home/test1/', '3': '/home/test2/', '9': '/home/test3/', '1': '/home/test4/', '91': '/home/test5/'}
        filelist = list(dict.keys())
        try:
            x, y = main(filelist)
            print(x, y)
            path1, path2 = dict.get(x), dict.get(y)
            print(path1, path2)
            # print(dict.get(str(y)))
            # os.makedirs(new_path, exist_ok=True)
            if not os.path.exists(os.path.join(new_path, '1')):
                shutil.copytree(path1, os.path.join(new_path, '1'))
                # os.makedirs(new_path, exist_ok=True)
                shutil.copytree(path2, os.path.join(new_path, '2'))
            else:
                print('已存在目标数据文件！')
        except IndexError:
            x = onefile(filelist)
            print(x)
            path1 = dict.get(x)
            print(path1)
            # os.makedirs(new_path, exist_ok=True)
            if not os.path.exists(os.path.join(new_path, '1')):
                shutil.copytree(path1, os.path.join(new_path, '1'))
            else:
                print('已存在目标数据文件！')





