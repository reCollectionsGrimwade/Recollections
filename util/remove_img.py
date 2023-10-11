import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import shutil

from typing import List

# Used to remove all broken images from all files

def get_all_files(mypath: str) -> list:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def move_file(src_dir: str, dest_dir: str, filename: str):
    shutil.move(join(src_dir, filename), join(dest_dir, filename))


def check_img_exist(path: str):
    file = Path(path)
    return file.exists()

def get_source(img_str_arr: List[str]):
    for i in range(len(img_str_arr)):
        string = img_str_arr[i]
        if "src" in string:
            # Get the url part
            # Some crazy guy put spaces in folder name
            # So, continue searching until next attribute is encountered
            start = string.split("=")[1].replace('"', '')
            for j in range(i+1, len(img_str_arr)):
                if "=" in img_str_arr[j]:
                    break
                start += " " + img_str_arr[j].replace('"', '')
            return start
    return

def remove_img(mypath: str):
    all_files = get_all_files(mypath)

    for file in all_files:
        print(file)
        if "html" not in file:
            continue

        new_file = ""

        with open(file, "r", encoding='utf-8') as fp:
            removed = set()

            all_file = fp.read()
            parsed_tags = all_file.split("<")

            for i in range(len(parsed_tags)):
                cur_parsed = parsed_tags[i]
                if "img" in cur_parsed:
                    
                    parse_space = cur_parsed.split(" ")
                    print(parse_space)
                    source = get_source(parse_space)
                    print(source)

                    if not check_img_exist(source):
                        removed.add(i)
            
            new_tags = []
            for i in range(len(parsed_tags)):
                if i not in removed:
                    new_tags.append(parsed_tags[i])

            new_file = "<".join(new_tags)
        
        with open(file, "w",  encoding='utf-8') as fp:
            fp.write(new_file)

    return


mypath = "D:/Student@Work/reCollection/reBuild_v1/"
remove_img(mypath)