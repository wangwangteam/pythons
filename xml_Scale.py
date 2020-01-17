#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/29 下午2:49
# @Author : zs
# @Site : 
# @File : add_hw2.py
# @Software: PyCharm

import xml.etree.ElementTree as ET
import os

def rewrite_xml(cwd, newcwd):
    for path, d, filelist in os.walk(cwd):
        for xmlname in filelist:
            if xmlname.endswith('.xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                root = tree.getroot()
                for width in root.iter('width'):
                    width.text = '640'
                for height in root.iter('height'):
                    height.text = '360'
                for xmin in root.iter('xmin'):
                    xmin.text = str(round(int(xmin.text)/3))
                for xmax in root.iter('xmax'):
                    xmax.text = str(round(int(xmax.text)/3))
                for ymin in root.iter('ymin'):
                    ymin.text = str(round(int(ymin.text)/3))
                for ymax in root.iter('ymax'):
                    ymax.text = str(round(int(ymax.text)/3))

                print('正在转换：', os.path.join(newcwd, xmlname))
                tree.write(os.path.join(newcwd, xmlname), encoding="utf-8", xml_declaration=True)



def rename(path):
    f = os.listdir(path)
    f.sort()
    for i in f:
        # print(i)
        oldname = os.path.join(path, i)
        num = str(int(i.split('.')[0]) + 1)
        print(i, num)
        newname = path + '/' + num.zfill(8) + '.xml'
        os.rename(oldname, newname)
        print(oldname, '--->', newname)


def rewritename(cwd, errorname, newname):
    for path, d, filelist in os.walk(cwd):
        for xmlname in filelist:
            if xmlname.endswith('.xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                root = tree.getroot()
                for name in root.iter('name'):
                    if name.text == errorname:
                        print(oldname)
                        name.text = newname
                tree.write(newcwd + xmlname, encoding="utf-8", xml_declaration=True)





if __name__ == '__main__':
    cwd = '/media/zs/sss/可见光剩余/'
    newcwd = '/home/zs/Downloads/xml3/'
    # errorname = ''
    # truename = ''
    # rewritename(newcwd, errorname, truename)
    for class_path in os.listdir(cwd):
        xml_path = os.path.join(cwd, class_path)
        newxml_path = os.path.join(newcwd, class_path)
        # print(xml_path)
        os.makedirs(newxml_path, exist_ok=True)
        rewrite_xml(xml_path, newxml_path)
                # rename(newxml_path)