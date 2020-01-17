import time
import requests
import base64
import os
import glob
import threading
import queue


#生成数据队列
def prod_src(src):
    for root, dirs, files in os.walk(src):
        for file in files:
            file_path = os.path.join(root, file)
            # print(file_path)
            q.put(file_path)


def Display(i):
    while 1:
        img_path = q.get(timeout=10)
        with open(img_path, 'rb') as f:
            imgbase64 = base64.b64encode(f.read())
        image = str(imgbase64, 'utf-8')
        json_data = {'image': image}
        st = time.time()
        # r = requests.post("http://127.0.0.1:5004/object", json=json_data).text
        r = requests.post("http://127.0.0.1:5003/face", json=json_data).text
        # r = requests.post("http://101.201.76.251:5004/decimage", json=json_data).text
        et = time.time()
        r = r.encode('utf-8').decode('unicode_escape')
        # print(r)
        print('time', et-st)
        try:
            result = eval(r)
            face_type = result['result']['face_list'][0]['face_type']['type']
            face_probability = result['result']['face_list'][0]['face_probability']
            live_score = result['result']['face_list'][0]['liveness']['livemapscore']
            # print('face_type:', face_type)
            # print('face_probability:', face_probability)
            # print('live_score:', live_score)
            if face_type == 'cartoon':
                print('cartoon:', img_path)
                with open('/home/zs/faceID_dab/daiab/split_data1/豆瓣3万人脸数据-拆分/error_file/cartoon_error.txt', 'a+') as f:
                    f.write(img_path + r + '\n')
            elif face_probability < 0.5:
                print('probability:', img_path)
                with open('/home/zs/faceID_dab/daiab/split_data1/豆瓣3万人脸数据-拆分/error_file/probability_error.txt', 'a+') as f:
                    f.write(img_path + r + '\n')
        except Exception as e:
            print(str(e))
            with open('/home/zs/faceID_dab/daiab/split_data1/豆瓣3万人脸数据-拆分/error_file/no_face_error.txt', 'a+') as f1:
                f1.write(img_path + str(e) +'\n')
if __name__=='__main__':
    path = '/home/zs/faceID_dab/daiab/split_data1/豆瓣3万人脸数据-拆分/0完成'
    q = queue.Queue(500)
    threads = []
    print('--------------准备生产原始数据-------------------')
    t = threading.Thread(target=prod_src, args=(path,), daemon=True)
    t.start()
    print('--------------准备chuli数据-------------------')
    for i in range(1):
        t1 = threading.Thread(target=Display, args=(path,))
        threads.append(t1)
        t1.start()


