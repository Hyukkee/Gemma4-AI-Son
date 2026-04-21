import React, { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image, Alert, ActivityIndicator } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import * as DocumentPicker from 'expo-document-picker';

// 백엔드 IP 주소 (본인 PC의 IPv4로 수정 필수)
const API_URL = 'http://192.168.0.15:8000'; 

export default function GuardianUploadScreen() {
  const [photo, setPhoto] = useState<string | null>(null);
  const [voice, setVoice] = useState<any>(null);
  const [uploading, setUploading] = useState(false);

  // 1. 추억 사진 선택
  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      setPhoto(result.assets[0].uri);
    }
  };

  // 2. 자녀 목소리 샘플 선택 (오디오 파일)
  const pickVoice = async () => {
    let result = await DocumentPicker.getDocumentAsync({
      type: 'audio/*',
      copyToCacheDirectory: true,
    });

    if (!result.canceled) {
      setVoice(result.assets[0]);
    }
  };

  // 3. 서버로 전송 (FormData 활용)
  const handleUpload = async () => {
    if (!photo || !voice) {
      Alert.alert("알림", "사진과 목소리 샘플을 모두 선택해주세요.");
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      
      // 사진 추가
      formData.append('file', {
        uri: photo,
        name: 'memory_photo.jpg',
        type: 'image/jpeg',
      } as any);

      // 사진 업로드 요청
      await fetch(`${API_URL}/upload/photo`, {
        method: 'POST',
        body: formData,
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // 목소리 추가 및 업로드
      const voiceData = new FormData();
      voiceData.append('file', {
        uri: voice.uri,
        name: voice.name,
        type: voice.mimeType,
      } as any);

      await fetch(`${API_URL}/upload/voice-sample`, {
        method: 'POST',
        body: voiceData,
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      Alert.alert("성공", "부모님께 소중한 추억과 목소리를 전달했습니다!");
      setPhoto(null);
      setVoice(null);
    } catch (error) {
      console.error(error);
      Alert.alert("오류", "업로드 중 문제가 발생했습니다.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>부모님께 추억 선물하기</Text>
      
      {/* 사진 섹션 */}
      <TouchableOpacity style={styles.uploadBox} onPress={pickImage}>
        {photo ? (
          <Image source={{ uri: photo }} style={styles.previewImage} />
        ) : (
          <Text style={styles.uploadText}>📸 추억 사진 선택</Text>
        )}
      </TouchableOpacity>

      {/* 목소리 섹션 */}
      <TouchableOpacity style={[styles.uploadBox, styles.voiceBox]} onPress={pickVoice}>
        <Text style={styles.uploadText}>
          {voice ? `🎙️ 목소리 선택됨: ${voice.name}` : '🎙️ 내 목소리 샘플 선택'}
        </Text>
      </TouchableOpacity>

      <Text style={styles.desc}>
        등록된 목소리는 AI가 분석하여, 부모님께 자녀분의 목소리로 다정하게 말을 건네는 데 사용됩니다.
      </Text>

      {/* 전송 버튼 */}
      <TouchableOpacity 
        style={[styles.submitButton, uploading && styles.disabledButton]} 
        onPress={handleUpload}
        disabled={uploading}
      >
        {uploading ? <ActivityIndicator color="#fff" /> : <Text style={styles.submitText}>선물 보내기</Text>}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 30, backgroundColor: '#fff', justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', textAlign: 'center', marginBottom: 40, color: '#2E7D32' },
  uploadBox: {
    height: 200, backgroundColor: '#F5F5F5', borderRadius: 20, 
    justifyContent: 'center', alignItems: 'center', marginBottom: 20,
    borderWidth: 1, borderColor: '#E0E0E0', borderStyle: 'dashed'
  },
  voiceBox: { height: 80, borderStyle: 'solid' },
  previewImage: { width: '100%', height: '100%', borderRadius: 20 },
  uploadText: { fontSize: 16, color: '#757575' },
  desc: { fontSize: 14, color: '#9E9E9E', textAlign: 'center', marginBottom: 40, lineHeight: 20 },
  submitButton: { backgroundColor: '#4CAF50', height: 60, borderRadius: 30, justifyContent: 'center', alignItems: 'center', elevation: 5 },
  submitText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  disabledButton: { backgroundColor: '#A5D6A7' }
});