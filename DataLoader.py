import numpy as np
import os
import xml.etree.ElementTree as ET
from detectron2.structures import BoxMode

class DataLoader:
    def __init__(self, dir) -> None:
        self.dir = dir
        self.tree = ET.parse(dir)
        self.root = self.tree.getroot()
        self.label = ['right_eyelid', 'left_eyelid', 'right_iris', 'left_iris', 'right_center', 'left_center']

    def setDir(self, Dir):
        self.dir = Dir
        self.tree = ET.parse(self.dir)
        self.root = self.tree.getroot()

    def travelXML(self, img_dir, comp):
        dataset_dicts = []

        for child in self.root:
            record = {}
            
            if child.get("name") is not None:
                filename = os.path.join(img_dir, child.get("name"))
                if child.get("name") not in comp:
                    continue
                height = int(child.get("height"))
                width = int(child.get("width"))
                img_id = int(child.get("id"))
                
                record["file_name"] = filename
                record["height"] = height
                record["width"] = width
                record["image_id"] = img_id
                record["annotations"] = []
                
                for data in child:
                    if data.tag in ["polygon", "point"]:
                        anno = {}
                        
                        if data.tag == "polygon":
                            px = []
                            py = []
                            seg = data.get("points").replace(";", " ").replace(",", " ").split(" ")
                            
                            for i in range(len(seg)):
                                px.append(float(seg[i])) if i%2 == 0 else py.append(float(seg[i]))

                            anno["bbox"] = [np.min(px), np.min(py), np.max(px), np.max(py)]
                            anno["bbox_mode"] = BoxMode.XYXY_ABS
                            anno["category_id"] = self.label.index(data.get("label"))
                            anno["segmentation"] = [list(map(float, seg))]
                            record["annotations"].append(anno)

                dataset_dicts.append(record)
                
        return dataset_dicts
    
    def CustomData(self, img_dir, xml_dir, comp):
        self.setDir(xml_dir)
        return self.travelXML(img_dir, comp)
