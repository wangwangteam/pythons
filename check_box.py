import xml.etree.ElementTree as ET
import os
import glob


def cover(xmlpath, thresh = 20):
    error = []
    error_type = []
    for path, d, filelist in os.walk(xmlpath):
        for xmlname in filelist:
            if xmlname.endswith('xml'):
                oldname = os.path.join(path, xmlname)
                print(oldname)
                tree = ET.parse(oldname)
                objs = tree.findall('object')
                BB = {}
                Center = {}
                m = 0
                for ix, obj in enumerate(objs):
                        box = obj.find('bndbox')
                        x = obj.find('point')
                        y = obj.find('polygon')
                        while x or y:
                            break
                        else:
                            xmin = float(box.find('xmin').text.strip())
                            ymin = float(box.find('ymin').text.strip())
                            xmax = float(box.find('xmax').text.strip())
                            ymax = float(box.find('ymax').text.strip())
                            b = [xmin, ymin, xmax, ymax]
                            BB[m] = b
                            Center[m] = ((xmax + xmin) / 2.0, (ymax + ymin) / 2.0)
                            m+=1

                if len(Center) > 0:
                    error_num = []
                    for i in range(len(Center) - 1):
                        c1 = Center[i]
                        for j in range(i + 1, len(Center)):
                            c2 = Center[j]
                            d = abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
                            if d < thresh:
                               error.append(oldname)
                               error_num.append(j)
                    error_type.append(str(len(error_num)))
    error = list(set(error))
    error.sort()
    error_type = [x for x in error_type if x != '0']
    for i in range(len(error)):
        keys = error[i]
        print('containing cover boxes : ', keys, error_type[i],'个')

def minibox(xmlpath, thresh = 20):
    error = []
    errors_nums = []

    for path, d, filelist in os.walk(xmlpath):
        for xmlname in filelist:
            if xmlname.endswith('xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                objs = tree.findall('object')
                n = 0
                m = []
                for ix, obj in enumerate(objs):
                    box = obj.find('bndbox')
                    if box is None:
                        continue
                    else:
                        xmin = float(box.find('xmin').text.strip())
                        ymin = float(box.find('ymin').text.strip())
                        xmax = float(box.find('xmax').text.strip())
                        ymax = float(box.find('ymax').text.strip())

                        width = xmax - xmin
                        hight = ymax - ymin
                        n+=1

                        if width < thresh or hight < thresh:
                            error.append(oldname)
                            m.append(n)
                errors_nums.append(str(len(m)))

    errors = list(set(error))
    errors.sort()
    error_num = [x for x in errors_nums if x != '0']
    for i in range(len(errors)):
        keys = errors[i]
        nums = error_num[i]
        print('containing small boxes : ', keys, nums, '个')


def point(xmlpath):
    errors =[]
    errors_nums=[]
    for path, d, filelist in os.walk(xmlpath):
        for xmlname in filelist:
            if xmlname.endswith('xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                objs = tree.findall('object')
                n = 0
                for ix, obj in enumerate(objs):
                        x = obj.find('point')
                        if x is None :
                            continue
                        else:
                            errors.append(oldname)
                            n+=1

                errors_nums.append(str(n))

    errors = list(set(errors))
    errors.sort()
    errors_nums = [x for x in errors_nums if x != '0']
    for i in range(len(errors)):
        keys = errors[i]
        nums = errors_nums[i]
        print('containing point boxes : ', keys, nums, '个')

def polygon(xmlpath):
    errors =[]
    errors_nums=[]
    for path, d, filelist in os.walk(xmlpath):
        for xmlname in filelist:
            if xmlname.endswith('xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                objs = tree.findall('object')
                n = 0
                for ix, obj in enumerate(objs):
                        x = obj.find('polygon')
                        if x is None :
                            continue
                        else:
                            errors.append(oldname)
                            n+=1

                errors_nums.append(str(n))

    errors = list(set(errors))
    errors.sort()
    errors_nums = [x for x in errors_nums if x != '0']
    for i in range(len(errors)):
        keys = errors[i]
        nums = errors_nums[i]
        print('containing polygon boxes : ', keys, nums, '个')

def del_point(xmlpath):
    errors =[]
    errors_nums=[]
    for path, d, filelist in os.walk(xmlpath):
        for xmlname in filelist:
            if xmlname.endswith('xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                root = tree.getroot()
                # print(root)
                for elem in tree.iter(tag='object'):
                    if elem.find('point'):
                        print(oldname)
                        root.remove(elem)
                tree.write(xmlpath + xmlname, encoding="utf-8", xml_declaration=True)
                    # if x is None:
                        #     continue
                        # else:
                        #     tree.remove(obj)
                        #     tree.write(xmlpath + xmlname, encoding="utf-8", xml_declaration=True)
                        #     errors.append(oldname)
                        #     n+=1
                #
                # errors_nums.append(str(n))
    #
    # errors = list(set(errors))
    # errors.sort()
    # errors_nums = [x for x in errors_nums if x != '0']
    # for i in range(len(errors)):
    #     keys = errors[i]
    #     nums = errors_nums[i]
    #     print('containing point boxes : ', keysa, nums, '个')

def filename(path):
    xmls = glob.glob(os.path.join(path, '*/*/'))
    return xmls



if __name__ == '__main__':
    path = '/media/zs/LinkData/zpf_data/txt/bask/'
    xml = filename(path)
    for xml in filename(path):
        print("~~~~~~~~~~~~~~~~~~~check cover  boxes~~~~~~~~~~~~~~~~~")
        cover(xmlpath=xml, thresh=15)

        print("~~~~~~~~~~~~~~~~~~~check mini boxes~~~~~~~~~~~~~~~~~~~")
        minibox(xmlpath=xml, thresh=7)

        print("~~~~~~~~~~~~~~~~~~~check point boxes~~~~~~~~~~~~~~~~~~~")
        point(xmlpath=xml)
        #
        print("~~~~~~~~~~~~~~~~~~~check polygon boxes~~~~~~~~~~~~~~~~~~~")
        polygon(xmlpath=xml)
        print('~~~~~~~~~~~~~~~~~~~del_point_boxes~~~~~~~~~~~~~~~~~~~')
        del_point(path)