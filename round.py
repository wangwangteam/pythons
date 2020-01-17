import xml.etree.ElementTree as ET
import os
import math
cwd = '/media/zs/wisin_linkdata/mk/shadowk/Annotations/'
# newcwd = 'newAnnotations/'
newcwd = '/media/zs/wisin_linkdata/mk/shadowk/Annotations/'
for path,d,filelist in os.walk(cwd):
    for xmlname in filelist:
        if xmlname.endswith('xml'):
            oldname = os.path.join(path,xmlname)
            # tree = ET.parse('/home/jianchao/Downloads/rBgODFuQ1s-ARPEFAVZHYGZrMS0490/Annotations/'+str(aaa)+'.xml')
            tree = ET.parse(oldname)
            root = tree.getroot()

            for xmin in root.iter('xmin'):
                xmin.text = str(math.floor(float(xmin.text)))
                a=xmin.text
                print(a)
            for xmax in root.iter('xmax'):
                xmax.text = str(math.floor(float(xmax.text)))
                b=xmax.text
                print(b)
            for ymin in root.iter('ymin'):
                ymin.text = str(math.floor(float(ymin.text)))
                c = ymin.text
                print(c)
            for ymax in root.iter('ymax'):
                ymax.text = str(math.floor(float(ymax.text)))
                d = ymax.text
                print(d)
            # for name in root.iter('name'):
            #     name.text = '@'
            #     e=name.text
            #     print(e)
            tree.write(newcwd + xmlname, encoding="utf-8", xml_declaration=True)


