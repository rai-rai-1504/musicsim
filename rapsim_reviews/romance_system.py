"""rapsim_reviews.romance_system
Dating app (Numble), hookups, public romance, marriages, divorces,
and player relationship progression.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING
from uuid import uuid4

from rapsim_reviews.date_system import format_week_range
from rapsim_reviews.ui_helpers import (
    choose_from_list,
    choose_item_from_list,
    meter_bar,
    money_fmt,
    prompt_int,
    prompt_text,
    clamp_meter,
    clamp_popularity,
    clamp_fatigue,
)
from rapsim_reviews.artist_ecosystem_seed import (
    ARTIST_ECOSYSTEM_SEEDS,
    ARTIST_LOVINGNESS,
    ARTIST_ROMANCE_PREFERENCES,
)

from rapsim_reviews.hidden_character_seeds import (
    HIDDEN_CHARACTER_BY_NAME,
    HIDDEN_CHARACTER_ROMANCE_PREFERENCES,
    HIDDEN_CHARACTER_SEEDS,
)

from rapsim_reviews.career_models import (
    Artist,
    RelationshipState,
    RomanceProfile,
    RomanceEvent,
    PlayerLoveRelationship,
    VALID_GENDERS,
    VALID_SEXUALITIES,
    SEXUALITY_OPTIONS_BY_GENDER,
    ROMANCE_ACTIVE_STATUSES,
    ROMANCE_PUBLIC_VISIBILITY,
    ROMANCE_STATUS_LABELS,
    TEST_RELATIONSHIP_LOCK,
    _player_week_index,
    _year_week_from_world_week,
    _apply_relationship_delta,
    _relationship_score,
    _ecosystem_seed_by_name,
    _ecosystem_artist_popularity,
    _ecosystem_artist_reputation,
    _find_world_runtime,
    _find_artist_any,
    _artist_display_name,
)
from rapsim_reviews.news_system import (
    NewsReport,
    _build_news_report,
    _apply_popularity_delta_to_actor,
    _apply_reputation_delta_to_actor,
    _recent_controversy_load,
    _ensure_news_state,
)

def _is_grammy_media_week(current_week: int) -> bool:
    return 49 <= (((int(current_week) - 1) % 52) + 1) <= 52

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld

def _validate_gender(gender: str) -> str:
    value = str(gender).strip().lower()
    if value not in VALID_GENDERS:
        raise ValueError(f"Invalid gender: {gender}")
    return value


def _validate_sexuality_for_gender(gender: str, sexuality: str) -> str:
    normalized_gender = _validate_gender(gender)
    value = str(sexuality).strip().lower()
    if value not in VALID_SEXUALITIES:
        raise ValueError(f"Invalid sexuality: {sexuality}")
    if value not in SEXUALITY_OPTIONS_BY_GENDER[normalized_gender]:
        raise ValueError(f"Invalid sexuality {sexuality} for gender {gender}")
    return value


def _prompt_gender() -> str:
    return VALID_GENDERS[choose_from_list("Choose gender", list(VALID_GENDERS), allow_cancel=False)]


def _prompt_sexuality(gender: str) -> str:
    options = list(SEXUALITY_OPTIONS_BY_GENDER[_validate_gender(gender)])
    return options[choose_from_list("Choose sexuality", options, allow_cancel=False)]


def _romance_preference_from_identity(gender: str, sexuality: str) -> str:
    normalized_gender = _validate_gender(gender)
    normalized_sexuality = _validate_sexuality_for_gender(normalized_gender, sexuality)
    if normalized_sexuality == "bisexual":
        return "prefers_both"
    if normalized_gender == "male":
        return "prefers_male" if normalized_sexuality == "gay" else "prefers_female"
    elif normalized_gender == "female":
        return "prefers_female" if normalized_sexuality == "lesbian" else "prefers_male"
    else: # non-binary
        if normalized_sexuality == "gay":
            return "prefers_male"
        elif normalized_sexuality == "lesbian":
            return "prefers_female"
        else:
            return "prefers_both"


def _ensure_romance_state(world: EcosystemWorld | None):
    if world is None:
        return
    if getattr(world, "romance_profiles", None) is None:
        world.romance_profiles = {}
    if getattr(world, "romance_event_history", None) is None:
        world.romance_event_history = {}
    if getattr(world, "romance_hidden_partner_claims", None) is None:
        world.romance_hidden_partner_claims = {}
    if getattr(world, "romance_last_processed_week", None) is None:
        world.romance_last_processed_week = 0
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        if seed.name not in world.romance_profiles:
            baseline = 46.0 + (int(seed.friendliness) * 0.22) + (int(ARTIST_LOVINGNESS.get(seed.name, 50)) * 0.12)
            world.romance_profiles[seed.name] = RomanceProfile(
                owner_name=seed.name,
                stability_score=clamp_meter(baseline),
            )


def _get_romance_profile(world: EcosystemWorld | None, artist_name: str) -> RomanceProfile | None:
    if world is None:
        return None
    _ensure_romance_state(world)
    return world.romance_profiles.get(artist_name)


def _player_current_love(player_artist: Artist) -> PlayerLoveRelationship | None:
    for rel in reversed(getattr(player_artist, "love_relationships", [])):
        if rel.status == "current":
            return rel
    return None


def _player_love_rows(player_artist: Artist, statuses: set[str] | None = None) -> list[PlayerLoveRelationship]:
    rows = list(getattr(player_artist, "love_relationships", []))
    if statuses is not None:
        rows = [rel for rel in rows if rel.status in statuses]
    return rows


def _player_romance_pref_matches(player_artist: Artist, partner_gender: str, partner_pref: str) -> bool:
    return _romance_pref_matches_target(player_artist.romance_preference, partner_gender) and _romance_pref_matches_target(partner_pref, player_artist.gender)


def _player_romance_compatible(player_artist: Artist, partner_name: str, partner_is_artist: bool) -> bool:
    meta = _partner_meta(partner_name, partner_is_artist)
    return bool(meta["available"]) and _player_romance_pref_matches(player_artist, str(meta["gender"]), str(meta["preference"]))


def _player_relationship_score(
    player_artist: Artist,
    partner_name: str,
    partner_is_artist: bool,
    world: EcosystemWorld | None = None,
) -> float:
    meta = _partner_meta(partner_name, partner_is_artist, world)
    friendship = _relationship_score(player_artist, partner_name) if partner_is_artist else 42.0
    pop_gap = abs(float(player_artist.popularity) - float(meta["popularity"]))
    rep_gap = abs(float(player_artist.reputation) - float(meta["reputation"]))
    score = 18.0
    score += friendship * 0.30
    score += float(meta["lovingness"]) * 0.24
    score += float(meta["friendliness"]) * 0.14
    score += max(0.0, 35.0 - pop_gap) * 0.50
    score += max(0.0, 30.0 - rep_gap) * 0.35
    score += max(0.0, float(player_artist.reputation) - 45.0) * 0.08
    if not _player_romance_compatible(player_artist, partner_name, partner_is_artist):
        score -= 45.0
    return clamp_meter(score)


def _publish_player_romance_event(
    player_artist: Artist,
    world: EcosystemWorld | None,
    event_type: str,
    partner_name: str,
    partner_is_artist: bool,
    confirmed: bool = False,
    visibility: str = "known",
    third_party_name: str = "",
):
    if world is None:
        return None
    from rapsim_reviews.twitter_system import _ensure_twitter_state, _generate_romance_tweets
    _ensure_news_state(world)
    _ensure_twitter_state(world)
    _ensure_romance_state(world)
    week = _player_week_index(player_artist)
    event = _record_romance_event(
        world,
        week,
        event_type,
        player_artist.name,
        partner_name,
        partner_is_artist,
        confirmed=confirmed,
        visibility=visibility,
        third_party_name=third_party_name,
        rumor_confidence="confirmed" if confirmed else "warm",
    )
    if world.news_module is not None:
        world.news_module.add_events(week, _generate_romance_news_reports(world, week))
    if world.twitter_module is not None:
        existing = world.twitter_module.get_tweets(week)
        generated = _generate_romance_tweets(week, world)
        seen = {tweet.id for tweet in existing}
        world.twitter_module.add_tweets(week, existing + [tweet for tweet in generated if tweet.id not in seen])
    return event


def _start_player_relationship(
    player_artist: Artist,
    world: EcosystemWorld | None,
    partner_name: str,
    partner_is_artist: bool,
    starting_love: float,
    starting_strength: float,
    visibility: str = "known",
):
    current = _player_current_love(player_artist)
    if current is not None:
        current.status = "ex"
        current.end_week = _player_week_index(player_artist)
        current.notes.append("ended when a new relationship started")
    rel = PlayerLoveRelationship(
        partner_name=partner_name,
        partner_is_artist=partner_is_artist,
        status="current",
        lovingness=clamp_meter(starting_love),
        strength=clamp_meter(starting_strength),
        start_week=_player_week_index(player_artist),
        visibility=visibility,
    )
    player_artist.love_relationships.append(rel)
    _publish_player_romance_event(player_artist, world, "relationship_confirmed", partner_name, partner_is_artist, confirmed=True, visibility=visibility)
    player_artist.reputation = clamp_meter(player_artist.reputation + 0.8)
    player_artist.popularity_state.organic = clamp_popularity(player_artist.popularity_state.organic + 0.5)
    return rel


def _end_player_relationship(player_artist: Artist, world: EcosystemWorld | None, reason: str = "breakup"):
    current = _player_current_love(player_artist)
    if current is None:
        print("You are not currently in a relationship.")
        return None
    current.status = "ex"
    current.end_week = _player_week_index(player_artist)
    current.notes.append(reason)
    _publish_player_romance_event(player_artist, world, "breakup", current.partner_name, current.partner_is_artist, confirmed=True, visibility="known")
    player_artist.reputation = clamp_meter(player_artist.reputation - 0.8)
    print(f"You and {current.partner_name} broke up.")
    return current


def _attempt_player_date(
    player_artist: Artist,
    world: EcosystemWorld | None,
    partner_name: str,
    partner_is_artist: bool,
    from_numble: bool = False,
):
    score = _player_relationship_score(player_artist, partner_name, partner_is_artist, world)
    meta = _partner_meta(partner_name, partner_is_artist, world)
    roll = random.uniform(0, 100)
    print(f"\nDate chance: {score:.1f}%")
    if roll <= score:
        starting_love = 38.0 + score * 0.42 + random.uniform(-4.0, 8.0)
        starting_strength = 34.0 + score * 0.36 + random.uniform(-3.0, 8.0)
        visibility = _romance_visibility(float(player_artist.popularity), float(meta["popularity"]), confirmed=True)
        rel = _start_player_relationship(player_artist, world, partner_name, partner_is_artist, starting_love, starting_strength, visibility)
        print(f"You and {partner_name} are dating now.")
        print(meter_bar("Lovingness", rel.lovingness))
        return True
    if from_numble:
        print(f"{partner_name} enjoyed the chat, but did not want to make it official.")
    else:
        print(f"{partner_name} said no to the date.")
    if partner_is_artist:
        _apply_relationship_delta(player_artist, partner_name, -random.uniform(1.0, 4.0))
    return False


def _player_hookup(
    player_artist: Artist,
    world: EcosystemWorld | None,
    partner_name: str,
    partner_is_artist: bool,
):
    score = _player_relationship_score(player_artist, partner_name, partner_is_artist, world)
    hookup_chance = clamp_meter(score + random.uniform(-12.0, 10.0))
    current = _player_current_love(player_artist)
    print(f"\nHookup chance: {hookup_chance:.1f}%")
    if random.uniform(0, 100) > hookup_chance:
        print(f"{partner_name} did not go for it.")
        return False
    print(f"You hooked up with {partner_name}.")
    if current is None:
        rel = PlayerLoveRelationship(
            partner_name=partner_name,
            partner_is_artist=partner_is_artist,
            status="fling",
            lovingness=clamp_meter(18.0 + hookup_chance * 0.25),
            strength=clamp_meter(14.0 + hookup_chance * 0.18),
            start_week=_player_week_index(player_artist),
            end_week=_player_week_index(player_artist),
            visibility="private",
        )
        player_artist.love_relationships.append(rel)
        return True

    current.cheated = True
    current.lovingness = clamp_meter(current.lovingness - random.uniform(14.0, 28.0))
    current.strength = clamp_meter(current.strength - random.uniform(10.0, 22.0))
    current.notes.append(f"cheated with {partner_name}")
    print(f"Cheating hurt your relationship with {current.partner_name}.")
    print(meter_bar("Lovingness", current.lovingness))
    leak_chance = clamp_meter(18.0 + max(player_artist.popularity, _partner_meta(partner_name, partner_is_artist, world)["popularity"]) * 0.45)
    if random.uniform(0, 100) <= leak_chance:
        current.public_scandal = True
        player_artist.reputation = clamp_meter(player_artist.reputation - 18.0)
        player_artist.popularity_state.organic = clamp_popularity(player_artist.popularity_state.organic + 1.2)
        _publish_player_romance_event(
            player_artist,
            world,
            "cheating_confirmed",
            current.partner_name,
            current.partner_is_artist,
            confirmed=True,
            visibility="tabloid",
            third_party_name=partner_name,
        )
        print("The cheating came out publicly. Reputation took a crazy hit.")
    else:
        _publish_player_romance_event(
            player_artist,
            world,
            "cheating_rumor",
            current.partner_name,
            current.partner_is_artist,
            confirmed=False,
            visibility="known",
            third_party_name=partner_name,
        )
        print("Rumors are floating, but nothing is fully confirmed yet.")
    return True


def _numble_matches(player_artist: Artist) -> list:
    week = _player_week_index(player_artist)
    if player_artist.numble_match_week == week and player_artist.numble_match_names:
        return [HIDDEN_CHARACTER_BY_NAME[name] for name in player_artist.numble_match_names if name in HIDDEN_CHARACTER_BY_NAME]
    compatible = [
        hidden for hidden in HIDDEN_CHARACTER_SEEDS
        if _player_romance_compatible(player_artist, hidden.name, False)
    ]
    near = [
        hidden for hidden in compatible
        if abs(float(player_artist.popularity) - float(getattr(hidden, "popularity", 50.0))) <= 28.0
    ]
    pool = near or compatible or list(HIDDEN_CHARACTER_SEEDS)
    weights = []
    for hidden in pool:
        meta = _partner_meta(hidden.name, False)
        pop_gap = abs(float(player_artist.popularity) - float(meta["popularity"]))
        rep_gap = abs(float(player_artist.reputation) - float(meta["reputation"]))
        weights.append(max(0.3, 4.0 - (pop_gap / 18.0) - (rep_gap / 35.0) + (float(meta["lovingness"]) / 80.0)))
    count = min(len(pool), random.randint(5, 6))
    matches = random.choices(pool, weights=weights, k=count)
    unique = []
    seen = set()
    for match in matches:
        if match.name in seen:
            continue
        seen.add(match.name)
        unique.append(match)
    while len(unique) < count and len(unique) < len(pool):
        extra = random.choice(pool)
        if extra.name not in seen:
            seen.add(extra.name)
            unique.append(extra)
    player_artist.numble_match_week = week
    player_artist.numble_match_names = [match.name for match in unique]
    return unique


def _artist_gender(name: str) -> str:
    seed = _ecosystem_seed_by_name(name)
    return str(getattr(seed, "gender", "male")) if seed is not None else "male"


def _artist_friendliness(name: str) -> int:
    seed = _ecosystem_seed_by_name(name)
    return int(getattr(seed, "friendliness", 50)) if seed is not None else 50


def _artist_lovingness(name: str) -> int:
    return int(ARTIST_LOVINGNESS.get(name, 50))


def _artist_aggression(name: str) -> int:
    seed = _ecosystem_seed_by_name(name)
    return int(getattr(seed, "aggression", 50)) if seed is not None else 50



def _relationship_social_bonus(world: EcosystemWorld, artist_name: str, partner_name: str, partner_is_artist: bool) -> float:
    if not partner_is_artist:
        return 1.0
    social = world.social_graph.get(artist_name, {})
    friends = set(social.get("friends", []))
    enemies = set(social.get("enemies", []))
    if partner_name in friends:
        return 1.7
    if partner_name in enemies:
        return 0.08
    return 0.95


def _romance_pref_matches_target(preference: str, target_gender: str) -> bool:
    if preference == "prefers_both":
        return True
    if preference == "prefers_male":
        return target_gender == "male"
    if preference == "prefers_female":
        return target_gender == "female"
    return False


def _romance_pair_compatible(artist_name: str, partner_name: str, partner_is_artist: bool) -> bool:
    artist_pref = _artist_hidden_preference(artist_name)
    artist_gender = _artist_gender(artist_name)
    if partner_is_artist:
        partner_pref = _artist_hidden_preference(partner_name)
        partner_gender = _artist_gender(partner_name)
    else:
        hidden = HIDDEN_CHARACTER_BY_NAME.get(partner_name)
        if hidden is None:
            return False
        partner_pref = str(HIDDEN_CHARACTER_ROMANCE_PREFERENCES.get(partner_name, "prefers_female"))
        partner_gender = str(getattr(hidden, "gender", "female"))
    return _romance_pref_matches_target(artist_pref, partner_gender) and _romance_pref_matches_target(partner_pref, artist_gender)


def _romance_visibility(popularity_a: float, popularity_b: float, confirmed: bool = False) -> str:
    peak = max(float(popularity_a), float(popularity_b))
    if confirmed and peak >= 84:
        return "tabloid"
    if peak >= 75:
        return "known"
    if peak >= 88 and random.random() < 0.45:
        return "tabloid"
    return "private"


def _romance_status_label(profile: RomanceProfile) -> str:
    label = ROMANCE_STATUS_LABELS.get(profile.status, profile.status)
    if profile.status == "married" and profile.marriage_count >= 2:
        if profile.marriage_count == 2:
            return "second marriage"
        if profile.marriage_count == 3:
            return "third marriage"
        return f"{profile.marriage_count}th marriage"
    if profile.status == "divorced":
        if profile.divorce_count <= 1:
            return "divorced once"
        if profile.divorce_count == 2:
            return "twice divorced"
        return f"divorced {profile.divorce_count} times"
    return label


def _separation_status_label(profile: RomanceProfile) -> str:
    status = str(getattr(profile, "separation_from_status", "") or "").strip()
    if not status:
        status = "married" if profile.marriage_week else "relationship"
    return ROMANCE_STATUS_LABELS.get(status, status)


def _romance_week_label(week_index: int) -> str:
    if not week_index:
        return "unknown"
    year, week = _year_week_from_world_week(int(week_index))
    return f"Y{year} W{week}"


def _format_week_span(weeks: int) -> str:
    weeks = max(0, int(weeks))
    years = weeks // 52
    rem_weeks = weeks % 52
    months = rem_weeks // 4
    leftover_weeks = rem_weeks % 4
    parts = []
    if years:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    if not years and leftover_weeks:
        parts.append(f"{leftover_weeks} week{'s' if leftover_weeks != 1 else ''}")
    if not parts:
        parts.append("less than a week")
    return ", ".join(parts[:2])


def _romance_duration_from_weeks(start_week: int, end_week: int) -> int:
    if not start_week or not end_week:
        return 0
    return max(1, int(end_week) - int(start_week) + 1)


def _current_romance_duration(profile: RomanceProfile, current_week: int) -> int:
    return _romance_duration_from_weeks(profile.relationship_start_week, current_week)


def _romance_news_headline(
    event_type: str,
    artist_name: str,
    partner_name: str,
    partner_is_artist: bool,
    current_week: int,
    third_party_name: str = "",
) -> str:
    year, _ = _year_week_from_world_week(current_week)
    pools = {
        "relationship_rumor": [
            'relationship speculation intensified this week after {artist} and {partner} were seen together repeatedly.',
            'sources say {artist} and {partner} have been spending time together away from the cameras.',
            'industry chatter continues to build around {artist} and {partner}, though neither side has confirmed anything.',
            'tabloid coverage picked up around {artist} and {partner} after several reported late-night appearances.',
        ],
        "relationship_confirmed": [
            '{artist} and {partner} have publicly confirmed their relationship after weeks of speculation.',
            '{artist} appears to have taken a private relationship public, with {partner} now firmly in the picture.',
            'what had been treated as rumor around {artist} and {partner} is now being spoken about as a confirmed relationship.',
            '{artist} and {partner} are now being described by multiple outlets as a confirmed couple.',
        ],
        "spotted_together": [
            '{artist} and {partner} were spotted together again, pushing relationship rumors into the wider conversation.',
            'another public sighting of {artist} and {partner} has intensified relationship speculation.',
            'award-week cameras kept finding {artist} and {partner} together, and rumor coverage followed quickly.',
        ],
        "engagement": [
            '{artist} and {partner} are said to be engaged after a relationship that stayed relatively quiet for months.',
            'sources close to {artist} say an engagement with {partner} has now been locked in.',
            '{artist} appears to be entering a new chapter, with reports of an engagement to {partner}.',
        ],
        "marriage": [
            '{artist} has reportedly married {partner} in a move that caught much of the industry off guard.',
            '{artist} and {partner} are being described as newly married after keeping the ceremony tightly controlled.',
            'public records and multiple reports now point to {artist} and {partner} having quietly married.',
        ],
        "breakup": [
            '{artist} and {partner} have reportedly split after a relationship that had become increasingly public.',
            'what had looked steady around {artist} and {partner} has now turned into a reported breakup.',
            '{artist} is said to be newly single after a difficult split from {partner}.',
        ],
        "separation": [
            '{artist} and {partner} are said to be quietly separated, with sources describing a difficult stretch behind the scenes.',
            'reports now suggest {artist} and {partner} have separated while trying to keep the details private.',
            'the marriage between {artist} and {partner} appears to have entered a separation period.',
        ],
        "divorce": [
            '{artist} and {partner} are now dealing with a reported divorce after months of speculation.',
            'multiple outlets now describe the split between {artist} and {partner} as a divorce, not a temporary separation.',
            '{artist} appears to be closing a marriage chapter, with divorce reports surrounding {partner}.',
        ],
        "cheating_rumor": [
            'rumors continue around {artist} after reports linked them to {third} while still involved with {partner}.',
            '{artist} is facing cheating allegations after being connected to {third} during an active relationship with {partner}.',
            'relationship coverage around {artist} turned sharply this week after allegations involving {third} surfaced.',
        ],
        "cheating_confirmed": [
            'fallout is growing around {artist} after a cheating scandal involving {third} and longtime partner {partner}.',
            'what began as rumor around {artist} has hardened into a damaging cheating scandal tied to {third}.',
            '{artist} is now dealing with a full public scandal after reports linked them to {third} during their relationship with {partner}.',
        ],
        "denial": [
            '{artist} has pushed back on recent relationship rumors involving {partner}.',
            'a spokesperson for {artist} is denying the latest speculation tied to {partner}.',
            '{artist} is publicly dismissing the latest round of rumors involving {partner}.',
        ],
        "reconciliation_rumor": [
            'rumors of a reconciliation around {artist} and {partner} are resurfacing after a recent public appearance.',
            '{artist} and {partner} are back in the rumor cycle after appearing more comfortable around each other again.',
            'industry observers believe {artist} and {partner} may be revisiting a past relationship.',
        ],
        "award_show_couple": [
            'award-night coverage this year kept returning to {artist} and {partner}, whose public appearance drew heavy attention.',
            '{artist} and {partner} became part of the award-show conversation after arriving together and staying close all night.',
            'one of the side stories of this year\'s ceremony involved {artist} and {partner}, who made a visible appearance as a couple.',
        ],
        "rollout_fallout": [
            'relationship turbulence around {artist} is now being discussed as a distraction from the current rollout.',
            'public interest in {artist} has shifted from the music to relationship fallout involving {partner}.',
            'industry discussion around {artist} this week centered on relationship drama more than the release itself.',
        ],
    }
    template = random.choice(pools.get(event_type, pools["relationship_rumor"]))
    return template.format(artist=artist_name, partner=partner_name, year=year, third=third_party_name or "another figure")


def _record_romance_event(
    world: EcosystemWorld,
    current_week: int,
    event_type: str,
    artist_name: str,
    partner_name: str,
    partner_is_artist: bool,
    confirmed: bool = False,
    visibility: str = "known",
    third_party_name: str = "",
    rumor_confidence: str = "soft",
) -> RomanceEvent:
    event = RomanceEvent(
        id=str(uuid4()),
        week=current_week,
        event_type=event_type,
        artist_name=artist_name,
        partner_name=partner_name,
        partner_is_artist=partner_is_artist,
        headline=_romance_news_headline(
            event_type,
            artist_name,
            partner_name,
            partner_is_artist,
            current_week,
            third_party_name=third_party_name,
        ),
        visibility=visibility,
        confirmed=confirmed,
        third_party_name=third_party_name,
        rumor_confidence=rumor_confidence,
    )
    world.romance_event_history.setdefault(current_week, []).append(event)
    return event


def _romance_stats_for_partner(partner_name: str, partner_is_artist: bool) -> tuple[int, int, float, float, str]:
    if partner_is_artist:
        return (
            _artist_friendliness(partner_name),
            _artist_lovingness(partner_name),
            float(_ecosystem_artist_popularity(partner_name)),
            float(_ecosystem_artist_reputation(partner_name)),
            _artist_gender(partner_name),
        )
    hidden = HIDDEN_CHARACTER_BY_NAME.get(partner_name)
    if hidden is None:
        return 50, 50, 50.0, 50.0, "female"
    return (
        int(getattr(hidden, "friendliness", 50)),
        int(getattr(hidden, "lovingness", 50)),
        float(getattr(hidden, "popularity", 50.0)),
        float(getattr(hidden, "reputation", 50.0)),
        str(getattr(hidden, "gender", "female")),
    )


def _romance_pair_weight(world: EcosystemWorld, artist_name: str, partner_name: str, partner_is_artist: bool) -> float:
    if not _romance_pair_compatible(artist_name, partner_name, partner_is_artist):
        return 0.0
    artist_pop = float(_ecosystem_artist_popularity(artist_name, world))
    artist_friendly = _artist_friendliness(artist_name)
    artist_loving = _artist_lovingness(artist_name)
    artist_aggr = _artist_aggression(artist_name)
    partner_friendly, partner_loving, partner_pop, _, _ = _romance_stats_for_partner(partner_name, partner_is_artist)
    pop_gap = abs(artist_pop - partner_pop)
    gap_factor = max(0.15, 1.0 - (pop_gap / 75.0))
    warmth = ((artist_friendly + partner_friendly) / 200.0) * 0.65 + ((artist_loving + partner_loving) / 200.0) * 0.85
    volatility_penalty = max(0.2, 1.0 - ((artist_aggr + (0 if not partner_is_artist else _artist_aggression(partner_name))) / 260.0))
    base = max(0.15, warmth) * gap_factor * volatility_penalty
    if partner_is_artist:
        partner_profile = _get_romance_profile(world, partner_name)
        if partner_profile is None or partner_profile.status != "single":
            return 0.0
        base *= _relationship_social_bonus(world, artist_name, partner_name, True)
        if artist_name in world.social_graph.get(partner_name, {}).get("enemies", []):
            base *= 0.08
    else:
        if _hidden_character_active_claim(world, partner_name):
            return 0.0
        hidden = HIDDEN_CHARACTER_BY_NAME.get(partner_name)
        archetype = str(getattr(hidden, "category", "")) if hidden is not None else ""
        if archetype in {"actor", "actress", "model"}:
            base *= 1.15
    return max(0.0, base)


def _update_pair_state(
    world: EcosystemWorld,
    artist_name: str,
    partner_name: str,
    partner_is_artist: bool,
    status: str,
    current_week: int,
    visibility: str,
):
    profile = _get_romance_profile(world, artist_name)
    if profile is None:
        return
    if status == "dating":
        profile.relationship_start_week = current_week
        profile.engagement_week = 0
        profile.marriage_week = 0
        profile.separation_week = 0
        profile.separation_from_status = ""
        profile.divorce_week = 0
    elif status == "engaged":
        profile.engagement_week = current_week
    elif status == "married":
        profile.marriage_week = current_week
        profile.marriage_count += 1
        profile.separation_week = 0
        profile.separation_from_status = ""
        profile.divorce_week = 0
    elif status == "separated":
        profile.separation_week = current_week
        profile.separation_from_status = profile.status if profile.status != "separated" else profile.separation_from_status
    elif status == "divorced":
        profile.divorce_week = current_week
        profile.divorce_count += 1
        profile.last_breakup_week = current_week
    elif status == "single":
        profile.last_breakup_week = current_week
    profile.status = status
    profile.partner_name = partner_name
    profile.partner_is_artist = partner_is_artist
    profile.visibility = visibility
    profile.last_event_week = current_week
    if partner_name and partner_name not in profile.partner_history:
        profile.partner_history.append(partner_name)


def _clear_pair_state(world: EcosystemWorld, artist_name: str, current_week: int, divorced: bool = False):
    profile = _get_romance_profile(world, artist_name)
    if profile is None:
        return
    _record_ex_relationship(profile, current_week, divorced=divorced)
    profile.status = "divorced" if divorced else "single"
    profile.partner_name = ""
    profile.partner_is_artist = False
    profile.visibility = "private"
    profile.last_breakup_week = current_week
    profile.last_event_week = current_week
    profile.relationship_start_week = 0
    profile.engagement_week = 0
    profile.marriage_week = 0
    profile.separation_week = 0
    profile.separation_from_status = ""


def _pair_key(a: str, b: str) -> tuple[str, str]:
    return tuple(sorted((a, b)))


def _mark_artist_enemies(world: EcosystemWorld, artist_a: str, artist_b: str):
    if artist_a == artist_b:
        return
    left = world.social_graph.setdefault(artist_a, {"friends": [], "enemies": []})
    right = world.social_graph.setdefault(artist_b, {"friends": [], "enemies": []})
    if artist_b not in left["enemies"]:
        left["enemies"].append(artist_b)
    if artist_a not in right["enemies"]:
        right["enemies"].append(artist_a)
    if artist_b in left["friends"]:
        left["friends"].remove(artist_b)
    if artist_a in right["friends"]:
        right["friends"].remove(artist_a)


def _romance_weekly_start_budget(world: EcosystemWorld) -> int:
    active = sum(1 for profile in world.romance_profiles.values() if profile.status in {"dating", "engaged", "married"})
    budget = 1 if random.random() < 0.28 else 0
    if active < 9 and random.random() < 0.08:
        budget += 1
    return budget


def _active_release_pressure(world: EcosystemWorld, artist_name: str) -> float:
    recent = world.release_history.get(artist_name, [])[-2:]
    pressure = 0.0
    for release in recent:
        age = max(0, int(world.week_number) - int(getattr(release, "week_number", world.week_number)))
        if age <= 8:
            pressure += max(0.0, 1.2 - (age / 8.0))
    return pressure


def _apply_romance_world_effects(world: EcosystemWorld, events: list[RomanceEvent], player_artist: Artist):
    for event in events:
        if event.event_type == "relationship_confirmed":
            _apply_popularity_delta_to_actor(event.artist_name, 0.6, player_artist, world)
            _apply_reputation_delta_to_actor(event.artist_name, 0.4, player_artist, world)
            if event.partner_is_artist:
                _apply_popularity_delta_to_actor(event.partner_name, 0.6, player_artist, world)
                _apply_reputation_delta_to_actor(event.partner_name, 0.4, player_artist, world)
        elif event.event_type == "marriage":
            _apply_reputation_delta_to_actor(event.artist_name, 0.8, player_artist, world)
            if event.partner_is_artist:
                _apply_reputation_delta_to_actor(event.partner_name, 0.8, player_artist, world)
        elif event.event_type in {"breakup", "separation"}:
            _apply_popularity_delta_to_actor(event.artist_name, 0.4, player_artist, world)
            _apply_reputation_delta_to_actor(event.artist_name, -0.5, player_artist, world)
            if event.partner_is_artist:
                _apply_popularity_delta_to_actor(event.partner_name, 0.4, player_artist, world)
                _apply_reputation_delta_to_actor(event.partner_name, -0.5, player_artist, world)
        elif event.event_type == "divorce":
            _apply_reputation_delta_to_actor(event.artist_name, -1.1, player_artist, world)
            if event.partner_is_artist:
                _apply_reputation_delta_to_actor(event.partner_name, -1.1, player_artist, world)
        elif event.event_type in {"cheating_rumor", "cheating_confirmed"}:
            _apply_reputation_delta_to_actor(event.artist_name, -1.8 if event.event_type == "cheating_confirmed" else -0.9, player_artist, world)
            _apply_popularity_delta_to_actor(event.artist_name, 0.7, player_artist, world)
            if event.partner_is_artist:
                _apply_reputation_delta_to_actor(event.partner_name, 0.3, player_artist, world)


def _simulate_romance_week(player_artist: Artist, world: EcosystemWorld | None, current_week: int) -> list[RomanceEvent]:
    if world is None:
        return []
    _ensure_romance_state(world)
    if int(getattr(world, "romance_last_processed_week", 0)) >= int(current_week):
        return list(world.romance_event_history.get(current_week, []))
    world.romance_event_history[current_week] = []
    events: list[RomanceEvent] = []
    processed_pairs: set[tuple[str, str]] = set()

    budget = _romance_weekly_start_budget(world)
    shuffled = [seed.name for seed in ARTIST_ECOSYSTEM_SEEDS]
    random.shuffle(shuffled)
    starts = 0
    for artist_name in shuffled:
        if starts >= budget:
            break
        if _try_start_relationship(world, artist_name, current_week, events):
            starts += 1

    for artist_name in shuffled:
        _resolve_relationship_turn(world, artist_name, current_week, processed_pairs, events)

    _apply_romance_world_effects(world, events, player_artist)
    world.romance_last_processed_week = current_week
    if events:
        world.romance_event_history[current_week] = list(events)
    return events


def _generate_romance_news_reports(world: EcosystemWorld | None, current_week: int) -> list[NewsReport]:
    if world is None:
        return []
    _ensure_romance_state(world)
    events = list(world.romance_event_history.get(current_week, []))
    if not events:
        return []
    if _is_grammy_media_week(current_week):
        priority = {"award_show_couple", "cheating_confirmed", "divorce", "marriage"}
        preferred = [event for event in events if event.event_type in priority]
        events = preferred[:1] if preferred else events[:1]
    reports: list[NewsReport] = []
    for event in events:
        report = _build_news_report(
            current_week,
            "relationship",
            event.headline,
            artist=event.artist_name,
            target=event.partner_name,
            subject=event.event_type,
        )
        report.id = event.id
        reports.append(report)
    return reports


def _apply_player_love_weekly_effects(artist: Artist, world: EcosystemWorld | None):
    current = _player_current_love(artist)
    if current is None:
        return
    partner_meta = _partner_meta(current.partner_name, current.partner_is_artist, world)
    pop_gap = abs(float(artist.popularity) - float(partner_meta["popularity"]))
    rep_gap = abs(float(artist.reputation) - float(partner_meta["reputation"]))
    career_pressure = max(0.0, (pop_gap - 24.0) * 0.10 + (rep_gap - 20.0) * 0.08)
    if artist.last_week_streams >= 1_000_000:
        current.lovingness = clamp_meter(current.lovingness + random.uniform(0.4, 1.4))
        current.strength = clamp_meter(current.strength + random.uniform(0.2, 0.9))
    current.lovingness = clamp_meter(current.lovingness - career_pressure)
    current.strength = clamp_meter(current.strength - (career_pressure * 0.7))
    if current.cheated:
        current.lovingness = clamp_meter(current.lovingness - random.uniform(1.0, 3.0))
        current.strength = clamp_meter(current.strength - random.uniform(0.8, 2.2))
    if current.lovingness >= 78.0 and current.strength >= 60.0:
        artist.popularity_state.organic = clamp_popularity(artist.popularity_state.organic + 0.20)
        artist.reputation = clamp_meter(artist.reputation + 0.15)
        artist.health = clamp_meter(artist.health + 0.8)
        print(f"Relationship boost: {current.partner_name}'s support helped your image and recovery.")
    elif current.lovingness <= 25.0:
        artist.popularity_state.organic = clamp_popularity(artist.popularity_state.organic - 0.25)
        artist.reputation = clamp_meter(artist.reputation - 0.35)
        artist.health = clamp_meter(artist.health - 0.8)
        print(f"Relationship stress: drama with {current.partner_name} hurt your focus and public image.")
    if current.lovingness <= 8.0 or current.strength <= 6.0:
        current.status = "ex"
        current.end_week = _player_week_index(artist)
        current.notes.append("collapsed from low lovingness")
        _publish_player_romance_event(artist, world, "breakup", current.partner_name, current.partner_is_artist, confirmed=True, visibility="known")
        print(f"{current.partner_name} ended the relationship. The love bar hit rock bottom.")


def numble_menu(player_artist: Artist, world: EcosystemWorld | None):
    matches = _numble_matches(player_artist)
    while True:
        print("\nNUMBLE")
        print("Celebrity dating software. Matches shuffle every week around your popularity range.")
        current = _player_current_love(player_artist)
        if current is not None:
            print(f"Current relationship: {current.partner_name}")
            print(meter_bar("Lovingness", current.lovingness))
        options = []
        for match in matches:
            meta = _partner_meta(match.name, False, world)
            chance = _player_relationship_score(player_artist, match.name, False, world)
            options.append(
                f"{match.name} | {meta['category']} | pop {meta['popularity']:.0f} | rep {meta['reputation']:.0f} | match {chance:.0f}%"
            )
        idx = choose_from_list("Your NUMBLE matches", options, allow_cancel=True)
        if idx is None:
            return
        target = matches[idx]
        while True:
            meta = _partner_meta(target.name, False, world)
            print(f"\n{target.name}")
            print(f"Type: {meta['category']} | Popularity {meta['popularity']:.0f} | Reputation {meta['reputation']:.0f}")
            print(f"Lovingness: {meta['lovingness']} | Friendliness: {meta['friendliness']}")
            current = _player_current_love(player_artist)
            actions = []
            if current is not None:
                actions.extend([
                    "Break up and start new relationship",
                    "Cheat and hook up",
                    "Just chat",
                    "Back",
                ])
            else:
                actions.extend([
                    "Start dating",
                    "Hook up",
                    "Just chat",
                    "Back",
                ])
            action = choose_from_list("NUMBLE options", actions, allow_cancel=False)
            if action == len(actions) - 1:
                break
            if current is not None:
                if action == 0:
                    _end_player_relationship(player_artist, world, reason=f"left for {target.name}")
                    _attempt_player_date(player_artist, world, target.name, False, from_numble=True)
                elif action == 1:
                    _player_hookup(player_artist, world, target.name, False)
                else:
                    print(f"You and {target.name} traded messages. The algorithm purrs ominously.")
            else:
                if action == 0:
                    _attempt_player_date(player_artist, world, target.name, False, from_numble=True)
                elif action == 1:
                    _player_hookup(player_artist, world, target.name, False)
                else:
                    print(f"You and {target.name} traded messages. Tiny sparks, maybe.")


def player_love_relationships_menu(player_artist: Artist, world: EcosystemWorld | None):
    while True:
        current = _player_current_love(player_artist)
        exes = _player_love_rows(player_artist, {"ex"})
        flings = _player_love_rows(player_artist, {"fling"})
        options = [
            f"Current relationship ({current.partner_name if current else 'none'})",
            f"Exes ({len(exes)})",
            f"Flings ({len(flings)})",
            "Back",
        ]
        choice = choose_from_list("Your Love Relationships", options, allow_cancel=False)
        if choice == 3:
            return
        if choice == 0:
            if current is None:
                print("\nYou are single right now.")
                continue
            while True:
                duration = _romance_duration_from_weeks(current.start_week, _player_week_index(player_artist))
                print(f"\nYou + {current.partner_name}")
                print(meter_bar("Lovingness", current.lovingness))
                print(meter_bar("Strength ", current.strength))
                print(f"Together: {_format_week_span(duration)} | Visibility: {current.visibility}")
                actions = [
                    "Ask on date",
                    "Post couple photo",
                    "Have a hard conversation",
                    "Break up",
                    "Back",
                ]
                action = choose_from_list("Manage relationship", actions, allow_cancel=False)
                if action == 4:
                    break
                if action == 0:
                    boost = random.uniform(4.0, 11.0)
                    current.lovingness = clamp_meter(current.lovingness + boost)
                    current.strength = clamp_meter(current.strength + boost * 0.65)
                    player_artist.fatigue = clamp_fatigue(player_artist.fatigue + 0.0)
                    print(f"The date went well. Lovingness +{boost:.1f}.")
                    print(meter_bar("Lovingness", current.lovingness))
                elif action == 1:
                    current.visibility = "known"
                    current.lovingness = clamp_meter(current.lovingness + random.uniform(1.0, 4.0))
                    player_artist.popularity_state.organic = clamp_popularity(player_artist.popularity_state.organic + 0.4)
                    _publish_player_romance_event(player_artist, world, "spotted_together", current.partner_name, current.partner_is_artist, confirmed=True, visibility="known")
                    print("The couple post warmed fans up and pushed the relationship into public view.")
                elif action == 2:
                    if current.cheated:
                        current.lovingness = clamp_meter(current.lovingness - random.uniform(2.0, 7.0))
                        current.strength = clamp_meter(current.strength - random.uniform(1.0, 5.0))
                        print("The conversation got tense. Secrets are heavy.")
                    else:
                        current.strength = clamp_meter(current.strength + random.uniform(3.0, 8.0))
                        print("You talked honestly. The relationship feels sturdier.")
                elif action == 3:
                    _end_player_relationship(player_artist, world)
                    break
        elif choice == 1:
            print("\nExes")
            if not exes:
                print("No exes yet.")
            for rel in reversed(exes[-20:]):
                print(f"- {rel.partner_name} | ended {_romance_week_label(rel.end_week)} | love {rel.lovingness:.1f} | {', '.join(rel.notes[-2:])}")
            input("\nPress Enter to go back...")
        elif choice == 2:
            print("\nFlings")
            if not flings:
                print("No flings yet.")
            for rel in reversed(flings[-20:]):
                print(f"- {rel.partner_name} | {_romance_week_label(rel.start_week)} | spark {rel.lovingness:.1f}")
            input("\nPress Enter to go back...")


def view_love_relationships_menu(world: EcosystemWorld | None):
    if world is None:
        print("\nNo relationship data available.")
        return
    _ensure_romance_state(world)
    current_week = int(getattr(world, "week_number", 0) or 0)
    active_statuses = {"dating", "engaged", "married", "separated"}
    rows = []
    seen_pairs = set()
    for artist_name, profile in sorted(world.romance_profiles.items(), key=lambda item: item[0].lower()):
        if profile.status not in active_statuses or not profile.partner_name:
            continue
        pair_name = profile.partner_name if profile.partner_is_artist else f"hidden:{profile.partner_name}"
        pair_key = _pair_key(artist_name, pair_name)
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        duration = _current_romance_duration(profile, current_week)
        rows.append(
            {
                "artist": artist_name,
                "partner": profile.partner_name,
                "status": _romance_status_label(profile),
                "visibility": profile.visibility,
                "start_week": int(profile.relationship_start_week or 0),
                "duration_weeks": duration,
            }
        )

    rows.sort(key=lambda row: (-row["duration_weeks"], row["artist"].lower(), row["partner"].lower()))
    print("\nCurrent Love Relationships")
    print("-" * 26)
    if not rows:
        print("No active love relationships right now.")
        input("\nPress Enter to go back...")
        return

    artist_width = max(len("Artist"), max(len(row["artist"]) for row in rows))
    partner_width = max(len("Partner"), max(len(row["partner"]) for row in rows))
    print(f"{'Artist':<{artist_width}}  {'Partner':<{partner_width}}  Status       Together")
    for row in rows:
        duration = int(row["duration_weeks"])
        together = (
            f"{_format_week_span(duration)} ({duration} week{'s' if duration != 1 else ''}, "
            f"since {_romance_week_label(row['start_week'])})"
        )
        print(
            f"{row['artist']:<{artist_width}}  {row['partner']:<{partner_width}}  "
            f"{row['status']:<12} {together}"
        )
    input("\nPress Enter to go back...")


def view_separated_relationships_menu(world: EcosystemWorld | None):
    if world is None:
        print("\nNo relationship data available.")
        return
    _ensure_romance_state(world)
    current_week = int(getattr(world, "week_number", 0) or 0)
    rows = []
    seen_pairs = set()
    for artist_name, profile in sorted(world.romance_profiles.items(), key=lambda item: item[0].lower()):
        if profile.status != "separated" or not profile.partner_name:
            continue
        pair_name = profile.partner_name if profile.partner_is_artist else f"hidden:{profile.partner_name}"
        pair_key = _pair_key(artist_name, pair_name)
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)
        duration = _current_romance_duration(profile, current_week)
        separated_for = _romance_duration_from_weeks(profile.separation_week, current_week)
        rows.append(
            {
                "artist": artist_name,
                "partner": profile.partner_name,
                "separated_from": _separation_status_label(profile),
                "separation_week": int(profile.separation_week or 0),
                "duration_weeks": duration,
                "separated_for_weeks": separated_for,
            }
        )

    rows.sort(key=lambda row: (-row["separated_for_weeks"], row["artist"].lower(), row["partner"].lower()))
    print("\nSeparated Relationships")
    print("-" * 23)
    if not rows:
        print("No separated relationships right now.")
        input("\nPress Enter to go back...")
        return

    artist_width = max(len("Artist"), max(len(row["artist"]) for row in rows))
    partner_width = max(len("Partner"), max(len(row["partner"]) for row in rows))
    print(f"{'Artist':<{artist_width}}  {'Partner':<{partner_width}}  Separated From  Since")
    for row in rows:
        separated_for = int(row["separated_for_weeks"])
        since = (
            f"{_romance_week_label(row['separation_week'])} "
            f"({_format_week_span(separated_for)}, {separated_for} week{'s' if separated_for != 1 else ''})"
        )
        total = int(row["duration_weeks"])
        print(
            f"{row['artist']:<{artist_width}}  {row['partner']:<{partner_width}}  "
            f"{row['separated_from']:<14} {since} | together {_format_week_span(total)}"
        )
    input("\nPress Enter to go back...")


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
    return min(15.0, delta * 3.0)


def _crit_delta(friendliness):
    scale = 0.85 + ((55.0 - friendliness) / 120.0)
    delta = -random.uniform(2.0, 6.0) * max(0.55, min(1.25, scale))
    return max(-7.5, min(-1.2, delta))


def _relationship_bar(value):
    return meter_bar("Relationship", value, width=22)


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


def manage_relationships_menu(player_artist, world: EcosystemWorld | None = None):
    while True:
        seeds = sorted(ARTIST_ECOSYSTEM_SEEDS, key=lambda s: s.name.lower())
        options = []
        for seed in seeds:
            state = player_artist.relationships.get(seed.name, RelationshipState())
            options.append(f"{seed.name} | rel {state.score:.1f} | friendly {int(seed.friendliness)}")
        idx = choose_from_list("Choose an artist to interact with", options, allow_cancel=True)
        if idx is None:
            return
        target = seeds[idx]
        state = player_artist.relationships.setdefault(target.name, RelationshipState(score=10.0))
        while True:
            week_index = _player_week_index(player_artist)
            if TEST_RELATIONSHIP_LOCK and getattr(player_artist, "_relationship_lock", False):
                state.score = 100.0
            friendliness = int(getattr(target, "friendliness", 50))
            lovingness = int(ARTIST_LOVINGNESS.get(target.name, 50))
            tier = _relationship_tier(friendliness)

            print(f"\n{target.name}")
            print(_relationship_bar(state.score))
            print(f"Friendship: {_friendship_label(state.score)}")
            print(f"Lovingness: {lovingness}")
            print("Tip: praise only boosts once per week. Requests/criticism always stack.")

            actions = [
                "Text them how you feel about their music",
                "Congratulate them on a release",
                "Send them a demo link",
                "Ask them for a gig slot",
                "Ask for a feature",
                "Request them for money",
                "Ask them out on a date",
                "Criticize their recent interview",
                "Back",
            ]
            action = choose_from_list("Interaction options", actions, allow_cancel=False)
            if action == 8:
                break

            def say(speaker, text):
                print(f"{speaker}: {text}")

            if action == 0:
                say(player_artist.name, prompt_text(f"{player_artist.name}: ", "just wanted to say i respect your music"))
                if not _should_respond(friendliness, state.score, "praise"):
                    say(target.name, "...")
                else:
                    if tier == "friendly":
                        say(target.name, random.choice([
                            "that means a lot. salute.",
                            "appreciate you. keep going.",
                            "love. i see you.",
                            "thank you, fr. keep making records.",
                        ]))
                    elif tier == "neutral":
                        say(target.name, random.choice([
                            "respect.",
                            "good looks.",
                            "appreciate that.",
                            "thanks.",
                        ]))
                    else:
                        say(target.name, random.choice([
                            "aight.",
                            "cool.",
                            "ok.",
                            "sure.",
                        ]))
                    if state.last_positive_week_interaction != week_index:
                        _apply_relationship_delta(
                            player_artist, target.name, _praise_delta(friendliness)
                        )
                        state.last_positive_week_interaction = week_index

            elif action == 1:
                say(player_artist.name, f"yo {target.name}, congrats on the drop. good work.")
                if not _should_respond(friendliness, state.score, "praise"):
                    say(target.name, "seen.")
                else:
                    if tier == "friendly":
                        say(target.name, random.choice([
                            "thank you. that means a lot.",
                            "love. i appreciate you.",
                            "real one. salute.",
                        ]))
                    elif tier == "neutral":
                        say(target.name, random.choice([
                            "appreciate it.",
                            "thanks.",
                            "respect.",
                        ]))
                    else:
                        say(target.name, random.choice([
                            "ok.",
                            "cool.",
                            "word.",
                        ]))
                    if state.last_positive_week_interaction != week_index:
                        _apply_relationship_delta(
                            player_artist,
                            target.name,
                            min(15.0, random.uniform(0.4, 2.0) * 3.0),
                        )
                        state.last_positive_week_interaction = week_index

            elif action == 2:
                say(player_artist.name, f"yo {target.name}, i just sent you a demo link. lmk what you think.")
                if not _should_respond(friendliness, state.score, "gig"):
                    say(target.name, "seen.")
                    _apply_relationship_delta(player_artist, target.name, -0.2)
                else:
                    if tier == "friendly":
                        say(target.name, random.choice([
                            "send it. i'll listen when i can.",
                            "bet. i'll check it out.",
                            "yeah, drop it. i'm curious.",
                        ]))
                    elif tier == "neutral":
                        say(target.name, random.choice([
                            "i'll see.",
                            "send it.",
                            "maybe.",
                        ]))
                    else:
                        say(target.name, random.choice([
                            "nah.",
                            "no.",
                            "stop texting me.",
                        ]))
                    delta = random.uniform(-0.8, 1.2)
                    if delta > 0:
                        delta = min(15.0, delta * 3.0)
                    _apply_relationship_delta(player_artist, target.name, delta)

            elif action == 3:
                say(player_artist.name, f"yo {target.name}, any chance i can open for you sometime?")
                if not _should_respond(friendliness, state.score, "gig"):
                    say(target.name, "seen.")
                    _apply_relationship_delta(player_artist, target.name, -0.4)
                else:
                    chance = (state.score / 100.0) * 0.65 + (friendliness / 100.0) * 0.25
                    if random.random() < chance and state.score >= 25:
                        say(target.name, random.choice([
                            "maybe. send me your best records and we'll talk.",
                            "yeah, i can see that. let's see the music.",
                            "possibly. hit my email with your strongest songs.",
                        ]))
                        _apply_relationship_delta(
                            player_artist,
                            target.name,
                            min(15.0, random.uniform(0.8, 2.5) * 3.0),
                        )
                    else:
                        if tier == "friendly":
                            say(target.name, random.choice([
                                "not right now, but keep grinding. it can happen later.",
                                "i can't promise that yet, but keep working and stay consistent.",
                            ]))
                        elif tier == "neutral":
                            say(target.name, random.choice([
                                "not right now.",
                                "i'm not looking for openers right now.",
                            ]))
                        else:
                            say(target.name, random.choice([
                                "nah.",
                                "no.",
                                "who are you again?",
                            ]))
                        _apply_relationship_delta(
                            player_artist, target.name, -random.uniform(0.6, 2.2)
                        )

            elif action == 4:
                say(player_artist.name, f"yo {target.name}, you down for a feature?")
                if week_index - state.last_request_week <= 4:
                    state.recent_requests += 1
                else:
                    state.recent_requests = 1
                state.last_request_week = week_index
                request_penalty = 1.2 + (state.recent_requests - 1) * 0.9
                if not _should_respond(friendliness, state.score, "money"):
                    say(target.name, "...")
                    _apply_relationship_delta(player_artist, target.name, -request_penalty)
                else:
                    base = (state.score / 100.0) * 0.7 + (friendliness / 100.0) * 0.2
                    if base > 0.55 and state.score >= 45:
                        if tier == "friendly":
                            say(target.name, random.choice([
                                "yeah. send the beat and the theme.",
                                "i'm down. what's the vibe?",
                                "let's do it. send the pack.",
                            ]))
                        else:
                            say(target.name, random.choice([
                                "maybe. send it.",
                                "i'll consider it. send details.",
                            ]))
                        bonus = min(15.0, random.uniform(1.0, 2.8) * 3.0)
                        _apply_relationship_delta(
                            player_artist, target.name, (-request_penalty + bonus)
                        )
                    else:
                        if tier == "friendly":
                            say(target.name, random.choice([
                                "not right now, but keep building and we can revisit.",
                                "i can't commit to that.",
                            ]))
                        elif tier == "neutral":
                            say(target.name, random.choice([
                                "no.",
                                "not happening.",
                            ]))
                        else:
                            say(target.name, random.choice([
                                "nah who are you again?",
                                "lol no.",
                                "stop.",
                            ]))
                        _apply_relationship_delta(
                            player_artist, target.name, (-request_penalty - 0.5)
                        )

            elif action == 5:
                say(player_artist.name, f"hey {target.name}, can i get a few bucks for my studio rent")
                if week_index - state.last_request_week <= 4:
                    state.recent_requests += 1
                else:
                    state.recent_requests = 1
                state.last_request_week = week_index

                request_penalty = 1.5 + (state.recent_requests - 1) * 1.2
                if not _should_respond(friendliness, state.score, "money"):
                    say(target.name, "...")
                    _apply_relationship_delta(player_artist, target.name, -request_penalty)
                else:
                    afford_chance = (state.score / 100.0) * 0.6 + (friendliness / 100.0) * 0.25
                    if random.random() < afford_chance and state.score >= 50:
                        if tier == "friendly":
                            say(target.name, random.choice([
                                "sure my man, return whenever you feel like.",
                                "i got you. just lock in and pay it forward later.",
                                "yeah, i can help. keep it moving.",
                            ]))
                        elif tier == "neutral":
                            say(target.name, random.choice([
                                "i can spot you a little. don't make it a habit.",
                                "fine. don't turn this into a pattern.",
                            ]))
                        else:
                            say(target.name, random.choice([
                                "nah.",
                                "no.",
                                "get your money up.",
                            ]))
                        _apply_relationship_delta(
                            player_artist, target.name, (-request_penalty + 3.0)
                        )
                    else:
                        if tier == "friendly":
                            say(target.name, random.choice([
                                "i really can't right now. i'm sorry my brother.",
                                "i can't do that, but i hope it works out.",
                            ]))
                        elif tier == "neutral":
                            say(target.name, random.choice([
                                "i can't.",
                                "not doing that.",
                            ]))
                        else:
                            say(target.name, random.choice([
                                "nah who are you again?",
                                "lol no.",
                                "stop texting me.",
                            ]))
                        _apply_relationship_delta(
                            player_artist, target.name, (-request_penalty - 0.6)
                        )

            elif action == 6:
                say(player_artist.name, f"yo {target.name}... you wanna go out sometime?")
                if week_index - state.last_request_week <= 4:
                    state.recent_requests += 1
                else:
                    state.recent_requests = 1
                state.last_request_week = week_index

                awkward_penalty = 1.6 + (state.recent_requests - 1) * 1.0
                if not _should_respond(friendliness, state.score, "date"):
                    say(target.name, "...")
                    _apply_relationship_delta(player_artist, target.name, -awkward_penalty)
                else:
                    base = (state.score / 100.0) * 0.55 + (lovingness / 100.0) * 0.35 + (friendliness / 100.0) * 0.10
                    if base > 0.62 and state.score >= 60:
                        if tier == "friendly":
                            say(target.name, random.choice([
                                "yeah. that's sweet. let's do it.",
                                "i'm down. let's keep it lowkey though.",
                                "okay, i can't lie, that's cute. yeah.",
                            ]))
                        else:
                            say(target.name, random.choice([
                                "sure. let's see.",
                                "yeah, why not.",
                            ]))
                        _apply_relationship_delta(
                            player_artist,
                            target.name,
                            min(15.0, random.uniform(4.0, 8.0) * 3.0),
                        )
                        _attempt_player_date(player_artist, world, target.name, True)
                    else:
                        if tier == "friendly":
                            say(target.name, random.choice([
                                "i'm flattered, but i can't.",
                                "not like that. i respect you though.",
                                "i'm not in that headspace right now.",
                            ]))
                        elif tier == "neutral":
                            say(target.name, random.choice([
                                "no.",
                                "nah.",
                                "i'm good.",
                            ]))
                        else:
                            say(target.name, random.choice([
                                "lol no.",
                                "that's crazy.",
                                "stop.",
                            ]))
                        _apply_relationship_delta(
                            player_artist,
                            target.name,
                            (-random.uniform(1.8, 4.2) - awkward_penalty),
                        )

            elif action == 7:
                say(player_artist.name, "that interview you did was kinda wild ngl.")
                if not _should_respond(friendliness, state.score, "criticize"):
                    say(target.name, "k.")
                    _apply_relationship_delta(player_artist, target.name, -0.8)
                else:
                    if tier == "friendly":
                        say(target.name, random.choice([
                            "i hear you. i could've handled that better.",
                            "fair. i was annoyed. my bad.",
                        ]))
                    elif tier == "neutral":
                        say(target.name, random.choice([
                            "ok.",
                            "cool opinion.",
                            "whatever.",
                        ]))
                    else:
                        say(target.name, random.choice([
                            "shut up.",
                            "you got too much to say.",
                            "mind your business.",
                        ]))
                    _apply_relationship_delta(player_artist, target.name, _crit_delta(friendliness))

            state.last_interaction_week = week_index
            state.last_contact_week = week_index


def _partner_meta(partner_name: str, partner_is_artist: bool, world: EcosystemWorld | None = None) -> dict:
    if partner_is_artist:
        seed = _ecosystem_seed_by_name(partner_name)
        return {
            "name": partner_name,
            "gender": _artist_gender(partner_name),
            "preference": _artist_hidden_preference(partner_name),
            "friendliness": _artist_friendliness(partner_name),
            "lovingness": _artist_lovingness(partner_name),
            "popularity": float(_ecosystem_artist_popularity(partner_name, world)),
            "reputation": float(_ecosystem_artist_reputation(partner_name, world)),
            "category": "artist",
            "available": seed is not None,
        }
    hidden = HIDDEN_CHARACTER_BY_NAME.get(partner_name)
    if hidden is None:
        return {
            "name": partner_name,
            "gender": "female",
            "preference": "prefers_male",
            "friendliness": 50,
            "lovingness": 50,
            "popularity": 50.0,
            "reputation": 50.0,
            "category": "hidden",
            "available": False,
        }
    return {
        "name": partner_name,
        "gender": str(getattr(hidden, "gender", "female")),
        "preference": str(HIDDEN_CHARACTER_ROMANCE_PREFERENCES.get(partner_name, "prefers_female")),
        "friendliness": int(getattr(hidden, "friendliness", 50)),
        "lovingness": int(getattr(hidden, "lovingness", 50)),
        "popularity": float(getattr(hidden, "popularity", 50.0)),
        "reputation": float(getattr(hidden, "reputation", 50.0)),
        "category": str(getattr(hidden, "category", "celebrity")),
        "available": True,
    }


def _artist_hidden_preference(name: str) -> str:
    seed = _ecosystem_seed_by_name(name)
    if seed is not None and getattr(seed, "romance_preference", None):
        return str(seed.romance_preference)
    return str(ARTIST_ROMANCE_PREFERENCES.get(name, "prefers_female"))


def _hidden_character_active_claim(world: EcosystemWorld, hidden_name: str) -> str | None:
    _ensure_romance_state(world)
    for artist_name, profile in world.romance_profiles.items():
        if (
            not profile.partner_is_artist
            and profile.partner_name == hidden_name
            and profile.status in ROMANCE_ACTIVE_STATUSES
        ):
            return artist_name
    return None


def _record_ex_relationship(profile: RomanceProfile, current_week: int, divorced: bool = False) -> None:
    if not profile.partner_name:
        return
    start_week = int(profile.relationship_start_week or 0)
    end_week = int(current_week or 0)
    duration_weeks = _romance_duration_from_weeks(start_week, end_week)
    entry = {
        "partner_name": profile.partner_name,
        "partner_is_artist": bool(profile.partner_is_artist),
        "start_week": start_week,
        "end_week": end_week,
        "duration_weeks": duration_weeks,
        "final_status": "divorce" if divorced or profile.status == "married" else "breakup",
    }
    if not profile.ex_relationships or profile.ex_relationships[-1] != entry:
        profile.ex_relationships.append(entry)


def _relationship_scandal_pressure(world: EcosystemWorld, artist_name: str, partner_name: str, partner_is_artist: bool) -> float:
    artist_pop = float(_ecosystem_artist_popularity(artist_name, world))
    partner_pop = float(_romance_stats_for_partner(partner_name, partner_is_artist)[2])
    artist_pressure = (_artist_aggression(artist_name) / 100.0) * 18.0
    artist_pressure += _recent_controversy_load(world, artist_name) * 3.2
    artist_pressure += _active_release_pressure(world, artist_name) * 4.5
    artist_pressure += max(0.0, artist_pop - 70.0) * 0.16
    if partner_is_artist:
        artist_pressure += (_artist_aggression(partner_name) / 100.0) * 9.0
        artist_pressure += _recent_controversy_load(world, partner_name) * 2.5
    artist_pressure += abs(artist_pop - partner_pop) * 0.12
    return clamp_meter(artist_pressure)


def _relationship_stability(world: EcosystemWorld, artist_name: str, partner_name: str, partner_is_artist: bool, profile: RomanceProfile) -> float:
    artist_friendly = _artist_friendliness(artist_name)
    artist_loving = _artist_lovingness(artist_name)
    artist_aggr = _artist_aggression(artist_name)
    partner_friendly, partner_loving, partner_pop, _, _ = _romance_stats_for_partner(partner_name, partner_is_artist)
    artist_pop = float(_ecosystem_artist_popularity(artist_name, world))
    weeks_together = max(1, int(world.week_number) - int(profile.relationship_start_week or world.week_number) + 1)
    base = 28.0
    base += ((artist_friendly + partner_friendly) / 200.0) * 24.0
    base += ((artist_loving + partner_loving) / 200.0) * 26.0
    base -= ((artist_aggr + (0 if not partner_is_artist else _artist_aggression(partner_name))) / 200.0) * 18.0
    base -= abs(artist_pop - partner_pop) * 0.16
    base -= _recent_controversy_load(world, artist_name) * 2.0
    if partner_is_artist:
        base -= _recent_controversy_load(world, partner_name) * 1.5
        base *= _relationship_social_bonus(world, artist_name, partner_name, True)
    base += min(8.0, weeks_together * 0.35)
    if profile.status == "married":
        base += 6.0
    if profile.status == "separated":
        base -= 14.0
    return clamp_meter(base)


def _try_start_relationship(world: EcosystemWorld, artist_name: str, current_week: int, events: list[RomanceEvent]) -> bool:
    profile = _get_romance_profile(world, artist_name)
    if profile is None or profile.status != "single":
        return False
    if (current_week - int(profile.last_breakup_week)) < 8:
        return False
    base_chance = 0.02
    base_chance += (_artist_lovingness(artist_name) / 1000.0)
    base_chance += (_artist_friendliness(artist_name) / 1800.0)
    base_chance -= (_artist_aggression(artist_name) / 2400.0)
    if random.random() >= max(0.01, base_chance):
        return False

    prefer_hidden = random.random() < 0.64
    weighted_candidates: list[tuple[str, bool, float]] = []
    if prefer_hidden:
        for hidden in HIDDEN_CHARACTER_SEEDS:
            weight = _romance_pair_weight(world, artist_name, hidden.name, False)
            if weight > 0:
                weighted_candidates.append((hidden.name, False, weight))
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        if seed.name == artist_name:
            continue
        weight = _romance_pair_weight(world, artist_name, seed.name, True)
        if weight > 0:
            weighted_candidates.append((seed.name, True, weight * (0.68 if prefer_hidden else 1.18)))
    if not weighted_candidates:
        return False
    partner_name, partner_is_artist, _ = random.choices(
        weighted_candidates,
        weights=[row[2] for row in weighted_candidates],
        k=1,
    )[0]
    partner_pop = float(_romance_stats_for_partner(partner_name, partner_is_artist)[2])
    visibility = _romance_visibility(float(_ecosystem_artist_popularity(artist_name, world)), partner_pop, confirmed=False)
    _update_pair_state(world, artist_name, partner_name, partner_is_artist, "dating", current_week, visibility)
    if partner_is_artist:
        _update_pair_state(world, partner_name, artist_name, True, "dating", current_week, visibility)
    event_type = "relationship_confirmed" if visibility in {"known", "tabloid"} and random.random() < 0.55 else "relationship_rumor"
    events.append(
        _record_romance_event(
            world,
            current_week,
            event_type,
            artist_name,
            partner_name,
            partner_is_artist,
            confirmed=event_type == "relationship_confirmed",
            visibility=visibility,
            rumor_confidence="growing" if event_type == "relationship_rumor" else "confirmed",
        )
    )
    return True


def _resolve_relationship_turn(
    world: EcosystemWorld,
    artist_name: str,
    current_week: int,
    processed_pairs: set[tuple[str, str]],
    events: list[RomanceEvent],
):
    profile = _get_romance_profile(world, artist_name)
    if profile is None or profile.status not in ROMANCE_ACTIVE_STATUSES or not profile.partner_name:
        return
    pair_key = _pair_key(artist_name, profile.partner_name if profile.partner_is_artist else f"hidden:{profile.partner_name}")
    if pair_key in processed_pairs:
        return
    processed_pairs.add(pair_key)

    partner_name = profile.partner_name
    partner_is_artist = profile.partner_is_artist
    partner_profile = _get_romance_profile(world, partner_name) if partner_is_artist else None
    profile.stability_score = _relationship_stability(world, artist_name, partner_name, partner_is_artist, profile)
    profile.scandal_pressure_score = _relationship_scandal_pressure(world, artist_name, partner_name, partner_is_artist)
    if partner_profile is not None:
        partner_profile.stability_score = profile.stability_score
        partner_profile.scandal_pressure_score = profile.scandal_pressure_score

    weeks_together = max(1, current_week - int(profile.relationship_start_week or current_week) + 1)
    high_profile = max(float(_ecosystem_artist_popularity(artist_name, world)), float(_romance_stats_for_partner(partner_name, partner_is_artist)[2])) >= 80.0

    if current_week in {49, 50, 51, 52} and profile.visibility != "private" and random.random() < 0.18:
        events.append(
            _record_romance_event(
                world,
                current_week,
                "award_show_couple",
                artist_name,
                partner_name,
                partner_is_artist,
                confirmed=True,
                visibility=profile.visibility,
            )
        )

    if profile.status == "dating" and profile.visibility == "private" and high_profile and random.random() < 0.12:
        events.append(
            _record_romance_event(
                world,
                current_week,
                "spotted_together",
                artist_name,
                partner_name,
                partner_is_artist,
                visibility="known",
                rumor_confidence="warm",
            )
        )
        profile.visibility = "known"
        if partner_profile is not None:
            partner_profile.visibility = "known"

    if profile.status == "dating" and weeks_together >= 10:
        engage_chance = max(0.0, ((profile.stability_score - 55.0) / 220.0) + ((_artist_lovingness(artist_name) + _romance_stats_for_partner(partner_name, partner_is_artist)[1]) / 900.0))
        if random.random() < engage_chance:
            visibility = _romance_visibility(float(_ecosystem_artist_popularity(artist_name, world)), float(_romance_stats_for_partner(partner_name, partner_is_artist)[2]), confirmed=True)
            _update_pair_state(world, artist_name, partner_name, partner_is_artist, "engaged", current_week, visibility)
            if partner_profile is not None:
                _update_pair_state(world, partner_name, artist_name, True, "engaged", current_week, visibility)
            events.append(_record_romance_event(world, current_week, "engagement", artist_name, partner_name, partner_is_artist, confirmed=True, visibility=visibility))
            return

    if profile.status == "engaged" and (current_week - int(profile.engagement_week or current_week)) >= 8:
        marriage_chance = max(0.0, ((profile.stability_score - 56.0) / 180.0) + ((_artist_lovingness(artist_name) - 45.0) / 500.0) - (profile.scandal_pressure_score / 650.0))
        if random.random() < marriage_chance:
            visibility = _romance_visibility(float(_ecosystem_artist_popularity(artist_name, world)), float(_romance_stats_for_partner(partner_name, partner_is_artist)[2]), confirmed=True)
            _update_pair_state(world, artist_name, partner_name, partner_is_artist, "married", current_week, visibility)
            if partner_profile is not None:
                _update_pair_state(world, partner_name, artist_name, True, "married", current_week, visibility)
            events.append(_record_romance_event(world, current_week, "marriage", artist_name, partner_name, partner_is_artist, confirmed=True, visibility=visibility))
            return

    cheating_risk = max(
        0.003,
        ((profile.scandal_pressure_score - 42.0) / 650.0)
        + ((_artist_aggression(artist_name) - 58.0) / 900.0)
        + ((48.0 - _artist_lovingness(artist_name)) / 900.0)
        + max(0.0, _ecosystem_artist_popularity(artist_name, world) - 78.0) / 1800.0,
    )
    if profile.status in {"dating", "engaged", "married"} and random.random() < cheating_risk:
        third_party_name = random.choice(HIDDEN_CHARACTER_SEEDS).name if random.random() < 0.7 else random.choice([seed.name for seed in ARTIST_ECOSYSTEM_SEEDS if seed.name not in {artist_name, partner_name}])
        confirmed = random.random() < 0.45
        event_type = "cheating_confirmed" if confirmed else "cheating_rumor"
        events.append(
            _record_romance_event(
                world,
                current_week,
                event_type,
                artist_name,
                partner_name,
                partner_is_artist,
                confirmed=confirmed,
                visibility="tabloid" if high_profile else "known",
                third_party_name=third_party_name,
                rumor_confidence="strong" if confirmed else "soft",
            )
        )
        profile.stability_score = clamp_meter(profile.stability_score - 24.0)
        if partner_profile is not None:
            partner_profile.stability_score = profile.stability_score
        if confirmed and partner_is_artist:
            _mark_artist_enemies(world, artist_name, partner_name)
        if confirmed and profile.status == "married":
            _update_pair_state(world, artist_name, partner_name, partner_is_artist, "separated", current_week, "tabloid" if high_profile else "known")
            if partner_profile is not None:
                _update_pair_state(world, partner_name, artist_name, True, "separated", current_week, "tabloid" if high_profile else "known")
            events.append(_record_romance_event(world, current_week, "separation", artist_name, partner_name, partner_is_artist, confirmed=True, visibility="tabloid" if high_profile else "known"))
            return
        if confirmed and profile.status in {"dating", "engaged"} and random.random() < 0.65:
            _clear_pair_state(world, artist_name, current_week)
            if partner_profile is not None:
                _clear_pair_state(world, partner_name, current_week)
                _mark_artist_enemies(world, artist_name, partner_name)
            events.append(_record_romance_event(world, current_week, "breakup", artist_name, partner_name, partner_is_artist, confirmed=True, visibility="tabloid" if high_profile else "known"))
            return

    breakup_risk = max(0.0, ((54.0 - profile.stability_score) / 220.0) + (profile.scandal_pressure_score / 1200.0))
    if profile.status == "dating" and weeks_together <= 6:
        breakup_risk *= 0.75
    elif profile.status == "engaged":
        breakup_risk *= 0.55
    elif profile.status == "married":
        breakup_risk *= 0.45
    if random.random() < breakup_risk:
        was_married = profile.status == "married"
        was_engaged = profile.status == "engaged"
        if was_married:
            _update_pair_state(world, artist_name, partner_name, partner_is_artist, "separated", current_week, profile.visibility)
            if partner_profile is not None:
                _update_pair_state(world, partner_name, artist_name, True, "separated", current_week, profile.visibility)
            events.append(_record_romance_event(world, current_week, "separation", artist_name, partner_name, partner_is_artist, confirmed=True, visibility=profile.visibility))
        else:
            _clear_pair_state(world, artist_name, current_week)
            if partner_profile is not None:
                _clear_pair_state(world, partner_name, current_week)
            if partner_is_artist and (_artist_aggression(artist_name) > 72 or _artist_aggression(partner_name) > 72 or was_engaged):
                _mark_artist_enemies(world, artist_name, partner_name)
            breakup_visibility = "tabloid" if profile.visibility == "tabloid" else "known"
            events.append(_record_romance_event(world, current_week, "breakup", artist_name, partner_name, partner_is_artist, confirmed=True, visibility=breakup_visibility))
        return

    if profile.status == "separated":
        divorce_risk = max(0.08, ((64.0 - profile.stability_score) / 105.0) + (profile.scandal_pressure_score / 650.0))
        if random.random() < divorce_risk and (current_week - int(profile.separation_week or current_week)) >= 6:
            _clear_pair_state(world, artist_name, current_week, divorced=True)
            profile.divorce_count += 1
            if partner_profile is not None:
                _clear_pair_state(world, partner_name, current_week, divorced=True)
                partner_profile.divorce_count += 1
                _mark_artist_enemies(world, artist_name, partner_name)
            events.append(_record_romance_event(world, current_week, "divorce", artist_name, partner_name, partner_is_artist, confirmed=True, visibility="tabloid" if high_profile else "known"))
            return
        if random.random() < 0.08:
            events.append(_record_romance_event(world, current_week, "reconciliation_rumor", artist_name, partner_name, partner_is_artist, visibility=profile.visibility, rumor_confidence="soft"))

    if profile.status == "dating" and profile.visibility == "private" and high_profile and random.random() < 0.05:
        profile.last_event_week = current_week
        events.append(_record_romance_event(world, current_week, "denial", artist_name, partner_name, partner_is_artist, visibility="known", rumor_confidence="soft"))

    if (
        profile.status in {"dating", "engaged"}
        and high_profile
        and _active_release_pressure(world, artist_name) > 0.6
        and (current_week - int(profile.last_event_week or 0)) >= 5
        and random.random() < 0.025
    ):
        profile.last_event_week = current_week
        events.append(_record_romance_event(world, current_week, "rollout_fallout", artist_name, partner_name, partner_is_artist, visibility=profile.visibility, rumor_confidence="warm"))

