# ------------------------------------------------------------
# Copyright (c) 2017-present, SeetaTech, Co.,Ltd.
#
# Licensed under the BSD 2-Clause License.
# You should have received a copy of the BSD 2-Clause License
# along with the software. If not, See,
#
#      <https://opensource.org/licenses/BSD-2-Clause>
#
# ------------------------------------------------------------

import os
import cv2
import xml.etree.ElementTree as ET
from collections import defaultdict


def int_f(x):
    return int(round(float(x)))


class PrepareData(object):
    def __init__(self, save_dir):
        self.saver = {}
        self.name_count = defaultdict(int)
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.data = []

    def init_saver(self, names):
        for name in names:
            path = os.path.join(self.save_dir, name)
            os.makedirs(path, exist_ok=True)
            self.saver[name] = path

    def extract(self, img_path, xml_path):
        image = cv2.imread(img_path)
        objs = ET.parse(xml_path).findall('object')

        for obj in objs:
            names = obj.find('name').text.lower()
            bndbox = obj.find('bndbox')
            xmin = int_f(bndbox.find('xmin').text)
            ymin = int_f(bndbox.find('ymin').text)
            xmax = int_f(bndbox.find('xmax').text)
            ymax = int_f(bndbox.find('ymax').text)
            roi = image[ymin:ymax, xmin:xmax, :]
            path = '{}/{:04d}.jpg'.format(self.saver[names], self.name_count[names])
            print(path)
            cv2.imwrite(path, roi)
            self.name_count[names] += 1
            self.data.append('{}\t{}\n'.format(path, names))

    def make(self, imgs_dir, xmls_dir):
        imgs_dir_win = imgs_dir.replace('\\', '/')
        xmls_dir_win = xmls_dir.replace('\\', '/')
        for idx, xml in enumerate(os.listdir(xmls_dir_win)):
            xml_path = os.path.join(xmls_dir_win, xml)
            img_path = os.path.join(imgs_dir_win, str(xml.split('.')[0]) + '.jpg')
            if not os.path.exists(img_path) or not os.path.exists(xml_path):
                print('img file or xml file not exists. ', xml_path)
                continue
            # print(xmls_dir,xml)
            print(idx, img_path)
            self.extract(img_path, xml_path)

    @staticmethod
    def attr_list(xmls_dir):
        names = []
        for xml in os.listdir(xmls_dir):
            xml_path = os.path.join(xmls_dir, xml)
            objs = ET.parse(xml_path).findall('object')
            for obj in objs:
                name = obj.find('name').text.lower()
                names.append(name)


        return set(names)


if __name__ == "__main__":
    imgs_dir = r'D:/006/006_completed/JEPGImages/'
    xmls_dir = r'D:/006/006_completed/Annotations/'
    save_dir = r'D:/006/006_completed/patch/'


    pd = PrepareData(save_dir)
    attrs = pd.attr_list(xmls_dir)
    print(attrs)
    pd.init_saver(attrs)
    pd.make(imgs_dir, xmls_dir)
