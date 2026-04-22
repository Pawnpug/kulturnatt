# checkar vid swipe, anger vad som visas för användaren
# Hur skall man kolla om en användare har likat en annan användare? För någonting för användare tex en lista den listan kommer antaligen sparas som ett attribut i user

from typing import List, Tuple, Optional, Dict
from user import User
from swipe_algo import SwipeAlgo, EVENT_MULTIPLIER, SONG_MOVIE_MULTIPLIER, ARTIST_DIRECTOR_MULTIPLIER, GENRE_MULTIPLIER


class MatchAlgo:
    """MatchAlgo - Hittar och sorterar matchningar checkar vid swipe,
    anger vad som visas för användaren"""
    #self - Referens till själva objektet (behövs alltid)
    #current_user: User - Den användare som söker matchning 
    #all_users: List[User] - En lista med alla användare i systemet (för att kunna jämföra med current_user)

    def __init__(self, current_user: User, all_users: List[User]):
        self.current_user = current_user  # Sparar den inloggade användaren
        self.all_users = all_users  # Sparar Listan med alla användare
        self.swipe_algo = SwipeAlgo()  # Skapar instans av SwipeAlgo

    def basic_check(self, other_user: User) -> bool:
        """
        Basic check - behöver stämma för att programmet skall gå vidare.
        """
        # Alice skickar fråga . Kolla Bobs matchningspreferenser Bob är 28 år och söker 25-35 åring, Alice är 25 år och söker 20-30 åringar
        # Steg 1: Kollar om Alice är inom Bobs ålderspreferenser (25 <= 28 <= 35) → JA (Alice är 25 år) 
        # Steg 2: Kollar om Bob är inom Alices ålderspreferenser (20 <= 28 <= 30) → JA (Bob är 28 år)
        user_in_other_range = (other_user.age_range[0] <= self.current_user.age <= other_user.age_range[1])
        other_in_user_range = (self.current_user.age_range[0] <= other_user.age <= self.current_user.age_range[1])
        
        # Kollar Alice vs Charlie
        # Alice skickar fråga . Kolla Charlies matchningspreferenser Charlie är 21 år och söker 18-23 åringar, Alice är 25 år och söker 20-30 åringar
        # Steg 1: Kollar om Alice är inom Charlies ålderspreferenser (18 <= 25 <= 23) → NEJ (Alice är 25 år)
        # Steg 2: Kollar om Charlie är inom Alices ålderspreferenser (20 <= 21 <= 30) → JA (Charlie är 21 år)
    
        if not (user_in_other_range and other_in_user_range):
            return False    

        # Visa ej blockerade användare
        if other_user.user_id in self.current_user.blocked_users:
            return False
        if self.current_user.user_id in other_user.blocked_users:
            return False

        return True

    def calculate_match_score(self, other_user: User) -> Tuple[int, Dict]:
        """Anropar SwipeAlgo's metod för poänguträkning"""
        total_score = self.swipe_algo.calculate_score(self.current_user, other_user)
        details = self.swipe_algo.get_match_details(self.current_user, other_user)
        return total_score, details

    def get_best_match_highlight(self, other_user: User) -> Tuple[str, int, int]:
        """Returnerar (bästa_kategori, antal_match, total_score)"""
        _, details = self.calculate_match_score(other_user)
        
        if not details:
            return ("Ingen match", 0, 0)  # Trippel med 3 värden (String - ingen matchning, integer 0 (antalmatchningar och integer totalpoäng 0))
        
        # Hitta kategorin med högst poäng
        best_category = max(details.items(), key=lambda x: x[1]['score'])  # Hittar den kategori som har högst poäng (x[1]['score']) och returnerar den kategorin (x[0]) och dess detaljer (x[1])
        category_name = best_category[0]  # Namnet på kategorin (events, songs_movies, artists_directors, genres)
        num_matches = len(best_category[1]['common'])  # Räknar antalet matchningar
        total_score = best_category[1]['score']  # Hämtar poängen för den bästa kategorin
        
        # Översätt kategori till läsbart namn
        category_display = {
            'events': 'Event',
            'songs_movies': 'Låtar/Filmer',
            'artists_directors': 'Artister/Regissörer',
            'genres': 'Genrer'
        }.get(category_name, category_name)
        
        return (category_display, num_matches, total_score)

    def get_potential_matches(self) -> List[Tuple[User, int, Dict]]:
        """Anropar SwipeAlgo's get_scored_users direkt"""
        return self.swipe_algo.get_scored_users(self.current_user, self.all_users)
        # Förslag sortera efter tid när swipet gjordes och inte efter poäng

    def get_swipe_nej_lista(self) -> List[User]:
        """Swipeat nej-lista (nej och unmatchade) - sorterad efter senast swipad"""
        return [user for user in self.all_users 
                if user.user_id in self.current_user.rejected_users]
    
    def get_next_profile(self) -> Optional[Tuple[User, int, Dict]]:
        """SwipeAlgo's metod get_next_profile() returnerar nästa profil att visa för användaren, baserat på poäng och vilka profiler som redan visats"""
        return self.swipe_algo.get_next_profile(self.current_user, self.all_users)
      
# ============= TESTNING =============

# Skapa användare
user1 = User(
    user_id=1, email="alice@email.com", username="Alice", age=25, gender="kvinna",
    blocked_users=[], seen_users=[], age_range=(20, 30),
    events=["Musikfestival", "Bio-premiär"], songs=["Bohemian Rhapsody"], movies=["Interstellar"],
    artists=["Freddie Mercury"], directors=["Christopher Nolan"],
    music_genre=["Rock"], movie_genre=["Sci-fi"]
)

user2 = User(
    user_id=2, email="bob@email.com", username="Bob", age=28, gender="man",
    blocked_users=[], seen_users=[], age_range=(25, 35),
    events=["Musikfestival"], songs=["Bohemian Rhapsody"], movies=["Pulp Fiction"],
    artists=["Freddie Mercury"], directors=["Quentin Tarantino"],
    music_genre=["Rock"], movie_genre=["Action"]
)

all_users = [user1, user2]

# Skapa matchAlgo
match_algo = MatchAlgo(user1, all_users)

# Hämta nästa profil
next_profile = match_algo.get_next_profile()
if next_profile:
    user, score, details = next_profile
    print(f"Nästa profil: {user.username}, Poäng: {score}")
    
    # Best-match highlight
    best_cat, num, total = match_algo.get_best_match_highlight(user)
    print(f"Best match: {best_cat} ({num} st, {total} poäng)")
    
    # Markera som visad
    match_algo.mark_profile_as_seen(user.user_id)