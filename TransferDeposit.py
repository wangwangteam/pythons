import os, shutil

def walk_dir(suffix, *paths):
    dir_map = []
    for path in paths:
        for (root, dirs, files) in os.walk(path):
            # print(root)
            for item in files:
                if item.endswith(suffix):
                    xml_path = os.path.join(root,item)
                    dir_map.append(xml_path)
    return  dir_map

def TransferDeposit(xmls_path,newpath):
    for path in xmls_path:
        shutil.copy(path, newpath)
        print(path)

if __name__ == '__main__':
    XML_DIR = r'/media/zs/13004/人脸（3)'
    new_path = r'/media/zs/LinkData/dragon_data/machine_write_xml/face_3/JPEGImages'
    xmls_path = walk_dir('jpg', XML_DIR)
    TransferDeposit(xmls_path, new_path)

