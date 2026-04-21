import { useEffect, useState } from 'react';
import { StyleSheet, Text, View, FlatList, ActivityIndicator } from 'react-native';

// 임시 백엔드 URL (실제 기기 테스트 시 본인 PC의 내부 IP로 변경 필요)
const API_URL = 'http://10.95.111.6:8000'; 
const DEVICE_ID = 'elderly_home_01';

export default function SafetyLogScreen() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/logs/${DEVICE_ID}`)
      .then((res) => res.json())
      .then((data) => {
        setLogs(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Backend connection error", err);
        setLoading(false);
      });
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.headerTitle}>부모님 안부 확인</Text>
      
      {loading ? (
        <ActivityIndicator size="large" color="#4CAF50" />
      ) : (
        <FlatList
          data={logs}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={[styles.card, item.is_emergency && styles.emergencyCard]}>
              <Text style={styles.time}>{new Date(item.timestamp).toLocaleTimeString()}</Text>
              <Text style={styles.output}>{item.output}</Text>
              {item.is_emergency && <Text style={styles.alertText}>🚨 응급 상황</Text>}
            </View>
          )}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#f5f5f5' },
  headerTitle: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  card: { backgroundColor: 'white', padding: 15, borderRadius: 10, marginBottom: 15, elevation: 3 },
  emergencyCard: { borderColor: 'red', borderWidth: 2, backgroundColor: '#ffe6e6' },
  time: { fontSize: 12, color: 'gray', marginBottom: 5 },
  output: { fontSize: 16, lineHeight: 24 },
  alertText: { color: 'red', fontWeight: 'bold', marginTop: 10 },
});