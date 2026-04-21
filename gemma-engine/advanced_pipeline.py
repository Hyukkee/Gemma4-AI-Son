import cv2
from PIL import Image
import torch
import requests
from ultralytics import YOLO

# 1. YOLO 모델 로드 (가장 가벼운 Nano 버전)
print("Loading YOLOv8n...")
yolo_model = YOLO('yolov8n.pt') 

# 2. IP 카메라 연결 (테스트를 위해 0번은 노트북 기본 웹캠)
# 실제 현장 적용 시: CAMERA_URL = "rtsp://아이디:비밀번호@192.168.0.50/stream1"
CAMERA_URL = "test_video.mp4"
cap = cv2.VideoCapture(CAMERA_URL)

# 백엔드 주소 (본인 환경에 맞게 수정)
BACKEND_URL = "http://10.95.111.6:8000/report"

# 임시로 사용할 Gemma 4 모의 함수 (실제 젬마 모델 로드는 이전 코드와 병합하면 됩니다)
def analyze_with_gemma(pil_image):
    print("🧠 [Gemma 4] 의심 상황 심층 분석 중...")
    # 여기에 실제 Gemma 4 추론 코드가 들어갑니다.
    # 현재는 데모용 Mock 데이터를 반환합니다.
    return {
        "device_id": "elderly_home_01",
        "mode": "safety",
        "thought": "<|think|> 어르신이 바닥에 누워있고 움직임이 없음. 낙상으로 판단됨.",
        "output": "어르신이 거실 바닥에 쓰러져 계십니다. 신속한 확인이 필요합니다.",
        "is_emergency": True
    }

print("🎥 카메라 감시 시작...")
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    
    # 1초에 3번 정도만 YOLO로 검사 (프레임 스킵 최적화)
    if frame_count % 10 == 0:
        # 1차 검출: YOLO
        results = yolo_model(frame, verbose=False)
        
        person_detected = False
        fall_suspected = False

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # 클래스 0은 '사람(person)'
                if int(box.cls[0]) == 0:
                    person_detected = True
                    # Bounding Box의 가로(w), 세로(h) 추출
                    x1, y1, x2, y2 = box.xyxy[0]
                    w = x2 - x1
                    h = y2 - y1
                    
                    # 💡 간단한 낙상 의심 로직: 세로보다 가로가 1.5배 길면 누워있다고 판단
                    if w > h * 1.5:
                        fall_suspected = True
                        # 화면에 빨간 박스 그리기
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

        # 2차 추론: YOLO가 낙상을 의심할 때만 Gemma 4 호출
        if person_detected and fall_suspected:
            print("⚠️ [YOLO] 낙상 의심 객체 발견! Gemma 4로 데이터 이관.")
            
            # OpenCV 이미지(BGR)를 PIL 이미지(RGB)로 변환
            color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(color_converted)
            
            # Gemma 4 심층 추론 실행
            gemma_result = analyze_with_gemma(pil_img)
            
            # 백엔드로 전송
            if gemma_result["is_emergency"]:
                requests.post(BACKEND_URL, json=gemma_result)
                print("🚨 백엔드로 응급 알람 전송 완료!")
                
                # 경고 발생 시 잠시 대기 (알람 중복 발송 방지)
                cv2.waitKey(5000) 

    # 화면에 영상 띄워주기
    cv2.imshow('AI-Son Camera View', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()