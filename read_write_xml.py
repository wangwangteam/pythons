# @Time    : 2019/9/26
# @Author  : Qi.bt
# @Software: PyCharm

import os
from xml.dom import minidom


def write_xml(path):
    for path, dir_name, file_xm in os.walk(path):
        for name in file_xm:
            if name.endswith('xml'):
                path_xml = path + '/' + name
                dom = minidom.parse(path_xml)
                root = dom.documentElement
                objects = root.getElementsByTagName('object')
                for object in objects:
                    try:
                        xmin = int(object.getElementsByTagName('xmin')[0].firstChild.data)
                        ymin = int(object.getElementsByTagName('ymin')[0].firstChild.data)
                        xmax = int(object.getElementsByTagName('xmax')[0].firstChild.data)
                        ymax = int(object.getElementsByTagName('ymax')[0].firstChild.data)
                    except:
                        continue
                    x1 = xmin
                    y1 = ymin
                    x2 = xmax
                    y2 = ymin
                    x3 = xmax
                    y3 = ymax
                    x4 = xmin
                    y4 = ymax
                    print(x1, y1, x2, y2, x3, y3, x4, y4)
                    # 删除节点
                    bn = root.getElementsByTagName("bndbox")[0]
                    if bn:
                        object.removeChild(bn)
                    polygon = dom.createElement('polygon')
                    object.appendChild(polygon)
                    # 添加节点x1-y4
                    x1_node = dom.createElement('x1')
                    y1_node = dom.createElement('y1')
                    x2_node = dom.createElement('x2')
                    y2_node = dom.createElement('y2')
                    x3_node = dom.createElement('x3')
                    y3_node = dom.createElement('y3')
                    x4_node = dom.createElement('x4')
                    y4_node = dom.createElement('y4')
                    polygon.appendChild(x1_node)
                    polygon.appendChild(y1_node)
                    polygon.appendChild(x2_node)
                    polygon.appendChild(y2_node)
                    polygon.appendChild(x3_node)
                    polygon.appendChild(y3_node)
                    polygon.appendChild(x4_node)
                    polygon.appendChild(y4_node)
                    name_x1 = dom.createTextNode(str(x1))
                    name_y1 = dom.createTextNode(str(y1))
                    name_x2 = dom.createTextNode(str(x2))
                    name_y2 = dom.createTextNode(str(y2))
                    name_x3 = dom.createTextNode(str(x3))
                    name_y3 = dom.createTextNode(str(y3))
                    name_x4 = dom.createTextNode(str(x4))
                    name_y4 = dom.createTextNode(str(y4))
                    x1_node.appendChild(name_x1)
                    x2_node.appendChild(name_x2)
                    x3_node.appendChild(name_x3)
                    x4_node.appendChild(name_x4)
                    y1_node.appendChild(name_y1)
                    y2_node.appendChild(name_y2)
                    y3_node.appendChild(name_y3)
                    y4_node.appendChild(name_y4)
                    try:
                        with open(path_xml, 'w', encoding='utf-8') as f:
                            dom.writexml(f, indent='', addindent='\t', newl='\n', encoding='utf-8')
                            print('ok')
                    except Exception as e:
                        print(e)


if __name__ == '__main__':
    # 文件路径
    path = '/home/zs/Downloads/车流/modalB'
    write_xml(path)
