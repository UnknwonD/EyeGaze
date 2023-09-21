import os
import cv2

# Find Items from Dir
# Return : List of Item's Location if Flag True or return file name
def findDir(Dir, flag=True):
    file_list = os.listdir(Dir)
    if flag:
        item_dir = []
        for item in file_list:
            if "." in item:
                continue
            item_dir.append(Dir+"/"+item)
        return item_dir
    else:
        return file_list

class tool4laod:
    def __init__(self, Dir):
        self.root = Dir
        self.dist = [30, 50]
        self.limit = 100 # 폴더당 100개의 이미지를 불러옴
        self.moved = False
    
    # ROOT 내의 이미지 폴더 명을 불러와서 모든 이미지 폴더의 이름을 불러옴
    # Flage False - 폴더 내부의 이미지 이름을 모두 불러옴
    def lookforF(self, flag=True):
        if flag:
            return findDir(self.root, 0)
        else:
            imgs = []
            folders = findDir(self.root, 0)
            for folder in folders:
                if "." in folder:
                    continue
                # imgs.append(findDir(self.root + "/" + folder))
                imgs.append(folder)
            return imgs

    # 최초 한 번만 실행, 이미지를 모두 한 폴더로 옮겨주는 역할 수행
    def __moveData(self):
        pass


