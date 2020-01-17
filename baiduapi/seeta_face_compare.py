import requests
import os
import shutil


def send_message(image1_file, image2_file):
    url = "https://cloud.seetatech.com/api/face/compare"
    values = {}
    values['api_key'] = "CC2893E9F79F4E6C970674BD29B6A124"
    values['secret_key'] = "B2DDA6CF540BC167815979778974061B"
    # values['predict_age'] = 1
    # values['predict_emotion'] = 1
    # values['frontal'] = 1
    # values['roi'] = '{"x": 30, "y": 30, "width": 9000, "height": 9000}'
    files = {'image1_file': open(image1_file, 'rb'), 'image2_file': open(image2_file, 'rb')}
    response = requests.post(url, values, verify=False, files=files)

    # print(response)
    res = response.json()
    print(res['res'])
    if res['res'] == 11113:
        os.remove(image2)
    elif res['res'] == 11112:
        os.remove(image1)
    try:
        confidence = res['confidence']
        print(res)
        return confidence
    except KeyError:
        pass




if __name__ == '__main__':
    path_dir = '/media/zs/LinkData/face_data/fece/'
    out_path = '/media/zs/LinkData/face_data/outface/'
    for i in os.listdir(path_dir):
        face_path = path_dir + i + '/'
        for j in range(len(os.listdir(face_path))):

            for img in os.listdir(face_path):
                if os.listdir(face_path):
                    image1 = face_path + os.listdir(face_path)[0]
                    image2 = face_path + img
                    # print(image1.split('/')[-1])
                print(image1, image2)
                if image1 == image2:
                    os.makedirs(out_path + i + '/' + str(j), exist_ok=True)
                    shutil.copy(image1, out_path + i + '/' + str(j) + '/' + img)
                    pass
                else:
                    score = send_message(image1, image2)
                    print(score)
                    if score == None:
                        continue
                    try:
                        if score > 0.7:
                            # os.makedirs(out_path + i + '/' + str(j),exist_ok=True)
                            shutil.move(image2, out_path + i + '/' + str(j) + '/' + img)
                    except TypeError:
                        pass
            try:
                os.remove(image1)
            except FileNotFoundError:
                pass
            # shutil.move(image1, out_path + i + '/' + str(j) + '/' + image1.split('/')[-1])











