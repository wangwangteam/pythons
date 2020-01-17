# @Time    : 2019/9/14
# @Author  : Qi.bt
# @Software: PyCharm


import os
from xml.dom import minidom


def read_xml():
    path = r'C:\Users\blue\Desktop'
    xml_list = os.listdir(path)
    for i in xml_list:
        if i.endswith('xml'):
            dizhi = path + '\\' + i
            dom = minidom.parse(dizhi)
            root = dom.documentElement
            objects = root.getElementsByTagName('object')
            segmented = root.getElementsByTagName('segmented')[0].firstChild.data
            for object in objects:
                try:
                    difficult = object.getElementsByTagName('difficult')[0].firstChild.data
                    occluded = object.getElementsByTagName('occluded')[0].firstChild.data
                    pose = object.getElementsByTagName('pose')[0].firstChild.data
                    truncated = object.getElementsByTagName('truncated')[0].firstChild.data
                    print(difficult, occluded, pose, truncated)
                except:
                    continue
                finally:
                    write_xml(difficult, occluded, pose, truncated, segmented)


def write_xml(path):
    xml_list = os.listdir(path)
    for i in xml_list:
        if i.endswith('xml'):
            dizhi = path + '/' + i
            dom = minidom.parse(dizhi)
            root = dom.documentElement
            annotation = dom.createElement('segmented')
            root.appendChild(annotation)
            segm = dom.createTextNode(str(0))
            annotation.appendChild(segm)
            objects = root.getElementsByTagName('object')
            for object in objects:
                diff = dom.createElement('difficult')
                object.appendChild(diff)
                name_d = dom.createTextNode(str(0))
                diff.appendChild(name_d)
                occ = dom.createElement('occluded')
                object.appendChild(occ)
                name_o = dom.createTextNode(str(0))
                occ.appendChild(name_o)
                po = dom.createElement('pose')
                object.appendChild(po)
                name_p = dom.createTextNode(str('Unspecified'))
                po.appendChild(name_p)
                trun = dom.createElement('truncated')
                object.appendChild(trun)
                name_t = dom.createTextNode(str(0))
                trun.appendChild(name_t)
                try:
                    with open(dizhi, 'w', encoding='utf-8') as f:
                        dom.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')
                        print('ok')
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    # read_xml()
    # 文件路径
    path = r'/media/zs/LinkData/dragon_data/safe_hat/Annotations'
    write_xml(path)
