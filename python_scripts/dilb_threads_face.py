# -*- coding:utf-8 -*-
import os
import dlib
import glob
import cv2
from PIL import Image
import gc
import threading
import time
import queue


try:
    import face_recognition_models

    # 加载检测模型文件
    detector = dlib.get_frontal_face_detector()

    # predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
    # pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

    shape_predictor_model = face_recognition_models.pose_predictor_five_point_model_location()
    # pose_predictor_5_point = dlib.shape_predictor(predictor_5_point_model)
    shape_detector = dlib.shape_predictor(shape_predictor_model)

    # cnn_face_detection_model = face_recognition_models.cnn_face_detector_model_location()
    # cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)

    face_rec_model = face_recognition_models.face_recognition_model_location()
    # face_encoder = dlib.face_recognition_model_v1(face_recognition_model)
    face_recognizer = dlib.face_recognition_model_v1(face_rec_model)

except Exception:
    print("Please install `face_recognition_models` with this command before using `face_recognition`:\n")
    print("pip install git+https://github.com/ageitgey/face_recognition_models")
    quit()



q = queue.Queue(50)     # 生成一个队列，用来保存“包子”，最大数量为10

def productor(i):
    # 生产者生产数据路径
    # while True:
        for path, dirs, files in os.walk(root):
            for dir in dirs:
                file_path = os.path.join(path, dir)
                # print(len(os.listdir(root)))
                # print('正在入队:', file_path)
                out_path = os.path.join(output, dir)
                q.put([file_path, out_path])


def consumer(j):
    # 消费者拿到路径进行数据处理
    while not q.empty():
        face_folder, output_folder = q.get()
        print(threading.current_thread().name, '正在出队：', face_folder)
        # 为后面操作方便，建了几个列表
        descriptors = []
        images = []
        # 遍历faces文件夹中所有的图片
        for f in glob.glob(os.path.join(face_folder, "*.jpg")):
            # print('Processing file：{}'.format(f))
            # 读取图片
            img = cv2.imread(f)
            # 转换到rgb颜色空间
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 检测人脸
            dets = detector(img2, 1)
            # print("Number of faces detected: {}".format(len(dets)))

            # 遍历所有的人脸
            for index, face in enumerate(dets):
                # 检测人脸特征点
                shape = shape_detector(img2, face)
                # 投影到128D
                face_descriptor = face_recognizer.compute_face_descriptor(img2, shape)
                # 保存相关信息
                descriptors.append(face_descriptor)
                images.append((img2, shape))

        # 聚类
        labels = dlib.chinese_whispers_clustering(descriptors, 0.35)
        # print("labels: {}".format(labels))
        num_classes = len(set(labels))
        print(threading.current_thread().name, "Number of clusters: {}".format(num_classes))

        # 为了方便操作，用字典类型保存
        face_dict = {}
        for i in range(num_classes):
            face_dict[i] = []
        # print face_dict
        for i in range(len(labels)):
            face_dict[labels[i]].append(images[i])

        # print face_dict.keys()
        # 遍历字典，保存结果
        # file_len = {}
        for key in face_dict.keys():
            file_dir = os.path.join(output_folder, str(key))
            if not os.path.isdir(file_dir):
                os.makedirs(file_dir, exist_ok=True)

            for index, (image, shape) in enumerate(face_dict[key]):
                file_path = os.path.join(file_dir, 'face_' + str(index))
                # print(file_path)
                im = Image.fromarray(image)
                im.save(file_path + '.jpg')
        try:
            del descriptors, face_descriptor, face_folder, file_dir, file_path, image, img, img2, labels, shape, images, dets, face_dict, im
            gc.collect()
        except UnboundLocalError:
            print('local variable referenced before assignment')


if __name__ == '__main__':
    root = '/home/linkdata/face_server/daiab/ceshi/out'
    output = '/home/linkdata/face_server/daiab/ceshi/1'
    # threads = []
    # 实例化了3个生产者
    for i in range(1):
        t = threading.Thread(target=productor, args=(i,), daemon=True)
        t.start()
        print('t_start')
        time.sleep(5)
        # 实例化了4个消费者
    for j in range(12):
        # print('v_strat')
        v = threading.Thread(target=consumer, args=(j,))
        v.start()
        # print('v_starting')

