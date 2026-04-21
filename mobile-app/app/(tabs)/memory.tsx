import { StyleSheet, Text, View, TouchableOpacity, Image } from 'react-native';

export default function MemoryScreen() {
  // 데모를 위한 하드코딩 데이터 (실제로는 백엔드 연동)
  const aiQuestion = "이 사진 속에 계신 분들은 누구인가요? 아주 즐거워 보이시네요. 이때 어떤 일이 있었는지 말씀해 주시겠어요?";

  return (
    <View style={styles.container}>
      <Text style={styles.title}>오늘의 추억 여행</Text>
      
      <View style={styles.imagePlaceholder}>
        <Text style={styles.imageText}>[옛날 가족 사진 영역]</Text>
      </View>

      <View style={styles.chatBubble}>
        <Text style={styles.aiName}>AI 자녀 (Gemma 4)</Text>
        <Text style={styles.aiMessage}>{aiQuestion}</Text>
      </View>

      <TouchableOpacity style={styles.micButton}>
        <Text style={styles.micButtonText}>🎙️ 대답하기</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, alignItems: 'center', backgroundColor: '#fff' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 20 },
  imagePlaceholder: { width: '100%', height: 250, backgroundColor: '#e0e0e0', justifyContent: 'center', alignItems: 'center', borderRadius: 15, marginBottom: 20 },
  imageText: { color: '#757575', fontSize: 16 },
  chatBubble: { width: '100%', backgroundColor: '#E8F5E9', padding: 20, borderRadius: 15, marginBottom: 30 },
  aiName: { fontSize: 14, fontWeight: 'bold', color: '#2E7D32', marginBottom: 10 },
  aiMessage: { fontSize: 18, lineHeight: 26, color: '#333' },
  micButton: { backgroundColor: '#4CAF50', paddingVertical: 15, paddingHorizontal: 40, borderRadius: 30 },
  micButtonText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
});

// 주요 로직: 마이크 녹음 -> 서버 전송 -> 응답 음성 재생
const startRecording = async () => {
  // 1. 녹음 시작 (expo-av 사용)
};

const stopAndSend = async () => {
  // 1. 녹음 중지 및 파일 추출
  // 2. 서버의 /chat/reminiscence (또는 대화 API)로 전송
  // 3. 서버에서 온 자녀 목소리 WAV 재생
  // 4. 화면에 대화 내역 업데이트
};