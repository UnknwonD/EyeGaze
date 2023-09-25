from DataLoader import DataLoader
import module

xml = "New_Sample/라벨링데이터/TL/U/002/50/NIA_EYE_U1_002_50_RGB.xml"
img_root = "New_Sample/원천데이터/TS_G1_1"

manager = module.tool4laod(img_root)
loader = DataLoader(xml)

person = manager.lookforF() # 이미지 상위폴더인 사람 번호가 들어옴
dists = ["30", "50"] # 사용할 데이터는 30, 50cm에서 촬영된 사진
xml_dir = [] #라벨이 들어있는 dir을 저장
img_dir = [] #이미지가 들어있는 dir을 저장

for p in person:
    for dist in dists:
        manager.setDir(f"New_Sample/원천데이터/TS_G1_1/{p}/{dist}/RGB/")
        img_dir.append(manager.lookforF(0)) # 이미지의 경로를 모두 불러옴
        xml_dir.append(f"New_Sample/라벨링데이터/TL/U/{p}/{dist}/NIA_EYE_U1_{p}_{dist}_RGB.xml")

img_folder = manager.lookforF(0)
json_dict = loader.CustomData(xml_dir)
print(json_dict[1]["images"])
