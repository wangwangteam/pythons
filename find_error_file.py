import xml.etree.ElementTree as ET
import os

"""
cwd : The root directory of oldXML
nwcwd: The root directory of rewrite XML
errorname : Error label name
newname : Correct label name 

"""

def find_errofile(cwd, filename):
    for path, d, filelist in os.walk(cwd):
        for xmlname in filelist:
            if xmlname.endswith('xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                root = tree.getroot()
                for name in root.iter('name'):
                    if name.text == filename:
                        print(oldname)




def rewrite_xml(errorname, newname):
    for path, d, filelist in os.walk(cwd):
        for xmlname in filelist:
            if xmlname.endswith('.xml'):
                oldname = os.path.join(path, xmlname)
                tree = ET.parse(oldname)
                root = tree.getroot()
                for name in root.iter('name'):
                    if name.text == errorname:
                        print(oldname)
                        name.text = newname
                tree.write(newcwd + xmlname, encoding="utf-8", xml_declaration=True)


def rewrite_xml2(errorname, newname, start_id, end_id):
    for path, d, filelist in os.walk(cwd):
        # print(filelist[1])
        filelist_new = filelist[int(start_id)-1:int(end_id)]
        print(filelist_new)
        for xmlname in filelist_new:
            if xmlname.endswith('xml'):
                oldname = os.path.join(path, xmlname)

                tree = ET.parse(oldname)
                root = tree.getroot()
                for name in root.iter('name'):
                    if name.text == errorname:
                        print(oldname)
                        name.text = newname
                tree.write(newcwd + xmlname, encoding="utf-8", xml_declaration=True)

if __name__ == '__main__':
    cwd = r'/media/zs/LinkData/dragon_data/face/Annotations/'
    newcwd = cwd
    start_id = '1086'
    end_id = '1119'
    errorname = 'L'
    # errorname = 'socclusion'daa
    turename2 = 'l'
    # turename2 = 'socclusion'
    # find_errofile(errorname)dd
    # rewrite_xml2(errorname, turename2, start_id, end_id)
    rewrite_xml(errorname, turename2)
    # find_errofile(cwd,errorname)











