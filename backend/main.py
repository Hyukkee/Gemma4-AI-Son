from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import datetime
from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional
from fastapi import APIRouter
import datetime

app = FastAPI(title="Gemma AI-Son API")

#대화문맥 및 페르소나 관리
class ChatRequest(BaseModel):
    device_id: str
    user_input: str
    history: list

@app.post("/chat/generate")
async def generate_chat(req: ChatRequest):
    # Gemma 4에게 부여할 페르소나 시스템 프롬프트
    system_prompt = (
        "너는 혼자 계신 부모님을 챙기는 다정한 아들/딸이야. "
        "어르신의 말씀을 경청하고, 공감하며, 가끔은 옛날 추억(업로드된 사진 정보 등)을 언급해줘. "
        "짧고 명확한 문장을 사용하되, 말투는 항상 따뜻해야 해."
    )
    
    # 실제 환경에서는 여기서 Gemma 4 모델 API를 호출합니다.
    # 데모를 위한 예시 응답 구조:
    ai_reply = "그랬구나 아버지. 오늘 날씨가 좀 쌀쌀한데 옷은 따뜻하게 입으셨어요?"
    thought = "<|think|> 아버지가 외롭다고 말씀하시니 날씨를 핑계로 안부를 묻고 대화를 이어가야겠다."
    
    return {
        "reply": ai_reply,
        "thought": thought
    }

# 데이터 모델 정의
class InferenceResult(BaseModel):
    device_id: str
    mode: str  # "safety" (안전), "reminiscence" (회상)
    thought: str  # Gemma 4의 사고 과정 (Thinking Mode)
    output: str   # 최종 답변/판단
    is_emergency: bool = False

# 임시 DB (개발/테스트용)
db_logs = []

@app.get("/")
def read_root():
    return {"message": "Gemma 4 AI-Son Backend API is running"}

@app.post("/report")
async def create_report(result: InferenceResult):
    """엔진으로부터 추론 결과를 받아 저장합니다."""
    log_entry = {
        "id": len(db_logs) + 1,
        "timestamp": datetime.datetime.now().isoformat(),
        **result.dict()
    }
    db_logs.append(log_entry)
    
    # 응급 상황 시 로직 (향후 모바일 앱으로 푸시 연동)
    if result.is_emergency:
        print(f"!!! 🚨 EMERGENCY DETECTED in {result.device_id} !!!")
        
    return {"status": "success", "log_id": log_entry["id"]}

@app.get("/logs/{device_id}", response_model=List[dict])
async def get_logs(device_id: str):
    """특정 기기(어르신 댁)의 안부 로그를 가져옵니다."""
    return [log for log in db_logs if log["device_id"] == device_id][::-1]

# 1. 일정 모델 추가
class CareSchedule(BaseModel):
    id: int
    task_type: str  # "medication", "meal", "sleep", "hospital"
    task_name: str  # 예: "혈압약", "점심 식사"
    scheduled_time: str  # "HH:MM" 형식
    is_completed: bool = False

# 임시 DB에 일정 추가 (실제로는 앱에서 설정)
db_schedules = [
    CareSchedule(id=1, task_type="medication", task_name="혈압약", scheduled_time="09:00"),
    CareSchedule(id=2, task_type="meal", task_name="점심 식사", scheduled_time="12:30"),
]

@app.get("/schedules/{device_id}")
async def get_schedules(device_id: str):
    return db_schedules

@app.post("/schedules/complete/{task_id}")
async def complete_task(task_id: int):
    for s in db_schedules:
        if s.id == task_id:
            s.is_completed = True
            # 여기서 자녀에게 푸시 알림을 보내는 로직이 들어감
            print(f"✅ 알림: 어르신이 {s.task_name} 과제를 완료하셨습니다!")
            return {"status": "success", "task": s.task_name}
    return {"status": "error", "message": "Task not found"}

# 리포트 생성을 위한 임시 데이터 구조
weekly_mock_data = {
    "device_id": "elderly_home_01",
    "period": "2026-04-13 ~ 2026-04-19",
    "logs": [
        {"type": "medication", "success_rate": "85%", "missed": ["수요일 점심 혈압약"]},
        {"type": "activity", "main_location": "거실 (70%)", "fall_suspected": 0},
        {"type": "conversation", "keywords": ["오키나와", "가족 여행", "허리 통증", "된장찌개"]}
    ]
}

@app.get("/report/weekly/{device_id}")
async def generate_weekly_report(device_id: str):
    """
    일주일간의 로우 데이터를 Gemma 4 프롬프트로 전송하여
    보호자가 읽기 쉬운 리포트 형태로 요약 및 변환합니다.
    """
    # 1. DB에서 해당 기기의 일주일 치 활동/대화/알림 로그를 가져옴 (여기서는 mock data 사용)
    raw_data = weekly_mock_data
    
    # 2. Gemma 4에게 보낼 프롬프트 작성
    gemma_prompt = f"""
    당신은 독거노인을 케어하는 전문 AI 분석가입니다. 
    다음 일주일 치 데이터를 분석하여 자녀(보호자)가 읽을 주간 요약 리포트를 작성해주세요.
    
    데이터: {raw_data}
    
    요구사항:
    1. 감정 상태 요약 (대화 키워드 기반)
    2. 신체 및 활동 상태 (복약률 및 활동 기반)
    3. 이번 주말 자녀를 위한 행동 가이드 (추천 액션)
    """
    
    # 3. Gemma 4 추론 실행 (실제 엔진 호출 부분)
    # response = requests.post("gemma_engine_url/analyze", json={"prompt": gemma_prompt})
    
    # 4. Gemma 4가 생성한 결과물 (Mock up)
    ai_summary = {
        "emotion": "아버님은 이번 주 '오키나와 가족 여행'을 자주 언급하시며 전반적으로 긍정적인 감정 상태를 보이셨습니다.",
        "physical": "복약 순응도는 85%로 매우 우수하나, 수요일에 한 차례 건너뛰셨습니다. 또한 '허리 통증'이라는 키워드가 포착되었습니다.",
        "recommendation": "이번 주말 안부 전화를 드릴 때, 오키나와 여행 사진을 함께 보며 이야기를 나누고 허리 통증이 어떠신지 꼭 여쭤보시길 권장합니다."
    }
    
    return {
        "status": "success",
        "period": raw_data["period"],
        "summary": ai_summary,
        "metrics": {
            "medication_rate": 85,
            "activity_level": "보통",
            "conversation_count": 12
        }
    }