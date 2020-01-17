from aip import AipFace
from aip import AipImageClassify
from flask import Flask, request
import base64
import json



""" 这里创建face的三个参数"""
APP_ID_face = '17621651'
API_KEY_face = 'j6qXAsKVzYtqoGGvX6tLoI15'
SECRET_KEY_face = 'IpyFTwYKgsc5j9SkqmDXRnnsCiVV9IfQ'
client_face = AipFace(APP_ID_face, API_KEY_face, SECRET_KEY_face)
""" 这里创建object的三个参数"""
APP_ID_obj = '18223036'
API_KEY_obj = 'oqsk7txXSU3zOgnxbbSqi0GV'
SECRET_KEY_obj = 'NFSgQtZ8dEHuY2z35dnOc5d4meKvysOU'
client_obj = AipImageClassify(APP_ID_obj, API_KEY_obj, SECRET_KEY_obj)

app = Flask("my-app")
@app.route('/object', methods=['POST'])
def object():
    image_base64 = request.json['image']
    # print(image_base64)
    with open('image.jpg', 'wb') as f:
        f.write(base64.b64decode(image_base64))
    image = get_file_content('image.jpg')
    """ 调用通用物体识别 """
    result = client_obj.advancedGeneral(image)
    print(result)
    return json.dumps(result)

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()



@app.route('/face', methods=['POST'])
def face():
    image_base64 = request.json['image']
    imageType = "BASE64"
    options = {}
    options["face_field"] = "age"
    options['face_field'] = 'face_type'
    options["max_face_num"] = 2
    options["face_type"] = "LIVE"
    options["liveness_control"] = "LOW"
    """ 调用人脸检测 """
    result = client_face.detect(image_base64, imageType, options)
    print(result)
    print(type(result))
    return json.dumps(result)


@app.route('/campareface', methods=['POST'])
def face():
    image_base64 = request.json['image']
    imageType = "BASE64"
    options = {}
    options["face_field"] = "age"
    options['face_field'] = 'face_type'
    options["max_face_num"] = 2
    options["face_type"] = "LIVE"
    options["liveness_control"] = "LOW"
    """ 调用人脸检测 """
    result = client_face.detect(image_base64, imageType, options)
    print(result)
    print(type(result))
    return json.dumps(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)


