# bestämmer vilka personer som visas för användaren, baserat på deras preferenser och tidigare swipes
from user import User
import random


# skapa en lista med filtrerade användare som används för scoring
def filter_users(current_user: User, all_users: list[User]) -> list[User]:
    user_pool = []

    current_user_disliked = set(getattr(current_user, "disliked_users", []))
    current_user_removed = set(getattr(current_user, "removed_users", []))
    current_user_unmatched = set(getattr(current_user, "unmatched_users", []))

    removed_ids = current_user_disliked | current_user_removed | current_user_unmatched

    for user in all_users:
        age_ok = (
            user.age_range[0] <= current_user.age <= user.age_range[1]
            and current_user.age_range[0] <= user.age <= current_user.age_range[1]
        )
        gender_ok = (current_user.gender == user.gender)
        not_blocked = (
            user.user_id not in current_user.blocked_users
            and current_user.user_id not in user.blocked_users
        )
        not_same_user = (user.user_id != current_user.user_id)
        not_removed = (user.user_id not in removed_ids)

        if age_ok and gender_ok and not_blocked and not_same_user and not_removed:
            user_pool.append(user)

    return user_pool


# konstanter som används för scoring, kommer ändras...
EVENT_MULTIPLIER = 80
SONG_MOVIE_MULTIPLIER = 10
ARTIST_DIRECTOR_MULTIPLIER = 7
GENRE_MULTIPLIER = 5


# använder de filtrerade användarna från user_pool för att räkna ut score
def scoring_users(current_user: User, user_pool: list[User]) -> list[tuple[User, int]]:
    ranked_user_pool = []

    # räkna hur många av varje typ de har gemensamt
    for user in user_pool:
        shared_events = len(set(current_user.events).intersection(set(user.events)))
        shared_songs = len(set(current_user.songs).intersection(set(user.songs)))
        shared_movies = len(set(current_user.movies).intersection(set(user.movies)))
        shared_artists = len(set(current_user.artists).intersection(set(user.artists)))
        shared_directors = len(set(current_user.directors).intersection(set(user.directors)))
        shared_music_genre = len(set(current_user.music_genre).intersection(set(user.music_genre)))
        shared_movie_genre = len(set(current_user.movie_genre).intersection(set(user.movie_genre)))

        # uträkning för score
        event_score = shared_events * EVENT_MULTIPLIER
        song_movie_score = (shared_songs + shared_movies) * SONG_MOVIE_MULTIPLIER
        artist_director_score = (shared_artists + shared_directors) * ARTIST_DIRECTOR_MULTIPLIER
        genre_score = (shared_music_genre + shared_movie_genre) * GENRE_MULTIPLIER

        user_score = event_score + song_movie_score + artist_director_score + genre_score
        ranked_user_pool.append((user, user_score))

    # om inga har gemensamma intressen -> slumpa user_pool men returnera fortfarande den
    if ranked_user_pool and max(score for _, score in ranked_user_pool) == 0:
        random.shuffle(ranked_user_pool)
        return ranked_user_pool

    ranked_user_pool.sort(key=lambda x: x[1], reverse=True)
    return ranked_user_pool


# huvudfunktion som kallar på de två övre, filter och scoring / sortering
def get_scored_users(current_user: User, all_users: list[User]) -> list[tuple[User, int]]:
    user_pool = filter_users(current_user, all_users)
    return scoring_users(current_user, user_pool)


# separat lista för bortswipade / avmatchade användare
# den byggs när man öppnar den och sorteras då om utifrån nuvarande score
def get_removed_users(current_user: User, all_users: list[User]) -> list[tuple[User, int]]:
    removed_user_pool = []

    current_user_disliked = set(getattr(current_user, "disliked_users", []))
    current_user_removed = set(getattr(current_user, "removed_users", []))
    current_user_unmatched = set(getattr(current_user, "unmatched_users", []))

    removed_ids = current_user_disliked | current_user_removed | current_user_unmatched

    for user in all_users:
        not_same_user = (user.user_id != current_user.user_id)

        not_blocked = (
            user.user_id not in current_user.blocked_users
            and current_user.user_id not in user.blocked_users
        )

        if user.user_id in removed_ids and not_same_user and not_blocked:
            removed_user_pool.append(user)

    return scoring_users(current_user, removed_user_pool)