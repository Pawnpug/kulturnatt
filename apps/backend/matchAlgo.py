# checkar vid swipe, anger vad som visas för användaren
# Hur skall man kolla om en användare har likat en annan användare? För någonting för användare tex en lista den listan kommer antaligen sparas som ett attribut i user

from typing import List, Tuple, Optional, Dict
from user import User
from swipeAlgo import get_scored_users, get_scored_rejected_users, EVENT_MULTIPLIER, SONG_MOVIE_MULTIPLIER, ARTIST_DIRECTOR_MULTIPLIER, GENRE_MULTIPLIER


class MatchAlgo:
    """MatchAlgo - Hittar och sorterar matchningar checkar vid swipe,
    anger vad som visas för användaren"""
    #self - Referens till själva objektet (behövs alltid)
    #current_user: User - Den användare som söker matchning 
    #all_users: List[User] - En lista med alla användare i systemet (för att kunna jämföra med current_user)

    def __init__(self, current_user: User, all_users: List[User]):
        self.current_user = current_user  # Sparar den inloggade användaren
        self.all_users = all_users  # Sparar Listan med alla användare

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
    
    def _get_common_items(self, other_user: User, attr1: str, attr2: str = None) -> set:
        """Hjälpfunktion för att hitta gemensamma items mellan två användare"""
        items1 = getattr(self.current_user, attr1)
        items2 = getattr(other_user, attr1)
        common = set(items1) & set(items2)
        
        if attr2:  # Om vi har två attribut att slå ihop (t.ex. songs och movies)
            items1_2 = getattr(self.current_user, attr2)
            items2_2 = getattr(other_user, attr2)
            common |= set(items1_2) & set(items2_2)
        
        return common
    
    def _get_match_details(self, other_user: User) -> Dict:
        """Hjälpfunktion för att få matchdetaljer från gemensamma intressen"""
        details = {}
        
        # Definerar kategorier: (nyckel, visningsnamn, attribut1, attribut2, multiplier)
        categories = [
            ('events', 'Event', 'events', None, EVENT_MULTIPLIER),
            ('songs_movies', 'Låtar/Filmer', 'songs', 'movies', SONG_MOVIE_MULTIPLIER),
            ('artists_directors', 'Artister/Regissörer', 'artists', 'directors', ARTIST_DIRECTOR_MULTIPLIER),
            ('genres', 'Genrer', 'music_genre', 'movie_genre', GENRE_MULTIPLIER)
        ]
        
        for key, _, attr1, attr2, multiplier in categories:
            common = self._get_common_items(other_user, attr1, attr2)
            if common:
                details[key] = {
                    'common': list(common),
                    'score': len(common) * multiplier
                }
        
        return details

    def calculate_match_score(self, other_user: User) -> Tuple[int, Dict]:
        """Beräknar poäng mellan två användare baserat på gemensamma intressen"""
        # Använder get_scored_users för att få poängen
        scored_users = get_scored_users(self.current_user, [other_user])
        total_score = scored_users[0][1] if scored_users else 0
        
        details = self._get_match_details(other_user)
        return total_score, details

    def get_best_match_highlight(self, other_user: User) -> Tuple[str, int, int]:
        """Returnerar (bästa_kategori, antal_match, total_score)"""
        _, details = self.calculate_match_score(other_user)
        
        if not details:
            return ("Ingen match", 0, 0)
        
        # Hitta kategorin med högst poäng
        best_category = max(details.items(), key=lambda x: x[1]['score'])
        category_name = best_category[0]  # Namnet på kategorin
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
        """Anropar SwipeAlgo's get_scored_users direkt och lägger till detaljer"""
        scored_users = get_scored_users(self.current_user, self.all_users)
        # Förslag sortera efter tid när swipet gjordes och inte efter poäng
        
        # Lägger till details för varje matchning
        return [(user, score, self._get_match_details(user)) for user, score in scored_users]

    def get_swipe_nej_lista(self) -> List[User]:
        """Swipeat nej-lista (nej och unmatchade) - sorterad efter senast swipad"""
        scored_rejected = get_scored_rejected_users(self.current_user, self.all_users)
        return [user for user, _ in scored_rejected]


# ============= TESTNING =============

if __name__ == "__main__":
    # Skapa användare
    alice = User(
        user_id=1, email="alice@email.com", username="Alice", age=25, gender="kvinna",
        blocked_users=[], rejected_users=[], age_range=(20, 30),
        events=["Musikfestival", "Bio-premiär"], songs=["Bohemian Rhapsody"], movies=["Interstellar"],
        artists=["Freddie Mercury"], directors=["Christopher Nolan"],
        music_genre=["Rock"], movie_genre=["Sci-fi"]
    )

    bob = User(
        user_id=2, email="bob@email.com", username="Bob", age=28, gender="man",
        blocked_users=[], rejected_users=[], age_range=(25, 35),
        events=["Musikfestival"], songs=["Bohemian Rhapsody"], movies=["Pulp Fiction"],
        artists=["Freddie Mercury"], directors=["Quentin Tarantino"],
        music_genre=["Rock"], movie_genre=["Action"]
    )

    charlie = User(
        user_id=3, email="charlie@email.com", username="Charlie", age=22, gender="man",
        blocked_users=[], rejected_users=[], age_range=(20, 28),
        events=["Sportevent"], songs=[], movies=["Fast & Furious"],
        artists=[], directors=["Michael Bay"],
        music_genre=[], movie_genre=["Action"]
    )

    all_users = [alice, bob, charlie]
    
    # Testa MatchAlgo för Alice
    print("=" * 50)
    print("MatchAlgo test för Alice")
    print("=" * 50)
    
    match_algo = MatchAlgo(alice, all_users)
    matches = match_algo.get_potential_matches()
    
    print("\nMatchningar sorterade efter poäng:")
    for idx, (user, score, details) in enumerate(matches):
        print(f"  {user.username} ({user.age} år): {score} poäng")
        
        # Visa highlight för bästa matchningen
        if idx == 0:
            highlight, num, cat_score = match_algo.get_best_match_highlight(user)
            if highlight != "Ingen match":
                print(f"    ✨ Bäst: {highlight} ({num} st, {cat_score} poäng)")
    
    # Testa basic_check
    print("\n" + "=" * 50)
    print("Basic check test")
    print("=" * 50)
    
    print(f"\nKollar om Alice och Bob klarar basic check:")
    result = match_algo.basic_check(bob)
    print(f"  Resultat: {result}")
    
    # Testa nej-listan
    print("\n" + "=" * 50)
    print("Nej-lista test")
    print("=" * 50)
    
    # Lägger till Bob i Alice's rejected_users
    alice.rejected_users.append(2)
    print(f"\nAlice rejectade Bob (user_id: 2)")
    
    nej_listan = match_algo.get_swipe_nej_lista()
    print(f"Användare i Alice's nej-lista:")
    for user in nej_listan:
        print(f"  {user.username} ({user.age} år)")