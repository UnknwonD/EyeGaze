from DataLoader import DataLoader
import module

xml_dir = "NIA_EYE_G1_001_50_RGB.xml"
img_root = "New_Sample/원천데이터/TS_G1_1"

manager = module.tool4laod(img_root)
loader = DataLoader(xml_dir)

img_folder = manager.lookforF(0)

print(loader.travelXML(1))
# json_dict = loader.CustomData()
# print(json_dict)
