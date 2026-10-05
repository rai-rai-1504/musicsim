"""rapsim_reviews.feature_system
Feature collaborations, inbound/outbound requests, pricing negotiation,
verse delivery, and collaboration quality scoring.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING
from uuid import uuid4

from rapsim_reviews.date_system import format_week_range, format_release_date
from rapsim_reviews.ui_helpers import (
    choose_from_list,
    choose_item_from_list,
    meter_bar,
    money_fmt,
    prompt_int,
    prompt_text,
    clamp_meter,
    clamp_popularity,
    _stable_rng_for_label,
)
from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS, ARTIST_FEATURE_TURNAROUND
from rapsim_reviews.career_models import (
    Artist,
    SongEntry,
    AlbumEntry,
    FeatureRequest,
    FEATURE_DEADLINE_WEEKS,
    GENRE_SKILL_WEIGHTS,
    SKILLS,
    classify_artist_skills,
    _player_week_index,
    _apply_relationship_delta,
    _relationship_score,
    _ecosystem_seed_by_name,
    _ecosystem_artist_popularity,
    _find_world_runtime,
    _find_artist_any,
    _ensure_song_bg_attrs,
    _jitter_attribute,
    _apply_producer_bg,
    _apply_engineer_bg,
)
from rapsim_reviews.sales_system import (
    _world_release_sales,
    _riaa_certification_label,
)
from rapsim_reviews.track_review.base import Song

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld

FEATURE_REJECTION_LINES = {
    "high": [
        "I'm so sorry, I just can't make this work right now. Don't take it personally.",
        "I love what you're doing, but I can't commit to this one. Respect always.",
        "Not right now, but keep sending. You're talented, for real.",
        "I can't jump on this, but I appreciate you reaching out.",
        "I wish I could, but it's not the right fit. Much love though.",
    ],
    "mid": [
        "Not this one.",
        "I'll pass for now.",
        "I can't do it.",
        "Not feeling it.",
        "Maybe another time.",
    ],
    "low": [
        "Nah. Not for me.",
        "No.",
        "Stop asking.",
        "Who is this again?",
        "Not happening.",
    ],
}

FEATURE_REJECT_VERSE_LINES = {
    "high": [
        "I'm so sorry bro, I just can't use this verse for technical reasons. Don't take it personally.",
        "I respect you a lot, but this one isn't fitting the record. Please don't take it the wrong way.",
        "I hear what you're trying to do, but I can't use it on this track. Much love though.",
        "This is close, but I can't lock it in. If you want to try once more, go for it.",
        "I appreciate the work, but it doesn't match what I need. Sorry.",
    ],
    "mid": [
        "Not gonna use this one.",
        "This isn't it.",
        "Doesn't fit the track.",
        "Nah, can't run with this.",
        "Try again if you want.",
    ],
    "low": [
        "Nah man this is bad.",
        "This is not going on my song.",
        "Nope.",
        "Don't send me this again.",
        "Stop wasting my time.",
    ],
}

FEATURE_ACCEPT_VERSE_LINES = {
    "high": [
        "This is hard. I'm putting it in.",
        "Perfect. This fits exactly.",
        "Yeah, that's the one. Let's go.",
        "Fire. You did your thing.",
        "Locked. Appreciate you.",
    ],
    "mid": [
        "Yeah, this works.",
        "Cool. I'll use it.",
        "This fits.",
        "Alright, let's run it.",
        "Good. Sending it through.",
    ],
    "low": [
        "Fine. It works.",
        "Okay. I'll use it.",
        "Whatever. It's good enough.",
        "Yeah.",
        "Aight.",
    ],
}


def _add_feature_to_title(title: str, feature_name: str) -> str:
    # Insert into existing "ft." list if present, and keep any "(prod. ...)" suffix.
    prod_suffix = ""
    head = title
    if "(prod." in title:
        head, prod_suffix = title.split("(prod.", 1)
        prod_suffix = "(prod." + prod_suffix
        head = head.rstrip()
    if " ft. " in head:
        left, feat_part = head.split(" ft. ", 1)
        feat_names = [n.strip() for n in feat_part.split(",") if n.strip()]
        if feature_name not in feat_names:
            feat_names.append(feature_name)
        head = f"{left} ft. {', '.join(feat_names)}"
    else:
        head = f"{head} ft. {feature_name}"
    return (head + " " + prod_suffix).strip()


def _apply_feature_bg_delta(song: Song, feat_seed, increased: bool) -> None:
    # Feature verse affects lyrics/vocals only; producer/engineer handled elsewhere.
    if song is None or feat_seed is None:
        return
    _ensure_song_bg_attrs(song, {"lyrics": 25, "vocals": 25, "production": 25, "mix/master": 25})
    lyr = float(getattr(song, "bg_lyrics", 5.0) or 5.0)
    voc = float(getattr(song, "bg_vocals", 5.0) or 5.0)
    feat_lyr = float(getattr(feat_seed, "skills", {}).get("lyrics", 50))
    feat_voc = float(getattr(feat_seed, "skills", {}).get("vocals", 50))

    if increased:
        lyr_target = min(9.5, max(1.0, lyr + 0.15 * (feat_lyr / 10.0)))
        voc_target = min(9.5, max(1.0, voc + 0.15 * (feat_voc / 10.0)))
        song.bg_lyrics = _jitter_attribute(lyr_target, span=0.4, lo=1.0, hi=9.9)
        song.bg_vocals = _jitter_attribute(voc_target, span=0.4, lo=1.0, hi=9.9)
    else:
        lyr_target = max(2.0, lyr - 0.5 * ((100.0 - feat_lyr) / 10.0))
        voc_target = max(2.0, voc - 0.5 * ((100.0 - feat_voc) / 10.0))
        song.bg_lyrics = _jitter_attribute(lyr_target, span=0.4, lo=2.0, hi=9.9)
        song.bg_vocals = _jitter_attribute(voc_target, span=0.4, lo=2.0, hi=9.9)


def _friendliness_tier(friendliness):
    if friendliness >= 70:
        return "high"
    if friendliness <= 30:
        return "low"
    return "mid"


def _roll_bg_attr_from_skill_rng(skill_value: float, rng: random.Random) -> float:
    s = float(skill_value) / 10.0
    lo = max(1.0, s - 2.0)
    hi = max(lo, s)
    return round(rng.uniform(lo, hi), 1)


def _new_request_id(week_index):
    return f"FR-{week_index}-{random.randint(1000, 9999)}"


def _feature_offer_money(player_artist):
    avg_skill = sum(float(player_artist.skills[s]) for s in SKILLS) / float(len(SKILLS))
    base = 250.0 + (avg_skill * 22.0)
    return round(random.uniform(base * 0.75, base * 1.35), 2)


def _ecosystem_artist_best_release(name, ecosystem_world: EcosystemWorld | None):
    if ecosystem_world is None:
        return None
    releases = ecosystem_world.release_history.get(name, [])
    if not releases:
        return None
    # Feature requests should only ever attach to singles (no EP/album/mixtape).
    singles = [r for r in releases if getattr(r, "release_type", "") == "single"]
    if not singles:
        return None
    best = max(singles, key=lambda r: getattr(r, "quality", getattr(r, "review", 0.0)))
    return best


def _apply_feature_popularity_boost(player_artist, amount=5.0, weeks=3):
    """Temporary popularity bump for features (decays automatically in simulate_week)."""
    amount = float(amount)
    weeks = int(weeks)
    if amount <= 0 or weeks <= 0:
        return
    # Keep the boost meaningful but not game-breaking.
    player_artist.popularity_state.feature_boost = clamp_popularity(
        player_artist.popularity_state.feature_boost + amount
    )
    player_artist.popularity_state.feature_boost = min(
        10.0, float(player_artist.popularity_state.feature_boost)
    )
    player_artist.popularity_state.feature_boost_weeks_left = max(
        int(player_artist.popularity_state.feature_boost_weeks_left), weeks
    )


def _ecosystem_verse_quality(seed, genre):
    if not seed:
        return 5.0
    weights = GENRE_SKILL_WEIGHTS.get(genre, GENRE_SKILL_WEIGHTS["pop"])
    skill_score = sum(float(seed.skills[s]) * float(w) for s, w in weights.items())
    genre_score = float(seed.genres.get(genre, 30))
    consistency = float(getattr(seed, "quality_consistency", 70))
    base = (skill_score * 0.55) + (genre_score * 0.25) + (consistency * 0.20)
    base = base / 10.0
    # More consistent artists have tighter variance.
    var = random.uniform(-1.2, 1.0)
    if consistency >= 85:
        var *= 0.55
    elif consistency <= 55:
        var *= 1.20
    quality = max(0.0, min(10.0, base + var))
    return round(quality, 1)


def _ecosystem_contribution_quality(seed, genre, kind: str) -> float:
    """Quality of what the ecosystem artist sends back (verse/beat/mix)."""
    if kind == "feature":
        return _ecosystem_verse_quality(seed, genre)
    if not seed:
        return 5.0
    qc = float(getattr(seed, "quality_consistency", 70))
    if kind == "producer":
        base = (seed.skills.get("production", 50) * 0.55) + (seed.genres.get(genre, 30) * 0.30) + (qc * 0.15)
    else:  # engineer
        base = (seed.skills.get("mix/master", 50) * 0.58) + (seed.genres.get(genre, 30) * 0.22) + (qc * 0.20)
    base = base / 10.0
    var = random.uniform(-1.1, 0.9)
    if qc >= 85:
        var *= 0.55
    elif qc <= 55:
        var *= 1.20
    quality = max(0.0, min(10.0, base + var))
    return round(quality, 1)


def _acceptance_threshold(seed, relationship):
    qc = float(getattr(seed, "quality_consistency", 70)) / 100.0
    if relationship > 90:
        return 0.0
    if relationship > 60:
        return 5.0
    if relationship < 10:
        return 9.0
    if relationship <= 30:
        if qc > 0.9:
            return 9.0
        if qc > 0.8:
            return 7.5
        if qc > 0.7:
            return 6.5
        return 5.0
    return 6.0


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


def send_feature_request_menu(player_artist):
    song_entries = [entry for entry in player_artist.singles if not entry.released]

    # Include album-draft-only songs (created straight into an album draft) so
    # the player can request collabs after adding songs to albums.
    known = {id(e.song) for e in player_artist.singles}
    album_only: list[tuple[str, Song]] = []
    for a in player_artist.albums:
        if a.released:
            continue
        for s in a.album.songs:
            if id(s) not in known:
                album_only.append((a.album.name, s))

    if not song_entries and not album_only:
        print("No unreleased songs to request a feature for.")
        return
    kind_idx = choose_from_list(
        "What are you requesting?",
        ["Feature (ft.)", "Producer (prod.)", "Engineer (mix/master)"],
        allow_cancel=True,
    )
    if kind_idx is None:
        return
    kind = "feature" if kind_idx == 0 else ("producer" if kind_idx == 1 else "engineer")
    labels = [f"{e.song.name} | {e.song.quality}/10 | {e.song.genre_label()}" for e in song_entries]
    labels += [f"{s.name} | {s.quality}/10 | {s.genre_label()} | album draft: {album}" for album, s in album_only]
    idx = choose_from_list("Choose an unreleased song", labels, allow_cancel=True)
    if idx is None:
        return
    song_entry: SongEntry | None = None
    chosen_song: Song | None = None
    chosen_album: str | None = None
    if idx < len(song_entries):
        song_entry = song_entries[idx]
        chosen_song = song_entry.song
    else:
        chosen_album, chosen_song = album_only[idx - len(song_entries)]

    seeds = sorted(ARTIST_ECOSYSTEM_SEEDS, key=lambda s: s.name.lower())
    # Filter by category.
    filtered = []
    for seed in seeds:
        cats = classify_artist_skills(seed)
        if kind == "feature":
            if ("lyricist" in cats) or ("vocalist" in cats) or ("growing" in cats):
                filtered.append(seed)
        elif kind == "producer":
            if "producer" in cats:
                filtered.append(seed)
        else:
            if "engineer" in cats:
                filtered.append(seed)
    seeds = filtered if filtered else seeds
    options = []
    for seed in seeds:
        rel = _relationship_score(player_artist, seed.name)
        options.append(f"{seed.name} | rel {rel:.1f} | cost ${seed.feature_cost:,}")
    pick = choose_from_list("Choose an artist to request a feature from", options, allow_cancel=True)
    if pick is None:
        return
    target = seeds[pick]
    relationship = _relationship_score(player_artist, target.name)
    friendliness = int(getattr(target, "friendliness", 50))
    tier = _friendliness_tier(friendliness)

    assert chosen_song is not None
    if chosen_song.quality < 3.0 and relationship <= 90:
        print(f"{target.name}: {random.choice(FEATURE_REJECTION_LINES[tier])}")
        _apply_relationship_delta(player_artist, target.name, -random.uniform(0.8, 2.5))
        return

    threshold = _acceptance_threshold(target, relationship)
    accepts = chosen_song.quality >= threshold
    if relationship > 90 and chosen_song.quality < 3.0:
        accepts = random.random() < 0.80

    if not accepts:
        print(f"{target.name}: {random.choice(FEATURE_REJECTION_LINES[tier])}")
        _apply_relationship_delta(player_artist, target.name, -random.uniform(0.6, 2.2))
        return

    cost = float(getattr(target, "feature_cost", 0.0))
    if relationship > 90:
        cost *= 0.20

    contract = getattr(player_artist, "label_contract", None)
    if contract and getattr(contract, "status", "") in ("active", "shelved", "recouped"):
        from rapsim_reviews.label_system import get_label_by_id
        lbl = get_label_by_id(contract.label_id)
        if lbl and lbl.collab_discount and target.name in lbl.signed_artists:
            cost = 0.0
            print(f"\n[LABEL BENEFIT] {target.name} is signed to {lbl.name}! Courtesy collab discount applied: $0.")

    cost = round(cost, 2)
    if player_artist.money < cost:
        print(f"You need {money_fmt(cost)} to book this feature. Balance: {money_fmt(player_artist.money)}")
        return
    player_artist.money -= cost

    week_index = _player_week_index(player_artist)
    turnaround = int(ARTIST_FEATURE_TURNAROUND.get(target.name, random.randint(2, 6)))
    turnaround = max(2, min(6, turnaround))
    req = FeatureRequest(
        request_id=_new_request_id(week_index),
        direction="outbound",
        artist_name=target.name,
        song_name=chosen_song.name,
        song_quality=float(chosen_song.quality),
        status="awaiting_verse",
        week_created=week_index,
        week_deadline=week_index + FEATURE_DEADLINE_WEEKS,
        weeks_until_artist_delivers=turnaround,
        paid=cost,
        request_kind=kind,
        player_album_name=chosen_album,
    )
    player_artist.feature_requests.append(req)
    print(f"{target.name}: bet. i'll send something in a few weeks.")


def view_feature_requests_menu(player_artist):
    active = [r for r in player_artist.feature_requests if r.status not in {"completed", "expired"}]
    if not active:
        print("No active feature requests right now.")
        return

    def label(req):
        due = f"due W{req.week_deadline}"
        return f"{req.request_id} | {req.direction} | {req.artist_name} | '{req.song_name}' | {req.status} | {due}"

    idx = choose_from_list("Feature requests", [label(r) for r in active], allow_cancel=True)
    if idx is None:
        return
    req = active[idx]
    seed = _ecosystem_seed_by_name(req.artist_name)
    friendliness = int(getattr(seed, "friendliness", 50)) if seed else 50
    tier = _friendliness_tier(friendliness)
    week_index = _player_week_index(player_artist)

    print(f"\n{req.artist_name} | {req.direction} | {getattr(req, 'request_kind', 'feature')}")
    print(f"Song: {req.song_name} | quality {req.song_quality}/10")
    print(f"Status: {req.status} | deadline {format_week_range(req.week_deadline)}")
    if req.artist_verse_quality is not None:
        print(f"Artist verse quality: {req.artist_verse_quality}/10")
    if req.player_verse_quality is not None:
        print(f"Your verse quality: {req.player_verse_quality}/10")

    actions = ["Back"]
    if req.direction == "inbound" and req.status == "pending":
        actions = ["Accept", "Reject", "Back"]
    elif req.direction == "inbound" and req.status in {"accepted", "awaiting_verse"}:
        actions = ["Work on my verse", "Back"]
    elif req.direction == "inbound" and req.status == "verse_sent":
        actions = ["Back"]
    elif req.direction == "outbound" and req.status == "verse_sent":
        actions = ["Accept", "Reject", "Back"]

    choice = choose_from_list("Request actions", actions, allow_cancel=False)
    if actions[choice] == "Back":
        return

    if req.direction == "inbound" and req.status == "pending":
        if actions[choice] == "Accept":
            req.status = "awaiting_verse"
            if req.paid > 0:
                player_artist.money += req.paid
                print(f"{req.artist_name}: i'll send {money_fmt(req.paid)} for the verse.")
            print(f"You: i'm in. send me the details.")
        elif actions[choice] == "Reject":
            req.status = "rejected"
            print(f"You turned it down.")
            _apply_relationship_delta(player_artist, req.artist_name, -random.uniform(0.6, 2.0))
        return

    if req.direction == "inbound" and req.status in {"accepted", "awaiting_verse"} and actions[choice] == "Work on my verse":
        from rapsim_reviews.career_mode import apply_action_cost, calculate_song_quality
        # Roll verse quality until kept, then send once the player is happy.
        while True:
            apply_action_cost(player_artist, fatigue_cost=8.0, health_risk=0.05)
            # Use the player's skills and the request's song quality as a loose proxy by picking a genre
            # from the player's current song pool when possible.
            genre = "hip hop"
            if player_artist.singles:
                genre = player_artist.singles[0].song.genres[0] if player_artist.singles[0].song.genres else "hip hop"
            rolled = calculate_song_quality(player_artist, [genre])
            print(f"Rolled verse quality: {rolled}/10")
            keep = choose_from_list("Keep this take?", ["Keep", "Reroll", "Cancel"], allow_cancel=False)
            if keep == 2:
                return
            if keep == 1:
                continue
            req.player_verse_quality = rolled
            send = choose_from_list("Send this verse?", ["Send", "Hold"], allow_cancel=False)
            if send == 0:
                req.status = "verse_sent"
                print("You sent the verse.")
                return
            return

    if req.direction == "outbound" and req.status == "verse_sent":
        if actions[choice] == "Accept":
            req.status = "completed"
            # Boost the player's song quality in-place if it still exists unreleased.
            applied = False
            for entry in player_artist.singles:
                if entry.song.name == req.song_name and not entry.released:
                    kind = getattr(req, "request_kind", "feature")
                    old_quality = float(entry.song.quality)
                    if kind == "feature":
                        entry.song.name = _add_feature_to_title(entry.song.name, req.artist_name)
                        if req.artist_name not in entry.features:
                            entry.features.append(req.artist_name)
                    elif kind == "producer":
                        entry.producer = req.artist_name
                        if "(prod." not in entry.song.name.lower():
                            entry.song.name = f"{entry.song.name} (prod. {req.artist_name})"
                    else:
                        entry.engineer = req.artist_name
                    entry.song.quality = round((entry.song.quality * 0.7) + (req.artist_verse_quality * 0.3), 1)
                    seed = _ecosystem_seed_by_name(req.artist_name)
                    if kind == "feature":
                        _ensure_song_bg_attrs(entry.song, player_artist.skills)
                        _apply_feature_bg_delta(entry.song, seed, increased=(entry.song.quality > old_quality))
                    elif kind == "producer":
                        _apply_producer_bg(entry.song, seed)
                    else:
                        _apply_engineer_bg(entry.song, seed)
                    applied = True
                    break

            if not applied and getattr(req, "player_album_name", None):
                for a in player_artist.albums:
                    if a.released or a.album.name != req.player_album_name:
                        continue
                    for s in a.album.songs:
                        if s.name != req.song_name:
                            continue
                        kind = getattr(req, "request_kind", "feature")
                        old_quality = float(s.quality)
                        if kind == "feature":
                            s.name = _add_feature_to_title(s.name, req.artist_name)
                        elif kind == "producer":
                            if "(prod." not in s.name.lower():
                                s.name = f"{s.name} (prod. {req.artist_name})"
                        # Engineer isn't shown in title for player songs right now.
                        s.quality = round((s.quality * 0.7) + (req.artist_verse_quality * 0.3), 1)
                        seed = _ecosystem_seed_by_name(req.artist_name)
                        if kind == "feature":
                            _ensure_song_bg_attrs(s, player_artist.skills)
                            _apply_feature_bg_delta(s, seed, increased=(s.quality > old_quality))
                        elif kind == "producer":
                            _apply_producer_bg(s, seed)
                        else:
                            _apply_engineer_bg(s, seed)
                        applied = True
                        break
                    if applied:
                        break
            _apply_relationship_delta(player_artist, req.artist_name, random.uniform(3.0, 8.0))
            _apply_feature_popularity_boost(player_artist, amount=5.0, weeks=3)
            print(f"{req.artist_name}: locked. sending it through.")
        elif actions[choice] == "Reject":
            req.status = "rejected"
            req.rejected_by_player = True
            print("You rejected it.")
        return

