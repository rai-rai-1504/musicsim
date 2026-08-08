"""CLI and simulation helpers for album reviews."""

from .base import *
from .critics import *

class AlbumSimulation:
    def __init__(self):
        song_critics = [
            MarcusVane(), DejaHayes(), VicOsei(), RayColdwell(),
            EarlMosely(), ZaraNights(), TobiasLund(), NinaPascal(),
            TeenaNaruka(), ShatamRai(),
        ]
        album_wrappers = [
            AlbumMarcusVane, AlbumDejaHayes, AlbumVicOsei, AlbumRayColdwell,
            AlbumEarlMosely, AlbumZaraNights, AlbumTobiasLund, AlbumNinaPascal,
            AlbumTeenaNaruka, AlbumShatamRai,
        ]
        self.album_critics = [
            wrapper(song_critic)
            for wrapper, song_critic in zip(album_wrappers, song_critics)
        ]

    def publish_album(self, album):
        _print_box(f"  ALBUM REVIEWS: '{album.name}'  ")
        meta = (f"{album.song_count()} tracks  |  "
                f"{fmt_duration(album.total_duration())}")
        print(f"  {meta}")
        _print_separator()
        print()

        # Tracklist preview
        print("  ┌─  TRACKLIST  ─────────────────────────────────────────────")
        for i, s in enumerate(album.songs, 1):
            gl = s.genre_label()
            print(f"  │  {i:>2}. {s.name:<28}  {gl:<22}  {fmt_duration(s.duration)}")
        print("  └────────────────────────────────────────────────────────────")
        print()

        all_album_scores            = []
        all_track_scores_by_critic  = []

        for ac in self.album_critics:
            album_score, song_scores, review_text = ac.write_review(album)
            all_album_scores.append(album_score)
            all_track_scores_by_critic.append((ac, album_score, song_scores))

            print(f"  ★  {ac.name}  [{ac.tagline}]")
            print(f"  {'─' * 60}")
            _wrap_print(review_text)
            print()
            print("  Track Ratings:")
            for song, sc in zip(album.songs, song_scores):
                bar = _score_bar(sc)
                print(f"    {song.name:<30}  {sc:>4}/10  {bar}")
            print(f"  Album Score: {album_score}/10")
            print()

        # Aggregate
        avg = round(sum(all_album_scores) / len(all_album_scores), 1)
        _print_box(f"  ALBUM: '{album.name}'  |  AVG CRITICAL SCORE: {avg}/10  ")

        if avg >= 9.5:   tag = "★  UNIVERSAL ACCLAIM  ★"
        elif avg >= 8.5: tag = "MASTERPIECE"
        elif avg >= 8.0: tag = "GENERALLY ACCLAIMED"
        elif avg >= 6.5: tag = "GENERALLY FAVOURABLE"
        elif avg >= 5.0: tag = "MIXED REVIEWS"
        elif avg >= 3.0: tag = "GENERALLY UNFAVOURABLE"
        else:            tag = "OVERWHELMING DISLIKE"
        print(f"  Consensus: {tag}")
        print()

        # Best and worst track across all critics
        n = len(album.songs)
        avg_per_track = []
        for ti in range(n):
            scores_for_track = [tsc[2][ti] for tsc in all_track_scores_by_critic]
            avg_per_track.append(round(sum(scores_for_track) / len(scores_for_track), 1))

        print("  Aggregate Track Scores:")
        for i, (song, sc) in enumerate(zip(album.songs, avg_per_track)):
            bar = _score_bar(sc)
            print(f"    {song.name:<30}  {sc:>4}/10  {bar}")
        print()
        best_ti  = avg_per_track.index(max(avg_per_track))
        worst_ti = avg_per_track.index(min(avg_per_track))
        print(f"  🏆 Best Track:    {album.songs[best_ti].name}  ({avg_per_track[best_ti]}/10)")
        print(f"  ⚠  Weakest Track: {album.songs[worst_ti].name}  ({avg_per_track[worst_ti]}/10)")
        _print_separator()
        return {
            "average": avg,
            "track_scores": avg_per_track,
            "critic_scores": [
                {"critic": ac.name, "score": album_score}
                for ac, album_score, _ in all_track_scores_by_critic
            ],
        }


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def _print_box(label):
    print("╔" + "═" * 64 + "╗")
    print("║" + label.center(64) + "║")
    print("╚" + "═" * 64 + "╝")

def _print_separator():
    print("─" * 66)

def _wrap_print(text, indent="  ", width=WRAP_WIDTH):
    words = text.split()
    line  = indent
    for word in words:
        if len(line) + len(word) + 1 > width:
            print(line)
            line = indent + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)

def _score_bar(score, width=10):
    filled = int(round(score / 10 * width))
    return "█" * filled + "░" * (width - filled)


# ─────────────────────────────────────────────
#  CLI HELPERS
# ─────────────────────────────────────────────

def banner():
    print()
    print("╔" + "═" * 64 + "╗")
    print("║" + "  🎵  MUSIC CAREER SIMULATOR  —  ALBUM MODE  🎵  ".center(64) + "║")
    print("╚" + "═" * 64 + "╝")
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
    gmap = {str(i + 1): g for i, g in enumerate(GENRES)}
    for key, val in gmap.items():
        print(f"    [{key:>2}]  {val}")
    while True:
        raw   = input("  ›› Pick 1 or 2 genre numbers (e.g. '1' or '3 7'): ").strip()
        parts = raw.split()
        if len(parts) == 1 and parts[0] in gmap:
            return [gmap[parts[0]]]
        if (len(parts) == 2 and parts[0] in gmap
                and parts[1] in gmap and parts[0] != parts[1]):
            return [gmap[parts[0]], gmap[parts[1]]]
        print("  ✗  Pick 1 or 2 valid different genre numbers.")

def select_theme():
    tmap = {str(i + 1): t for i, t in enumerate(THEMES)}
    return get_choice("SELECT THEME:", tmap)

def select_core_genre():
    return get_choice("SELECT ALBUM CORE GENRE:",
                      {str(i + 1): g for i, g in enumerate(GENRES)})

def select_core_theme():
    return get_choice("SELECT ALBUM CORE THEME:",
                      {str(i + 1): t for i, t in enumerate(THEMES)})

QUALITY_FLAVORS = [
    "feels like something could be here.",
    "the vibe is rough but it's something.",
    "this one has a pulse.",
    "produced clean, heart unclear.",
    "sounds promising.",
    "could be great, could be nothing.",
    "the energy is there.",
    "something's clicking.",
    "built in the right key.",
    "mid-session energy.",
    "you feel the momentum.",
    "tight from the jump.",
    "something special might be happening.",
    "every second is pulling its weight.",
    "this one could define the album.",
]

def main():
    banner()
    sim = AlbumSimulation()

    while True:
        print()
        cmd = input("  Press [A] to create an album  |  [Q] to quit  ›› ").strip().lower()
        if cmd == 'q':
            print("\n  See you on the charts.\n")
            break
        if cmd != 'a':
            continue

        print()
        album_name = input("  Album name: ").strip() or "Untitled Album"
        core_genre = select_core_genre()
        core_theme = select_core_theme()
        album      = Album(album_name, core_genre, core_theme)

        print()
        print(f"  ┌─────────────────────────────────────────────────────┐")
        print(f"  │  Album created: '{album_name}'")
        print(f"  │  Minimum songs to publish: {MIN_SONGS}")
        print(f"  └─────────────────────────────────────────────────────┘")

        while True:
            quality = random.randint(1, 10)
            flavor  = pick(QUALITY_FLAVORS)
            n       = album.song_count()

            print()
            print(f"  ┌──────────────────────────────────────────────────┐")
            print(f"  │  Song generated  —  Quality: {quality}/10  —  {flavor:<20}│")
            print(f"  │  Album so far: {n} track{'s' if n != 1 else ' '}  {'  *** READY TO PUBLISH ***' if n >= MIN_SONGS else f'  ({MIN_SONGS - n} more to unlock publish)':<26}│")
            print(f"  └──────────────────────────────────────────────────┘")
            print(f"    [1]  Add song to album")
            print(f"    [2]  Scrap and generate new song")
            if n >= MIN_SONGS:
                print(f"    [3]  Publish album  ({n} tracks)")

            act = input("  ›› ").strip()

            if act == '2':
                continue

            if act == '3':
                if n < MIN_SONGS:
                    print(f"  ✗  Need at least {MIN_SONGS} songs to publish. You have {n}.")
                    continue
                print()
                print(f"  Publishing '{album_name}' with {n} tracks...")
                print()
                sim.publish_album(album)
                break

            if act == '1':
                print()
                name     = input("  Song name: ").strip() or f"Track {n + 1}"
                genres   = select_genres()
                theme    = select_theme()
                print("\n  ┌────────────────────────────────────┐")
                print("  │           SONG DURATION            │")
                print("  └────────────────────────────────────┘")
                duration = parse_duration()
                song     = Song(quality, name, genres, theme, duration)
                album.add_song(song)
                print(f"\n  ✓  '{name}' added to '{album_name}'.  ({album.song_count()} tracks so far)")
                continue
