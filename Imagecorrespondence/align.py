#!/usr/bin/env python
# encoding: utf-8

# --------------------------------------------------------
# file: seeta_dataset.py
# Copyright(c) 2017-2020 SeetaTech
# Written by Zhuang Liu
# 2019/5/13 15:02
# --------------------------------------------------------

import os
import os.path as osp
import cv2
import xml.etree.ElementTree as ET
import numpy as np

def get_points(xml_path):
    root = ET.parse(xml_path)
    objs = root.findall('object')
    pts = []
    for obj in objs:
        point = obj.find('point')
        x = int(point.find('x').text)
        y = int(point.find('y').text)
        pts.append([x, y])
    return pts

def init_warpMatrixFromMultiplyXMLs(rgb_xmls, infrared_xmls):
    src_pts = []
    dst_pts = []
    for i in range(len(rgb_xmls)):
        rgb_xml = rgb_xmls[i]
        infrared_xml = infrared_xmls[i]
        src_pts.extend(get_points(rgb_xml))
        dst_pts.extend(get_points(infrared_xml))
    src_pts = np.float32(src_pts).reshape(-1, 1, 2)
    dst_pts = np.float32(dst_pts).reshape(-1, 1, 2)
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    return H

def init_transform_matrix():
    # initialize mapping matrix
    ids = [2, 4, 5, 8, 12, 21, 30, 35, 47, 60]
    rgb_xmls = [osp.join('KJW-MAP', 'DJI_{:0>4}.xml'.format(id)) for id in ids]
    infrared_xmls = [osp.join('/home/zs/python_scripts/rgb/KJW-MAP', 'DJI_{:0>4}_R.xml'.format(id-1)) for id in ids]
    H = init_warpMatrixFromMultiplyXMLs(rgb_xmls, infrared_xmls)
    return H

def cv_imread(file_path, type=0):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    if type == 0:
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    return cv_img

# H: transform matrix
# image_pair: [rgb_path, infrared_path]
def processing_data(H, image_pair, crop_ratio = 0.2, progress=False):
    src_rgb_path = image_pair[0]
    src_infrared_path = image_pair[1]
    dst_rgb_path = src_rgb_path.replace('demo', 'demo_res')
    dst_infrared_path = src_infrared_path.replace('demo', 'demo_res')
   # warp rgb image to infrared image
    rgb_img = cv_imread(src_rgb_path, -1)
    infrared_img = cv_imread(src_infrared_path, -1)
    h, w, _ = infrared_img.shape
    wrap = cv2.warpPerspective(rgb_img, H, (w, h))
    if progress:
        cv2.imwrite(dst_rgb_path[:-4]+'_oriwarp.jpg', wrap)
        cv2.imwrite(dst_infrared_path[:-4]+'_ori.jpg', infrared_img)
    # center-crop
    top = int(h / 2 * crop_ratio)
    bottom = h - top
    left = int(w / 2 * crop_ratio)
    right = w - left
    wrap = wrap[top:bottom, left:right, :]
    infrared_img = infrared_img[top:bottom, left:right, :]
    if progress:
        cv2.imwrite(dst_rgb_path[:-4]+'_oriwarp_centercrop.jpg', wrap)
        cv2.imwrite(dst_infrared_path[:-4]+'_ori_centercrop.jpg', infrared_img)

    # resize back to (h, w, 3)
    wrap = cv2.resize(wrap, (w, h), interpolation=cv2.INTER_CUBIC)
    infrared_img = cv2.resize(infrared_img, (w, h), interpolation=cv2.INTER_CUBIC)
    # save
    if progress:
        cv2.imwrite(dst_rgb_path, wrap, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        cv2.imwrite(dst_infrared_path, infrared_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    print(dst_infrared_path)
    print(dst_rgb_path)
    cv2.imshow('wrap', wrap)
    cv2.imshow('infrared', infrared_img)
    cv2.waitKey(0)

if __name__ == '__main__':
    H = init_transform_matrix()

    root_dir = 'demo1'
    imagenames = os.listdir(root_dir)
    for imagename in imagenames:
        if 'R' in imagename:
            idstr = imagename.split('_')[0]
            id = int(idstr)
            src_infrared_path = osp.join(root_dir, imagename)
            src_rgb_path = osp.join(root_dir, idstr + '.jpg')
            processing_data(H, [src_rgb_path, src_infrared_path], progress=True)
