import numpy as np
import xml.etree.ElementTree as ET
# from detectron2.structures import BoxMode

class DataLoader:
    def __init__(self, dir) -> None:
        self.dir = dir
        self.tree = ET.parse(dir)
        self.root = self.tree.getroot()
        self.label = ['left_eyelid', 'right_center', 'left_center', 'right_iris', 'left_iris', 'right_eyelid']
    
    # return list[dict] that contains every information in XML
    # flag : if True, It will travel XML Tree finding annotations else image meta data as default
    def travelXML(self, flag=0):
        dict_list = []
        anno_id = 0

        for child in self.root:
            if not flag:
                tmp_dict = {}
                tmp_dict["file_name"] = child.get("name")
                # img -> 1280 * 72o
                tmp_dict["height"] = child.get("height")
                tmp_dict["width"] = child.get("width")
                tmp_dict["id"] = child.get("id")

                dict_list.append(tmp_dict)
            
            else:
            # img 내부 정보를 불러옴
                for data in child:
                    tmp_dict = {}
                    tmp_dict["id"] = anno_id
                    tmp_dict["image_id"] = child.get("id")
            
                    # 시선 중앙값 -> 이걸 어떻게 쓰지 
                    if data.tag == "points":
                        tmp = data.get("points").split(",")
                    #segmentation
                    if data.tag == "polygon":
                        seg = float(data.get("points").replace(";", " "))
                        px = []
                        py = []
                        for i in range(seg):
                            px.append(seg[i]) if i%2 == 0 else py.append(seg[i])

                        tmp_dict["bbox"] = [np.min(px), np.min(py), np.max(px), np.max(py)]
                        # tmp_dict["bbox_mode"] = BoxMode.XYXY_ABS | 얘는 Detectron 다운 받고 해야됨
                        tmp_dict["category_id"] = self.label.index(data.get("label"))
                        tmp_dict["segmentation"] = seg

                    anno_id += 1
                    dict_list.append(tmp_dict)
        return dict_list    
                
    def CustomData(self):
        data_dict = [{"info": {"description" : "project_Gaze"}}]
        data_dict.append({"images" : []})
        data_dict.append({"annotations" : []})

        tmp_dict = {}
        tmp_dict = self.travelXML(0)
        data_dict[1]["images"].append(tmp_dict) # 접근 방법

        tmp_dict = self.travelXML(1)
        data_dict[2]["annotations"].append(tmp_dict)

        return data_dict