#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/18 上午9:52
# @Author : zs
# @Site : 
# @File : rename.py
# @Software: PyCharm

import os, cv2
path = r"/media/zs/13004/132/xml/20/DJI_0014_out/"

f = os.listdir(path)
f.sort()
for i in f:
    # print(i)
    oldname= path + i
    num =str(int(i.split('.')[0]) + 1)
    print(i, num)
    newname = path + num.zfill(8) + '.xml'
    os.rename(oldname, newname)
    print(oldname, '--->', newname)

