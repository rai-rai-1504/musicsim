"""Hidden non-artist social seeds for later romance and tabloid systems.

These characters are intentionally kept outside the main music ecosystem roster.
They are lightweight public figures that can be referenced by future modules
without affecting release calendars, reviews, or artist simulation logic.
"""

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class HiddenCharacterSeed:
    name: str
    category: str
    gender: str
    sexuality: str | None
    romance_preference: str | None
    friendliness: int
    lovingness: int
    popularity: float
    reputation: int


VALID_ROMANCE_PREFERENCES = ("prefers_male", "prefers_female", "prefers_both")


def _stable_hidden_rng(label: str) -> random.Random:
    value = 0
    for ch in label:
        value = (value * 131 + ord(ch)) & 0xFFFFFFFF
    return random.Random(value)


def _hidden_romance_preference_for_name(name: str) -> str:
    rng = _stable_hidden_rng("hidden-romance-pref:" + str(name))
    return rng.choices(
        VALID_ROMANCE_PREFERENCES,
        weights=[20, 72, 8],
        k=1,
    )[0]


def _hidden_seed(
    name: str,
    category: str,
    friendliness: int,
    lovingness: int,
    popularity: float,
    reputation: int,
    gender: str | None = None,
    sexuality: str | None = None,
) -> HiddenCharacterSeed:
    if gender is None:
        if category == "actor":
            gender = "male"
        elif category in {"actress", "model"}:
            gender = "female"
        else:
            gender = "male"
    return HiddenCharacterSeed(
        name=str(name),
        category=str(category),
        gender=str(gender),
        sexuality=sexuality,
        romance_preference=_hidden_romance_preference_for_name(name),
        friendliness=int(friendliness),
        lovingness=int(lovingness),
        popularity=float(popularity),
        reputation=int(reputation),
    )


def _female_athlete_seed(
    name: str,
    friendliness: int,
    lovingness: int,
    popularity: float,
    reputation: int,
) -> HiddenCharacterSeed:
    return _hidden_seed(
        name,
        "athlete",
        friendliness,
        lovingness,
        popularity,
        reputation,
        gender="female",
    )


def _male_athlete_seed(
    name: str,
    friendliness: int,
    lovingness: int,
    popularity: float,
    reputation: int,
) -> HiddenCharacterSeed:
    return _hidden_seed(name, "athlete", friendliness, lovingness, popularity, reputation, gender="male")


ACTOR_SEEDS: list[HiddenCharacterSeed] = [
    _hidden_seed("Leonardo DiCaprio", "actor", 48, 32, 96.0, 94),
    _hidden_seed("Brad Pitt", "actor", 58, 45, 93.0, 88),
    _hidden_seed("Tom Cruise", "actor", 36, 28, 95.0, 84),
    _hidden_seed("Denzel Washington", "actor", 72, 54, 91.0, 97),
    _hidden_seed("Robert Downey Jr.", "actor", 68, 57, 95.0, 93),
    _hidden_seed("Ryan Gosling", "actor", 64, 61, 90.0, 92),
    _hidden_seed("Ryan Reynolds", "actor", 78, 69, 92.0, 89),
    _hidden_seed("Jake Gyllenhaal", "actor", 62, 52, 86.0, 89),
    _hidden_seed("Christian Bale", "actor", 34, 30, 88.0, 94),
    _hidden_seed("Michael B. Jordan", "actor", 74, 73, 89.0, 90),
    _hidden_seed("Chris Hemsworth", "actor", 76, 72, 91.0, 88),
    _hidden_seed("Chris Evans", "actor", 82, 74, 90.0, 91),
    _hidden_seed("Paul Mescal", "actor", 67, 66, 82.0, 88),
    _hidden_seed("Timothee Chalamet", "actor", 61, 64, 92.0, 87),
    _hidden_seed("Austin Butler", "actor", 58, 56, 84.0, 83),
    _hidden_seed("Barry Keoghan", "actor", 43, 49, 80.0, 79),
    _hidden_seed("Cillian Murphy", "actor", 46, 38, 89.0, 95),
    _hidden_seed("Pedro Pascal", "actor", 84, 71, 91.0, 93),
    _hidden_seed("Andrew Garfield", "actor", 79, 76, 88.0, 92),
    _hidden_seed("Dev Patel", "actor", 73, 68, 84.0, 91),
    _hidden_seed("Oscar Isaac", "actor", 70, 59, 85.0, 90),
    _hidden_seed("Daniel Kaluuya", "actor", 66, 57, 82.0, 90),
    _hidden_seed("Idris Elba", "actor", 75, 58, 88.0, 92),
    _hidden_seed("Lakeith Stanfield", "actor", 51, 47, 79.0, 84),
    _hidden_seed("Adam Driver", "actor", 39, 35, 86.0, 93),
    _hidden_seed("Keanu Reeves", "actor", 88, 62, 94.0, 98),
    _hidden_seed("Joaquin Phoenix", "actor", 28, 24, 87.0, 91),
    _hidden_seed("Colman Domingo", "actor", 77, 63, 81.0, 93),
    _hidden_seed("Jeremy Allen White", "actor", 57, 54, 83.0, 84),
    _hidden_seed("Sebastian Stan", "actor", 63, 55, 84.0, 86),
    _hidden_seed("Glen Powell", "actor", 74, 67, 83.0, 82),
    _hidden_seed("Jonathan Majors", "actor", 22, 31, 78.0, 38),
    _hidden_seed("Donald Glover", "actor", 59, 48, 87.0, 90),
    _hidden_seed("Daniel Radcliffe", "actor", 76, 65, 85.0, 94),
    _hidden_seed("Joseph Quinn", "actor", 68, 60, 79.0, 82),
    _hidden_seed("Nicholas Hoult", "actor", 69, 58, 80.0, 86),
    _hidden_seed("Paul Rudd", "actor", 89, 64, 88.0, 95),
    _hidden_seed("Mark Ruffalo", "actor", 73, 53, 84.0, 92),
    _hidden_seed("Mahershala Ali", "actor", 71, 49, 83.0, 95),
    _hidden_seed("Matt Damon", "actor", 65, 46, 88.0, 89),
    _hidden_seed("Ben Affleck", "actor", 44, 41, 89.0, 76),
    _hidden_seed("Henry Cavill", "actor", 72, 62, 87.0, 88),
    _hidden_seed("John Boyega", "actor", 74, 61, 81.0, 88),
    _hidden_seed("Simu Liu", "actor", 71, 57, 80.0, 84),
    _hidden_seed("Riz Ahmed", "actor", 67, 55, 82.0, 91),
    _hidden_seed("Jamie Foxx", "actor", 63, 52, 89.0, 87),
    _hidden_seed("Will Smith", "actor", 54, 50, 94.0, 70),
    _hidden_seed("Jamie Dornan", "actor", 68, 63, 78.0, 84),
    _hidden_seed("Kit Harington", "actor", 61, 57, 76.0, 82),
    _hidden_seed("Regé-Jean Page", "actor", 70, 66, 79.0, 85),
]

ACTRESS_SEEDS: list[HiddenCharacterSeed] = [
    _hidden_seed("Zendaya", "actress", 81, 78, 95.0, 94),
    _hidden_seed("Margot Robbie", "actress", 74, 68, 93.0, 92),
    _hidden_seed("Florence Pugh", "actress", 76, 72, 88.0, 91),
    _hidden_seed("Emma Stone", "actress", 72, 62, 91.0, 95),
    _hidden_seed("Jennifer Lawrence", "actress", 79, 65, 92.0, 90),
    _hidden_seed("Scarlett Johansson", "actress", 61, 54, 94.0, 92),
    _hidden_seed("Ana de Armas", "actress", 68, 63, 87.0, 85),
    _hidden_seed("Sydney Sweeney", "actress", 58, 66, 89.0, 80),
    _hidden_seed("Megan Fox", "actress", 46, 44, 86.0, 73),
    _hidden_seed("Angelina Jolie", "actress", 56, 41, 96.0, 93),
    _hidden_seed("Natalie Portman", "actress", 71, 52, 90.0, 95),
    _hidden_seed("Anne Hathaway", "actress", 77, 61, 89.0, 91),
    _hidden_seed("Carey Mulligan", "actress", 69, 55, 82.0, 94),
    _hidden_seed("Saoirse Ronan", "actress", 74, 67, 85.0, 94),
    _hidden_seed("Greta Lee", "actress", 75, 62, 78.0, 90),
    _hidden_seed("Mikey Madison", "actress", 57, 58, 74.0, 82),
    _hidden_seed("Ayo Edebiri", "actress", 85, 74, 82.0, 92),
    _hidden_seed("Hunter Schafer", "actress", 67, 70, 84.0, 88),
    _hidden_seed("Jenna Ortega", "actress", 64, 69, 90.0, 86),
    _hidden_seed("Dakota Johnson", "actress", 55, 51, 84.0, 81),
    _hidden_seed("Blake Lively", "actress", 73, 64, 88.0, 84),
    _hidden_seed("Rachel McAdams", "actress", 78, 66, 86.0, 93),
    _hidden_seed("Viola Davis", "actress", 76, 54, 89.0, 98),
    _hidden_seed("Lupita Nyong'o", "actress", 82, 69, 85.0, 96),
    _hidden_seed("Emma Watson", "actress", 71, 63, 90.0, 92),
    _hidden_seed("Kristen Stewart", "actress", 49, 46, 86.0, 88),
    _hidden_seed("Rooney Mara", "actress", 42, 39, 79.0, 89),
    _hidden_seed("Mila Kunis", "actress", 64, 56, 86.0, 84),
    _hidden_seed("Jessica Chastain", "actress", 72, 53, 84.0, 94),
    _hidden_seed("Cate Blanchett", "actress", 63, 47, 90.0, 98),
    _hidden_seed("Charlize Theron", "actress", 68, 52, 91.0, 94),
    _hidden_seed("Nicole Kidman", "actress", 61, 50, 90.0, 93),
    _hidden_seed("Sandra Bullock", "actress", 75, 58, 89.0, 91),
    _hidden_seed("Salma Hayek", "actress", 70, 56, 88.0, 89),
    _hidden_seed("Gal Gadot", "actress", 69, 58, 88.0, 79),
    _hidden_seed("Hailee Steinfeld", "actress", 74, 72, 83.0, 86),
    _hidden_seed("Zoë Kravitz", "actress", 58, 59, 85.0, 87),
    _hidden_seed("Phoebe Dynevor", "actress", 66, 65, 77.0, 82),
    _hidden_seed("Phoebe Waller-Bridge", "actress", 76, 49, 80.0, 94),
    _hidden_seed("Jodie Comer", "actress", 71, 61, 82.0, 91),
    _hidden_seed("Rosamund Pike", "actress", 53, 38, 79.0, 92),
    _hidden_seed("Kerry Washington", "actress", 73, 57, 84.0, 92),
    _hidden_seed("Keke Palmer", "actress", 87, 75, 83.0, 90),
    _hidden_seed("Selena Gomez", "actress", 78, 82, 94.0, 87),
    _hidden_seed("Bella Thorne", "actress", 42, 53, 75.0, 61),
    _hidden_seed("Rachel Zegler", "actress", 59, 67, 80.0, 77),
    _hidden_seed("Millie Bobby Brown", "actress", 65, 71, 88.0, 83),
    _hidden_seed("Naomi Scott", "actress", 74, 68, 79.0, 86),
    _hidden_seed("Lily Collins", "actress", 73, 64, 81.0, 87),
    _hidden_seed("Adria Arjona", "actress", 68, 63, 77.0, 83),
]

MODEL_SEEDS: list[HiddenCharacterSeed] = [
    _hidden_seed("Gigi Hadid", "model", 77, 71, 92.0, 86),
    _hidden_seed("Bella Hadid", "model", 63, 61, 93.0, 87),
    _hidden_seed("Kendall Jenner", "model", 49, 44, 96.0, 76),
    _hidden_seed("Hailey Bieber", "model", 58, 57, 91.0, 79),
    _hidden_seed("Emily Ratajkowski", "model", 55, 60, 88.0, 78),
    _hidden_seed("Adut Akech", "model", 76, 66, 79.0, 92),
    _hidden_seed("Anok Yai", "model", 66, 59, 81.0, 90),
    _hidden_seed("Winnie Harlow", "model", 74, 63, 82.0, 88),
    _hidden_seed("Naomi Campbell", "model", 32, 26, 95.0, 97),
    _hidden_seed("Irina Shayk", "model", 57, 49, 86.0, 85),
    _hidden_seed("Cara Delevingne", "model", 69, 58, 87.0, 80),
    _hidden_seed("Kaia Gerber", "model", 71, 67, 82.0, 84),
    _hidden_seed("Rosie Huntington-Whiteley", "model", 65, 54, 84.0, 88),
    _hidden_seed("Candice Swanepoel", "model", 68, 57, 83.0, 87),
    _hidden_seed("Ashley Graham", "model", 86, 73, 84.0, 93),
    _hidden_seed("Lori Harvey", "model", 59, 55, 82.0, 79),
    _hidden_seed("Paloma Elsesser", "model", 82, 70, 78.0, 91),
    _hidden_seed("Elsa Hosk", "model", 67, 58, 80.0, 85),
    _hidden_seed("Taylor Hill", "model", 73, 64, 79.0, 86),
    _hidden_seed("Barbara Palvin", "model", 72, 69, 81.0, 84),
    _hidden_seed("Adriana Lima", "model", 61, 48, 90.0, 92),
    _hidden_seed("Joan Smalls", "model", 64, 52, 82.0, 89),
    _hidden_seed("Lais Ribeiro", "model", 71, 60, 78.0, 84),
    _hidden_seed("Jasmine Tookes", "model", 78, 68, 79.0, 88),
    _hidden_seed("Duckie Thot", "model", 74, 65, 77.0, 87),
    _hidden_seed("Precious Lee", "model", 81, 69, 76.0, 90),
    _hidden_seed("Soo Joo Park", "model", 68, 56, 75.0, 88),
    _hidden_seed("Tina Kunakey", "model", 70, 63, 76.0, 82),
    _hidden_seed("Alex Consani", "model", 84, 72, 76.0, 88),
    _hidden_seed("Amelia Gray", "model", 57, 55, 78.0, 76),
    _hidden_seed("Mona Tougaard", "model", 72, 62, 74.0, 87),
    _hidden_seed("Alek Wek", "model", 74, 55, 80.0, 95),
    _hidden_seed("Shalom Harlow", "model", 70, 50, 79.0, 94),
    _hidden_seed("Lila Moss", "model", 62, 61, 74.0, 78),
    _hidden_seed("Grace Elizabeth", "model", 69, 58, 76.0, 84),
    _hidden_seed("Saskia de Brauw", "model", 58, 47, 73.0, 89),
    _hidden_seed("Imaan Hammam", "model", 75, 64, 79.0, 90),
    _hidden_seed("Devon Aoki", "model", 61, 49, 78.0, 91),
    _hidden_seed("Tyra Banks", "model", 66, 46, 89.0, 85),
    _hidden_seed("Heidi Klum", "model", 72, 52, 88.0, 84),
    _hidden_seed("Karlie Kloss", "model", 70, 57, 85.0, 86),
    _hidden_seed("Behati Prinsloo", "model", 74, 66, 79.0, 83),
    _hidden_seed("Camila Morrone", "model", 63, 62, 77.0, 80),
    _hidden_seed("Brooks Nader", "model", 68, 59, 74.0, 76),
    _hidden_seed("Ming Xi", "model", 71, 56, 77.0, 85),
    _hidden_seed("Liu Wen", "model", 78, 61, 82.0, 94),
    _hidden_seed("Sora Choi", "model", 69, 54, 74.0, 86),
    _hidden_seed("Mayowa Nicholas", "model", 75, 65, 73.0, 87),
    _hidden_seed("Abbey Lee", "model", 59, 45, 76.0, 82),
    _hidden_seed("Jourdan Dunn", "model", 80, 67, 81.0, 89),
]

ATHLETE_SEEDS: list[HiddenCharacterSeed] = [
    _male_athlete_seed("LeBron James", 73, 62, 98.0, 97),
    _male_athlete_seed("Stephen Curry", 84, 71, 95.0, 96),
    _male_athlete_seed("Kevin Durant", 44, 39, 94.0, 88),
    _male_athlete_seed("Giannis Antetokounmpo", 86, 73, 92.0, 97),
    _male_athlete_seed("Jayson Tatum", 68, 63, 89.0, 88),
    _male_athlete_seed("Luka Doncic", 61, 57, 91.0, 88),
    _male_athlete_seed("Nikola Jokic", 58, 51, 90.0, 96),
    _male_athlete_seed("Shai Gilgeous-Alexander", 72, 68, 88.0, 90),
    _male_athlete_seed("Ja Morant", 47, 51, 89.0, 68),
    _male_athlete_seed("Devin Booker", 64, 59, 87.0, 85),
    _male_athlete_seed("Patrick Mahomes", 78, 68, 96.0, 95),
    _male_athlete_seed("Joe Burrow", 71, 61, 88.0, 90),
    _male_athlete_seed("Lamar Jackson", 73, 60, 89.0, 93),
    _male_athlete_seed("Josh Allen", 69, 58, 88.0, 89),
    _male_athlete_seed("Aaron Judge", 66, 52, 87.0, 91),
    _male_athlete_seed("Shohei Ohtani", 74, 59, 97.0, 98),
    _male_athlete_seed("Mookie Betts", 79, 64, 86.0, 93),
    _male_athlete_seed("Bryce Harper", 57, 49, 85.0, 88),
    _male_athlete_seed("Novak Djokovic", 41, 33, 93.0, 95),
    _male_athlete_seed("Carlos Alcaraz", 77, 71, 89.0, 93),
    _male_athlete_seed("Jannik Sinner", 68, 58, 86.0, 92),
    _male_athlete_seed("Rafael Nadal", 82, 60, 94.0, 99),
    _female_athlete_seed("Iga Swiatek", 65, 57, 85.0, 95),
    _female_athlete_seed("Coco Gauff", 84, 76, 88.0, 94),
    _female_athlete_seed("Aryna Sabalenka", 59, 52, 83.0, 88),
    _female_athlete_seed("Simone Biles", 81, 67, 92.0, 99),
    _female_athlete_seed("Naomi Osaka", 76, 69, 90.0, 95),
    _male_athlete_seed("Lewis Hamilton", 72, 56, 94.0, 97),
    _male_athlete_seed("Max Verstappen", 33, 28, 92.0, 90),
    _male_athlete_seed("Lando Norris", 78, 65, 87.0, 89),
    _male_athlete_seed("George Russell", 67, 55, 82.0, 86),
    _male_athlete_seed("Kylian Mbappe", 62, 60, 96.0, 92),
    _male_athlete_seed("Erling Haaland", 58, 48, 92.0, 90),
    _male_athlete_seed("Jude Bellingham", 73, 66, 91.0, 91),
    _male_athlete_seed("Lionel Messi", 67, 53, 99.0, 99),
    _male_athlete_seed("Cristiano Ronaldo", 39, 37, 99.0, 93),
    _male_athlete_seed("Vinicius Junior", 61, 55, 90.0, 85),
    _male_athlete_seed("Mohamed Salah", 77, 58, 91.0, 96),
    _male_athlete_seed("Bukayo Saka", 86, 74, 87.0, 94),
    _male_athlete_seed("Travis Kelce", 79, 73, 94.0, 88),
    _male_athlete_seed("Jalen Hurts", 74, 58, 86.0, 92),
    _male_athlete_seed("C.J. Stroud", 71, 60, 81.0, 89),
    _female_athlete_seed("A'ja Wilson", 83, 70, 84.0, 96),
    _female_athlete_seed("Caitlin Clark", 69, 61, 90.0, 91),
    _female_athlete_seed("Angel Reese", 58, 57, 88.0, 83),
    _female_athlete_seed("Serena Williams", 80, 63, 97.0, 99),
    _female_athlete_seed("Megan Rapinoe", 74, 54, 86.0, 95),
    _female_athlete_seed("Alex Morgan", 78, 66, 87.0, 93),
    _male_athlete_seed("Usain Bolt", 82, 59, 93.0, 98),
    _male_athlete_seed("Noah Lyles", 64, 56, 84.0, 86),
]


HIDDEN_CHARACTER_SEEDS: list[HiddenCharacterSeed] = [
    *ACTOR_SEEDS,
    *ACTRESS_SEEDS,
    *MODEL_SEEDS,
    *ATHLETE_SEEDS,
]

HIDDEN_CHARACTERS_BY_CATEGORY: dict[str, list[HiddenCharacterSeed]] = {
    "actor": ACTOR_SEEDS,
    "actress": ACTRESS_SEEDS,
    "model": MODEL_SEEDS,
    "athlete": ATHLETE_SEEDS,
}

HIDDEN_CHARACTER_BY_NAME: dict[str, HiddenCharacterSeed] = {
    seed.name: seed for seed in HIDDEN_CHARACTER_SEEDS
}

HIDDEN_CHARACTER_LOVINGNESS: dict[str, int] = {
    seed.name: int(seed.lovingness) for seed in HIDDEN_CHARACTER_SEEDS
}

HIDDEN_CHARACTER_POPULARITY: dict[str, float] = {
    seed.name: float(seed.popularity) for seed in HIDDEN_CHARACTER_SEEDS
}

HIDDEN_CHARACTER_REPUTATION: dict[str, int] = {
    seed.name: int(seed.reputation) for seed in HIDDEN_CHARACTER_SEEDS
}

HIDDEN_CHARACTER_ROMANCE_PREFERENCES: dict[str, str] = {
    seed.name: str(seed.romance_preference or "prefers_female")
    for seed in HIDDEN_CHARACTER_SEEDS
}
