from os import listdir
from os.path import isfile, join

# Add css section for all headers img

def get_all_files(mypath: str) -> list:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def get_header(filename):
    headers = ['access', 'acquisition', 'assessing_skills', 'books', 'disaster', 'dust', 'electronic', 'handling', 'health', 'humidity', 'leather', 'light', 'management', 'metal', 'networking', 'outdoor', 'paper', 'photographs', 'planning', 'policy', 'storage', 'surveys', 'transportation', 'volunteer', 'wood']
    for header in headers:
        if header in filename.lower():
            return header
    print(f"Heh? {filename}")

mypath = "D:\\Student@Work\\reCollection\\previous\\"
all_files = get_all_files(mypath)
print(all_files)

for file in all_files:
    if "clean" in file:
        header = get_header(file)
        if header != None:
            print(file)
            cur_file = ""
            with open(file, "r", encoding='utf-8') as fp:
                cur_file = fp.read()
            two_pieces = cur_file.split('<div class="before-main-wrapper"><div class="header-wrapper"><div class="hero-titles">')
            if len(two_pieces) > 1:
                cur_file = two_pieces[0] + '<div class="before-main-wrapper"><div class="header-wrapper header-panel" id="'+ header + '"><div class="hero-titles">' + two_pieces[1]
                print(cur_file)

                with open(file, "w", encoding='utf-8') as fp:
                    fp.write(cur_file)
                print(header)

