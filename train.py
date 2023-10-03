from detectron2.data import DatasetCatalog, MetadataCatalog, build_detection_train_loader
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from DataLoader import DataLoader
import module

import os

xml = "New_Sample/label/TL/U/002/50/NIA_EYE_U1_002_50_RGB.xml"
img_root = "New_Sample/image/TS_G1_1"

manager = module.tool4laod(img_root)
loader = DataLoader(xml)
isModel = False
cnt = 0
person = manager.lookforF() # 이미지 상위폴더인 사람 번호가 들어옴
dists = ["50", "30"] # 사용할 데이터는 30, 50cm에서 촬영된 사진
classes = ['right_eyelid', 'left_eyelid',  'right_iris', 'left_iris', 'right_center', 'left_center']

# detectron2 학습 ( 각 사람마다 30cm와 50cm에서 촬영된 이미지에 대한 모델을 학습진행 )
for p in person:
    for dist in dists:
        print(f"Debug: {cnt}, New_Sample/image/TS_G1_1/{p}/{dist}/RGB/")
        cnt += 1
        
        # img_dir = manager.lookforF(0) # 이미지의 경로의 모든 이미지 파일 경로를 담은 리스트
        img_dir = f"New_Sample/image/TS_G1_1/{p}/{dist}/RGB/"

        manager.setDir(f"New_Sample/image/TS_G1_1/{p}/{dist}/RGB/")
        cp_img = manager.lookforF()

        img_dir = os.path.abspath(img_dir)
        

        xml_dir = f"New_Sample/label/TL/U/{p}/{dist}/NIA_EYE_U1_{p}_{dist}_RGB.xml"
        data_dict = loader.CustomData(img_dir, xml_dir, cp_img)
        module.extractJson(data_dict)
        # data_sample = loader.CustomData(img_dir, xml_dir)
        # print(data_sample[0])
        
        # Dataset 등록
        dataset_name = f"dataset_{p}_{dist}"
        DatasetCatalog.register(dataset_name, lambda img_dir=img_dir, xml_dir=xml_dir, comp = cp_img: loader.CustomData(img_dir, xml_dir, comp))
        # DatasetCatalog.register(dataset_name, loader.CustomData(img_dir, xml_dir))
        MetadataCatalog.get(dataset_name).set(thing_classes=classes) # 클래스 이름 설정
        
        #### 학습코드 ####
        cfg = get_cfg()
        # if isModel:
        cfg.MODEL.WEIGHTS = "/Users/idaeho/Desktop/Eye_Gaze/model/model_final.pth"
        cfg.MODEL.DEVICE = "cpu"
        cfg.OUTPUT_DIR = "/Users/idaeho/Desktop/Eye_Gaze/model" # 모델을 저장할 위치
        cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")) # 예시로 Faster R-CNN 사용
        cfg.DATASETS.TRAIN = (dataset_name,)
        cfg.DATASETS.TEST = () # Test set을 사용하지 않음
        cfg.DATALOADER.NUM_WORKERS = 0
        cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml") 
        cfg.SOLVER.IMS_PER_BATCH = 2
        cfg.SOLVER.BASE_LR = 0.0025 
        cfg.SOLVER.MAX_ITER = 20 # 학습 iteration
        cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 6  # 클래스 개수
        
        trainer = DefaultTrainer(cfg)
        trainer.resume_or_load(resume=False)
        trainer.train()

        trainer.checkpointer.save("model_final")
        isModel = True