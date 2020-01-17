import cv2, os

def addimg(img_path, label_path, new_path):
    img = cv2.imread(img_path)
    label = cv2.imread(label_path)
    add = cv2.addWeighted(img, 1.0, label, 0.5, 0)
    path = new_path + '/' + i
    cv2.imwrite(path, add)

def walk_dir(suffix, *paths):
    dir_map = []
    for path in paths:
        for (root, dirs, files) in os.walk(path):
            for item in files:
                if item.endswith(suffix):
                    dir_map.append(item)
    return  dir_map


def dir_name(path):
    dir_names = os.listdir(path)
    return dir_names


def path_join(img_path):
    imgs_path = os.path.join(img_path, 'imgs')
    labels_path = os.path.join(img_path, 'label')
    new_path = os.path.join(img_path,'add')
    os.makedirs(new_path, exist_ok=True)
    return imgs_path, labels_path, new_path


if __name__ == '__main__':
    DATA_PATH = r'G:\add_test'
    dir_names = dir_name(DATA_PATH)
    for d in dir_names:
        img_path = os.path.join(DATA_PATH,d)
        i_path, l_path, new_path = path_join(img_path)
        for i in walk_dir('png',i_path):
            imgss_path = os.path.join(i_path,i)
            lables_path = os.path.join(l_path,i)
            addimg(imgss_path, lables_path, new_path)
        print(i_path)







