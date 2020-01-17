import urllib, sys
import urllib.request as urllib2#urllib2在py3中我们用urllib.request来替换
import ssl
import json, os, time, shutil

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=j6qXAsKVzYtqoGGvX6tLoI15&client_secret=IpyFTwYKgsc5j9SkqmDXRnnsCiVV9IfQ'
request = urllib2.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib2.urlopen(request)
content = response.read()
if (content):
    access_token=json.loads(content)["access_token"]
    # print(access_token)

# url="https://aip.baidubce.com/rest/2.0/face/v3/search?access_token="+access_token

# encoding:utf-8
import urllib


'''
人脸搜索
'''
import base64

def face_det(img_path, new_path):
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~开始比对~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    with open(img_path, 'rb') as f:
        imageB = base64.b64encode(f.read())
    image = str(imageB, 'utf-8')

    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"


    params = {"image": image, "image_type": "BASE64","quality_control": "LOW", "face_field": "quality", 'max_face_num' : 10}
    # params["image"] = image
    # param = str(params)

    request_url = request_url + "?access_token=" + access_token


    try:
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~开始请求～～～～～～～～～～～～～～～～～～～～～～～～～～～～')
        response = urllib2.urlopen(request_url, data=urllib.parse.urlencode(params).encode("utf-8"))  # data=urllib.parse.urlencode(data).encode("utf-8")
        print('请求状态码：', response.status)
        # response = urllib2.urlopen(request_url)
        content = response.read()
        content = bytes.decode(content)
        response.close()
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~请求结束～～～～～～～～～～～～～～～～～～～～～～～～～～～～')
    except Exception as e:
        print(e)
        print('正在重试！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
        time.sleep(2)

    try:
        content_dict = eval(content)
        # local = content_dict['result']['face_list']['location']
        probability = content_dict['result']['face_list'][0]['face_probability']
        blur = content_dict['result']['face_list'][0]['quality']['blur']
        left_eye = content_dict['result']['face_list'][0]['quality']['occlusion']['left_eye']
        right_eye = content_dict['result']['face_list'][0]['quality']['occlusion']['right_eye']
        complete = content_dict['result']['face_list'][0]['quality']['completeness']
        nose = content_dict['result']['face_list'][0]['quality']['occlusion']['nose']
        print('人脸信度：', probability, '模糊度：', blur, '左眼遮挡程度：', left_eye, '右眼遮挡程度：', right_eye,
              '人脸完整度：', complete, '鼻子遮挡程度：', nose)
        if probability < 0.8:
            os.remove(img_path)
            print('人脸置信度：', probability, '\033[0;31m未检测到人脸,delete finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        elif blur > 0.7:
            os.remove(img_path)
            print('模糊程度：', blur, '\033[0;31m图像太模糊,delete finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        elif left_eye > 0.5:
            os.remove(img_path)
            print('左眼遮挡程度：', left_eye, '\033[0;31m左眼遮挡严重,delete finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        elif right_eye > 0.5:
            os.remove(img_path)
            print('右眼遮挡程度：', right_eye, '\033[0;31m右眼遮挡严重,delete finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        elif complete < 0.5:
            os.remove(img_path)
            print('人脸完整度：', complete, '\033[0;31m人脸不完整,delete finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        elif nose > 0.5:
            os.remove(img_path)
            print('鼻子遮挡度：', nose, '\033[0;31m鼻子遮挡严重,delete finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        else:
            os.makedirs('/media/zs/LinkData/face_data/output_1114/' + new_path.split('/')[6], exist_ok=True)
            shutil.move(img_path, new_path)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~比对结束~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    except NameError:
        os.remove(img_path)
        print('\033[0;31mno face, delete finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')

def get_name(path_filenames,labels,id):
    refilelist = []
    for i in range(len(labels)):
        if labels[i]==id:
            refilelist.append(path_filenames[i])
    return refilelist



if __name__ == '__main__':
    path_dir = '/home/zs/Downloads/face/'
    new_path = '/media/zs/LinkData/face_data/11/'
    for i in os.listdir(path_dir):
        face_path = path_dir + i + '/'
        # print(face_path)
        for img in os.listdir(face_path):
            print(face_path + img, new_path + i + '/' + img)
            # iiii = new_path + i + '/' + img
            try:
                res = face_det(face_path + img, new_path + i + '/' + img)
            except urllib.error.URLError as e:
                time.sleep(10)
                print('Connection reset by peer, 正在重试！！！！！！！！！！！')
                res = face_det(face_path + img, new_path + i + '/' + img)
            # print(iiii.split('/')[6])
