#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/11/27 上午9:24
# @Author : zs
# @Site :
# @File : rewrite_xml_cla_name.py
# @Software: PyCharm
import xml.etree.ElementTree as ET
import os

def rewrite_xml(cwd, newtag):
    if cwd.endswith('.xml'):
        print(cwd)
        tree = ET.parse(cwd)
        root = tree.getroot()
        for name in root.iter('name'):
            print(name.tag, '-------->', newtag)
            name.tag = newtag
        tree.write(cwd, encoding="utf-8", xml_declaration=True)


if __name__ == '__main__':
    cwd = '/home/zs/python_scripts/test/'
    newtag = 'test'
    for dir in os.listdir(cwd):
        file_path = os.path.join(cwd, dir)
        rewrite_xml(file_path, newtag)