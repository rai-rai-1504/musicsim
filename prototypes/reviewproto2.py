import random

# --- Data Models ---

class Song:
    def __init__(self, quality, name=None, genre=None, theme=None, duration=None):
        self.quality = quality
        self.name = name
        self.genre = genre
        self.theme = theme
        self.duration = duration


# --- Helpers ---

def pick(options):
    return random.choice(options)


def shuffle_sentences(sentences):
    random.shuffle(sentences)
    return " ".join(sentences)


# --- Critics ---

class Critic:
    def __init__(self, name):
        self.name = name

    def review(self, song):
        raise NotImplementedError


# --- HARSH CRITIC ---

class HarshCritic(Critic):

    def genre_line(self, song):
        if song.genre == "pop":
            return pick([
                "this leans into generic pop tropes without offering anything new",
                "as a pop track, it feels painfully predictable",
                "it follows the most uninspired version of pop structure",
            ])
        if song.genre == "rock":
            return pick([
                "at least the rock elements bring some rawness",
                "the rock direction gives it some edge",
            ])
        return pick([
            "it doesn’t strongly establish its genre identity",
        ])

    def theme_line(self, song):
        if song.theme == "party":
            return pick([
                "the party theme comes off as shallow and repetitive",
                "it relies too much on empty energy",
            ])
        if song.theme == "deep":
            return pick([
                "the attempt at depth is one of the few redeeming aspects",
                "there’s at least some effort toward substance",
            ])
        return pick([
            "the theme doesn’t leave much of an impact",
        ])

    def duration_line(self, song):
        if song.duration > 300:
            return pick([
                "its longer runtime actually helps it breathe a little",
                "the extended length is one of the few things working in its favor",
            ])
        if song.duration < 160:
            return pick([
                "it’s over before it even starts, which doesn’t help",
                "the short length makes it feel even more underdeveloped",
            ])
        return pick([
            "the runtime is neither helping nor saving it",
        ])

    def verdict(self, score):
        if score <= 3:
            return "a weak and largely forgettable effort"
        elif score <= 6:
            return "a flawed and inconsistent track"
        else:
            return "decent in parts but still held back by major issues"

    def review(self, song):
        score = song.quality

        if song.genre == "rock": score += 1
        if song.genre == "pop": score -= 2
        if song.theme == "deep": score += 1
        if song.theme == "party": score -= 2
        if song.duration < 120: score -= 2

        score -= 2
        score = max(0, min(10, round(score, 1)))

        sentences = [
            self.genre_line(song),
            self.theme_line(song),
            self.duration_line(song),
            f"overall, this is {self.verdict(score)}, so I’m giving it a {score}/10"
        ]

        return score, shuffle_sentences(sentences)


# --- GENUINE CRITIC ---

class GenuineCritic(Critic):

    def review(self, song):
        score = round(song.quality, 1)

        sentences = [
            pick([
                f"as a {song.genre} track, it delivers a fairly balanced experience",
                f"within the {song.genre} space, it feels reasonably put together",
            ]),
            pick([
                f"the {song.theme} theme comes through with moderate clarity",
                f"the thematic direction is present but not always consistent",
            ]),
            pick([
                "the duration feels appropriate for what it tries to achieve",
                "the runtime is handled in a fairly standard way",
            ]),
            pick([
                f"overall, '{song.name}' is a measured effort, and I’d rate it {score}/10",
                f"taking everything into account, this lands at {score}/10",
            ])
        ]

        return score, shuffle_sentences(sentences)


# --- LENIENT CRITIC ---

class LenientCritic(Critic):

    def genre_line(self, song):
        if song.genre == "pop":
            return pick([
                "this pop direction makes it immediately enjoyable",
                "as a pop track, it’s quite catchy",
            ])
        return pick([
            "it has a pleasant overall sound",
        ])

    def theme_line(self, song):
        if song.theme == "party":
            return pick([
                "the party vibe really adds to its appeal",
                "it’s fun and energetic throughout",
            ])
        return pick([
            "the theme adds a nice touch",
        ])

    def duration_line(self, song):
        if song.duration > 240:
            return pick([
                "it does feel a bit too long at times",
                "it could have been slightly shorter",
            ])
        return pick([
            "the runtime works quite well",
        ])

    def verdict(self, score):
        if score <= 3:
            return "not the best, but still has some charm"
        elif score <= 6:
            return "a decent and enjoyable track"
        else:
            return "a really enjoyable and well-done track"

    def review(self, song):
        score = song.quality

        if song.duration > 300: score -= 2
        if song.genre == "pop" and song.theme == "party": score += 3

        score += 1
        score = max(0, min(10, round(score, 1)))

        sentences = [
            self.genre_line(song),
            self.theme_line(song),
            self.duration_line(song),
            f"overall, '{song.name}' is {self.verdict(score)}, so I’d give it a {score}/10"
        ]

        return score, shuffle_sentences(sentences)


# --- Simulation ---

class Simulation:
    def __init__(self):
        self.critics = [
            HarshCritic("Harsh"),
            GenuineCritic("Genuine"),
            LenientCritic("Lenient")
        ]

    def publish_song(self, song):
        print(f"\n--- Reviews for '{song.name}' ---")
        for critic in self.critics:
            score, text = critic.review(song)
            print(f"\n{critic.name}:\n{text}\n")


# --- CLI ---

def get_choice(prompt, options):
    while True:
        print(prompt)
        for key, val in options.items():
            print(f"{key}. {val}")
        choice = input("Choose: ")
        if choice in options:
            return options[choice]
        print("Invalid choice. Try again.")


def parse_duration():
    while True:
        try:
            mins = int(input("Minutes: "))
            secs = int(input("Seconds: "))
            if 0 <= secs < 60:
                return mins * 60 + secs
        except:
            print("Invalid duration. Try again.")


def main():
    sim = Simulation()

    while True:
        cmd = input("\nPress 'c' to create a song (or 'q' to quit): ").lower()

        if cmd == 'q': break
        if cmd != 'c': continue

        while True:
            quality = random.randint(1, 10)
            print(f"Created a song with quality {quality}")

            choice = input("Press 1 to delete, 2 to publish: ")

            if choice == '1': continue

            if choice == '2':
                name = input("Song name: ")

                genre = get_choice("Select genre:", {'1': 'pop', '2': 'hip hop', '3': 'rock'})
                theme = get_choice("Select theme:", {'1': 'deep', '2': 'party', '3': 'happy'})

                print("Enter duration:")
                duration = parse_duration()

                song = Song(quality, name, genre, theme, duration)
                sim.publish_song(song)
                break


if __name__ == "__main__":
    main()
