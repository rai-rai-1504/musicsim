import random

# --- Data Models ---

class Song:
    def __init__(self, quality, name=None, genre=None, theme=None, duration=None):
        self.quality = quality  # 1-10
        self.name = name
        self.genre = genre
        self.theme = theme
        self.duration = duration  # seconds


# --- Helper Text System ---

def pick(options):
    return random.choice(options)


def duration_comment(duration):
    short_opts = [
        "it feels far too brief to establish any real identity or leave a lasting impression",
        "it wraps up so quickly that the ideas barely have time to breathe",
        "it ends abruptly, cutting off what could have developed into something meaningful",
        "its short runtime makes the experience feel incomplete and somewhat rushed",
        "it comes and goes before any real momentum is built",
        "it feels like a sketch rather than a fully realized piece",
        "it lacks the time needed to properly explore its own ideas",
        "it feels more like a teaser than a finished product",
        "it closes just as it starts to get interesting",
        "it leaves behind a sense of something unfinished",
        "it barely scratches the surface before ending",
        "it feels compressed and underdeveloped due to its length",
        "it struggles to make an impact within such a short span",
        "it feels like it needed at least another minute to work",
        "it comes off as rushed rather than concise",
        "it doesn’t give its themes enough room to resonate",
        "it feels clipped and prematurely concluded",
        "it ends before any emotional payoff is reached",
        "it feels like an idea cut short rather than completed",
        "it leaves more questions than satisfaction due to its brevity",
    ]

    long_opts = [
        "it stretches on longer than necessary, diluting its strongest moments",
        "it feels bloated, with ideas that repeat without adding much value",
        "it struggles to justify its extended runtime",
        "it becomes exhausting by the time it reaches its conclusion",
        "it drags, losing focus as it progresses",
        "it feels padded rather than purposeful in its length",
        "it overstays its welcome without offering enough variation",
        "it feels unnecessarily extended beyond its core idea",
        "it begins to feel repetitive midway through",
        "it lacks the dynamism needed to sustain such length",
        "it feels like it could have been tighter and more impactful",
        "it meanders instead of progressing meaningfully",
        "it feels indulgent rather than engaging",
        "it becomes tiring before it becomes rewarding",
        "it struggles to maintain interest throughout",
        "it feels stretched thin over too much time",
        "it doesn’t evolve enough to justify its duration",
        "it feels overextended without strong payoff",
        "it lingers without building toward anything substantial",
        "it could benefit greatly from trimming down",
    ]

    mid_opts = [
        "the runtime feels well-balanced, allowing ideas to develop naturally",
        "it maintains a comfortable length without overstaying its welcome",
        "it finds a good middle ground between brevity and depth",
        "it feels appropriately timed for what it aims to do",
        "it flows well within its duration without feeling rushed or dragged",
        "it uses its runtime efficiently",
        "it feels complete without being excessive",
        "it holds attention consistently from start to finish",
        "it strikes a solid balance in pacing",
        "it feels neither too short nor unnecessarily long",
        "it allows its themes enough space to land",
        "it keeps things engaging throughout its runtime",
        "it avoids both rushing and dragging",
        "it feels structurally sound in its timing",
        "it delivers its ideas within a satisfying length",
        "it maintains momentum across its duration",
        "it feels tightly constructed and well-paced",
        "it offers just enough time for immersion",
        "it avoids filler while still feeling complete",
        "it feels measured and deliberate in length",
    ]

    if duration < 120:
        return pick(short_opts)
    elif duration > 300:
        return pick(long_opts)
    else:
        return pick(mid_opts)


def genre_comment(genre):
    pools = {
        "pop": [
            "as a pop track, it leans heavily into familiar structures, for better or worse",
            "within the pop space, it attempts to balance accessibility with identity",
            "as a pop offering, it plays things relatively safe",
            "in the context of pop, it feels somewhat formulaic",
            "as a pop track, it prioritizes catchiness over depth",
            "within pop conventions, it feels predictable",
            "as a pop record, it focuses on immediate appeal",
            "it sits comfortably within modern pop sensibilities",
            "as a pop track, it rarely takes risks",
            "within the pop genre, it feels commercially inclined",
            "as a pop entry, it aims for broad appeal",
            "it reflects many of the clichés of contemporary pop",
            "as a pop piece, it feels polished but safe",
            "within pop, it struggles to stand out",
            "as a pop track, it relies on familiar hooks",
            "it feels like a textbook pop structure",
            "as a pop release, it emphasizes simplicity",
            "within the genre, it feels somewhat interchangeable",
            "as a pop song, it leans into accessibility",
            "it aligns closely with mainstream pop expectations",
        ],
        "hip hop": [
            "as a hip hop track, it shows varying levels of lyrical and sonic intent",
            "within hip hop, it attempts to balance flow and production",
            "as a hip hop piece, it leans more on vibe than substance",
            "within the hip hop space, it feels somewhat inconsistent",
            "as a hip hop track, it tries to assert identity",
            "it reflects elements of modern hip hop trends",
            "as a hip hop record, it varies in execution",
            "within hip hop, it feels uneven at times",
            "as a hip hop entry, it lacks strong distinction",
            "it shows glimpses of creativity within hip hop",
            "as a hip hop track, it leans into rhythm over message",
            "within the genre, it feels somewhat derivative",
            "as a hip hop release, it plays with familiar motifs",
            "it fits within current hip hop aesthetics",
            "as a hip hop track, it struggles to fully commit",
            "within hip hop, it shows moderate ambition",
            "as a hip hop piece, it feels partially realized",
            "it attempts to align with contemporary hip hop sounds",
            "as a hip hop offering, it lacks consistency",
            "within hip hop, it delivers mixed results",
        ],
        "rock": [
            "as a rock track, it carries a certain raw energy",
            "within rock, it leans into its instrumental presence",
            "as a rock piece, it emphasizes intensity",
            "within the rock genre, it feels somewhat traditional",
            "as a rock track, it attempts to channel authenticity",
            "it reflects classic rock influences",
            "as a rock record, it focuses on grit and texture",
            "within rock, it feels grounded but not innovative",
            "as a rock entry, it plays within known boundaries",
            "it captures some of the spirit of rock",
            "as a rock track, it leans into its energy",
            "within rock, it feels somewhat safe",
            "as a rock piece, it shows moderate intensity",
            "it aligns with familiar rock structures",
            "as a rock release, it lacks bold experimentation",
            "within rock, it feels somewhat restrained",
            "as a rock track, it delivers in parts",
            "it captures moments of genuine rock appeal",
            "as a rock offering, it feels uneven",
            "within the genre, it delivers a mixed experience",
        ]
    }
    return pick(pools.get(genre, ["it sits somewhat ambiguously within its genre"]))


def theme_comment(theme):
    pools = {
        "deep": [
            "the deeper themes attempt to add emotional weight",
            "it tries to explore more introspective territory",
            "the thematic direction leans toward seriousness",
            "it attempts emotional resonance with varying success",
            "the deeper intent is evident but not always effective",
            "it reaches for emotional depth",
            "the thematic core feels somewhat introspective",
            "it gestures toward meaningful expression",
            "the depth feels unevenly executed",
            "it attempts to be reflective",
            "the emotional angle is present but inconsistent",
            "it aims for substance over surface",
            "the depth is noticeable but not fully realized",
            "it tries to engage on a deeper level",
            "the theme carries some weight",
            "it leans into introspection",
            "the emotional tone fluctuates",
            "it attempts seriousness",
            "the depth feels partially convincing",
            "it strives for emotional impact",
        ],
        "party": [
            "the party theme focuses heavily on energy and vibe",
            "it prioritizes fun over depth",
            "the theme leans into carefree expression",
            "it embraces a celebratory tone",
            "the focus is clearly on entertainment",
            "it aims to be lively and engaging",
            "the party angle is front and center",
            "it thrives on high energy",
            "the theme feels straightforward",
            "it pushes for immediate enjoyment",
            "the tone is unapologetically fun",
            "it leans into surface-level appeal",
            "the party aspect is consistent",
            "it focuses on rhythm and vibe",
            "the theme is simple but effective",
            "it emphasizes enjoyment over meaning",
            "the energy is sustained throughout",
            "it avoids complexity intentionally",
            "the theme is clear and direct",
            "it aims purely for engagement",
        ],
        "happy": [
            "the happy tone brings a lighter atmosphere",
            "it leans into positivity",
            "the theme emphasizes brightness",
            "it carries an uplifting feel",
            "the tone is optimistic throughout",
            "it focuses on feel-good elements",
            "the theme adds a sense of warmth",
            "it maintains a cheerful direction",
            "the mood remains consistently light",
            "it aims to uplift",
            "the tone is pleasant and easygoing",
            "it leans into simplicity",
            "the happiness feels genuine at times",
            "it creates a light listening experience",
            "the mood is steady",
            "it prioritizes positivity",
            "the tone feels accessible",
            "it avoids darker elements",
            "the theme is straightforward",
            "it maintains a bright outlook",
        ]
    }
    return pick(pools.get(theme, ["the theme feels somewhat unclear"]))


def score_comment(score):
    low = [
        "ultimately coming across as a disappointing and underwhelming effort",
        "failing to leave any significant impression",
        "ending up as a forgettable addition",
        "falling short on most fronts",
        "struggling to justify its own existence",
        "feeling largely uninspired",
        "lacking any real standout quality",
        "coming off as poorly executed",
        "failing to deliver on its premise",
        "feeling directionless overall",
        "lacking cohesion and purpose",
        "coming across as half-baked",
        "missing the mark almost entirely",
        "offering little of value",
        "failing to engage meaningfully",
        "feeling like a misstep",
        "lacking conviction",
        "falling flat in execution",
        "feeling uninspired throughout",
        "not offering much to return to",
    ]

    mid = [
        "resulting in a fairly average and inconsistent track",
        "ending up as a mixed but listenable effort",
        "coming across as decent but flawed",
        "offering some value despite its issues",
        "delivering a passable experience",
        "showing potential but lacking refinement",
        "feeling somewhat uneven overall",
        "landing somewhere in the middle",
        "offering moments of quality",
        "being serviceable but not memorable",
        "providing a moderately engaging listen",
        "working in parts but not as a whole",
        "delivering a safe but unremarkable result",
        "feeling acceptable yet unexciting",
        "showing glimpses of strength",
        "being competent but not standout",
        "holding together without excelling",
        "remaining fairly standard",
        "offering limited replay value",
        "feeling okay but not compelling",
    ]

    high = [
        "coming together as a strong and engaging track",
        "resulting in a compelling listening experience",
        "standing out as a well-executed piece",
        "delivering a memorable performance",
        "showing clear artistic intent",
        "offering a satisfying experience",
        "feeling cohesive and confident",
        "presenting a polished outcome",
        "leaving a positive impression",
        "working effectively as a whole",
        "showing consistency throughout",
        "offering strong replay value",
        "delivering on its ideas",
        "feeling well-realized",
        "standing above average",
        "showing notable quality",
        "feeling refined",
        "maintaining engagement",
        "presenting a clear vision",
        "coming across as impactful",
    ]

    top = [
        "emerging as an exceptional and standout release",
        "feeling like one of the stronger outputs in recent memory",
        "delivering an outstanding and memorable experience",
        "standing out with remarkable execution",
        "showcasing a high level of artistry",
        "leaving a lasting impression",
        "feeling near flawless in execution",
        "demonstrating exceptional cohesion",
        "offering a truly compelling listen",
        "standing out prominently",
        "delivering a highly refined piece",
        "showing remarkable consistency",
        "feeling fully realized",
        "presenting a strong artistic statement",
        "achieving a high level of impact",
        "feeling complete and confident",
        "offering exceptional replay value",
        "standing among the best",
        "delivering excellence across the board",
        "showing top-tier execution",
    ]

    if score <= 3:
        return pick(low)
    elif score <= 6:
        return pick(mid)
    elif score <= 8:
        return pick(high)
    else:
        return pick(top)


# --- Critics ---

class Critic:
    def __init__(self, name):
        self.name = name

    def review(self, song):
        raise NotImplementedError

    def generate_review_text(self, song, score):
        g = genre_comment(song.genre)
        t = theme_comment(song.theme)
        d = duration_comment(song.duration)
        s = score_comment(score)

        paragraph = (
            f"From a structural standpoint, {g}, and this plays a significant role in shaping how the track is perceived overall. "
            f"At the same time, {t}, which adds another layer to the listening experience, though not always with complete consistency. "
            f"In terms of pacing and runtime, {d}, which directly impacts how engaging the track remains from start to finish. "
            f"Taking everything into account, the song \"{song.name}\" ends up {s}, hence a score of {score}/10 is what I'll give."
        )

        return paragraph


class HarshCritic(Critic):
    def review(self, song):
        score = song.quality

        if song.genre == "rock":
            score += 1
        if song.genre == "pop":
            score -= 2

        if song.theme == "deep":
            score += 1
        if song.theme == "party":
            score -= 1

        if song.duration < 120:
            score -= 2

        score -= 2

        score = max(0, min(10, round(score, 1)))
        return score, self.generate_review_text(song, score)


class GenuineCritic(Critic):
    def review(self, song):
        score = round(song.quality, 1)
        return score, self.generate_review_text(song, score)


class LenientCritic(Critic):
    def review(self, song):
        score = song.quality

        if song.duration > 300:
            score -= 2

        if song.genre == "pop" and song.theme == "party":
            score += 3

        score += 1

        score = max(0, min(10, round(score, 1)))
        return score, self.generate_review_text(song, score)


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
            pass
        print("Invalid duration. Try again.")


def main():
    sim = Simulation()

    while True:
        cmd = input("\nPress 'c' to create a song (or 'q' to quit): ").lower()

        if cmd == 'q':
            break

        if cmd != 'c':
            continue

        while True:
            quality = random.randint(1, 10)
            print(f"Created a song with quality {quality}")

            choice = input("Press 1 to delete, 2 to publish: ")

            if choice == '1':
                continue

            if choice == '2':
                name = input("Song name: ")

                genre = get_choice(
                    "Select genre:",
                    {'1': 'pop', '2': 'hip hop', '3': 'rock'}
                )

                theme = get_choice(
                    "Select theme:",
                    {'1': 'deep', '2': 'party', '3': 'happy'}
                )

                print("Enter duration:")
                duration = parse_duration()

                song = Song(quality, name, genre, theme, duration)
                sim.publish_song(song)
                break


if __name__ == "__main__":
    main()
