"""Name generation helpers for the standalone artist ecosystem simulator."""

import random

GENRE_WORDS = {
    "hip hop": ["Block", "Cipher", "Pressure", "Chrome", "Corner", "Legacy", "Keys", "Concrete"],
    "pop": ["Neon", "Summer", "Mirror", "Flash", "Heartbeat", "Glow", "Fever", "Daydream"],
    "rock": ["Static", "Thunder", "Wire", "Ashes", "Machine", "Voltage", "Basement", "Aftershock"],
    "jazz": ["Blue", "Smoke", "Velvet", "Afterhours", "Lantern", "Suite", "Moon", "Keys"],
    "classical": ["Elegy", "Sonata", "Cathedral", "Nocturne", "Chamber", "Prelude", "Swan", "Requiem"],
    "electronic": ["Signal", "Pulse", "Circuit", "Frequency", "Afterimage", "Neon", "Grid", "Voltage"],
    "r&b": ["Silk", "Velvet", "Afterglow", "Room", "Rain", "Touch", "Satin", "Halo"],
    "metal": ["Iron", "Blood", "Wound", "Ritual", "Crown", "Collapse", "Grave", "Furnace"],
    "country": ["Highway", "Porch", "Dust", "Whiskey", "River", "County", "Lantern", "Backroad"],
    "reggae": ["Island", "Sunrise", "Kingston", "Roots", "Drift", "Palm", "Dub", "Harbor"],
    "folk": ["Cabin", "Winter", "Field", "Letter", "River", "Lantern", "Hollow", "Birdsong"],
    "blues": ["Crossroad", "Midnight", "Bottle", "Rain", "Delta", "Hollow", "Train", "Mercy"],
    "punk": ["Riot", "Basement", "Static", "Crash", "Youth", "Spit", "Poster", "Noise"],
    "soul": ["Grace", "Sunday", "Gold", "Mercy", "Choir", "Flame", "Bloom", "Sanctuary"],
    "experimental": ["Fragment", "Static", "Dream", "Glass", "Labyrinth", "Void", "Cipher", "Artifact"],
}

THEME_WORDS = {
    "heartbreak": ["Aftertaste", "Goodbye", "Distance", "Cold Room", "Last Call", "Bruise"],
    "party": ["Red Cups", "Night Drive", "House Lights", "Backseat", "Champagne", "Afterparty"],
    "protest": ["Sirens", "No Peace", "Burning Signs", "Flag", "March", "Witness"],
    "nostalgia": ["Old Photos", "Memory Lane", "Home Video", "August", "Polaroid", "Yesterday"],
    "love": ["Stay", "Wildflower", "Your Name", "Slow Dance", "Promise", "Honey"],
    "existential": ["Why Am I Here", "Exit Sign", "Bad Dream", "Void", "Questions", "Awake"],
    "street life": ["Corner Store", "Late Rent", "Blue Lights", "Back Block", "Ten Toes", "No Witness"],
    "spirituality": ["Pray For Me", "Halo", "Psalm", "Holy Water", "Angels", "Grace"],
    "rage": ["Crash Out", "No Mercy", "Black Smoke", "Teeth", "Pressure", "Break Something"],
    "euphoria": ["Skyline", "Levitate", "Glow Up", "First Light", "No Ceiling", "Floating"],
}

ALBUM_STRUCTURES = [
    "{genre} {theme}",
    "{theme} In {genre}",
    "The {genre} {theme}",
    "{theme}: A {genre} Story",
    "{genre} Season",
    "{theme} Language",
]

EP_STRUCTURES = [
    "{theme} EP",
    "{genre} Sketches",
    "{theme} Sessions",
    "{genre} Pack",
    "{theme} Hours",
]

MIXTAPE_STRUCTURES = [
    "{genre} Tape",
    "{theme} Files",
    "{genre} Vol. {number}",
    "{theme} Demo Pack",
    "{genre} Bootleg",
]

SINGLE_STRUCTURES = [
    "{theme}",
    "{genre} {theme}",
    "{theme} Tonight",
    "{genre} Dreams",
    "{theme} / {genre}",
]


def _word(pool, fallback):
    if pool:
        return random.choice(pool)
    return fallback


def _number():
    return random.choice(["1", "2", "3", "4", "5"])


def generate_release_name(release_type, genre=None, theme=None):
    genre_word = _word(GENRE_WORDS.get(genre, []), "Neon")
    theme_word = _word(THEME_WORDS.get(theme, []), "Dream")

    if release_type == "single":
        structure = random.choice(SINGLE_STRUCTURES)
    elif release_type == "ep":
        structure = random.choice(EP_STRUCTURES)
    elif release_type == "mixtape":
        structure = random.choice(MIXTAPE_STRUCTURES)
    else:
        structure = random.choice(ALBUM_STRUCTURES)

    return structure.format(
        genre=genre_word,
        theme=theme_word,
        number=_number(),
    )


def generate_song_name(genre=None, theme=None):
    return generate_release_name("single", genre=genre, theme=theme)


def generate_album_name(genre=None, theme=None):
    return generate_release_name("album", genre=genre, theme=theme)


def generate_ep_name(genre=None, theme=None):
    return generate_release_name("ep", genre=genre, theme=theme)


def generate_mixtape_name(genre=None, theme=None):
    return generate_release_name("mixtape", genre=genre, theme=theme)

