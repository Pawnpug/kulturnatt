import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  TextInput,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from "react-native";

type ArtistSuggestion = {
  name: string;
  country?: string | null;
  type?: string | null;
};

type Props = {
  onSelectArtist?: (artist: ArtistSuggestion) => void;
};

/*
  ÄNDRA DENNA SENARE TILL RÄTT BACKEND-ADRESS

  Webbläsare:
  http://localhost:8000

  Android Emulator:
  http://10.0.2.2:8000

  Fysisk mobil:
  http://DIN-IP:8000
*/

const API_BASE_URL = "http://10.0.2.2:8000";

export default function ArtistSearch({ onSelectArtist }: Props) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<ArtistSuggestion[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query.trim().length < 2) {
      setResults([]);
      return;
    }

    const timeout = setTimeout(() => {
      fetchArtists(query);
    }, 300);

    return () => clearTimeout(timeout);
  }, [query]);

  const fetchArtists = async (searchText: string) => {
    try {
      setLoading(true);

      const response = await fetch(
        `${API_BASE_URL}/artists/suggestions?query=${encodeURIComponent(
          searchText
        )}&limit=5`
      );

      const data = await response.json();

      if (Array.isArray(data)) {
        setResults(data);
      } else {
        setResults([]);
      }
    } catch (error) {
      console.log(error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const chooseArtist = (artist: ArtistSuggestion) => {
    setQuery(artist.name);
    setResults([]);

    if (onSelectArtist) {
      onSelectArtist(artist);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Choose artist</Text>

      <TextInput
        style={styles.input}
        placeholder="Search artist..."
        value={query}
        onChangeText={setQuery}
      />

      {loading && <ActivityIndicator style={{ marginTop: 10 }} />}

      <FlatList
        data={results}
        keyExtractor={(item, index) => item.name + index}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.row}
            onPress={() => chooseArtist(item)}
          >
            <Text style={styles.name}>{item.name}</Text>

            {!!item.country && (
              <Text style={styles.meta}>{item.country}</Text>
            )}
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: "100%",
  },

  title: {
    fontSize: 18,
    fontWeight: "700",
    marginBottom: 10,
  },

  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 10,
    padding: 12,
    backgroundColor: "#fff",
  },

  row: {
    padding: 12,
    borderBottomWidth: 1,
    borderColor: "#eee",
  },

  name: {
    fontSize: 16,
    fontWeight: "600",
  },

  meta: {
    color: "#666",
    marginTop: 2,
  },
});