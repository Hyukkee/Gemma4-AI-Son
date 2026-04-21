import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import os
import shutil
from pathlib import Path
from fastapi import UploadFile, File

# 저장 폴더 설정
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "photos").mkdir(exist_ok=True)
(UPLOAD_DIR / "voice_samples").mkdir(exist_ok=True)

@app.post("/upload/photo")
async def upload_photo(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / "photos" / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "success", "file_path": str(file_path)}

@app.post("/upload/voice-sample")
async def upload_voice(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / "voice_samples" / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "success", "message": "자녀 음성 샘플 등록 완료"}

class GemmaSonEngine:
    def __init__(self, model_id="google/gemma-4-E2B-it"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = model_id
        
        # 4-bit 양자화로 메모리 최적화 (로컬 구동 핵심)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.bfloat16,
            load_in_4bit=True
        )

    def infer(self, image_path, mode="safety"):
        """
        image_path: 분석할 이미지 경로
        mode: 'safety' (위험감지) 또는 'reminiscence' (회상요법)
        """
        image = Image.open(image_path).convert("RGB")
        
        # 전문 사회복지사 관점의 시스템 프롬프트 주입
        if mode == "safety":
            prompt = (
                "<|think|> 당신은 독거노인의 안전을 책임지는 AI 자녀입니다. "
                "사진 속 어르신의 자세와 주변 환경을 분석하세요. "
                "낙상, 약물 오남용, 화재 위험 등을 체크하고 응급 상황 여부를 판단하세요. "
                "위험하다면 'EMERGENCY' 단어를 포함하여 보고하세요."
            )
        else:
            prompt = (
                "<|think|> 당신은 다정한 AI 자녀입니다. "
                "어르신이 보여주신 옛날 사진의 내용을 분석하여, "
                "어르신의 장기 기억을 자극하고 기분을 좋게 만들 수 있는 다정한 질문을 하세요."
            )

        messages = [
            {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": prompt}]}
        ]
        
        inputs = self.processor.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=True, return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            output = self.model.generate(**inputs, max_new_tokens=512)
        
        return self.processor.decode(output[0], skip_special_tokens=True)

# 테스트 실행부
if __name__ == "__main__":
    engine = GemmaSonEngine()
    # 결과 = engine.infer("test_image.jpg", mode="safety")
    # print(결과)