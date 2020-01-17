import os

def ListFilesToTxt(dir, file, wildcard, recursion):
    exts = wildcard.split(" ")
    for root, subdirs, files in os.walk(dir):
        n = 0
        for name in files:
            n+=1
            for ext in exts:
                if (name.endswith(ext)):
                    # file.write(str(n) + ',' + dir + name[:-4]+ '.jpg' + '\n')
                    file.write(str(n) + '\n')
                    break
        if (not recursion):
            break

def Test():
    dir = "/home/zs/python_scripts/test_data/3x2mnhapba6hcb6/"
    outfile = "/home/zs/python_scripts/test_data/3x2mnhapba6hcb6/list.txt"
    wildcard = ".jpg"

    file = open(outfile, "w")
    if not file:
        print("cannot open the file %s for writing" % outfile)
    ListFilesToTxt(dir, file, wildcard, 0)
    file.close()

Test()
