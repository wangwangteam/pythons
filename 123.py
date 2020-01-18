#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/18 下午5:48
# @Author : zs
# @Site : 
# @File : add_hw.py
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
                    xmin.text = str(int(1920/640*int(xmin.text)))
                for xmax in root.iter('xmax'):
                    xmax.text = str(int(1920 / 640 * int(xmax.text)))
                for ymin in root.iter('ymin'):
                    ymin.text = str(int(1080/360*int(ymin.text)))
                for ymax in root.iter('ymax'):
                    ymax.text = str(int(1080/360*int(ymax.text)))

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
    cwd = '/home/zs/Downloads/xmls/'
    newcwd = '/home/zs/Downloads/xml1/'
    # errorname = ''
    # truename = ''
    # rewritename(newcwd, errorname, truename)
    for class_path in os.listdir(cwd):
        image_path = os.path.join(cwd, class_path)
        for img in os.listdir(image_path):
            t = image_path + '/' + img
            for image in os.listdir(t):
                img_path = os.path.join(t, image)
                tt = img_path.split('/')[0:6]
                ttt = img_path.split('/')[7:10]
                s = '/'.join(tt)
                ss = '/'.join(ttt)

                xml_path = os.path.join(s, 'xml', ss)
                newxml_path = os.path.join(s, 'newxml', ss)
                # print(xml_path)
                os.makedirs(newxml_path, exist_ok=True)
                rewrite_xml(xml_path, newxml_path)
                # rename(newxml_path)