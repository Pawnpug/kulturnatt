import uuid

from fastapi import FastAPI
from pydantic import BaseModel
from services import setup_profile, on_profile_update, perform_match

app = FastAPI()

class ProfileSetupRequest(BaseModel):
    user_id: uuid.UUID
    username: str
    age: int
    gender: str
    preferred_gender: list[str]
    age_range: list[int]
    events: list[str]
    songs: list[str]
    movies: list[str]
    show: list[str]
    artists: list[str]
    directors: list[str]
    music_genre: list[str]
    movie_genre: list[str]
    art: bool
    literature: list[str]
    
@app.post("/profile/setup")
def profile_setup(request: ProfileSetupRequest):
    setup_profile(
        user_id = request.user_id,
        username = request.username,
        age = request.age,
        gender = request.gender,
        preferred_gender = request.preferred_gender,
        age_range = request.age_range,
        events = request.events,
        songs = request.songs,
        movies = request.movies,
        show = request.show,
        artists = request.artists,
        directors = request.directors,
        music_genre = request.music_genre,
        movie_genre = request.movie_genre,
        art = request.art,
        literature = request.literature,
    )
    return {"status": "ok"}

