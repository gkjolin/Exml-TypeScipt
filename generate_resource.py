#!/usr/bin/python
#coding=utf-8
import os,shutil
import xml.dom.minidom
import  json;
from path import *

global resource
resource = open("resource.json", 'w')

# templete = "'{\n    "name": "{0}",\n    "type": "image",\n    "url": "{1}"\n}'"
config = open('resource_templete.txt')
group = open('group_templete.txt')
final = open('final_templete.txt')
sheet = open('sheet_templete.txt')

resourcetemplete = config.read()
grouptemplete = group.read()
finaltemplete = final.read()
sheettemplete = sheet.read();

def gen_group(dir, root):
    path = root+'/'+dir
    files = os.listdir(path)
    keys = ""
    
    for file in files:
        if not os.path.isdir(path+'/'+file):
            name = file.replace('.', '_')
            keys = keys +name + ','
    
    temp = grouptemplete
    keys = keys[0:len(keys)-1]
    
    if keys == '':
        return ''

    temp = temp.replace('__keys__', keys).replace('__name__', dir)
    resource.writelines(temp)
    resource.flush()
    return temp


def get_subkeys(fileName):
    json_file= open(fileName)
    rd = json_file.read();
    json_object = json.loads(rd)
    keys = '';
    for key in json_object['frames']:
        keys += key + ','
        print(key)

    return keys

def gen_resources(dir, root):
    path = root+'/'+dir
    path = path.replace('\\', '/')
    files = os.listdir(path)
    arr = path.partition('assets')
    url_prefix = arr[1]+arr[2] + '/'
    lines = ''
    file_type=''
    
    for file in files:
        if not os.path.isdir(path+'/'+file):
            url = url_prefix + file
            if file.find('.png') > -1 or file.find('.jpg') > -1:
                file_type ='image'
                pass
            elif file.find('.fnt')> -1:
                file_type = 'font'
                pass
            elif file.find('.mp3')> -1:
                file_type = 'sound'
                pass
            elif file.find('.txt')> -1:
                file_type = 'text'
                pass
            else:
                if dir == "sheet":
                    file_type='sheet'
                else:
                    file_type='json'
                    pass
                pass

            name = file.replace('.', '_')

            if(file_type == 'sheet'):
                temp = sheettemplete
                file_path = os.path.join(path, file)
                subkeys = get_subkeys(file_path)
                temp = temp.replace('__name', name).replace('__url', url).replace('__image', file_type).replace('__subkeys', subkeys);
            else:
                temp = resourcetemplete
                temp = temp.replace('__name', name).replace('__url', url).replace('__image', file_type)

            lines = lines + temp

    return lines

def main():
    _group_ = ''
    for root, dirs, files in os.walk(ASSET_FILE):
        for dir in dirs:
            out = gen_group(dir, root)
            if(len(out) > 0):
                _group_ = _group_ + out
        pass
    pass
    _group_ = _group_[0:len(_group_)-2]
    _resource_ = ''
    for root, dirs, files in os.walk(ASSET_FILE):
        for dir in dirs:
           _resource_= _resource_ + gen_resources(dir, root)
        pass
    pass
    _resource_ = _resource_[0:len(_resource_)-2]
    temp = finaltemplete
    temp = temp.replace('__groups__', _group_).replace('__resources__',_resource_)
    resource = open("resource.json", 'w')
    resource.writelines(temp)
    resource.flush()
    resource.close()
    shutil.copyfile("resource.json",TARGET)

if __name__ == '__main__':
    main()