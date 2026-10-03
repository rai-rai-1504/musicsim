"""rapsim_reviews.career_mode
Top-level career mode orchestrator, simulation loop, character progression,
and main CLI gameplay interface.

Refactored into domain-focused subsystem modules while maintaining 100% backward
compatibility via full re-exports.
"""
from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING
from uuid import uuid4

# ──────────────────────────────────────────────────────────────────────
#  RE-EXPORTS FROM MODULAR SUBSYSTEMS (100% BACKWARD COMPATIBILITY)
# ──────────────────────────────────────────────────────────────────────
from rapsim_reviews.date_system import format_week_range, format_release_date, assign_release_days
from rapsim_reviews import (
    ui_helpers as _ui_helpers,
    career_models as _career_models,
    critic_system as _critic_system,
    sales_system as _sales_system,
    news_system as _news_system,
    grammy_system as _grammy_system,
    romance_system as _romance_system,
    twitter_system as _twitter_system,
    ratings_system as _ratings_system,
    feature_system as _feature_system,
    catalog_system as _catalog_system,
    label_system as _label_system,
)
from rapsim_reviews.ui_helpers import *
from rapsim_reviews.career_models import *
from rapsim_reviews.critic_system import *
from rapsim_reviews.sales_system import *
from rapsim_reviews.news_system import *
from rapsim_reviews.grammy_system import *
from rapsim_reviews.romance_system import *
from rapsim_reviews.twitter_system import *
from rapsim_reviews.ratings_system import *
from rapsim_reviews.feature_system import *
from rapsim_reviews.catalog_system import *
from rapsim_reviews.label_system import *

for _mod in (
    _ui_helpers,
    _career_models,
    _critic_system,
    _sales_system,
    _news_system,
    _grammy_system,
    _romance_system,
    _twitter_system,
    _ratings_system,
    _feature_system,
    _catalog_system,
    _label_system,
):
    for _k, _v in _mod.__dict__.items():
        if not _k.startswith('__'):
            globals()[_k] = _v


# ──────────────────────────────────────────────────────────────────────
#  CORE ENGINE & SIMULATION IMPORTS
# ──────────────────────────────────────────────────────────────────────
from rapsim_reviews.track_review import Simulation, Song, GENRES, THEMES
from rapsim_reviews.album_review import AlbumSimulation, Album, MIN_SONGS
from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS, ARTIST_LOVINGNESS

from rapsim_reviews.artist_ecosystem_sim import (
    create_world,
    step_world,
    prepare_release_calendar,
    roll_catchiness_value,
    roll_virality_value_and_maturity,
    stream_decay_multiplier,
    stream_random_range,
    catchiness_stream_multiplier,
    classify_artist_skills,
    ARTIST_BASE_REPUTATION,
)
from rapsim_reviews.live_module import go_live
from rapsim_reviews.concert_system import ConcertBooking, concerts_menu, run_concert, VENUES, DEFAULT_PRICE_TEMPLATES
from rapsim_reviews.diss_track_system import (
    build_scheduled_tweets,
    display_diss_track,
    ensure_diss_state,
    is_hip_hop_artist,
    release_diss_track,
    schedule_verdict,
    should_release_diss_track,
    should_respond_to_diss,
    step_diss_streams,
)
from rapsim_reviews.beat_system import (
    BeatNegotiation,
    BeatPack,
    PACK_DISCOUNT_DEFAULT,
    PACK_SIZE_OPTIONS,
    accept_negotiation,
    add_beat_to_vault,
    apply_prod_credit_to_title,
    available_vault_beats_for_song_genres,
    beat_by_id,
    beat_has_pending_negotiation,
    beat_is_in_any_pack,
    beat_genre_matches_song,
    catalog_sellers_grouped,
    create_outbound_negotiation,
    solo_listed_beats,
    create_player_beat,
    ensure_beat_market,
    estimated_pack_weekly_sale_probability,
    estimated_weekly_sale_probability,
    format_listing_menu_line,
    format_pricing_help,
    format_seller_menu_line,
    genre_mismatch_penalty_amount,
    player_listable_beats,
    purchase_ecosystem_listing,
    producer_will_accept_offer,
    roll_beat_quality,
    sales_analytics_summary,
    step_beat_market_week,
    suggested_list_price,
    suggested_pack_price,
    vault_beats,
)


if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld

def clamp_stat(value):
    return max(1, min(100, int(value)))


def weighted_choice_from_pool(pool: list[dict]) -> dict:
    return random.choices(pool, weights=[max(0.0, float(item.get("w", 1))) for item in pool], k=1)[0]


def choose_medium(controversy_type, loop_count):
    pool = dict(MEDIUM_WEIGHTS)
    if loop_count > 0:
        pool.pop("song", None)
    if controversy_type in (1, 3):
        pool.pop("song", None)
    return weighted_choice(pool)


def course_cost_for_level(level):
    if level < 40:
        return 250.0
    if level < 60:
        return 1000.0
    if level < 80:
        return 5000.0
    if level < 90:
        return 20000.0
    return 100000.0


def live_decay_value(current_boost):
    if current_boost <= 0:
        return 0.0
    if current_boost > 2.0:
        return random.uniform(1.0, 2.0)
    return 0.0


def choose_song_genres():
    count = prompt_int("How many genres for this song? (1 or 2): ", 1, 2)
    return choose_unique_items("Pick song genre", GENRES, count)


def choose_theme():
    return choose_item_from_list("Pick theme", THEMES, allow_cancel=False)


def parse_duration():
    mins = prompt_int("Minutes: ", 0)
    secs = prompt_int("Seconds: ", 0, 59)
    return mins * 60 + secs


def weighted_skill_score(artist, genre):
    weights = GENRE_SKILL_WEIGHTS[genre]
    return sum(artist.skills[skill] * weight for skill, weight in weights.items())


def roll_song_quality(max_quality, fatigue):
    max_quality = max(0.0, min(10.0, max_quality))
    if max_quality <= 0:
        return 0.0 if fatigue > 100 else 0.1

    low = max(0.0, max_quality - 2.5)
    if max_quality <= 5.0:
        rolled = random.uniform(low, max_quality)
    else:
        band_roll = random.random()
        if band_roll < 0.20:
            rolled = random.uniform(max(low, max_quality - 2.5), max(low, max_quality - 2.0))
        elif band_roll < 0.80:
            rolled = random.uniform(max(low, max_quality - 2.0), max(low, max_quality - 1.0))
        elif band_roll < 0.90:
            rolled = random.uniform(max(low, max_quality - 1.0), max(low, max_quality - 0.5))
        else:
            rolled = random.uniform(max(low, max_quality - 0.5), max_quality)

    if fatigue <= 100.0:
        rolled = max(0.1, rolled)
    else:
        rolled = max(0.0, rolled)
    return round(min(10.0, rolled), 1)


def _roll_bg_attribute_from_skill(skill_value: float) -> float:
    # skill_value is 0-100; attribute lives ~1-10 but typically below 9.5.
    s = float(skill_value) / 10.0
    lo = max(1.0, s - 2.0)
    hi = max(lo, s)
    return round(random.uniform(lo, hi), 1)


def _jitter_attribute(value: float, span: float = 0.4, lo: float = 1.0, hi: float = 9.9) -> float:
    return round(max(lo, min(hi, random.uniform(value - span, value + span))), 1)


def _ensure_song_bg_attrs(song: Song, artist_skills: dict) -> None:
    if getattr(song, "bg_lyrics", None) is None:
        song.bg_lyrics = _roll_bg_attribute_from_skill(artist_skills.get("lyrics", 25))
    if getattr(song, "bg_vocals", None) is None:
        song.bg_vocals = _roll_bg_attribute_from_skill(artist_skills.get("vocals", 25))
    if getattr(song, "bg_production", None) is None:
        song.bg_production = _roll_bg_attribute_from_skill(artist_skills.get("production", 25))
    if getattr(song, "bg_mix", None) is None:
        song.bg_mix = _roll_bg_attribute_from_skill(artist_skills.get("mix/master", 25))


def _apply_producer_bg(song: Song, producer_seed) -> None:
    if song is None or producer_seed is None:
        return
    prod_skill = float(getattr(producer_seed, "skills", {}).get("production", 50))
    song.bg_production = _roll_bg_attribute_from_skill(prod_skill)


def _apply_engineer_bg(song: Song, engineer_seed) -> None:
    if song is None or engineer_seed is None:
        return
    mix_skill = float(getattr(engineer_seed, "skills", {}).get("mix/master", 50))
    song.bg_mix = _roll_bg_attribute_from_skill(mix_skill)


def calculate_song_quality(artist, genres, theme=None):
    # `theme` is currently unused (themes are not yet part of the player Artist model),
    # but we accept it for backward compatibility with older call sites.
    craft = sum(weighted_skill_score(artist, genre) for genre in genres) / len(genres)
    genre_mastery = sum(artist.genres[genre] for genre in genres) / len(genres)
    blend_penalty = 0.0
    if len(genres) == 2:
        gap = abs(artist.genres[genres[0]] - artist.genres[genres[1]])
        blend_penalty = min(6.0, gap * 0.08)
    raw_percent = max(1.0, (craft * 0.62) + (genre_mastery * 0.38) - blend_penalty)
    consistency_range = random.uniform(-0.35, 0.35)
    curved = 1.0 + 8.25 * ((raw_percent / 100.0) ** 2.35)

    # Rare "everything clicked" outcome: even maxed artists only touch 10 occasionally.
    inspiration_bonus = 0.0
    if raw_percent >= 96 and random.random() < 0.02:
        inspiration_bonus = random.uniform(0.45, 0.9)
    elif raw_percent >= 90 and random.random() < 0.008:
        inspiration_bonus = random.uniform(0.15, 0.45)

    fatigue_penalty = max(0.0, (artist.fatigue - 75.0) / 10.0)
    overfatigue_penalty = max(0.0, (artist.fatigue - 100.0) / 4.5)
    health_penalty = max(0.0, (50.0 - artist.health) / 22.0)
    quality = curved + consistency_range + inspiration_bonus - fatigue_penalty - health_penalty
    quality -= overfatigue_penalty
    quality = max(0.0, min(10.0, quality))
    return roll_song_quality(quality, artist.fatigue)


def weighted_skill_score_excluding_production(artist, genre):
    """Lyrics, vocals, and mix/master only — production comes from the vault beat separately."""
    weights = GENRE_SKILL_WEIGHTS[genre]
    total = 0.0
    weight_sum = 0.0
    for skill, weight in weights.items():
        if skill == "production":
            continue
        total += float(artist.skills[skill]) * weight
        weight_sum += weight
    if weight_sum <= 0:
        return float(artist.skills.get("vocals", 25))
    return total / weight_sum


def _song_quality_cap_before_roll(artist, genres, craft, beat_genre=None) -> float:
    genre_mastery = sum(artist.genres[genre] for genre in genres) / len(genres)
    blend_penalty = 0.0
    if len(genres) == 2:
        gap = abs(artist.genres[genres[0]] - artist.genres[genres[1]])
        blend_penalty = min(6.0, gap * 0.08)
    raw_percent = max(1.0, (craft * 0.62) + (genre_mastery * 0.38) - blend_penalty)
    consistency_range = random.uniform(-0.35, 0.35)
    curved = 1.0 + 8.25 * ((raw_percent / 100.0) ** 2.35)
    inspiration_bonus = 0.0
    if raw_percent >= 96 and random.random() < 0.02:
        inspiration_bonus = random.uniform(0.45, 0.9)
    elif raw_percent >= 90 and random.random() < 0.008:
        inspiration_bonus = random.uniform(0.15, 0.45)
    fatigue_penalty = max(0.0, (artist.fatigue - 75.0) / 10.0)
    overfatigue_penalty = max(0.0, (artist.fatigue - 100.0) / 4.5)
    health_penalty = max(0.0, (50.0 - artist.health) / 22.0)
    quality = curved + consistency_range + inspiration_bonus - fatigue_penalty - health_penalty
    quality -= overfatigue_penalty
    if beat_genre is not None and not beat_genre_matches_song(beat_genre, genres):
        quality -= genre_mismatch_penalty_amount()
    return max(0.0, min(10.0, quality))


def calculate_song_quality_with_vault_beat(artist, genres, beat_quality, beat_genre=None, theme=None):
    """Roll from lyrics/vocals/mix/master, then add 25% of beat quality (60-100% of that share)."""
    craft = sum(weighted_skill_score_excluding_production(artist, genre) for genre in genres) / len(genres)
    cap = _song_quality_cap_before_roll(artist, genres, craft, beat_genre=beat_genre)
    base_quality = roll_song_quality(cap, artist.fatigue)
    beat_share = float(beat_quality) * 0.25
    beat_bonus = beat_share * random.uniform(0.6, 1.0)
    final_quality = round(min(10.0, base_quality + beat_bonus), 1)
    return final_quality, base_quality, round(beat_bonus, 1)


def choose_beat_genre():
    idx = choose_from_list("What genre is this beat?", GENRES, allow_cancel=False)
    return GENRES[idx]


def create_artist():
    name = prompt_text("Enter artist name: ", "Untitled Artist")
    gender = _prompt_gender()
    sexuality = _prompt_sexuality(gender)
    chosen_skills = choose_unique_items("Choose starting skill", SKILLS, 2)
    chosen_genres = choose_unique_items("Choose starting genre", GENRES, 2)

    if TEST_START_MAXED:
        skills = {skill: 90 for skill in SKILLS}
        genres = {genre: 90 for genre in GENRES}
    else:
        skills = {skill: 25 for skill in SKILLS}
        for skill in chosen_skills:
            skills[skill] = 60
        genres = {genre: 30 for genre in GENRES}
        for genre in chosen_genres:
            genres[genre] = 60

    artist = Artist(
        name=name,
        skills=skills,
        genres=genres,
        gender=_validate_gender(gender),
        sexuality=_validate_sexuality_for_gender(gender, sexuality),
        romance_preference=_romance_preference_from_identity(gender, sexuality),
    )
    if TEST_START_MAXED:
        artist.money = float(TEST_START_MONEY)
        artist.popularity_state.organic = float(TEST_START_POPULARITY)
        artist.live_popularity = float(TEST_START_POPULARITY)
        
        # Populate catalog with 12 unreleased songs with varying attributes
        test_tracks = [
            ("Spitfire", 8.5, 9.0, 8.0, "rage", 165),
            ("Midnight Melancholy", 7.2, 5.0, 6.5, "heartbreak", 210),
            ("Neon Nights", 6.0, 8.5, 9.0, "party", 195),
            ("Street Philosophy", 9.2, 4.0, 5.0, "street life", 240),
            ("Dreamscape", 5.5, 7.0, 7.5, "euphoria", 180),
            ("Lost Echoes", 7.8, 6.0, 5.5, "nostalgia", 205),
            ("Heavy Heart", 4.5, 3.0, 4.0, "love", 190),
            ("Rebel Cry", 8.0, 7.5, 7.0, "protest", 215),
            ("Shadow Play", 3.5, 6.5, 8.0, "existential", 170),
            ("Aura", 9.5, 10.0, 9.5, "spirituality", 185),
            ("Basement Freestyle", 5.0, 2.0, 3.0, "rage", 150),
            ("Cyber Love", 6.8, 8.0, 8.5, "love", 200),
        ]
        for name_t, qual, viral, catch, theme_t, dur in test_tracks:
            dummy_song = Song(
                quality=qual,
                name=name_t,
                genres=["hip hop"],
                theme=theme_t,
                duration=dur,
                catchiness=catch,
                virality=viral
            )
            song_entry = SongEntry(
                song=dummy_song,
                released=False,
                average_review=qual,
                source_label="Single"
            )
            artist.singles.append(song_entry)
    if TEST_RELATIONSHIP_BOOTSTRAP:
        seeds = sorted(ARTIST_ECOSYSTEM_SEEDS, key=lambda s: s.name.lower())
        for seed in seeds:
            score = 100.0 if TEST_RELATIONSHIP_LOCK else 20.0
            artist.relationships[seed.name] = RelationshipState(
                score=score,
                last_interaction_week=0,
                last_contact_week=0,
            )
        if TEST_RELATIONSHIP_LOCK:
            setattr(artist, "_relationship_lock", True)
    else:
        for seed in ARTIST_ECOSYSTEM_SEEDS:
            friendly = int(getattr(seed, "friendliness", 50))
            base = random.uniform(5.0, 12.0) + (friendly / 100.0) * 18.0
            artist.relationships[seed.name] = RelationshipState(
                score=clamp_meter(base),
                last_interaction_week=0,
                last_contact_week=0,
            )
    ensure_beat_market(artist)
    return artist


def display_artist(artist):
    print("\n" + "=" * 72)
    print(f"{artist.name} | {format_week_range(year=artist.year, week=artist.week)}")
    print(meter_bar("Health ", artist.health))
    print(meter_bar("Fatigue", artist.fatigue, invert=True))
    print(meter_bar("Popular", artist.popularity))
    print(f"Reputation: {artist.reputation:.1f}%")
    if getattr(artist, "concert_history", None):
        print(f"Live Perf : {artist.live_performance_rating:.1f}/100")
    current_love = _player_current_love(artist)
    if current_love is not None:
        print(meter_bar("Love   ", current_love.lovingness))
        print(f"Partner: {current_love.partner_name} ({current_love.status})")
    print(f"Money  : {money_fmt(artist.money)}")
    if artist.current_course:
        print(
            f"Course in progress: {artist.current_course} "
            f"({artist.course_weeks_left} weeks left)"
        )
    if artist.management:
        print(
            f"Management: {artist.management.company_name} "
            f"({artist.management.term_label}, {artist.management.weeks_left} weeks left, "
            f"{artist.management.stream_cut_pct:.1f}% cut, "
            f"base pop {artist.management.current_weekly_popularity:.1f}%, "
            f"billing {money_fmt(artist.management.billing_amount)} "
            f"every {artist.management.billing_every_weeks} week(s))"
        )
    if artist.side_hustle:
        print(
            f"Job: {artist.side_hustle.job_name} "
            f"({artist.side_hustle.weeks_left} weeks left, pays {money_fmt(artist.side_hustle.weekly_pay)}/week, "
            f"fatigue load {artist.side_hustle.weekly_fatigue:.1f}%)"
        )
    print("\nSkills")
    for skill in SKILLS:
        print(f"- {skill}: {artist.skills[skill]}/100")

    print("\nGenres")
    for genre in GENRES:
        if artist.genres[genre] > 10:
            print(f"- {genre}: {artist.genres[genre]}/100")

    unreleased_singles = [entry for entry in artist.singles if not entry.released]
    unreleased_albums = [entry for entry in artist.albums if not entry.released]
    print(f"\nUnreleased singles: {len(unreleased_singles)}")
    print(f"Album drafts: {len(unreleased_albums)}")
    if artist.last_week_streams > 0 or artist.last_week_earnings > 0:
        print(
            f"Last week: {artist.last_week_streams:,} streams | "
            f"{money_fmt(artist.last_week_earnings)} earned"
        )


def _world_release_editions(world: EcosystemWorld, release_id: str) -> list[PhysicalEdition]:
    _ensure_sales_state(world)
    if release_id not in world.physical_inventory_by_release:
        world.physical_inventory_by_release[release_id] = []
    return world.physical_inventory_by_release[release_id]


def _ecosystem_release_quality(release) -> float:
    tracks = list(getattr(release, "tracks", None) or ())
    if tracks:
        return sum(float(getattr(track, "quality", getattr(release, "quality", 0.0))) for track in tracks) / len(tracks)
    return float(getattr(release, "quality", 0.0))


def _releases_for_week(world: EcosystemWorld, week_number: int) -> list:
    rows = []
    for artist_name, releases in world.release_history.items():
        for release in releases:
            if int(getattr(release, "week_number", -1)) == int(week_number):
                rows.append(release)
    return rows


def apply_action_cost(artist, fatigue_cost, health_risk=0.0):
    import inspect
    caller_name = ""
    try:
        stack = inspect.stack()
        for frame in stack:
            if frame.function in {"create_song_for_artist", "create_beats_action", "run_concert", "concerts_menu", "charity_show"}:
                caller_name = frame.function
                break
    except Exception:
        pass

    if not caller_name:
        fatigue_cost = 0.0

    fatigue_multiplier = 1.0 + max(0.0, (100.0 - artist.health) / 180.0)
    if artist.current_course:
        fatigue_multiplier *= 1.15
    artist.fatigue = clamp_fatigue(artist.fatigue + (fatigue_cost * fatigue_multiplier))

    if artist.fatigue >= 110:
        artist.health = clamp_meter(
            artist.health - (health_risk * 1.1) - random.uniform(0.8, 1.8)
        )
    elif artist.fatigue >= 100:
        artist.health = clamp_meter(
            artist.health - (health_risk * 0.8) - random.uniform(0.4, 1.0)
        )
    elif artist.fatigue >= 90:
        artist.health = clamp_meter(
            artist.health - (health_risk * 0.35) - random.uniform(0.1, 0.4)
        )


def add_popularity(artist, amount):
    artist.popularity_state.organic = clamp_popularity(
        artist.popularity_state.organic + amount
    )


def too_exhausted_for_skill_gain(artist):
    return artist.fatigue >= 100.0


def skill_training_profile(current_value):
    if current_value < 30:
        return 6.0, 100.0
    if current_value < 50:
        return 7.5, 85.0
    if current_value < 70:
        return 9.0, 65.0
    if current_value < 80:
        return 11.0, 45.0
    if current_value < 90:
        return 13.5, 30.0
    return 16.0, 20.0


def action_locked_by_health(artist, action_name):
    if artist.health < 20.0:
        print(
            f"You are in terrible health right now. {action_name} is locked until you recover. "
            "Only going live is still available."
        )
        return True
    return False


def practice_skill(artist, skill_name):
    if action_locked_by_health(artist, f"working on {skill_name}"):
        return
    current_value = artist.skills[skill_name]
    fatigue_cost, fatigue_limit = skill_training_profile(current_value)
    if artist.fatigue > fatigue_limit:
        print(
            f"{skill_name} is hard to improve at this level. You need to be under "
            f"{int(fatigue_limit)}% fatigue to push it higher."
        )
        return
    apply_action_cost(artist, fatigue_cost=fatigue_cost, health_risk=0.18)
    if too_exhausted_for_skill_gain(artist):
        print(
            f"You tried to work on {skill_name}, but you are completely exhausted. "
            "No skill gain this time."
        )
        return
    artist.skills[skill_name] = clamp_stat(artist.skills[skill_name] + 1)
    print(f"{skill_name} improved to {artist.skills[skill_name]}/100.")


def start_genre_course(artist):
    if action_locked_by_health(artist, "starting a genre course"):
        return
    if artist.current_course:
        print("You are already enrolled in a genre course.")
        return
    idx = choose_from_list("Choose a genre course", GENRES, allow_cancel=True)
    if idx is None:
        return
    target_genre = GENRES[idx]
    course_cost = course_cost_for_level(artist.genres[target_genre])
    if artist.money < course_cost:
        print(
            f"You need {money_fmt(course_cost)} to start a {target_genre} course. "
            f"Current balance: {money_fmt(artist.money)}."
        )
        return
    apply_action_cost(artist, fatigue_cost=5.0, health_risk=0.15)
    artist.current_course = target_genre
    artist.course_weeks_left = 12
    artist.money -= course_cost
    print(
        f"Started a 12-week {artist.current_course} course for {money_fmt(course_cost)}."
    )


def create_album_entry():
    album_name = prompt_text("Album name: ", "Untitled Album")
    core_genre = GENRES[choose_from_list("Choose album core genre", GENRES)]
    core_theme = THEMES[choose_from_list("Choose album core theme", THEMES)]
    album = Album(album_name, core_genre, core_theme)
    return AlbumEntry(album=album)


def create_album_draft(artist):
    if action_locked_by_health(artist, "creating an album draft"):
        return
    apply_action_cost(artist, fatigue_cost=4.5, health_risk=0.1)
    entry = create_album_entry()
    artist.albums.append(entry)
    print(
        f"Created album draft '{entry.album.name}'. "
        f"Minimum songs before release: {MIN_SONGS}."
    )


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


def create_song_for_artist(artist):
    if action_locked_by_health(artist, "creating songs"):
        return
    apply_action_cost(artist, fatigue_cost=8.5, health_risk=0.18)

    genres = choose_song_genres()
    theme = choose_theme()
    market = ensure_beat_market(artist)
    vault_options = available_vault_beats_for_song_genres(market, genres)
    selected_beat = None
    if vault_options:
        use_beat = choose_from_list(
            "Use a beat from your Beat Vault?",
            ["No — roll without a vault beat", "Yes — choose a matching-genre vault beat"],
            allow_cancel=False,
        )
        if use_beat == 1:
            labels = [
                f"{beat.name} | {beat.genre} | {beat.quality}/10"
                + (
                    f" | prod. {beat.producer_name}"
                    if beat.producer_name
                    else ""
                )
                for beat in vault_options
            ]
            pick = choose_from_list("Choose vault beat (must match song genre)", labels, allow_cancel=True)
            if pick is not None:
                selected_beat = vault_options[pick]
    else:
        all_unused = [b for b in market.vault if not b.consumed]
        if all_unused:
            print(
                "\nNo vault beats match this song's genre. "
                "Using a beat from another genre would hurt song quality — create or buy a matching beat first."
            )

    beat_bonus = 0.0
    base_vocal_quality = None
    if selected_beat is not None:
        quality, base_vocal_quality, beat_bonus = calculate_song_quality_with_vault_beat(
            artist, genres, selected_beat.quality, beat_genre=selected_beat.genre
        )
        print(
            f"\nUsing vault beat '{selected_beat.name}' ({selected_beat.genre}, {selected_beat.quality}/10)."
        )
        print(
            f"Lyrics/vocals/mix roll: {base_vocal_quality}/10 | "
            f"Beat adds +{beat_bonus} (25% of {selected_beat.quality}/10, randomized) | "
            f"Combined: {quality}/10"
        )
    else:
        quality = calculate_song_quality(artist, genres)
    catchiness = roll_catchiness_value()
    virality, maturity = roll_virality_value_and_maturity()

    print("\nSong rolled.")
    print(f"Quality: {quality}/10")
    print(f"Catchiness: {catchiness} (0.1-5)")
    print(f"Virality: {virality} (1-5) | maturity in {maturity} weeks after release")
    keep_choice = choose_from_list(
        "Do you want to keep this song idea?",
        ["Keep it", "Discard it"],
        allow_cancel=False,
    )
    if keep_choice == 1:
        print("You scrapped the song idea and moved on.")
        return

    name = prompt_text("Song name: ", "Untitled")
    if selected_beat is not None and selected_beat.producer_name:
        name = apply_prod_credit_to_title(name, selected_beat.producer_name)
        print(f"Credited on title: (prod. {selected_beat.producer_name})")
    print("\nSong duration")
    duration = parse_duration()
    if selected_beat is not None:
        bg_production = round(float(selected_beat.quality), 1)
    else:
        bg_production = _roll_bg_attribute_from_skill(artist.skills.get("production", 25))
    song = Song(
        quality,
        name,
        genres,
        theme,
        duration,
        catchiness=catchiness,
        virality=virality,
        maturity_weeks=maturity,
        bg_lyrics=_roll_bg_attribute_from_skill(artist.skills.get("lyrics", 25)),
        bg_vocals=_roll_bg_attribute_from_skill(artist.skills.get("vocals", 25)),
        bg_production=bg_production,
        bg_mix=_roll_bg_attribute_from_skill(artist.skills.get("mix/master", 25)),
    )
    if selected_beat is not None:
        selected_beat.consumed = True
        selected_beat.listed = False
        song.beat_id = selected_beat.beat_id
        song.beat_quality = float(selected_beat.quality)

    print(f"\nSong created: '{song.name}'")
    print(f"Computed quality: {song.quality}/10")
    print(f"Genres: {song.genre_label()} | Theme: {song.theme}")

    destination = choose_from_list(
        "Where should this song go?",
        ["Add to album", "Keep as single"],
        allow_cancel=False,
    )
    if destination == 0:
        album_entry = choose_album_draft(artist, allow_create=True)
        if album_entry is None:
            artist.singles.append(SongEntry(song=song, source_label="Single"))
            print("No album selected, so the song was saved as a single.")
            return
        album_entry.album.add_song(song)
        print(
            f"Added '{song.name}' to '{album_entry.album.name}' "
            f"({album_entry.album.song_count()} tracks)."
        )
        return

    artist.singles.append(SongEntry(song=song, source_label="Single"))
    print(f"Saved '{song.name}' as an unreleased single.")


def create_deluxe_draft(artist):
    if action_locked_by_health(artist, "creating a deluxe draft"):
        return
    apply_action_cost(artist, fatigue_cost=4.0, health_risk=0.1)
    released = [entry for entry in artist.albums if entry.released]
    if not released:
        print("No released albums are available for a deluxe edition.")
        return
    options = [
        f"{entry.album.name} - {entry.album.song_count()} tracks"
        for entry in released
    ]
    idx = choose_from_list("Choose released album for a deluxe edition", options, True)
    if idx is None:
        return

    source = released[idx]
    deluxe_name = prompt_text(
        "Deluxe title: ",
        f"{source.album.name} (Deluxe)",
    )
    deluxe_album = Album(deluxe_name, source.album.core_genre, source.album.core_theme)
    for song in source.album.songs:
        deluxe_album.add_song(song)
    entry = AlbumEntry(album=deluxe_album, deluxe_of=source.album.name)
    artist.albums.append(entry)
    print(
        f"Created deluxe draft '{deluxe_album.name}' with "
        f"{deluxe_album.song_count()} carried-over tracks."
    )


def go_live_action(artist):
    apply_action_cost(artist, fatigue_cost=1.5, health_risk=0.03)
    artist.live_count_this_week += 1
    artist.popularity_state.live_boost = min(
        LIVE_WEEKLY_POP_CAP, artist.popularity_state.live_boost + 2.0
    )
    go_live(artist)


def update_course(artist):
    if artist.current_course is None:
        return
    artist.course_weeks_left -= 1
    if artist.course_weeks_left <= 0:
        artist.genres[artist.current_course] = clamp_stat(
            artist.genres[artist.current_course] + 10
        )
        print(f"Course complete. {artist.current_course} increased by +10.")
        artist.current_course = None
        artist.course_weeks_left = 0


def stream_decay_multiplier(weeks_since_release):
    if weeks_since_release < 4:
        return 1.0
    if weeks_since_release >= 11:
        return 0.05
    progress = (weeks_since_release - 3) / 8.0
    return 1.0 - (0.95 * progress)


def stream_random_range(base_streams):
    growth = min(1.0, base_streams / 200000.0)
    low_mult = 0.6 + (0.18 * growth)
    high_mult = 1.2 - (0.14 * growth)
    return low_mult, high_mult


def catchiness_stream_multiplier(catchiness):
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
        (5.0, 8.0),
    ]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if c <= x1:
            t = (c - x0) / (x1 - x0)
            return y0 + (y1 - y0) * t
    return points[-1][1]


def virality_bonus_for_week(entry: SongEntry, streams_base: int):
    song = entry.song
    v = getattr(song, "virality", None)
    maturity = getattr(song, "maturity_weeks", None)
    if v is None or maturity is None:
        return 0
    if v < 2.0:
        return 0
    if not entry.virality_triggered and entry.weeks_since_release >= maturity:
        entry.virality_triggered = True
        entry.virality_weeks_active = 0
        entry.virality_max_weekly_bonus = 0
        entry.virality_baseline_streams = int(max(0, streams_base))

    if not entry.virality_triggered:
        return 0

    age = entry.virality_weeks_active
    if v < 3.0:
        lo, hi = 100_000, 500_000
    elif v < 4.0:
        lo, hi = 2_000_000, 10_000_000
    else:
        lo, hi = 30_000_000, 70_000_000

    if age <= 7:
        bonus = int(random.uniform(lo, hi))
        entry.virality_max_weekly_bonus = max(entry.virality_max_weekly_bonus, bonus)
        return bonus

    peak = max(entry.virality_max_weekly_bonus, hi)
    floor_bonus = max(int(0.02 * peak), int(entry.virality_baseline_streams))
    t = min(1.0, max(0.0, (age - 8) / 8.0))
    target = (1.0 - t) * peak + t * floor_bonus
    bonus = int(random.uniform(target * 0.88, target * 1.05))
    return max(0, bonus)


def stream_count_for_song(entry, popularity):

    quality_factor = max(0.0, min(1.0, entry.song.quality / 10.0))
    popularity_factor = max(0.0, min(1.0, popularity / 100.0))
    weighted_score = (popularity_factor * 0.7) + (quality_factor * 0.3)

    # Main stream curve (millions at the top end). Popularity drives more than quality,
    # but bad songs still get punished hard even at high popularity.
    base_constant = 2_000_000 if float(popularity) < 20.0 else 10_000_000
    base_streams = base_constant * (weighted_score**1.85) * (quality_factor**1.7)
    base_streams *= stream_decay_multiplier(entry.weeks_since_release)

    catchiness = getattr(entry.song, "catchiness", None)
    base_streams *= catchiness_stream_multiplier(catchiness)

    low_mult, high_mult = stream_random_range(base_streams)
    streams_base = int(random.uniform(base_streams * low_mult, base_streams * high_mult))

    # Without virality, even the biggest records rarely push beyond ~150M/week.
    streams_base = min(150_000_000, streams_base)

    streams = streams_base + virality_bonus_for_week(entry, streams_base)
    return max(0, streams)


def stream_payout(streams):
    base = streams * 0.01
    ten_k_bonus = (streams // 10_000) * 10
    hundred_k_bonus = (streams // 100_000) * 500
    million_bonus = (streams // 1_000_000) * 3000
    return base + ten_k_bonus + hundred_k_bonus + million_bonus


def apply_weekly_management(artist):
    fee = 0.0
    if artist.management:
        artist.management.current_weekly_popularity = random.uniform(
            artist.management.weekly_popularity_range[0],
            artist.management.weekly_popularity_range[1],
        )
        artist.popularity_state.management = artist.management.current_weekly_popularity
        artist.management.weeks_until_payment -= 1
        if artist.management.weeks_until_payment <= 0:
            fee = artist.management.billing_amount
            artist.money -= fee
            artist.management.weeks_until_payment = artist.management.billing_every_weeks
        artist.management.weeks_left -= 1
        if artist.management.weeks_left <= 0:
            print(f"{artist.management.company_name} contract has ended.")
            artist.management = None
    else:
        artist.popularity_state.management = max(
            0.0, artist.popularity_state.management - random.uniform(5.0, 7.0)
        )
    return fee


def advance_release_cycles(artist):
    for entry in artist.singles:
        if not entry.released:
            continue
        if entry.release_popularity_weeks_left > 0:
            entry.release_popularity_weeks_left -= 1
            if entry.release_popularity_weeks_left <= 0:
                entry.release_popularity_value = 0.0
        entry.weeks_since_release += 1
        if entry.virality_triggered:
            entry.virality_weeks_active += 1


def popularity_from_streams(entries):
    caps = {
        "1k": 2.0,
        "10k": 4.0,
        "100k": 8.0,
        "1m": 10.0,
    }
    used = {key: 0.0 for key in caps}
    gained = 0.0

    for entry in sorted(entries, key=lambda e: e.last_week_streams, reverse=True):
        # Album tracks don't add per-track popularity; the album bump covers that.
        if str(getattr(entry, "source_label", "")).startswith("Album:"):
            continue
        streams = entry.last_week_streams
        if streams >= 1_000_000:
            tier, gain = "1m", 5.0
        elif streams >= 100_000:
            tier, gain = "100k", 3.0
        elif streams >= 10_000:
            tier, gain = "10k", 1.0
        elif streams >= 1_000:
            tier, gain = "1k", 0.5
        else:
            continue

        room = caps[tier] - used[tier]
        if room <= 0:
            continue
        add = min(gain, room, 20.0 - gained)
        used[tier] += add
        gained += add
        if gained >= 20.0:
            break

    return gained


def process_weekly_streams(artist):
    total_streams = 0
    gross_income = 0.0
    physical_income = 0.0
    popularity_snapshot = artist.popularity
    for entry in artist.singles:
        if not entry.released:
            entry.last_week_streams = 0
            entry.last_week_digital_sales = 0
            entry.last_week_physical_sales = 0
            continue
        weekly_streams = stream_count_for_song(entry, popularity_snapshot)
        entry.last_week_streams = weekly_streams
        entry.total_streams += weekly_streams
        entry.last_week_digital_sales = int(weekly_streams) // 1000
        entry.total_digital_sales += int(entry.last_week_digital_sales)
        physical_units, physical_revenue = _apply_physical_sales(
            entry.physical_editions,
            weekly_streams=int(weekly_streams),
            popularity=float(popularity_snapshot),
            quality=float(entry.song.quality),
            release_type="single",
        )
        entry.last_week_physical_sales = int(physical_units)
        entry.total_physical_sales += int(physical_units)
        if entry.first_week_sales <= 0 and int(entry.weeks_since_release) == 0:
            entry.first_week_sales = int(entry.last_week_digital_sales + entry.last_week_physical_sales)
        total_streams += weekly_streams
        gross_income += stream_payout(weekly_streams)
        physical_income += float(physical_revenue)

    cut_pct = artist.management.stream_cut_pct if artist.management else 0.0
    management_cut = gross_income * (cut_pct / 100.0)
    net_income = gross_income - management_cut
    for album_entry in artist.albums:
        if not album_entry.released:
            continue
        linked_tracks = [
            linked_entry
            for song in album_entry.album.songs
            for linked_entry in [next((e for e in artist.singles if e.song is song and e.released), None)]
            if linked_entry is not None
        ]
        stream_base = sum(int(track.last_week_streams or 0) for track in linked_tracks)
        avg_quality = (
            sum(float(track.song.quality) for track in linked_tracks) / len(linked_tracks)
            if linked_tracks else float(album_entry.average_review or 5.0)
        )
        physical_units, physical_revenue = _apply_physical_sales(
            album_entry.physical_editions,
            weekly_streams=int(stream_base),
            popularity=float(popularity_snapshot),
            quality=float(avg_quality),
            release_type="deluxe" if album_entry.deluxe_of else "album",
        )
        album_entry.last_week_physical_sales = int(physical_units)
        album_entry.total_physical_sales = sum(int(edition.total_units_sold) for edition in album_entry.physical_editions)
        physical_income += float(physical_revenue)
        _player_album_sales_snapshot(artist, album_entry)
    artist.money += net_income + physical_income
    artist.last_week_streams = total_streams
    artist.last_week_management_cut = management_cut
    artist.last_week_earnings = net_income
    artist.last_week_physical_income = float(physical_income)
    return total_streams, net_income, management_cut, cut_pct, physical_income


def fatigue_after_recovery(previous_fatigue, recurring_fatigue_cost):
    previous_fatigue = clamp_fatigue(previous_fatigue)
    if previous_fatigue <= 0:
        return clamp_fatigue(recurring_fatigue_cost)
    if previous_fatigue <= recurring_fatigue_cost:
        return clamp_fatigue(recurring_fatigue_cost)

    recovery = BASE_WEEKLY_RECOVERY
    if recurring_fatigue_cost > 0:
        recovery -= (recurring_fatigue_cost / 100.0) * BASE_WEEKLY_RECOVERY
    recovery = max(0.0, recovery)
    return clamp_fatigue(previous_fatigue - recovery)


def simulate_week(artist, ecosystem_world: EcosystemWorld | None = None):
    # Run scheduled concerts for the current week index before advancing the week
    current_wk = _player_week_index(artist)
    if not hasattr(artist, "upcoming_concerts"):
        artist.upcoming_concerts = []
    if not hasattr(artist, "concert_history"):
        artist.concert_history = []
    to_run = [b for b in artist.upcoming_concerts if b.week == current_wk]
    for booking in to_run:
        venue = next((v for v in VENUES if v.id == booking.venue_id), None)
        is_owned = False
        ov = None
        if not venue and hasattr(artist, "owned_venues"):
            ov = next((v for v in artist.owned_venues if v.id == booking.venue_id), None)
            if ov:
                is_owned = True
                from rapsim_reviews.concert_system import Venue
                prestige_val = int(ov.review_stars * 18.0)
                ticket_tiers = {"floor": int(ov.base_hire_cost * 0.02), "general": int(ov.base_hire_cost * 0.015), "vip": int(ov.base_hire_cost * 0.05)}
                if ticket_tiers["floor"] <= 0:
                    ticket_tiers = {"floor": 20, "general": 12, "vip": 60}
                venue = Venue(
                    id=ov.id,
                    name=ov.name + " (OWNED)",
                    city="Player City",
                    country="Player Land",
                    category=ov.category,
                    capacity=ov.capacity,
                    popularity_req=0,
                    prestige=prestige_val,
                    organizer_id="org_player",
                    ticket_tiers=ticket_tiers,
                    ambiance_bonus=round((ov.review_stars - 3.0) * 0.1, 2),
                    weekly_availability=list(range(1, 53))
                )
        if venue:
            run_concert(booking, venue, artist, artist.singles, world=ecosystem_world)
            artist.money += booking.net_revenue
            artist.live_popularity = clamp_popularity(artist.live_popularity + booking.live_popularity_delta)
            artist.reputation = clamp_meter(artist.reputation + booking.rep_delta)
            artist.concert_history.append(booking)
            artist.upcoming_concerts.remove(booking)
            
            # Log player show in owned venue
            if is_owned and ov is not None:
                cont_desc = "None"
                if getattr(booking, "controversy_events", None):
                    # Gather descriptions/outcomes of controversy events
                    parts = []
                    for e in booking.controversy_events:
                        desc = e.get("outcome", e.get("desc", ""))
                        if not desc and e.get("news"):
                            desc = "Viral news leak"
                        if desc:
                            parts.append(desc)
                    if parts:
                        cont_desc = "; ".join(parts)
                
                log_entry = {
                    "week": current_wk,
                    "artist_name": artist.name,
                    "attendance": booking.attendance,
                    "gross_revenue": getattr(booking, "gross_revenue", 0.0),
                    "rent_fee": 0.0,
                    "cut_pct": 0.0,
                    "revenue_to_venue": getattr(booking, "net_revenue", 0.0),
                    "controversy": cont_desc
                }
                ov.past_shows_log.append(log_entry)
                ov.past_events_history.append({
                    "week": current_wk,
                    "type": "player_show",
                    "details": f"Hosted your show '{getattr(booking, 'id', 'Concert')}' ({booking.attendance:,} attendees)",
                    "net": getattr(booking, "net_revenue", 0.0)
                })
                
                # Default buzz boost based on artist popularity, capped at 10
                initial_buzz = ov.buzz
                
                # Apply controversy outcome to the venue rating and buzz
                if getattr(booking, "controversy_events", None):
                    for ev in booking.controversy_events:
                        rep_d = ev.get("rep_delta", 0.0)
                        pop_d = ev.get("pop_delta", 0.0)
                        rating_hit = random.uniform(0.1, 0.3) if rep_d >= 0 else -random.uniform(0.8, 1.5)
                        ov.rating_modifier = getattr(ov, "rating_modifier", 0.0) + rating_hit
                        
                        buzz_hit = int(pop_d * 0.8)
                        ov.buzz = max(0.0, min(100.0, ov.buzz + buzz_hit))
                
                # Add default baseline buzz boost for hosting player show
                base_buzz_boost = min(10, int(artist.popularity * 0.10))
                ov.buzz = min(100.0, ov.buzz + base_buzz_boost)
                
                # Ensure total buzz added by the performance is capped at 10
                total_buzz_added = ov.buzz - initial_buzz
                if total_buzz_added > 10:
                    ov.buzz = min(100.0, initial_buzz + 10)
                    
                # Force rating recalculation right after show
                from rapsim_reviews.venue_management import update_venue_ratings
                update_venue_ratings(ov)

    # Step owned venues (taxes, upkeeps, construction, NPC event completions)
    from rapsim_reviews.venue_management import step_owned_venues
    step_owned_venues(artist, ecosystem_world)

    fatigue_before_recovery = artist.fatigue
    update_course(artist)
    management_fee = apply_weekly_management(artist)
    total_streams, net_income, management_cut, cut_pct, physical_income = process_weekly_streams(artist)
    stream_popularity_gain = popularity_from_streams(
        [entry for entry in artist.singles if entry.released]
    )
    artist.popularity_state.weekly_song = stream_popularity_gain
    if artist.popularity_state.album_release_weeks_left > 0:
        artist.popularity_state.album_release_weeks_left -= 1
        if artist.popularity_state.album_release_weeks_left <= 0:
            artist.popularity_state.album_release_boost = 0.0
    advance_release_cycles(artist)
    job_pay, recurring_job_fatigue, reduced_job_pay = process_side_hustle_week(artist)
    artist.week += 1
    if artist.week > 52:
        artist.week = 1
        artist.year += 1
    artist.fatigue = fatigue_after_recovery(fatigue_before_recovery, recurring_job_fatigue)
    health_recovery = random.uniform(4.0, 7.5)
    if artist.fatigue <= 35:
        health_recovery += random.uniform(0.5, 1.5)
    artist.health = clamp_meter(artist.health + health_recovery)
    artist.popularity_state.live_boost = live_decay_value(
        artist.popularity_state.live_boost
    )
    # Feature boost decays over 3 weeks (non-stacking beyond a small cap).
    if artist.popularity_state.feature_boost_weeks_left > 0:
        artist.popularity_state.feature_boost_weeks_left -= 1
        if artist.popularity_state.feature_boost_weeks_left <= 0:
            artist.popularity_state.feature_boost_weeks_left = 0
            artist.popularity_state.feature_boost = 0.0
        else:
            artist.popularity_state.feature_boost = clamp_popularity(
                artist.popularity_state.feature_boost - (5.0 / 3.0)
            )
    artist.live_count_this_week = 0
    artist.last_week_management_fee = management_fee
    _apply_player_love_weekly_effects(artist, ecosystem_world)
    print(f"Simulated forward to {format_week_range(year=artist.year, week=artist.week)}.")
    print(
        f"Weekly payout: {money_fmt(net_income)} | "
        f"Streams: {total_streams:,} | "
        f"Management cut: {cut_pct:.1f}% ({money_fmt(management_cut)})"
    )
    if physical_income > 0:
        print(f"Physical sales income: {money_fmt(physical_income)}")

    # Record Label Recoupment Engine
    contract = getattr(artist, "label_contract", None)
    if contract and getattr(contract, "status", "") in ("active", "shelved", "recouped"):
        lbl = get_label_by_id(contract.label_id)
        if lbl:
            gross_music_pay = net_income + physical_income
            actual_artist_pay = process_weekly_label_recoupment(artist, contract, lbl, gross_music_pay)
            diff = gross_music_pay - actual_artist_pay
            artist.money -= diff
            if contract.recoupment_balance > 0:
                print(f"Label recoupment: {money_fmt(diff)} retained by {lbl.name} (Remaining balance: {money_fmt(contract.recoupment_balance)})")
            elif diff > 0:
                print(f"Label royalty cut: {int(contract.post_recoup_royalty_cut*100)}% ({money_fmt(diff)}) to {lbl.name}")

    if management_fee > 0:
        print(f"Management fee paid: {money_fmt(management_fee)}")
    if job_pay > 0:
        print(f"Side hustle pay: {money_fmt(job_pay)}")
    if reduced_job_pay:
        print("You were extra tired last week, your boss cut some money off.")
    if stream_popularity_gain > 0:
        print(f"Popularity from song performance: +{stream_popularity_gain:.1f}")
    beat_income = step_beat_market_week(artist, ecosystem_world, _player_week_index(artist))
    beat_market = ensure_beat_market(artist)
    if beat_income > 0:
        print(f"Beat Store income: {money_fmt(beat_income)}")
    if beat_market.weekly_notifications:
        print("\nBeat Store this week:")
        for note in beat_market.weekly_notifications[:10]:
            print(f"- {note}")
    if ecosystem_world is not None:
        step_world(ecosystem_world)
        ensure_diss_state(ecosystem_world)
        step_diss_streams(ecosystem_world, ecosystem_world.artist_popularity)
        _sync_diss_runtime_streams(ecosystem_world)
        _step_ecosystem_sales(ecosystem_world)
        _record_ecosystem_low_reviews(ecosystem_world)
        _ensure_news_state(ecosystem_world)
        _ensure_romance_state(ecosystem_world)
        _process_scheduled_diss_news(ecosystem_world, ecosystem_world.week_number)
        release_reports = [] if _is_grammy_media_week(ecosystem_world.week_number) else _generate_new_release_news(ecosystem_world, ecosystem_world.week_number)
        if release_reports and ecosystem_world.news_module is not None:
            ecosystem_world.news_module.add_events(ecosystem_world.week_number, release_reports)
        grammy_reports = _generate_grammy_news(artist, ecosystem_world, ecosystem_world.week_number)
        if grammy_reports and ecosystem_world.news_module is not None:
            ecosystem_world.news_module.add_events(ecosystem_world.week_number, grammy_reports)
        current_week_index = _player_week_index(artist)
        _simulate_romance_week(artist, ecosystem_world, current_week_index)
        romance_reports = _generate_romance_news_reports(ecosystem_world, current_week_index)
        if romance_reports and ecosystem_world.news_module is not None:
            ecosystem_world.news_module.add_events(current_week_index, romance_reports)
        sales_reports = _generate_sales_news_reports(artist, ecosystem_world, current_week_index)
        if sales_reports and ecosystem_world.news_module is not None:
            ecosystem_world.news_module.add_events(current_week_index, sales_reports)
    _decay_relationships(artist, _player_week_index(artist))

    controversy_events = _simulate_controversies(artist, ecosystem_world, _player_week_index(artist))
    public_controversy_events = [
        event for event in controversy_events
        if _should_publish_news_event(event, artist, ecosystem_world)
    ]
    if public_controversy_events:
        print("\nIndustry news this week:")
        for event in public_controversy_events[:5]:
            channel, reporter = _event_channel_and_reporter(event, ecosystem_world)
            print(f"- [{channel} | {reporter}] {event.headline}")
    if ecosystem_world is not None:
        industry_reports = [
            report for report in ecosystem_world.news_module.get_news(_player_week_index(artist))
            if isinstance(report, NewsReport)
        ] if ecosystem_world.news_module is not None else []
        if industry_reports:
            if not public_controversy_events:
                print("\nIndustry news this week:")
            for report in industry_reports[:5]:
                channel, reporter = _event_channel_and_reporter(report, ecosystem_world)
                print(f"- [{channel} | {reporter}] {report.headline}")
    weekly_tweets = _generate_weekly_tweets(_player_week_index(artist), ecosystem_world, artist)
    if weekly_tweets:
        print(f"Twitter this week: {len(weekly_tweets)} posts across artists, fans, and critics.")
    artist.releases_this_week = []

    # Record Label Weekly Subsystem Step
    contract = getattr(artist, "label_contract", None)
    if contract and getattr(contract, "status", "") in ("active", "shelved", "recouped"):
        lbl = get_label_by_id(contract.label_id)
        if lbl:
            contract.weeks_elapsed += 1
            roster_artists = get_label_roster_artists(lbl, artist, ecosystem_world)

            # Roster Priority
            eff_ad, eff_gig, eff_pop = evaluate_roster_priority(artist, contract, lbl, roster_artists)
            artist.popularity_state.organic = clamp_popularity(artist.popularity_state.organic + eff_pop)
            if contract.is_priority_artist and eff_pop > 0:
                print(f"Label priority boost: +{eff_pop:.1f} weekly popularity from {lbl.name}")

            # Shelving Risk
            is_shelved, shelve_msg = evaluate_shelving_risk(artist, contract, lbl, roster_artists)
            if is_shelved and contract.status != "shelved":
                contract.status = "shelved"
                print(f"\n[LABEL NOTICE] {shelve_msg}")
            elif not is_shelved and contract.status == "shelved":
                contract.status = "active"
                print(f"\n[LABEL NOTICE] {lbl.name} has resumed active promotion and lifted your release hold.")

            # Drop Risk
            dropped, drop_msg = evaluate_drop_risk(artist, contract, lbl)
            if dropped:
                print(f"\n[LABEL TERMINATION] {drop_msg}")

            # Breach / Expiry
            curr_wk = _player_week_index(artist)
            breached, damage, breach_msg = evaluate_contract_breach(artist, contract, lbl, curr_wk)
            if breached:
                print(f"\n[LABEL BREACH] {breach_msg}")
                artist.money -= damage
            elif contract.status == "expired":
                print(f"\n[LABEL CONTRACT FULFILLED] {breach_msg}")
    elif not contract or getattr(contract, "status", "") in ("expired", "dropped", "breach"):
        # Unsigned player: chance of inbound approaches from eligible labels
        for lbl in LABELS:
            if can_label_approach_player(lbl, artist):
                if random.random() < 0.15:
                    if not hasattr(artist, "pending_label_offers"):
                        artist.pending_label_offers = []
                    if not any(o.id == lbl.id for o in artist.pending_label_offers):
                        artist.pending_label_offers.append(lbl)
                        print(f"\n[LABEL SCOUT] {lbl.name} ({lbl.tier.upper()}) is interested in signing you! Check Record Labels menu.")
                    break

    current_week = _player_week_index(artist)
    notifications = []
    # Tick feature requests, deliver verses, enforce deadlines.
    for req in artist.feature_requests:
        if req.status in {"completed", "rejected", "expired"}:
            continue
        if req.direction == "outbound" and req.status == "awaiting_verse":
            req.weeks_until_artist_delivers = max(0, int(req.weeks_until_artist_delivers) - 1)
            if req.weeks_until_artist_delivers == 0:
                seed = _ecosystem_seed_by_name(req.artist_name)
                genre = "hip hop"
                # Try to infer genre from the player's song if it exists.
                for entry in artist.singles:
                    if entry.song.name == req.song_name:
                        if entry.song.genres:
                            genre = entry.song.genres[0]
                        break
                req.artist_verse_quality = _ecosystem_contribution_quality(seed, genre, getattr(req, "request_kind", "feature"))
                req.status = "verse_sent"
                notifications.append(
                    f"{req.artist_name} sent their {req.request_kind} for '{req.song_name}' ({req.artist_verse_quality}/10)."
                )

        if current_week > req.week_deadline:
            if req.direction == "inbound" and req.player_verse_quality is None:
                req.status = "expired"
                seed = _ecosystem_seed_by_name(req.artist_name)
                aggression = int(getattr(seed, "aggression", 50)) if seed else 50
                drop = random.uniform(8.0, 15.0) * (0.75 + (aggression / 200.0))
                _apply_relationship_delta(artist, req.artist_name, -drop)
                artist.reputation = clamp_meter(artist.reputation - 3.0)
                notifications.append(
                    f"You missed the deadline on {req.artist_name}'s feature. They've moved on."
                )
            elif req.direction == "outbound" and req.artist_verse_quality is None:
                req.status = "expired"

        if req.direction == "inbound" and req.status == "verse_sent":
            seed = _ecosystem_seed_by_name(req.artist_name)
            relationship = _relationship_score(artist, req.artist_name)
            threshold = _acceptance_threshold(seed, relationship) if seed else 6.5
            qc = float(getattr(seed, "quality_consistency", 70)) / 100.0 if seed else 0.7
            min_needed = threshold
            if relationship > 60:
                min_needed = 5.0
            if relationship > 90:
                min_needed = 0.0
            ok = req.player_verse_quality >= min_needed
            if ok:
                req.status = "completed"
                _apply_relationship_delta(artist, req.artist_name, random.uniform(3.0, 8.0))
                _apply_feature_popularity_boost(artist, amount=5.0, weeks=3)
                if (
                    ecosystem_world is not None
                    and req.ecosystem_release_id is not None
                    and req.ecosystem_track_index is not None
                ):
                    apply_feature_to_pending_release(
                        ecosystem_world,
                        artist_name=req.artist_name,
                        release_id=req.ecosystem_release_id,
                        track_index=int(req.ecosystem_track_index),
                        feature_artist_name=artist.name,
                        verse_quality=float(req.player_verse_quality),
                        current_week=int(ecosystem_world.week_number),
                    )
                friendliness = int(getattr(seed, "friendliness", 50)) if seed else 50
                tier = _friendliness_tier(friendliness)
                notifications.append(f"{req.artist_name}: {random.choice(FEATURE_ACCEPT_VERSE_LINES[tier])}")
            else:
                friendliness = int(getattr(seed, "friendliness", 50)) if seed else 50
                tier = _friendliness_tier(friendliness)
                notifications.append(f"{req.artist_name}: {random.choice(FEATURE_REJECT_VERSE_LINES[tier])}")
                _apply_relationship_delta(artist, req.artist_name, -random.uniform(3.0, 5.0))
                if req.resend_used:
                    req.status = "rejected"
                else:
                    req.status = "awaiting_verse"
                    req.resend_used = True

    # Generate inbound requests from ecosystem.
    if ecosystem_world is not None:
        for seed in ARTIST_ECOSYSTEM_SEEDS:
            artist_pop = float(getattr(seed, "popularity", 0.0))
            player_pop = float(artist.popularity)
            relationship = _relationship_score(artist, seed.name)
            if abs(player_pop - artist_pop) > 25.0 and relationship <= 90.0:
                continue
            active_inbound = any(
                r.direction == "inbound"
                and r.artist_name == seed.name
                and r.status in {"pending", "accepted", "awaiting_verse", "verse_sent"}
                for r in artist.feature_requests
            )
            if active_inbound:
                continue
            chance = (float(getattr(seed, "release_tendency", 50)) / 100.0) * 0.15
            if random.random() >= chance:
                continue
            pending = ecosystem_world.pending_major_by_artist.get(seed.name)
            if not pending or not pending.tracks:
                continue
            # Only request features for a specific track on an upcoming project, not the project itself.
            track_index = random.randrange(0, len(pending.tracks))
            track = pending.tracks[track_index]
            # Ensure the project isn't dropping immediately after requesting a feature.
            pending.week_release = max(int(pending.week_release), int(ecosystem_world.week_number) + 2)

            # Don't spam the same song request over and over (especially close together).
            title = str(getattr(track, "title", "Untitled"))
            same_track = [
                r
                for r in artist.feature_requests
                if r.artist_name == seed.name
                and r.ecosystem_release_id == str(getattr(pending, "release_id", ""))
                and r.ecosystem_track_index == int(track_index)
                and r.status in {"pending", "accepted", "awaiting_verse", "verse_sent"}
            ]
            if same_track:
                continue
            same_song = [
                r
                for r in artist.feature_requests
                if r.artist_name == seed.name and r.song_name == title
            ]
            if any(r.status == "completed" for r in same_song):
                continue
            if same_song:
                last_week = max(int(getattr(r, "week_created", 0)) for r in same_song)
                if (current_week - last_week) < 12:
                    continue
            offer = _feature_offer_money(artist)
            req = FeatureRequest(
                request_id=_new_request_id(current_week),
                direction="inbound",
                artist_name=seed.name,
                song_name=title,
                song_quality=float(getattr(track, "quality", 6.0)),
                status="pending",
                week_created=current_week,
                week_deadline=current_week + FEATURE_DEADLINE_WEEKS,
                weeks_until_artist_delivers=0,
                paid=offer,
                ecosystem_release_id=str(getattr(pending, "release_id", "")),
                ecosystem_track_index=int(track_index),
                forced_release_week=None,
            )
            # This track/project will not release until after the request deadline, but it must
            # release within 8 weeks after the deadline ends (testing rule).
            req.forced_release_week = req.week_deadline + random.randint(1, 8)
            pending.week_release = int(req.forced_release_week)
            artist.feature_requests.append(req)
            notifications.append(
                f"{seed.name} wants you on their track '{req.song_name}' - quality {req.song_quality}/10. Offer {money_fmt(offer)}. Check feature requests."
            )

    if notifications:
        print("\nFEATURES")
        for line in notifications:
            print(f"- {line}")


def view_ecosystem_artists():
    raise RuntimeError("Use view_ecosystem_artists_menu(world) instead.")


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


def _relationship_tier(friendliness):
    if friendliness >= 70:
        return "friendly"
    if friendliness >= 45:
        return "neutral"
    return "rude"


def _friendship_label(score):
    score = clamp_meter(score)
    if score <= 10:
        return "they strongly hate you"
    if score <= 20:
        return "he doesn't know you or either hates you"
    if score <= 30:
        return "barely knows you or wants to forget you"
    if score <= 40:
        return "more like a colleague honestly"
    if score <= 55:
        return "he digs you"
    if score <= 65:
        return "you are friends"
    if score <= 75:
        return "you are good friends"
    if score <= 85:
        return "your are good good friends"
    if score <= 92:
        return "get a room you two"
    return "ride or die kinda shit"


def _should_respond(friendliness, relationship, kind):
    base = 0.35 + (friendliness / 200.0) + (relationship / 220.0)
    if kind in {"money", "date"}:
        base -= 0.10
    if kind == "criticize":
        base -= 0.05
    return random.random() < max(0.10, min(0.95, base))


def _praise_delta(friendliness):
    delta = 0.5 + (friendliness / 100.0) * 4.5 + random.uniform(-0.5, 0.7)
    delta = max(0.5, min(5.0, delta))
    # Make relationship building faster: positive interactions are much more impactful.
    return min(15.0, delta * 3.0)


def _crit_delta(friendliness):
    scale = 0.85 + ((55.0 - friendliness) / 120.0)
    delta = -random.uniform(2.0, 6.0) * max(0.55, min(1.25, scale))
    return max(-7.5, min(-1.2, delta))


def _decay_relationships(artist, week_index):
    if TEST_RELATIONSHIP_LOCK and getattr(artist, "_relationship_lock", False):
        for seed in ARTIST_ECOSYSTEM_SEEDS:
            state = artist.relationships.get(seed.name)
            if state:
                state.score = 100.0
        return
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        state = artist.relationships.get(seed.name)
        if not state:
            continue
        gap = week_index - state.last_contact_week
        if gap <= 3:
            continue
        friendliness = int(getattr(seed, "friendliness", 50))
        decay = random.uniform(0.8, 1.6)
        if friendliness < 45:
            decay *= 1.15
        else:
            decay *= 0.95
        state.score = clamp_meter(state.score - decay)


def _relationship_bar(value):
    return meter_bar("Relationship", value, width=22)


def create_beats_action(artist):
    if action_locked_by_health(artist, "creating beats"):
        return
    apply_action_cost(artist, fatigue_cost=6.0, health_risk=0.12)
    beat_genre = choose_beat_genre()
    quality = roll_beat_quality(artist, roll_song_quality)
    print("\nBeat rolled.")
    print(f"Genre: {beat_genre}")
    print(f"Quality: {quality}/10 (from production + mix/master skills)")
    choice = choose_from_list(
        "What do you want to do with this beat?",
        ["Store in Beat Vault", "Discard"],
        allow_cancel=False,
    )
    if choice == 1:
        print("Beat discarded.")
        return
    name = prompt_text("Beat name: ", f"{beat_genre.title()} Beat {len(ensure_beat_market(artist).vault) + 1}")
    beat = create_player_beat(artist, name, quality, beat_genre, _player_week_index(artist))
    add_beat_to_vault(artist, beat)
    fair = suggested_list_price(beat.quality, artist.popularity, beat.genre)
    print(f"Stored '{beat.name}' in your Beat Vault ({beat.genre}, {beat.quality}/10).")
    print(f"Suggested Beat Store list price at your current popularity: {money_fmt(fair)}")


def beat_vault_menu(artist):
    market = ensure_beat_market(artist)
    while True:
        beats = vault_beats(market, include_consumed=True)
        if not beats:
            print("\nBeat Vault is empty.")
            input("Press Enter...")
            return
        options = []
        for beat in beats:
            status = "USED" if beat.consumed else ("LISTED" if beat.listed else "READY")
            src = "yours" if beat.is_player_made else f"prod. {beat.producer_name}"
            genre = getattr(beat, "genre", "hip hop")
            options.append(f"{beat.name} | {genre} | {beat.quality}/10 | {status} | {src}")
        choice = choose_from_list("Beat Vault", options + ["Back"], allow_cancel=False)
        if choice is None or choice == len(options):
            return
        beat = beats[choice]
        if beat.consumed:
            print(f"'{beat.name}' was already used on a song.")
            input("Press Enter...")
            continue
        action = choose_from_list(
            f"'{beat.name}'",
            ["Rename", "Remove from vault", "Back"],
            allow_cancel=False,
        )
        if action == 0:
            beat.name = prompt_text("New name: ", beat.name)
        elif action == 1:
            if beat.listed:
                print("This beat is currently listed on the Beat Store. Unlist it before removing it from the vault.")
                input("Press Enter...")
                continue
            if beat_is_in_any_pack(market, beat.beat_id):
                print("This beat belongs to a beat pack. Remove the pack listing before removing the beat from the vault.")
                input("Press Enter...")
                continue
            if beat_has_pending_negotiation(market, beat.beat_id):
                print("This beat has a pending negotiation attached to it. Resolve that first.")
                input("Press Enter...")
                continue
            market.vault.remove(beat)
            print("Beat removed.")


def _beat_store_list_beat(artist, market):
    listable = player_listable_beats(market, artist.name)
    if not listable:
        print("No self-made vault beats available to list (pack beats must be sold as packs).")
        return
    labels = [f"{b.name} | {b.genre} | {b.quality}/10" for b in listable]
    idx = choose_from_list("List beat for sale", labels, allow_cancel=True)
    if idx is None:
        return
    beat = listable[idx]
    fair = suggested_list_price(beat.quality, artist.popularity, beat.genre)
    est_fair = estimated_weekly_sale_probability(beat.quality, fair, artist.popularity, beat.genre) * 100
    print(f"Suggested fair price: {money_fmt(fair)} (~{est_fair:.0f}% weekly sale chance at your popularity).")
    price = float(prompt_int("List price ($): ", max(100, int(fair * 0.5))))
    beat.list_price = price
    beat.listed = True
    beat.discount_pct = 0.0
    est = estimated_weekly_sale_probability(beat.quality, price, artist.popularity, beat.genre) * 100
    print(f"Listed '{beat.name}' ({beat.genre}) at {money_fmt(price)} (~{est:.0f}% weekly sale chance).")


def _beat_store_discount(artist, market):
    listed = solo_listed_beats(market, artist.name)
    packs = [p for p in market.packs if p.listed]
    if not listed and not packs:
        print("Nothing listed on the Beat Store right now.")
        return
    options = [f"[Beat] {b.name} — {b.discount_pct * 100:.0f}% off" for b in listed]
    options += [f"[Pack] {p.name} — {p.discount_pct * 100:.0f}% off" for p in packs]
    idx = choose_from_list("Apply discount", options, allow_cancel=True)
    if idx is None:
        return
    pct = prompt_int("Discount percent (0-90): ", 0, 90) / 100.0
    if idx < len(listed):
        listed[idx].discount_pct = pct
        print(f"Discount set to {pct * 100:.0f}% on '{listed[idx].name}'.")
    else:
        packs[idx - len(listed)].discount_pct = pct
        print(f"Discount set on pack.")


def _beat_store_create_pack(artist, market):
    listable = player_listable_beats(market, artist.name)
    if len(listable) < 3:
        print("Need at least 3 self-made vault beats not already in a pack.")
        return
    size = PACK_SIZE_OPTIONS[choose_from_list("Pack size", ["3 beats", "4 beats"], allow_cancel=False)]
    labels = [f"{b.name} | {b.genre} | {b.quality}/10" for b in listable]
    chosen_ids = []
    while len(chosen_ids) < size:
        remaining = [b for b in listable if b.beat_id not in chosen_ids]
        if not remaining:
            break
        rem_labels = [f"{b.name} | {b.genre} | {b.quality}/10" for b in remaining]
        pick = choose_from_list(f"Pick beat {len(chosen_ids) + 1}/{size}", rem_labels, allow_cancel=True)
        if pick is None:
            return
        chosen_ids.append(remaining[pick].beat_id)
    beats = [beat_by_id(market, bid) for bid in chosen_ids]
    suggested = suggested_pack_price([b for b in beats if b], artist.popularity, discount=PACK_DISCOUNT_DEFAULT)
    pack_name = prompt_text("Pack name: ", "Vault Pack")
    price = float(prompt_int(f"Pack price ($) [suggested ~{int(suggested)}]: ", 100))
    pack = BeatPack(
        pack_id=str(uuid4()),
        name=pack_name,
        beat_ids=tuple(chosen_ids),
        list_price=price,
        discount_pct=0.0,
        listed=True,
    )
    market.packs.append(pack)
    # Beats stay in the pack listing only — do not mark solo list_price (avoids None price bugs).
    for bid in chosen_ids:
        b = beat_by_id(market, bid)
        if b:
            b.listed = False
            b.list_price = None
            b.discount_pct = 0.0
    print(f"Listed pack '{pack.name}' with {size} beats at {money_fmt(price)}.")


def _beat_store_analytics(market):
    stats = sales_analytics_summary(market)
    print("\n--- Beat Store Analytics ---")
    print(f"Total sales: {stats['total_sales']}")
    print(f"Total revenue: {money_fmt(stats['total_revenue'])}")
    if stats["total_sales"]:
        print(f"Average sale: {money_fmt(stats['avg_price'])}")
    if stats["top_buyers"]:
        print("\nTop buyers:")
        for name, count in stats["top_buyers"]:
            print(f"  {name}: {count} purchase(s)")
    if stats["recent"]:
        print("\nRecent sales:")
        for sale in stats["recent"]:
            print(f"  W{sale.week}: {sale.buyer} — {sale.item_name} — {money_fmt(sale.price)}")


def _beat_store_negotiations(artist, market):
    pending = [n for n in market.pending_negotiations if n.status == "pending"]
    if not pending:
        print("No pending beat negotiations.")
        return
    for neg in pending:
        item = neg.beat_id or neg.pack_id or neg.listing_id or "item"
        print(
            f"\n[{neg.direction}] {neg.buyer_name} ↔ {neg.seller_name} | {item} | "
            f"listed {money_fmt(neg.listed_price)} | offer {money_fmt(neg.offer_price)}"
        )
        if neg.direction == "inbound":
            action = choose_from_list(
                "Negotiation",
                [
                    "Accept offer",
                    "Reject — don't sell",
                    "Skip for now",
                ],
                allow_cancel=False,
            )
            if action == 0:
                if accept_negotiation(artist, neg):
                    print(f"Sold. You received {money_fmt(neg.offer_price)}.")
                else:
                    print("Could not complete sale.")
            elif action == 1:
                neg.status = "rejected"
                print("Negotiation rejected.")
        else:
            action = choose_from_list(
                "Your purchase negotiation",
                ["Accept counter-offer", "Walk away"],
                allow_cancel=False,
            )
            if action == 0:
                if accept_negotiation(artist, neg):
                    print("Purchase completed. Beat added to vault.")
                else:
                    print("Could not complete purchase (check funds).")
            else:
                neg.status = "rejected"


def _beat_store_buy_producer_beats(artist, market):
    grouped = catalog_sellers_grouped(market)
    if not grouped:
        print("No beats for sale in the ecosystem catalog this week.")
        return

    while True:
        seller_names = sorted(
            grouped.keys(),
            key=lambda name: (
                -len(grouped[name]),
                -max(float(item.price) for item in grouped[name]),
            ),
        )
        seller_labels = [format_seller_menu_line(name, grouped[name]) for name in seller_names]
        seller_pick = choose_from_list(
            "Beat Store — choose a seller",
            seller_labels + ["Back to Beat Store menu"],
            allow_cancel=False,
        )
        if seller_pick is None or seller_pick == len(seller_labels):
            return

        seller = seller_names[seller_pick]
        listings = sorted(grouped[seller], key=lambda item: (item.price, -item.quality))
        beat_labels = [format_listing_menu_line(item) for item in listings]
        beat_pick = choose_from_list(
            f"Beats by {seller}",
            beat_labels + ["Back to seller list"],
            allow_cancel=False,
        )
        if beat_pick is None or beat_pick == len(beat_labels):
            continue

        listing = listings[beat_pick]
        action = choose_from_list(
            f"{listing.beat_name} — {listing.genre} — {listing.quality}/10",
            [
                f"Buy now ({money_fmt(listing.price)})",
                "Negotiate lower price",
                "Back",
            ],
            allow_cancel=False,
        )
        if action == 2:
            continue
        if action == 0:
            if artist.money < listing.price:
                print(f"Not enough money. You have {money_fmt(artist.money)}.")
                continue
            beat = purchase_ecosystem_listing(artist, listing, _player_week_index(artist))
            if beat:
                print(
                    f"Purchased '{beat.name}' ({beat.genre}, {beat.quality}/10) — "
                    f"prod. {beat.producer_name} — added to Beat Vault."
                )
                grouped = catalog_sellers_grouped(market)
                if seller not in grouped:
                    return
            continue

        offer = float(prompt_int("Your offer ($): ", 100))
        if offer >= float(listing.price):
            if artist.money < listing.price:
                print(f"Not enough money. You have {money_fmt(artist.money)}.")
                continue
            beat = purchase_ecosystem_listing(artist, listing, _player_week_index(artist))
            if beat:
                print(f"Purchased at list price. '{beat.name}' is in your vault.")
            grouped = catalog_sellers_grouped(market)
            if seller not in grouped:
                return
            continue
        if producer_will_accept_offer(float(listing.price), offer, listing.producer_name):
            listing.price = offer
            beat = purchase_ecosystem_listing(artist, listing, _player_week_index(artist))
            if beat:
                print(
                    f"{listing.producer_name} accepted {money_fmt(offer)}. "
                    f"'{beat.name}' (prod. {beat.producer_name}) is in your vault."
                )
            grouped = catalog_sellers_grouped(market)
            if seller not in grouped:
                return
        else:
            negotiation = create_outbound_negotiation(
                market,
                artist.name,
                listing,
                offer,
                _player_week_index(artist),
            )
            if negotiation is None:
                print("You already have a pending offer on this beat.")
            else:
                min_serious = max(99.0, float(listing.price) * 0.45)
                print(
                    f"Offer sent to {listing.producer_name} at {money_fmt(offer)} "
                    f"(list {money_fmt(listing.price)}). "
                    f"They should respond within a week or two. Serious offers usually start around {money_fmt(min_serious)}."
                )


def _beat_store_pricing_help(artist):
    print("\n" + "\n".join(format_pricing_help(artist)))
    input("\nPress Enter...")


def beat_store_menu(artist, ecosystem_world=None):
    market = ensure_beat_market(artist)
    _ = ecosystem_world
    while True:
        choice = choose_from_list(
            "Beat Store",
            [
                "List a vault beat for sale (self-made only)",
                "Create & list beat pack (3-4 beats)",
                "Apply discount to listed beat/pack",
                "Buy beats (pick seller, then beat)",
                "Pending negotiations",
                "Sales analytics",
                "Pricing help (recommended list prices)",
                "View listed inventory",
                "Back",
            ],
            allow_cancel=False,
        )
        if choice == 8:
            return
        if choice == 0:
            _beat_store_list_beat(artist, market)
        elif choice == 1:
            _beat_store_create_pack(artist, market)
        elif choice == 2:
            _beat_store_discount(artist, market)
        elif choice == 3:
            _beat_store_buy_producer_beats(artist, market)
        elif choice == 4:
            _beat_store_negotiations(artist, market)
        elif choice == 5:
            _beat_store_analytics(market)
        elif choice == 6:
            _beat_store_pricing_help(artist)
        elif choice == 7:
            listed_beats = solo_listed_beats(market, artist.name)
            listed_packs = [p for p in market.packs if p.listed]
            if not listed_beats and not listed_packs:
                print("Nothing listed.")
            for b in listed_beats:
                eff = b.effective_price()
                if eff is None:
                    print(f"  Beat: {b.name} | {b.genre} | {b.quality}/10 | (no list price set)")
                    continue
                est = estimated_weekly_sale_probability(
                    b.quality, eff, artist.popularity, b.genre
                ) * 100
                print(
                    f"  Beat: {b.name} | {b.genre} | {b.quality}/10 | {money_fmt(eff)} "
                    f"({b.discount_pct*100:.0f}% off) ~{est:.0f}%/wk"
                )
            for p in listed_packs:
                pack_beats = [beat_by_id(market, bid) for bid in p.beat_ids]
                pack_beats = [b for b in pack_beats if b]
                avg_q = sum(b.quality for b in pack_beats) / max(1, len(pack_beats))
                pack_genre = pack_beats[0].genre if pack_beats else "hip hop"
                eff = p.effective_price()
                est = estimated_pack_weekly_sale_probability(
                    pack_beats, eff, artist.popularity
                ) * 100
                beat_names = ", ".join(b.name for b in pack_beats[:4])
                print(
                    f"  Pack: {p.name} | {len(p.beat_ids)} beats ({beat_names}) | "
                    f"{money_fmt(eff)} ({p.discount_pct*100:.0f}% off) ~{est:.0f}%/wk"
                )


def diss_tracks_menu(world: EcosystemWorld | None):
    if world is None:
        print("\nNo diss tracks recorded.")
        return
    ensure_diss_state(world)
    if not world.diss_tracks:
        print("\nNo diss tracks recorded.")
        return
    while True:
        options = [
            f'{track.instigator} - "{track.title}" | vs {track.target} | reception {track.reception_score}/10 | {track.total_streams:,} streams'
            for track in reversed(world.diss_tracks)
        ]
        choice = choose_from_list("Diss tracks", options + ["Back"], allow_cancel=False)
        if choice is None or choice == len(options):
            return
        display_diss_track(list(reversed(world.diss_tracks))[choice])
        input("Press Enter to go back...")


def show_actions():
    print("\nActions")
    print("1. Ghostwrite (+1 lyrics)")
    print("2. Open mic (+1 vocals)")
    print("3. Produce (+1 production)")
    print("4. Mix/master (+1 mix/master)")
    print("5. Start genre course (12 weeks -> +10 genre)")
    print("6. Create album draft")
    print("7. Create song")
    print("8. Create deluxe draft")
    print("9. Release music")
    print("10. Go live")
    print("11. Work side hustle")
    print("12. Media management")
    print("13. Shawtify streams")
    print("14. New releases")
    print("15. View artists")
    print("16. Release Calendar")
    print("17. NEWS")
    print("18. TWITTER")
    print("19. User Ratings (IMDb)")
    print("20. Manage relationships")
    print("21. Catalog manager")
    print("22. View feature requests")
    print("23. Simulate next week")
    print("24. Simulate 52 weeks (testing)")
    print("25. HOT 100")
    print("26. Grammys")
    print("27. Diss tracks")
    print("28. Love relationships")
    print("29. Separated relationships")
    print("30. Create beats")
    print("31. Beat Vault")
    print("32. Beat Store")
    print("33. Manage physical copies")
    print("34. View Sales")
    print("35. NUMBLE")
    print("36. Your Love Relationships")
    print("37. Concerts")
    print("38. Manage Venue")
    print("39. Record Labels")
    print("40. Quit")


def simulate_many_weeks(artist, ecosystem_world: EcosystemWorld | None, weeks: int = 52):
    for i in range(int(weeks)):
        simulate_week(artist, ecosystem_world)
        # Avoid a totally endless wall of output when testing.
        if (i + 1) % 13 == 0 and (i + 1) != weeks:
            input("\n(Testing) 13 weeks simulated. Press Enter to keep going...")


def main():
    artist = create_artist()
    track_sim = Simulation()
    album_sim = AlbumSimulation()
    ecosystem_world = create_world()
    ecosystem_world.news_module = NewsModule()
    ecosystem_world.twitter_module = TwitterModule()
    step_world(ecosystem_world)

    while True:
        display_artist(artist)
        show_actions()
        choice = prompt_text("Choose action: ", "").lower()

        if choice == "1":
            practice_skill(artist, "lyrics")
        elif choice == "2":
            practice_skill(artist, "vocals")
        elif choice == "3":
            practice_skill(artist, "production")
        elif choice == "4":
            practice_skill(artist, "mix/master")
        elif choice == "5":
            start_genre_course(artist)
        elif choice == "6":
            create_album_draft(artist)
        elif choice == "7":
            create_song_for_artist(artist)
        elif choice == "8":
            create_deluxe_draft(artist)
        elif choice == "9":
            release_menu(artist, track_sim, album_sim)
        elif choice == "10":
            go_live_action(artist)
        elif choice == "11":
            work_side_hustle(artist)
        elif choice == "12":
            management_menu(artist)
        elif choice == "13":
            show_shawtify_streams(artist)
        elif choice == "14":
            view_ecosystem_new_releases(ecosystem_world)
        elif choice == "15":
            view_ecosystem_artists_menu(ecosystem_world)
        elif choice == "16":
            release_calendar_menu(ecosystem_world)
        elif choice == "17":
            news_menu(artist, ecosystem_world)
        elif choice == "18":
            twitter_menu(ecosystem_world)
        elif choice == "19":
            user_ratings_menu(artist, ecosystem_world)
        elif choice == "20":
            manage_relationships_menu(artist, ecosystem_world)
        elif choice == "21":
            catalog_menu(artist)
        elif choice == "22":
            view_feature_requests_menu(artist)
        elif choice == "23":
            simulate_week(artist, ecosystem_world)
        elif choice == "24":
            simulate_many_weeks(artist, ecosystem_world, weeks=52)
        elif choice == "25":
            show_hot_100(artist, ecosystem_world)
        elif choice == "26":
            grammy_awards_menu(artist, ecosystem_world)
        elif choice == "27":
            diss_tracks_menu(ecosystem_world)
        elif choice == "28":
            view_love_relationships_menu(ecosystem_world)
        elif choice == "29":
            view_separated_relationships_menu(ecosystem_world)
        elif choice == "30":
            create_beats_action(artist)
        elif choice == "31":
            beat_vault_menu(artist)
        elif choice == "32":
            beat_store_menu(artist, ecosystem_world)
        elif choice == "33":
            manage_physical_copies_menu(artist)
        elif choice == "34":
            view_player_sales_menu(artist)
        elif choice == "35":
            numble_menu(artist, ecosystem_world)
        elif choice == "36":
            player_love_relationships_menu(artist, ecosystem_world)
        elif choice == "37":
            concerts_menu(artist, ecosystem_world)
        elif choice == "38":
            from rapsim_reviews.venue_management import venue_management_menu
            venue_management_menu(artist, ecosystem_world)
        elif choice == "39":
            label_management_menu(artist, ecosystem_world)
        elif choice == "40":
            print("See you on the charts.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
