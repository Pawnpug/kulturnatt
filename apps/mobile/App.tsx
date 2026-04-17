import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Kulturnatt</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f3f0d6',
    alignItems: 'center',
    paddingTop: 80,
  },
  title: {
    color: '#44150e',
    fontSize: 36,
    fontWeight: 'bold',
    paddingTop: 30,
    marginBottom: 20,
  },
});
