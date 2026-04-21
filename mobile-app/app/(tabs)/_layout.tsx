import { Tabs } from 'expo-router';
import { FontAwesome } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs screenOptions={{ tabBarActiveTintColor: '#4CAF50' }}>
      <Tabs.Screen
        name="index"
        options={{
          title: '안심 로그',
          tabBarIcon: ({ color }) => <FontAwesome name="heartbeat" size={24} color={color} />,
        }}
      />
      <Tabs.Screen
        name="memory"
        options={{
          title: '추억 대화',
          tabBarIcon: ({ color }) => <FontAwesome name="photo" size={24} color={color} />,
        }}
      />
    </Tabs>
  );
}