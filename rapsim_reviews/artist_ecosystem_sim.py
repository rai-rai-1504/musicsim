"""Standalone running simulator for the seeded artist ecosystem."""

import random
from dataclasses import dataclass, field
import statistics
from typing import Iterable

from rapsim_reviews.artist_ecosystem_seed import (
    ARTIST_BASE_REPUTATION,
    ARTIST_ECOSYSTEM_SEEDS,
    ARTIST_RELEASE_COOLOFFS,
    EcosystemArtistSeed,
)
from rapsim_reviews.album_review.base import Album as ReviewAlbum, personality_base, compute_boring_penalty
from rapsim_reviews.track_review.base import Song as ReviewSong
from rapsim_reviews.ecosystem_name_generator import (
    generate_album_name,
    generate_ep_name,
    generate_mixtape_name,
    generate_song_name,
)


ROLE_RELEASE_WEIGHTS = {
    "rapper": {"single": 0.50, "ep": 0.16, "album": 0.17, "mixtape": 0.17},
    "rapper-singer": {"single": 0.52, "ep": 0.15, "album": 0.21, "mixtape": 0.12},
    "singer": {"single": 0.56, "ep": 0.16, "album": 0.22, "mixtape": 0.06},
    "singer-writer": {"single": 0.53, "ep": 0.17, "album": 0.24, "mixtape": 0.06},
    "artist-producer": {"single": 0.41, "ep": 0.18, "album": 0.24, "mixtape": 0.17},
    "producer": {"single": 0.36, "ep": 0.21, "album": 0.21, "mixtape": 0.22},
    "mix-engineer": {"single": 0.64, "ep": 0.15, "album": 0.16, "mixtape": 0.05},
    "mastering-engineer": {"single": 0.63, "ep": 0.15, "album": 0.17, "mixtape": 0.05},
    "band": {"single": 0.48, "ep": 0.18, "album": 0.26, "mixtape": 0.08},
}


@dataclass(frozen=True)
class WeeklyRelease:
    release_id: str
    artist_name: str
    release_type: str
    title: str
    genre: str
    theme: str
    review: float
    week_number: int
    quality: float
    tracks: tuple["ProjectTrack", ...] | None = None


@dataclass(frozen=True)
class ProjectTrack:
    song_id: str
    title: str
    genre: str
    theme: str
    quality: float
    review: float = 0.0
    lyricists: tuple[str, ...] = ()
    vocalists: tuple[str, ...] = ()
    producers: tuple[str, ...] = ()
    engineers: tuple[str, ...] = ()
    features: tuple[str, ...] = ()
    feature_qualities: tuple[tuple[str, float], ...] = ()
    bg_lyrics: float | None = None
    bg_vocals: float | None = None
    bg_production: float | None = None
    bg_mix: float | None = None


@dataclass
class EcosystemSongRuntime:
    song_id: str
    artist_name: str
    title: str
    genre: str
    theme: str
    quality: float
    review: float
    release_week: int
    catchiness: float
    virality: float
    maturity_weeks: int
    weeks_since_release: int = 0
    total_streams: int = 0
    last_week_streams: int = 0
    virality_triggered: bool = False
    virality_weeks_active: int = 0
    virality_max_weekly_bonus: int = 0
    virality_baseline_streams: int = 0
    lyricists: tuple[str, ...] = ()
    vocalists: tuple[str, ...] = ()
    producers: tuple[str, ...] = ()
    engineers: tuple[str, ...] = ()
    features: tuple[str, ...] = ()
    feature_qualities: tuple[tuple[str, float], ...] = ()
    is_growing: bool = False
    project_label: str = "Single"


@dataclass
class PendingRelease:
    release_id: str
    artist_name: str
    release_type: str
    title: str
    core_genre: str
    core_theme: str
    tracks: list[ProjectTrack]
    week_created: int
    week_release: int


@dataclass
class EcosystemArtistRuntime:
    seed: EcosystemArtistSeed
    last_release_week: int | None = None
    releases_made: int = 0
    type_cooldowns: dict[str, int] | None = None
    first_release_weeks: dict[str, int] | None = None
    next_release_weeks: dict[str, int] | None = None
    planned_followup_type: str | None = None
    planned_followup_week: int | None = None
    pending_major: PendingRelease | None = None


@dataclass
class EcosystemWorld:
    week_number: int
    roster: list[EcosystemArtistRuntime]
    last_week_releases: list[WeeklyRelease]
    release_history: dict[str, list[WeeklyRelease]]
    pending_major_by_artist: dict[str, PendingRelease]
    social_graph: dict[str, dict[str, list[str]]]
    songs_by_artist: dict[str, list[str]]
    song_runtime: dict[str, EcosystemSongRuntime]
    artist_popularity: dict[str, float]
    artist_reputation: dict[str, float]
    artist_popularity_controversy_offset: dict[str, float]
    artist_reputation_controversy_offset: dict[str, float]
    controversy_history_by_artist: dict[str, list]
    pending_responses_by_artist: dict[str, list]
    recent_low_reviews_by_artist: dict[str, list]
    releases_this_week_by_artist: dict[str, list]
    weekly_events: dict[int, list]
    announced_releases: dict[int, list[PendingRelease]]
    calendar_last_prepared_week: int = -1
    news_module: object | None = None
    twitter_module: object | None = None
    diss_tracks: list = field(default_factory=list)
    pending_diss_responses: list[dict] = field(default_factory=list)
    diss_news_schedule: dict[int, list] = field(default_factory=dict)
    diss_tweet_schedule: dict[int, list] = field(default_factory=dict)
    diss_verdicts: list[dict] = field(default_factory=list)


def weighted_choice(weight_map: dict[str, float]) -> str:
    labels = list(weight_map.keys())
    weights = list(weight_map.values())
    return random.choices(labels, weights=weights, k=1)[0]


def top_weighted_key(values: dict[str, int]) -> str:
    ordered = sorted(values.items(), key=lambda item: item[1], reverse=True)[:4]
    keys = [key for key, _ in ordered]
    weights = [weight for _, weight in ordered]
    return random.choices(keys, weights=weights, k=1)[0]


def choose_release_type(seed: EcosystemArtistSeed) -> str:
    weights = ROLE_RELEASE_WEIGHTS.get(seed.role, ROLE_RELEASE_WEIGHTS["rapper"])
    return weighted_choice(weights)

def _seed_rng(label: str) -> random.Random:
    # Stable per-label RNG so social graphs don't reshuffle every week.
    # Keep it deterministic across runs but not obviously sequential.
    h = 0
    for ch in label:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return random.Random(h)


def roll_catchiness_value(rng: random.Random | None = None) -> float:
    rng = rng or random
    r = rng.random()
    # 0.1-1 (20%), 1-2 (50%), 2-3 (20%), 3-4 (8%), 4-5 (2%)
    if r < 0.20:
        return round(rng.uniform(0.1, 1.0), 2)
    if r < 0.70:
        return round(rng.uniform(1.0, 2.0), 2)
    if r < 0.90:
        return round(rng.uniform(2.0, 3.0), 2)
    if r < 0.98:
        return round(rng.uniform(3.0, 4.0), 2)
    return round(rng.uniform(4.0, 5.0), 2)


def roll_virality_value_and_maturity(rng: random.Random | None = None) -> tuple[float, int]:
    # TESTING MODE (matches career_mode):
    # 1-2: 80%, 2-3: 15%, 3-4: 4.95%, 4-5: 0.05%, maturity 100-200 weeks.
    rng = rng or random
    r = rng.random()
    if r < 0.80:
        v = rng.uniform(1.0, 2.0)
    elif r < 0.95:
        v = rng.uniform(2.0, 3.0)
    elif r < 0.9995:
        v = rng.uniform(3.0, 4.0)
    else:
        v = rng.uniform(4.0, 5.0)
    return round(v, 2), int(rng.randint(100, 200))


def catchiness_stream_multiplier(catchiness: float | None) -> float:
    if catchiness is None:
        return 1.0
    c = max(0.1, min(5.0, float(catchiness)))
    if c <= 1.0:
        t = (c - 0.1) / 0.9
        return 0.2 + (0.8 * max(0.0, min(1.0, t)))
    points = [
        (1.0, 1.0),
        (2.0, 1.9),
        (3.0, 2.8),
        (4.0, 3.5),
        # Boost 4-5 category only (1-4 unchanged).
        (5.0, 8.0),
    ]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if c <= x1:
            t = (c - x0) / (x1 - x0)
            return y0 + (y1 - y0) * t
    return points[-1][1]


def stream_decay_multiplier(weeks_since_release: int) -> float:
    if weeks_since_release < 4:
        return 1.0
    if weeks_since_release >= 11:
        return 0.05
    progress = (weeks_since_release - 3) / 8.0
    return 1.0 - (0.95 * progress)


def stream_random_range(base_streams: float) -> tuple[float, float]:
    growth = min(1.0, float(base_streams) / 200000.0)
    low_mult = 0.6 + (0.18 * growth)
    high_mult = 1.2 - (0.14 * growth)
    return low_mult, high_mult


def _virality_bonus_for_week(song: EcosystemSongRuntime, rng: random.Random, streams_base: int) -> int:
    v = float(song.virality)
    maturity = int(song.maturity_weeks)
    if v < 2.0:
        return 0
    if (not song.virality_triggered) and (song.weeks_since_release >= maturity):
        song.virality_triggered = True
        song.virality_weeks_active = 0
        song.virality_max_weekly_bonus = 0
        song.virality_baseline_streams = int(max(0, streams_base))
    if not song.virality_triggered:
        return 0
    age = int(song.virality_weeks_active)
    if v < 3.0:
        lo, hi = 100_000, 500_000
    elif v < 4.0:
        lo, hi = 2_000_000, 10_000_000
    else:
        lo, hi = 30_000_000, 70_000_000
    if age <= 7:
        bonus = int(rng.uniform(lo, hi))
        song.virality_max_weekly_bonus = max(song.virality_max_weekly_bonus, bonus)
        return bonus
    peak = max(song.virality_max_weekly_bonus, hi)
    floor_bonus = max(int(0.02 * peak), int(song.virality_baseline_streams))
    t = min(1.0, max(0.0, (age - 8) / 8.0))
    target = (1.0 - t) * peak + t * floor_bonus
    bonus = int(rng.uniform(target * 0.88, target * 1.05))
    return max(0, bonus)


def stream_count_for_ecosystem_song(song: EcosystemSongRuntime, popularity: float, rng: random.Random) -> int:
    quality_factor = max(0.0, min(1.0, float(song.quality) / 10.0))
    popularity_factor = max(0.0, min(1.0, float(popularity) / 100.0))
    weighted_score = (popularity_factor * 0.7) + (quality_factor * 0.3)
    base_constant = 2_000_000 if float(popularity) < 20.0 else 10_000_000
    base_streams = base_constant * (weighted_score**1.85) * (quality_factor**1.7)
    base_streams *= stream_decay_multiplier(int(song.weeks_since_release))
    if not getattr(song, "is_growing", False):
        base_streams *= catchiness_stream_multiplier(song.catchiness)
    low_mult, high_mult = stream_random_range(base_streams)
    streams_base = int(rng.uniform(base_streams * low_mult, base_streams * high_mult))
    streams_base = min(150_000_000, streams_base)
    if getattr(song, "is_growing", False):
        return max(0, int(streams_base))
    return max(0, int(streams_base + _virality_bonus_for_week(song, rng, streams_base)))


def build_social_graph(seeds: list[EcosystemArtistSeed]) -> dict[str, dict[str, list[str]]]:
    """Return {artist: {friends:[...], enemies:[...]}}."""
    names = [s.name for s in seeds]
    by_name = {s.name: s for s in seeds}
    graph: dict[str, dict[str, list[str]]] = {}

    # Friends derived from friendliness (Clairo-style friendly artists have lots of friends,
    # colder artists like Eminem have fewer).
    for seed in seeds:
        rng = _seed_rng("social:" + seed.name)
        pool = [n for n in names if n != seed.name]

        friendly = int(getattr(seed, "friendliness", 50))
        controversy = int(getattr(seed, "controversy", 40))

        # Friends scale: ~6-7 for cold artists, ~18-20 for very friendly ones.
        base_friends = int(round(5 + (friendly / 100.0) * 15))
        base_friends = max(4, min(22, base_friends + rng.randint(-2, 2)))

        rng.shuffle(pool)
        friends = pool[:base_friends]
        graph[seed.name] = {"friends": friends, "enemies": []}

    # Enemies: toned down and capped (max 10). Driven by:
    # - other artist being very controversial
    # - other artist being very unfriendly
    # - self being very controversial (more feuds overall)
    # Friendly artists should rarely show up in hate lists.
    for seed in seeds:
        rng = _seed_rng("enemies:" + seed.name)
        self_cont = int(getattr(seed, "controversy", 40))
        self_friendly = int(getattr(seed, "friendliness", 50))
        friends = set(graph[seed.name]["friends"])

        # Most controversial artists top out around 10 enemies.
        target_enemies = int(round(1 + (self_cont / 100.0) * 9))
        target_enemies = max(0, min(10, target_enemies + rng.randint(-1, 1)))

        candidates = []
        weights = []
        for other_name in names:
            if other_name == seed.name:
                continue
            if other_name in friends:
                continue
            other = by_name[other_name]
            other_cont = int(getattr(other, "controversy", 40))
            other_friendly = int(getattr(other, "friendliness", 50))

            # Friendly artists are rarely enemies (Dijon/Bon Iver types).
            if other_friendly >= 70 and rng.random() < 0.92:
                continue

            # Similar controversy rates: less likely to feud (can still happen rarely).
            cont_gap = abs(self_cont - other_cont)
            similar_high = self_cont >= 65 and other_cont >= 65 and cont_gap <= 15
            if similar_high and rng.random() < 0.88:
                continue

            # Weight toward hating very controversial or very unfriendly people.
            w = 0.15
            if other_cont >= 90:
                w += 2.2
            elif other_cont >= 75:
                w += 1.2
            elif other_cont >= 60:
                w += 0.55

            if other_friendly <= 30:
                w += 1.25
            elif other_friendly <= 45:
                w += 0.5

            # Your own controversy increases feud likelihood overall.
            w *= 0.75 + (self_cont / 160.0)

            # Small random feud chance, even without obvious reasons.
            w += rng.uniform(0.0, 0.25)

            candidates.append(other_name)
            weights.append(max(0.01, w))

        enemies: list[str] = []
        if target_enemies > 0 and candidates:
            # Sample without replacement using repeated weighted draws.
            pool = list(zip(candidates, weights))
            for _ in range(target_enemies):
                if not pool:
                    break
                names_pool = [p[0] for p in pool]
                weights_pool = [p[1] for p in pool]
                pick = rng.choices(names_pool, weights=weights_pool, k=1)[0]
                enemies.append(pick)
                pool = [p for p in pool if p[0] != pick]

        # 90+ controversial artists appear in ~60% of people's enemy lists (unless they are friendly / close friends).
        controversial = [s.name for s in seeds if int(getattr(s, "controversy", 0)) >= 90]
        for target in controversial:
            if target == seed.name or target in friends or target in enemies:
                continue
            other = by_name[target]
            if int(getattr(other, "friendliness", 50)) >= 70:
                continue
            if rng.random() < 0.60 and len(enemies) < 10:
                enemies.append(target)

        # No overlap with friends.
        enemies = [e for e in enemies if e not in friends]
        graph[seed.name]["enemies"] = enemies[:10]

    # Hard-coded relationship: Dijon and Mk.gee are best friends.
    if "Dijon" in graph and "Mk.gee" in graph:
        for a, b in (("Dijon", "Mk.gee"), ("Mk.gee", "Dijon")):
            friends = list(graph[a].get("friends", []))
            enemies = list(graph[a].get("enemies", []))
            if b in enemies:
                enemies = [x for x in enemies if x != b]
            if b not in friends:
                friends.insert(0, b)
            else:
                # Move to front.
                friends = [b] + [x for x in friends if x != b]
            graph[a]["friends"] = friends[:25]
            graph[a]["enemies"] = enemies[:10]

    return graph


def _friend_list(world: "EcosystemWorld", artist_name: str) -> set[str]:
    return set(world.social_graph.get(artist_name, {}).get("friends", []))


def _enemy_list(world: "EcosystemWorld", artist_name: str) -> set[str]:
    return set(world.social_graph.get(artist_name, {}).get("enemies", []))


def release_title_for_type(release_type: str, genre: str, theme: str) -> str:
    if release_type == "single":
        return generate_song_name(genre=genre, theme=theme)
    if release_type == "ep":
        return generate_ep_name(genre=genre, theme=theme)
    if release_type == "mixtape":
        return generate_mixtape_name(genre=genre, theme=theme)
    return generate_album_name(genre=genre, theme=theme)


def integer_review(seed: EcosystemArtistSeed, genre: str, theme: str, release_type: str) -> int:
    skill_average = sum(seed.skills.values()) / len(seed.skills)
    genre_score = seed.genres[genre]
    theme_score = seed.themes[theme]
    consistency = seed.quality_consistency
    popularity_pressure = max(0.0, (seed.popularity - 85.0) * 0.02)

    base = (
        (skill_average * 0.42)
        + (genre_score * 0.24)
        + (theme_score * 0.16)
        + (consistency * 0.18)
    ) / 10.0

    if release_type == "single":
        variance = random.uniform(-1.8, 1.2)
    elif release_type == "ep":
        variance = random.uniform(-1.4, 1.0)
    else:
        variance = random.uniform(-1.7, 0.8)

    if consistency >= 85:
        variance *= 0.55
    elif consistency <= 50:
        variance *= 1.25

    review = round(base + variance - popularity_pressure)
    return max(1, min(10, int(review)))


def _new_release_id(artist_name: str, week_number: int) -> str:
    token = random.randint(1000, 9999)
    safe = "".join(ch for ch in artist_name if ch.isalnum())[:8]
    return f"ER-{safe}-{week_number}-{token}"


def _new_song_id(release_id: str, track_index: int) -> str:
    return f"{release_id}:t{int(track_index)}"


def _roll_bg_attribute_from_skill_value(skill_value: float, rng: random.Random) -> float:
    s = float(skill_value) / 10.0
    lo = max(1.0, s - 2.0)
    hi = max(lo, s)
    return round(rng.uniform(lo, hi), 1)


def _jitter_attribute(value: float, rng: random.Random, span: float = 0.4, lo: float = 1.0, hi: float = 9.9) -> float:
    return round(max(lo, min(hi, rng.uniform(value - span, value + span))), 1)


def _track_quality(seed: EcosystemArtistSeed, genre: str, theme: str, project_ability: int) -> float:
    skill_average = sum(seed.skills.values()) / len(seed.skills)
    genre_score = seed.genres.get(genre, 30)
    theme_score = seed.themes.get(theme, 30)
    consistency = seed.quality_consistency
    popularity_pressure = max(0.0, (seed.popularity - 85.0) * 0.02)

    base = (
        (skill_average * 0.42)
        + (genre_score * 0.24)
        + (theme_score * 0.16)
        + (consistency * 0.18)
    ) / 10.0

    # Variance: quality_consistency controls how tight the spread is, project_ability
    # controls how consistent the *project* feels track-to-track.
    qc = max(0.0, min(1.0, consistency / 100.0))
    var_span = (1.9 * (1.0 - qc)) + 0.55
    proj_factor = 1.25 - (max(0, min(100, project_ability)) / 200.0)
    var_span *= proj_factor
    variance = random.uniform(-var_span, var_span * 0.75)

    quality = base + variance - popularity_pressure
    return round(max(0.0, min(10.0, quality)), 1)


def _target_track_count(release_type: str) -> int:
    if release_type == "ep":
        return random.randint(3, 6)
    if release_type == "mixtape":
        roll = random.random()
        if roll < 0.70:
            return random.randint(6, 14)
        if roll < 0.95:
            return random.randint(15, 20)
        return random.randint(21, 25)
    # album
    roll = random.random()
    if roll < 0.40:
        return random.randint(7, 13)
    if roll < 0.80:
        return random.randint(14, 18)
    if roll < 0.95:
        return random.randint(19, 22)
    if roll < 0.99:
        return random.randint(23, 25)
    return random.randint(26, 35)


def _length_modifier(release_type: str, n_tracks: int) -> float:
    if release_type == "ep":
        lo, hi = 3, 6
    elif release_type == "mixtape":
        lo, hi = 8, 18
    else:
        lo, hi = 8, 16
    if n_tracks < lo:
        return -0.35
    if n_tracks > hi:
        return -0.35
    return 0.2


def compute_project_score(title: str, core_genre: str, core_theme: str, tracks: list[ProjectTrack], release_type: str) -> float:
    album = ReviewAlbum(title, core_genre, core_theme)
    for t in tracks:
        album.add_song(
            ReviewSong(
                quality=float(t.quality),
                name=t.title,
                genres=[t.genre],
                theme=t.theme,
                duration=random.randint(125, 265),
            )
        )
    song_scores = [
        float(getattr(t, "review", 0.0) or 0.0) if float(getattr(t, "review", 0.0) or 0.0) > 0 else float(s.quality)
        for t, s in zip(tracks, album.songs)
    ]
    base = personality_base(song_scores, "balanced")
    cohesion_pen = album.cohesion_penalty()
    theme_mod = album.theme_alignment_modifier()
    flow_mod = album.track_flow_modifier()
    length_mod = _length_modifier(release_type, album.song_count())
    boring_pen, _ = compute_boring_penalty(album, 0.15)
    stdev = statistics.pstdev(song_scores) if len(song_scores) > 1 else 0.0
    consistency_pen = min(1.4, stdev * 0.22)
    raw = base - cohesion_pen + theme_mod + flow_mod + length_mod - boring_pen - consistency_pen
    return round(max(1.0, min(10.0, raw)), 1)


def assign_project_track_reviews(
    tracks: list[ProjectTrack],
    release_type: str,
    seed_label: str,
) -> list[ProjectTrack]:
    rated_tracks: list[ProjectTrack] = []
    for idx, track in enumerate(tracks):
        rng = _seed_rng(f"{seed_label}:track-review:{idx}:{track.title}")
        quality = float(getattr(track, "quality", 0.0))
        if release_type == "ep":
            variance = rng.uniform(-0.9, 0.7)
        elif release_type == "mixtape":
            variance = rng.uniform(-1.1, 0.8)
        else:
            variance = rng.uniform(-1.0, 0.75)
        review = max(1.0, min(10.0, round(quality + variance, 1)))
        rated_tracks.append(
            ProjectTrack(
                song_id=track.song_id,
                title=track.title,
                genre=track.genre,
                theme=track.theme,
                quality=float(track.quality),
                review=float(review),
                lyricists=tuple(track.lyricists),
                vocalists=tuple(track.vocalists),
                producers=tuple(track.producers),
                engineers=tuple(track.engineers),
                features=tuple(track.features),
                feature_qualities=tuple(getattr(track, "feature_qualities", ())),
                bg_lyrics=track.bg_lyrics,
                bg_vocals=track.bg_vocals,
                bg_production=track.bg_production,
                bg_mix=track.bg_mix,
            )
        )
    return rated_tracks


def recent_singles(world: "EcosystemWorld", artist_name: str, week_number: int, window_weeks: int = 8) -> list[WeeklyRelease]:
    history = world.release_history.get(artist_name, [])
    out: list[WeeklyRelease] = []
    for r in history:
        if r.release_type != "single":
            continue
        if (week_number - r.week_number) <= window_weeks and (week_number - r.week_number) > 0:
            out.append(r)
    return out


def build_project_tracks(seed: EcosystemArtistSeed, core_genre: str, core_theme: str, total_tracks: int, project_ability: int) -> list[ProjectTrack]:
    project_ability = int(max(0, min(100, project_ability)))
    p_core_genre = max(0.55, min(0.92, 0.50 + project_ability / 200.0))
    p_core_theme = max(0.50, min(0.90, 0.45 + project_ability / 220.0))

    top_genres = sorted(seed.genres.items(), key=lambda kv: kv[1], reverse=True)[:4]
    genre_keys = [g for g, _ in top_genres] or [core_genre]
    genre_weights = [w for _, w in top_genres] or [1]

    top_themes = sorted(seed.themes.items(), key=lambda kv: kv[1], reverse=True)[:4]
    theme_keys = [t for t, _ in top_themes] or [core_theme]
    theme_weights = [w for _, w in top_themes] or [1]

    used_titles: set[str] = set()
    tracks: list[ProjectTrack] = []
    for _ in range(total_tracks):
        genre = core_genre if random.random() < p_core_genre else random.choices(genre_keys, weights=genre_weights, k=1)[0]
        theme = core_theme if random.random() < p_core_theme else random.choices(theme_keys, weights=theme_weights, k=1)[0]
        title = generate_song_name(genre=genre, theme=theme)
        tries = 0
        while title in used_titles and tries < 10:
            title = generate_song_name(genre=genre, theme=theme)
            tries += 1
        used_titles.add(title)
        q = _track_quality(seed, genre, theme, project_ability)
        # song_id/review are assigned when the project is scheduled/released.
        tracks.append(ProjectTrack(song_id="", title=title, genre=genre, theme=theme, quality=q, review=0.0))
    return tracks


def _seed_by_name(world: "EcosystemWorld") -> dict[str, EcosystemArtistSeed]:
    return {rt.seed.name: rt.seed for rt in world.roster}


def _is_feature_capable(seed: EcosystemArtistSeed) -> bool:
    role = str(getattr(seed, "role", "")).lower()
    if "engineer" in role:
        return False
    return True


def classify_artist_skills(seed: EcosystemArtistSeed) -> set[str]:
    """
    Categories based on strongest suite:
    - Determine highest skill.
    - If highest < 30: growing
    - Else possess any skill within [highest - pct*highest, highest] where pct=0.30 if highest>50 else 0.20
    Returns a set of: {"lyricist","vocalist","producer","engineer","growing"}.
    """
    skills = {
        "lyrics": int(seed.skills.get("lyrics", 0)),
        "vocals": int(seed.skills.get("vocals", 0)),
        "production": int(seed.skills.get("production", 0)),
        "mix/master": int(seed.skills.get("mix/master", 0)),
    }
    highest = max(skills.values()) if skills else 0
    if highest < 30:
        return {"growing"}
    pct = 0.30 if highest > 50 else 0.20
    threshold = highest - (pct * highest)
    cats: set[str] = set()
    if skills["lyrics"] >= threshold:
        cats.add("lyricist")
    if skills["vocals"] >= threshold:
        cats.add("vocalist")
    if skills["production"] >= threshold:
        cats.add("producer")
    if skills["mix/master"] >= threshold:
        cats.add("engineer")
    if not cats:
        cats.add("growing")
    return cats


def _is_engineer_only(seed: EcosystemArtistSeed) -> bool:
    cats = classify_artist_skills(seed)
    if "growing" in cats:
        return False
    return ("engineer" in cats) and ("producer" not in cats) and ("lyricist" not in cats) and ("vocalist" not in cats)


def _producer_candidates(world: "EcosystemWorld", genre: str | None, exclude: set[str]) -> list[EcosystemArtistSeed]:
    out: list[EcosystemArtistSeed] = []
    for rt in world.roster:
        seed = rt.seed
        if seed.name in exclude:
            continue
        cats = classify_artist_skills(seed)
        if "growing" in cats:
            continue
        if "producer" not in cats:
            continue
        prod_skill = int(seed.skills.get("production", 0))
        if prod_skill < 70:
            continue
        if genre is None:
            out.append(seed)
        else:
            # Prefer producers that actually live in this genre.
            if int(seed.genres.get(genre, 0)) >= 45:
                out.append(seed)
    return out


def _pick_producer(
    world: "EcosystemWorld",
    main: EcosystemArtistSeed,
    genre: str,
    rng: random.Random,
) -> tuple[str, float]:
    """Return (producer_name, producer_delta). Producer can be the main artist (self-produced)."""
    prod_skill = int(main.skills.get("production", 0))
    main_cats = classify_artist_skills(main)

    # Special rule: Dijon is always produced by Mk.gee (best-friend pipeline).
    if main.name == "Dijon":
        by_name = _seed_by_name(world)
        mk = by_name.get("Mk.gee")
        if mk is not None:
            enemies = _enemy_list(world, main.name)
            reverse_enemies = {rt.seed.name for rt in world.roster if main.name in _enemy_list(world, rt.seed.name)}
            exclude = set(enemies) | reverse_enemies | {main.name}
            if mk.name not in exclude:
                qc = int(getattr(mk, "quality_consistency", 70))
                pskill = int(mk.skills.get("production", 70))
                gfit = int(mk.genres.get(genre, 50))
                delta = ((qc - 70) / 100.0) * 0.85 + ((pskill - 70) / 100.0) * 0.65 + ((gfit - 60) / 100.0) * 0.45
                delta += rng.uniform(-0.25, 0.25)
                delta = max(-0.6, min(0.9, delta))
                return mk.name, round(delta, 2)

    if prod_skill >= 70:
        self_prob = rng.uniform(0.60, 0.80)
    elif prod_skill >= 45:
        self_prob = rng.uniform(0.20, 0.30)
    else:
        self_prob = 0.0

    enemies = _enemy_list(world, main.name)
    # No collaboration with people either side dislikes.
    reverse_enemies = {rt.seed.name for rt in world.roster if main.name in _enemy_list(world, rt.seed.name)}
    exclude = set(enemies) | reverse_enemies | {main.name}
    producers = _producer_candidates(world, genre, exclude=exclude)
    if not producers:
        # If genre match isn't available, fall back to any strong producer.
        producers = _producer_candidates(world, None, exclude=exclude)

    # Growing artists mostly self-produce (or keep it local).
    if "growing" in main_cats:
        self_prob = max(self_prob, 0.75)
    use_self = (rng.random() < self_prob) or (not producers and prod_skill >= 45)
    if use_self:
        delta = 0.0
        if 45 <= prod_skill < 70:
            # Mid producers self-producing can hurt a bit.
            delta -= rng.uniform(0.5, 1.5)
        elif prod_skill >= 85:
            delta += rng.uniform(0.0, 0.4)
        return main.name, round(delta, 2)

    # External producer: weight by genre fit and production skill.
    weights = []
    for p in producers:
        w = 1.0 + (int(p.genres.get(genre, 0)) / 50.0) + (int(p.skills.get("production", 0)) / 60.0)
        weights.append(w)
    chosen = rng.choices(producers, weights=weights, k=1)[0]
    qc = int(getattr(chosen, "quality_consistency", 70))
    pskill = int(chosen.skills.get("production", 70))
    gfit = int(chosen.genres.get(genre, 50))
    delta = ((qc - 70) / 100.0) * 0.85 + ((pskill - 70) / 100.0) * 0.65 + ((gfit - 60) / 100.0) * 0.45
    delta += rng.uniform(-0.35, 0.35)
    delta = max(-0.9, min(0.9, delta))
    return chosen.name, round(delta, 2)


def _feature_frequency(friendliness: int) -> float:
    friendliness = max(0, min(100, int(friendliness)))
    # Very friendly: ~60% of songs have features; very unfriendly: ~20%.
    return 0.20 + 0.40 * (friendliness / 100.0)


def _pick_features(
    world: "EcosystemWorld",
    main: EcosystemArtistSeed,
    genre: str,
    theme: str,
    rng: random.Random,
    max_features: int = 5,
) -> list[EcosystemArtistSeed]:
    friendliness = int(getattr(main, "friendliness", 50))
    main_cats = classify_artist_skills(main)
    if rng.random() > _feature_frequency(friendliness):
        return []

    # How many features? Friendly artists stack features more often.
    n = 1
    if rng.random() < 0.28 + (friendliness / 400.0):
        n += 1
    if rng.random() < 0.10 + (friendliness / 900.0):
        n += 1
    if rng.random() < 0.05 + (friendliness / 1400.0):
        n += 1
    if rng.random() < 0.02 + (friendliness / 2000.0):
        n += 1
    n = max(1, min(max_features, n))

    enemies = _enemy_list(world, main.name)
    friends = _friend_list(world, main.name)
    reverse_enemies = {rt.seed.name for rt in world.roster if main.name in _enemy_list(world, rt.seed.name)}

    # Candidate pool.
    by_name = _seed_by_name(world)
    candidates: list[EcosystemArtistSeed] = []
    for rt in world.roster:
        seed = rt.seed
        if seed.name == main.name:
            continue
        if seed.name in enemies:
            continue
        if seed.name in reverse_enemies:
            continue
        cats = classify_artist_skills(seed)
        # Only lyricists/vocalists can be "ft.".
        if "growing" in cats:
            pass
        elif ("lyricist" not in cats) and ("vocalist" not in cats):
            continue
        # Growing artists collaborate only with other growing artists.
        if ("growing" in main_cats) != ("growing" in cats):
            continue
        candidates.append(seed)

    # Pick with weights: genre fit, theme fit, and friend bias. 5% wildcard breaks the "genre fit" rule.
    picks: list[EcosystemArtistSeed] = []
    used: set[str] = set()
    for _ in range(n):
        pool = [c for c in candidates if c.name not in used]
        if not pool:
            break
        wildcard = rng.random() < 0.05
        weights = []
        filtered = []
        for c in pool:
            g = int(c.genres.get(genre, 0))
            t = int(c.themes.get(theme, 0))
            if not wildcard and g < 45:
                continue
            # Theme awareness: low theme proficiency makes them less likely.
            theme_gate = 1.0
            if t < 40:
                theme_gate = 0.15
            elif t < 55:
                theme_gate = 0.55
            friend_boost = 2.8 if c.name in friends else 1.0
            w = (1.0 + (g / 80.0) + (t / 85.0)) * friend_boost * theme_gate
            weights.append(max(0.05, w))
            filtered.append(c)
        if not filtered:
            # Fall back to anyone not hated.
            filtered = pool
            weights = [1.0 + (2.2 if c.name in friends else 1.0) for c in filtered]
        chosen = rng.choices(filtered, weights=weights, k=1)[0]
        used.add(chosen.name)
        picks.append(chosen)
    return picks


def _apply_collaboration_caps(base_quality: float, raw_quality: float, rng: random.Random) -> float:
    """Soft-cap collaboration impact so it feels real (not formulaic)."""
    base_quality = float(base_quality)
    raw_quality = float(raw_quality)
    upper = base_quality + 2.0
    lower = base_quality - 2.0

    if raw_quality > upper:
        # Allow a tiny bit above the cap for realism (matches your example).
        raw_quality = rng.uniform(base_quality + 1.8, base_quality + 2.2)
    elif raw_quality < lower:
        raw_quality = rng.uniform(base_quality - 2.2, base_quality - 1.8)
    else:
        raw_quality = raw_quality + rng.uniform(-0.15, 0.15)

    # Rarely exceed 9.5; tiny chance to touch 10.
    if raw_quality > 9.5:
        if rng.random() < 0.035:
            raw_quality = rng.uniform(9.6, 10.0)
        else:
            raw_quality = min(raw_quality, 9.5 - rng.uniform(0.0, 0.2))
    return round(max(0.0, min(10.0, raw_quality)), 1)


def _feature_quality_from_delta(feature: EcosystemArtistSeed, delta: float, rng: random.Random) -> float:
    # Convert the 0-100 skill average to the game's 0-10 display scale.
    x = ((float(feature.skills.get("lyrics", 50)) / 100.0) + (float(feature.skills.get("vocals", 50)) / 100.0)) / 2.0
    x *= 10.0
    if delta >= 0:
        low, high = x - 2.0, x + 1.0
    else:
        low, high = x - 4.0, x - 2.0
    return round(max(0.0, min(10.0, rng.uniform(low, high))), 1)


def apply_collaborations_to_track(
    world: "EcosystemWorld",
    main: EcosystemArtistSeed,
    track: ProjectTrack,
    rng: random.Random,
) -> ProjectTrack:
    """Return a new ProjectTrack with features/producer embedded in the title and quality adjusted."""
    producer_name, producer_delta = _pick_producer(world, main, track.genre, rng)
    features = _pick_features(world, main, track.genre, track.theme, rng, max_features=5)

    base_quality = float(track.quality)
    raw_quality = base_quality + float(producer_delta)

    def _pick_engineer() -> tuple[str, float]:
        mm = int(main.skills.get("mix/master", 0))
        main_cats = classify_artist_skills(main)
        if mm >= 70:
            self_prob = rng.uniform(0.70, 0.88)
        elif mm >= 50:
            self_prob = rng.uniform(0.25, 0.40)
        else:
            self_prob = 0.0

        enemies = _enemy_list(world, main.name)
        reverse_enemies = {rt.seed.name for rt in world.roster if main.name in _enemy_list(world, rt.seed.name)}
        exclude = set(enemies) | reverse_enemies | {main.name}

        engineers: list[EcosystemArtistSeed] = []
        for rt in world.roster:
            s = rt.seed
            if s.name in exclude:
                continue
            cats = classify_artist_skills(s)
            if "growing" in cats:
                continue
            if "engineer" not in cats:
                continue
            if int(s.skills.get("mix/master", 0)) < 70:
                continue
            if int(s.genres.get(track.genre, 0)) >= 45:
                engineers.append(s)
        if not engineers:
            for rt in world.roster:
                s = rt.seed
                if s.name in exclude:
                    continue
                cats = classify_artist_skills(s)
                if "growing" in cats:
                    continue
                if "engineer" not in cats:
                    continue
                if int(s.skills.get("mix/master", 0)) >= 70:
                    engineers.append(s)

        if "growing" in main_cats:
            self_prob = max(self_prob, 0.75)

        use_self = rng.random() < self_prob or not engineers
        if use_self:
            delta = 0.0
            if 50 <= mm < 70:
                delta -= rng.uniform(0.4, 1.2)
            elif mm >= 85:
                delta += rng.uniform(0.0, 0.35)
            return main.name, round(delta, 2)

        weights = []
        for e in engineers:
            w = 1.0 + (int(e.genres.get(track.genre, 0)) / 55.0) + (int(e.skills.get("mix/master", 0)) / 60.0)
            weights.append(w)
        chosen = rng.choices(engineers, weights=weights, k=1)[0]
        qc = int(getattr(chosen, "quality_consistency", 70))
        eskill = int(chosen.skills.get("mix/master", 70))
        gfit = int(chosen.genres.get(track.genre, 50))
        delta = ((qc - 70) / 100.0) * 0.65 + ((eskill - 70) / 100.0) * 0.70 + ((gfit - 60) / 100.0) * 0.35
        delta += rng.uniform(-0.35, 0.35)
        delta = max(-0.9, min(0.9, delta))
        return chosen.name, round(delta, 2)

    engineer_name, engineer_delta = _pick_engineer()
    raw_quality += float(engineer_delta)

    # Feature deltas accumulate, then get soft-capped vs the original base.
    feature_deltas: list[tuple[EcosystemArtistSeed, float]] = []
    feature_qualities: list[tuple[str, float]] = []
    for f in features:
        qc = int(getattr(f, "quality_consistency", 70))
        theme_fit = int(f.themes.get(track.theme, 50))
        delta = ((qc - 70) / 100.0) * 0.65 + ((theme_fit - 55) / 100.0) * 0.35
        delta += rng.uniform(-0.45, 0.45)
        delta = max(-0.7, min(0.7, delta))
        raw_quality += delta
        feature_deltas.append((f, float(delta)))
        feature_qualities.append((f.name, _feature_quality_from_delta(f, float(delta), rng)))

    final_quality = _apply_collaboration_caps(base_quality, raw_quality, rng)

    # Background craft attributes (lyrics/vocals/prod/mix) follow who contributed.
    bg_lyrics = _roll_bg_attribute_from_skill_value(int(main.skills.get("lyrics", 25)), rng)
    bg_vocals = _roll_bg_attribute_from_skill_value(int(main.skills.get("vocals", 25)), rng)
    bg_production = _roll_bg_attribute_from_skill_value(int(main.skills.get("production", 25)), rng)
    bg_mix = _roll_bg_attribute_from_skill_value(int(main.skills.get("mix/master", 25)), rng)

    # Producer/engineer overwrite those components.
    by_name = _seed_by_name(world)
    prod_seed = by_name.get(producer_name, main)
    eng_seed = by_name.get(engineer_name, main)
    bg_production = _roll_bg_attribute_from_skill_value(int(prod_seed.skills.get("production", 25)), rng)
    bg_mix = _roll_bg_attribute_from_skill_value(int(eng_seed.skills.get("mix/master", 25)), rng)

    # For each feature, apply the attribute bump/penalty based on whether that feature pushed the song up or down.
    for f, delta in feature_deltas:
        lyr_skill = int(f.skills.get("lyrics", 50))
        voc_skill = int(f.skills.get("vocals", 50))
        if delta >= 0:
            bg_lyrics = _jitter_attribute(
                min(9.5, max(1.0, bg_lyrics + 0.15 * (lyr_skill / 10.0))),
                rng,
            )
            bg_vocals = _jitter_attribute(
                min(9.5, max(1.0, bg_vocals + 0.15 * (voc_skill / 10.0))),
                rng,
            )
        else:
            bg_lyrics = _jitter_attribute(
                max(2.0, bg_lyrics - 0.5 * ((100.0 - lyr_skill) / 10.0)),
                rng,
                lo=2.0,
            )
            bg_vocals = _jitter_attribute(
                max(2.0, bg_vocals - 0.5 * ((100.0 - voc_skill) / 10.0)),
                rng,
                lo=2.0,
            )

    # Contributor metadata.
    main_cats = classify_artist_skills(main)
    lyricists = [main.name] if ("lyricist" in main_cats) else []
    vocalists = [main.name] if ("vocalist" in main_cats) else []
    for f in features:
        fcats = classify_artist_skills(f)
        if "lyricist" in fcats:
            lyricists.append(f.name)
        if "vocalist" in fcats:
            vocalists.append(f.name)

    # Title formatting: features and producer only (engineer hidden from title).
    base_title = track.title
    feat_names = [f.name for f in features]
    feat_suffix = (" ft. " + ", ".join(feat_names)) if feat_names else ""
    display = f"{main.name} - {base_title}{feat_suffix} (prod. {producer_name})"

    return ProjectTrack(
        song_id=track.song_id,
        title=display,
        genre=track.genre,
        theme=track.theme,
        quality=final_quality,
        review=float(getattr(track, "review", 0.0)),
        lyricists=tuple(dict.fromkeys(lyricists)),
        vocalists=tuple(dict.fromkeys(vocalists)),
        producers=tuple(dict.fromkeys([producer_name])),
        engineers=tuple(dict.fromkeys([engineer_name])),
        features=tuple(feat_names),
        feature_qualities=tuple(feature_qualities),
        bg_lyrics=float(bg_lyrics),
        bg_vocals=float(bg_vocals),
        bg_production=float(bg_production),
        bg_mix=float(bg_mix),
    )


def initial_single_week(seed: EcosystemArtistSeed) -> int:
    tendency = seed.release_tendency
    if tendency >= 80:
        return random.randint(1, 36)
    if tendency >= 65:
        return random.randint(4, 52)
    if tendency >= 50:
        return random.randint(8, 78)
    if tendency >= 35:
        return random.randint(14, 96)
    return random.randint(26, 104)


def initial_release_weeks(seed: EcosystemArtistSeed) -> dict[str, int]:
    base = initial_single_week(seed)
    cooloffs = base_cooloffs_for(seed)
    weeks = {
        "single": base,
        "ep": random.randint(12, 104),
        "mixtape": random.randint(16, 104),
        "album": random.randint(24, 104),
    }
    for release_type, cooldown in cooloffs.items():
        if cooldown >= 900:
            weeks[release_type] = 9999
    if seed.release_tendency < 35:
        weeks["album"] = min(156, weeks["album"] + random.randint(12, 52))
    elif seed.release_tendency < 55:
        weeks["album"] = min(130, weeks["album"] + random.randint(6, 26))
    return weeks


def base_cooloffs_for(seed: EcosystemArtistSeed) -> dict[str, int]:
    return dict(
        ARTIST_RELEASE_COOLOFFS.get(
            seed.name,
            {"single": 10, "ep": 24, "mixtape": 36, "album": 72},
        )
    )


def build_release_schedule() -> dict[str, int]:
    return {"single": 0, "ep": 0, "mixtape": 0, "album": 0}


def next_release_gap(seed: EcosystemArtistSeed, release_type: str, cooldown_weeks: int) -> int:
    if release_type == "single":
        cooldown_weeks = max(10, cooldown_weeks)
    tendency_push = int(((100 - seed.release_tendency) / 100.0) * cooldown_weeks * 0.35)
    if release_type == "single":
        random_push = random.randint(1, max(3, cooldown_weeks // 5))
    else:
        random_push = random.randint(0, max(2, cooldown_weeks // 6))
    if release_type in {"album", "ep", "mixtape"}:
        cooldown_weeks = max(52, cooldown_weeks)
    return cooldown_weeks + tendency_push + random_push


def relative_lock_weeks(seed: EcosystemArtistSeed, source_type: str, target_type: str) -> int:
    cooloffs = base_cooloffs_for(seed)
    album_cooloff = cooloffs["album"]
    major_types = {"album", "ep", "mixtape"}
    if source_type in major_types and target_type in major_types and source_type != target_type:
        return max(52, min(120, int(album_cooloff * 0.55)))
    if source_type == "album":
        if target_type == "single":
            return max(12, min(32, int(album_cooloff * 0.16)))
        if target_type in {"ep", "mixtape"}:
            return max(52, min(120, int(album_cooloff * 0.55)))
    if source_type in {"ep", "mixtape"}:
        if target_type == "single":
            return random.randint(8, 18)
        if target_type in {"ep", "mixtape"}:
            return max(52, min(120, int(album_cooloff * 0.55)))
        if target_type == "album":
            return max(52, min(120, int(album_cooloff * 0.55)))
    if source_type == "single" and target_type in {"ep", "mixtape", "album"}:
        return random.randint(3, 10)
    return 0


def apply_release_cooldowns(runtime_artist: EcosystemArtistRuntime, release_type: str, week_number: int):
    seed = runtime_artist.seed
    base_cooloff = base_cooloffs_for(seed)[release_type]
    runtime_artist.type_cooldowns[release_type] = next_release_gap(
        seed,
        release_type,
        base_cooloff,
    )
    runtime_artist.next_release_weeks[release_type] = (
        week_number + runtime_artist.type_cooldowns[release_type]
    )

    for target_type in runtime_artist.type_cooldowns:
        if target_type == release_type:
            continue
        lock_weeks = relative_lock_weeks(seed, release_type, target_type)
        if lock_weeks <= 0:
            continue
        runtime_artist.type_cooldowns[target_type] = max(
            runtime_artist.type_cooldowns[target_type],
            lock_weeks,
        )
        runtime_artist.next_release_weeks[target_type] = max(
            runtime_artist.next_release_weeks[target_type],
            week_number + lock_weeks,
        )


def reserve_release_windows(runtime_artist: EcosystemArtistRuntime, release_type: str, week_number: int):
    """Reserve future calendar slots using the same timing rules as a real release."""
    seed = runtime_artist.seed
    base_cooloff = base_cooloffs_for(seed)[release_type]
    own_gap = next_release_gap(seed, release_type, base_cooloff)
    runtime_artist.next_release_weeks[release_type] = max(
        int(runtime_artist.next_release_weeks.get(release_type, 0)),
        week_number + own_gap,
    )

    for target_type in runtime_artist.next_release_weeks:
        if target_type == release_type:
            continue
        lock_weeks = relative_lock_weeks(seed, release_type, target_type)
        if lock_weeks <= 0:
            continue
        runtime_artist.next_release_weeks[target_type] = max(
            int(runtime_artist.next_release_weeks.get(target_type, 0)),
            week_number + lock_weeks,
        )


def plan_single_followup(runtime_artist: EcosystemArtistRuntime, week_number: int):
    if random.random() > 0.75:
        return
    seed = runtime_artist.seed
    project_weights = {
        key: value
        for key, value in ROLE_RELEASE_WEIGHTS.get(seed.role, ROLE_RELEASE_WEIGHTS["rapper"]).items()
        if key in {"album", "ep", "mixtape"} and base_cooloffs_for(seed)[key] < 900
    }
    if not project_weights:
        return
    project_type = weighted_choice(project_weights)
    cooldown_wait = runtime_artist.type_cooldowns.get(project_type, 0)
    if cooldown_wait > 20:
        return
    earliest_allowed = max(week_number + random.randint(4, 12), week_number + cooldown_wait)
    runtime_artist.planned_followup_type = project_type
    runtime_artist.planned_followup_week = earliest_allowed
    runtime_artist.next_release_weeks[project_type] = earliest_allowed


def choose_available_release_type(runtime_artist: EcosystemArtistRuntime, week_number: int, surprise_mode: bool = False) -> str | None:
    major_types = {"album", "ep", "mixtape"}
    if runtime_artist.pending_major is not None:
        # Don't schedule another major project while one is already queued.
        pass
    # Sole engineers don't release music.
    if _is_engineer_only(runtime_artist.seed):
        return None
    if (
        runtime_artist.planned_followup_type
        and runtime_artist.planned_followup_week is not None
        and week_number >= runtime_artist.planned_followup_week
        and runtime_artist.type_cooldowns[runtime_artist.planned_followup_type] <= 0
    ):
        if runtime_artist.pending_major is None or runtime_artist.planned_followup_type not in major_types:
            return runtime_artist.planned_followup_type

    weights = ROLE_RELEASE_WEIGHTS.get(
        runtime_artist.seed.role,
        ROLE_RELEASE_WEIGHTS["rapper"],
    )
    available = {
        release_type: weight
        for release_type, weight in weights.items()
        if runtime_artist.type_cooldowns[release_type] <= 0
        and week_number >= runtime_artist.next_release_weeks[release_type]
        and base_cooloffs_for(runtime_artist.seed)[release_type] < 900
        and (runtime_artist.pending_major is None or release_type not in major_types)
    }
    if not available:
        return None
    if surprise_mode:
        # Surprise releases should feel like events, not the default release path.
        release_chance = min(0.035, 0.003 + (runtime_artist.seed.release_tendency / 4500.0))
    else:
        release_chance = min(0.88, 0.25 + (runtime_artist.seed.release_tendency / 140.0))
    if random.random() > release_chance:
        return None
    return weighted_choice(available)


def build_runtime_roster() -> list[EcosystemArtistRuntime]:
    roster: list[EcosystemArtistRuntime] = []
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        first_weeks = initial_release_weeks(seed)
        roster.append(
            EcosystemArtistRuntime(
                seed=seed,
                type_cooldowns=build_release_schedule(),
                first_release_weeks=first_weeks,
                next_release_weeks=dict(first_weeks),
            )
        )
    return roster


def maybe_release(runtime_artist: EcosystemArtistRuntime, week_number: int, world: "EcosystemWorld") -> WeeklyRelease | None:
    seed = runtime_artist.seed
    major_types = {"album", "ep", "mixtape"}
    rng = _seed_rng(f"release:{seed.name}:{week_number}")

    # Release queued project if it's due.
    if runtime_artist.pending_major is not None and week_number >= runtime_artist.pending_major.week_release:
        pending = runtime_artist.pending_major
        # Add any lead singles from the last 8 weeks that aren't already on the tracklist.
        singles = recent_singles(world, seed.name, week_number, window_weeks=8)
        existing_ids = {t.song_id for t in pending.tracks if t.song_id}
        for s in singles:
            if not getattr(s, "tracks", None):
                continue
            lead_track = s.tracks[0]
            if lead_track.song_id and lead_track.song_id in existing_ids:
                continue
            insert_at = random.randint(0, max(0, len(pending.tracks)))
            pending.tracks.insert(insert_at, lead_track)
            if lead_track.song_id:
                existing_ids.add(lead_track.song_id)

        pending.tracks = assign_project_track_reviews(
            pending.tracks,
            pending.release_type,
            f"{seed.name}:{pending.release_id}:{week_number}",
        )
        project_score = compute_project_score(
            pending.title,
            pending.core_genre,
            pending.core_theme,
            pending.tracks,
            pending.release_type,
        )
        runtime_artist.last_release_week = week_number
        runtime_artist.releases_made += 1
        apply_release_cooldowns(runtime_artist, pending.release_type, week_number)
        if runtime_artist.planned_followup_type == pending.release_type:
            runtime_artist.planned_followup_type = None
            runtime_artist.planned_followup_week = None

        release = WeeklyRelease(
            release_id=pending.release_id,
            artist_name=seed.name,
            release_type=pending.release_type,
            title=pending.title,
            genre=pending.core_genre,
            theme=pending.core_theme,
            review=float(project_score),
            week_number=week_number,
            quality=float(project_score),
            tracks=tuple(pending.tracks),
        )
        runtime_artist.pending_major = None
        world.pending_major_by_artist.pop(seed.name, None)
        return release

    release_type = choose_available_release_type(runtime_artist, week_number, surprise_mode=True)
    if release_type is None:
        return None
    genre = top_weighted_key(seed.genres)
    theme = top_weighted_key(seed.themes)

    # Major projects get queued and release 2-12 weeks later.
    if release_type in major_types:
        if runtime_artist.pending_major is not None:
            return None
        delay = random.randint(2, 12)
        release_week = week_number + delay
        title = release_title_for_type(release_type, genre, theme)
        project_ability = getattr(seed, "project_ability", None)
        if project_ability is None:
            # Derive project-making ability from consistency + mix/master + production.
            project_ability = (
                int(getattr(seed, "quality_consistency", 70)) * 0.55
                + int(seed.skills.get("mix/master", 50)) * 0.25
                + int(seed.skills.get("production", 50)) * 0.20
            )
        project_ability = int(max(35, min(98, round(project_ability))))
        target_len = _target_track_count(release_type)
        leads = recent_singles(world, seed.name, release_week, window_weeks=8)
        lead_tracks: list[ProjectTrack] = []
        for r in leads:
            if getattr(r, "tracks", None):
                lead_tracks.append(r.tracks[0])
            else:
                # Backward-compat: older history items may not have track details.
                lead_tracks.append(
                    ProjectTrack(
                        song_id="",
                        title=r.title,
                        genre=r.genre,
                        theme=r.theme,
                        quality=float(r.quality),
                        review=float(getattr(r, "review", 0.0)),
                    )
                )
        remaining = max(0, target_len - len(lead_tracks))
        new_tracks = build_project_tracks(seed, genre, theme, remaining, project_ability)
        # Apply collaborations to new songs (lead singles already have their own credits).
        collabbed = [apply_collaborations_to_track(world, seed, t, rng) for t in new_tracks]
        release_id = _new_release_id(seed.name, week_number)
        # Assign stable song ids to the new project tracks.
        fixed_collabbed: list[ProjectTrack] = []
        for idx, t in enumerate(collabbed, 1):
            fixed_collabbed.append(
                ProjectTrack(
                    song_id=_new_song_id(release_id, idx),
                    title=t.title,
                    genre=t.genre,
                    theme=t.theme,
                    quality=float(t.quality),
                    review=float(t.review),
                    lyricists=t.lyricists,
                    vocalists=t.vocalists,
                    producers=t.producers,
                    engineers=t.engineers,
                    features=t.features,
                    feature_qualities=t.feature_qualities,
                    bg_lyrics=t.bg_lyrics,
                    bg_vocals=t.bg_vocals,
                    bg_production=t.bg_production,
                    bg_mix=t.bg_mix,
                )
            )
        tracks = lead_tracks + fixed_collabbed
        pending = PendingRelease(
            release_id=release_id,
            artist_name=seed.name,
            release_type=release_type,
            title=title,
            core_genre=genre,
            core_theme=theme,
            tracks=tracks,
            week_created=week_number,
            week_release=release_week,
        )
        runtime_artist.pending_major = pending
        world.pending_major_by_artist[seed.name] = pending
        # Prevent repeatedly scheduling the same type while it's pending.
        runtime_artist.next_release_weeks[release_type] = release_week
        if runtime_artist.planned_followup_type == release_type:
            runtime_artist.planned_followup_type = None
            runtime_artist.planned_followup_week = None
        return None

    # Single releases immediately.
    title = release_title_for_type(release_type, genre, theme)
    review = float(integer_review(seed, genre, theme, release_type))
    quality = max(0.0, min(10.0, round(random.uniform(review - 0.6, review + 0.6), 1)))

    release_id = _new_release_id(seed.name, week_number)

    # Add producer/features to singles too.
    single_track = ProjectTrack(
        song_id=_new_song_id(release_id, 0),
        title=title,
        genre=genre,
        theme=theme,
        quality=float(quality),
        review=float(review),
    )
    single_track = apply_collaborations_to_track(world, seed, single_track, rng)
    title = single_track.title
    quality = float(single_track.quality)

    runtime_artist.last_release_week = week_number
    runtime_artist.releases_made += 1
    apply_release_cooldowns(runtime_artist, release_type, week_number)
    if release_type == "single":
        plan_single_followup(runtime_artist, week_number)
    if runtime_artist.planned_followup_type == release_type:
        runtime_artist.planned_followup_type = None
        runtime_artist.planned_followup_week = None

    return WeeklyRelease(
        release_id=release_id,
        artist_name=seed.name,
        release_type=release_type,
        title=title,
        genre=genre,
        theme=theme,
        review=float(review),
        week_number=week_number,
        quality=quality,
        tracks=(single_track,),
    )


def _project_ability_for_seed(seed: EcosystemArtistSeed) -> int:
    project_ability = getattr(seed, "project_ability", None)
    if project_ability is None:
        project_ability = (
            int(getattr(seed, "quality_consistency", 70)) * 0.55
            + int(seed.skills.get("mix/master", 50)) * 0.25
            + int(seed.skills.get("production", 50)) * 0.20
        )
    return int(max(35, min(98, round(project_ability))))


def _build_pending_release(
    runtime_artist: EcosystemArtistRuntime,
    week_created: int,
    week_release: int,
    world: "EcosystemWorld",
    release_type: str,
) -> PendingRelease | None:
    seed = runtime_artist.seed
    rng = _seed_rng(f"calendar:{seed.name}:{week_created}:{week_release}:{release_type}")
    genre = top_weighted_key(seed.genres)
    theme = top_weighted_key(seed.themes)
    release_id = _new_release_id(seed.name, week_created)
    title = release_title_for_type(release_type, genre, theme)

    if release_type in {"album", "ep", "mixtape"}:
        project_ability = _project_ability_for_seed(seed)
        target_len = _target_track_count(release_type)
        leads = recent_singles(world, seed.name, week_release, window_weeks=8)
        lead_tracks = [r.tracks[0] for r in leads if getattr(r, "tracks", None)]
        remaining = max(0, target_len - len(lead_tracks))
        new_tracks = build_project_tracks(seed, genre, theme, remaining, project_ability)
        collabbed = [apply_collaborations_to_track(world, seed, t, rng) for t in new_tracks]
        fixed_collabbed: list[ProjectTrack] = []
        for idx, t in enumerate(collabbed, 1):
            fixed_collabbed.append(
                ProjectTrack(
                    song_id=_new_song_id(release_id, idx),
                    title=t.title,
                    genre=t.genre,
                    theme=t.theme,
                    quality=float(t.quality),
                    review=float(t.review),
                    lyricists=t.lyricists,
                    vocalists=t.vocalists,
                    producers=t.producers,
                    engineers=t.engineers,
                    features=t.features,
                    feature_qualities=t.feature_qualities,
                    bg_lyrics=t.bg_lyrics,
                    bg_vocals=t.bg_vocals,
                    bg_production=t.bg_production,
                    bg_mix=t.bg_mix,
                )
            )
        return PendingRelease(
            release_id=release_id,
            artist_name=seed.name,
            release_type=release_type,
            title=title,
            core_genre=genre,
            core_theme=theme,
            tracks=lead_tracks + fixed_collabbed,
            week_created=week_created,
            week_release=week_release,
        )

    review = float(integer_review(seed, genre, theme, release_type))
    quality = max(0.0, min(10.0, round(rng.uniform(review - 0.6, review + 0.6), 1)))
    single_track = ProjectTrack(
        song_id=_new_song_id(release_id, 0),
        title=title,
        genre=genre,
        theme=theme,
        quality=float(quality),
        review=float(review),
    )
    single_track = apply_collaborations_to_track(world, seed, single_track, rng)
    return PendingRelease(
        release_id=release_id,
        artist_name=seed.name,
        release_type=release_type,
        title=single_track.title,
        core_genre=genre,
        core_theme=theme,
        tracks=[single_track],
        week_created=week_created,
        week_release=week_release,
    )


def _release_pending(world: EcosystemWorld, runtime_artist: EcosystemArtistRuntime, pending: PendingRelease, week_number: int) -> WeeklyRelease:
    seed = runtime_artist.seed
    if pending.release_type in {"album", "ep", "mixtape"}:
        singles = recent_singles(world, seed.name, week_number, window_weeks=8)
        existing_ids = {t.song_id for t in pending.tracks if t.song_id}
        for s in singles:
            if not getattr(s, "tracks", None):
                continue
            lead_track = s.tracks[0]
            if lead_track.song_id and lead_track.song_id in existing_ids:
                continue
            insert_at = random.randint(0, max(0, len(pending.tracks)))
            pending.tracks.insert(insert_at, lead_track)
            if lead_track.song_id:
                existing_ids.add(lead_track.song_id)

        pending.tracks = assign_project_track_reviews(
            pending.tracks,
            pending.release_type,
            f"{seed.name}:{pending.release_id}:{week_number}",
        )
        project_score = compute_project_score(
            pending.title,
            pending.core_genre,
            pending.core_theme,
            pending.tracks,
            pending.release_type,
        )
        review = float(project_score)
        quality = float(project_score)
        title = pending.title
    else:
        track = pending.tracks[0]
        review = float(track.review)
        quality = float(track.quality)
        title = track.title

    runtime_artist.last_release_week = week_number
    runtime_artist.releases_made += 1
    apply_release_cooldowns(runtime_artist, pending.release_type, week_number)
    if pending.release_type == "single":
        plan_single_followup(runtime_artist, week_number)
    if runtime_artist.planned_followup_type == pending.release_type:
        runtime_artist.planned_followup_type = None
        runtime_artist.planned_followup_week = None
    if runtime_artist.pending_major and runtime_artist.pending_major.release_id == pending.release_id:
        runtime_artist.pending_major = None
        world.pending_major_by_artist.pop(seed.name, None)

    return WeeklyRelease(
        release_id=pending.release_id,
        artist_name=seed.name,
        release_type=pending.release_type,
        title=title,
        genre=pending.core_genre,
        theme=pending.core_theme,
        review=review,
        week_number=week_number,
        quality=quality,
        tracks=tuple(pending.tracks),
    )


def _runtime_by_name(world: EcosystemWorld) -> dict[str, EcosystemArtistRuntime]:
    return {rt.seed.name: rt for rt in world.roster}


def _scheduled_artist_weeks(world: EcosystemWorld) -> set[tuple[str, int]]:
    out: set[tuple[str, int]] = set()
    for week, items in getattr(world, "announced_releases", {}).items():
        for pending in items:
            out.add((pending.artist_name, int(week)))
    for rt in world.roster:
        if rt.pending_major is not None:
            out.add((rt.seed.name, int(rt.pending_major.week_release)))
    return out


def _can_calendar_schedule(runtime_artist: EcosystemArtistRuntime, current_week: int, target_week: int, release_type: str) -> bool:
    if _is_engineer_only(runtime_artist.seed):
        return False
    if base_cooloffs_for(runtime_artist.seed)[release_type] >= 900:
        return False
    delta = max(0, int(target_week) - int(current_week))
    cooldown_left = max(0, int(runtime_artist.type_cooldowns.get(release_type, 0)) - delta)
    if cooldown_left > 0:
        return False
    if int(target_week) < int(runtime_artist.next_release_weeks.get(release_type, 999999)):
        return False
    if release_type in {"album", "ep", "mixtape"} and runtime_artist.pending_major is not None:
        return False
    return True


def prepare_release_calendar(world: EcosystemWorld, lookahead: int = 4) -> dict[int, list[PendingRelease]]:
    """Commit some releases into the next few weeks while leaving room for surprise drops."""
    if not hasattr(world, "announced_releases") or world.announced_releases is None:
        world.announced_releases = {}

    current = int(world.week_number)
    if int(getattr(world, "calendar_last_prepared_week", -1)) != current:
        scheduled = _scheduled_artist_weeks(world)
        major_types = {"album", "ep", "mixtape"}

        for offset in range(1, int(lookahead) + 1):
            target_week = current + offset
            world.announced_releases.setdefault(target_week, [])

            # Keep the calendar active, but don't overfill it. Normal surprise drops still happen in step_world.
            existing_count = len(world.announced_releases[target_week])
            # Calendar capacity should not throttle artists' actual release cadence.
            target_count = random.choices(
                [14, 16, 18, 20, 22, 24, 26],
                weights=[6, 12, 20, 26, 20, 12, 4],
                k=1,
            )[0]
            if existing_count >= target_count:
                continue

            candidates = list(world.roster)
            random.shuffle(candidates)
            for rt in candidates:
                if len(world.announced_releases[target_week]) >= target_count:
                    break
                if (rt.seed.name, target_week) in scheduled:
                    continue
                if any(rt.seed.name == p.artist_name for p in world.announced_releases[target_week]):
                    continue

                weights = ROLE_RELEASE_WEIGHTS.get(rt.seed.role, ROLE_RELEASE_WEIGHTS["rapper"])
                available = {
                    kind: weight
                    for kind, weight in weights.items()
                    if _can_calendar_schedule(rt, current, target_week, kind)
                }
                if not available:
                    continue

                reveal_chance = min(0.88, 0.25 + (rt.seed.release_tendency / 140.0))
                # The nearer a week is, the more likely an announcement appears late.
                reveal_chance *= {1: 1.35, 2: 1.05, 3: 0.85, 4: 0.70}.get(offset, 1.0)
                reveal_chance = min(0.95, reveal_chance)
                if random.random() > reveal_chance:
                    continue

                release_type = weighted_choice(available)
                pending = _build_pending_release(rt, current, target_week, world, release_type)
                if pending is None:
                    continue
                world.announced_releases[target_week].append(pending)
                scheduled.add((rt.seed.name, target_week))

                if release_type in major_types:
                    rt.pending_major = pending
                    world.pending_major_by_artist[rt.seed.name] = pending
                reserve_release_windows(rt, release_type, target_week)
        world.calendar_last_prepared_week = current

    # Include normal pending major projects in the visible window even if they were scheduled elsewhere.
    visible: dict[int, list[PendingRelease]] = {
        current + offset: list(world.announced_releases.get(current + offset, []))
        for offset in range(1, int(lookahead) + 1)
    }
    seen_ids = {p.release_id for items in visible.values() for p in items}
    for rt in world.roster:
        pending = rt.pending_major
        if pending is None:
            continue
        if current < int(pending.week_release) <= current + lookahead and pending.release_id not in seen_ids:
            visible.setdefault(int(pending.week_release), []).append(pending)
            seen_ids.add(pending.release_id)
    return visible


def simulate_week(week_number: int, roster: list[EcosystemArtistRuntime]) -> list[WeeklyRelease]:
    releases: list[WeeklyRelease] = []
    # Standalone sim doesn't keep pending state, so spin up a tiny world wrapper.
    tmp_world = EcosystemWorld(
        week_number=week_number - 1,
        roster=roster,
        last_week_releases=[],
        release_history={r.seed.name: [] for r in roster},
        pending_major_by_artist={},
        social_graph=build_social_graph([r.seed for r in roster]),
        songs_by_artist={r.seed.name: [] for r in roster},
        song_runtime={},
        artist_popularity={r.seed.name: float(r.seed.popularity) for r in roster},
        artist_reputation={r.seed.name: float(ARTIST_BASE_REPUTATION.get(r.seed.name, 50.0)) for r in roster},
        artist_popularity_controversy_offset={r.seed.name: 0.0 for r in roster},
        artist_reputation_controversy_offset={r.seed.name: 0.0 for r in roster},
        controversy_history_by_artist={r.seed.name: [] for r in roster},
        pending_responses_by_artist={r.seed.name: [] for r in roster},
        recent_low_reviews_by_artist={r.seed.name: [] for r in roster},
        releases_this_week_by_artist={r.seed.name: [] for r in roster},
        weekly_events={},
        announced_releases={},
        calendar_last_prepared_week=-1,
    )
    for runtime_artist in roster:
        for release_type, value in runtime_artist.type_cooldowns.items():
            runtime_artist.type_cooldowns[release_type] = max(0, value - 1)
        release = maybe_release(runtime_artist, week_number, tmp_world)
        if release is not None:
            releases.append(release)

    print(f"\nWeek {week_number}")
    print(f"Artists dropped: {len(releases)}")
    for release in releases:
        print(
            f"{release.artist_name} released {release.release_type} "
            f"'{release.title}' in genre {release.genre} and theme {release.theme} "
            f"| review: {release.review}/10 | week {release.week_number}"
        )
    return releases


def create_world(seeds: Iterable[EcosystemArtistSeed] | None = None) -> EcosystemWorld:
    if seeds is None:
        seeds = ARTIST_ECOSYSTEM_SEEDS
    roster = build_runtime_roster()
    history: dict[str, list[WeeklyRelease]] = {seed.name: [] for seed in seeds}
    return EcosystemWorld(
        week_number=0,
        roster=roster,
        last_week_releases=[],
        release_history=history,
        pending_major_by_artist={},
        social_graph=build_social_graph(list(seeds)),
        songs_by_artist={seed.name: [] for seed in seeds},
        song_runtime={},
        artist_popularity={seed.name: float(seed.popularity) for seed in seeds},
        artist_reputation={seed.name: float(ARTIST_BASE_REPUTATION.get(seed.name, 50.0)) for seed in seeds},
        artist_popularity_controversy_offset={seed.name: 0.0 for seed in seeds},
        artist_reputation_controversy_offset={seed.name: 0.0 for seed in seeds},
        controversy_history_by_artist={seed.name: [] for seed in seeds},
        pending_responses_by_artist={seed.name: [] for seed in seeds},
        recent_low_reviews_by_artist={seed.name: [] for seed in seeds},
        releases_this_week_by_artist={seed.name: [] for seed in seeds},
        weekly_events={},
        announced_releases={},
        calendar_last_prepared_week=-1,
    )


def step_world(world: EcosystemWorld) -> list[WeeklyRelease]:
    # Keep the release pipeline alive even when the player never opens the calendar UI.
    prepare_release_calendar(world, lookahead=4)
    world.week_number += 1
    releases: list[WeeklyRelease] = []
    for artist_name in list(world.releases_this_week_by_artist.keys()):
        world.releases_this_week_by_artist[artist_name] = []
    for runtime_artist in world.roster:
        for release_type, value in runtime_artist.type_cooldowns.items():
            runtime_artist.type_cooldowns[release_type] = max(0, value - 1)

    runtime_by_name = _runtime_by_name(world)
    due_announced = []
    if hasattr(world, "announced_releases") and world.announced_releases is not None:
        due_announced = list(world.announced_releases.pop(world.week_number, []))

    released_artists: set[str] = set()
    for pending in due_announced:
        runtime_artist = runtime_by_name.get(pending.artist_name)
        if runtime_artist is None:
            continue
        release = _release_pending(world, runtime_artist, pending, world.week_number)
        releases.append(release)
        released_artists.add(release.artist_name)
        world.release_history.setdefault(release.artist_name, []).append(release)
        world.releases_this_week_by_artist.setdefault(release.artist_name, []).append(release)

    for runtime_artist in world.roster:
        if runtime_artist.seed.name in released_artists:
            continue
        release = maybe_release(runtime_artist, world.week_number, world)
        if release is not None:
            releases.append(release)
            world.release_history.setdefault(release.artist_name, []).append(release)
            world.releases_this_week_by_artist.setdefault(release.artist_name, []).append(release)
    world.last_week_releases = releases
    _register_released_songs(world, releases)
    _step_ecosystem_streams(world)
    return releases


def _register_released_songs(world: EcosystemWorld, releases: list[WeeklyRelease]) -> None:
    for release in releases:
        if not getattr(release, "tracks", None):
            continue
        rng = _seed_rng(f"songmeta:{release.artist_name}:{release.release_id}")
        seed = next((rt.seed for rt in world.roster if rt.seed.name == release.artist_name), None)
        is_growing = False
        if seed is not None:
            is_growing = "growing" in classify_artist_skills(seed)
        project_label = "Single"
        if str(getattr(release, "release_type", "")) != "single":
            project_label = f"{release.title}({release.release_type})"
        for t in release.tracks:
            song_id = str(getattr(t, "song_id", "")) or _new_song_id(release.release_id, 0)
            if song_id in world.song_runtime:
                continue
            if is_growing:
                # Growing artists don't get catchiness/virality advantages yet.
                catchiness = 1.0
                virality, maturity = 1.0, 10_000
            else:
                catchiness = roll_catchiness_value(rng)
                virality, maturity = roll_virality_value_and_maturity(rng)
            world.song_runtime[song_id] = EcosystemSongRuntime(
                song_id=song_id,
                artist_name=release.artist_name,
                title=str(getattr(t, "title", release.title)),
                genre=str(getattr(t, "genre", release.genre)),
                theme=str(getattr(t, "theme", release.theme)),
                quality=float(getattr(t, "quality", release.quality)),
                review=float(getattr(t, "review", getattr(release, "review", 0.0))),
                release_week=int(getattr(release, "week_number", world.week_number)),
                catchiness=float(catchiness),
                virality=float(virality),
                maturity_weeks=int(maturity),
                lyricists=tuple(getattr(t, "lyricists", ())),
                vocalists=tuple(getattr(t, "vocalists", ())),
                producers=tuple(getattr(t, "producers", ())),
                engineers=tuple(getattr(t, "engineers", ())),
                features=tuple(getattr(t, "features", ())),
                feature_qualities=tuple(getattr(t, "feature_qualities", ())),
                is_growing=bool(is_growing),
                project_label=str(project_label),
            )
            world.songs_by_artist.setdefault(release.artist_name, []).append(song_id)


def _step_ecosystem_streams(world: EcosystemWorld) -> None:
    seed_by_name = {rt.seed.name: rt.seed for rt in world.roster}
    for song_id, s in list(world.song_runtime.items()):
        if s.weeks_since_release > 30:
            s.last_week_streams = int(s.last_week_streams * 0.95)
            if s.last_week_streams < 100:
                s.last_week_streams = 0
            s.total_streams += int(s.last_week_streams)
            s.weeks_since_release += 1
            if s.virality_triggered:
                s.virality_weeks_active += 1
            continue

        seed = seed_by_name.get(s.artist_name)
        if seed:
            pop = float(world.artist_popularity.get(s.artist_name, getattr(seed, "popularity", 0.0)))
        else:
            pop = float(world.artist_popularity.get(s.artist_name, 0.0))
        rng = _seed_rng(f"streams:{song_id}:{world.week_number}")
        s.last_week_streams = stream_count_for_ecosystem_song(s, pop, rng)
        s.total_streams += int(s.last_week_streams)
        s.weeks_since_release += 1
        if s.virality_triggered:
            s.virality_weeks_active += 1


def apply_feature_to_pending_release(
    world: EcosystemWorld,
    artist_name: str,
    release_id: str,
    track_index: int,
    feature_artist_name: str,
    verse_quality: float,
    current_week: int,
) -> bool:
    pending = world.pending_major_by_artist.get(artist_name)
    if not pending or pending.release_id != release_id:
        return False
    if track_index < 0 or track_index >= len(pending.tracks):
        return False
    track = pending.tracks[track_index]
    new_title = track.title
    # Insert feature name into the existing "ft." list if present, before the "(prod. ...)" suffix.
    prod_suffix = ""
    if "(prod." in new_title:
        head, prod_suffix = new_title.split("(prod.", 1)
        prod_suffix = "(prod." + prod_suffix
        head = head.rstrip()
    else:
        head = new_title

    if " ft. " in head:
        left, feat_part = head.split(" ft. ", 1)
        feat_names = [n.strip() for n in feat_part.split(",") if n.strip()]
        if feature_artist_name not in feat_names:
            feat_names.append(feature_artist_name)
        head = f"{left} ft. {', '.join(feat_names)}"
    else:
        head = f"{head} ft. {feature_artist_name}"
    new_title = (head + " " + prod_suffix).strip()

    base_quality = float(track.quality)
    raw_quality = (base_quality * 0.7) + (float(verse_quality) * 0.3)
    rng = _seed_rng(f"featapply:{artist_name}:{release_id}:{track_index}:{current_week}")
    new_quality = _apply_collaboration_caps(base_quality, raw_quality, rng)

    features = list(track.features)
    if feature_artist_name not in features:
        features.append(feature_artist_name)
    lyricists = list(track.lyricists)
    vocalists = list(track.vocalists)
    # Player verse implies writing + performance.
    if feature_artist_name not in lyricists:
        lyricists.append(feature_artist_name)
    if feature_artist_name not in vocalists:
        vocalists.append(feature_artist_name)
    feature_qualities = [
        (str(name), float(score))
        for name, score in getattr(track, "feature_qualities", ())
    ]
    if feature_artist_name not in {name for name, _ in feature_qualities}:
        feature_qualities.append((feature_artist_name, round(max(0.0, min(10.0, float(verse_quality))), 1)))

    pending.tracks[track_index] = ProjectTrack(
        song_id=track.song_id,
        title=new_title,
        genre=track.genre,
        theme=track.theme,
        quality=float(new_quality),
        review=float(getattr(track, "review", 0.0)),
        lyricists=tuple(lyricists),
        vocalists=tuple(vocalists),
        producers=tuple(track.producers),
        engineers=tuple(track.engineers),
        features=tuple(features),
        feature_qualities=tuple(feature_qualities),
        bg_lyrics=track.bg_lyrics,
        bg_vocals=track.bg_vocals,
        bg_production=track.bg_production,
        bg_mix=track.bg_mix,
    )
    # Release timing is controlled by the feature-request deadline window in career_mode.
    return True


def main():
    roster = build_runtime_roster()
    week_number = 1

    while True:
        simulate_week(week_number, roster)
        raw = input("\nPress x to simulate next week, or q to quit: ").strip().lower()
        if raw == "q":
            break
        if raw != "x":
            print("Invalid input. Use x to simulate or q to quit.")
            continue
        week_number += 1


if __name__ == "__main__":
    main()
