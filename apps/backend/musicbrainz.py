import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MUSICBRAINZ_API_KEY")

# Base-URL för MusicBrainz API
BASE = "https://musicbrainz.org/ws/2"

# Base-URL för Cover Art Archive
CAA_BASE = "https://coverartarchive.org"

HEADERS = {
    "User-Agent": "KulturMatch (elinflodin999@gmail.com)",
    "Accept": "application/json",
}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"



# HTTP-funktioner


def _get(endpoint, params=None):
    r = requests.get(
        f"{BASE}/{endpoint}",
        headers=HEADERS,
        params=params,
        timeout=10
    )
    r.raise_for_status()
    return r.json()


def _get_cover_json(path):
    r = requests.get(
        f"{CAA_BASE}/{path}",
        headers={
            "Accept": "application/json",
            "User-Agent": HEADERS["User-Agent"]
        },
        timeout=10
    )

    if r.status_code == 404:
        return None

    r.raise_for_status()
    return r.json()


# Hjälpfunktioner

def ms_to_minutes_seconds(ms):
    if not ms:
        return None

    total_seconds = ms // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return f"{minutes}:{seconds:02d}"


def extract_artist_names(artist_credit):
    artist_names = []

    for item in artist_credit or []:
        if isinstance(item, dict):
            name = item.get("name")
            if name:
                artist_names.append(name)

    return ", ".join(artist_names)


def extract_year(date_string):
    if not date_string:
        return None

    return str(date_string)[:4]


def extract_cover_data(front_image):
    thumbnails = front_image.get("thumbnails", {})

    return {
        "image_url": front_image.get("image"),
        "thumb_250": thumbnails.get("250") or thumbnails.get("small"),
        "thumb_500": thumbnails.get("500") or thumbnails.get("large"),
        "thumb_1200": thumbnails.get("1200"),
        "is_front": front_image.get("front", False),
        "comment": front_image.get("comment", "")
    }


# Sökning

def search_artists(query, limit=5):
    """
    Söker efter artister.
    """
    return _get("artist", {
        "query": query,
        "fmt": "json",
        "limit": limit
    })


def search_recordings(query, limit=5):
    """
    Söker efter låtar.
    """
    return _get("recording", {
        "query": query,
        "fmt": "json",
        "limit": limit
    })


def search_releases(query, limit=5):
    """
    Söker efter album/releases.
    """
    return _get("release", {
        "query": query,
        "fmt": "json",
        "limit": limit
    })


# Hämta info

def get_artist(artist_id):
    return _get(f"artist/{artist_id}", {
        "fmt": "json"
    })


def get_recording(recording_id):
    return _get(f"recording/{recording_id}", {
        "fmt": "json",
        "inc": "releases"
    })


def get_release(release_id):
    return _get(f"release/{release_id}", {
        "fmt": "json"
    })


# Omslagsbilder

def get_release_cover_art(release_id):
    if not release_id:
        return None

    data = _get_cover_json(f"release/{release_id}")

    if not data or not data.get("images"):
        return None

    front_image = None

    for image in data["images"]:
        if image.get("front") is True:
            front_image = image
            break

    if front_image is None:
        front_image = data["images"][0]

    return extract_cover_data(front_image)


def get_recording_cover_art(recording_id):
    if not recording_id:
        return None

    try:
        recording = get_recording(recording_id)
    except requests.exceptions.RequestException:
        return None

    if not recording:
        return None

    releases = recording.get("releases", [])

    if not releases:
        return None

    for release in releases:
        release_id = release.get("id")
        if not release_id:
            continue

        try:
            cover = get_release_cover_art(release_id)
            if cover:
                return cover
        except requests.exceptions.RequestException:
            continue

    return None



# Formattering för frontend


def format_artist(artist):
    return {
        "name": artist.get("name"),
        "country": artist.get("country"),
        "type": artist.get("type"),
        "disambiguation": artist.get("disambiguation"),
    }


def format_recording(recording, include_cover=True, include_fallback_length=True):
    recording_id = recording.get("id")
    length_ms = recording.get("length")
    release_date = None


    if length_ms is None and include_fallback_length and recording_id:
        try:
            full_recording = get_recording(recording_id)
            if full_recording:
                length_ms = full_recording.get("length")

                releases = full_recording.get("releases", [])
                if releases:
                    release_date = releases[0].get("date")
        except requests.exceptions.RequestException:
            length_ms = None

    if release_date is None:
        releases = recording.get("releases", [])
        if releases:
            release_date = releases[0].get("date")

    cover = None
    if include_cover and recording_id:
        cover = get_recording_cover_art(recording_id)

    return {
        "title": recording.get("title"),
        "artists": extract_artist_names(recording.get("artist-credit")),
        "length": ms_to_minutes_seconds(length_ms),
        "year": extract_year(release_date),
        "disambiguation": recording.get("disambiguation"),
        "cover": cover
    }


def format_release(release, include_cover=True):
    release_id = release.get("id")
    cover = None

    if include_cover and release_id:
        cover = get_release_cover_art(release_id)

    date_value = release.get("date")

    return {
        "title": release.get("title"),
        "artists": extract_artist_names(release.get("artist-credit")),
        "date": date_value,
        "year": extract_year(date_value),
        "country": release.get("country"),
        "status": release.get("status"),
        "cover": cover
    }


# Hämta förslag för autocomplete

def get_artist_suggestions(query, limit=5):
    results = search_artists(query, limit=limit)
    artists = results.get("artists", []) if results else []

    return [format_artist(artist) for artist in artists]


def get_recording_suggestions(query, limit=5):
    results = search_recordings(query, limit=limit)
    recordings = results.get("recordings", []) if results else []

    return [
        format_recording(recording, include_cover=False, include_fallback_length=False)
        for recording in recordings
    ]


def get_release_suggestions(query, limit=5):
    results = search_releases(query, limit=limit)
    releases = results.get("releases", []) if results else []

    return [format_release(release, include_cover=False) for release in releases]


def get_search_suggestions(query, category, limit=5):
    if category == "artist":
        return get_artist_suggestions(query, limit)

    if category == "recording":
        return get_recording_suggestions(query, limit)

    if category == "release":
        return get_release_suggestions(query, limit)

    return []

def get_artist_results(query, limit=10):
 
    results = search_artists(query, limit=limit)
    artists = results.get("artists", []) if results else []

    return [format_artist(artist) for artist in artists]


def get_recording_results(query, limit=10):
    results = search_recordings(query, limit=limit)
    recordings = results.get("recordings", []) if results else []

    return [format_recording(recording, include_cover=True, include_fallback_length=True) for recording in recordings]


def get_release_results(query, limit=10):
    results = search_releases(query, limit=limit)
    releases = results.get("releases", []) if results else []

    return [format_release(release, include_cover=True) for release in releases]


def get_search_results(query, category, limit=10):
    if category == "artist":
        return get_artist_results(query, limit)

    if category == "recording":
        return get_recording_results(query, limit)

    if category == "release":
        return get_release_results(query, limit)

    return []


# För att kunna välja i sin profil

def get_profile_song_data(query, limit=1):
    results = search_recordings(query, limit=limit)
    recordings = results.get("recordings", []) if results else []

    if not recordings:
        return None

    recording = recordings[0]
    formatted = format_recording(recording, include_cover=True, include_fallback_length=True)

    return {
        "title": formatted.get("title"),
        "artists": formatted.get("artists"),
        "year": formatted.get("year"),
        "cover": formatted.get("cover")
    }


# Testutskrift i terminal

def print_artist_suggestions(query):
    suggestions = get_artist_suggestions(query, limit=5)

    print(f"\nArtistförslag för '{query}':\n")
    for i, item in enumerate(suggestions, 1):
        text = item["name"]
        if item.get("country"):
            text += f" ({item['country']})"
        print(f"{i}. {text}")


def print_recording_suggestions(query):
    suggestions = get_recording_suggestions(query, limit=5)

    print(f"\nLåtförslag för '{query}':\n")
    for i, item in enumerate(suggestions, 1):
        parts = [item.get("title")]
        if item.get("artists"):
            parts.append(item["artists"])
        if item.get("length"):
            parts.append(item["length"])
        print(f"{i}. " + " - ".join([p for p in parts if p]))


def print_release_suggestions(query):
    suggestions = get_release_suggestions(query, limit=5)

    print(f"\nAlbumförslag för '{query}':\n")
    for i, item in enumerate(suggestions, 1):
        parts = [item.get("title")]
        if item.get("artists"):
            parts.append(item["artists"])
        if item.get("year"):
            parts.append(item["year"])
        print(f"{i}. " + " - ".join([p for p in parts if p]))


def print_artist_results(query):
    results = get_artist_results(query, limit=10)

    print(f"\nArtistresultat för '{query}':\n")
    for i, item in enumerate(results, 1):
        parts = [item.get("name")]
        if item.get("country"):
            parts.append(item["country"])
        if item.get("type"):
            parts.append(item["type"])
        print(f"{i}. " + " - ".join([p for p in parts if p]))


def print_recording_results(query):
    results = get_recording_results(query, limit=10)

    print(f"\nLåtresultat för '{query}':\n")
    for i, item in enumerate(results, 1):
        parts = [item.get("title")]
        if item.get("artists"):
            parts.append(item["artists"])
        if item.get("length"):
            parts.append(item["length"])
        if item.get("year"):
            parts.append(item["year"])

        line = " - ".join([p for p in parts if p])
        print(f"{i}. {line}")

        if item.get("cover") and item["cover"].get("thumb_250"):
            print(f"   Cover: {item['cover']['thumb_250']}")


def print_release_results(query):
    results = get_release_results(query, limit=10)

    print(f"\nAlbumresultat för '{query}':\n")
    for i, item in enumerate(results, 1):
        parts = [item.get("title")]
        if item.get("artists"):
            parts.append(item["artists"])
        if item.get("year"):
            parts.append(item["year"])

        line = " - ".join([p for p in parts if p])
        print(f"{i}. {line}")

        if item.get("cover") and item["cover"].get("thumb_250"):
            print(f"   Cover: {item['cover']['thumb_250']}")


def print_profile_song_data(query):
    result = get_profile_song_data(query)

    print(f"\nProfil-låt för '{query}':\n")

    if not result:
        print("Ingen låt hittades.")
        return

    parts = [result.get("title")]
    if result.get("artists"):
        parts.append(result["artists"])
    if result.get("year"):
        parts.append(result["year"])

    print(" - ".join([p for p in parts if p]))

    if result.get("cover") and result["cover"].get("thumb_250"):
        print(f"Cover: {result['cover']['thumb_250']}")


# Backend test

if __name__ == "__main__":
    try:
        print("Vad vill du testa?")
        print("1. Artistförslag")
        print("2. Låtförslag")
        print("3. Albumförslag")
        print("4. Artistresultat")
        print("5. Låtresultat")
        print("6. Albumresultat")
        print("7. Profil-låt")

        choice = input("\nVälj 1-7: ").strip()
        query = input("Skriv din sökning: ").strip()

        if choice == "1":
            print_artist_suggestions(query)
        elif choice == "2":
            print_recording_suggestions(query)
        elif choice == "3":
            print_release_suggestions(query)
        elif choice == "4":
            print_artist_results(query)
        elif choice == "5":
            print_recording_results(query)
        elif choice == "6":
            print_release_results(query)
        elif choice == "7":
            print_profile_song_data(query)
        else:
            print("Ogiltigt val.")

    except requests.exceptions.RequestException as e:
        print(f"Ett fel uppstod vid API-anrop: {e}")
    except Exception as e:
        print(f"Ett oväntat fel uppstod: {e}")