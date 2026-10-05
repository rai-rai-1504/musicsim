"""rapsim_reviews.catalog_system
Player catalog management (drafts, tracklists, deletions), single and album releases,
ecosystem artist discography inspection, and release calendar viewer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING

from rapsim_reviews.date_system import format_release_date, format_week_range
from rapsim_reviews.ui_helpers import (
    choose_from_list,
    choose_item_from_list,
    prompt_text,
    prompt_int,
    money_fmt,
    _stable_rng_for_label,
)
from rapsim_reviews.album_review import MIN_SONGS
from rapsim_reviews.album_review.base import Album
from rapsim_reviews.track_review.base import GENRES, THEMES
from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS, ARTIST_LOVINGNESS
from rapsim_reviews.artist_ecosystem_sim import (
    prepare_release_calendar,
    roll_catchiness_value,
    roll_virality_value_and_maturity,
)
from rapsim_reviews.career_models import (
    Artist,
    SongEntry,
    AlbumEntry,
    release_bump_for_quality,
    _player_week_index,
    _ecosystem_seed_by_name,
    _ecosystem_artist_popularity,
    _ecosystem_artist_reputation,
    _ensure_song_bg_attrs,
)
from rapsim_reviews.sales_system import (
    _ensure_sales_state,
    _world_release_sales,
    _riaa_certification_label,
    _player_song_sales_snapshot,
    _player_album_sales_snapshot,
    _physical_stock_summary,
    manage_physical_copies_menu,
)
from rapsim_reviews.feature_system import send_feature_request_menu
from rapsim_reviews.romance_system import (
    _artist_lovingness,
    _get_romance_profile,
    _romance_status_label,
    _current_romance_duration,
    _format_week_span,
    _romance_week_label,
    _separation_status_label,
)
from rapsim_reviews.feature_system import _roll_bg_attr_from_skill_rng

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld
    from rapsim_reviews.track_review.base import Simulation
    from rapsim_reviews.album_review.base import AlbumSimulation

def list_catalog(artist):
    print("\nSingles")
    singles = [e for e in artist.singles if e.source_label == "Single"]
    if singles:
        for idx, entry in enumerate(singles, 1):
            status = "released" if entry.released else "unreleased"
            sales = _player_song_sales_snapshot(entry) if entry.released else None
            rating = (
                f" | avg reviews: {entry.average_review}/10"
                if entry.average_review is not None
                else ""
            )
            sales_label = ""
            if sales is not None:
                sales_label = (
                    f" | sales fw {sales.first_week_sales:,} / lw {sales.last_week_sales:,} / total {sales.total_sales:,}"
                )
            print(
                f"- {idx}. {entry.song.name} | {entry.song.quality}/10 | "
                f"{entry.song.genre_label()} | {status}{rating}{sales_label}"
            )
    else:
        print("- None")

    print("\nAlbums")
    if artist.albums:
        for idx, entry in enumerate(artist.albums, 1):
            status = "released" if entry.released else "draft"
            tag = "deluxe" if entry.deluxe_of else "album"
            sales_label = ""
            if entry.released:
                snapshot = _player_album_sales_snapshot(artist, entry)
                sales_label = (
                    f" | sales fw {snapshot.first_week_sales:,} / lw {snapshot.last_week_sales:,} / total {snapshot.total_sales:,}"
                )
            print(
                f"- {idx}. {entry.album.name} | {entry.album.song_count()} tracks | "
                f"{tag} | {status}{sales_label}"
            )
    else:
        print("- None")


def delete_single_entry(artist):
    singles = [e for e in artist.singles if e.source_label == "Single"]
    if not singles:
        print("No singles available to delete.")
        return
    options = [
        f"{entry.song.name} | {'released' if entry.released else 'unreleased'} | {entry.source_label}"
        for entry in singles
    ]
    idx = choose_from_list("Choose a single entry to delete", options, allow_cancel=True)
    if idx is None:
        return
    removed = singles[idx]
    artist.singles.remove(removed)
    print(f"Deleted single entry for '{removed.song.name}'.")


def create_album_entry():
    album_name = prompt_text("Album name: ", "Untitled Album")
    core_genre = GENRES[choose_from_list("Choose album core genre", GENRES)]
    core_theme = THEMES[choose_from_list("Choose album core theme", THEMES)]
    album = Album(album_name, core_genre, core_theme)
    return AlbumEntry(album=album)


def choose_album_draft(artist, allow_create=False):
    drafts = [entry for entry in artist.albums if not entry.released]
    if not drafts:
        if allow_create:
            create_new = prompt_text("No draft albums. Create one now? (y/n): ", "y")
            if create_new.lower() == "y":
                entry = create_album_entry()
                artist.albums.append(entry)
                return entry
        print("No draft albums available.")
        return None

    options = []
    if allow_create:
        options.append("Create a new album draft")
    for entry in drafts:
        tag = "Deluxe" if entry.deluxe_of else "Album"
        options.append(f"{entry.album.name} [{tag}] - {entry.album.song_count()} tracks")

    idx = choose_from_list("Choose album draft", options, allow_cancel=True)
    if idx is None:
        return None
    if allow_create:
        if idx == 0:
            entry = create_album_entry()
            artist.albums.append(entry)
            return entry
        return drafts[idx - 1]
    return drafts[idx]


def add_single_to_album(artist):
    singles = [e for e in artist.singles if e.source_label == "Single"]
    if not singles:
        print("No singles available to add.")
        return
    album_entry = choose_album_draft(artist, allow_create=True)
    if album_entry is None:
        return
    options = [
        f"{entry.song.name} | {'released' if entry.released else 'unreleased'} | {entry.source_label}"
        for entry in singles
    ]
    idx = choose_from_list(
        f"Choose a single to add to '{album_entry.album.name}'",
        options,
        allow_cancel=True,
    )
    if idx is None:
        return
    entry = singles[idx]
    if entry.song in album_entry.album.songs:
        print(f"'{entry.song.name}' is already on '{album_entry.album.name}'.")
        return
    album_entry.album.add_song(entry.song)
    # Hide it from Singles once it belongs to an album draft. We'll still track streams when released.
    entry.source_label = f"Album Draft: {album_entry.album.name}"
    print(f"Added '{entry.song.name}' to '{album_entry.album.name}'.")


def view_player_song_metadata_menu(artist):
    if not artist.singles:
        print("No songs available.")
        return
    options = []
    entries = list(artist.singles)
    for e in entries:
        status = "released" if e.released else "unreleased"
        options.append(f"{e.song.name} | {status} | {e.source_label}")
    idx = choose_from_list("Choose a song", options, allow_cancel=True)
    if idx is None:
        return
    e = entries[idx]
    s = e.song
    print("\nMetadata")
    print(f"Title   : {s.name}")
    print(f"Quality : {s.quality}/10")
    print(f"Genre   : {s.genre_label()}")
    print(f"Theme   : {s.theme}")
    if getattr(s, "catchiness", None) is not None:
        print(f"Catchy  : {s.catchiness}")
    if getattr(s, "virality", None) is not None and getattr(s, "maturity_weeks", None) is not None:
        remaining = max(0, int(s.maturity_weeks) - int(e.weeks_since_release))
        print(f"Virality: {s.virality} | matures in {remaining}w")
    if getattr(s, "bg_lyrics", None) is not None:
        print(f"Lyrics  : {s.bg_lyrics}/10")
    if getattr(s, "bg_vocals", None) is not None:
        print(f"Vocals  : {s.bg_vocals}/10")
    if getattr(s, "bg_production", None) is not None:
        print(f"Prod    : {s.bg_production}/10")
    if getattr(s, "bg_mix", None) is not None:
        print(f"Mix/Mst : {s.bg_mix}/10")
    if e.features:
        print(f"Features: {', '.join(e.features)}")
    if e.released:
        sales = _player_song_sales_snapshot(e)
        print(
            f"Sales   : first week {sales.first_week_sales:,} | "
            f"last week {sales.last_week_sales:,} | total {sales.total_sales:,} | "
            f"{_riaa_certification_label(sales.total_sales)}"
        )
        if e.physical_editions:
            print(f"Physical: {_physical_stock_summary(e.physical_editions)}")
    if e.producer:
        print(f"Producer: {e.producer}")
    if e.engineer:
        print(f"Engineer: {e.engineer}")
    if e.released:
        print(f"Streams : total {e.total_streams:,} | last week {e.last_week_streams:,}")
        if e.average_review is not None:
            print(f"Reviews : avg {e.average_review}/10")
    input("\nPress Enter to go back...")


def view_player_album_tracklist_menu(artist):
    drafts_and_released = list(artist.albums)
    if not drafts_and_released:
        print("No albums available.")
        return
    options = []
    for a in drafts_and_released:
        status = "released" if a.released else "draft"
        tag = "Deluxe" if a.deluxe_of else "Album"
        options.append(f"{a.album.name} | {tag} | {status} | {a.album.song_count()} tracks")
    idx = choose_from_list("Choose an album", options, allow_cancel=True)
    if idx is None:
        return
    entry = drafts_and_released[idx]
    titles = [s.name for s in entry.album.songs]
    if not titles:
        print("No tracks yet.")
        input("\nPress Enter to go back...")
        return
    title_width = max(len("Title"), max(len(t) for t in titles))
    print(f"\n{'Title':<{title_width}}  {'Genre':<11} {'Theme':<14} Quality")
    for s in entry.album.songs:
        print(f"{s.name:<{title_width}}  {s.genre_label():<11} {str(s.theme):<14} {s.quality:>4}/10")

    # Project-level craft averages (background attributes).
    totals = {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
    count = 0
    for s in entry.album.songs:
        _ensure_song_bg_attrs(s, artist.skills)
        if getattr(s, "bg_lyrics", None) is None:
            continue
        totals["lyrics"] += float(s.bg_lyrics)
        totals["vocals"] += float(s.bg_vocals)
        totals["prod"] += float(s.bg_production)
        totals["mix"] += float(s.bg_mix)
        count += 1
    if count > 0:
        print(
            f"\nAvg craft | lyrics {totals['lyrics']/count:.1f} | vocals {totals['vocals']/count:.1f} | "
            f"prod {totals['prod']/count:.1f} | mix {totals['mix']/count:.1f}"
        )
    if entry.released:
        snapshot = _player_album_sales_snapshot(artist, entry)
        print(
            f"Sales     | first week {snapshot.first_week_sales:,} | "
            f"last week {snapshot.last_week_sales:,} | total {snapshot.total_sales:,} | "
            f"{_riaa_certification_label(snapshot.total_sales)}"
        )
        if entry.physical_editions:
            print(f"Physical  | {_physical_stock_summary(entry.physical_editions)}")

    pick = choose_from_list(
        "View track metadata?",
        [f"{i+1}. {entry.album.songs[i].name}" for i in range(len(entry.album.songs))] + ["Back"],
        allow_cancel=False,
    )
    if pick is None or pick == len(entry.album.songs):
        return
    song = entry.album.songs[pick]

    # Try to find the SongEntry for streams/reviews if it exists.
    song_entry = next((e for e in artist.singles if e.song is song), None)

    # Ensure attributes exist even for older saves.
    _ensure_song_bg_attrs(song, artist.skills)

    print("\nMetadata")
    print(f"Title   : {song.name}")
    print(f"Quality : {song.quality}/10")
    print(f"Genre   : {song.genre_label()}")
    print(f"Theme   : {song.theme}")
    if getattr(song, "catchiness", None) is not None:
        print(f"Catchy  : {song.catchiness}")
    if getattr(song, "virality", None) is not None and getattr(song, "maturity_weeks", None) is not None:
        ws = int(song_entry.weeks_since_release) if song_entry else 0
        remaining = max(0, int(song.maturity_weeks) - ws)
        print(f"Virality: {song.virality} | matures in {remaining}w")
    print(f"Lyrics  : {song.bg_lyrics}/10")
    print(f"Vocals  : {song.bg_vocals}/10")
    print(f"Prod    : {song.bg_production}/10")
    print(f"Mix/Mst : {song.bg_mix}/10")

    if song_entry and song_entry.features:
        print(f"Features: {', '.join(song_entry.features)}")
    if song_entry and song_entry.producer:
        print(f"Producer: {song_entry.producer}")
    if song_entry and song_entry.engineer:
        print(f"Engineer: {song_entry.engineer}")
    if song_entry and song_entry.released:
        print(f"Streams : total {song_entry.total_streams:,} | last week {song_entry.last_week_streams:,}")
        song_sales = _player_song_sales_snapshot(song_entry)
        print(
            f"Sales   : first week {song_sales.first_week_sales:,} | "
            f"last week {song_sales.last_week_sales:,} | total {song_sales.total_sales:,}"
        )
        if song_entry.average_review is not None:
            print(f"Reviews : avg {song_entry.average_review}/10")

    input("\nPress Enter to go back...")


def catalog_menu(artist):
    while True:
        list_catalog(artist)
        choice = choose_from_list(
            "Catalog options",
            ["View song metadata", "View album tracklist", "Delete single entry", "Add single to album", "Send feature request", "Back"],
            allow_cancel=False,
        )
        if choice == 0:
            view_player_song_metadata_menu(artist)
        elif choice == 1:
            view_player_album_tracklist_menu(artist)
        elif choice == 2:
            delete_single_entry(artist)
        elif choice == 3:
            add_single_to_album(artist)
        elif choice == 4:
            send_feature_request_menu(artist)
        else:
            return


def release_single(artist, track_sim):
    options = [entry for entry in artist.singles if not entry.released]
    if not options:
        print("No unreleased singles available.")
        return
    labels = [
        f"{entry.song.name} - {entry.song.genre_label()} - {entry.song.quality}/10"
        for entry in options
    ]
    idx = choose_from_list("Choose a single to release", labels, allow_cancel=True)
    if idx is None:
        return
    entry = options[idx]

    contract = getattr(artist, "label_contract", None)
    if contract and getattr(contract, "status", "") == "shelved":
        print("\n[LABEL BLOCKED] Your record label has currently SHELVED your release pipeline.")
        print("Your project cannot be distributed until the label lifts the release hold.")
        return

    if getattr(entry.song, "catchiness", None) is None:
        entry.song.catchiness = roll_catchiness_value()
    if getattr(entry.song, "virality", None) is None or getattr(entry.song, "maturity_weeks", None) is None:
        v, m = roll_virality_value_and_maturity()
        entry.song.virality = v
        entry.song.maturity_weeks = m
    print(f"\nReleasing single '{entry.song.name}'...\n")
    result = track_sim.publish_song(entry.song)
    entry.released = True
    entry.release_week_index = _player_week_index(artist)
    entry.average_review = result["average"]
    entry.release_popularity_value = release_bump_for_quality(entry.song.quality)
    entry.release_popularity_weeks_left = 1
    entry.weeks_since_release = 0
    entry.virality_triggered = False
    entry.virality_weeks_active = 0
    entry.virality_max_weekly_bonus = 0
    entry.last_week_digital_sales = 0
    entry.last_week_physical_sales = 0
    artist.releases_this_week.append(entry)
    critic_names = [critic.name for critic in getattr(track_sim, "critics", [])]
    for critic_name, score in zip(critic_names, list(result.get("scores", []) or [])):
        if float(score) < 5.5:
            artist.recent_low_reviews.append(
                {
                    "critic": critic_name,
                    "score": float(score),
                    "week": _player_week_index(artist),
                    "song": entry.song.name,
                }
            )
    artist.recent_low_reviews = artist.recent_low_reviews[-20:]


def release_album(artist, album_sim):
    options = [entry for entry in artist.albums if not entry.released]
    if not options:
        print("No unreleased albums available.")
        return
    labels = [
        f"{entry.album.name} - {entry.album.song_count()} tracks"
        for entry in options
    ]
    idx = choose_from_list("Choose an album to release", labels, allow_cancel=True)
    if idx is None:
        return
    entry = options[idx]

    contract = getattr(artist, "label_contract", None)
    if contract and getattr(contract, "status", "") == "shelved":
        print("\n[LABEL BLOCKED] Your record label has currently SHELVED your upcoming releases.")
        print("Your project cannot be commercially distributed until the label unshelves your pipeline.")
        return

    if entry.album.song_count() < MIN_SONGS:
        print(
            f"Albums need at least {MIN_SONGS} tracks before release. "
            f"'{entry.album.name}' has {entry.album.song_count()}."
        )
        return
    print(f"\nReleasing album '{entry.album.name}'...\n")
    album_result = album_sim.publish_album(entry.album)
    if isinstance(album_result, dict):
        entry.average_review = float(album_result.get("average", 0.0) or 0.0)
        track_scores = list(album_result.get("track_scores", []) or [])
        critic_scores = list(album_result.get("critic_scores", []) or [])
    else:
        entry.average_review = float(album_result or 0.0)
        track_scores = []
        critic_scores = []
    entry.released = True
    album_release_week_index = _player_week_index(artist)
    entry.release_week_index = album_release_week_index
    artist.releases_this_week.append(entry)

    if contract and getattr(contract, "status", "") in ("active", "recouped"):
        contract.albums_delivered += 1
        print(f"  [LABEL UPDATE] Album delivered! ({contract.albums_delivered}/{contract.album_commitment} projects fulfilled)")
    # Album release gives a one-week popularity bump (songs inside don't stack their own bumps).
    artist.popularity_state.album_release_boost = 10.0
    artist.popularity_state.album_release_weeks_left = 1
    for idx, song in enumerate(entry.album.songs):
        track_review = (
            float(track_scores[idx])
            if idx < len(track_scores)
            else float(entry.average_review or 0.0)
        )
        if getattr(song, "catchiness", None) is None:
            song.catchiness = roll_catchiness_value()
        if getattr(song, "virality", None) is None or getattr(song, "maturity_weeks", None) is None:
            v, m = roll_virality_value_and_maturity()
            song.virality = v
            song.maturity_weeks = m
        existing = next((s for s in artist.singles if s.song is song), None)
        if existing:
            existing.released = True
            existing.average_review = track_review
            existing.source_label = f"Album: {entry.album.name}"
            existing.release_week_index = album_release_week_index
            existing.release_popularity_value = 0.0
            existing.release_popularity_weeks_left = 0
            existing.weeks_since_release = 0
            existing.virality_triggered = False
            existing.virality_weeks_active = 0
            existing.virality_max_weekly_bonus = 0
            existing.last_week_digital_sales = 0
            existing.last_week_physical_sales = 0
        else:
            artist.singles.append(
                SongEntry(
                    song=song,
                    released=True,
                    average_review=track_review,
                    source_label=f"Album: {entry.album.name}",
                    release_popularity_value=0.0,
                    release_popularity_weeks_left=0,
                    weeks_since_release=0,
                    virality_triggered=False,
                    virality_weeks_active=0,
                    virality_max_weekly_bonus=0,
                    release_week_index=album_release_week_index,
                )
            )
    for critic_row in critic_scores:
        if float(critic_row.get("score", 10.0)) < 5.5:
            artist.recent_low_reviews.append(
                {
                    "critic": str(critic_row.get("critic", "Unknown Critic")),
                    "score": float(critic_row.get("score", 0.0)),
                    "week": album_release_week_index,
                    "song": entry.album.name,
                }
            )
    artist.recent_low_reviews = artist.recent_low_reviews[-20:]


def _print_ecosystem_new_releases(world: EcosystemWorld):
    print(f"\nNew releases | {format_week_range(world.week_number)}")
    if not world.last_week_releases:
        print("- No releases this week.")
        return
    _ensure_sales_state(world)
    print(f"- Artists dropped: {len(world.last_week_releases)}")
    for release in world.last_week_releases:
        extra = ""
        if getattr(release, "tracks", None):
            extra = f" | {len(release.tracks)} tracks"
        viral_note = ""
        if getattr(release, "tracks", None) and release.tracks:
            s = release.tracks[0]
            sid = getattr(s, "song_id", "")
            if sid and sid in world.song_runtime:
                viral_note = f" | viral {world.song_runtime[sid].virality}"
        sales = _world_release_sales(world, str(getattr(release, "release_id", "")))
        print(
            f"- {release.artist_name} | {release.release_type} | '{release.title}' | "
            f"{format_release_date(release)} | "
            f"{release.review}/10{extra}{viral_note} | "
            f"sales {sales.first_week_sales:,} first week / {sales.total_sales:,} total"
        )


def _print_artist_details(seed, world: EcosystemWorld | None = None):
    print(f"\n{seed.name}")
    rep = int(round(_ecosystem_artist_reputation(seed.name, world)))
    pop = int(round(_ecosystem_artist_popularity(seed.name, world)))
    print(f"Reputation: {rep}")
    print(f"Popularity : {pop}")
    print(f"Friendliness: {int(seed.friendliness)}")
    print(f"Lovingness: {_artist_lovingness(seed.name)}")
    pa = getattr(seed, "project_ability", None)
    if pa is None:
        pa = (
            int(getattr(seed, "quality_consistency", 70)) * 0.55
            + int(seed.skills.get("mix/master", 50)) * 0.25
            + int(seed.skills.get("production", 50)) * 0.20
        )
    print(f"Project ability: {int(round(pa))}")
    if world is not None:
        social = world.social_graph.get(seed.name, {})
        friends = social.get("friends", [])
        enemies = social.get("enemies", [])
        romance = _get_romance_profile(world, seed.name)
        if romance is not None:
            current_week = int(getattr(world, "week_number", 0) or 0)
            print(f"Love life: {_romance_status_label(romance)}")
            if romance.partner_name:
                print(f"Partner: {romance.partner_name}")
                duration = _current_romance_duration(romance, current_week)
                print(
                    f"Together for: {_format_week_span(duration)} "
                    f"({duration} week{'s' if duration != 1 else ''}, since {_romance_week_label(romance.relationship_start_week)})"
                )
                if romance.status == "separated":
                    print(
                        f"Separated from: {_separation_status_label(romance)} "
                        f"at {_romance_week_label(romance.separation_week)}"
                    )
            print(f"Marriages: {romance.marriage_count}")
            print(f"Divorces : {romance.divorce_count}")
            if romance.ex_relationships:
                print("Exes:")
                for ex in reversed(romance.ex_relationships[-8:]):
                    duration = int(ex.get("duration_weeks", 0) or 0)
                    final_status = str(ex.get("final_status", "breakup")).replace("_", " ")
                    print(
                        f"- {ex.get('partner_name', 'Unknown')} | {_format_week_span(duration)} "
                        f"({duration} week{'s' if duration != 1 else ''}) | "
                        f"{_romance_week_label(int(ex.get('start_week', 0) or 0))} -> "
                        f"{_romance_week_label(int(ex.get('end_week', 0) or 0))} | {final_status}"
                    )
            else:
                print("Exes: none recorded")
        print(f"Friends with: {', '.join(friends[:20])}{'...' if len(friends) > 20 else ''}")
        print(f"Enemies with: {', '.join(enemies[:20])}{'...' if len(enemies) > 20 else ''}")

    print("\nSkills")
    for skill, value in sorted(seed.skills.items(), key=lambda kv: kv[0]):
        print(f"- {skill}: {int(value)}")

    top_genres = sorted(seed.genres.items(), key=lambda kv: kv[1], reverse=True)[:8]
    print("\nGenres")
    for genre, value in top_genres:
        print(f"- {genre}: {int(value)}")

    top_themes = sorted(seed.themes.items(), key=lambda kv: kv[1], reverse=True)[:8]
    print("\nThemes")
    for theme, value in top_themes:
        print(f"- {theme}: {int(value)}")

    if world is not None:
        song_ids = world.songs_by_artist.get(seed.name, [])
        if song_ids:
            ranked = sorted(
                (world.song_runtime[sid] for sid in song_ids if sid in world.song_runtime),
                key=lambda s: s.total_streams,
                reverse=True,
            )
            print("\nMost popular songs")
            for idx, s in enumerate(ranked[:5], 1):
                date_label = format_release_date(s.release_week)
                title = s.title
                prefix = f"{seed.name} - "
                if title.startswith(prefix):
                    title = title[len(prefix):]
                print(f"- {idx}. {title} | {s.total_streams:,} streams | {date_label}")


def _print_artist_releases(world: EcosystemWorld, artist_name: str):
    releases = world.release_history.get(artist_name, [])
    if not releases:
        print("\nNo releases recorded yet.")
        return
    _ensure_sales_state(world)
    print("\nTitle                          Type      Review   Streams        1st Wk    Last Wk     Total      Cert       Release Date")
    for release in releases:
        date_label = format_release_date(release)
        title = release.title
        prefix = f"{artist_name} - "
        if title.startswith(prefix):
            title = title[len(prefix):]
        title = (title[:28] + "...") if len(title) > 31 else title
        streams = 0
        if getattr(release, "tracks", None):
            for t in release.tracks:
                sid = getattr(t, "song_id", "")
                if sid and sid in world.song_runtime:
                    streams += int(world.song_runtime[sid].total_streams)
        sales = _world_release_sales(world, str(getattr(release, "release_id", "")))
        print(
            f"{title:<31} {release.release_type:<9} {release.review:>2}/10    {streams:>10,}   "
            f"{sales.first_week_sales:>8,}  {sales.last_week_sales:>9,}  {sales.total_sales:>9,}  "
            f"{_riaa_certification_label(sales.total_sales):<10} {date_label}"
        )


def _fallback_feature_quality(feature_name: str, track_title: str) -> float | None:
    seed = _ecosystem_seed_by_name(feature_name)
    if seed is None:
        return None
    rng = _stable_rng_for_label(f"feature-quality-backfill:{track_title}:{feature_name}")
    x = ((float(seed.skills.get("lyrics", 50)) / 100.0) + (float(seed.skills.get("vocals", 50)) / 100.0)) / 2.0
    x *= 10.0
    return round(max(0.0, min(10.0, rng.uniform(x - 2.0, x + 1.0))), 1)


def _feature_quality_rows(track, runtime_song=None) -> list[tuple[str, float]]:
    rows = list(getattr(runtime_song, "feature_qualities", ()) or getattr(track, "feature_qualities", ()) or ())
    normalized: list[tuple[str, float]] = []
    seen = set()
    for name, score in rows:
        normalized.append((str(name), float(score)))
        seen.add(str(name))
    for name in getattr(runtime_song, "features", ()) or getattr(track, "features", ()) or ():
        if name in seen:
            continue
        fallback = _fallback_feature_quality(str(name), str(getattr(track, "title", "")))
        if fallback is not None:
            normalized.append((str(name), fallback))
    return normalized


def _view_artist_releases_menu(world: EcosystemWorld, artist_name: str):
    releases = world.release_history.get(artist_name, [])
    if not releases:
        print("\nNo releases recorded yet.")
        return
    def _strip_artist_prefix(title: str) -> str:
        prefix = f"{artist_name} - "
        return title[len(prefix):] if title.startswith(prefix) else title
    while True:
        labels = []
        for r in releases:
            date_label = format_release_date(r)
            track_note = f" | {len(r.tracks)} tracks" if getattr(r, "tracks", None) else ""
            labels.append(f"{r.release_type} | '{r.title}' | {r.review}/10 | {date_label}{track_note}")
        idx = choose_from_list("Releases", labels + ["Back"], allow_cancel=False)
        if idx is None or idx == len(labels):
            return
        chosen = releases[idx]
        tracks = list(getattr(chosen, "tracks", None) or ())
        if not tracks:
            # Backward compat: very old entries.
            tracks = []
        sales = _world_release_sales(world, str(getattr(chosen, "release_id", "")))
        display_titles = [_strip_artist_prefix(t.title) for t in tracks] if tracks else []
        title_width = max(len("Title"), max((len(t) for t in display_titles), default=5))
        print(
            f"\nProject sales | first week {sales.first_week_sales:,} | "
            f"last week {sales.last_week_sales:,} | total {sales.total_sales:,} | "
            f"{_riaa_certification_label(sales.total_sales)}"
        )
        print(f"\n{'Title':<{title_width}}  {'Genre':<11} {'Theme':<14} Review   Streams")
        # Project-level craft averages (background attributes).
        totals = {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
        count = 0
        for t, disp in zip(tracks, display_titles):
            sid = getattr(t, 'song_id', '')
            runtime_song = world.song_runtime[sid] if sid and sid in world.song_runtime else None
            total = int(runtime_song.total_streams) if runtime_song is not None else 0
            review_score = (
                float(getattr(runtime_song, "review", getattr(t, "review", 0.0)))
                if runtime_song is not None
                else float(getattr(t, "review", 0.0))
            )
            print(f"{disp:<{title_width}}  {t.genre:<11} {t.theme:<14} {review_score:>4.1f}/10  {total:>8,}")

            # Use stored bg attributes when available; otherwise backfill using credited contributors
            # (producer/engineer) so the ranges make sense.
            bg_lyrics = getattr(t, "bg_lyrics", None)
            bg_vocals = getattr(t, "bg_vocals", None)
            bg_prod = getattr(t, "bg_production", None)
            bg_mix = getattr(t, "bg_mix", None)
            if bg_lyrics is None or bg_vocals is None or bg_prod is None or bg_mix is None:
                rng = _stable_rng_for_label(f"bgbackfill:{artist_name}:{getattr(t,'title','')}")
                seed_main = _ecosystem_seed_by_name(artist_name)
                seed_prod = _ecosystem_seed_by_name(t.producers[0]) if getattr(t, "producers", ()) else None
                seed_eng = _ecosystem_seed_by_name(t.engineers[0]) if getattr(t, "engineers", ()) else None
                seed_lyr = _ecosystem_seed_by_name(t.lyricists[0]) if getattr(t, "lyricists", ()) else None
                seed_voc = _ecosystem_seed_by_name(t.vocalists[0]) if getattr(t, "vocalists", ()) else None
                if seed_main is not None:
                    if bg_lyrics is None:
                        src = seed_lyr or seed_main
                        bg_lyrics = _roll_bg_attr_from_skill_rng(src.skills.get("lyrics", 25), rng)
                    if bg_vocals is None:
                        src = seed_voc or seed_main
                        bg_vocals = _roll_bg_attr_from_skill_rng(src.skills.get("vocals", 25), rng)
                    if bg_prod is None:
                        src = seed_prod or seed_main
                        bg_prod = _roll_bg_attr_from_skill_rng(src.skills.get("production", 25), rng)
                    if bg_mix is None:
                        src = seed_eng or seed_main
                        bg_mix = _roll_bg_attr_from_skill_rng(src.skills.get("mix/master", 25), rng)
            if bg_lyrics is not None and bg_vocals is not None and bg_prod is not None and bg_mix is not None:
                totals["lyrics"] += float(bg_lyrics)
                totals["vocals"] += float(bg_vocals)
                totals["prod"] += float(bg_prod)
                totals["mix"] += float(bg_mix)
                count += 1

        if count > 0:
            print(
                f"\nAvg craft | lyrics {totals['lyrics']/count:.1f} | vocals {totals['vocals']/count:.1f} | "
                f"prod {totals['prod']/count:.1f} | mix {totals['mix']/count:.1f}"
            )
        # Allow selecting a track to view metadata.
        pick = choose_from_list(
            "View track metadata?",
            [f"{i+1}. {display_titles[i]}" for i in range(len(display_titles))] + ["Back"],
            allow_cancel=False,
        )
        if pick is None or pick == len(display_titles):
            continue
        track = tracks[pick]
        sid = getattr(track, "song_id", "")
        runtime_song = world.song_runtime[sid] if sid and sid in world.song_runtime else None
        print("\nMetadata")
        if getattr(track, "lyricists", ()):
            print(f"Lyricists   : {', '.join(track.lyricists)}")
        if getattr(track, "vocalists", ()):
            print(f"Vocalists   : {', '.join(track.vocalists)}")
        if getattr(track, "producers", ()):
            print(f"Producers   : {', '.join(track.producers)}")
        if getattr(track, "engineers", ()):
            print(f"Engineered by: {', '.join(track.engineers)}")
        feature_quality_rows = _feature_quality_rows(track, runtime_song)
        if feature_quality_rows:
            print("Feature qualities:")
            for feature_name, score in feature_quality_rows:
                print(f"- {feature_name} -> {score:.1f}/10")
        # Background craft attributes: newer ecosystem tracks store these, but we
        # also backfill for older entries using credited contributors so the ranges make sense.
        bg_lyrics = getattr(track, "bg_lyrics", None)
        bg_vocals = getattr(track, "bg_vocals", None)
        bg_prod = getattr(track, "bg_production", None)
        bg_mix = getattr(track, "bg_mix", None)
        if bg_lyrics is None or bg_vocals is None or bg_prod is None or bg_mix is None:
            rng = _stable_rng_for_label(f"bgbackfill:{artist_name}:{getattr(track,'title','')}")
            seed_main = _ecosystem_seed_by_name(artist_name)
            seed_prod = _ecosystem_seed_by_name(track.producers[0]) if getattr(track, "producers", ()) else None
            seed_eng = _ecosystem_seed_by_name(track.engineers[0]) if getattr(track, "engineers", ()) else None
            seed_lyr = _ecosystem_seed_by_name(track.lyricists[0]) if getattr(track, "lyricists", ()) else None
            seed_voc = _ecosystem_seed_by_name(track.vocalists[0]) if getattr(track, "vocalists", ()) else None
            if seed_main is not None:
                if bg_lyrics is None:
                    src = seed_lyr or seed_main
                    bg_lyrics = _roll_bg_attr_from_skill_rng(src.skills.get("lyrics", 25), rng)
                if bg_vocals is None:
                    src = seed_voc or seed_main
                    bg_vocals = _roll_bg_attr_from_skill_rng(src.skills.get("vocals", 25), rng)
                if bg_prod is None:
                    src = seed_prod or seed_main
                    bg_prod = _roll_bg_attr_from_skill_rng(src.skills.get("production", 25), rng)
                if bg_mix is None:
                    src = seed_eng or seed_main
                    bg_mix = _roll_bg_attr_from_skill_rng(src.skills.get("mix/master", 25), rng)

        if bg_lyrics is not None:
            print(f"Lyrics score: {float(bg_lyrics):.1f}/10")
        if bg_vocals is not None:
            print(f"Vocals score: {float(bg_vocals):.1f}/10")
        if bg_prod is not None:
            print(f"Prod score  : {float(bg_prod):.1f}/10")
        if bg_mix is not None:
            print(f"Mix score   : {float(bg_mix):.1f}/10")
        input("\nPress Enter to go back...")


def view_ecosystem_artists_menu(world: EcosystemWorld):
    while True:
        seeds = sorted(ARTIST_ECOSYSTEM_SEEDS, key=lambda s: s.name.lower())
        options = []
        for seed in seeds:
            rep = int(round(_ecosystem_artist_reputation(seed.name, world)))
            pop = int(round(_ecosystem_artist_popularity(seed.name, world)))
            total = 0
            for sid in world.songs_by_artist.get(seed.name, []):
                if sid in world.song_runtime:
                    total += int(world.song_runtime[sid].total_streams)
            options.append(f"{seed.name} | rep {rep} | pop {pop} | streams {total:,}")
        idx = choose_from_list("Choose an artist", options, allow_cancel=True)
        if idx is None:
            return
        chosen = seeds[idx]
        while True:
            _print_artist_details(chosen, world=world)
            action = choose_from_list("Options", ["See releases", "Back"], allow_cancel=False)
            if action == 0:
                _view_artist_releases_menu(world, chosen.name)
            else:
                break


def view_ecosystem_new_releases(world: EcosystemWorld):
    _print_ecosystem_new_releases(world)


def release_calendar_menu(world: EcosystemWorld):
    calendar = prepare_release_calendar(world, lookahead=4)
    current = int(world.week_number)

    while True:
        week_keys = [current + offset for offset in range(1, 5)]
        options = []
        print("\nRelease Calendar")
        print("A four-week peek at announced ecosystem drops. Surprise releases can still appear when the week arrives.")
        for week_number in week_keys:
            items = calendar.get(week_number, [])
            options.append(f"{format_week_range(week_number)} | {len(items)} announced release{'s' if len(items) != 1 else ''}")

        idx = choose_from_list("Choose a week", options + ["Back"], allow_cancel=False)
        if idx is None or idx == len(options):
            return

        week_number = week_keys[idx]
        items = calendar.get(week_number, [])
        print(f"\n{format_week_range(week_number)} Release Window")
        if not items:
            print("- Nothing announced yet. That does not mean nobody is dropping.")
            input("\nPress Enter to go back...")
            continue

        title_width = max(len("Title"), max(len(p.title) for p in items))
        artist_width = max(len("Artist"), max(len(p.artist_name) for p in items))
        print(f"{'Artist':<{artist_width}}  {'Type':<8}  {'Title':<{title_width}}  {'Genre':<12}  Tracks")
        for pending in sorted(items, key=lambda x: (x.week_release, x.release_type, x.artist_name.lower(), x.title.lower())):
            track_count = len(getattr(pending, "tracks", []) or [])
            print(
                f"{pending.artist_name:<{artist_width}}  {pending.release_type:<8}  "
                f"{pending.title:<{title_width}}  {pending.core_genre:<12}  {track_count}"
            )
        input("\nPress Enter to go back...")


def release_menu(artist, track_sim, album_sim):
    choice = choose_from_list(
        "Release menu",
        ["Release single", "Release album", "Manage physical copies"],
        allow_cancel=True,
    )
    if choice is None:
        return
    if choice == 0:
        release_single(artist, track_sim)
    elif choice == 1:
        release_album(artist, album_sim)
    else:
        manage_physical_copies_menu(artist)

