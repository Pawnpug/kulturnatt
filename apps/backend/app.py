from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from musicbrainz import get_artist_suggestions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/artists/suggestions")
def artist_suggestions(query: str, limit: int = 5):
    return get_artist_suggestions(query, limit)