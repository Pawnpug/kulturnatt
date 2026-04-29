import React from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

type Props = {
  onLoginPress?: () => void;
  onCreateAccountPress?: () => void;
};

export default function StartScreen({
  onLoginPress,
  onCreateAccountPress,
}: Props) {
  const insets = useSafeAreaInsets();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>tsm</Text>

      <View style={[styles.buttonSection, { bottom: insets.bottom + 90 }]}>
        <TouchableOpacity style={styles.loginButton} onPress={onLoginPress}>
          <Text style={styles.buttonText}>Log in</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.createButton}
          onPress={onCreateAccountPress}
        >
          <Text style={styles.buttonText}>Create account</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#ECD7F8",
    alignItems: "center",
  },

  title: {
    marginTop: 250,
    fontSize: 80,
    fontWeight: "900",
    color: "#000",
    letterSpacing: 2,
    fontStyle: "italic",
  },

  buttonSection: {
    position: "absolute",
    width: "100%",
    alignItems: "center",
    paddingHorizontal: 32,
  },

  loginButton: {
    width: "100%",
    backgroundColor: "#f7f2f8",
    paddingVertical: 14,
    borderRadius: 28,
    alignItems: "center",
    marginBottom: 62,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 7 },
    shadowOpacity: 0.28,
    shadowRadius: 8,
    elevation: 8,
  },

  createButton: {
    width: "100%",
    backgroundColor: "#C058E2",
    paddingVertical: 14,
    borderRadius: 28,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 7 },
    shadowOpacity: 0.28,
    shadowRadius: 8,
    elevation: 8,
  },

  buttonText: {
    fontSize: 20,
    fontWeight: "800",
    color: "#000",
  },
});