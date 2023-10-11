from os import listdir
from os.path import isfile, join

# Add css section for all headers img pre-downloaded from Wayback

def get_all_files(mypath: str) -> list:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

cur_css = ""
with open("headers.css", "r") as fp:
    cur_css = fp.read() + "\n"

mypath = "D:\\Student@Work\\reCollection\\previous\\static\\images\\headers\\"

all_files = get_all_files(mypath)
print(list(map(lambda f: f.replace(".jpg", ""), all_files)))

for file in all_files:
    css_name = file.replace(".jpg", "")
    cur_css += '''#'''+ css_name +'''{
    background-image: url("../images/headers/'''+ css_name +'''.jpg");
}

'''

with open("headers.css", "w") as fp:
    fp.write(cur_css)

