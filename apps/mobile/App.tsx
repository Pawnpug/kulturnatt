import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import ArtistSearch from "./components/ArtistSearch";

export default function App() {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text style={styles.header}>Music search test</Text>

        <View style={styles.card}>
          <ArtistSearch
            onSelectArtist={(artist) => {
              console.log("Selected artist:", artist);
            }}
          />
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#f2f2f2",
  },
  container: {
    flex: 1,
    padding: 20,
  },
  header: {
    fontSize: 24,
    fontWeight: "700",
    marginBottom: 16,
  },
  card: {
    flex: 1,
    backgroundColor: "#fff",
    borderRadius: 16,
    padding: 16,
  },
});