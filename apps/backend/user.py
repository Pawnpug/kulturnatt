class User:
    def __init__(
        self,
        user_id: int,
        email: str,
        username: str,
        age: int,
        gender: str,
        blocked_users: list[int],
        rejected_users: list[int],
        liked_users: list[int],
        matchade_users: list[int],
        age_range: tuple[int, int],
        events: list[str],
        songs: list[str],
        movies: list[str],
        artists: list[str],
        directors: list[str],
        music_genre: list[str],
        movie_genre: list[str],
    ):
        self.user_id = user_id
        self.email = email
        self.username = username
        self.age = age
        self.gender = gender
        self.blocked_users = blocked_users
        self.rejected_users = rejected_users
        self.liked_users = liked_users
        self.matchade_users = matchade_users
        self.age_range = age_range
        self.events = events
        self.songs = songs
        self.movies = movies
        self.artists = artists
        self.directors = directors
        self.music_genre = music_genre
        self.movie_genre = movie_genre
