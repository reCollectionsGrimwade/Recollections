import os
from os import listdir
from os.path import isfile, join
import shutil

# Workflow: Download all Wayback pages along with its dependency into 1 folder
# (this original_wayback) -> Select shared dependency and put into 1 common
# folder (as most dependency are shared, except images) -> Run this file
# to remove all the wayback injection and cryptic, unnecessary part from the
# CMS + parse the folders and remove everything except image, then move
# everything to a new, cleaned folder for deployment 

# File IO
def get_all_files(mypath: str) -> list:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def move_file(src_dir: str, dest_dir: str, filename: str):
    shutil.move(join(src_dir, filename), join(dest_dir, filename))

def clean_links(filename: str):
    file = open(filename, "r", encoding='utf-8')
    all_file = file.read()
    file.close()

    split_space = all_file.split(" ")

    for i in range(len(split_space)):
        terms = split_space[i]
        split_quote = terms.split('"')
        for x in range(len(split_quote)):
            mini_term = split_quote[x]
            if ("web.archive" in mini_term):
                split_quote[x] = ""
        split_space[i] = '"'.join(split_quote)

    new_file = " ".join(split_space)

    with open(filename, "w", encoding='utf-8') as file:
        file.write(new_file)

# Clean Wayback
def clean_wayback(filename: str) -> str:
    title = filename.replace(" _ reCollections", "").replace(".html", "")
    temp_top = '''
<!DOCTYPE html>
<!-- saved from  -->
<html>
<link rel="stylesheet" href="./static/css/headers.css">



	
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>''' + title +  ''' | reCollections</title>

		
<link rel="stylesheet" id="dslc-main-css-css" href="./static/old_dependencies/main.min.css" type="text/css" media="all">
<link rel="stylesheet" id="dslc-modules-css-css" href="./static/old_dependencies/modules.min.css" type="text/css" media="all">
<link rel="stylesheet" id="shoestrap_css-css" href="./static/old_dependencies/ss-style.css" type="text/css" media="all">
<style id="shoestrap_css-inline-css" type="text/css">
.dslc-modules-section-wrapper, .dslca-add-modules-section {padding-left:15px; padding-right:15px}
.content-info {background:#282a2b;padding-top:90px;padding-bottom:15px;margin-top:20px;}#footer-copyright { margin-top:75px;  }.content a:hover { color:#e3634d }.btn:hover { background-color:#e3634d!important; border-color:#e3634d!important }
body .before-main-wrapper .header-wrapper a, body .before-main-wrapper .header-wrapper h1, body .before-main-wrapper .header-wrapper h2, body .before-main-wrapper .header-wrapper h3, body .before-main-wrapper .header-wrapper h4, body .before-main-wrapper .header-wrapper h5, body .before-main-wrapper .header-wrapper h6  { color: #ffffff; }body .before-main-wrapper .header-wrapper{ color: #ffffff;padding-top:100px;padding-bottom:100px;}
</style>

<script type="text/javascript" src="./static/old_dependencies/jquery.js.download"></script>
<script type="text/javascript" src="./static/old_dependencies/mediaelement-and-player.min.js.download"></script>

<script type="text/javascript" src="./static/old_dependencies/main.min.js.download"></script>
<script type="text/javascript" src="./static/old_dependencies/modernizr-2.7.0.min.js.download"></script>
<script type="text/javascript" src="./static/old_dependencies/main.js.download"></script>

		
	<body>
    \n
'''

    temp_bottom = '''
	</body>
	</html>
'''
    first_sign = '''<div class="before-main-wrapper"><div class="header-wrapper"><div class="hero-titles">'''
    second_sign = '''</div><!-- .dslc-module -->'''


    all_file = ""
    with open(filename, "r", encoding='utf-8') as fp:
        all_file = fp.read()
        remove_header = all_file.split(first_sign)
        all_file = temp_top + first_sign + remove_header[1]
        remove_bottom = all_file.split(second_sign)
        all_file = remove_bottom[0] + second_sign + temp_bottom

    new_name = "clean" + filename.replace(" _ reCollections", "")
    new_name = new_name.replace(" ", "")
    with open(new_name, "w", encoding='utf-8') as fp: 
        fp.write(all_file)
    
    clean_links(new_name)
    return new_name

def clean_and_move_single(mypath: str, topath: str, filename: str):
    new_name = clean_wayback(filename)
    move_file(mypath, topath, new_name)

def clean_and_move(mypath: str, topath: str):
    # Clean and move all files in original_wayback
    all_files = get_all_files(mypath)
    print(all_files)

    for file in all_files:
        if ".py" in file:
            continue
        clean_and_move_single(mypath, topath, file)



# Deal with folder (Cleaning all dependencies except images)
def is_img_file(filename:str) -> bool:
    all_img_ext = [".png", ".jpg", ".jpeg"]
    for img_ext in all_img_ext:
        if img_ext in filename.lower():
            return True
    return False

def folder_parser_single(cur_path: str, folder: str):
    folder_path = join(cur_path, folder) + "\\"
    print(folder_path)
    all_files = get_all_files(folder_path)

    for file in all_files:
        if not is_img_file(file):
            print(file)
            os.remove(join(folder_path, file))

def folder_parse(cur_path: str):
    # Remove everything except images
    all_folders = [f for f in listdir(cur_path) if not isfile(join(cur_path, f))]
    for folder in all_folders:
        folder_parser_single(cur_path, folder)



#----------------MAIN-----------------------------------

# Path where all the files located
mypath = "D:\\Student@Work\\reCollection\\reBuild_v1\\original_wayback\\"
# Clean folder to move files to for deployment
topath = "D:\\Student@Work\\reCollection\\reBuild_v1\\"

# folder_parse(mypath)

clean_and_move_single(mypath, topath, "Paintings _ reCollections.html")
folder_parser_single(mypath, "Paintings _ reCollections_files")