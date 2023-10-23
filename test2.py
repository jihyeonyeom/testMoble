from flask import Flask, request, jsonify
from datetime import datetime
from ultralytics import YOLO
import cv2
import math

local_image_dir = 'test'  # 로컬 저장 디렉토리를 원하는 경로로 수정

# PCB 불량 검출
def object_detect(image_path):
    model = YOLO("best.pt")
    
    classNames = [
    "missing_hole",
    "mouse_bite",
    "open_circuit",
    "short",
    ]
    image_src = f'{local_image_dir}/{image_path}'
    src = cv2.imread(image_src)
    results = model(src)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            print(currentClass)
            if conf > 0.5:
                if (
                    currentClass == "missing_hole"
                    or currentClass == "mouse_bite"
                    or currentClass == "open_circuit"
                    or currentClass == "short"
                ):
                    return "detect"
    return "None"

temp = object_detect("1.jpg")
print(temp)