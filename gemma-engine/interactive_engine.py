import whisper
import torch
import requests
from TTS.api import TTS

class InteractiveDialogueEngine:
    def __init__(self, device_id, backend_url):
        self.device_id = device_id
        self.backend_url = backend_url
        
        # 1. STT 모델 (Whisper: 사투리나 작은 목소리 인식에 강함)
        print("🎙️ STT 엔진 로딩 중...")
        self.stt_model = whisper.load_model("base")
        
        # 2. TTS 엔진 (자녀 목소리 복제)
        print("🔊 TTS 엔진 로딩 중...")
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda" if torch.cuda.is_available() else "cpu")
        
        # 대화 문맥 유지용 메모리
        self.conversation_history = []

    def listen_and_process(self, audio_path, child_voice_sample):
        """어르신의 음성 파일을 처리하여 자녀의 목소리 응답을 생성"""
        
        # [Step 1] 어르신 말씀 텍스트화 (STT)
        print("👂 듣는 중...")
        result = self.stt_model.transcribe(audio_path, language="ko")
        elderly_text = result["text"]
        print(f"👴 어르신: {elderly_text}")

        # [Step 2] Gemma 4를 통한 대화 생성 (LLM)
        # 백엔드에 현재 문맥과 어르신의 말을 보내 자녀 페르소나의 답변을 받아옴
        response = requests.post(
            f"{self.backend_url}/chat/generate",
            json={
                "device_id": self.device_id,
                "user_input": elderly_text,
                "history": self.conversation_history
            }
        )
        
        ai_response_text = response.json().get("reply")
        thought_process = response.json().get("thought") # Gemma 4의 Thinking Mode
        
        print(f"🧠 AI 사고과정: {thought_process}")
        print(f"👶 AI 자녀: {ai_response_text}")

        # 문맥 업데이트
        self.conversation_history.append({"role": "user", "content": elderly_text})
        self.conversation_history.append({"role": "assistant", "content": ai_response_text})

        # [Step 3] 자녀 목소리로 합성 (TTS)
        output_path = f"response_{self.device_id}.wav"
        self.tts.tts_to_file(
            text=ai_response_text,
            speaker_wav=child_voice_sample,
            language="ko",
            file_path=output_path
        )
        
        return output_path, ai_response_text