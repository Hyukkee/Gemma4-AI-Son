import cv2
import time
from datetime import datetime
from ultralytics import YOLO
import requests

# 자녀 목소리 합성 엔진 (우리가 만든 것)
# from voice_pipeline import VoiceCloningEngine 

class ActiveCareEngine:
    def __init__(self, device_id, backend_url):
        self.device_id = device_id
        self.backend_url = backend_url
        self.yolo = YOLO('yolov8n.pt')  # 물체 감지용
        # self.voice_engine = VoiceCloningEngine()
        self.is_waiting_for_action = False
        self.current_task = None

    def check_schedules(self):
        """백엔드에서 현재 시간의 일정을 가져옴"""
        now = datetime.now().strftime("%H:%M")
        response = requests.get(f"{self.backend_url}/schedules/{self.device_id}")
        if response.status_code == 200:
            for schedule in response.json():
                if schedule['scheduled_time'] == now and not schedule['is_completed']:
                    return schedule
        return None

    def run(self, camera_source=0):
        cap = cv2.VideoCapture(camera_source)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            # 1. 일정 체크
            task = self.check_schedules()
            if task and not self.is_waiting_for_action:
                self.current_task = task
                self.is_waiting_for_action = True
                print(f"📢 알림 발생: {task['task_name']} 시간입니다.")
                # 실제로는 tts_to_file 후 재생
                # self.voice_engine.generate_child_voice(f"아버지, {task['task_name']} 드실 시간이에요!", ...)

            # 2. 행동 인식 (YOLO)
            if self.is_waiting_for_action:
                results = self.yolo(frame, verbose=False)
                for r in results:
                    # 'bottle'(39)이나 'cup'(41)을 들고 입 근처로 가져가는지 확인
                    for box in r.boxes:
                        cls = int(box.cls[0])
                        if cls in [39, 41]: # 병이나 컵이 감지되면
                            print(f"✨ 확인: {self.current_task['task_name']} 수행 감지!")
                            
                            # 백엔드에 완료 보고
                            requests.post(f"{self.backend_url}/schedules/complete/{self.current_task['id']}")
                            
                            # 자녀 목소리로 칭찬 출력
                            # self.voice_engine.generate_child_voice("잘하셨어요 아버지! 역시 최고예요.", ...)
                            
                            self.is_waiting_for_action = False
                            self.current_task = None
                            time.sleep(10) # 알림 중복 방지

            cv2.imshow('Active Care Monitoring', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()

# engine = ActiveCareEngine("elderly_home_01", "http://127.0.0.1:8000")
# engine.run("test_video.mp4")