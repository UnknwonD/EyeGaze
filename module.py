import os
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

def ConbineData(person, dists, xml_dir, img_dir):
    # 이렇게 하니까, 이미지 고유 id의 희소성이 사라짐..
    manager = tool4laod("root")
    tmp_xml = []
    tmp_img = []
    for p in person:
        for dist in dists:
            manager.setDir(f"New_Sample/원천데이터/TS_G1_1/{p}/{dist}/RGB/")
            tmp_img.append(manager.lookforF(0)) # 이미지의 경로를 모두 불러옴
            tmp_xml.append(f"New_Sample/라벨링데이터/TL/U/{p}/{dist}/NIA_EYE_U1_{p}_{dist}_RGB.xml")

    xml_dir = tmp_xml
    img_dir = tmp_img
    


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

