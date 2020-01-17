import os
path = r"/media/zs/LinkData/linkdata_1101/JF1101"
f = os.listdir(path)
for i in f:
    ID_path = path + '/' + i + '/'
    for files in os.listdir(ID_path):
        if files.endswith('.png'):
            oldname = os.path.join(ID_path, files)
        elif files.endswith('.bmp'):
            destroy_img = os.path.join(ID_path, files)
    newname = ID_path + i.split('_')[0] + '_0.png'
    os.rename(oldname, newname)
    print(oldname, '--->', newname)
    try:
        if os.path.exists(destroy_img):
            os.remove(destroy_img)
            print(destroy_img, 'delete complte!')
        else:
            print('the file doesnt exist!')
            pass
    except NameError:
        print('delete errrrrrrrrrr:' ,oldname)



