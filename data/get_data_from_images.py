#!/bin/python3

from os import scandir
from os import listdir
from os import path
import fnmatch
import json

def list_directories(path):
    dir_list = []
    for entry in scandir(path):
        if entry.is_dir() and not entry.is_symlink():
            dir_list.append(entry.path)
            dir_list.extend(list_directories(entry.path))
    return dir_list

def count_images_jpg():
    dict = {}
    for dir in list_directories("."):        
        count = len(fnmatch.filter(listdir(dir), '*.jpg'))
        dict[str(path.basename(dir))] = count
    
    # Serializing json  
    json_object = json.dumps(dict, indent = 4) 
    print(json_object)

count_images_jpg()
 