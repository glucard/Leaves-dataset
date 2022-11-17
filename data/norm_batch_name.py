#!/bin/python3

import os
directory = os.path.realpath(os.path.dirname(__file__))

temp_dir = input(f"Directory to norm (Default: {directory}): ")
directory = directory if temp_dir == '' else temp_dir
if not os.path.isdir(directory):
    print(f"{directory} is not a directory\n Aborting...")
    exit(-1)

print(f"Directory to norm: {directory}")
list_dir = []
for d in os.listdir(directory):
    if os.path.isdir(d):
        list_dir.append(d)

print("Dir list: " + str(list_dir))

c = input("All files are going to be renamed. Continue? (y/n): ")
if c != 'y':
    print("Aborting...")
    exit()

for heap_name in list_dir:
    heap_path = directory+'\\'+heap_name

    if not os.path.isdir(heap_path):
        continue
    
    
    print(heap_path)
    # using temporary name first to not overwrite file
    for i, file_name in enumerate(os.listdir(heap_path)):
        extension = os.path.splitext(file_name)[1]
        old_name = heap_path+'\\'+file_name
        new_name = heap_path+'\\'+f"TEMP_FILE_NAME_{heap_name}.{i}{extension}"
        os.rename(old_name, new_name)
    
    # renaming
    for i, file_name in enumerate(os.listdir(heap_path)):
        old_name = heap_path+'\\'+file_name
        new_name = heap_path+'\\'+f"{heap_name}.{i}{extension}"
        os.rename(old_name, new_name)