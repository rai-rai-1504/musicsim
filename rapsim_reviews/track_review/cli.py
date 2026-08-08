"""CLI and simulation helpers for track reviews."""

from .base import *
from .critics import *

class Simulation:
    def __init__(self):
        self.critics = [
            MarcusVane(),
            DejaHayes(),
            VicOsei(),
            RayColdwell(),
            EarlMosely(),
            ZaraNights(),
            TobiasLund(),
            NinaPascal(),
            TeenaNaruka(),
            ShatamRai(),
        ]

    def publish_song(self, song):
        print()
        print("╔" + "═" * 62 + "╗")
        label = f"  REVIEWS: '{song.name}'  "
        print("║" + label.center(62) + "║")
        meta  = f"Genre: {song.genre_label()}  |  Theme: {song.theme}  |  {fmt_duration(song.duration)}"
        print("║" + meta.center(62) + "║")
        print("╚" + "═" * 62 + "╝")

        scores = []
        for critic in self.critics:
            score, text = critic.review(song)
            scores.append(score)
            print()
            print(f"  ★  {critic.name}  [{critic.tagline}]")
            print(f"  {'─' * 58}")
            words = text.split()
            line  = "  "
            for word in words:
                if len(line) + len(word) + 1 > 74:
                    print(line)
                    line = "  " + word + " "
                else:
                    line += word + " "
            if line.strip():
                print(line)
            print()

        avg = round(sum(scores) / len(scores), 1)
        print("╔" + "═" * 62 + "╗")
        print("║" + f"  AVERAGE CRITICAL SCORE:  {avg} / 10  ".center(62) + "║")
        if avg >= 9.5:   tag = "★  UNIVERSAL ACCLAIM  ★"
        elif avg >= 8.0: tag = "GENERALLY ACCLAIMED"
        elif avg >= 6.5: tag = "GENERALLY FAVOURABLE"
        elif avg >= 5.0: tag = "MIXED REVIEWS"
        elif avg >= 3.0: tag = "GENERALLY UNFAVOURABLE"
        else:            tag = "OVERWHELMING DISLIKE"
        print("║" + f"  {tag}  ".center(62) + "║")
        print("╚" + "═" * 62 + "╝")
        return {"scores": scores, "average": avg}


def fmt_duration(secs):
    return f"{secs // 60}:{secs % 60:02d}"


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

def banner():
    print()
    print("╔" + "═" * 62 + "╗")
    print("║" + "  🎵  MUSIC CAREER SIMULATOR  —  REVIEW ENGINE  🎵  ".center(62) + "║")
    print("╚" + "═" * 62 + "╝")
    print()


def get_choice(prompt, options):
    while True:
        print(f"\n  {prompt}")
        for key, val in options.items():
            print(f"    [{key}]  {val}")
        choice = input("  ›› ").strip()
        if choice in options:
            return options[choice]
        print("  ✗  Invalid choice — try again.")


def parse_duration():
    while True:
        try:
            mins = int(input("  Minutes: "))
            secs = int(input("  Seconds: "))
            if 0 <= secs < 60 and mins >= 0:
                return mins * 60 + secs
        except (ValueError, TypeError):
            pass
        print("  ✗  Invalid duration — try again.")


def select_genres():
    print("\n  ┌─────────────────────────────────────────┐")
    print("  │           SELECT GENRE(S)               │")
    print("  └─────────────────────────────────────────┘")
    genre_map = {str(i + 1): g for i, g in enumerate(GENRES)}
    for key, val in genre_map.items():
        print(f"    [{key:>2}]  {val}")
    while True:
        raw   = input("  ›› Pick 1 or 2 genre numbers (e.g. '1' or '3 7'): ").strip()
        parts = raw.split()
        if len(parts) == 1 and parts[0] in genre_map:
            return [genre_map[parts[0]]]
        if len(parts) == 2 and parts[0] in genre_map and parts[1] in genre_map and parts[0] != parts[1]:
            return [genre_map[parts[0]], genre_map[parts[1]]]
        print("  ✗  Pick 1 or 2 valid different genre numbers.")


def select_theme():
    theme_map = {str(i + 1): t for i, t in enumerate(THEMES)}
    return get_choice("SELECT THEME:", theme_map)


def main():
    banner()
    sim = Simulation()

    while True:
        print()
        cmd = input("  Press [C] to create a song  |  [Q] to quit  ›› ").strip().lower()
        if cmd == 'q':
            print("\n  See you on the charts.\n")
            break
        if cmd != 'c':
            continue

        while True:
            quality = random.randint(1, 10)
            print()
            print(f"  ┌──────────────────────────────────────┐")
            print(f"  │   Song generated  —  Quality: {quality}/10    │")
            print(f"  └──────────────────────────────────────┘")
            print(f"    [1]  Scrap it and re-roll")
            print(f"    [2]  Publish this one")
            act = input("  ›› ").strip()

            if act == '1':
                continue

            if act == '2':
                print()
                name     = input("  Song name: ").strip() or "Untitled"
                genres   = select_genres()
                theme    = select_theme()
                print("\n  ┌────────────────────────────────────┐")
                print("  │           SONG DURATION            │")
                print("  └────────────────────────────────────┘")
                duration = parse_duration()
                song     = Song(quality, name, genres, theme, duration)
                sim.publish_song(song)
                break
