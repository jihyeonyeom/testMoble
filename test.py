from flask import Flask, request, jsonify
from datetime import datetime
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import math
import cvzone

app = Flask(__name__)

@app.route('/image_save', methods=['POST'])
def image_save():
    local_image_dir = '/home/ubuntu/yolo_test/Images'  # 로컬 저장 디렉토리를 원하는 경로로 수정
    
    try:
        current_time = datetime.now()
        image_file = f'{current_time.strftime("%Y-%m-%d_%H-%M-%S")}.jpg'  # 형식에 맞게 파일 이름 생성

        # POST 요청에서 이미지 데이터를 읽어옵니다.
        image_data = request.data
        image_array = np.frombuffer(image_data, dtype=np.uint8)
        
        # 이미지 데이터를 OpenCV 형식으로 변환
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # OpenCV 이미지를 PIL 이미지로 변환
        image_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image_path = f'{local_image_dir}/{image_file}'
        image_pil.save(image_path)
        
        result = object_detect(image_path)
        # 이미지에서 불량 검출 YOLO
        if result != "":
            response_data = {"message": "detect"}
            return jsonify(response_data)
        else:
            response_data = {"message": "None"}
            return jsonify(response_data)
    except Exception as e:
        response_data = {"message": "error", "error_message": str(e)}
        return jsonify(response_data)

# PCB 불량 검출
def object_detect(image_path):
    myColor = (0, 0, 255)
    text_area = ""
    model = YOLO("best.pt")
    
    classNames = [
    "missing_hole",
    "mouse_bite",
    "open_circuit",
    "short",
    ]
    src = cv2.imread(image_path)
    results = model(src)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            if conf > 0.5:
                if (
                    currentClass == "missing_hole"
                    or currentClass == "mouse_bite"
                    or currentClass == "open_circuit"
                    or currentClass == "short"
                ):
                    cvzone.putTextRect(
                        src,
                        f"{currentClass} {conf}",
                        (max(0, x1), max(35, y1 - 7)),
                        scale=1,
                        thickness=1,
                        colorB=myColor,
                        colorT=(255, 255, 255),
                        colorR=myColor,
                        offset=5,
                    )
                    cv2.rectangle(src, (x1, y1), (x2, y2), myColor, 3)
                    if text_area == "":
                        text_area = currentClass
                    else:
                        text_area = text_area + ", " + currentClass
    cv2.imwrite(image_path, src)
    return text_area
    
    
if __name__=="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="0.0.0.0", port="5000", debug=True)
