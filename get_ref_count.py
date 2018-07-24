#!/usr/bin/python
#coding=utf-8
import os,shutil

from path import *
SKIN = "E:\\resource\\gameSkins"
INGORE_FILES = ["effect", "battle", "sheet", "item", "building"];
def get_file_ref(icon_name):
    flag = True;
    for root, dirs, files in os.walk(SKIN):
        for f in files:
            file_name = os.path.join(root,f);
            skins = open(file_name,"r");
            lines = skins.read();
            if lines.find(icon_name) != -1:
                flag = False;
                break;
    if flag:
        print(icon_name + ' not used in the skin files');

def is_ingore_file(path):
    for f in INGORE_FILES:
        if path.find(f) >= 0:
            return True;
    return False;

def main():
    for root, dirs, files in os.walk(ASSET_FILE):

        for f in files:
            if (f.endswith('.jpg') or f.endswith('.png')) and not is_ingore_file(root):
                icon_name= f.replace('.', '_');
                get_file_ref(icon_name);
    pass


if __name__ == '__main__':
    main()
