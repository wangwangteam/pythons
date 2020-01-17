# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
from collections import defaultdict


def walk_dir(suffix, *paths):
    dir_map = {}
    for path in paths:
        for (root, dirs, files) in os.walk(path):
            # print(files)
            for item in files:
                if item.endswith(suffix):
                    d = os.path.abspath(os.path.join(root, item))
                    dir_map[os.path.splitext(item)[0]] = d
    return dir_map

def count(xmls):
    result = defaultdict(int)
    for key in xmls:
        # print(key)
        tree = ET.parse(xmls[key])
        objs = tree.findall('object')
        for ix, obj in enumerate(objs):
            bbox = obj.find('bndbox')
            if bbox is None:
                continue
            name = obj.find('name').text
            result[name] += 1
    return result


if __name__ == '__main__':

    XML_DIR = r'/media/zs/LinkData/dragon_data/cars/rectangle/Annotations/'
    xmls = walk_dir('xml', XML_DIR)
    ret = count(xmls)
    # print(ret)
    count_num = 0
    for i in range(len(ret)):
        keys = list(ret.keys())
        count_num += ret[keys[i]]
        print(keys[i], ":", ret[keys[i]])
        print('all classes is :', keys)
        print('count_num is: ', count_num)

