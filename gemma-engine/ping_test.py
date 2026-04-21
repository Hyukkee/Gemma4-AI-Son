import requests

# 백엔드 서버 주소 (모바일 앱 테스트 시 본인 PC의 IP로 변경했다면 똑같이 맞춰주세요)
url = "http://10.95.111.6:8000/report"

# 백엔드로 보낼 가짜 응급 데이터
payload = {
    "device_id": "elderly_home_01",
    "mode": "safety",
    "thought": "<|think|> 주변에 약병이 흩어져 있고 쓰러져 계심. 위험함.",
    "output": "어르신이 거실에 쓰러져 계십니다. 주변에 수면제 통이 발견되었습니다.",
    "is_emergency": True
}

# 발사!
try:
    response = requests.post(url, json=payload)
    print(f"✅ 전송 성공! 서버 응답: {response.json()}")
except Exception as e:
    print(f"❌ 전송 실패: {e}")