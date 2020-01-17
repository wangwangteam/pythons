import os, shutil




def filelist(path):
    imgs = []
    for img in os.listdir(path):
        imgs.append(img)
    return imgs


if __name__ == '__main__':
    more_path = '/media/zs/LinkData/dragon_data/face/Annotations/'
    less_path = '/media/zs/LinkData/dragon_data/face_1/JPEGImages/'
    new_path = '/media/zs/LinkData/face_1/Annotations/'
    more_imgs = filelist(more_path)
    for img in more_imgs:
        img_path = os.path.join(less_path, img.split('.')[0] + '.jpg')
        # qqq = more_imgs + img
        # www = new_path + img

        if os.path.exists(img_path):
            pass
        else:
            shutil.copy(more_path + img, new_path + img)


