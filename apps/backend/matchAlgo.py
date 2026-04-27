from user import User

# Returnerar en dictionary med alla gemensamma intressen mellan två användare
# Använder set-operatorn & (snitt) för att hitta overlap i deras listor
def get_shared_interests(user_a: User, user_b: User) -> dict:
    return {
        "events":      list(set(user_a.events)      & set(user_b.events)),
        "songs":       list(set(user_a.songs)       & set(user_b.songs)),
        "movies":      list(set(user_a.movies)      & set(user_b.movies)),
        "artists":     list(set(user_a.artists)     & set(user_b.artists)),
        "directors":   list(set(user_a.directors)   & set(user_b.directors)),
        "music_genre": list(set(user_a.music_genre) & set(user_b.music_genre)),
        "movie_genre": list(set(user_a.movie_genre) & set(user_b.movie_genre)),
    }

# Kollar om två användare gillar varandra ömsesidigt
# Returnerar True om användare B finns i A's liked_users OCH användare A finns i B's liked_users
def is_mutual_like(user_a: User, user_b: User) -> bool:
    return user_b.user_id in user_a.liked_users and user_a.user_id in user_b.liked_users

# Skapar en match om båda användarna gillar varandra
# Tar bort varandra från liked_users och lägger till i matched_users
# Returnerar dictionary med användarna och deras gemensamma intressen, eller None om ingen ömsesidig like
def create_match(user_a: User, user_b: User) -> dict | None:
    if not is_mutual_like(user_a, user_b):
        return None
    user_a.liked_users.remove(user_b.user_id)
    user_b.liked_users.remove(user_a.user_id)
    user_a.matched_users.append(user_b.user_id)
    user_b.matched_users.append(user_a.user_id)

    return {
        "users": (user_a, user_b),
        "shared": get_shared_interests(user_a, user_b),
    }
