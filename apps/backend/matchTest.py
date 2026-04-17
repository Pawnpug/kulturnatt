class Person:
    def __init__(self, name, age, music, movies):
        self.name = name
        self.age = age
        self.music = music
        self.movies = movies

hugo = Person("Hugo", 22, ["jazz", "pop"], ["Pacific Rim", "The Godfather"])
eva = Person("Eva", 50, ["rap"], ["The Godfather"])
bianca = Person("Bianca", 40, ["jazz", "rnb"], ["Star Wars"])

def match(p1, p2):
    shared_music = set(p1.music) & set(p2.music)
    shared_movies = set(p1.movies) & set(p2.movies)
    if(shared_music):
        print(f"Match för samma musiksmak mellan {p1.name} och {p2.name}")
    elif(shared_movies):
        print(f"Match för samma filmsmak mellan {p1.name} och {p2.name}")
    else: print("Ingen match mellan personerna")

match(hugo, eva)