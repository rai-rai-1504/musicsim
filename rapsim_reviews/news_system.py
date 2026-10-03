"""rapsim_reviews.news_system
News channels, controversies, feuds, diss battle coverage, and media reporting.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
from typing import TYPE_CHECKING
from uuid import uuid4

from rapsim_reviews.date_system import format_release_date, format_week_range
from rapsim_reviews.ui_helpers import (
    choose_from_list,
    meter_bar,
    money_fmt,
    prompt_int,
    prompt_text,
    clamp_meter,
    clamp_popularity,
    _stable_rng_for_label,
    weighted_choice,
    weighted_choice_from_pool,
)
from rapsim_reviews.critic_system import (
    CRITIC_NAMES,
    CRITIC_PROFILES,
    _critic_username,
    _expand_pool_dict,
    _expand_sentence_pool,
)
from rapsim_reviews.diss_track_system import (
    ensure_diss_state,
    is_hip_hop_artist,
    should_release_diss_track,
    release_diss_track,
    should_respond_to_diss,
    DISS_NEWS_TEMPLATES,
    schedule_verdict,
    build_scheduled_news,
)
from rapsim_reviews.track_review.base import Song
from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS

def _is_grammy_media_week(current_week: int) -> bool:
    return 49 <= (((int(current_week) - 1) % 52) + 1) <= 52

from rapsim_reviews.career_models import (
    Artist,
    SongEntry,
    AlbumEntry,
    RelationshipState,
    _apply_relationship_delta,
    _relationship_score,
    _player_week_index,
    _year_week_from_world_week,
    _ecosystem_seed_by_name,
    _ecosystem_artist_popularity,
    _ecosystem_artist_reputation,
    _find_world_runtime,
    _find_artist_any,
    _artist_display_name,
    _is_growing_artist_name,
    PLAYER_DEFAULT_CONTROVERSY,
    PLAYER_DEFAULT_BRUTALITY,
    CONTROVERSY_POPULARITY_CAP,
    CONTROVERSY_REPUTATION_CAP,
    MAX_BEEF_RESPONSES,
    MIN_BEEFS_PER_YEAR,
    MAX_BEEFS_PER_YEAR,
)
from rapsim_reviews.sales_system import (
    _player_release_sales_candidates,
    _ecosystem_release_sales_candidates,
)
from rapsim_reviews.artist_ecosystem_sim import weighted_choice

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld, WeeklyRelease, EcosystemArtistRuntime

NEWS_CHANNELS = {
    "general": {
        "name": "Pulsewire",
        "tagline": "industry desk",
        "personality": "fast, polished, and obsessed with the big picture",
        "reporters": ("Nia Brooks", "Calvin Reed", "Tessa Vale"),
    },
    "rumor": {
        "name": "WhisperWire",
        "tagline": "rumor desk",
        "personality": "tabloid, nosy, and always one source away from chaos",
        "reporters": ("Mara Quinn", "Jules Hart", "Rico Sloane"),
    },
    "relationship": {
        "name": "Heartline",
        "tagline": "love desk",
        "personality": "romantic, celebrity-focused, and shameless about chemistry",
        "reporters": ("Ava Lane", "Dani Flores", "Noor Bell"),
    },
    "growing": {
        "name": "Undercurrent",
        "tagline": "rising artist watch",
        "personality": "supportive, taste-making, and early on the next wave",
        "reporters": ("Micah Stone", "Skye Monroe", "Jun Park"),
    },
    "sales": {
        "name": "SoundScan Daily",
        "tagline": "sales desk",
        "personality": "numbers-first, dry in the best way, and trusted by labels",
        "reporters": ("Elliot Price", "Sana Mercer", "Victor Hale"),
    },
}


CONTROVERSY_MEDIUMS = [
    "song",
    "twitter",
    "interview",
    "alleged",
    "concert statement",
    "rumour",
    "confirmed sources",
]


MEDIUM_WEIGHTS = {
    "song": 5,
    "twitter": 30,
    "interview": 20,
    "alleged": 18,
    "concert statement": 12,
    "rumour": 10,
    "confirmed sources": 5,
}


def choose_medium(controversy_type: int, loop_count: int) -> str:
    pool = dict(MEDIUM_WEIGHTS)
    if loop_count > 0:
        pool.pop("song", None)
    if controversy_type in (1, 3):
        pool.pop("song", None)
    return weighted_choice(pool)


EXTERNAL_TARGETS = [
    "the government", "the music industry", "streaming platforms", "record labels",
    "his ex-partner", "her ex-partner", "a religious group", "a political party",
    "the press", "social media", "a sports organization", "a film studio",
    "a fashion brand", "a tech company", "a rival city", "his former label",
    "her former management", "the awards committee", "the radio industry",
    "a media personality", "a celebrity", "a billionaire", "a politician",
    "a journalist", "an activist group", "his family member", "her producer",
    "a business partner", "a podcast host", "a tv network",
]


TYPE_1_ACTIONS = [
    {"key": "hate_tweet", "template": "posted a series of tweets attacking {target}", "rep": -8, "pop": +6, "w": 12},
    {"key": "interview_attack", "template": 'called out {target} in a wide-ranging interview, saying they are "the root of everything wrong"', "rep": -5, "pop": +5, "w": 11},
    {"key": "stage_rant", "template": "went on a lengthy rant about {target} mid-concert, stopping the show entirely", "rep": -4, "pop": +7, "w": 10},
    {"key": "expose_post", "template": "posted alleged receipts exposing {target} on social media", "rep": -3, "pop": +8, "w": 9},
    {"key": "boycott_call", "template": "called on fans to boycott {target}, citing personal reasons", "rep": +3, "pop": +4, "w": 8},
    {"key": "public_apology", "template": "issued a public apology to {target} after a previous incident resurfaced", "rep": +6, "pop": +3, "w": 7},
    {"key": "cryptic_post", "template": "posted a cryptic message widely interpreted as a direct attack on {target}", "rep": -2, "pop": +4, "w": 7},
    {"key": "whistleblower", "template": "publicly exposed alleged wrongdoing by {target}, becoming a controversial whistleblower", "rep": +8, "pop": +6, "w": 4},
    {"key": "open_letter", "template": "published an open letter to {target} that went massively viral", "rep": +3, "pop": +6, "w": 4},
    {"key": "industry_speech", "template": "gave an industry speech directly calling out {target} for systemic failures", "rep": +5, "pop": +4, "w": 4},
]


TYPE_2_ACTIONS = [
    {"key": "diss_track", "template": 'took a direct shot at {target} on their new song "{song}"', "rep_i": -3, "pop_i": +8, "rep_t": -4, "pop_t": +7, "w": 10},
    {"key": "lyric_jab", "template": 'included a thinly veiled reference to {target} in "{song}" that fans decoded instantly', "rep_i": -2, "pop_i": +6, "rep_t": -2, "pop_t": +5, "w": 9},
    {"key": "bar_callout", "template": 'dedicated an entire verse to calling out {target} on their new release "{song}"', "rep_i": -2, "pop_i": +7, "rep_t": -5, "pop_t": +6, "w": 9},
    {"key": "hook_mention", "template": 'name-dropped {target} in the hook of "{song}" in what critics are calling a pointed attack', "rep_i": -1, "pop_i": +5, "rep_t": -3, "pop_t": +4, "w": 8},
    {"key": "twitter_beef", "template": "publicly called out {target} on Twitter, saying they lack talent and integrity", "rep_i": -4, "pop_i": +5, "rep_t": -3, "pop_t": +4, "w": 11},
    {"key": "interview_shot", "template": "took a shot at {target} in an interview, questioning their artistry", "rep_i": -3, "pop_i": +4, "rep_t": -3, "pop_t": +3, "w": 10},
    {"key": "subtweet_artist", "template": "appeared to subtweet {target} with a post that fans immediately connected", "rep_i": -2, "pop_i": +4, "rep_t": -2, "pop_t": +3, "w": 9},
    {"key": "stage_callout", "template": "called out {target} by name from the stage at a sold-out show", "rep_i": -3, "pop_i": +6, "rep_t": -4, "pop_t": +5, "w": 8},
    {"key": "ghostwrite_claim", "template": "alleged that {target} doesn't write their own music via a cryptic but clear post", "rep_i": -3, "pop_i": +7, "rep_t": -7, "pop_t": +5, "w": 6},
    {"key": "challenge", "template": "challenged {target} to a public battle and gave them 2 weeks to respond", "rep_i": -2, "pop_i": +7, "rep_t": -3, "pop_t": +5, "w": 5},
    {"key": "industry_plant", "template": "called {target} an industry plant with no organic fanbase in a viral post", "rep_i": -3, "pop_i": +5, "rep_t": -5, "pop_t": +4, "w": 4},
    {"key": "family_mention", "template": "made a pointed reference to {target}'s personal life in a way many called unacceptable", "rep_i": -7, "pop_i": +5, "rep_t": -5, "pop_t": +4, "w": 2},
]


TYPE_2_RESPONSE_ACTIONS = {
    1: [
        {"key": "response_1_twitter_thread", "template": "posted a forceful Twitter thread accusing {target} of misrepresenting the situation", "rep_i": -2, "pop_i": +5, "rep_t": -2, "pop_t": +4, "w": 10},
        {"key": "response_1_interview_clapback", "template": "used a radio interview to dismiss {target}'s claims as unserious", "rep_i": -2, "pop_i": +4, "rep_t": -2, "pop_t": +3, "w": 9},
        {"key": "response_1_livestream", "template": "went live to pick apart {target}'s claims line by line", "rep_i": -3, "pop_i": +5, "rep_t": -3, "pop_t": +4, "w": 8},
        {"key": "response_1_stage", "template": "answered from the stage, telling {target} to keep their name out of weak records", "rep_i": -3, "pop_i": +6, "rep_t": -3, "pop_t": +5, "w": 8},
    ],
    2: [
        {"key": "response_2_receipts", "template": "posted alleged receipts intended to challenge {target}'s account of the dispute", "rep_i": -3, "pop_i": +6, "rep_t": -4, "pop_t": +5, "w": 10},
        {"key": "response_2_interview_escalation", "template": "escalated the feud in an interview, saying {target} is not built for real pressure", "rep_i": -3, "pop_i": +5, "rep_t": -3, "pop_t": +4, "w": 9},
        {"key": "response_2_laugh_off", "template": "publicly dismissed {target}'s response as an attempt to control the narrative", "rep_i": -2, "pop_i": +5, "rep_t": -3, "pop_t": +4, "w": 8},
        {"key": "response_2_space", "template": "joined a live audio space and criticized {target}'s catalog at length", "rep_i": -4, "pop_i": +6, "rep_t": -4, "pop_t": +5, "w": 7},
    ],
    3: [
        {"key": "response_3_family_edge", "template": "crossed a new line by making the feud with {target} feel deeply personal", "rep_i": -5, "pop_i": +6, "rep_t": -4, "pop_t": +5, "w": 9},
        {"key": "response_3_ghostwriter", "template": "doubled down and said {target} has never been what fans think they are creatively", "rep_i": -4, "pop_i": +6, "rep_t": -5, "pop_t": +5, "w": 8},
        {"key": "response_3_full_meltdown", "template": "extended the feud with {target} across multiple public platforms", "rep_i": -6, "pop_i": +7, "rep_t": -4, "pop_t": +5, "w": 7},
        {"key": "response_3_challenge", "template": "dared {target} to respond again and said silence would count as surrender", "rep_i": -3, "pop_i": +7, "rep_t": -3, "pop_t": +5, "w": 8},
    ],
    4: [
        {"key": "response_4_nuclear_post", "template": "posted a lengthy statement intended to undercut {target}'s side of the story", "rep_i": -6, "pop_i": +7, "rep_t": -5, "pop_t": +5, "w": 9},
        {"key": "response_4_backstage_claim", "template": "made explosive backstage claims about {target} that immediately dominated timelines", "rep_i": -5, "pop_i": +7, "rep_t": -5, "pop_t": +5, "w": 8},
        {"key": "response_4_stream_rant", "template": "used a livestream to accuse {target} of relying on public relations spin", "rep_i": -5, "pop_i": +6, "rep_t": -4, "pop_t": +5, "w": 8},
        {"key": "response_4_direct_threat", "template": "made the feud with {target} feel dangerous after a chilling direct warning", "rep_i": -7, "pop_i": +6, "rep_t": -5, "pop_t": +5, "w": 5},
    ],
    5: [
        {"key": "response_5_final_word", "template": "delivered a final statement on {target}, framing it as the end of the dispute", "rep_i": -6, "pop_i": +8, "rep_t": -5, "pop_t": +6, "w": 10},
        {"key": "response_5_receipts_dump", "template": "ended the feud by unloading every last receipt they had on {target}", "rep_i": -5, "pop_i": +7, "rep_t": -5, "pop_t": +6, "w": 9},
        {"key": "response_5_last_interview", "template": "called this the last time they would speak on {target} while restating their criticism", "rep_i": -5, "pop_i": +7, "rep_t": -4, "pop_t": +5, "w": 8},
        {"key": "response_5_burn_bridge", "template": "ended the exchange with a closing statement that left little room for reconciliation with {target}", "rep_i": -6, "pop_i": +7, "rep_t": -5, "pop_t": +5, "w": 8},
    ],
}


TYPE_3_ACTIONS = [
    {"key": "twitter_critic", "template": "criticized {target} on Twitter after their review, questioning their credibility", "rep_i": -4, "pop_i": +4, "w": 12},
    {"key": "interview_critic", "template": "spent a full interview segment attacking {target}'s credibility as a reviewer", "rep_i": -3, "pop_i": +3, "w": 10},
    {"key": "review_clown", "template": "called {target}'s review embarrassing and demanded they retract it publicly", "rep_i": -2, "pop_i": +4, "w": 10},
    {"key": "bias_accusation", "template": "accused {target} of being paid off to give low scores to certain artists", "rep_i": -3, "pop_i": +5, "w": 7},
    {"key": "challenge_critic", "template": "challenged {target} to actually create music before reviewing it", "rep_i": -1, "pop_i": +4, "w": 8},
]


CRITIC_RESPONSES = [
    {"key": "double_down", "template": "{target} responded to the attack, saying their review stands and doubling down on every point", "rep_i_delta": -3, "pop_i_delta": +2, "w": 10},
    {"key": "clapback_short", "template": '{target} responded in two words: "review stands."', "rep_i_delta": -2, "pop_i_delta": +3, "w": 9},
    {"key": "full_essay", "template": "{target} published a lengthy essay responding to every claim made against them", "rep_i_delta": -3, "pop_i_delta": +3, "w": 7},
    {"key": "sympathy_shift", "template": "the public sided with {target} after the attack, creating a sympathy backlash against the artist", "rep_i_delta": -5, "pop_i_delta": -2, "w": 5},
    {"key": "silence", "template": "{target} has not responded publicly to the attack", "rep_i_delta": +1, "pop_i_delta": 0, "w": 8},
]


SONG_DELIVERY_KEYS = {"diss_track", "lyric_jab", "bar_callout", "hook_mention"}


HEADLINE_TEMPLATES = {
    "type1": [
        "{instigator} {action} via {medium}.",
        "{instigator} sparks controversy after they {action}.",
        "Fans react as {instigator} {action} on {medium}.",
    ],
    "type2_song": [
        '{instigator} fires shots at {target} on new track "{song}".',
        '"{song}" by {instigator} appears to be a direct response to {target}.',
        '{instigator} dedicates bars to {target} on latest release "{song}".',
    ],
    "type2_other": [
        "{instigator} {action} aimed at {target} via {medium}.",
        "Feud escalates as {instigator} {action} at {target}.",
        "{target} becomes the focus of {instigator}'s latest comments after the artist {action}.",
    ],
    "type2_response": [
        "Response #{loop}: {instigator} responds to {target}: {action}.",
        "Response #{loop}: {target}-{instigator} feud continues as {instigator} {action}.",
        "Response #{loop}: {instigator} {action} in ongoing feud with {target}.",
        "Escalation response #{loop}: {instigator} {action} in remarks aimed at {target}.",
    ],
    "type3": [
        "{instigator} lashes out at critic {target}: {action}.",
        "{instigator} {action} after {target}'s harsh review.",
        "Artist vs critic: {instigator} {action} targeting {target}.",
    ],
    "type3_critic_response": [
        "Critic {target} responds to {instigator}'s attack: {action}.",
        "{target} fires back at {instigator}: {action}.",
    ],
}

NEW_RELEASE_NEWS_TEMPLATES = {
    "return": [
        '{artist} returns after a long break with "{title}", a {release_type} arriving after more than six months away from releases.',
        'After {gap} weeks without new music, {artist} releases "{title}" and immediately draws industry attention.',
        '{artist} ends a lengthy release gap with "{title}", putting a spotlight back on their catalogue.',
    ],
    "major_project": [
        '{artist} releases new {release_type} "{title}", marking one of the week\'s major music stories.',
        'New {release_type} from {artist}: "{title}" arrives with {track_count} tracks and early review chatter.',
        '{artist} puts a full project into the market with "{title}", a {release_type} expected to shape the week.',
    ],
    "star_project": [
        'With popularity above 80, {artist} releases "{title}" and turns the drop into an immediate industry headline.',
        '{artist} uses major-star momentum to launch "{title}", a {release_type} drawing wide attention.',
        'A high-profile release week for {artist}: "{title}" arrives as their popularity sits near the top of the scene.',
    ],
}


NEWS_VARIANT_PREFIXES = []

NEWS_VARIANT_SUFFIXES = [
    "and the reaction was immediate.",
    "industry attention has followed.",
    "the response is expected to continue through the week.",
    "that is where the public conversation stands.",
    "observers say the remarks could have lasting fallout.",
    "the comments added new attention to the story.",
    "the exchange is now drawing broader coverage.",
    "the situation remains active.",
    "the statement changed the tone of the discussion.",
    "the response has kept the story in circulation.",
]


HEADLINE_TEMPLATES = _expand_pool_dict(
    HEADLINE_TEMPLATES,
    min_extra=10,
    max_extra=14,
    prefixes=NEWS_VARIANT_PREFIXES,
    suffixes=NEWS_VARIANT_SUFFIXES,
)

NEW_RELEASE_NEWS_TEMPLATES = _expand_pool_dict(
    NEW_RELEASE_NEWS_TEMPLATES,
    min_extra=10,
    max_extra=14,
    prefixes=NEWS_VARIANT_PREFIXES,
    suffixes=NEWS_VARIANT_SUFFIXES,
)



@dataclass
class ControversyEvent:
    id: str
    week: int
    controversy_type: int
    instigator: str
    target: str
    action_key: str
    medium: str
    rep_delta_instigator: float
    pop_delta_instigator: float
    rep_delta_target: float
    pop_delta_target: float
    song_title: str | None = None
    response_to_id: str | None = None
    loop_count: int = 0
    terminated: bool = False
    headline: str = ""


@dataclass
class NewsReport:
    id: str
    week: int
    report_type: str
    headline: str
    medium: str = "news"
    artist: str = ""
    target: str = ""
    subject: str = ""
    channel: str = ""
    reporter: str = ""


@dataclass
class NewsChannel:
    key: str
    name: str
    tagline: str
    personality: str
    reporters: tuple[str, ...]


class NewsModule:
    def __init__(self):
        self.weekly_headlines: dict[int, list[ControversyEvent]] = {}

    def add_events(self, week: int, events: list[ControversyEvent]):
        if events:
            self.weekly_headlines.setdefault(week, []).extend(events)

    def get_news(self, week: int) -> list[ControversyEvent]:
        return list(self.weekly_headlines.get(week, []))

    def get_all_news(self, last_n_weeks: int, current_week: int) -> list[tuple[int, ControversyEvent]]:
        result = []
        for w in range(max(0, current_week - last_n_weeks), current_week + 1):
            for event in self.weekly_headlines.get(w, []):
                result.append((w, event))
        return sorted(result, key=lambda item: (-item[0], item[1].headline))


def _pick_reporter(channel_key: str, stable_key: str) -> str:
    meta = _news_channel_meta(channel_key)
    reporters = list(meta.get("reporters", ()) or ("Staff Reporter",))
    if not reporters:
        return "Staff Reporter"
    rng = _stable_rng_for_label(f"reporter:{channel_key}:{stable_key}")
    return str(rng.choice(reporters))


def _ensure_news_state(world: EcosystemWorld | None):
    if world is not None and getattr(world, "news_module", None) is None:
        world.news_module = NewsModule()


def _news_channel_meta(key: str) -> dict:
    return NEWS_CHANNELS.get(key, NEWS_CHANNELS["general"])


def _channel_key_for_news_report(report_type: str, artist: str = "", subject: str = "", world: EcosystemWorld | None = None) -> str:
    report_type = str(report_type or "")
    subject = str(subject or "").lower()
    if "rumor" in report_type or "rumor" in subject:
        return "rumor"
    if report_type == "relationship":
        return "relationship"
    if report_type == "sales":
        return "sales"
    if report_type == "new_release" and artist and world is not None and _is_growing_artist_name(artist, world):
        return "growing"
    return "general"


def _event_channel_and_reporter(event, world: EcosystemWorld | None = None) -> tuple[str, str]:
    if isinstance(event, NewsReport):
        channel = str(event.channel or "")
        reporter = str(event.reporter or "")
        if channel and reporter:
            return channel, reporter
        key = _channel_key_for_news_report(event.report_type, event.artist, event.subject, world)
        return _news_channel_meta(key)["name"], _pick_reporter(key, str(getattr(event, "id", "")))
    if isinstance(event, ControversyEvent):
        if event.controversy_type == 2 and event.loop_count >= 4:
            key = "rumor"
        elif event.controversy_type == 2:
            key = "general"
        elif event.controversy_type == 1 and event.medium == "twitter":
            key = "rumor"
        else:
            key = "general"
        return _news_channel_meta(key)["name"], _pick_reporter(key, str(getattr(event, "id", "")))
    return _news_channel_meta("general")["name"], _pick_reporter("general", "fallback")


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


def _recent_controversy_load(world: EcosystemWorld, artist_name: str) -> float:
    history = world.controversy_history_by_artist.get(artist_name, [])
    recent = [event for event in history if (int(world.week_number) - int(getattr(event, "week", 0))) <= 10]
    return float(len(recent))


def _controversy_action_rep(event: ControversyEvent) -> float:
    if event.controversy_type != 1:
        return 0.0
    for action in TYPE_1_ACTIONS:
        if action["key"] == event.action_key:
            return float(action["rep"])
    return 0.0


def _artist_controversy_value(subject) -> float:
    if subject is None:
        return 0.0
    if isinstance(subject, Artist):
        return float(getattr(subject, "controversy", PLAYER_DEFAULT_CONTROVERSY))
    return float(getattr(subject.seed, "controversy", 25.0))


def _controversy_initiation_gate(subject) -> float:
    value = _artist_controversy_value(subject)
    if value > 60.0:
        return 0.80
    return 0.20


def _action_weight_value(action: dict) -> float:
    return float(action.get("w", 1.0))


def _action_impact_value(action: dict, controversy_type: int) -> float:
    if controversy_type == 1:
        return abs(float(action.get("rep", 0.0))) + abs(float(action.get("pop", 0.0)))
    if controversy_type == 2:
        return (
            abs(float(action.get("rep_i", 0.0)))
            + abs(float(action.get("pop_i", 0.0)))
            + abs(float(action.get("rep_t", 0.0)))
            + abs(float(action.get("pop_t", 0.0)))
        )
    return abs(float(action.get("rep_i", action.get("rep_i_delta", 0.0)))) + abs(
        float(action.get("pop_i", action.get("pop_i_delta", 0.0)))
    )


def _weighted_initial_action_pool(subject, base_pool: list[dict], controversy_type: int) -> list[dict]:
    controversy_value = _artist_controversy_value(subject)
    adjusted: list[dict] = []
    for action in base_pool:
        copy = dict(action)
        weight = float(copy.get("w", 1.0))
        impact = _action_impact_value(copy, controversy_type)
        if controversy_value > 75.0:
            if impact >= 14.0:
                weight *= 1.85
            elif impact >= 10.0:
                weight *= 1.45
            else:
                weight *= 0.90
        elif controversy_value > 60.0:
            if impact >= 10.0:
                weight *= 1.20
        else:
            if impact >= 14.0:
                weight *= 0.10
            elif impact >= 10.0:
                weight *= 0.25
            elif impact >= 7.0:
                weight *= 0.55
            else:
                weight *= 1.20
        copy["w"] = max(0.1, weight)
        adjusted.append(copy)
    return adjusted


def _artist_brutality_value(subject) -> float:
    if subject is None:
        return 0.0
    if isinstance(subject, Artist):
        return float(getattr(subject, "brutality", PLAYER_DEFAULT_BRUTALITY))
    return float(getattr(subject.seed, "aggression", 30.0))


def _artist_recent_low_reviews(subject, world: EcosystemWorld | None) -> list[dict]:
    if isinstance(subject, Artist):
        return subject.recent_low_reviews
    return world.recent_low_reviews_by_artist.setdefault(subject.seed.name, []) if world is not None else []


def _artist_pending_responses(subject, world: EcosystemWorld | None) -> list[dict]:
    if isinstance(subject, Artist):
        return subject.pending_responses
    return world.pending_responses_by_artist.setdefault(subject.seed.name, []) if world is not None else []


def _artist_controversy_history(subject, world: EcosystemWorld | None) -> list[ControversyEvent]:
    if isinstance(subject, Artist):
        return subject.controversy_history
    return world.controversy_history_by_artist.setdefault(subject.seed.name, []) if world is not None else []


def _artist_releases_this_week(subject, world: EcosystemWorld | None) -> list:
    if isinstance(subject, Artist):
        return subject.releases_this_week
    return world.releases_this_week_by_artist.setdefault(subject.seed.name, []) if world is not None else []


def _apply_popularity_delta_to_actor(name: str, delta: float, player_artist: Artist, world: EcosystemWorld | None):
    if name == player_artist.name:
        current_offset = float(getattr(player_artist, "controversy_popularity_offset", 0.0))
        new_offset = max(-CONTROVERSY_POPULARITY_CAP, min(CONTROVERSY_POPULARITY_CAP, current_offset + float(delta)))
        actual_delta = new_offset - current_offset
        player_artist.controversy_popularity_offset = new_offset
        player_artist.popularity_state.organic = clamp_popularity(player_artist.popularity_state.organic + actual_delta)
        return
    if world is not None:
        current_offset = float(world.artist_popularity_controversy_offset.get(name, 0.0))
        new_offset = max(-CONTROVERSY_POPULARITY_CAP, min(CONTROVERSY_POPULARITY_CAP, current_offset + float(delta)))
        actual_delta = new_offset - current_offset
        world.artist_popularity_controversy_offset[name] = new_offset
        current = _ecosystem_artist_popularity(name, world)
        world.artist_popularity[name] = clamp_popularity(current + actual_delta)


def _apply_reputation_delta_to_actor(name: str, delta: float, player_artist: Artist, world: EcosystemWorld | None):
    if name == player_artist.name:
        current_offset = float(getattr(player_artist, "controversy_reputation_offset", 0.0))
        new_offset = max(-CONTROVERSY_REPUTATION_CAP, min(CONTROVERSY_REPUTATION_CAP, current_offset + float(delta)))
        actual_delta = new_offset - current_offset
        player_artist.controversy_reputation_offset = new_offset
        player_artist.reputation = clamp_meter(player_artist.reputation + actual_delta)
        return
    if world is not None:
        current_offset = float(world.artist_reputation_controversy_offset.get(name, 0.0))
        new_offset = max(-CONTROVERSY_REPUTATION_CAP, min(CONTROVERSY_REPUTATION_CAP, current_offset + float(delta)))
        actual_delta = new_offset - current_offset
        world.artist_reputation_controversy_offset[name] = new_offset
        current = _ecosystem_artist_reputation(name, world)
        world.artist_reputation[name] = clamp_meter(current + actual_delta)


def _is_enemy_name(subject, target_name: str, player_artist: Artist, world: EcosystemWorld | None) -> bool:
    if isinstance(subject, Artist):
        return _relationship_score(player_artist, target_name) <= 20.0
    social = world.social_graph.get(subject.seed.name, {}) if world is not None else {}
    return target_name in social.get("enemies", [])


def _enemy_names_for_subject(subject, player_artist: Artist, world: EcosystemWorld | None) -> list[str]:
    if isinstance(subject, Artist):
        return [
            name for name, state in subject.relationships.items()
            if state.score <= 20.0
        ]
    social = world.social_graph.get(subject.seed.name, {}) if world is not None else {}
    return list(social.get("enemies", []))


def _friend_names_for_subject(subject, player_artist: Artist, world: EcosystemWorld | None) -> list[str]:
    if isinstance(subject, Artist):
        return [
            name for name, state in subject.relationships.items()
            if state.score >= 65.0
        ]
    social = world.social_graph.get(subject.seed.name, {}) if world is not None else {}
    return list(social.get("friends", []))


def _all_artist_names(player_artist: Artist, world: EcosystemWorld | None) -> list[str]:
    names = [player_artist.name]
    if world is not None:
        names.extend(runtime.seed.name for runtime in world.roster)
    return names


def _get_action_template(action_key: str, pool: list[dict]) -> str:
    for item in pool:
        if item["key"] == action_key:
            return str(item["template"])
    return "{target}"


def _choose_target_type2(subject, player_artist: Artist, world: EcosystemWorld | None) -> str | None:
    all_names = [
        name for name in _all_artist_names(player_artist, world)
        if name != _artist_display_name(subject) and name != player_artist.name
    ]
    if not all_names:
        return None
    enemies = _enemy_names_for_subject(subject, player_artist, world)
    controversy_value = _artist_controversy_value(subject)
    enemy_bias = 0.90 if controversy_value < 60.0 else 0.80
    if enemies and random.random() < enemy_bias:
        return random.choice(enemies)
    friends = set(_friend_names_for_subject(subject, player_artist, world))
    candidates = [name for name in all_names if name not in friends]
    if not candidates:
        candidates = all_names
    return random.choice(candidates)


def _should_trigger_controversy(subject, current_week: int, world: EcosystemWorld | None) -> bool:
    if not isinstance(subject, Artist) and _is_growing_artist_name(_artist_display_name(subject), world):
        return False
    base_prob = (_artist_controversy_value(subject) / 100.0) * 0.65
    if random.random() > base_prob:
        return False
    gate = 0.95 if _artist_controversy_value(subject) > 60.0 else 0.60
    if random.random() > gate:
        return False
    recent = [
        event for event in _artist_controversy_history(subject, world)
        if event.week >= current_week - 3 and event.loop_count == 0
    ]
    return not recent


def _recent_beef_start_count(world: EcosystemWorld | None, current_week: int) -> int:
    if world is None:
        return 0
    count = 0
    year_start = ((int(current_week) - 1) // 52) * 52 + 1
    for events in getattr(world, "weekly_events", {}).values():
        for event in events:
            if (
                isinstance(event, ControversyEvent)
                and event.controversy_type == 2
                and event.loop_count == 0
                and int(event.week) >= year_start
                and int(event.week) <= int(current_week)
            ):
                count += 1
    return count


def _annual_beef_target(world: EcosystemWorld | None, current_week: int) -> int:
    if world is None:
        return MAX_BEEFS_PER_YEAR
    year_index = max(1, ((int(current_week) - 1) // 52) + 1)
    if not hasattr(world, "_annual_beef_targets"):
        world._annual_beef_targets = {}
    targets = world._annual_beef_targets
    if year_index not in targets:
        rng = _stable_rng_for_label(f"annual-beef-target:{year_index}")
        targets[year_index] = int(rng.randint(MIN_BEEFS_PER_YEAR, MAX_BEEFS_PER_YEAR))
    return int(targets[year_index])


def _beef_budget_available(world: EcosystemWorld | None, current_week: int) -> bool:
    if world is None:
        return True
    target = _annual_beef_target(world, current_week)
    current_count = _recent_beef_start_count(world, current_week)
    if current_count >= target:
        return False
    week_in_year = ((int(current_week) - 1) % 52) + 1
    paced_limit = max(1, min(target, int(round((target * week_in_year) / 52.0 + 1.0))))
    return current_count < paced_limit


def _choose_controversy_type(subject, world: EcosystemWorld | None) -> int:
    weights = {1: 42, 2: 50, 3: 8}
    if not _artist_recent_low_reviews(subject, world):
        weights[3] = 0
    return int(weighted_choice(weights))


def _should_controversy_respond(target_subject, action_weight: float, loop_count: int) -> bool:
    if loop_count >= MAX_BEEF_RESPONSES:
        return False
    brutality_factor = _artist_brutality_value(target_subject) / 100.0
    weight_factor = min(0.26, max(0.04, float(action_weight) / 36.0))
    base = 0.24 + (brutality_factor * 0.58) + weight_factor
    if loop_count >= 2:
        base += 0.12
    if loop_count >= 4:
        base += 0.06
    return random.random() < max(0.20, min(0.95, base))


def _should_critic_respond() -> bool:
    return random.random() < 0.65


def _schedule_response(current_week: int) -> int:
    return current_week + 2


def _planned_beef_response_count() -> int:
    if random.random() < 0.55:
        return MAX_BEEF_RESPONSES
    return random.randint(1, MAX_BEEF_RESPONSES - 1)


def _find_controversy_event_by_id(event_id: str | None, player_artist: Artist, world: EcosystemWorld | None) -> ControversyEvent | None:
    if not event_id:
        return None
    for event in getattr(player_artist, "controversy_history", []):
        if isinstance(event, ControversyEvent) and event.id == event_id:
            return event
    if world is None:
        return None
    for events in getattr(world, "weekly_events", {}).values():
        for event in events:
            if isinstance(event, ControversyEvent) and event.id == event_id:
                return event
    for history in getattr(world, "controversy_history_by_artist", {}).values():
        for event in history:
            if isinstance(event, ControversyEvent) and event.id == event_id:
                return event
    return None


def _valid_pending_beef_response(
    response: dict,
    responder_name: str,
    response_loop: int,
    current_week: int,
    player_artist: Artist,
    world: EcosystemWorld | None,
) -> bool:
    previous = _find_controversy_event_by_id(response.get("response_to_id"), player_artist, world)
    if previous is None:
        return False
    if previous.controversy_type != 2:
        return False
    if int(previous.loop_count) != response_loop - 1:
        return False
    if int(previous.week) >= int(current_week):
        return False
    return previous.instigator == str(response.get("target")) and previous.target == responder_name


def _type2_action_pool(loop_count: int, allow_song: bool) -> list[dict]:
    if loop_count <= 0:
        if allow_song:
            return TYPE_2_ACTIONS
        return [item for item in TYPE_2_ACTIONS if item["key"] not in SONG_DELIVERY_KEYS]
    return list(TYPE_2_RESPONSE_ACTIONS.get(loop_count, TYPE_2_RESPONSE_ACTIONS[MAX_BEEF_RESPONSES]))


def _should_publish_news_event(event: ControversyEvent, player_artist: Artist, world: EcosystemWorld | None) -> bool:
    if event.instigator == player_artist.name or event.target == player_artist.name:
        return False
    if _is_growing_artist_name(event.instigator, world):
        return False
    if event.controversy_type in {2, 3} and _is_growing_artist_name(event.target, world):
        return False
    return True


def _build_type1_event(instigator_name: str, target: str, action: dict, week: int) -> ControversyEvent:
    medium = choose_medium(1, 0)
    event = ControversyEvent(
        id=str(uuid4()),
        week=week,
        controversy_type=1,
        instigator=instigator_name,
        target=target,
        action_key=action["key"],
        medium=medium,
        rep_delta_instigator=float(action["rep"]),
        pop_delta_instigator=float(action["pop"]),
        rep_delta_target=0.0,
        pop_delta_target=0.0,
    )
    event.headline = _generate_headline(event)
    return event


def _build_type2_event(instigator_name: str, target: str, action: dict, week: int, loop_count: int, song_title: str | None, response_to_id: str | None) -> ControversyEvent:
    medium = "song" if song_title else choose_medium(2, loop_count)
    event = ControversyEvent(
        id=str(uuid4()),
        week=week,
        controversy_type=2,
        instigator=instigator_name,
        target=target,
        action_key=action["key"],
        medium=medium,
        rep_delta_instigator=float(action["rep_i"]),
        pop_delta_instigator=float(action["pop_i"]),
        rep_delta_target=float(action["rep_t"]),
        pop_delta_target=float(action["pop_t"]),
        song_title=song_title,
        response_to_id=response_to_id,
        loop_count=loop_count,
        terminated=loop_count >= MAX_BEEF_RESPONSES,
    )
    event.headline = _generate_headline(event)
    return event


def _build_type3_event(instigator_name: str, critic_name: str, action: dict, week: int, response_to_id: str | None = None, is_critic_response: bool = False) -> ControversyEvent:
    event = ControversyEvent(
        id=str(uuid4()),
        week=week,
        controversy_type=3,
        instigator=instigator_name,
        target=critic_name,
        action_key=action["key"],
        medium=choose_medium(3, 0),
        rep_delta_instigator=float(action.get("rep_i", action.get("rep_i_delta", 0.0))),
        pop_delta_instigator=float(action.get("pop_i", action.get("pop_i_delta", 0.0))),
        rep_delta_target=0.0,
        pop_delta_target=0.0,
        response_to_id=response_to_id,
        loop_count=1 if is_critic_response else 0,
        terminated=is_critic_response,
    )
    event.headline = _generate_headline(event, critic_response=is_critic_response)
    return event


def _generate_headline(event: ControversyEvent, critic_response: bool = False) -> str:
    if event.controversy_type == 1:
        template = random.choice(HEADLINE_TEMPLATES["type1"])
        action_desc = _get_action_template(event.action_key, TYPE_1_ACTIONS)
        return template.format(instigator=event.instigator, action=action_desc.format(target=event.target), medium=event.medium, target=event.target)
    if event.controversy_type == 2:
        if event.song_title:
            template = random.choice(HEADLINE_TEMPLATES["type2_song"])
            return template.format(instigator=event.instigator, target=event.target, song=event.song_title)
        if event.loop_count > 0:
            template = random.choice(HEADLINE_TEMPLATES["type2_response"])
            action_desc = _get_action_template(event.action_key, _type2_action_pool(event.loop_count, allow_song=False))
            return template.format(instigator=event.instigator, target=event.target, action=action_desc.format(target=event.target), loop=event.loop_count)
        template = random.choice(HEADLINE_TEMPLATES["type2_other"])
        action_desc = _get_action_template(event.action_key, TYPE_2_ACTIONS)
        return template.format(instigator=event.instigator, target=event.target, action=action_desc.format(target=event.target), medium=event.medium)
    template_key = "type3_critic_response" if critic_response else "type3"
    template = random.choice(HEADLINE_TEMPLATES[template_key])
    source_pool = CRITIC_RESPONSES if critic_response else TYPE_3_ACTIONS
    action_desc = _get_action_template(event.action_key, source_pool)
    return template.format(instigator=event.instigator, target=event.target, action=action_desc.format(target=event.target))


def _apply_controversy_effects(event: ControversyEvent, player_artist: Artist, world: EcosystemWorld | None):
    _apply_reputation_delta_to_actor(event.instigator, event.rep_delta_instigator, player_artist, world)
    _apply_popularity_delta_to_actor(event.instigator, event.pop_delta_instigator, player_artist, world)
    if event.controversy_type == 2:
        _apply_reputation_delta_to_actor(event.target, event.rep_delta_target, player_artist, world)
        _apply_popularity_delta_to_actor(event.target, event.pop_delta_target, player_artist, world)
        if event.instigator == player_artist.name:
            _apply_relationship_delta(player_artist, event.target, -15.0)
        elif event.target == player_artist.name:
            _apply_relationship_delta(player_artist, event.instigator, -15.0)
        elif world is not None:
            social = world.social_graph.setdefault(event.instigator, {"friends": [], "enemies": []})
            if event.target not in social["enemies"]:
                social["enemies"].append(event.target)
            reverse = world.social_graph.setdefault(event.target, {"friends": [], "enemies": []})
            if event.instigator not in reverse["enemies"]:
                reverse["enemies"].append(event.instigator)


def _record_controversy_event(event: ControversyEvent, player_artist: Artist, world: EcosystemWorld | None):
    if event.instigator == player_artist.name:
        player_artist.controversy_history.append(event)
    elif world is not None:
        world.controversy_history_by_artist.setdefault(event.instigator, []).append(event)

    target_runtime = _find_world_runtime(world, event.target)
    if event.target == player_artist.name:
        player_artist.controversy_history.append(event)
    elif target_runtime is not None and event.controversy_type == 2:
        world.controversy_history_by_artist.setdefault(event.target, []).append(event)


def _recent_release_song_title(subject, world: EcosystemWorld | None) -> str | None:
    releases = _artist_releases_this_week(subject, world)
    if not releases:
        return None
    latest = releases[-1]
    if hasattr(latest, "song"):
        return str(latest.song.name)
    return str(getattr(latest, "title", "")) or None


def _record_ecosystem_low_reviews(world: EcosystemWorld | None):
    if world is None:
        return
    for release in list(getattr(world, "last_week_releases", []) or []):
        if float(getattr(release, "review", 10.0)) >= 5.5:
            continue
        critic_name = random.choice(CRITIC_NAMES)
        world.recent_low_reviews_by_artist.setdefault(release.artist_name, []).append(
            {
                "critic": critic_name,
                "score": float(release.review),
                "week": int(getattr(release, "week_number", world.week_number)),
                "song": str(getattr(release, "title", "")),
            }
        )
        world.recent_low_reviews_by_artist[release.artist_name] = world.recent_low_reviews_by_artist[release.artist_name][-20:]


def _build_news_report(
    week: int,
    report_type: str,
    headline: str,
    artist: str = "",
    target: str = "",
    subject: str = "",
    channel_key: str | None = None,
) -> NewsReport:
    channel_key = channel_key or _channel_key_for_news_report(report_type, artist, subject)
    return NewsReport(
        id=str(uuid4()),
        week=int(week),
        report_type=report_type,
        headline=headline,
        artist=artist,
        target=target,
        subject=subject,
        channel=str(_news_channel_meta(channel_key)["name"]),
        reporter=_pick_reporter(channel_key, f"{week}:{report_type}:{artist}:{subject}:{headline}"),
    )


def _release_track_count(release) -> int:
    return len(list(getattr(release, "tracks", ()) or ()))


def _release_gap_weeks(world: EcosystemWorld, artist_name: str, release_week: int) -> int | None:
    previous_weeks = [
        int(getattr(release, "week_number", 0))
        for release in world.release_history.get(artist_name, [])
        if int(getattr(release, "week_number", 0)) < int(release_week)
    ]
    if not previous_weeks:
        return None
    return int(release_week) - max(previous_weeks)


def _generate_new_release_news(world: EcosystemWorld | None, current_week: int) -> list[NewsReport]:
    if world is None:
        return []
    reports: list[NewsReport] = []
    for release in list(getattr(world, "last_week_releases", []) or []):
        artist_name = str(getattr(release, "artist_name", ""))
        growing = _is_growing_artist_name(artist_name, world)
        release_week = int(getattr(release, "week_number", current_week))
        release_type = str(getattr(release, "release_type", "single"))
        title = str(getattr(release, "title", "Untitled"))
        popularity = _ecosystem_artist_popularity(artist_name, world)
        gap = _release_gap_weeks(world, artist_name, release_week)
        major_project = release_type in {"album", "mixtape"}
        star_return = popularity > 80.0 and gap is not None and gap > 26
        if growing:
            headline = random.choice(
                [
                    '{artist} is building quiet momentum with "{title}". Undercurrent says keep an eye on this one.',
                    'rising artist {artist} drops "{title}" and the early listeners are already talking.',
                    '"{title}" puts {artist} back on the radar for anyone tracking the next wave.',
                    '{artist} just released "{title}" and the growth arc is getting harder to ignore.',
                ]
            ).format(
                artist=artist_name,
                title=title,
            )
            reports.append(_build_news_report(release_week, "new_release", headline, artist=artist_name, subject=title, channel_key="growing"))
            continue
        if not major_project and not star_return:
            continue
        if star_return and major_project:
            pool_key = "star_project"
        elif star_return:
            pool_key = "return"
        else:
            pool_key = "major_project"
        template = random.choice(NEW_RELEASE_NEWS_TEMPLATES[pool_key])
        headline = template.format(
            artist=artist_name,
            title=title,
            release_type=release_type,
            gap=gap or 0,
            track_count=_release_track_count(release),
        )
        reports.append(_build_news_report(release_week, "new_release", headline, artist=artist_name, subject=title))
    return reports


def _generate_sales_news_reports(player_artist: Artist, world: EcosystemWorld | None, current_week: int) -> list[NewsReport]:
    rows = _player_release_sales_candidates(player_artist) + _ecosystem_release_sales_candidates(world)
    rows = [row for row in rows if int(row["last_week_sales"]) > 0 or int(row["first_week_sales"]) > 0]
    if not rows:
        return []
    first_week_rows = [row for row in rows if int(row["release_week"]) == int(current_week) and int(row["first_week_sales"]) > 0]
    reports: list[NewsReport] = []
    if first_week_rows:
        top_first = max(first_week_rows, key=lambda row: (row["first_week_sales"], row["total_sales"]))
        reports.append(
            _build_news_report(
                current_week,
                "sales",
                random.choice(
                    [
                        '{artist} moves {sales:,} first-week units on "{title}".',
                        'SoundScan Daily has {artist} opening "{title}" with {sales:,} units in week one.',
                        '"{title}" starts with {sales:,} units for {artist}, according to early sales tracking.',
                    ]
                ).format(
                    artist=top_first["artist"],
                    title=top_first["title"],
                    sales=int(top_first["first_week_sales"]),
                ),
                artist=top_first["artist"],
                subject=top_first["title"],
            )
        )
    top_catalog = max(rows, key=lambda row: (row["last_week_sales"], row["total_sales"]))
    if int(top_catalog["last_week_sales"]) > 0:
        reports.append(
            _build_news_report(
                current_week,
                "sales",
                random.choice(
                    [
                        '{artist} posts {sales:,} units on "{title}" this week, with {total:,} total so far.',
                        'weekly sales watch: {artist} adds {sales:,} units to "{title}" and reaches {total:,} overall.',
                        '"{title}" keeps moving for {artist}: {sales:,} units this week, {total:,} in total.',
                    ]
                ).format(
                    artist=top_catalog["artist"],
                    title=top_catalog["title"],
                    sales=int(top_catalog["last_week_sales"]),
                    total=int(top_catalog["total_sales"]),
                ),
                artist=top_catalog["artist"],
                subject=top_catalog["title"],
            )
        )
    return reports[:2]


def _diss_actor(name: str, player_artist: Artist, world: EcosystemWorld | None):
    if name == player_artist.name:
        return SimpleNamespace(
            name=name, skills=player_artist.skills, genres=player_artist.genres,
            aggression=float(player_artist.brutality), battle_skills=int(player_artist.battle_skills),
            popularity=float(player_artist.popularity),
        )
    runtime = _find_world_runtime(world, name)
    if runtime is None:
        return None
    seed = runtime.seed
    return SimpleNamespace(
        name=seed.name, skills=seed.skills, genres=seed.genres,
        aggression=float(seed.aggression), battle_skills=int(getattr(seed, "battle_skills", 50)),
        popularity=float(_ecosystem_artist_popularity(seed.name, world)),
    )


def _add_diss_release_news(world: EcosystemWorld, track):
    headline = random.choice(DISS_NEWS_TEMPLATES["released"]).format(
        instigator=track.instigator, target=track.target, title=track.title,
    )
    world.news_module.add_events(
        track.week_released,
        [_build_news_report(track.week_released, "diss_release", headline, track.instigator, track.target, track.title)],
    )


def _register_diss_as_release(player_artist: Artist, world: EcosystemWorld, track) -> None:
    release_id = f"diss:{track.id}"
    song_id = f"diss-song:{track.id}"
    if track.instigator == player_artist.name:
        if any(getattr(entry, "source_label", "") == f"Diss: {track.target}" and entry.song.name == track.title for entry in player_artist.singles):
            return
        song = Song(
            float(track.quality),
            track.title,
            ["hip hop"],
            "rage",
            180,
            catchiness=float(track.catchiness),
            virality=float(track.virality),
            maturity_weeks=int(track.maturity_weeks),
        )
        player_artist.singles.append(
            SongEntry(
                song=song,
                released=True,
                average_review=float(track.critic_score),
                source_label=f"Diss: {track.target}",
                total_streams=int(track.total_streams),
                last_week_streams=int(track.last_week_streams),
                release_popularity_value=0.0,
                release_popularity_weeks_left=0,
                weeks_since_release=0,
                producer=track.producer,
                engineer=track.engineer,
                virality_triggered=bool(track.virality_triggered),
                virality_weeks_active=int(track.virality_weeks_active),
                virality_max_weekly_bonus=int(track.virality_max_weekly_bonus),
                virality_baseline_streams=int(track.virality_baseline_streams),
                release_week_index=int(track.week_released),
            )
        )
        return

    if any(str(getattr(release, "release_id", "")) == release_id for release in world.release_history.get(track.instigator, [])):
        return
    release = WeeklyRelease(
        release_id=release_id,
        artist_name=track.instigator,
        release_type="single",
        title=track.title,
        genre="hip hop",
        theme="rage",
        review=float(track.reception_score),
        week_number=int(track.week_released),
        quality=float(track.quality),
        tracks=(
            ProjectTrack(
                song_id=song_id,
                title=track.title,
                genre="hip hop",
                theme="rage",
                quality=float(track.quality),
                review=float(track.reception_score),
                lyricists=(track.instigator,),
                vocalists=(track.instigator,),
                producers=tuple([track.producer] if track.producer else ()),
                engineers=tuple([track.engineer] if track.engineer else ()),
            ),
        ),
    )
    world.release_history.setdefault(track.instigator, []).append(release)
    if int(world.week_number) == int(track.week_released):
        world.last_week_releases.append(release)
    if song_id not in world.song_runtime:
        world.song_runtime[song_id] = EcosystemSongRuntime(
            song_id=song_id,
            artist_name=track.instigator,
            title=track.title,
            genre="hip hop",
            theme="rage",
            quality=float(track.quality),
            review=float(track.reception_score),
            release_week=int(track.week_released),
            catchiness=float(track.catchiness),
            virality=float(track.virality),
            maturity_weeks=int(track.maturity_weeks),
            weeks_since_release=max(0, int(world.week_number) - int(track.week_released)),
            total_streams=int(track.total_streams),
            last_week_streams=int(track.last_week_streams),
            virality_triggered=bool(track.virality_triggered),
            virality_weeks_active=int(track.virality_weeks_active),
            virality_max_weekly_bonus=int(track.virality_max_weekly_bonus),
            virality_baseline_streams=int(track.virality_baseline_streams),
            producers=tuple([track.producer] if track.producer else ()),
            engineers=tuple([track.engineer] if track.engineer else ()),
            project_label="Diss Track",
        )
        world.songs_by_artist.setdefault(track.instigator, []).append(song_id)


def _sync_diss_runtime_streams(world: EcosystemWorld | None) -> None:
    if world is None:
        return
    ensure_diss_state(world)
    for track in world.diss_tracks:
        song_id = f"diss-song:{track.id}"
        runtime_song = world.song_runtime.get(song_id)
        if runtime_song is None:
            continue
        runtime_song.review = float(track.reception_score)
        runtime_song.last_week_streams = int(track.last_week_streams)
        runtime_song.total_streams = int(track.total_streams)
        runtime_song.weeks_since_release = max(0, int(world.week_number) - int(track.week_released))
        runtime_song.virality = float(track.virality)
        runtime_song.maturity_weeks = int(track.maturity_weeks)
        runtime_song.virality_triggered = bool(track.virality_triggered)
        runtime_song.virality_weeks_active = int(track.virality_weeks_active)
        runtime_song.virality_max_weekly_bonus = int(track.virality_max_weekly_bonus)
        runtime_song.virality_baseline_streams = int(track.virality_baseline_streams)


def _release_diss_and_schedule_reply(player_artist: Artist, world: EcosystemWorld, instigator_name: str, target_name: str, current_week: int, diss_number: int, battle_id: str | None = None):
    instigator = _diss_actor(instigator_name, player_artist, world)
    target = _diss_actor(target_name, player_artist, world)
    if instigator is None or target is None:
        return None
    track = release_diss_track(world, instigator, target, current_week, diss_number, ARTIST_ECOSYSTEM_SEEDS, battle_id=battle_id)
    _register_diss_as_release(player_artist, world, track)
    _add_diss_release_news(world, track)
    true_ratio = len(track.true_claims) / max(1, len(track.claims))
    _apply_reputation_delta_to_actor(instigator_name, (track.reception_score - 5.0) * 1.2, player_artist, world)
    _apply_popularity_delta_to_actor(instigator_name, track.brutality * .4 + true_ratio * 2.0, player_artist, world)
    _apply_reputation_delta_to_actor(target_name, -(len(track.false_claims) * .5) - track.reception_score * .3, player_artist, world)
    _apply_popularity_delta_to_actor(target_name, track.brutality * .3, player_artist, world)
    if diss_number < 5 and should_respond_to_diss(target, instigator):
        response_week = current_week + random.randint(2, 3)
        world.pending_diss_responses.append({
            "instigator": target_name,
            "target": instigator_name,
            "diss_number": diss_number + 1,
            "target_week": response_week,
            "battle_id": track.battle_id,
        })
        world.diss_tweet_schedule.setdefault(response_week - 1, []).append(("pre_response", (target_name, track.id)))
    else:
        no_response = random.choice(DISS_NEWS_TEMPLATES["no_response"]).format(
            target=target_name, instigator=instigator_name, title=track.title, round=diss_number,
        )
        world.news_module.add_events(
            current_week + 1,
            [_build_news_report(current_week + 1, "diss_no_response", no_response, instigator_name, target_name, track.title)],
        )
        schedule_verdict(world, track, current_week)
    return track


def _process_diss_battles(player_artist: Artist, world: EcosystemWorld | None, current_week: int, controversy_events: list[ControversyEvent]):
    if world is None:
        return
    ensure_diss_state(world)
    due = [item for item in world.pending_diss_responses if int(item.get("target_week", -1)) == current_week]
    world.pending_diss_responses = [item for item in world.pending_diss_responses if int(item.get("target_week", -1)) != current_week]
    for response in due:
        _release_diss_and_schedule_reply(
            player_artist, world, str(response["instigator"]), str(response["target"]),
            current_week, int(response["diss_number"]), battle_id=response.get("battle_id"),
        )

    year_start = ((int(current_week) - 1) // 52) * 52 + 1

    def _artist_diss_battle_count(name: str) -> int:
        battle_ids = {
            str(track.battle_id)
            for track in world.diss_tracks
            if int(track.week_released) >= year_start
            and int(track.week_released) <= int(current_week)
            and name in {track.instigator, track.target}
        }
        return len(battle_ids)

    for event in controversy_events:
        if event.controversy_type != 2 or int(event.loop_count) < 5:
            continue
        instigator = _diss_actor(event.instigator, player_artist, world)
        target = _diss_actor(event.target, player_artist, world)
        if (
            instigator is None
            or target is None
            or not is_hip_hop_artist(target)
            or not should_release_diss_track(instigator, int(event.loop_count))
        ):
            continue
        if _artist_diss_battle_count(event.instigator) >= 2 or _artist_diss_battle_count(event.target) >= 2:
            continue
        if any(
            {track.instigator, track.target} == {event.instigator, event.target}
            and int(track.week_released) >= int(current_week) - 51
            for track in world.diss_tracks
        ):
            continue
        _release_diss_and_schedule_reply(player_artist, world, event.instigator, event.target, current_week, 1)


def _process_scheduled_diss_news(world: EcosystemWorld | None, current_week: int):
    if world is None:
        return
    ensure_diss_state(world)
    reports = build_scheduled_news(world, current_week, _build_news_report)
    if reports:
        world.news_module.add_events(current_week, reports)


def _simulate_controversies(player_artist: Artist, world: EcosystemWorld | None, current_week: int) -> list[ControversyEvent]:
    _ensure_news_state(world)
    new_events: list[ControversyEvent] = []
    subjects = list(world.roster) if world is not None else []

    for subject in subjects:
        pending = _artist_pending_responses(subject, world)
        due = [item for item in pending if int(item.get("target_week", -1)) == current_week]
        for response in due:
            instigator_name = _artist_display_name(subject)
            if int(response.get("controversy_type", 0)) == 2:
                response_loop = int(response.get("loop_count", 1))
                if (
                    response_loop < 1
                    or response_loop > MAX_BEEF_RESPONSES
                    or not _valid_pending_beef_response(response, instigator_name, response_loop, current_week, player_artist, world)
                ):
                    continue
                pool = _type2_action_pool(response_loop, allow_song=False)
                action = weighted_choice_from_pool(pool)
                event = _build_type2_event(
                    instigator_name=instigator_name,
                    target=str(response["target"]),
                    action=action,
                    week=current_week,
                    loop_count=response_loop,
                    song_title=None,
                    response_to_id=response.get("response_to_id"),
                )
                new_events.append(event)
                target_subject = _find_artist_any(str(response["target"]), player_artist, world)
                max_response_loop = int(response.get("max_response_loop", _planned_beef_response_count()))
                max_response_loop = max(1, min(MAX_BEEF_RESPONSES, max_response_loop))
                if (
                    target_subject is not None
                    and str(response["target"]) != player_artist.name
                    and response_loop < max_response_loop
                ):
                    _artist_pending_responses(target_subject, world).append(
                        {
                            "target": instigator_name,
                            "controversy_type": 2,
                            "loop_count": response_loop + 1,
                            "target_week": _schedule_response(current_week),
                            "response_to_id": event.id,
                            "max_response_loop": max_response_loop,
                        }
                    )
            elif int(response.get("controversy_type", 0)) == 3:
                action = weighted_choice_from_pool(CRITIC_RESPONSES)
                event = _build_type3_event(
                    instigator_name=instigator_name,
                    critic_name=str(response["target"]),
                    action=action,
                    week=current_week,
                    response_to_id=response.get("response_to_id"),
                    is_critic_response=True,
                )
                new_events.append(event)
        remaining = [item for item in pending if int(item.get("target_week", -1)) != current_week]
        pending.clear()
        pending.extend(remaining)

    for subject in subjects:
        if not _should_trigger_controversy(subject, current_week, world):
            continue
        ctype = _choose_controversy_type(subject, world)
        instigator_name = _artist_display_name(subject)

        if ctype == 1:
            target = random.choice(EXTERNAL_TARGETS)
            event = _build_type1_event(
                instigator_name,
                target,
                weighted_choice_from_pool(_weighted_initial_action_pool(subject, TYPE_1_ACTIONS, 1)),
                current_week,
            )
            new_events.append(event)
            continue

        if ctype == 2:
            if not _beef_budget_available(world, current_week):
                continue
            target_name = _choose_target_type2(subject, player_artist, world)
            if not target_name:
                continue
            if _is_growing_artist_name(target_name, world):
                continue
            song_title = _recent_release_song_title(subject, world)
            pool = _weighted_initial_action_pool(subject, _type2_action_pool(0, allow_song=bool(song_title)), 2)
            action = weighted_choice_from_pool(pool)
            if action["key"] in SONG_DELIVERY_KEYS and not song_title:
                action = weighted_choice_from_pool(_weighted_initial_action_pool(subject, _type2_action_pool(0, allow_song=False), 2))
            event = _build_type2_event(instigator_name, target_name, action, current_week, 0, song_title if action["key"] in SONG_DELIVERY_KEYS else None, None)
            new_events.append(event)
            target_subject = _find_artist_any(target_name, player_artist, world)
            if target_subject is not None and target_name != player_artist.name and _should_controversy_respond(target_subject, _action_weight_value(action), 0):
                _artist_pending_responses(target_subject, world).append(
                    {
                        "target": instigator_name,
                        "controversy_type": 2,
                        "loop_count": 1,
                        "target_week": _schedule_response(current_week),
                        "response_to_id": event.id,
                        "max_response_loop": _planned_beef_response_count(),
                    }
                )
            continue

        recent = _artist_recent_low_reviews(subject, world)
        if not recent:
            continue
        low_review = random.choice(recent[-5:])
        action = weighted_choice_from_pool(_weighted_initial_action_pool(subject, TYPE_3_ACTIONS, 3))
        event = _build_type3_event(instigator_name, str(low_review["critic"]), action, current_week)
        new_events.append(event)
        if _should_critic_respond():
            _artist_pending_responses(subject, world).append(
                {
                    "target": str(low_review["critic"]),
                    "controversy_type": 3,
                    "target_week": current_week + 2,
                    "response_to_id": event.id,
                }
            )

    for event in new_events:
        _apply_controversy_effects(event, player_artist, world)
        _record_controversy_event(event, player_artist, world)
    if world is not None:
        world.weekly_events[current_week] = list(new_events)
        if world.news_module is not None:
            publishable_events = [event for event in new_events if _should_publish_news_event(event, player_artist, world)]
            if _is_grammy_media_week(current_week) and len(publishable_events) > 1:
                publishable_events = random.sample(publishable_events, 1)
            world.news_module.add_events(
                current_week,
                publishable_events,
            )
        _process_diss_battles(player_artist, world, current_week, new_events)
    return new_events


def _news_type_label(event: ControversyEvent):
    if isinstance(event, NewsReport):
        if event.report_type == "new_release":
            return "RELEASE"
        if event.report_type == "grammy":
            return "GRAMMYS"
        if event.report_type.startswith("diss_"):
            return "DISS TRACK"
        return "NEWS"
    if event.controversy_type == 1:
        return "EXTERNAL"
    if event.controversy_type == 3:
        return "CRITIC WAR"
    if event.loop_count > 0:
        return "RESPONSE"
    return "BEEF"


def _news_player_border(event: ControversyEvent, player_artist: Artist):
    if isinstance(event, NewsReport):
        if event.artist == player_artist.name or event.target == player_artist.name:
            return "#AFA9EC"
        return "#6B7280"
    if event.target == player_artist.name:
        return "#F87171"
    if event.instigator == player_artist.name:
        return "#AFA9EC"
    return "#6B7280"


def _print_news_card(event: ControversyEvent, player_artist: Artist):
    type_label = _news_type_label(event)
    medium = str(event.medium).upper()
    border = _news_player_border(event, player_artist)
    channel, reporter = _event_channel_and_reporter(event)
    week_str = format_week_range(event.week)
    print("+" + "-" * 72 + "+")
    print(f"| [{type_label:<10}] [{medium:<17}] {week_str:<36}|")
    print(f"| Border {border:<61}|")
    print(f"| Source {channel:<20} Reporter {reporter:<28}|")
    if isinstance(event, ControversyEvent) and event.controversy_type == 2 and event.loop_count > 0:
        print(f"| Response #{event.loop_count:<62}|")
    print("|" + " " * 72 + "|")
    words = event.headline.split()
    line = "|  "
    for word in words:
        if len(line) + len(word) + 1 > 73:
            print(line.ljust(73) + "|")
            line = "|  " + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line.ljust(73) + "|")
    if isinstance(event, ControversyEvent) and (event.instigator == player_artist.name or event.target == player_artist.name):
        delta = (
            f"{event.rep_delta_instigator:+.0f} rep / {event.pop_delta_instigator:+.0f} pop"
            if event.instigator == player_artist.name
            else f"{event.rep_delta_target:+.0f} rep / {event.pop_delta_target:+.0f} pop"
        )
        print("|" + " " * 72 + "|")
        print(f"|  Player impact: {delta:<54}|")
    print("+" + "-" * 72 + "+")


def news_menu(player_artist: Artist, world: EcosystemWorld | None):
    _ensure_news_state(world)
    current_week = _player_week_index(player_artist)
    news_module = world.news_module if world is not None else NewsModule()
    while True:
        choice = choose_from_list("INDUSTRY NEWS", ["This Week", "Archive", "Back"], allow_cancel=False)
        if choice == 2:
            return
        if choice == 0:
            print(f"\nINDUSTRY NEWS | {format_week_range(current_week)}")
            events = news_module.get_news(current_week)
            if not events:
                print("No headlines this week.")
                continue
            for event in events:
                _print_news_card(event, player_artist)
            input("\nPress Enter to go back...")
            continue

        search = prompt_text("Filter by artist name / type / medium (blank = all): ", "").strip().lower()
        events = news_module.get_all_news(260, current_week)
        filtered = []
        for week, event in events:
            channel, reporter = _event_channel_and_reporter(event)
            haystack = " ".join([
                getattr(event, "instigator", getattr(event, "artist", "")).lower(),
                getattr(event, "target", "").lower(),
                event.medium.lower(),
                _news_type_label(event).lower(),
                channel.lower(),
                reporter.lower(),
                event.headline.lower(),
            ])
            if search and search not in haystack:
                continue
            filtered.append((week, event))
        if not filtered:
            print("No archived headlines matched that filter.")
            continue
        for _, event in filtered[:50]:
            _print_news_card(event, player_artist)
        input("\nPress Enter to go back...")

