import os
from urllib import request, parse
import time
from cluster import knn_detect,get_file_name
import copy
import shutil
# client_id 为官网获取的AK， client_secret 为官网获取的SK
# 获取token
def get_token():
    client_id = 'j6qXAsKVzYtqoGGvX6tLoI15'
    client_secret ='IpyFTwYKgsc5j9SkqmDXRnnsCiVV9IfQ'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s'%(client_id, client_secret)
    req = request.Request(host)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    try:
        response = request.urlopen(req)
    except ConnectionResetError:
        print("connectting error")
        get_token()
    # 获得请求结果
    content = response.read()
    # 结果转化为字符
    content = bytes.decode(content)
    # 转化为字典
    content = eval(content[:-1])
    return content['access_token']


# 转换图片
# 读取文件内容，转换为base64编码
# 二进制方式打开图文件
def imgdata(file1path, file2path):
    import base64
    import json
    f1 = open(r'%s' % file1path, 'rb')
    f2 = open(r'%s' % file2path, 'rb')
    pic1 = base64.b64encode(f1.read())
    pic2 = base64.b64encode(f2.read())
    image1 = str(pic1, 'utf-8')
    image2 = str(pic2, 'utf-8')
    params =json.dumps(
        [{"image": image1, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
         {"image": image2, "image_type": "BASE64", "face_type": "IDCARD", "quality_control": "LOW"}]).encode(encoding='utf-8')
    return params




# 提交进行对比获得结果
def img(file1path, file2path):
    time_start = time.time()
    token = get_token()
    # 人脸识别API
    # url = 'https://aip.baidubce.com/rest/2.0/face/v2/detect?access_token='+token
    # 人脸对比API
    url = 'https://aip.baidubce.com/rest/2.0/face/v3/match?access_token=' + token
    params = imgdata(file1path, file2path)
    # urlencode处理需提交的数据
    # data = parse.urlencode(params).encode('utf-8')
    req = request.Request(url, data=params)
    req.add_header('Content-Type', 'application/json; charset=UTF-8')
    try:
        response = request.urlopen(req)
    except Exception:
        img(file1path,file2path)
    content = response.read()
    content = bytes.decode(content)
    content_dict = eval(content)
    if content_dict.get('result') is None:
        if os.path.exists(file1path):
            os.remove(file1path)
            return 0
        else:
            pass



    # 获得分数
    time_end = time.time()
    time_c = time_end - time_start
    print('time cost:', time_c, 's')
    score = content_dict['result']['score']
    if score > 85:
        print('照片相似度：' + str(score) + ',同一个人')
    else:
        print( '照片相似度：' + str(score) + ',不是同一个人')
    return score


def get_name(path_filenames,labels,id):
    refilelist = []
    for i in range(len(labels)):
        if labels[i]==id:
            refilelist.append(path_filenames[i])
    return refilelist

if __name__ == '__main__':
    error = []
    path_dir = '/media/zs/LinkData/machine_1028/Struct_KeyPoint_1018/4A/4A#175-176@18'
    nums = 4
    n = 0
    for dirs in os.listdir(path_dir):
        start_time = time.time()
        try:
            path_filenames = get_file_name(path_dir + '/' + dirs + '/capture_images/2019-10-19')
        except FileNotFoundError:
            continue
        if not path_filenames:
            continue
        try:
            labels, cluster_centers = knn_detect(path_filenames, nums)
        except ValueError:
            continue
        tmp = os.listdir(path_dir + '/' + dirs)
        file2path = tmp[2]
        file1path = tmp[1]
        try:
            res = img(path_dir + '/' + dirs + '/'+file1path, path_dir + '/' + dirs + '/'+file2path)
            n += 1
            print(n, path_dir + '/' + dirs + '/'+file1path, path_dir + '/' + dirs + '/'+file2path)
            if res < 85:
                shutil.rmtree(path_dir + '/' + dirs)
                continue
        except NameError:
            error.append(path_dir + '/' + dirs)
            shutil.rmtree(path_dir + '/' + dirs)
            continue
        for i in range(nums):
            file_list = get_name(path_filenames, labels, i)
            file3path = file_list[0]
            # time.sleep(0.8)
            try:
                res = img(file3path, path_dir + '/' + dirs + '/'+file2path)
                if res < 85 or res is None:
                    for img_file in file_list:
                        if os.path.exists(img_file):
                            os.remove(img_file)
                        else:
                            pass
            except NameError:
                os.remove(file3path)
                continue
        end_time = time.time()
        time_c = end_time - start_time
        print('time cost:', time_c, 's')
                # file3path = file_list[1]
                # res = img(file3path, path_dir + '/' + dirs + '/'+file2path)
                # os.remove(img_file)
                # if res < 60:
                #     for img_file in file_list:
                #         os.remove(img_file)
    file = open('error1.txt', 'w')
    file.write(str(error))
    file.close()
    list_remain = copy.deepcopy(error)


