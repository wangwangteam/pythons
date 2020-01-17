#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/29 下午7:40
# @Author : zs
# @Site : 
# @File : rename3.py
# @Software: PyCharm

import os, re
path = r"/home/zs/Downloads/XML/"

f = os.listdir(path)
f.sort()
n = 0
for i in f:
    # print(i)

    oldname = os.path.join(path, i)

    newname = os.path.join(path, str(int(re.findall(r'[(](.*?)[)]', i)[0])-1) + '.xml')
    # n += 1
    os.rename(oldname, newname)
    print(oldname, '--->', newname)