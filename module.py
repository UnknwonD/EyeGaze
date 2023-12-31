import os
import json
import shutil

# Find Items from Dir
# Return : List of Item's Location if Flag True or return file name
def findDir(Dir, flag=True):
    file_list = os.listdir(Dir)
    if flag:
        item_dir = []
        for item in file_list:
            if "." in item and ".jpg" not in item:
                continue
            item_dir.append(Dir+"/"+item)
        return item_dir
    else:
        if "." in file_list[0] and ".jpg" not in file_list[0]:
            file_list.remove(".DS_Store")
        return file_list
    
# 최초 한 번만 실행, 이미지를 모두 한 폴더로 옮겨주는 역할 수행
def moveData(file_list, from_dir, to_dir):
    src = from_dir
    dest = to_dir

    for file in file_list:
        shutil.move(src + "/" + file, dest + "/" + file)

def extractJson(dicts):
    with open('label.json', 'w') as f : 
	    json.dump(dicts, f, indent=4)
    


class tool4laod:
    def __init__(self, Dir):
        self.root = Dir
        self.limit = 100 # 폴더당 100개의 이미지를 불러옴
        self.moved = False

    def setDir(self, Dir):
        self.root = Dir
    
    # ROOT 내의 이미지 폴더 명을 불러와서 지금 위치에서 모든 이미지 폴더나 파일 이름을 불러옴
    # Flage False - 폴더 내부의 이미지 이름을 모두 불러옴
    def lookforF(self, flag=True):
        if flag:
            return findDir(self.root, 0)
        else:
            imgs = []
            folders = findDir(self.root, 1)
            for folder in folders:
                if "." in folder and ".jpg" not in folder:
                    continue
                # imgs.append(findDir(self.root + "/" + folder))
                imgs.append(folder)
            return imgs

