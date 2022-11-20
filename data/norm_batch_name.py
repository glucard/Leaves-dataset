#!/bin/python3

import os, re

def getExtension(filename):
    return os.path.splitext(filename)[1] 

def atoi(text):
    return int(text) if text.isdigit() else text

def naturalKeys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def renameDir(dirlist, path, name, preffix=""):
    for i, file_name in enumerate(dirlist):
        extension = getExtension(file_name)
        old_name = os.path.join(path + os.sep, file_name)
        new_name = os.path.join(path + os.sep, f"{preffix}{name}.{i}{extension}")
        os.rename(old_name, new_name)

directory = os.path.realpath(os.path.dirname(__file__))

temp_dir = input(f"Directory to norm (Default: {directory}): ")
directory = directory if temp_dir == '' else temp_dir
if not os.path.isdir(directory):
    print(f"{directory} is not a directory\n Aborting...")
    exit(-1)

print(f"Directory to norm: {directory}")
list_dir = []
for d in os.listdir(directory):
    if os.path.isdir(directory + os.sep + d):
        list_dir.append(d)

print("Dir list: " + str(list_dir))

c = input("All files are going to be renamed. Continue? (y/n): ")
if c != 'y':
    print("Aborting...")
    exit()

for heap_name in list_dir:

    heap_path = os.path.join(directory + os.sep, heap_name)

    if not os.path.isdir(heap_path):
        continue

    print(heap_path+"...", end="")
    images_name = os.listdir(heap_path)
    images_name.sort(key=naturalKeys)
    images_name.sort(key=lambda name: re.sub("\d", "", name) != f"{heap_name}.{getExtension(name)}")

    # using temporary name first to not overwrite file
    renameDir(images_name, heap_path, heap_name, preffix="TEMP_FILE_NAME_")
    
    # renaming
    images_name = os.listdir(heap_path)
    images_name.sort(key=naturalKeys)
    renameDir(images_name, heap_path, heap_name)
    print("Done.")
