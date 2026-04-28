import uuid
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from user import User

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def row_to_user(row: dict) -> User:
    return User(
        user_id=uuid.UUID(row["id_profile"]),
        username=row["username"],
        age=row["age"],
        gender=row["gender"],
        preferred_gender=row["preferred_gender"],
        user_ranked_list=row["user_ranked_list"],
        blocked_users=[uuid.UUID(u) for u in row["blocked_users"]],
        rejected_users=[uuid.UUID(u) for u in row["rejected_users"]],
        liked_users=[uuid.UUID(u) for u in row["liked_users"]],
        matched_users=[uuid.UUID(u) for u in row["matched_users"]],
        age_range=tuple(row["age_range"]),
        events=row["events"],
        songs=row["songs"],
        movies=row["movies"],
        artists=row["artists"],
        directors=row["directors"],
        music_genre=row["music_genre"],
        movie_genre=row["movie_genre"],
    )


def get_all_users() -> list[User]:
    response = supabase.table("profile").select("*").execute()
    return [row_to_user(row) for row in response.data]


def save_ranked_list(user_id: uuid.UUID, ranked_list: list[dict]):
    supabase.table("profile").update({"user_ranked_list": ranked_list}).eq("id_profile", str(user_id)).execute()


def update_profile(user: User):
    supabase.table("profile").update({
        "username": user.username,
        "age": user.age,
        "gender": user.gender,
        "preferred_gender": user.preferred_gender,
        "age_range": list(user.age_range),
        "events": user.events,
        "songs": user.songs,
        "movies": user.movies,
        "artists": user.artists,
        "directors": user.directors,
        "music_genre": user.music_genre,
        "movie_genre": user.movie_genre,
    }).eq("id_profile", str(user.user_id)).execute()


def save_match(user_a: User, user_b: User):
    supabase.table("profile").update({
        "liked_users": [str(u) for u in user_a.liked_users],
        "matched_users": [str(u) for u in user_a.matched_users],
    }).eq("id_profile", str(user_a.user_id)).execute()
    supabase.table("profile").update({
        "liked_users": [str(u) for u in user_b.liked_users],
        "matched_users": [str(u) for u in user_b.matched_users],
    }).eq("id_profile", str(user_b.user_id)).execute()
