from DataLoader import DataLoader
import module

xml = "New_Sample/라벨링데이터/TL/U/002/50/NIA_EYE_U1_002_50_RGB.xml"
xml_dir = ["New_Sample/라벨링데이터/TL/U/011/50/NIA_EYE_U1_011_50_RGB.xml"]
img_root = "New_Sample/원천데이터/TS_G1_1"
dists = ["30", "50"]

manager = module.tool4laod(img_root)
loader = DataLoader(xml)

img_folders = manager.lookforF(False)


for Dir in img_folders:
    for dist in dists:
        tmp = Dir + "/" + dist + "/RGB/"
        manager.setDir(tmp)
        # print(manager.lookforF(0)) # 이미지의 이름을 모두 불러옴

# img_folder = manager.lookforF(0)
json_dict = loader.CustomData(xml_dir)
print(json_dict[1]["images"])
