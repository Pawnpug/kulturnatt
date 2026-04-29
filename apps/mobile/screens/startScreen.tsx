import React from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
} from "react-native";

type Props = {
  onLoginPress?: () => void;
  onCreateAccountPress?: () => void;
};

export default function StartScreen({
  onLoginPress,
  onCreateAccountPress,
}: Props) {
  return (
    <View style={styles.container}>
      {/* APPNAMN */}
      <Text style={styles.title}>tsm</Text>

      {/* LOGIN */}
      <TouchableOpacity
        style={styles.primaryButton}
        onPress={onLoginPress}
      >
        <Text style={styles.primaryButtonText}>Login</Text>
      </TouchableOpacity>

      {/* CREATE ACCOUNT */}
      <TouchableOpacity
        style={styles.secondaryButton}
        onPress={onCreateAccountPress}
      >
        <Text style={styles.secondaryButtonText}>
          Create Account
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#ffffff",
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 24,
  },

  title: {
    fontSize: 42,
    fontWeight: "800",
    color: "#111",
    marginBottom: 50,
    textTransform: "uppercase",
  },

  primaryButton: {
    width: "100%",
    backgroundColor: "#111",
    paddingVertical: 16,
    borderRadius: 18,
    alignItems: "center",
    marginBottom: 14,
  },

  primaryButtonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "700",
  },

  secondaryButton: {
    width: "100%",
    backgroundColor: "#f2f2f2",
    paddingVertical: 16,
    borderRadius: 18,
    alignItems: "center",
  },

  secondaryButtonText: {
    color: "#111",
    fontSize: 16,
    fontWeight: "700",
  },
});