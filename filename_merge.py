import os


path = '/home/zs/faceID_dab/daiab/split_data1/豆瓣3万人脸数据-拆分/2'

for dir in os.listdir(path):
    dir_path = os.path.join(path, dir)
    n_name = dir_path + '/' + dir_path.split('/')[-1]
    for file_path in os.listdir(dir_path):
        child_file = os.path.join(dir_path, file_path)
        # n1_name = n_name + '_' + file_path.split('_')[-1]
        n1_name = n_name + "_" + file_path
        print(n_name)
        print(n1_name)
        print(child_file)
        # print(n_name)
        os.rename(child_file, n1_name)



