from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.config import get_cfg
from detectron2 import model_zoo
import os
import cv2

# 설정 불러오기
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")) # 학습에 사용한 설정 파일을 지정합니다.

# 학습된 가중치 불러오기
cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model/model_final.pth") # 학습이 끝난 후 생성된 .pth 파일의 경로를 지정합니다.
cfg.MODEL.DEVICE = "cpu"

# 테스트 설정
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # 예: Confidence threshold
cfg.MODEL.ROI_HEADS.NUM_CLASSES = 6  # 클래스 개수
cfg.DATASETS.TEST = ("dataset_011_50", )

predictor = DefaultPredictor(cfg)

# 테스트 이미지 불러오기
image = cv2.imread("path_to_your_test_image.jpg")

# 예측
outputs = predictor(image)

# 결과 시각화 (옵션)
v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TEST[0]), scale=1.2)
v = v.draw_instance_predictions(outputs["instances"].to("cpu"))
cv2.imshow("predictions", v.get_image()[:, :, ::-1])
