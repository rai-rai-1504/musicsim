"""rapsim_reviews.ratings_system
Hot 100 chart, IMDb user scores, song and album rating curves,
leaderboards, and project track views.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING

from rapsim_reviews.date_system import format_release_date, format_week_range
from rapsim_reviews.ui_helpers import (
    choose_from_list,
    meter_bar,
    money_fmt,
    prompt_text,
    clamp_meter,
    clamp_popularity,
    clamp_rating,
    clamp_signed_rating,
    _stable_rng_for_label,
)
from rapsim_reviews.career_models import (
    Artist,
    SongEntry,
    AlbumEntry,
    _player_week_index,
    _year_week_from_world_week,
    _ecosystem_seed_by_name,
    _ecosystem_artist_popularity,
    _find_world_runtime,
    _is_growing_artist_name,
)
from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS
from rapsim_reviews.artist_ecosystem_sim import classify_artist_skills
from rapsim_reviews.diss_track_system import ensure_diss_state

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld

def show_hot_100(player_artist, world: EcosystemWorld | None):
    rows = []

    # Player songs.
    for entry in player_artist.singles:
        if not entry.released:
            continue
        project = "Single"
        if str(getattr(entry, "source_label", "")).startswith("Album:"):
            project = f"{entry.source_label.replace('Album: ', '')}(album)"
        rows.append(
            {
                "title": entry.song.name,
                "artist": player_artist.name,
                "project": project,
                "release_week": int(entry.release_week_index or 0),
                "streams": int(entry.last_week_streams or 0),
            }
        )

    # Ecosystem songs.
    if world is not None:
        for song in world.song_runtime.values():
            title = str(getattr(song, "title", ""))
            artist_name = str(getattr(song, "artist_name", ""))
            prefix = f"{artist_name} - "
            if title.startswith(prefix):
                title = title[len(prefix) :]
            rows.append(
                {
                    "title": title,
                    "artist": artist_name,
                    "project": str(getattr(song, "project_label", "Single")),
                    "release_week": int(getattr(song, "release_week", 0)),
                    "streams": int(getattr(song, "last_week_streams", 0)),
                }
            )

    rows = [r for r in rows if r["streams"] > 0]
    if not rows:
        print("\nHOT 100")
        print("- No streams recorded last week.")
        return

    rows.sort(key=lambda r: r["streams"], reverse=True)
    rows = rows[:100]

    def date_label(week_index: int) -> str:
        if not week_index:
            return "-"
        return format_release_date(week_index)

    title_width = max(len("Title"), max((len(r["title"]) for r in rows), default=5))
    artist_width = max(len("Artist"), max((len(r["artist"]) for r in rows), default=6))
    project_width = max(len("Project"), max((len(r["project"]) for r in rows), default=7))

    print("\nHOT 100 (Last Week Streams)")
    print(
        f"{'Rank':<4}  "
        f"{'Title':<{title_width}}  "
        f"{'Artist':<{artist_width}}  "
        f"{'Project':<{project_width}}  "
        f"{'Release Date':<17}  "
        f"{'Streams Last Week':>16}"
    )
    for i, r in enumerate(rows, 1):
        print(
            f"{i:<4}  "
            f"{r['title']:<{title_width}}  "
            f"{r['artist']:<{artist_width}}  "
            f"{r['project']:<{project_width}}  "
            f"{date_label(r['release_week']):<17}  "
            f"{r['streams']:>16,}"
        )


def _current_rating_week(player_artist, world: EcosystemWorld | None = None) -> int:
    player_week = _player_week_index(player_artist)
    world_week = int(getattr(world, "week_number", 0) or 0)
    return max(player_week, world_week, 1)


def _rating_rng(song_key: str, week_number: int) -> random.Random:
    return _stable_rng_for_label(f"user-rating:{song_key}:w{int(week_number)}")


def _catchiness_to_rating_scale(catchiness) -> float:
    if catchiness is None:
        return 1.0
    return max(0.1, min(5.0, float(catchiness))) * 2.0


def _player_song_display_review(entry: SongEntry, album_review: float | None = None) -> float:
    if getattr(entry, "average_review", None) is not None:
        return float(entry.average_review)
    if album_review is not None:
        return float(album_review)
    return float(entry.song.quality)


def _ecosystem_song_display_review(runtime_song, track=None) -> float:
    if getattr(runtime_song, "review", None) is not None:
        return float(runtime_song.review)
    if track is not None and getattr(track, "review", None) is not None:
        return float(track.review)
    return float(getattr(runtime_song, "quality", 0.0))


def _virality_sentiment_adjustment(
    *,
    virality_triggered: bool,
    virality_value,
    virality_weeks_active: int,
    rng: random.Random,
) -> float:
    if not virality_triggered:
        return 0.0
    v = max(1.0, min(5.0, float(virality_value or 1.0)))
    age = max(0, int(virality_weeks_active))
    age_factor = max(0.35, 1.0 - (age / 14.0))
    ceiling = (0.08 + ((v - 1.0) / 4.0) * 0.32) * age_factor
    direction = 1.0 if rng.random() < 0.52 else -1.0
    return direction * rng.uniform(0.03, ceiling)


def _compute_user_rating_snapshot(
    *,
    song_key: str,
    review_score: float,
    catchiness,
    artist_popularity: float,
    last_week_streams: int,
    total_streams: int,
    virality_triggered: bool,
    virality_value,
    virality_weeks_active: int,
    week_number: int,
) -> dict:
    rng = _rating_rng(song_key, week_number)
    catchiness_score = _catchiness_to_rating_scale(catchiness)
    base_score = (float(review_score) * 0.85) + (catchiness_score * 0.15)
    artist_factor = max(0.0, min(1.0, float(artist_popularity) / 100.0))
    drift = rng.uniform(-0.4, 0.4)
    popularity_bias = (artist_factor - 0.5) * 0.08
    virality_adjustment = _virality_sentiment_adjustment(
        virality_triggered=virality_triggered,
        virality_value=virality_value,
        virality_weeks_active=virality_weeks_active,
        rng=rng,
    )
    weekly_shift = max(-0.5, min(0.5, drift + popularity_bias + virality_adjustment))
    score = clamp_rating(base_score + weekly_shift)
    score = round(score, 1)

    streams_for_votes = max(int(total_streams), int(last_week_streams), 1)
    votes = streams_for_votes * 0.08
    votes *= rng.uniform(0.97, 1.03)
    return {
        "score": score,
        "votes": max(1, int(round(votes))),
        "base_score": round(base_score, 2),
        "weekly_shift": round(weekly_shift, 2),
    }


def _player_song_imdb_snapshot(
    artist,
    entry: SongEntry,
    week_number: int,
    displayed_review: float | None = None,
) -> dict:
    song = entry.song
    return _compute_user_rating_snapshot(
        song_key=f"player:{artist.name}:{entry.release_week_index}:{entry.source_label}:{song.name}",
        review_score=(
            float(displayed_review)
            if displayed_review is not None
            else _player_song_display_review(entry)
        ),
        catchiness=getattr(song, "catchiness", None),
        artist_popularity=float(artist.popularity),
        last_week_streams=int(entry.last_week_streams or 0),
        total_streams=int(entry.total_streams or 0),
        virality_triggered=bool(getattr(entry, "virality_triggered", False)),
        virality_value=getattr(song, "virality", None),
        virality_weeks_active=int(getattr(entry, "virality_weeks_active", 0) or 0),
        week_number=week_number,
    )


def _ecosystem_song_imdb_snapshot(
    artist_name: str,
    runtime_song,
    track,
    artist_popularity: float,
    week_number: int,
) -> dict:
    return _compute_user_rating_snapshot(
        song_key=f"ecosystem:{artist_name}:{getattr(runtime_song, 'song_id', getattr(runtime_song, 'title', 'song'))}",
        review_score=_ecosystem_song_display_review(runtime_song, track),
        catchiness=getattr(runtime_song, "catchiness", None),
        artist_popularity=float(artist_popularity),
        last_week_streams=int(getattr(runtime_song, "last_week_streams", 0) or 0),
        total_streams=int(getattr(runtime_song, "total_streams", 0) or 0),
        virality_triggered=bool(getattr(runtime_song, "virality_triggered", False)),
        virality_value=getattr(runtime_song, "virality", None),
        virality_weeks_active=int(getattr(runtime_song, "virality_weeks_active", 0) or 0),
        week_number=week_number,
    )


def _project_imdb_summary(track_snapshots: list[dict]) -> tuple[float, int]:
    if not track_snapshots:
        return 0.0, 0
    score = sum(track["score"] for track in track_snapshots) / len(track_snapshots)
    votes = sum(track["votes"] for track in track_snapshots) / len(track_snapshots)
    return round(score, 1), max(1, int(round(votes)))


def _player_released_projects(artist) -> list[dict]:
    projects = []
    for entry in artist.singles:
        if not entry.released:
            continue
        if str(getattr(entry, "source_label", "")).startswith("Album:"):
            continue
        projects.append(
            {
                "project_id": f"player-single:{entry.release_week_index}:{entry.song.name}",
                "title": entry.song.name,
                "release_type": "single",
                "release_week": int(entry.release_week_index or 0),
                "tracks": [{"title": entry.song.name, "song": entry.song, "entry": entry}],
            }
        )
    for album_entry in artist.albums:
        if not album_entry.released:
            continue
        tracks = []
        release_week = 0
        for song in album_entry.album.songs:
            linked_entry = next((e for e in artist.singles if e.song is song and e.released), None)
            if linked_entry is not None:
                release_week = max(release_week, int(linked_entry.release_week_index or 0))
            tracks.append({"title": song.name, "song": song, "entry": linked_entry})
        release_type = "deluxe" if album_entry.deluxe_of else "album"
        projects.append(
            {
                "project_id": f"player-project:{release_type}:{album_entry.album.name}:{release_week}",
                "title": album_entry.album.name,
                "release_type": release_type,
                "release_week": release_week,
                "tracks": tracks,
            }
        )
    projects.sort(key=lambda project: (project["release_week"], project["title"].lower()), reverse=True)
    return projects


def _player_project_imdb_view(project: dict, artist, week_number: int) -> dict:
    track_rows = []
    album_review = None
    if project["release_type"] in {"album", "deluxe"}:
        album_entry = next(
            (
                entry for entry in artist.albums
                if entry.released and entry.album.name == project["title"]
            ),
            None,
        )
        if album_entry is not None and album_entry.average_review is not None:
            album_review = float(album_entry.average_review)
    for track in project["tracks"]:
        entry = track["entry"]
        if entry is None or not getattr(entry, "released", False):
            continue
        review_score = _player_song_display_review(entry, album_review=album_review)
        snapshot = _player_song_imdb_snapshot(
            artist,
            entry,
            week_number,
            displayed_review=review_score,
        )
        track_rows.append(
            {
                "title": track["title"],
                "score": snapshot["score"],
                "votes": snapshot["votes"],
                "review": review_score,
                "catchiness": getattr(entry.song, "catchiness", None),
                "streams": int(entry.total_streams or 0),
                "last_week_streams": int(entry.last_week_streams or 0),
                "viral": bool(entry.virality_triggered),
            }
        )
    score, votes = _project_imdb_summary(track_rows)
    return {
        "title": project["title"],
        "release_type": project["release_type"],
        "release_week": project["release_week"],
        "score": score,
        "votes": votes,
        "tracks": track_rows,
    }


def _ecosystem_project_imdb_view(world: EcosystemWorld, release, artist_popularity: float, week_number: int) -> dict:
    artist_name = str(getattr(release, "artist_name", ""))
    prefix = f"{artist_name} - "
    track_rows = []
    for track in list(getattr(release, "tracks", None) or ()):
        runtime_song = world.song_runtime.get(getattr(track, "song_id", ""))
        if runtime_song is None:
            continue
        snapshot = _ecosystem_song_imdb_snapshot(artist_name, runtime_song, track, artist_popularity, week_number)
        title = str(getattr(track, "title", ""))
        if title.startswith(prefix):
            title = title[len(prefix) :]
        review_score = _ecosystem_song_display_review(runtime_song, track)
        track_rows.append(
            {
                "title": title,
                "score": snapshot["score"],
                "votes": snapshot["votes"],
                "review": review_score,
                "catchiness": getattr(runtime_song, "catchiness", None),
                "streams": int(getattr(runtime_song, "total_streams", 0) or 0),
                "last_week_streams": int(getattr(runtime_song, "last_week_streams", 0) or 0),
                "viral": bool(getattr(runtime_song, "virality_triggered", False)),
            }
        )
    score, votes = _project_imdb_summary(track_rows)
    title = str(getattr(release, "title", ""))
    if title.startswith(prefix):
        title = title[len(prefix) :]
    return {
        "title": title,
        "release_type": str(getattr(release, "release_type", "single")),
        "release_week": int(getattr(release, "week_number", 0) or 0),
        "score": score,
        "votes": votes,
        "tracks": track_rows,
    }


def _imdb_release_date_label(week_index: int) -> str:
    if not week_index:
        return "-"
    return format_release_date(week_index)


def _print_imdb_project_tracks(project_view: dict) -> None:
    print(
        f"\n{project_view['title']} [{project_view['release_type']}]"
        f" | user score {project_view['score']}/10 | users rated {project_view['votes']:,}"
    )
    if not project_view["tracks"]:
        print("- No released tracks available yet.")
        return
    title_width = max(len("Track"), max(len(track["title"]) for track in project_view["tracks"]))
    print(
        f"{'Track':<{title_width}}  {'User':>6}  {'Users':>8}  {'Review':>7}  "
        f"{'Catchy':>6}  {'Last Wk':>10}  {'Total':>10}"
    )
    for track in project_view["tracks"]:
        catchy = "-" if track["catchiness"] is None else f"{float(track['catchiness']):.2f}"
        viral_tag = " viral" if track["viral"] else ""
        print(
            f"{track['title']:<{title_width}}  "
            f"{track['score']:>4.1f}/10  "
            f"{track['votes']:>8,}  "
            f"{track['review']:>4.1f}/10  "
            f"{catchy:>6}  "
            f"{track['last_week_streams']:>10,}  "
            f"{track['streams']:>10,}{viral_tag}"
        )


def _release_year_bounds(week_number: int) -> tuple[int, int, int]:
    year, _ = _year_week_from_world_week(week_number)
    start = ((year - 1) * 52) + 1
    end = year * 52
    return year, start, end


def _strip_artist_prefix(title: str, artist_name: str) -> str:
    prefix = f"{artist_name} - "
    if str(title).startswith(prefix):
        return str(title)[len(prefix) :]
    return str(title)


def _player_song_project_label(entry: SongEntry) -> str:
    source = str(getattr(entry, "source_label", "") or "Single")
    if source.startswith("Album: "):
        return source.split(": ", 1)[1]
    return "Single"


def _collect_project_rating_rows(player_artist, world: EcosystemWorld | None, week_number: int) -> list[dict]:
    rows: list[dict] = []

    for project in _player_released_projects(player_artist):
        if project["release_type"] != "album":
            continue
        view = _player_project_imdb_view(project, player_artist, week_number)
        rows.append(
            {
                "artist": player_artist.name,
                "title": project["title"],
                "release_type": "album",
                "score": float(view["score"]),
                "votes": int(view["votes"]),
                "release_week": int(project["release_week"] or 0),
                "track_count": len(view["tracks"]),
            }
        )

    if world is not None:
        for artist_name, releases in world.release_history.items():
            seed = _ecosystem_seed_by_name(artist_name)
            artist_popularity = float(world.artist_popularity.get(artist_name, getattr(seed, "popularity", 0.0) if seed else 0.0))
            for release in releases:
                release_type = str(getattr(release, "release_type", ""))
                if release_type not in {"album", "mixtape"}:
                    continue
                view = _ecosystem_project_imdb_view(world, release, artist_popularity, week_number)
                rows.append(
                    {
                        "artist": artist_name,
                        "title": view["title"],
                        "release_type": release_type,
                        "score": float(view["score"]),
                        "votes": int(view["votes"]),
                        "release_week": int(view["release_week"] or 0),
                        "track_count": len(view["tracks"]),
                    }
                )
    return rows


def _collect_song_rating_rows(player_artist, world: EcosystemWorld | None, week_number: int) -> list[dict]:
    rows: list[dict] = []

    player_album_reviews = {
        entry.album.name: float(entry.average_review or 0.0)
        for entry in player_artist.albums
        if entry.released and entry.average_review is not None
    }
    for entry in player_artist.singles:
        if not entry.released:
            continue
        project_label = _player_song_project_label(entry)
        album_review = player_album_reviews.get(project_label) if project_label != "Single" else None
        review_score = _player_song_display_review(entry, album_review=album_review)
        snapshot = _player_song_imdb_snapshot(
            player_artist,
            entry,
            week_number,
            displayed_review=review_score,
        )
        rows.append(
            {
                "artist": player_artist.name,
                "title": entry.song.name,
                "project": project_label,
                "score": float(snapshot["score"]),
                "votes": int(snapshot["votes"]),
                "review": float(review_score),
                "release_week": int(entry.release_week_index or 0),
                "streams": int(entry.total_streams or 0),
            }
        )

    if world is not None:
        for runtime_song in world.song_runtime.values():
            snapshot = _ecosystem_song_imdb_snapshot(
                runtime_song.artist_name,
                runtime_song,
                runtime_song,
                float(world.artist_popularity.get(runtime_song.artist_name, 0.0)),
                week_number,
            )
            rows.append(
                {
                    "artist": str(runtime_song.artist_name),
                    "title": _strip_artist_prefix(str(runtime_song.title), str(runtime_song.artist_name)),
                    "project": str(getattr(runtime_song, "project_label", "Single")),
                    "score": float(snapshot["score"]),
                    "votes": int(snapshot["votes"]),
                    "review": float(_ecosystem_song_display_review(runtime_song, runtime_song)),
                    "release_week": int(getattr(runtime_song, "release_week", 0) or 0),
                    "streams": int(getattr(runtime_song, "total_streams", 0) or 0),
                }
            )
    return rows


def _collect_artist_rating_rows(player_artist, world: EcosystemWorld | None, week_number: int) -> list[dict]:
    stats: dict[str, dict] = {}

    def ensure_row(name: str, *, growing: bool) -> dict:
        if name not in stats:
            stats[name] = {"artist": name, "scores": [], "votes": 0, "growing": growing}
        return stats[name]

    for project in _player_released_projects(player_artist):
        view = _player_project_imdb_view(project, player_artist, week_number)
        row = ensure_row(player_artist.name, growing=False)
        row["scores"].append(float(view["score"]))
        row["votes"] += int(view["votes"])

    if world is not None:
        seed_lookup = {seed.name: seed for seed in ARTIST_ECOSYSTEM_SEEDS}
        for artist_name, releases in world.release_history.items():
            seed = seed_lookup.get(artist_name)
            growing = bool(seed is not None and "growing" in classify_artist_skills(seed))
            artist_popularity = float(world.artist_popularity.get(artist_name, getattr(seed, "popularity", 0.0) if seed else 0.0))
            for release in releases:
                view = _ecosystem_project_imdb_view(world, release, artist_popularity, week_number)
                row = ensure_row(artist_name, growing=growing)
                row["scores"].append(float(view["score"]))
                row["votes"] += int(view["votes"])

    rows: list[dict] = []
    for row in stats.values():
        if not row["scores"]:
            continue
        rows.append(
            {
                "artist": row["artist"],
                "score": round(sum(row["scores"]) / len(row["scores"]), 2),
                "release_count": len(row["scores"]),
                "votes": int(row["votes"]),
                "growing": bool(row["growing"]),
            }
        )
    return rows


def _print_ratings_chart_header(title: str, subtitle: str) -> None:
    print(f"\n{title}")
    print(subtitle)
    print("-" * max(len(title), len(subtitle), 72))


def _print_project_leaderboard(rows: list[dict], *, title: str, limit: int) -> None:
    _print_ratings_chart_header(
        title,
        "User ratings move every week based on review, catchiness, virality, and live sentiment.",
    )
    if not rows:
        print("No eligible projects yet.")
        return
    artist_w = max(len("Artist"), max(len(str(r["artist"])) for r in rows[:limit]))
    title_w = max(len("Project"), max(len(str(r["title"])) for r in rows[:limit]))
    print(
        f"{'RK':>3}  {'Project':<{title_w}}  {'Artist':<{artist_w}}  {'Type':<7}  "
        f"{'User':>6}  {'Votes':>9}  {'Date':<17}  {'Tracks':>6}"
    )
    for idx, row in enumerate(rows[:limit], 1):
        print(
            f"{idx:>3}  {row['title']:<{title_w}}  {row['artist']:<{artist_w}}  "
            f"{row['release_type']:<7}  {row['score']:>4.1f}/10  {row['votes']:>9,}  "
            f"{_imdb_release_date_label(row['release_week']):<17}  {row['track_count']:>6}"
        )


def _print_song_leaderboard(rows: list[dict], *, title: str, limit: int) -> None:
    _print_ratings_chart_header(
        title,
        "Singles and project cuts all compete here. Same score engine, same weekly reshuffle.",
    )
    if not rows:
        print("No eligible songs yet.")
        return
    artist_w = max(len("Artist"), max(len(str(r["artist"])) for r in rows[:limit]))
    title_w = max(len("Song"), max(len(str(r["title"])) for r in rows[:limit]))
    project_w = max(len("Project"), max(len(str(r["project"])) for r in rows[:limit]))
    print(
        f"{'RK':>3}  {'Song':<{title_w}}  {'Artist':<{artist_w}}  {'Project':<{project_w}}  "
        f"{'User':>6}  {'Votes':>9}  {'Date':<17}  {'Streams':>12}"
    )
    for idx, row in enumerate(rows[:limit], 1):
        print(
            f"{idx:>3}  {row['title']:<{title_w}}  {row['artist']:<{artist_w}}  {row['project']:<{project_w}}  "
            f"{row['score']:>4.1f}/10  {row['votes']:>9,}  {_imdb_release_date_label(row['release_week']):<17}  "
            f"{row['streams']:>12,}"
        )


def _collect_diss_rating_rows(world: EcosystemWorld | None) -> list[dict]:
    if world is None:
        return []
    ensure_diss_state(world)
    rows = []
    for track in world.diss_tracks:
        true_count = len(getattr(track, "true_claims", []) or [])
        claim_count = len(getattr(track, "claims", []) or [])
        credibility = (true_count / claim_count * 10.0) if claim_count else 5.0
        rows.append(
            {
                "artist": track.instigator,
                "target": track.target,
                "title": track.title,
                "score": float(track.user_rating),
                "reception": float(track.reception_score),
                "quality": float(track.quality),
                "brutality": float(track.brutality),
                "credibility": float(credibility),
                "release_week": int(track.week_released),
                "streams": int(track.total_streams or 0),
            }
        )
    return rows


def _print_diss_leaderboard(rows: list[dict], *, title: str, limit: int = 20) -> None:
    _print_ratings_chart_header(
        title,
        "Diss rating uses the diss track user score; reception is quality 60%, credibility 25%, brutality 15%. "
        "Streams use the same popularity/quality/catchiness curve as singles, plus virality.",
    )
    if not rows:
        print("No diss tracks have been released yet.")
        return
    artist_w = max(len("Artist"), max(len(str(r["artist"])) for r in rows[:limit]))
    target_w = max(len("Target"), max(len(str(r["target"])) for r in rows[:limit]))
    title_w = max(len("Diss Track"), max(len(str(r["title"])) for r in rows[:limit]))
    print(
        f"{'RK':>3}  {'Diss Track':<{title_w}}  {'Artist':<{artist_w}}  {'Target':<{target_w}}  "
        f"{'User':>6}  {'Rec':>5}  {'Cred':>5}  {'Brut':>5}  {'Date':<17}  {'Streams':>12}"
    )
    for idx, row in enumerate(rows[:limit], 1):
        print(
            f"{idx:>3}  {row['title']:<{title_w}}  {row['artist']:<{artist_w}}  {row['target']:<{target_w}}  "
            f"{row['score']:>4.1f}/10  {row['reception']:>4.1f}  {row['credibility']:>4.1f}  "
            f"{row['brutality']:>4.1f}  {_imdb_release_date_label(row['release_week']):<17}  {row['streams']:>12,}"
        )


def _print_artist_leaderboard(rows: list[dict], *, title: str, limit: int, hated: bool = False) -> None:
    _print_ratings_chart_header(
        title,
        "Artist score = average user rating across all recorded releases. Small sample artists are filtered out.",
    )
    if not rows:
        print("No eligible artists yet.")
        return
    artist_w = max(len("Artist"), max(len(str(r["artist"])) for r in rows[:limit]))
    vibe_label = "Hate" if hated else "Love"
    print(
        f"{'RK':>3}  {'Artist':<{artist_w}}  {'Avg':>6}  {'Releases':>8}  {'Votes':>10}  {vibe_label:>6}"
    )
    for idx, row in enumerate(rows[:limit], 1):
        meter = (10.0 - float(row["score"])) if hated else float(row["score"])
        print(
            f"{idx:>3}  {row['artist']:<{artist_w}}  {row['score']:>4.1f}/10  "
            f"{row['release_count']:>8}  {row['votes']:>10,}  {meter:>4.1f}"
        )


def _view_player_user_ratings_menu(player_artist, world: EcosystemWorld | None) -> None:
    projects = _player_released_projects(player_artist)
    if not projects:
        print("\nNo released music from you is showing on IMDb yet.")
        return
    week_number = _current_rating_week(player_artist, world)
    while True:
        labels = []
        project_views = []
        for project in projects:
            view = _player_project_imdb_view(project, player_artist, week_number)
            project_views.append(view)
            labels.append(
                f"{view['release_type']} | {view['title']} | {view['score']}/10 | "
                f"{view['votes']:,} users | {_imdb_release_date_label(view['release_week'])}"
            )
        idx = choose_from_list("Your User Ratings (IMDb)", labels + ["Back"], allow_cancel=False)
        if idx is None or idx == len(labels):
            return
        _print_imdb_project_tracks(project_views[idx])
        input("\nPress Enter to go back...")


def _view_ecosystem_user_ratings_menu(player_artist, world: EcosystemWorld, artist_name: str) -> None:
    releases = list(world.release_history.get(artist_name, []))
    if not releases:
        print("\nNo releases recorded yet.")
        return
    seed = _ecosystem_seed_by_name(artist_name)
    artist_popularity = float(getattr(seed, "popularity", 0.0)) if seed else 0.0
    week_number = _current_rating_week(player_artist, world)
    while True:
        labels = []
        project_views = []
        for release in releases:
            view = _ecosystem_project_imdb_view(world, release, artist_popularity, week_number)
            project_views.append(view)
            labels.append(
                f"{view['release_type']} | {view['title']} | {view['score']}/10 | "
                f"{view['votes']:,} users | {_imdb_release_date_label(view['release_week'])}"
            )
        idx = choose_from_list(f"{artist_name} User Ratings (IMDb)", labels + ["Back"], allow_cancel=False)
        if idx is None or idx == len(labels):
            return
        _print_imdb_project_tracks(project_views[idx])
        input("\nPress Enter to go back...")


def user_ratings_menu(player_artist, world: EcosystemWorld | None) -> None:
    print("\nUSER RATINGS CENTRAL")
    print("Song user score = 85% review + 15% catchiness, then weekly sentiment and virality nudge it around.")
    print("Project user score = average of that project's song user scores. Every chart below can change every week.")

    entries = [
        {
            "name": player_artist.name,
            "kind": "player",
            "popularity": float(player_artist.popularity),
            "streams": sum(int(entry.total_streams or 0) for entry in player_artist.singles if entry.released),
        }
    ]
    if world is not None:
        for seed in sorted(ARTIST_ECOSYSTEM_SEEDS, key=lambda s: s.name.lower()):
            total_streams = 0
            for sid in world.songs_by_artist.get(seed.name, []):
                runtime_song = world.song_runtime.get(sid)
                if runtime_song is not None:
                    total_streams += int(getattr(runtime_song, "total_streams", 0) or 0)
            entries.append(
                {
                    "name": seed.name,
                    "kind": "ecosystem",
                    "popularity": float(seed.popularity),
                    "streams": total_streams,
                }
            )

    while True:
        current_week = _current_rating_week(player_artist, world)
        current_year, start_week, end_week = _release_year_bounds(current_week)
        choice = choose_from_list(
            "Ratings menu",
            [
                "Browse artist IMDb pages",
                "Top 100 rated projects of all time",
                f"Top 50 rated albums/mixtapes of Year {current_year}",
                "Top 20 rated artists of all time",
                "Top 10 hated artists of all time",
                "Top 100 rated songs of all time",
                f"Top 50 rated songs of Year {current_year}",
                "Top 20 rated diss tracks of all time",
                "Back",
            ],
            allow_cancel=False,
        )
        if choice == 8:
            return
        if choice == 0:
            options = []
            for row in entries:
                tag = "you" if row["kind"] == "player" else "ecosystem"
                options.append(
                    f"{row['name']} | {tag} | pop {row['popularity']:.1f} | streams {row['streams']:,}"
                )
            idx = choose_from_list("Choose an artist", options, allow_cancel=True)
            if idx is None:
                continue
            chosen = entries[idx]
            if chosen["kind"] == "player":
                _view_player_user_ratings_menu(player_artist, world)
            elif world is not None:
                _view_ecosystem_user_ratings_menu(player_artist, world, chosen["name"])
            continue

        if choice in {1, 2}:
            rows = _collect_project_rating_rows(player_artist, world, current_week)
            rows = sorted(rows, key=lambda r: (-r["score"], -r["votes"], -r["release_week"], r["title"].lower()))
            if choice == 2:
                rows = [r for r in rows if start_week <= int(r["release_week"]) <= end_week]
            label = (
                "Top 100 Rated Projects of All Time"
                if choice == 1
                else f"Top 50 Rated Albums/Mixtapes of Year {current_year}"
            )
            _print_project_leaderboard(rows, title=label, limit=(100 if choice == 1 else 50))
            input("\nPress Enter to go back...")
            continue

        if choice in {3, 4}:
            rows = _collect_artist_rating_rows(player_artist, world, current_week)
            rows = [r for r in rows if int(r["release_count"]) >= 2]
            if choice == 4:
                rows = [r for r in rows if not r["growing"]]
                rows = sorted(rows, key=lambda r: (r["score"], -r["release_count"], -r["votes"], r["artist"].lower()))
                _print_artist_leaderboard(rows, title="Top 10 Hated Artists of All Time", limit=10, hated=True)
            else:
                rows = sorted(rows, key=lambda r: (-r["score"], -r["release_count"], -r["votes"], r["artist"].lower()))
                _print_artist_leaderboard(rows, title="Top 20 Rated Artists of All Time", limit=20, hated=False)
            input("\nPress Enter to go back...")
            continue

        if choice in {5, 6}:
            rows = _collect_song_rating_rows(player_artist, world, current_week)
            rows = sorted(rows, key=lambda r: (-r["score"], -r["votes"], -r["streams"], -r["release_week"], r["title"].lower()))
            if choice == 6:
                rows = [r for r in rows if start_week <= int(r["release_week"]) <= end_week]
            label = (
                "Top 100 Rated Songs of All Time"
                if choice == 5
                else f"Top 50 Rated Songs of Year {current_year}"
            )
            _print_song_leaderboard(rows, title=label, limit=(100 if choice == 5 else 50))
            input("\nPress Enter to go back...")
            continue

        if choice == 7:
            rows = _collect_diss_rating_rows(world)
            rows = sorted(rows, key=lambda r: (-r["score"], -r["streams"], -r["reception"], -r["release_week"], r["title"].lower()))
            _print_diss_leaderboard(rows, title="Top 20 Rated Diss Tracks of All Time", limit=20)
            input("\nPress Enter to go back...")

