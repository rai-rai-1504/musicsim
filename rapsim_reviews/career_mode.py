"""Career mode that connects artist skills to the existing review engines."""

import math
import random
from dataclasses import dataclass, field
from types import SimpleNamespace
from uuid import uuid4

from rapsim_reviews.album_review import Album, AlbumSimulation, MIN_SONGS
from rapsim_reviews.artist_ecosystem_seed import (
    ARTIST_BASE_REPUTATION,
    ARTIST_ECOSYSTEM_SEEDS,
    ARTIST_FEATURE_TURNAROUND,
    ARTIST_LOVINGNESS,
    ARTIST_ROMANCE_PREFERENCES,
)
from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld, create_world, prepare_release_calendar, step_world
from rapsim_reviews.artist_ecosystem_sim import apply_feature_to_pending_release
from rapsim_reviews.artist_ecosystem_sim import classify_artist_skills
from rapsim_reviews.artist_ecosystem_sim import EcosystemSongRuntime, ProjectTrack, WeeklyRelease
from rapsim_reviews.diss_track_system import (
    DISS_NEWS_TEMPLATES,
    build_scheduled_news,
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
from rapsim_reviews.hidden_character_seeds import (
    HIDDEN_CHARACTER_BY_NAME,
    HIDDEN_CHARACTER_ROMANCE_PREFERENCES,
    HIDDEN_CHARACTER_SEEDS,
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
from rapsim_reviews.live_module import go_live
from rapsim_reviews.concert_system import ConcertBooking, concerts_menu, run_concert, VENUES, DEFAULT_PRICE_TEMPLATES
from rapsim_reviews.track_review import GENRES, THEMES, Simulation, Song

SKILLS = ["lyrics", "vocals", "production", "mix/master"]
BASE_WEEKLY_RECOVERY = 50.0
LIVE_WEEKLY_POP_CAP = 6.0
NEGOTIATION_WALK_AWAY_BUFFER = 14.0
FEATURE_DEADLINE_WEEKS = 4
TEST_RELATIONSHIP_BOOTSTRAP = True
TEST_RELATIONSHIP_LOCK = True
TEST_START_MAXED = True
TEST_START_MONEY = 100_000_000.0
TEST_START_POPULARITY = 80.0
PLAYER_DEFAULT_CONTROVERSY = 35.0
PLAYER_DEFAULT_BRUTALITY = 45.0
CONTROVERSY_POPULARITY_CAP = 5.0
CONTROVERSY_REPUTATION_CAP = 15.0
MAX_BEEF_RESPONSES = 5
MIN_BEEFS_PER_YEAR = 24
MAX_BEEFS_PER_YEAR = 32
VALID_GENDERS = ("male", "female", "non-binary")
VALID_SEXUALITIES = ("straight", "gay", "lesbian", "bisexual")
SEXUALITY_OPTIONS_BY_GENDER = {
    "male": ("straight", "gay", "bisexual"),
    "female": ("straight", "lesbian", "bisexual"),
    "non-binary": ("straight", "gay", "lesbian", "bisexual"),
}
ROMANCE_ACTIVE_STATUSES = {"dating", "engaged", "married", "separated"}
ROMANCE_PUBLIC_VISIBILITY = ("private", "known", "tabloid")
ROMANCE_STATUS_LABELS = {
    "single": "single",
    "dating": "dating",
    "engaged": "engaged",
    "married": "married",
    "separated": "separated",
    "divorced": "divorced",
}
PHYSICAL_UNIT_COSTS = {"disc": 20.0, "vinyl": 65.0}
PHYSICAL_BULK_DISCOUNTS = (
    (100_000, 0.20),
    (25_000, 0.15),
    (5_000, 0.10),
    (1_000, 0.05),
)
PHYSICAL_LIMITED_COST_MULT = 2.0
PHYSICAL_LIMITED_DEMAND_MULT = 1.60
PHYSICAL_BASE_PRICES = {
    ("single", "disc"): 24.99,
    ("single", "vinyl"): 79.99,
    ("album", "disc"): 39.99,
    ("album", "vinyl"): 109.99,
    ("deluxe", "disc"): 44.99,
    ("deluxe", "vinyl"): 124.99,
    ("mixtape", "disc"): 34.99,
    ("mixtape", "vinyl"): 99.99,
}
RIAA_CERTIFICATIONS = [
    (10_000_000, "Diamond"),
    (6_000_000, "6x Platinum"),
    (5_000_000, "5x Platinum"),
    (4_000_000, "4x Platinum"),
    (3_000_000, "3x Platinum"),
    (2_000_000, "2x Platinum"),
    (1_000_000, "Platinum"),
    (500_000, "Gold"),
]
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


@dataclass(frozen=True)
class CriticProfile:
    name: str
    username: str
    gender: str
    sexuality: str
    romance_preference: str


CRITIC_PROFILES = [
    CriticProfile("Marcus Vane", "@marcusvane", "male", "straight", "prefers_female"),
    CriticProfile("Deja Hayes", "@dejahayes", "female", "bisexual", "prefers_both"),
    CriticProfile("Vic Osei", "@vicosei", "male", "gay", "prefers_male"),
    CriticProfile("Ray Coldwell", "@raycoldwell", "male", "straight", "prefers_female"),
    CriticProfile("Earl Mosely", "@earlmosely", "male", "bisexual", "prefers_both"),
    CriticProfile("Zara Nights", "@zaranights", "female", "straight", "prefers_male"),
    CriticProfile("Tobias Lund", "@tobiaslund", "male", "straight", "prefers_female"),
    CriticProfile("Nina Pascal", "@ninapascal", "female", "lesbian", "prefers_female"),
    CriticProfile("Teena Naruka", "@teenaruka", "female", "bisexual", "prefers_both"),
    CriticProfile("Shatam Rai", "@shatamrai", "male", "straight", "prefers_female"),
]
CRITIC_NAMES = [critic.name for critic in CRITIC_PROFILES]
CRITIC_PROFILE_BY_NAME = {critic.name: critic for critic in CRITIC_PROFILES}

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

GRAMMY_NEWS_TEMPLATES = {
    "nominations": [
        'This year\'s Grammy nominations are out, with "{title}" by {artist} setting the tone in {category}.',
        'The Grammy field is set, and {artist} lands a major nomination for "{title}" in {category}.',
        'Nominations day puts {category} in focus as {artist} earns a place for "{title}".',
        '{artist} enters the Grammy conversation with "{title}", one of the key nominees in {category}.',
        'The {category} slate is already drawing debate, led by {artist}\'s "{title}".',
        'This year\'s Grammy shortlist gives {artist} a prominent spot in {category} for "{title}".',
    ],
    "nomination_roundup": [
        'This year\'s Grammy nominations are out, with {artist}\'s "{title}" setting the pace across the major album categories.',
        'The Grammy field is set, and the early story is {artist} leading a crowded race with "{title}".',
        'Nominations day brings a wide-open Grammy slate, with "{title}" by {artist} emerging as one of the headline projects.',
    ],
    "nomination_snub": [
        'The first debate after nominations day centers on {category}, where {artist}\'s "{title}" made the cut and several fan favorites did not.',
        'Grammy nomination reactions are already split over {category}, especially after {artist} secured a nod for "{title}".',
        'Award watchers are arguing over the {category} field after {artist} landed a nomination for "{title}".',
    ],
    "nomination_insider": [
        'Insiders say {artist}\'s nomination for "{title}" in {category} was stronger inside voting circles than the public expected.',
        'People close to the process say {category} came down to tight margins, with {artist}\'s "{title}" making a late surge.',
        'Behind the scenes, {artist}\'s "{title}" was reportedly one of the harder Grammy nominations for voters to ignore.',
    ],
    "winner": [
        'Grammy winners announced: {artist} wins {category} for "{title}".',
        '{artist} takes home {category} at this year\'s Grammys with "{title}".',
        'This year\'s Grammy for {category} goes to {artist} for "{title}".',
        'Grammy night delivers a major win for {artist}, whose "{title}" claims {category}.',
        '{artist} leaves Grammy night with {category}, powered by "{title}".',
    ],
    "insider": [
        'Insiders say the room reacted strongly after {artist} won {category}, with several teams reassessing their award-season strategy.',
        'Sources around Grammy night say {artist}\'s {category} win for "{title}" became the main backstage talking point.',
        'Post-awards chatter centers on {artist}, whose {category} win reportedly shifted the mood among rival camps.',
    ],
    "rumour": [
        'Rumours from Grammy night suggest {artist}\'s win for "{title}" did not sit well with at least one rival camp.',
        'Unconfirmed reports from after the awards say the {category} result sparked private frustration among competing teams.',
        'Award-night rumours point to tension after {artist} won {category}, though no artist has publicly addressed it.',
    ],
    "feud": [
        'Grammy night fallout: sources say {artist} and {target} had a tense exchange after the {category} result.',
        'A post-awards disagreement involving {artist} and {target} is becoming one of the bigger stories after Grammy night.',
        'Industry chatter links {artist} and {target} to a brewing dispute following the {category} announcement.',
    ],
}

CRITIC_USERNAMES = {critic.name: critic.username for critic in CRITIC_PROFILES}

FAN_PREFIXES = ["real", "official", "the", "big", "lil", "young", "not", "just", "ur", "its", "im", "only", "that", "xo", "og", "rare"]
FAN_NOUNS = ["fan", "wave", "vibes", "steez", "plug", "mind", "mode", "world", "era", "type", "szn", "drip", "gang", "lore", "side", "soul"]
FAN_SUFFIXES = ["2k", "3k", "xo", "fr", "irl", "rn", "tbh", "btw", "official", "real", "verified", "based", "coded", "pilled"]
FAN_NUMBERS = ["1", "2", "3", "7", "99", "00", "23", "404", "666"]

ARTIST_CONTROVERSY_TWEETS = {
    "hate_tweet": [
        "i've had enough. {target} is everything wrong with this world and i won't pretend otherwise.",
        "let's be real about {target}. someone has to say it.",
        "everything i've seen from {target} has been a lie. done pretending.",
        "tired of staying quiet about {target}. not anymore.",
    ],
    "expose_post": [
        "y'all want receipts? here they are. {target} has some explaining to do. thread.",
        "thread time. what {target} doesn't want you to know. 1/",
        "since {target} wants to act innocent, let me refresh some memories.",
    ],
    "cryptic_post": [
        "some people move in silence while others just move wrong. you know who you are.",
        "not naming names but {target} knows exactly what they did.",
        "accountability doesn't care about your PR team.",
    ],
    "boycott_call": [
        "i'm calling on everyone to reconsider their support of {target}. here's why:",
        "i no longer support {target} and i'm not asking anyone to either.",
    ],
    "public_apology": [
        "i said some things about {target} that i need to own. i was wrong. i'm sorry.",
        "owed {target} an apology for a while now. here it is publicly.",
    ],
    "twitter_beef": [
        "{target} has been talking. let's talk back.",
        "i've been quiet about {target} for too long. that ends now.",
        "nah {target} you don't get to move like that without hearing from me.",
        "{target} really thought i wouldn't respond. interesting.",
        "there is a difference between confidence and whatever {target} is doing. tonight we discuss it.",
        "i kept one eye on {target} all week and somehow they still disappointed me.",
        "{target} keeps mistaking silence for distance. i was standing right there.",
    ],
    "clout_accusation": [
        "{target} has been riding waves they didn't make for years. everyone sees it.",
        "the clout chasing from {target} has gotten embarrassing at this point.",
    ],
    "ghostwrite_claim": [
        "asking for a friend: does {target} write their own music?",
        "the pen that writes {target}'s bars should get the credit tbh.",
        "{target} rhymes like somebody else left the session early.",
        "if {target} wrote that alone then i wrote the moon landing.",
    ],
    "challenge": [
        "{target}. 16 bars. any platform. any time. let the music speak.",
        "put a mic in front of {target} and put a mic in front of me. let's go.",
        "{target} can pick the beat, the room, and the excuse.",
        "i want {target} on wax, not in captions.",
    ],
    "dismissal": [
        "{target} stopped being relevant when they stopped being honest.",
        "i don't have beef with {target}. you can't have beef with someone who isn't at your level.",
    ],
    "twitter_critic": [
        "{target} gave my project a {score}. let me know when you've made something.",
        "{target}'s {score} tells me more about them than it does about my music.",
        "{target} is a joke. a {score}? really?",
    ],
    "bias_accusation": [
        "{target} has a pattern. low score my music, glowing review for anyone else. do the math.",
        "genuine question: who is paying {target} to hate on certain artists?",
    ],
    "challenge_critic": [
        "{target} make a song. just one. then we can talk about what's good.",
        "critics like {target} only exist because they can't create.",
    ],
    "credentials_attack": [
        "who gave {target} a platform to review music they clearly don't understand?",
        "the amount of influence {target} has over real artists is a crime against music.",
    ],
    "subtweet": [
        "some people should really just stay quiet. saves everyone the embarrassment.",
        "the audacity is always free, isn't it.",
        "love the confidence. hate the competence.",
    ],
    "response_1_twitter_thread": [
        "response #1. {target} opened that door, now we can really talk.",
        "response #1 and i'm keeping it light. {target} don't make me go deeper.",
        "first response out the way. {target} still acting confused is hilarious.",
        "response #1. {target} tossed a match and looked surprised at the smoke.",
        "first response and i already had to leave half the folder closed.",
    ],
    "response_1_interview_clapback": [
        "response #1. {target} wanted a reply and now they've got one.",
        "that little move from {target} wasn't going to sit unanswered. response #1.",
    ],
    "response_1_livestream": [
        "response #1. i went live because {target} clearly needed extra attention.",
        "for response #1, let me simplify this for {target} in public.",
    ],
    "response_1_stage": [
        "response #1. told the crowd exactly what i think about {target}.",
        "response #1 happened from the stage because {target} earned that energy.",
    ],
    "response_2_receipts": [
        "response #2. receipts attached. now what, {target}?",
        "second response and now i'm posting proof because {target} keeps playing games.",
        "response #2. screenshots age better than excuses.",
        "second response. {target} made me organize the evidence by date.",
    ],
    "response_2_interview_escalation": [
        "response #2. {target} wanted another round, so here we are.",
        "second response and i'm being generous by only saying this much about {target}.",
    ],
    "response_2_laugh_off": [
        "response #2. the funniest part is {target} thinking they landed anything serious.",
        "round two. still not impressed by {target}.",
    ],
    "response_2_space": [
        "response #2 and yes i had time today. {target} should've stayed quiet.",
        "second response. opened the space because {target} needed a longer explanation.",
    ],
    "response_3_family_edge": [
        "response #3. now it's obvious {target} wanted this to get ugly.",
        "third response. if {target} keeps pushing, this gets worse.",
        "response #3. we are past music now because {target} kept kicking the door.",
        "third response. everybody wanted lines crossed until the lines had names on them.",
    ],
    "response_3_ghostwriter": [
        "response #3. saying it again because {target} clearly didn't hear me the first time.",
        "third response. the truth about {target} does not get softer with repetition.",
    ],
    "response_3_full_meltdown": [
        "response #3 and i'm done pretending this is a normal disagreement.",
        "third response. {target} turned this into chaos and now everyone can watch.",
    ],
    "response_3_challenge": [
        "response #3. booth, stage, anywhere. {target} stop hiding behind timelines.",
        "third response. if {target} still has something to say then prove it properly.",
    ],
    "response_4_nuclear_post": [
        "response #4. this is the part where {target} figures out they pushed too far.",
        "fourth response. i tried to keep it cute. not anymore.",
        "response #4. the polite version expired.",
        "fourth response. {target} is about to miss the old tone.",
    ],
    "response_4_backstage_claim": [
        "response #4. now let's talk about what {target} does when cameras are off.",
        "fourth response and suddenly the backstage stories matter a lot more.",
    ],
    "response_4_stream_rant": [
        "response #4. if {target} wanted peace they missed the exit two turns ago.",
        "fourth response. went live because one post wasn't enough for this mess.",
    ],
    "response_4_direct_threat": [
        "response #4. {target} keeps treating this like a joke. bad decision.",
        "fourth response. i don't think {target} understands the tone anymore.",
    ],
    "response_5_final_word": [
        "response #5. final word. {target} can keep the silence or keep the damage.",
        "fifth response. i'm done after this. {target} can live with the record.",
    ],
    "response_5_receipts_dump": [
        "response #5. every receipt i had is out now. {target} figure it out.",
        "fifth response. emptied the folder on {target}. nothing left to hide.",
        "response #5. last envelope opened. {target} can argue with paper now.",
        "fifth response. no more hints, no more mercy captions.",
    ],
    "response_5_last_interview": [
        "response #5. last time i'm speaking on {target} and that's me being kind.",
        "fifth response. after this, {target} gets no more oxygen from me.",
    ],
    "response_5_burn_bridge": [
        "response #5. there is no bridge left with {target}. that's final.",
        "fifth response. closed the book on {target} and burned the cover too.",
    ],
}

ARTIST_RELEASE_ANNOUNCEMENT = {
    "single": ['"{title}" - week {week}.', 'new single "{title}" dropping week {week}.', 'dropping "{title}" week {week}. no more waiting.', '"{title}" - w{week}. just trust.'],
    "album": ['new album "{title}" drops week {week}.', 'the album. "{title}". week {week}. finally.', '"{title}" - a full album. week {week}. i am ready.', 'the project is done. "{title}" - w{week}.'],
    "ep": ['"{title}" ep dropping week {week}.', 'small but complete. "{title}" ep - week {week}.', 'ep mode. "{title}" - week {week}.'],
    "mixtape": ['"{title}" tape coming week {week}. free game.', 'dropping the tape. "{title}" - w{week}.', 'tape dropping week {week}. "{title}". for the real ones.'],
}

ARTIST_TRACKLIST_REVEAL = [
    '"{album}" tracklist:\n\n{tracklist}\n\nweek {week}.',
    "here's what \"{album}\" looks like:\n\n{tracklist}",
    "for the people asking. \"{album}\" tracklist.\n\n{tracklist}",
    "\"{album}\" - full tracklist below.\n\n{tracklist}",
]

ARTIST_FRIEND_PRAISE = {
    "single": ['{artist}\'s "{title}" is the song of the week. not up for debate.', 'go stream "{title}" by {artist}. that is the whole tweet.', 'been playing "{title}" by {artist} on repeat. certified.'],
    "album": ['{artist}\'s "{title}" is a body of work. front to back.', 'the way {artist} sequenced "{title}" - genius. whole project hits.', '"{title}" by {artist} is what i needed to hear this week.'],
    "ep": ['{artist}\'s "{title}" ep is 4 records of zero filler.', 'short and perfect. {artist}\'s "{title}" ep.'],
    "mixtape": ['{artist} dropped the "{title}" tape and the streets are talking.', '"{title}" by {artist}. tape of the season. easily.'],
}

FAN_CONTROVERSY_REACTIONS = {
    "type1_negative": ['the {instigator} situation with {target} is genuinely concerning', 'why is {instigator} always in something', '{instigator} really said hold my drink and went off on {target}'],
    "type1_positive": ['{instigator} said what needed to be said about {target}. period.', 'finally someone said it. {instigator} is not wrong about {target}.'],
    "type2_beef": ['the {instigator} and {target} beef is getting real interesting', '{instigator} vs {target}. who do we think wins this?', '{instigator} really went there. {target} move now.'],
    "type2_response": ['{instigator} responding to {target} is everything i needed today', 'round {loop} of the {instigator}/{target} beef. buckle up.', 'the timeline is fed. {instigator} responded to {target}.'],
    "type3_critic": ['{instigator} really went after {target} huh. bold.', '{target} gave {instigator} a bad score and now the whole timeline is mad', '{instigator} is not letting that {target} review go'],
}

FAN_RELEASE_REACTIONS = {
    "hype_high": ['the {artist} "{title}" rollout is sending me. cannot wait.', 'week {week} cannot come fast enough. {artist} is about to end people.', '{artist} dropping "{title}" week {week} is the only news that matters.'],
    "hype_medium": ['not gonna lie i am interested in what {artist} does with "{title}"', '{artist} dropping "{title}" - curious to see where they go with this.', 'keeping an eye on the {artist} "{title}" drop. could be something.'],
    "hype_low": ['another {artist} project? okay. we will see.', 'i will give "{title}" by {artist} a chance but expectations are tempered.', '{artist} dropping again. i will stream it once i guess.'],
}

FAN_RELEASE_RECEPTION = {
    "love_song": ['"{title}" by {artist} just went into heavy rotation. incredible.', 'the way "{title}" hits at 2am. {artist} knew exactly what they were doing.', 'been playing "{title}" 15 times today and i have no plans to stop.'],
    "like_song": ['"{title}" is a solid record. {artist} keeps delivering.', 'the {artist} "{title}" track is pretty good actually.', '"{title}" grew on me. {artist} has range.'],
    "mid_song": ['"{title}" is fine i guess. expected more from {artist}.', 'not bad but not great. {artist}\'s "{title}" did not move me.', '{artist}\'s "{title}" feels like a placeholder tbh.'],
    "hate_song": ['who approved "{title}" by {artist}?? be honest.', '{artist}\'s "{title}" is really not it.', '"{title}" by {artist} is the sound of running out of ideas.'],
    "love_album": ['"{title}" by {artist} is a complete body of work. front to back.', '"{title}" is the album of the year and i am not accepting debate.', 'every track on "{title}" serves a purpose. {artist} does not miss.'],
    "hate_album": ['"{title}" is not the project i needed from {artist}. at all.', '{artist} had all that time and gave us "{title}". disappointed.', '{artist}\'s "{title}" is the definition of diminishing returns.'],
}

FAN_FEATURE_REACTIONS = {
    "great_verse": ['{feature} on the {artist} song "{title}" is the verse of the year.', 'the {feature} verse on "{title}" literally rewired my brain.', '{feature} came into "{title}" and completely took over.'],
    "good_verse": ['{feature} added real value to "{title}". solid verse.', 'the {feature} feature on "{title}" is pretty strong. good call by {artist}.', '{feature} showed up on "{title}". that is a good get.'],
    "bad_verse": ['who approved the {feature} verse on "{title}".', '{feature} on "{title}" is not it. pulled the whole song down.', '{artist} should have kept "{title}" solo. the {feature} verse really hurt it.'],
}

FAN_RUMOURS = [
    "not sure if this is confirmed but apparently {artist} has been working on new music for over a year now",
    "the {artist} silence is either them cooking something incredible or label drama. 50/50.",
    "my source says {artist} has already finished their next project and it is different from anything before",
    "theory: {artist} is dropping soon. the engagement pattern on their page is suspicious.",
    "heard through someone who heard through someone that {artist} and {target} have been in the studio",
    "i wonder if the {artist}/{target} situation affected the album rollout. the timing is weird.",
]

CRITIC_TWEETS = {
    "pre_release_positive": ['the upcoming {artist} project "{title}" is generating real energy in the right rooms.', 'if the singles are any indication, {artist}\'s "{title}" could be the defining release of this stretch.', '{artist} has been in serious form recently. "{title}" arriving week {week}.'],
    "pre_release_skeptical": ['week {week} brings {artist}\'s "{title}". the question is whether the recent form translates to a full project.', 'cautiously interested in "{title}" by {artist}. the catalogue has been inconsistent lately.', '{artist}\'s "{title}" needs to prove something that their recent singles have not.'],
    "best_of_week": ['best release this week: "{title}" by {artist}. {score}/10 from me.', 'the week belonged to {artist}. "{title}" is the only record i will still be thinking about by friday.', 'weekly roundup and "{title}" by {artist} clears the field comfortably. {score}/10.'],
    "worst_of_week": ['worst release this week: "{title}" by {artist}. {score}/10.', 'giving "{title}" a {score} is not a takedown. it is an honest accounting of a disappointing release.', 'not everything can be great. "{title}" by {artist} this week is evidence of that. {score}/10.'],
    "feature_strong": ['the {feature} verse on "{title}" is the most technically accomplished thing released this week.', '{feature} on the {artist} track "{title}" - that is what a feature contribution should look like.'],
    "feature_weak": ['the {feature} feature on "{title}" is puzzling. the rest of the song deserved better.', '{feature} on "{title}" is a rare stumble. the verse does not serve the song.'],
    "feature_neutral": ['the {feature} contribution to "{title}" is competent without being essential.', '{feature} on "{title}" does what is asked. nothing more.'],
    "critic_response_doubledown": ['my review of "{title}" stands. {score}/10.', 'calling my review of {artist}\'s "{title}" a fraud does not change the score. {score}/10.', 'the review is the review. "{title}" by {artist} - {score}/10.'],
    "critic_clapback_short": ['the score stands.', '{score}/10. i said what i said.', 'read the review. it explains itself.'],
    "critic_re_review_threat": ['given the response to my "{title}" review i am considering a second listen. to go lower.', 'revisiting "{title}" after this week\'s noise. my initial score may have been generous.'],
    "critic_mic_drop": ['"{title}" by {artist}. {score}/10.', 'my review: still there. still accurate.', '[original review link]'],
}

GRAMMY_ARTIST_TWEETS = {
    "acceptance": [
        'thank you to everyone who lived with "{title}" this year. this {category} means more than i can explain.',
        'we won {category}. grateful for the team, the fans, and everyone who believed in "{title}".',
        '{category}. wow. "{title}" was personal and seeing it recognized like this is unreal.',
        'taking this {category} home for everyone who worked on "{title}". thank you.',
    ],
    "nominee_reaction": [
        '"{title}" is nominated for {category}. grateful, surprised, and very aware of how strong this field is.',
        'honored to see "{title}" in the {category} conversation. this year has been wild.',
        '{category} nomination. thank you to everyone who carried "{title}" with us.',
    ],
    "sore_loser": [
        'interesting choice for {category}. congratulations to {winner}, i guess.',
        'so "{winner_title}" wins {category}. everyone saw the field. i will leave it there.',
        'no disrespect, but {category} had stronger work than "{winner_title}". people know.',
        'award rooms love a safe pick. congrats to {winner} though.',
    ],
}

GRAMMY_FAN_TWEETS = {
    "nomination_gossip": [
        'i do not care what anybody says, {artist} absolutely deserved that {category} nomination for "{title}".',
        '"{title}" getting into {category} just saved these nominations from being completely unserious.',
        '{artist} in {category} feels right to me and i am not arguing with anyone about it.',
        'i already know people are mad about {artist} getting into {category} and i honestly do not care.',
        '{artist} making {category} for "{title}" is the first nomination today that actually clicked for me.',
        'the {category} field is chaos already but i am standing ten toes behind "{title}" by {artist}.',
        'if {artist} had missed {category} for "{title}" i would have called these nominations fraudulent immediately.',
        'the only thing i know for sure is that "{title}" by {artist} belongs in {category}.',
        'some of these nominations are wild but {artist} in {category} is not one of the mistakes.',
        'i am fine with a lot today purely because {artist} got into {category} for "{title}".',
        '{artist} in {category} just gave this whole Grammy race actual stakes for me.',
        'the group chat is screaming about {category} and honestly i am on {artist}\'s side.',
    ],
    "winner_love": [
        '{artist} winning {category} for "{title}" is exactly the result i wanted.',
        'oh they got {category} right for once. "{title}" by {artist} absolutely deserved that.',
        'i am so serious, {artist} taking {category} just redeemed the whole night for me.',
        '"{title}" winning {category} feels correct, clean, and overdue.',
        'best result of the night so far: {artist} winning {category}. no notes.',
        'that {category} win for {artist} just made me sit up like yes finally.',
        'i was ready to complain and then they gave {category} to {artist}. fair enough.',
        '{artist} took {category} and i need everyone to stop pretending that is not the right call.',
        'that {category} trophy belongs to "{title}". i am glad the room acted accordingly.',
        'i love when the obvious best project actually wins and {artist} just did that.',
        '{artist} winning {category} has me defending the Grammys for the next ten minutes.',
        'for once the award went to the project i have been yelling about all year.',
    ],
    "winner_hate": [
        'i am sorry but {artist} winning {category} for "{title}" is a terrible result.',
        'that {category} win just annoyed me immediately. no way "{title}" was the strongest option.',
        'the academy really heard that whole field and still gave {category} to {artist}. unbelievable.',
        'i do not hate {artist} but that {category} result is nonsense to me.',
        'giving {category} to "{title}" is exactly why people do not trust these awards.',
        'i just stared at the screen after that {category} win like be serious.',
        '{artist} taking {category} feels like the safest possible choice and i mean that as an insult.',
        'nah i cannot defend that one. {category} should have gone somewhere else entirely.',
        'that {category} result is going to bother me for the rest of the night.',
        'i know people will spin it but {artist} did not have the best project in {category}.',
        'this is one of those Grammy wins where you instantly know discourse is about to get ugly.',
        'they really handed {category} to {artist} and expected us not to complain.',
    ],
    "snub_gossip": [
        '{loser} losing {category} to {winner} just ruined the mood for me immediately.',
        'i am not accepting {loser} losing {category}. that one is staying with me.',
        '{category} going to {winner} over {loser} is exactly the kind of thing that starts fan wars.',
        'you can already feel the timeline turning on that {category} result because {loser} did not win.',
        '{loser} losing {category} is the part where i close the app and stop being reasonable.',
        'if {loser} lost {category} so that {winner} could win, then yes i am complaining.',
        '{category} went to {winner} and now i fully understand why {loser} fans are furious.',
        'that {category} result just made everybody pick sides and i am not on {winner}\'s side.',
        'i am going to be hearing about {loser} losing {category} all week and honestly fair enough.',
        'the second {winner} got announced for {category} i knew {loser} fans were about to explode.',
    ],
}

GRAMMY_CRITIC_TWEETS = {
    "nomination_opinion": [
        'The {category} nominations are credible, but "{title}" by {artist} is the one to watch.',
        '{artist} landing in {category} for "{title}" feels less like a surprise and more like overdue recognition.',
        'Strong {category} field this year. "{title}" gives {artist} a real path to the award.',
    ],
    "winner_opinion": [
        '{artist} winning {category} for "{title}" is defensible. Not obvious, but defensible.',
        'The {category} result rewards craft over noise. "{title}" by {artist} had the stronger full-project case.',
        'I would not have picked every winner tonight, but {artist} taking {category} makes sense.',
        '{category} going to "{title}" by {artist} will age better than the immediate reaction suggests.',
    ],
    "winner_skeptical": [
        '{artist} winning {category} is the kind of Grammy choice that will split critics for a while.',
        'I understand the {category} argument for "{title}", but the academy played it conservative.',
        'Good project, strange result. {category} had more adventurous options than "{title}".',
    ],
}

AUTHOR_TYPE_COLORS = {"artist": "\033[95m", "fan": "\033[96m", "critic": "\033[93m"}
RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"

TYPE_LABELS = {
    "controversy": "BEEF",
    "announcement": "DROP",
    "tracklist_reveal": "TRACKLIST",
    "friend_praise": "PRAISE",
    "controversy_reaction": "REACTION",
    "hype": "HYPE",
    "reception": "TAKE",
    "feature_reaction": "VERSE",
    "rumour": "RUMOUR",
    "pre_release": "PREVIEW",
    "best_of_week": "BEST",
    "worst_of_week": "WORST",
    "controversy_response": "RESPONSE",
    "grammy_nomination": "GRAMMYS",
    "grammy_acceptance": "GRAMMYS",
    "grammy_shade": "GRAMMYS",
    "grammy_reaction": "GRAMMYS",
    "grammy_opinion": "GRAMMYS",
    "diss_release": "DISS",
    "diss_response": "DISS",
    "diss_hype": "DISS",
    "diss_review": "DISS",
    "diss_claims": "DISS",
    "diss_verdict": "VERDICT",
}


POOL_VARIANT_PREFIXES = []

POOL_VARIANT_SUFFIXES = [
    "and the timeline noticed.",
    "nobody is pretending otherwise.",
    "there is no soft way to say that.",
    "people are going to talk about it all week.",
    "that is where things are now.",
    "everyone can read between the lines.",
    "it feels bigger than a passing moment.",
    "this is going to echo for a while.",
    "it landed exactly how you think it landed.",
    "and that changed the mood immediately.",
]

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


def _expand_sentence_pool(
    pool: list[str],
    min_extra: int = 10,
    max_extra: int = 14,
    prefixes: list[str] | None = None,
    suffixes: list[str] | None = None,
) -> list[str]:
    expanded = list(pool)
    seen = set(expanded)
    extras_needed = min(max_extra, max(min_extra, len(pool)))
    prefix_pool = prefixes if prefixes is not None else POOL_VARIANT_PREFIXES
    suffix_pool = suffixes if suffixes is not None else POOL_VARIANT_SUFFIXES
    for base in pool:
        if len(expanded) >= len(pool) + extras_needed:
            break
        if prefix_pool:
            for prefix in prefix_pool:
                variant = f"{prefix} {base}"
                if variant not in seen:
                    expanded.append(variant)
                    seen.add(variant)
                if len(expanded) >= len(pool) + extras_needed:
                    break
            if len(expanded) >= len(pool) + extras_needed:
                break
        for suffix in suffix_pool:
            trimmed = base[:-1] if base.endswith((".", "!", "?")) else base
            variant = f"{trimmed}. {suffix}"
            if variant not in seen:
                expanded.append(variant)
                seen.add(variant)
            if len(expanded) >= len(pool) + extras_needed:
                break
    return expanded


def _expand_pool_dict(
    pool_dict: dict[str, list[str]],
    min_extra: int = 10,
    max_extra: int = 14,
    prefixes: list[str] | None = None,
    suffixes: list[str] | None = None,
) -> dict[str, list[str]]:
    for key, pool in list(pool_dict.items()):
        pool_dict[key] = _expand_sentence_pool(
            list(pool),
            min_extra=min_extra,
            max_extra=max_extra,
            prefixes=prefixes,
            suffixes=suffixes,
        )
    return pool_dict


HEADLINE_TEMPLATES = _expand_pool_dict(
    HEADLINE_TEMPLATES,
    min_extra=10,
    max_extra=12,
    prefixes=NEWS_VARIANT_PREFIXES,
    suffixes=NEWS_VARIANT_SUFFIXES,
)
ARTIST_CONTROVERSY_TWEETS = _expand_pool_dict(ARTIST_CONTROVERSY_TWEETS, min_extra=10, max_extra=14)
ARTIST_RELEASE_ANNOUNCEMENT = _expand_pool_dict(ARTIST_RELEASE_ANNOUNCEMENT, min_extra=10, max_extra=12)
ARTIST_FRIEND_PRAISE = _expand_pool_dict(ARTIST_FRIEND_PRAISE, min_extra=10, max_extra=12)
FAN_CONTROVERSY_REACTIONS = _expand_pool_dict(FAN_CONTROVERSY_REACTIONS, min_extra=10, max_extra=14)
FAN_RELEASE_REACTIONS = _expand_pool_dict(FAN_RELEASE_REACTIONS, min_extra=10, max_extra=14)
FAN_RELEASE_RECEPTION = _expand_pool_dict(FAN_RELEASE_RECEPTION, min_extra=10, max_extra=14)
FAN_FEATURE_REACTIONS = _expand_pool_dict(FAN_FEATURE_REACTIONS, min_extra=10, max_extra=14)
CRITIC_TWEETS = _expand_pool_dict(CRITIC_TWEETS, min_extra=10, max_extra=14)
NEW_RELEASE_NEWS_TEMPLATES = _expand_pool_dict(
    NEW_RELEASE_NEWS_TEMPLATES,
    min_extra=8,
    max_extra=10,
    prefixes=NEWS_VARIANT_PREFIXES,
    suffixes=NEWS_VARIANT_SUFFIXES,
)
ARTIST_TRACKLIST_REVEAL = _expand_sentence_pool(ARTIST_TRACKLIST_REVEAL, min_extra=10, max_extra=12)
FAN_RUMOURS = _expand_sentence_pool(FAN_RUMOURS, min_extra=10, max_extra=14)

SIDE_HUSTLES = [
    {"name": "Burger Bunker", "pay": 35.0, "fatigue": 18.0},
    {"name": "Needle & Noise Records", "pay": 75.0, "fatigue": 24.0},
    {"name": "RushRoute Delivery", "pay": 130.0, "fatigue": 31.0},
    {"name": "Moonline Warehouse", "pay": 220.0, "fatigue": 38.0},
]

MANAGEMENT_COMPANIES = [
    {"name": "Amplify Collective", "yearly_cost": 12000.0, "pop_gain": (8.0, 13.0), "base_cut": 10.0, "strictness": 0.85},
    {"name": "The Narrative Arc", "yearly_cost": 35000.0, "pop_gain": (13.0, 18.0), "base_cut": 12.0, "strictness": 1.0},
    {"name": "Momentum Media", "yearly_cost": 90000.0, "pop_gain": (22.0, 30.0), "base_cut": 15.0, "strictness": 1.15},
    {"name": "Catalyst Comms", "yearly_cost": 220000.0, "pop_gain": (34.0, 42.0), "base_cut": 18.0, "strictness": 1.3},
    {"name": "Verve Public Relations", "yearly_cost": 550000.0, "pop_gain": (46.0, 56.0), "base_cut": 22.0, "strictness": 1.45},
]

GENRE_SKILL_WEIGHTS = {
    "pop": {"lyrics": 0.20, "vocals": 0.35, "production": 0.25, "mix/master": 0.20},
    "hip hop": {"lyrics": 0.40, "vocals": 0.15, "production": 0.30, "mix/master": 0.15},
    "rock": {"lyrics": 0.20, "vocals": 0.30, "production": 0.30, "mix/master": 0.20},
    "jazz": {"lyrics": 0.15, "vocals": 0.25, "production": 0.30, "mix/master": 0.30},
    "classical": {"lyrics": 0.05, "vocals": 0.15, "production": 0.40, "mix/master": 0.40},
    "electronic": {"lyrics": 0.05, "vocals": 0.10, "production": 0.50, "mix/master": 0.35},
    "r&b": {"lyrics": 0.20, "vocals": 0.35, "production": 0.25, "mix/master": 0.20},
    "metal": {"lyrics": 0.15, "vocals": 0.30, "production": 0.30, "mix/master": 0.25},
    "country": {"lyrics": 0.35, "vocals": 0.30, "production": 0.20, "mix/master": 0.15},
    "reggae": {"lyrics": 0.25, "vocals": 0.25, "production": 0.25, "mix/master": 0.25},
    "folk": {"lyrics": 0.35, "vocals": 0.30, "production": 0.20, "mix/master": 0.15},
    "blues": {"lyrics": 0.20, "vocals": 0.35, "production": 0.20, "mix/master": 0.25},
    "punk": {"lyrics": 0.20, "vocals": 0.25, "production": 0.30, "mix/master": 0.25},
    "soul": {"lyrics": 0.20, "vocals": 0.40, "production": 0.20, "mix/master": 0.20},
    "experimental": {"lyrics": 0.15, "vocals": 0.15, "production": 0.40, "mix/master": 0.30},
}


@dataclass
class SongEntry:
    song: Song
    released: bool = False
    average_review: float | None = None
    release_id: str = field(default_factory=lambda: str(uuid4()))
    source_label: str = "Single"
    total_streams: int = 0
    last_week_streams: int = 0
    total_digital_sales: int = 0
    last_week_digital_sales: int = 0
    total_physical_sales: int = 0
    last_week_physical_sales: int = 0
    first_week_sales: int = 0
    release_popularity_value: float = 0.0
    release_popularity_weeks_left: int = 0
    weeks_since_release: int = 0
    producer: str | None = None
    engineer: str | None = None
    features: list[str] = field(default_factory=list)
    physical_editions: list["PhysicalEdition"] = field(default_factory=list)
    virality_triggered: bool = False
    virality_weeks_active: int = 0  # 0-based age of virality at the start of a week
    virality_max_weekly_bonus: int = 0
    virality_baseline_streams: int = 0
    release_week_index: int | None = None


@dataclass
class FeatureRequest:
    request_id: str
    direction: str  # "inbound" or "outbound"
    artist_name: str
    song_name: str
    song_quality: float
    status: str  # "pending", "accepted", "rejected", "awaiting_verse", "verse_sent", "completed", "expired"
    week_created: int
    week_deadline: int
    artist_verse_quality: float | None = None
    player_verse_quality: float | None = None
    weeks_until_artist_delivers: int = 0
    paid: float = 0.0
    rejected_by_player: bool = False
    resend_used: bool = False
    ecosystem_release_id: str | None = None
    ecosystem_track_index: int | None = None
    request_kind: str = "feature"  # feature, producer, engineer
    player_album_name: str | None = None
    forced_release_week: int | None = None


@dataclass
class AlbumEntry:
    album: Album
    released: bool = False
    release_id: str = field(default_factory=lambda: str(uuid4()))
    release_week_index: int | None = None
    deluxe_of: str | None = None
    average_review: float | None = None
    total_digital_sales: int = 0
    last_week_digital_sales: int = 0
    total_physical_sales: int = 0
    last_week_physical_sales: int = 0
    first_week_sales: int = 0
    physical_editions: list["PhysicalEdition"] = field(default_factory=list)


@dataclass
class ManagementContract:
    company_name: str
    term_label: str
    weeks_left: int
    billing_amount: float
    billing_every_weeks: int
    weeks_until_payment: int
    weekly_popularity_range: tuple[float, float]
    current_weekly_popularity: float
    stream_cut_pct: float


@dataclass
class JobContract:
    job_name: str
    weekly_pay: float
    weekly_fatigue: float
    weeks_left: int


@dataclass
class PopularityState:
    organic: float = 2.0
    management: float = 0.0
    weekly_song: float = 0.0
    live_boost: float = 0.0
    feature_boost: float = 0.0
    feature_boost_weeks_left: int = 0
    album_release_boost: float = 0.0
    album_release_weeks_left: int = 0


@dataclass
class RelationshipState:
    score: float = 0.0
    last_interaction_week: int = 0
    last_positive_week_interaction: int = 0
    last_positive_week_live: int = 0
    last_contact_week: int = 0
    last_request_week: int = 0
    recent_requests: int = 0


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


@dataclass
class PhysicalEdition:
    format_name: str
    unit_cost: float
    list_price: float
    discount_pct: float = 0.0
    limited_edition: bool = False
    copies_created: int = 0
    copies_remaining: int = 0
    total_units_sold: int = 0
    last_week_units_sold: int = 0
    total_revenue: float = 0.0
    total_manufacturing_cost: float = 0.0

    def effective_price(self) -> float:
        return max(0.5, float(self.list_price) * (1.0 - max(0.0, min(0.9, float(self.discount_pct)))))


@dataclass
class SalesSnapshot:
    total_digital: int = 0
    last_week_digital: int = 0
    total_physical: int = 0
    last_week_physical: int = 0
    first_week_sales: int = 0

    @property
    def total_sales(self) -> int:
        return int(self.total_digital + self.total_physical)

    @property
    def last_week_sales(self) -> int:
        return int(self.last_week_digital + self.last_week_physical)


@dataclass
class Tweet:
    id: str
    week: int
    author: str
    username: str
    author_type: str
    tweet_type: str
    content: str
    reply_to_id: str | None
    likes: int
    retweets: int
    controversy_id: str | None = None


@dataclass
class RomanceProfile:
    owner_name: str
    status: str = "single"
    partner_name: str = ""
    partner_is_artist: bool = False
    relationship_start_week: int = 0
    engagement_week: int = 0
    marriage_week: int = 0
    separation_week: int = 0
    separation_from_status: str = ""
    divorce_week: int = 0
    marriage_count: int = 0
    divorce_count: int = 0
    visibility: str = "private"
    stability_score: float = 52.0
    scandal_pressure_score: float = 0.0
    last_breakup_week: int = -999
    last_event_week: int = 0
    partner_history: list[str] = field(default_factory=list)
    ex_relationships: list[dict] = field(default_factory=list)


@dataclass
class RomanceEvent:
    id: str
    week: int
    event_type: str
    artist_name: str
    partner_name: str
    partner_is_artist: bool
    headline: str
    visibility: str = "known"
    confirmed: bool = False
    third_party_name: str = ""
    rumor_confidence: str = "soft"


@dataclass
class PlayerLoveRelationship:
    partner_name: str
    partner_is_artist: bool
    status: str = "dating"
    lovingness: float = 50.0
    strength: float = 50.0
    start_week: int = 0
    end_week: int = 0
    visibility: str = "private"
    cheated: bool = False
    public_scandal: bool = False
    notes: list[str] = field(default_factory=list)


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


class TwitterModule:
    def __init__(self):
        self.weekly_tweets: dict[int, list[Tweet]] = {}
        self.announced_release_ids: set[str] = set()
        self.tracklist_revealed_ids: set[str] = set()

    def add_tweets(self, week: int, tweets: list[Tweet]):
        if tweets:
            self.weekly_tweets[week] = list(tweets)

    def get_tweets(self, week: int) -> list[Tweet]:
        return list(self.weekly_tweets.get(week, []))

    def get_all_tweets(self, last_n_weeks: int, current_week: int) -> list[tuple[int, Tweet]]:
        result = []
        for w in range(max(0, current_week - last_n_weeks), current_week + 1):
            for tweet in self.weekly_tweets.get(w, []):
                result.append((w, tweet))
        return sorted(result, key=lambda item: (-item[0], -(item[1].likes + item[1].retweets * 2)))


@dataclass
class Artist:
    name: str
    skills: dict
    genres: dict
    gender: str = "male"
    sexuality: str = "straight"
    romance_preference: str = "prefers_female"
    current_course: str | None = None
    course_weeks_left: int = 0
    week: int = 1
    year: int = 1
    fatigue: float = 0.0
    health: float = 100.0
    popularity_state: PopularityState = field(default_factory=PopularityState)
    money: float = 0.0
    live_count_this_week: int = 0
    management: ManagementContract | None = None
    side_hustle: JobContract | None = None
    last_week_earnings: float = 0.0
    last_week_management_cut: float = 0.0
    last_week_management_fee: float = 0.0
    last_week_streams: int = 0
    last_week_physical_income: float = 0.0
    singles: list[SongEntry] = field(default_factory=list)
    albums: list[AlbumEntry] = field(default_factory=list)
    relationships: dict[str, RelationshipState] = field(default_factory=dict)
    feature_requests: list[FeatureRequest] = field(default_factory=list)
    reputation: float = 50.0
    controversy: float = PLAYER_DEFAULT_CONTROVERSY
    brutality: float = PLAYER_DEFAULT_BRUTALITY
    battle_skills: int = 50
    controversy_popularity_offset: float = 0.0
    controversy_reputation_offset: float = 0.0
    controversy_history: list[ControversyEvent] = field(default_factory=list)
    pending_responses: list[dict] = field(default_factory=list)
    recent_low_reviews: list[dict] = field(default_factory=list)
    releases_this_week: list[dict] = field(default_factory=list)
    grammy_state: dict[int, dict] = field(default_factory=dict)  # year -> results cache
    beat_market: object | None = None
    love_relationships: list[PlayerLoveRelationship] = field(default_factory=list)
    numble_match_week: int = 0
    numble_match_names: list[str] = field(default_factory=list)
    upcoming_concerts: list[ConcertBooking] = field(default_factory=list)
    concert_history: list[ConcertBooking] = field(default_factory=list)
    price_templates: dict = field(default_factory=lambda: dict(DEFAULT_PRICE_TEMPLATES))
    setlist_templates: dict = field(default_factory=dict)
    live_popularity: float = 2.0
    owned_venues: list = field(default_factory=list)

    @property
    def live_performance_rating(self) -> float:
        if not getattr(self, "concert_history", None):
            return 0.0
        scores = [b.performance_score for b in self.concert_history]
        if not scores:
            return 0.0
        return (sum(scores) / len(scores)) * 10.0

    @property
    def popularity(self):
        return clamp_popularity(
            self.popularity_state.organic
            + self.popularity_state.management
            + self.popularity_state.live_boost
            + self.popularity_state.feature_boost
            + self.popularity_state.weekly_song
            + (self.popularity_state.album_release_boost if self.popularity_state.album_release_weeks_left > 0 else 0.0)
            + active_release_popularity(self)
        )


def clamp_stat(value):
    return max(1, min(100, int(value)))


def clamp_meter(value):
    return max(0.0, min(100.0, float(value)))


def clamp_fatigue(value):
    return max(0.0, min(140.0, float(value)))


def clamp_popularity(value):
    return max(0.0, min(100.0, float(value)))


def money_fmt(value):
    return f"${value:,.2f}"


def clamp_rating(value):
    return max(1.0, min(10.0, float(value)))


def clamp_signed_rating(value):
    return max(-10.0, min(10.0, float(value)))


def weighted_choice(weight_map: dict):
    items = [(key, float(value)) for key, value in weight_map.items() if float(value) > 0]
    if not items:
        raise ValueError("weighted_choice requires at least one positive weight")
    labels = [item[0] for item in items]
    weights = [item[1] for item in items]
    return random.choices(labels, weights=weights, k=1)[0]


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


def release_bump_for_quality(quality):
    if quality <= 3.0:
        return 1.0
    if quality <= 5.0:
        return 2.0
    if quality <= 7.0:
        return 3.0
    if quality <= 9.0:
        return 4.0
    return 5.0


def active_release_popularity(artist):
    return sum(
        entry.release_popularity_value
        for entry in artist.singles
        if entry.released and entry.release_popularity_weeks_left > 0
    )


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


def roll_catchiness_value():
    # 0.1-1 (20%), 1-2 (50%), 2-3 (20%), 3-4 (8%), 4-5 (2%)
    r = random.random()
    if r < 0.20:
        return round(random.uniform(0.1, 1.0), 2)
    if r < 0.70:
        return round(random.uniform(1.0, 2.0), 2)
    if r < 0.90:
        return round(random.uniform(2.0, 3.0), 2)
    if r < 0.98:
        return round(random.uniform(3.0, 4.0), 2)
    return round(random.uniform(4.0, 5.0), 2)


def roll_virality_value_and_maturity():
    # TESTING MODE (user-tuned distribution):
    # 1-2: 80%, 2-3: 15%, 3-4: 4.95%, 4-5: 0.05%
    r = random.random()
    if r < 0.80:
        v = random.uniform(1.0, 2.0)
    elif r < 0.95:
        v = random.uniform(2.0, 3.0)
    elif r < 0.9995:
        v = random.uniform(3.0, 4.0)
    else:
        v = random.uniform(4.0, 5.0)
    maturity = random.randint(100, 200)
    return round(v, 2), maturity


def catchiness_stream_multiplier(catchiness):
    if catchiness is None:
        return 1.0
    c = max(0.1, min(5.0, float(catchiness)))

    # Under 1.0: a flat performance haircut.
    if c <= 1.0:
        # 0.1 => 0.2x, 1.0 => 1.0x
        t = (c - 0.1) / 0.9
        return 0.2 + (0.8 * max(0.0, min(1.0, t)))

    # Above 1.0: piecewise curve that keeps "catchy" songs noticeably ahead without
    # making every high-quality track feel identical.
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

    # After 8 weeks of virality, decay to a floor:
    # max(2% of virality peak bonus, the pre-virality stream level).
    peak = max(entry.virality_max_weekly_bonus, hi)
    floor_bonus = max(int(0.02 * peak), int(entry.virality_baseline_streams))
    # Ease down toward the floor over ~8 weeks, then hover around it.
    t = min(1.0, max(0.0, (age - 8) / 8.0))  # week 9 => 0, week 16+ => 1
    target = (1.0 - t) * peak + t * floor_bonus
    bonus = int(random.uniform(target * 0.88, target * 1.05))
    return max(0, bonus)


def meter_bar(label, value, width=22, invert=False):
    value = clamp_meter(value)
    display_value = 100.0 - value if invert else value
    filled = int(round((display_value / 100.0) * width))
    filled = max(0, min(width, filled))
    empty = width - filled
    return f"{label}: [{'#' * filled}{'-' * empty}]"


def prompt_text(prompt, default=None):
    raw = input(prompt).strip()
    if raw:
        return raw
    return default


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


def prompt_int(prompt, minimum=None, maximum=None, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            value = int(default)
        else:
            try:
                value = int(raw)
            except ValueError:
                print("Enter a valid number.")
                continue
        if minimum is not None and value < minimum:
            print(f"Enter a number >= {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a number <= {maximum}.")
            continue
        return value


def prompt_float(prompt, minimum=None, maximum=None, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            value = float(default)
        else:
            try:
                value = float(raw)
            except ValueError:
                print("Enter a valid number.")
                continue
        if minimum is not None and value < minimum:
            print(f"Enter a number >= {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a number <= {maximum}.")
            continue
        return float(value)


def choose_from_list(title, options, allow_cancel=False):
    while True:
        print(f"\n{title}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        if allow_cancel:
            print("0. Cancel")
        choice = prompt_int("Choose: ", 0 if allow_cancel else 1, len(options))
        if allow_cancel and choice == 0:
            return None
        return choice - 1


def choose_item_from_list(title, options, allow_cancel=False):
    idx = choose_from_list(title, options, allow_cancel=allow_cancel)
    if idx is None:
        return None
    return options[idx]


def choose_unique_items(title, options, count):
    chosen = []
    while len(chosen) < count:
        remaining = [opt for opt in options if opt not in chosen]
        idx = choose_from_list(
            f"{title} ({len(chosen) + 1}/{count})",
            remaining,
            allow_cancel=False,
        )
        chosen.append(remaining[idx])
    return chosen


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
    print(f"{artist.name} | Year {artist.year} Week {artist.week}")
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


def _ensure_news_state(world: EcosystemWorld | None):
    if world is not None and getattr(world, "news_module", None) is None:
        world.news_module = NewsModule()


def _ensure_twitter_state(world: EcosystemWorld | None):
    if world is not None and getattr(world, "twitter_module", None) is None:
        world.twitter_module = TwitterModule()


def _news_channel_meta(key: str) -> dict:
    return NEWS_CHANNELS.get(key, NEWS_CHANNELS["general"])


def _pick_reporter(channel_key: str, stable_key: str) -> str:
    meta = _news_channel_meta(channel_key)
    reporters = list(meta.get("reporters", ()) or ("Staff Reporter",))
    if not reporters:
        return "Staff Reporter"
    rng = _stable_rng_for_label(f"reporter:{channel_key}:{stable_key}")
    return str(rng.choice(reporters))


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


def _first_week_sales_value(last_week_sales: int, first_week_sales: int) -> int:
    return int(first_week_sales or last_week_sales or 0)


def _riaa_certification_label(total_sales: int) -> str:
    for threshold, label in RIAA_CERTIFICATIONS:
        if int(total_sales) >= int(threshold):
            return label
    return "-"


def _effective_sale_price(list_price: float, discount_pct: float) -> float:
    return max(0.5, float(list_price) * (1.0 - max(0.0, min(0.9, float(discount_pct)))))


def _physical_bulk_discount(copies: int) -> float:
    for threshold, discount in PHYSICAL_BULK_DISCOUNTS:
        if int(copies) >= int(threshold):
            return float(discount)
    return 0.0


def _physical_unit_cost(format_name: str, copies: int, limited_edition: bool = False) -> float:
    base_cost = float(PHYSICAL_UNIT_COSTS[format_name])
    if limited_edition:
        base_cost *= float(PHYSICAL_LIMITED_COST_MULT)
    return round(base_cost * (1.0 - _physical_bulk_discount(copies)), 2)


def _physical_edition_label(edition: PhysicalEdition) -> str:
    prefix = "limited " if bool(getattr(edition, "limited_edition", False)) else ""
    return f"{prefix}{edition.format_name}"


def _physical_financials(editions: list[PhysicalEdition]) -> tuple[float, float, float, float]:
    spent = 0.0
    revenue = 0.0
    for edition in editions:
        edition_spent = float(getattr(edition, "total_manufacturing_cost", 0.0) or 0.0)
        if edition_spent <= 0:
            edition_spent = float(getattr(edition, "unit_cost", 0.0) or 0.0) * int(getattr(edition, "copies_created", 0) or 0)
        spent += edition_spent
        revenue += float(getattr(edition, "total_revenue", 0.0) or 0.0)
    profit = revenue - spent
    margin = (profit / revenue * 100.0) if revenue > 0 else 0.0
    return float(spent), float(revenue), float(profit), float(margin)


def _release_kind_label(release_type: str) -> str:
    release_type = str(release_type or "single")
    if release_type in {"album", "deluxe", "mixtape"}:
        return release_type
    return "single"


def _physical_fair_price(release_type: str, format_name: str, quality: float, popularity: float) -> float:
    base = PHYSICAL_BASE_PRICES.get((_release_kind_label(release_type), format_name), 9.99)
    quality_factor = 0.82 + (max(1.0, min(10.0, float(quality))) / 10.0) * 0.38
    popularity_factor = 0.88 + (max(0.0, min(100.0, float(popularity))) / 100.0) * 0.32
    return round(base * quality_factor * popularity_factor, 2)


def _physical_pricing_multiplier(price_ratio: float, effective_price: float, format_name: str) -> float:
    price_ratio = max(0.01, float(price_ratio))
    effective_price = max(0.5, float(effective_price))
    if price_ratio <= 1.0:
        return 1.0 + ((1.0 - price_ratio) * 0.35)

    # Above fair price, demand falls exponentially. Absolute luxury pricing gets
    # another hard penalty so absurd prices do not keep selling through volume.
    ratio_mult = math.exp(-1.8 * ((price_ratio - 1.0) ** 1.65))
    barrier = 60.0 if format_name == "disc" else 160.0
    if effective_price <= barrier:
        absolute_mult = 1.0
    else:
        absolute_mult = math.exp(-((effective_price - barrier) / barrier) ** 1.35)
    return max(0.0, min(1.35, ratio_mult * absolute_mult))


def _physical_units_from_streams(
    *,
    weekly_streams: int,
    popularity: float,
    quality: float,
    release_type: str,
    format_name: str,
    effective_price: float,
    limited_edition: bool = False,
) -> int:
    if int(weekly_streams) <= 0 or float(popularity) <= 50.0:
        return 0
    base = float(weekly_streams) / 5000.0
    quality_mult = 0.70 + (max(1.0, min(10.0, float(quality))) / 10.0) * 0.55
    popularity_mult = 0.65 + (max(0.0, min(100.0, float(popularity))) / 100.0) * 0.75
    fair_price = _physical_fair_price(release_type, format_name, quality, popularity)
    if limited_edition:
        fair_price = round(fair_price * 1.35, 2)
    price_ratio = float(effective_price) / max(0.5, fair_price)
    pricing_mult = _physical_pricing_multiplier(price_ratio, effective_price, format_name)
    limited_mult = float(PHYSICAL_LIMITED_DEMAND_MULT) if limited_edition else 1.0
    units = base * quality_mult * popularity_mult * pricing_mult * limited_mult * random.uniform(0.75, 1.25)
    whole = int(units)
    frac = units - whole
    if random.random() < frac:
        whole += 1
    return max(0, whole)


def _apply_physical_sales(
    editions: list[PhysicalEdition],
    *,
    weekly_streams: int,
    popularity: float,
    quality: float,
    release_type: str,
) -> tuple[int, float]:
    total_units = 0
    total_revenue = 0.0
    for edition in editions:
        edition.last_week_units_sold = 0
        if edition.copies_remaining <= 0:
            continue
        effective_price = edition.effective_price()
        demand_units = _physical_units_from_streams(
            weekly_streams=int(weekly_streams),
            popularity=float(popularity),
            quality=float(quality),
            release_type=release_type,
            format_name=edition.format_name,
            effective_price=effective_price,
            limited_edition=bool(getattr(edition, "limited_edition", False)),
        )
        sold = min(int(edition.copies_remaining), int(demand_units))
        if sold <= 0:
            continue
        edition.copies_remaining -= sold
        edition.last_week_units_sold = sold
        edition.total_units_sold += sold
        revenue = sold * effective_price
        edition.total_revenue += revenue
        total_units += sold
        total_revenue += revenue
    return int(total_units), float(total_revenue)


def _player_song_sales_snapshot(entry: SongEntry) -> SalesSnapshot:
    return SalesSnapshot(
        total_digital=int(entry.total_digital_sales),
        last_week_digital=int(entry.last_week_digital_sales),
        total_physical=int(entry.total_physical_sales),
        last_week_physical=int(entry.last_week_physical_sales),
        first_week_sales=int(entry.first_week_sales),
    )


def _player_album_sales_snapshot(artist, album_entry: AlbumEntry) -> SalesSnapshot:
    tracks = [
        linked_entry
        for song in album_entry.album.songs
        for linked_entry in [next((e for e in artist.singles if e.song is song and e.released), None)]
        if linked_entry is not None
    ]
    total_digital = sum(int(track.total_digital_sales) for track in tracks)
    last_week_digital = sum(int(track.last_week_digital_sales) for track in tracks)
    total_physical = sum(int(edition.total_units_sold) for edition in album_entry.physical_editions)
    last_week_physical = sum(int(edition.last_week_units_sold) for edition in album_entry.physical_editions)
    if album_entry.first_week_sales <= 0 and (last_week_digital + last_week_physical) > 0:
        album_entry.first_week_sales = int(last_week_digital + last_week_physical)
    album_entry.total_digital_sales = int(total_digital)
    album_entry.last_week_digital_sales = int(last_week_digital)
    album_entry.total_physical_sales = int(total_physical)
    album_entry.last_week_physical_sales = int(last_week_physical)
    return SalesSnapshot(
        total_digital=int(total_digital),
        last_week_digital=int(last_week_digital),
        total_physical=int(total_physical),
        last_week_physical=int(last_week_physical),
        first_week_sales=int(album_entry.first_week_sales),
    )


def _ensure_sales_state(world: EcosystemWorld | None):
    if world is None:
        return
    if getattr(world, "song_sales_state", None) is None:
        world.song_sales_state = {}
    if getattr(world, "release_sales_state", None) is None:
        world.release_sales_state = {}
    if getattr(world, "physical_inventory_by_release", None) is None:
        world.physical_inventory_by_release = {}


def _world_song_sales(world: EcosystemWorld, song_id: str) -> SalesSnapshot:
    _ensure_sales_state(world)
    if song_id not in world.song_sales_state:
        world.song_sales_state[song_id] = SalesSnapshot()
    return world.song_sales_state[song_id]


def _world_release_sales(world: EcosystemWorld, release_id: str) -> SalesSnapshot:
    _ensure_sales_state(world)
    if release_id not in world.release_sales_state:
        world.release_sales_state[release_id] = SalesSnapshot()
    return world.release_sales_state[release_id]


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


def _ensure_ecosystem_physical_inventory(world: EcosystemWorld, release, popularity: float):
    if float(popularity) <= 50.0:
        return
    editions = _world_release_editions(world, str(getattr(release, "release_id", "")))
    if editions:
        return
    release_type = _release_kind_label(str(getattr(release, "release_type", "single")))
    quality = _ecosystem_release_quality(release)
    base_copies = 60 if release_type == "single" else 140
    pop_bonus = int(max(0.0, float(popularity) - 50.0) * (3 if release_type == "single" else 5))
    total_copies = max(20, base_copies + pop_bonus)
    disc_share = 0.75 if release_type == "single" else 0.55
    disc_copies = int(total_copies * disc_share)
    vinyl_copies = max(0, total_copies - disc_copies)
    for format_name, copies in (("disc", disc_copies), ("vinyl", vinyl_copies)):
        if copies <= 0:
            continue
        editions.append(
            PhysicalEdition(
                format_name=format_name,
                unit_cost=float(PHYSICAL_UNIT_COSTS[format_name]),
                list_price=_physical_fair_price(release_type, format_name, quality, popularity),
                discount_pct=0.0,
                copies_created=int(copies),
                copies_remaining=int(copies),
            )
        )


def _step_ecosystem_sales(world: EcosystemWorld):
    _ensure_sales_state(world)
    popularity_by_name = getattr(world, "artist_popularity", {}) or {}
    for runtime_song in world.song_runtime.values():
        song_state = _world_song_sales(world, str(getattr(runtime_song, "song_id", "")))
        digital_units = int(getattr(runtime_song, "last_week_streams", 0) or 0) // 1000
        song_state.last_week_digital = int(digital_units)
        song_state.total_digital += int(digital_units)
        song_state.last_week_physical = 0
        if song_state.first_week_sales <= 0 and digital_units > 0 and int(getattr(runtime_song, "weeks_since_release", 0)) <= 1:
            song_state.first_week_sales = int(digital_units)

    for releases in world.release_history.values():
        for release in releases:
            release_id = str(getattr(release, "release_id", ""))
            if not release_id:
                continue
            weeks_since_release = int(getattr(world, "week_number", 0)) - int(getattr(release, "week_number", 0))
            tracks = list(getattr(release, "tracks", None) or ())
            if weeks_since_release > 30:
                weekly_streams = sum(int(getattr(world.song_runtime.get(str(getattr(track, "song_id", "")), None), "last_week_streams", 0) or 0) for track in tracks)
                editions = _world_release_editions(world, release_id)
                is_sold_out = (not editions) or all(int(getattr(edition, "copies_remaining", 0)) <= 0 for edition in editions)
                if weekly_streams == 0 and is_sold_out:
                    release_state = _world_release_sales(world, release_id)
                    release_state.last_week_digital = 0
                    release_state.last_week_physical = 0
                    release_state.total_digital = sum(int(_world_song_sales(world, str(getattr(t, "song_id", ""))).total_digital) for t in tracks)
                    release_state.total_physical = sum(int(getattr(edition, "total_units_sold", 0)) for edition in editions)
                    continue

            release_state = _world_release_sales(world, release_id)
            release_state.last_week_digital = 0
            release_state.total_digital = 0
            for track in tracks:
                track_state = _world_song_sales(world, str(getattr(track, "song_id", "")))
                release_state.last_week_digital += int(track_state.last_week_digital)
                release_state.total_digital += int(track_state.total_digital)
            popularity = float(popularity_by_name.get(str(getattr(release, "artist_name", "")), 0.0))
            _ensure_ecosystem_physical_inventory(world, release, popularity)
            physical_units, _ = _apply_physical_sales(
                _world_release_editions(world, release_id),
                weekly_streams=sum(int(getattr(world.song_runtime.get(str(getattr(track, "song_id", "")), None), "last_week_streams", 0) or 0) for track in tracks),
                popularity=popularity,
                quality=_ecosystem_release_quality(release),
                release_type=str(getattr(release, "release_type", "single")),
            )
            release_state.last_week_physical = int(physical_units)
            release_state.total_physical = sum(int(edition.total_units_sold) for edition in _world_release_editions(world, release_id))
            if release_state.first_week_sales <= 0 and int(getattr(release, "week_number", 0)) == int(getattr(world, "week_number", 0)):
                release_state.first_week_sales = int(release_state.last_week_sales)


def artist_username(name):
    cleaned = []
    for ch in str(name).lower():
        if ch.isalnum():
            cleaned.append(ch)
    return "@" + "".join(cleaned)


def generate_fan_username():
    style = random.randint(1, 5)
    if style == 1:
        return f"@{random.choice(FAN_PREFIXES)}{random.choice(FAN_NOUNS)}{random.choice(FAN_NUMBERS)}"
    if style == 2:
        return f"@{random.choice(FAN_NOUNS)}{random.choice(FAN_SUFFIXES)}"
    if style == 3:
        name_parts = ["alex", "jay", "kai", "sam", "rio", "dev", "zoe", "ash", "lee", "nova"]
        return f"@{random.choice(name_parts)}{random.choice(FAN_NUMBERS)}{random.choice(FAN_SUFFIXES)}"
    if style == 4:
        return f"@{random.choice(FAN_PREFIXES)}{random.choice(FAN_NOUNS)}{random.choice(FAN_SUFFIXES)}"
    return f"@{random.choice(FAN_NOUNS)}{random.choice(FAN_NUMBERS)}"


def _critic_username(name: str) -> str:
    return CRITIC_USERNAMES.get(name, artist_username(name))


def _tweet_release_title(title: str, artist_name: str) -> str:
    prefix = f"{artist_name} - "
    short = title[len(prefix):] if str(title).startswith(prefix) else str(title)
    return short.strip()


def _compact_tweet_title(title: str, max_len: int = 54) -> str:
    text = str(title).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def _ecosystem_artist_object(world: EcosystemWorld, artist_name: str):
    runtime = _find_world_runtime(world, artist_name)
    if runtime is None:
        return None
    romance = _get_romance_profile(world, artist_name)
    return SimpleNamespace(
        name=artist_name,
        popularity=float(_ecosystem_artist_popularity(artist_name, world)),
        friend_list=list(world.social_graph.get(artist_name, {}).get("friends", [])),
        enemy_list=list(world.social_graph.get(artist_name, {}).get("enemies", [])),
        is_growing="growing" in classify_artist_skills(runtime.seed),
        romance_status=romance.status if romance is not None else "single",
        romance_partner=romance.partner_name if romance is not None else "",
    )


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


def _romance_week_label(week_index: int) -> str:
    if not week_index:
        return "unknown"
    year, week = _year_week_from_world_week(int(week_index))
    return f"Y{year} W{week}"


def _romance_duration_from_weeks(start_week: int, end_week: int) -> int:
    if not start_week or not end_week:
        return 0
    return max(1, int(end_week) - int(start_week) + 1)


def _current_romance_duration(profile: RomanceProfile, current_week: int) -> int:
    return _romance_duration_from_weeks(profile.relationship_start_week, current_week)


def _separation_status_label(profile: RomanceProfile) -> str:
    status = str(getattr(profile, "separation_from_status", "") or "").strip()
    if not status:
        status = "married" if profile.marriage_week else "relationship"
    return ROMANCE_STATUS_LABELS.get(status, status)


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


def _active_release_pressure(world: EcosystemWorld, artist_name: str) -> float:
    recent = world.release_history.get(artist_name, [])[-2:]
    pressure = 0.0
    for release in recent:
        age = max(0, int(world.week_number) - int(getattr(release, "week_number", world.week_number)))
        if age <= 8:
            pressure += max(0.0, 1.2 - (age / 8.0))
    return pressure


def _recent_controversy_load(world: EcosystemWorld, artist_name: str) -> float:
    history = world.controversy_history_by_artist.get(artist_name, [])
    recent = [event for event in history if (int(world.week_number) - int(getattr(event, "week", 0))) <= 10]
    return float(len(recent))


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


def _romance_weekly_start_budget(world: EcosystemWorld) -> int:
    active = sum(1 for profile in world.romance_profiles.values() if profile.status in {"dating", "engaged", "married"})
    budget = 1 if random.random() < 0.28 else 0
    if active < 9 and random.random() < 0.08:
        budget += 1
    return budget


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


def _is_growing_artist_name(name: str, world: EcosystemWorld | None) -> bool:
    runtime = _find_world_runtime(world, name)
    if runtime is None:
        return False
    return "growing" in classify_artist_skills(runtime.seed)


def _releases_for_week(world: EcosystemWorld, week_number: int) -> list:
    rows = []
    for artist_name, releases in world.release_history.items():
        for release in releases:
            if int(getattr(release, "week_number", -1)) == int(week_number):
                rows.append(release)
    return rows


def _weekly_release_score(release) -> float:
    return float(getattr(release, "review", getattr(release, "review_score", 0.0)))


def _release_song_rows(release) -> list[dict]:
    tracks = list(getattr(release, "tracks", ()) or ())
    if not tracks:
        return []
    rows = []
    for track in tracks:
        feature_rows = list(getattr(track, "feature_qualities", ()) or ())
        rows.append(
            {
                "name": _tweet_release_title(str(getattr(track, "title", "")), str(getattr(release, "artist_name", ""))),
                "main_artist": str(getattr(release, "artist_name", "")),
                "features": [{"artist_name": str(name), "verse_quality": float(score)} for name, score in feature_rows],
            }
        )
    return rows


def _controversy_action_rep(event: ControversyEvent) -> float:
    if event.controversy_type != 1:
        return 0.0
    for action in TYPE_1_ACTIONS:
        if action["key"] == event.action_key:
            return float(action["rep"])
    return 0.0


def _artist_controversy_tweet_pool(event: ControversyEvent) -> list[str]:
    pool = ARTIST_CONTROVERSY_TWEETS.get(event.action_key)
    if pool:
        return pool
    if event.controversy_type == 2 and event.loop_count > 0:
        return ARTIST_CONTROVERSY_TWEETS["subtweet"]
    return ARTIST_CONTROVERSY_TWEETS["subtweet"]


def _display_twitter_feed(tweets, current_week, limit=None):
    def _wrap_lines(text: str, width: int = 62) -> list[str]:
        words = str(text).split()
        if not words:
            return [""]
        lines = []
        line = ""
        for word in words:
            candidate = word if not line else f"{line} {word}"
            if len(candidate) > width:
                lines.append(line)
                line = word
            else:
                line = candidate
        if line:
            lines.append(line)
        return lines

    def _short_count(value: int) -> str:
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M".rstrip("0").rstrip(".") + "M"
        if value >= 1_000:
            return f"{value // 1000}K"
        return str(value)

    print()
    print("+" + "-" * 70 + "+")
    print("|" + f" X / TWITTER / WEEK {current_week} ".center(70) + "|")
    print("+" + "-" * 70 + "+")
    print()
    sections = [
        ("ARTIST TWEETS", [tweet for tweet in tweets if tweet.author_type == "artist"]),
        ("FAN TWEETS", [tweet for tweet in tweets if tweet.author_type == "fan"]),
        ("CRITIC TWEETS", [tweet for tweet in tweets if tweet.author_type == "critic"]),
    ]

    for section_title, section_tweets in sections:
        print(section_title)
        print("-" * len(section_title))
        if not section_tweets:
            print("  none")
            print()
            continue
        visible = section_tweets if limit is None else section_tweets[:limit]
        for idx, tweet in enumerate(visible):
            label = TYPE_LABELS.get(tweet.tweet_type, "")
            likes_str = _short_count(int(tweet.likes))
            rt_str = _short_count(int(tweet.retweets))
            header = f"{tweet.author}  {tweet.username}  [{label}]"
            print(header)
            for line in _wrap_lines(tweet.content, width=66):
                print(f"  {line}")
            print(f"  likes {likes_str} | rts {rt_str}")
            print()
            if idx < len(visible) - 1:
                print("  " + "-" * 66)
                print()
        print()
def _find_world_runtime(world: EcosystemWorld | None, artist_name: str):
    if world is None:
        return None
    for runtime in world.roster:
        if runtime.seed.name == artist_name:
            return runtime
    return None


def _find_artist_any(name: str, player_artist: Artist, world: EcosystemWorld | None):
    if name == player_artist.name:
        return player_artist
    return _find_world_runtime(world, name)


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


def _artist_display_name(subject) -> str:
    if isinstance(subject, Artist):
        return subject.name
    return subject.seed.name


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


def _ecosystem_artist_popularity(name, ecosystem_world: EcosystemWorld | None = None):
    seed = _ecosystem_seed_by_name(name)
    base = float(getattr(seed, "popularity", 0.0)) if seed else 0.0
    if ecosystem_world is None:
        return base
    return float(getattr(ecosystem_world, "artist_popularity", {}).get(name, base))


def _ecosystem_artist_reputation(name, ecosystem_world: EcosystemWorld | None = None):
    base = float(ARTIST_BASE_REPUTATION.get(name, 50))
    if ecosystem_world is None:
        return base
    return float(getattr(ecosystem_world, "artist_reputation", {}).get(name, base))


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


def _grammy_week_number(current_week: int) -> int:
    return _year_week_from_world_week(current_week)[1]


def _is_grammy_media_week(current_week: int) -> bool:
    return 49 <= _grammy_week_number(current_week) <= 52


def _player_release_sales_candidates(player_artist: Artist) -> list[dict]:
    rows: list[dict] = []
    for entry in player_artist.singles:
        if not entry.released:
            continue
        if str(getattr(entry, "source_label", "")).startswith("Album:"):
            continue
        snapshot = _player_song_sales_snapshot(entry)
        rows.append(
            {
                "artist": player_artist.name,
                "title": entry.song.name,
                "release_type": "single",
                "release_week": int(entry.release_week_index or 0),
                "first_week_sales": int(snapshot.first_week_sales),
                "last_week_sales": int(snapshot.last_week_sales),
                "total_sales": int(snapshot.total_sales),
            }
        )
    for album_entry in player_artist.albums:
        if not album_entry.released:
            continue
        snapshot = _player_album_sales_snapshot(player_artist, album_entry)
        rows.append(
            {
                "artist": player_artist.name,
                "title": album_entry.album.name,
                "release_type": "deluxe" if album_entry.deluxe_of else "album",
                "release_week": int(album_entry.release_week_index or 0),
                "first_week_sales": int(snapshot.first_week_sales),
                "last_week_sales": int(snapshot.last_week_sales),
                "total_sales": int(snapshot.total_sales),
            }
        )
    return rows


def _ecosystem_release_sales_candidates(world: EcosystemWorld | None) -> list[dict]:
    if world is None:
        return []
    _ensure_sales_state(world)
    rows: list[dict] = []
    for artist_name, releases in world.release_history.items():
        for release in releases:
            state = _world_release_sales(world, str(getattr(release, "release_id", "")))
            rows.append(
                {
                    "artist": artist_name,
                    "title": str(getattr(release, "title", "")),
                    "release_type": str(getattr(release, "release_type", "single")),
                    "release_week": int(getattr(release, "week_number", 0)),
                    "first_week_sales": int(state.first_week_sales),
                    "last_week_sales": int(state.last_week_sales),
                    "total_sales": int(state.total_sales),
                }
            )
    return rows


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


def _grammy_winners_revealed_for_week(week_in_year: int) -> int:
    if week_in_year >= 52:
        return len(GRAMMY_CATEGORY_ORDER)
    if week_in_year >= 51:
        return 5
    if week_in_year >= 50:
        return 3
    if week_in_year >= 49:
        return 1
    return 0


def _grammy_categories_announced_this_week(week_in_year: int) -> list[str]:
    current_count = _grammy_winners_revealed_for_week(week_in_year)
    previous_count = _grammy_winners_revealed_for_week(week_in_year - 1)
    return GRAMMY_CATEGORY_ORDER[previous_count:current_count]


def _grammy_nomination_blocks(results: dict) -> list[tuple[str, list[dict]]]:
    blocks = []
    for category in GRAMMY_CATEGORY_ORDER:
        nominees = list(results.get(category, {}).get("nominees") or [])
        if nominees:
            blocks.append((category, nominees))
    return blocks


def _generate_grammy_tweets(current_week: int, world: EcosystemWorld, player_artist, all_artists: list[Artist], all_critics: list[str]) -> list[Tweet]:
    if player_artist is None or not _is_grammy_media_week(current_week):
        return []
    year, week_in_year = _year_week_from_world_week(current_week)
    results = _ensure_grammy_results(player_artist, world, year)
    if not results:
        return []

    tweets: list[Tweet] = []
    artist_names = {artist.name for artist in all_artists}

    def add_artist_tweet(author_name: str, tweet_type: str, content: str, big: bool = True):
        if author_name not in artist_names:
            return
        tweets.append(
            Tweet(
                id=str(uuid4()),
                week=current_week,
                author=author_name,
                username=artist_username(author_name),
                author_type="artist",
                tweet_type=tweet_type,
                content=content,
                reply_to_id=None,
                likes=random.randint(40000, 900000) if big else random.randint(10000, 220000),
                retweets=random.randint(12000, 260000) if big else random.randint(3000, 70000),
            )
        )

    def add_fan_tweet(content: str):
        tweets.append(
            Tweet(
                id=str(uuid4()),
                week=current_week,
                author="fan",
                username=generate_fan_username(),
                author_type="fan",
                tweet_type="grammy_reaction",
                content=content,
                reply_to_id=None,
                likes=random.randint(1000, 65000),
                retweets=random.randint(200, 22000),
            )
        )

    def add_critic_tweet(content: str):
        critic_name = random.choice(all_critics)
        tweets.append(
            Tweet(
                id=str(uuid4()),
                week=current_week,
                author=critic_name,
                username=_critic_username(critic_name),
                author_type="critic",
                tweet_type="grammy_opinion",
                content=content,
                reply_to_id=None,
                likes=random.randint(2500, 70000),
                retweets=random.randint(500, 18000),
            )
        )

    if week_in_year == 49:
        blocks = _grammy_nomination_blocks(results)
        for category, nominees in random.sample(blocks, min(5, len(blocks))):
            lead = nominees[0]
            artist_obj = _ecosystem_artist_object(world, lead["artist"])
            if artist_obj is not None:
                template = random.choice(GRAMMY_ARTIST_TWEETS["nominee_reaction"])
                add_artist_tweet(
                    lead["artist"],
                    "grammy_nomination",
                    template.format(category=category, title=_compact_tweet_title(lead["title"])),
                    big=True,
                )
            fan_template = random.choice(GRAMMY_FAN_TWEETS["nomination_gossip"])
            add_fan_tweet(fan_template.format(category=category, artist=lead["artist"], title=_compact_tweet_title(lead["title"])))
            critic_template = random.choice(GRAMMY_CRITIC_TWEETS["nomination_opinion"])
            add_critic_tweet(critic_template.format(category=category, artist=lead["artist"], title=_compact_tweet_title(lead["title"])))

    announced_categories = _grammy_categories_announced_this_week(week_in_year)
    for category in announced_categories:
        block = results.get(category, {})
        winner = block.get("winner")
        nominees = list(block.get("nominees") or [])
        if not winner:
            continue
        winner_name = winner["artist"]
        winner_title = _compact_tweet_title(winner["title"])
        template = random.choice(GRAMMY_ARTIST_TWEETS["acceptance"])
        add_artist_tweet(winner_name, "grammy_acceptance", template.format(category=category, title=winner_title), big=True)

        for _ in range(random.randint(2, 4)):
            fan_pool = "winner_love" if random.random() < 0.5 else "winner_hate"
            fan_template = random.choice(GRAMMY_FAN_TWEETS[fan_pool])
            add_fan_tweet(fan_template.format(category=category, artist=winner_name, title=winner_title))

        if len(nominees) > 1:
            loser = random.choice([nominee for nominee in nominees if nominee["artist"] != winner_name])
            fan_template = random.choice(GRAMMY_FAN_TWEETS["snub_gossip"])
            add_fan_tweet(fan_template.format(category=category, loser=loser["artist"], winner=winner_name))

        critic_pool = "winner_skeptical" if random.random() < 0.35 else "winner_opinion"
        critic_template = random.choice(GRAMMY_CRITIC_TWEETS[critic_pool])
        add_critic_tweet(critic_template.format(category=category, artist=winner_name, title=winner_title))

        controversial_losers = []
        winner_obj = _ecosystem_artist_object(world, winner_name)
        for nominee in nominees:
            loser_name = nominee["artist"]
            if loser_name == winner_name:
                continue
            loser_obj = _ecosystem_artist_object(world, loser_name)
            if loser_obj is None or float(getattr(loser_obj, "controversy", 0.0)) <= 70.0:
                continue
            if winner_obj is not None and winner_name in getattr(loser_obj, "friend_list", []):
                continue
            controversial_losers.append(loser_obj)
        for loser_obj in random.sample(controversial_losers, min(2, len(controversial_losers))):
            template = random.choice(GRAMMY_ARTIST_TWEETS["sore_loser"])
            add_artist_tweet(
                loser_obj.name,
                "grammy_shade",
                template.format(category=category, winner=winner_name, winner_title=winner_title),
                big=False,
            )

    return tweets


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


def _generate_romance_tweets(current_week: int, world: EcosystemWorld | None, grammy_media_week: bool = False) -> list[Tweet]:
    if world is None:
        return []
    _ensure_romance_state(world)
    events = list(world.romance_event_history.get(current_week, []))
    if not events:
        return []
    if grammy_media_week and len(events) > 1:
        events = random.sample(events, 1)
    tweets: list[Tweet] = []
    artist_pools = {
        "relationship_confirmed": [
            "keeping this one close, but yes, me and {partner} are together.",
            "some things are better said plainly. {partner} and i are together.",
            "not interested in the noise. i'm happy, and {partner} is a big part of that.",
        ],
        "engagement": [
            "we said yes to the future. love to {partner}.",
            "life moved in a beautiful direction. grateful for {partner} tonight.",
            "engaged. calm heart, full house, big love for {partner}.",
        ],
        "marriage": [
            "married. no speech, just gratitude and a lot of love for {partner}.",
            "it is official. me and {partner} are married.",
            "kept it close, kept it real, made it official with {partner}.",
        ],
        "breakup": [
            "not everything is supposed to last forever. wishing {partner} peace.",
            "some endings are quiet for a reason. i hope {partner} is good.",
            "moving forward privately. that is all i am saying about me and {partner}.",
        ],
        "separation": [
            "hard season. asking for space and grace right now.",
            "sometimes distance is the honest thing.",
            "private situation. please let it stay that way.",
        ],
        "divorce": [
            "this chapter is closed. i want peace for everyone involved.",
            "not every promise survives the life around it.",
            "keeping the details private, but yes, the marriage is over.",
        ],
        "cheating_rumor": [
            "people really turn half a story into a whole lie overnight.",
            "i see the rumors. most of yall do not know what actually happened.",
            "every blurry photo becomes a fake biography on here.",
        ],
        "cheating_confirmed": [
            "some people deserve an apology and some of yall deserve silence.",
            "i made a mess where i should have shown character. i know that.",
            "there is no clean way to talk about disappointing people you loved.",
        ],
        "denial": [
            "that rumor is not true.",
            "not dating who yall say i am dating.",
            "for once, believe less of what you read.",
        ],
        "award_show_couple": [
            "good night, good music, good company.",
            "beautiful night with beautiful energy.",
            "we had a good time. let the cameras talk.",
        ],
    }
    fan_pools = {
        "relationship_confirmed": [
            "wait i actually love this for {artist}.",
            "{artist} going public with {partner} feels right to me.",
            "finally a celebrity relationship i can get behind.",
            "i knew it. that chemistry was not subtle at all.",
        ],
        "relationship_rumor": [
            "i do not care what anyone says, {artist} and {partner} are absolutely together.",
            "the rumor mill is loud because {artist} and {partner} do not look accidental.",
            "if this turns out fake i will be shocked because {artist} and {partner} are moving like a couple.",
        ],
        "spotted_together": [
            "how many times do they need to be seen together before we call it what it is.",
            "{artist} and {partner} are not beating the rumors anymore.",
            "every new sighting makes this look more real.",
        ],
        "engagement": [
            "okay that engagement news is actually sweet.",
            "i did not expect {artist} to get engaged this year but good for them.",
            "i love when a chaotic industry gives us one sincere headline.",
        ],
        "marriage": [
            "wow {artist} really got married. love that for them.",
            "quiet celebrity weddings are always the coolest ones.",
            "{artist} being married now just shifted the whole timeline in my head.",
        ],
        "breakup": [
            "not me being genuinely sad about {artist} and {partner} splitting.",
            "that breakup hurts more than it should.",
            "i knew the pressure around {artist} was getting ugly.",
        ],
        "separation": [
            "that separation headline feels heavy.",
            "i hate how public the rough parts always become.",
            "you can tell this situation around {artist} is not just gossip anymore.",
        ],
        "divorce": [
            "the divorce news around {artist} is rough.",
            "celebrity divorce headlines always feel colder than they should.",
            "that marriage ending was messy long before the paperwork hit the news.",
        ],
        "cheating_rumor": [
            "if the cheating rumor around {artist} is true that is nasty work.",
            "i do not want to believe it, but that story around {artist} sounds ugly.",
            "the {artist} cheating discourse is about to be unbearable.",
        ],
        "cheating_confirmed": [
            "nah if {artist} really did that to {partner}, that is foul.",
            "i cannot defend {artist} on this one.",
            "cheating and then making everyone talk about your rollout is nasty behavior.",
        ],
        "reconciliation_rumor": [
            "not them dragging me back into this relationship saga again.",
            "if {artist} and {partner} get back together i need the full story.",
            "they are about to restart the whole cycle, i can feel it.",
        ],
        "award_show_couple": [
            "{artist} and {partner} just became part of the awards-night plot.",
            "everyone is talking about winners but i am still stuck on {artist} and {partner}.",
            "that red carpet moment just fed the rumor machine for another month.",
        ],
        "rollout_fallout": [
            "the music should be the story but the relationship drama is swallowing the whole rollout.",
            "{artist} cannot get a clean release week with this much relationship mess around them.",
            "the rollout is fighting for its life against the gossip blogs right now.",
        ],
    }
    critic_pools = {
        "relationship_confirmed": [
            "{artist} confirming the relationship with {partner} probably helps the public-image conversation more than it hurts it.",
            "there is enough warmth around {artist} right now that this relationship reveal reads as stabilizing, not distracting.",
        ],
        "breakup": [
            "the breakup becomes part of {artist}'s public story whether they want it or not.",
            "breakup coverage like this can pull attention away from the actual music for weeks.",
        ],
        "divorce": [
            "a divorce headline carries a different weight for an artist brand than a normal breakup.",
            "public divorces tend to reshape how the next release is read, fairly or not.",
        ],
        "cheating_confirmed": [
            "confirmed cheating scandals hit reputation faster than almost any ordinary tabloid cycle.",
            "this kind of scandal can redraw the conversation around {artist} overnight.",
        ],
        "rollout_fallout": [
            "once relationship drama starts outrunning the rollout, every song gets interpreted through it.",
            "the publicity balance has clearly tilted away from the music this week.",
        ],
        "award_show_couple": [
            "their award-show appearance was never going to stay a side note.",
            "for a couple already under attention, that ceremony appearance added another layer of scrutiny.",
        ],
    }
    for event in events:
        likes_base = 12000 + int(max(_ecosystem_artist_popularity(event.artist_name, world), 35.0) * 1800)
        if event.event_type in artist_pools and (event.confirmed or event.event_type in {"cheating_rumor", "cheating_confirmed", "breakup", "separation", "divorce", "award_show_couple"}):
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author=event.artist_name,
                    username=artist_username(event.artist_name),
                    author_type="artist",
                    tweet_type="romance",
                    content=random.choice(artist_pools[event.event_type]).format(artist=event.artist_name, partner=event.partner_name, third=event.third_party_name),
                    reply_to_id=None,
                    likes=random.randint(likes_base, likes_base * 3),
                    retweets=random.randint(4000, 90000),
                )
            )
        if event.event_type == "cheating_confirmed" and _artist_aggression(event.artist_name) > 72:
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author=event.artist_name,
                    username=artist_username(event.artist_name),
                    author_type="artist",
                    tweet_type="romance",
                    content=random.choice([
                        "everybody wants a villain until the full story actually comes out.",
                        "save the fake morality for somebody else.",
                        "the same people talking loud now never cared about the truth in the first place.",
                    ]),
                    reply_to_id=None,
                    likes=random.randint(likes_base // 2, likes_base * 2),
                    retweets=random.randint(2500, 60000),
                )
            )
        fan_pool = fan_pools.get(event.event_type)
        if fan_pool is not None:
            fan_count = 2 if event.event_type in {"relationship_confirmed", "cheating_confirmed", "breakup", "award_show_couple"} else 1
            for _ in range(fan_count):
                tweets.append(
                    Tweet(
                        id=str(uuid4()),
                        week=current_week,
                        author="fan",
                        username=generate_fan_username(),
                        author_type="fan",
                        tweet_type="romance",
                        content=random.choice(fan_pool).format(artist=event.artist_name, partner=event.partner_name, third=event.third_party_name),
                        reply_to_id=None,
                        likes=random.randint(4000, 80000),
                        retweets=random.randint(700, 28000),
                    )
                )
        critic_pool = critic_pools.get(event.event_type)
        if critic_pool is not None and random.random() < 0.85:
            critic_name = random.choice(CRITIC_NAMES)
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author=critic_name,
                    username=_critic_username(critic_name),
                    author_type="critic",
                    tweet_type="romance",
                    content=random.choice(critic_pool).format(artist=event.artist_name, partner=event.partner_name, third=event.third_party_name),
                    reply_to_id=None,
                    likes=random.randint(3000, 45000),
                    retweets=random.randint(500, 16000),
                )
            )
    return tweets


def _generate_weekly_tweets(current_week: int, world: EcosystemWorld | None, player_artist=None) -> list[Tweet]:
    if world is None:
        return []
    _ensure_twitter_state(world)
    twitter_module = world.twitter_module
    all_artists = [_ecosystem_artist_object(world, runtime.seed.name) for runtime in world.roster]
    all_artists = [artist for artist in all_artists if artist is not None]
    all_critics = list(CRITIC_NAMES)
    release_calendar = prepare_release_calendar(world, lookahead=4)
    this_week_releases = list(world.last_week_releases)
    controversy_events = list(world.weekly_events.get(current_week, []))
    tweets: list[Tweet] = []
    def _diss_tweet_factory(author: str, author_type: str, tweet_type: str, content: str) -> Tweet:
        if author_type == "artist":
            display_author = author
            username = artist_username(author)
        elif author_type == "critic":
            display_author = random.choice(CRITIC_NAMES)
            username = _critic_username(display_author)
        else:
            display_author = "fan"
            username = generate_fan_username()
        return Tweet(
            id=str(uuid4()), week=current_week, author=display_author, username=username,
            author_type=author_type, tweet_type=tweet_type, content=content,
            reply_to_id=None, likes=random.randint(1000, 220000),
            retweets=random.randint(200, 70000),
        )
    tweets.extend(build_scheduled_tweets(world, current_week, _diss_tweet_factory))
    grammy_media_week = _is_grammy_media_week(current_week)
    tweets.extend(_generate_grammy_tweets(current_week, world, player_artist, all_artists, all_critics))
    tweets.extend(_generate_romance_tweets(current_week, world, grammy_media_week))

    for event in controversy_events:
        if grammy_media_week and random.random() > 0.15:
            continue
        if event.medium != "twitter":
            continue
        artist = _ecosystem_artist_object(world, event.instigator)
        if artist is None:
            continue
        template = random.choice(_artist_controversy_tweet_pool(event))
        content = template.format(target=event.target, score="low", loop=event.loop_count)
        tweets.append(
            Tweet(
                id=str(uuid4()),
                week=current_week,
                author=artist.name,
                username=artist_username(artist.name),
                author_type="artist",
                tweet_type="controversy",
                content=content,
                reply_to_id=None,
                likes=random.randint(8000, 180000),
                retweets=random.randint(2000, 60000),
                controversy_id=event.id,
            )
        )

    upcoming = []
    for week_number, items in release_calendar.items():
        if current_week < int(week_number) <= current_week + 4:
            upcoming.extend(items)
    unannounced = [release for release in upcoming if release.release_id not in twitter_module.announced_release_ids]
    if unannounced and not grammy_media_week:
        for release in random.sample(unannounced, min(random.randint(3, 4), len(unannounced))):
            artist = _ecosystem_artist_object(world, release.artist_name)
            if artist is None:
                continue
            template = random.choice(ARTIST_RELEASE_ANNOUNCEMENT.get(release.release_type, ARTIST_RELEASE_ANNOUNCEMENT["single"]))
            year, week = _year_week_from_world_week(int(release.week_release))
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author=artist.name,
                    username=artist_username(artist.name),
                    author_type="artist",
                    tweet_type="announcement",
                    content=template.format(title=_compact_tweet_title(_tweet_release_title(release.title, release.artist_name)), week=f"Y{year} W{week}"),
                    reply_to_id=None,
                    likes=random.randint(15000, 400000),
                    retweets=random.randint(5000, 120000),
                )
            )
            twitter_module.announced_release_ids.add(release.release_id)

    tracklist_candidates = [
        release for release in upcoming
        if release.release_type == "album"
        and release.release_id not in twitter_module.tracklist_revealed_ids
        and current_week + 1 <= int(release.week_release) <= current_week + 3
        and getattr(release, "tracks", None)
    ]
    if tracklist_candidates and not grammy_media_week:
        for release in random.sample(tracklist_candidates, min(random.randint(0, 2), len(tracklist_candidates))):
            artist = _ecosystem_artist_object(world, release.artist_name)
            if artist is None:
                continue
            tracklist_lines = "\n".join(
                f"{idx + 1}. {_compact_tweet_title(_tweet_release_title(track.title, release.artist_name), max_len=42)}"
                for idx, track in enumerate(list(release.tracks)[:12])
            )
            if len(release.tracks) > 12:
                tracklist_lines += f"\n+{len(release.tracks) - 12} more"
            template = random.choice(ARTIST_TRACKLIST_REVEAL)
            year, week = _year_week_from_world_week(int(release.week_release))
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author=artist.name,
                    username=artist_username(artist.name),
                    author_type="artist",
                    tweet_type="tracklist_reveal",
                    content=template.format(album=_compact_tweet_title(_tweet_release_title(release.title, release.artist_name)), tracklist=tracklist_lines, week=f"Y{year} W{week}"),
                    reply_to_id=None,
                    likes=random.randint(20000, 600000),
                    retweets=random.randint(8000, 200000),
                )
            )
            twitter_module.tracklist_revealed_ids.add(release.release_id)

    praise_cap = random.randint(2, 3)
    praise_count = 0
    shuffled_releases = list(this_week_releases)
    random.shuffle(shuffled_releases)
    for release in shuffled_releases:
        if grammy_media_week:
            break
        if praise_count >= praise_cap:
            break
        potential_praisers = [
            artist for artist in all_artists
            if release.artist_name in artist.friend_list and artist.name != release.artist_name
        ]
        if not potential_praisers:
            continue
        praiser = random.choice(potential_praisers)
        template = random.choice(ARTIST_FRIEND_PRAISE.get(release.release_type, ARTIST_FRIEND_PRAISE["single"]))
        tweets.append(
            Tweet(
                id=str(uuid4()),
                week=current_week,
                author=praiser.name,
                username=artist_username(praiser.name),
                author_type="artist",
                tweet_type="friend_praise",
                content=template.format(artist=release.artist_name, title=_compact_tweet_title(_tweet_release_title(release.title, release.artist_name))),
                reply_to_id=None,
                likes=random.randint(5000, 80000),
                retweets=random.randint(1000, 25000),
            )
        )
        praise_count += 1

    relevant_events = []
    relevant_events.extend(controversy_events)
    relevant_events.extend(world.weekly_events.get(current_week - 1, []))
    if relevant_events and not grammy_media_week:
        for event in random.sample(relevant_events, min(len(relevant_events), random.randint(4, 5))):
            if _is_growing_artist_name(event.instigator, world):
                continue
            if event.controversy_type in {2, 3} and _is_growing_artist_name(event.target, world):
                continue
            if event.controversy_type == 1:
                pool_key = "type1_positive" if _controversy_action_rep(event) > 0 else "type1_negative"
            elif event.controversy_type == 2:
                pool_key = "type2_response" if event.loop_count > 0 else "type2_beef"
            else:
                pool_key = "type3_critic"
            template = random.choice(FAN_CONTROVERSY_REACTIONS[pool_key])
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author="fan",
                    username=generate_fan_username(),
                    author_type="fan",
                    tweet_type="controversy_reaction",
                    content=template.format(instigator=event.instigator, target=event.target, loop=event.loop_count or 1),
                    reply_to_id=None,
                    likes=random.randint(200, 12000),
                    retweets=random.randint(50, 4000),
                    controversy_id=event.id,
                )
            )

    announced_upcoming = [release for release in upcoming if release.release_id in twitter_module.announced_release_ids]
    if announced_upcoming and not grammy_media_week:
        for release in random.sample(announced_upcoming, min(len(announced_upcoming), random.randint(5, 6))):
            artist_obj = _ecosystem_artist_object(world, release.artist_name)
            if artist_obj is None or artist_obj.is_growing:
                continue
            if artist_obj.popularity > 65:
                hype_key = "hype_high"
            elif artist_obj.popularity > 35:
                hype_key = "hype_medium"
            else:
                hype_key = "hype_low"
            template = random.choice(FAN_RELEASE_REACTIONS[hype_key])
            year, week = _year_week_from_world_week(int(release.week_release))
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author="fan",
                    username=generate_fan_username(),
                    author_type="fan",
                    tweet_type="hype",
                    content=template.format(artist=release.artist_name, title=_compact_tweet_title(_tweet_release_title(release.title, release.artist_name)), week=f"Y{year} W{week}"),
                    reply_to_id=None,
                    likes=random.randint(100, 8000),
                    retweets=random.randint(20, 2000),
                )
            )

    reception_pool = list(this_week_releases) + _releases_for_week(world, current_week - 1)
    eligible_releases = []
    for release in reception_pool:
        artist_obj = _ecosystem_artist_object(world, release.artist_name)
        if artist_obj is None or not artist_obj.is_growing:
            eligible_releases.append(release)
    if eligible_releases and not grammy_media_week:
        for release in random.sample(eligible_releases, min(len(eligible_releases), random.randint(8, 10))):
            score = _weekly_release_score(release)
            if score >= 8.5:
                pool_key = "love_album" if release.release_type in {"album", "mixtape"} else "love_song"
            elif score >= 6.5:
                pool_key = "like_song"
            elif score >= 4.5:
                pool_key = "mid_song"
            else:
                pool_key = "hate_album" if release.release_type in {"album", "mixtape"} else "hate_song"
            template = random.choice(FAN_RELEASE_RECEPTION[pool_key])
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author="fan",
                    username=generate_fan_username(),
                    author_type="fan",
                    tweet_type="reception",
                    content=template.format(artist=release.artist_name, title=_compact_tweet_title(_tweet_release_title(release.title, release.artist_name))),
                    reply_to_id=None,
                    likes=random.randint(150, 15000),
                    retweets=random.randint(30, 5000),
                )
            )

    featured_songs = [
        song for release in this_week_releases
        for song in _release_song_rows(release)
        if song["features"]
    ]
    if featured_songs and not grammy_media_week:
        for song in random.sample(featured_songs, min(len(featured_songs), random.randint(3, 4))):
            if _is_growing_artist_name(song["main_artist"], world):
                continue
            feature = random.choice(song["features"])
            fq = float(feature["verse_quality"])
            pool_key = "great_verse" if fq >= 8.0 else ("good_verse" if fq >= 6.0 else "bad_verse")
            template = random.choice(FAN_FEATURE_REACTIONS[pool_key])
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author="fan",
                    username=generate_fan_username(),
                    author_type="fan",
                    tweet_type="feature_reaction",
                    content=template.format(feature=feature["artist_name"], artist=song["main_artist"], title=_compact_tweet_title(song["name"])),
                    reply_to_id=None,
                    likes=random.randint(300, 25000),
                    retweets=random.randint(80, 8000),
                )
            )

    if all_artists and not grammy_media_week:
        rumour_pool = [artist for artist in all_artists if not artist.is_growing]
        for artist in random.sample(rumour_pool, min(len(rumour_pool), random.randint(2, 3))):
            possible_targets = [candidate for candidate in all_artists if candidate.name != artist.name]
            target_name = random.choice(possible_targets).name if possible_targets else "someone"
            template = random.choice(FAN_RUMOURS)
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author="fan",
                    username=generate_fan_username(),
                    author_type="fan",
                    tweet_type="rumour",
                    content=template.format(artist=artist.name, target=target_name, week=current_week + random.randint(2, 6)),
                    reply_to_id=None,
                    likes=random.randint(100, 5000),
                    retweets=random.randint(20, 1500),
                )
            )

    prediction_pool = [
        release for release in upcoming
        if current_week + 1 <= int(release.week_release) <= current_week + 3
    ]
    if prediction_pool and not grammy_media_week:
        for _ in range(random.randint(1, 2)):
            release = random.choice(prediction_pool)
            critic_name = random.choice(all_critics)
            artist_obj = _ecosystem_artist_object(world, release.artist_name)
            if artist_obj is not None and artist_obj.is_growing:
                continue
            artist_pop = artist_obj.popularity if artist_obj is not None else 50
            pool_key = "pre_release_positive" if artist_pop > 55 else "pre_release_skeptical"
            template = random.choice(CRITIC_TWEETS[pool_key])
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author=critic_name,
                    username=_critic_username(critic_name),
                    author_type="critic",
                    tweet_type="pre_release",
                    content=template.format(artist=release.artist_name, title=_compact_tweet_title(_tweet_release_title(release.title, release.artist_name)), week=release.week_release),
                    reply_to_id=None,
                    likes=random.randint(500, 8000),
                    retweets=random.randint(100, 2500),
                )
            )

    if this_week_releases:
        covered_releases = [
            release for release in this_week_releases
            if not _is_growing_artist_name(release.artist_name, world)
        ]
        sorted_releases = sorted(covered_releases, key=_weekly_release_score, reverse=True)
    else:
        sorted_releases = []
    if sorted_releases and not grammy_media_week:
        for pool_key, release in [("best_of_week", sorted_releases[0]), ("worst_of_week", sorted_releases[-1])]:
            if random.random() < 0.75:
                critic_name = random.choice(all_critics)
                template = random.choice(CRITIC_TWEETS[pool_key])
                tweets.append(
                    Tweet(
                        id=str(uuid4()),
                        week=current_week,
                        author=critic_name,
                        username=_critic_username(critic_name),
                        author_type="critic",
                        tweet_type=pool_key,
                        content=template.format(artist=release.artist_name, title=_compact_tweet_title(_tweet_release_title(release.title, release.artist_name)), score=_weekly_release_score(release)),
                        reply_to_id=None,
                        likes=random.randint(800, 12000),
                        retweets=random.randint(200, 4000),
                    )
                )

    if featured_songs and not grammy_media_week:
        for song in random.sample(featured_songs, min(len(featured_songs), random.randint(2, 3))):
            if _is_growing_artist_name(song["main_artist"], world):
                continue
            feature = random.choice(song["features"])
            fq = float(feature["verse_quality"])
            pool_key = "feature_strong" if fq >= 8.0 else ("feature_neutral" if fq >= 5.5 else "feature_weak")
            critic_name = random.choice(all_critics)
            template = random.choice(CRITIC_TWEETS[pool_key])
            tweets.append(
                Tweet(
                    id=str(uuid4()),
                    week=current_week,
                    author=critic_name,
                    username=_critic_username(critic_name),
                    author_type="critic",
                    tweet_type="feature_reaction",
                    content=template.format(feature=feature["artist_name"], artist=song["main_artist"], title=_compact_tweet_title(song["name"])),
                    reply_to_id=None,
                    likes=random.randint(600, 9000),
                    retweets=random.randint(150, 3000),
                )
            )

    for event in controversy_events:
        if grammy_media_week:
            continue
        if event.medium != "twitter" or event.controversy_type != 3:
            continue
        if _is_growing_artist_name(event.instigator, world):
            continue
        critic_name = event.target
        action_weight = abs(next((float(action["rep_i"]) for action in TYPE_3_ACTIONS if action["key"] == event.action_key), 3.0))
        pool_key = random.choice(["critic_response_doubledown", "critic_clapback_short"]) if action_weight >= 4 else random.choice(["critic_mic_drop", "critic_clapback_short"])
        template = random.choice(CRITIC_TWEETS[pool_key])
        tweets.append(
            Tweet(
                id=str(uuid4()),
                week=current_week,
                author=critic_name,
                username=_critic_username(critic_name),
                author_type="critic",
                tweet_type="controversy_response",
                content=template.format(target=event.instigator, score="low", title=event.song_title or "the project", artist=event.instigator),
                reply_to_id=None,
                likes=random.randint(1000, 20000),
                retweets=random.randint(300, 7000),
                controversy_id=event.id,
            )
        )

    tweets.sort(key=lambda tweet: tweet.likes + tweet.retweets * 2, reverse=True)
    twitter_module.add_tweets(current_week, tweets)
    return tweets


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


def process_side_hustle_week(artist):
    if not artist.side_hustle:
        return 0.0, 0.0, False
    weekly_pay = artist.side_hustle.weekly_pay
    weekly_fatigue = 0.0
    was_extra_tired = artist.fatigue > weekly_fatigue
    if was_extra_tired:
        extra_fatigue = artist.fatigue - weekly_fatigue
        weekly_pay = max(
            0.0,
            weekly_pay - ((extra_fatigue / 100.0) / 2.0 * artist.side_hustle.weekly_pay),
        )
    artist.money += weekly_pay
    artist.side_hustle.weeks_left -= 1
    if artist.side_hustle.weeks_left <= 0:
        print(f"{artist.side_hustle.job_name} shift contract ended.")
        artist.side_hustle = None
    return weekly_pay, weekly_fatigue, was_extra_tired


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
    print(f"Simulated forward to Year {artist.year}, Week {artist.week}.")
    print(
        f"Weekly payout: {money_fmt(net_income)} | "
        f"Streams: {total_streams:,} | "
        f"Management cut: {cut_pct:.1f}% ({money_fmt(management_cut)})"
    )
    if physical_income > 0:
        print(f"Physical sales income: {money_fmt(physical_income)}")
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
        y, w = _year_week_from_world_week(week_index)
        return f"Y{y} W{w}"

    title_width = max(len("Title"), max((len(r["title"]) for r in rows), default=5))
    artist_width = max(len("Artist"), max((len(r["artist"]) for r in rows), default=6))
    project_width = max(len("Project"), max((len(r["project"]) for r in rows), default=7))

    print("\nHOT 100 (Last Week Streams)")
    print(
        f"{'Rank':<4}  "
        f"{'Title':<{title_width}}  "
        f"{'Artist':<{artist_width}}  "
        f"{'Project':<{project_width}}  "
        f"{'Release Date':<12}  "
        f"{'Streams Last Week':>16}"
    )
    for i, r in enumerate(rows, 1):
        print(
            f"{i:<4}  "
            f"{r['title']:<{title_width}}  "
            f"{r['artist']:<{artist_width}}  "
            f"{r['project']:<{project_width}}  "
            f"{date_label(r['release_week']):<12}  "
            f"{r['streams']:>16,}"
        )


def _grammy_year_window(year: int) -> tuple[int, int]:
    # Projects released in weeks 1-48 (inclusive) count toward that year's Grammys.
    start = ((max(1, int(year)) - 1) * 52) + 1
    end = start + 47
    return start, end


def _avg_project_bg_from_tracks(tracks) -> dict[str, float]:
    totals = {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
    n = 0
    for t in tracks or []:
        bg_lyrics = getattr(t, "bg_lyrics", None)
        bg_vocals = getattr(t, "bg_vocals", None)
        bg_prod = getattr(t, "bg_production", None)
        bg_mix = getattr(t, "bg_mix", None)
        if bg_lyrics is None or bg_vocals is None or bg_prod is None or bg_mix is None:
            continue
        totals["lyrics"] += float(bg_lyrics)
        totals["vocals"] += float(bg_vocals)
        totals["prod"] += float(bg_prod)
        totals["mix"] += float(bg_mix)
        n += 1
    if n <= 0:
        return {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
    return {k: totals[k] / n for k in totals}


def _weighted_award_pick(nominees: list[dict]) -> dict | None:
    if not nominees:
        return None
    if len(nominees) == 1:
        return nominees[0]

    ordered = sorted(nominees, key=lambda n: float(n.get("rep", 0.0)), reverse=True)
    top = ordered[0]
    low = ordered[-1]
    mid = ordered[1:-1]

    pool = [top] + mid + [low]
    weights = [0.40]
    if mid:
        each = (1.0 - 0.40 - 0.04) / len(mid)
        weights += [each] * len(mid)
    weights += [0.04]
    return random.choices(pool, weights=weights, k=1)[0]


GRAMMY_CATEGORIES = [
    ("Best Hip Hop Album", lambda p: p["genre"] == "hip hop", 6),
    ("Best Pop Album", lambda p: p["genre"] == "pop", 6),
    ("Best Rock Album", lambda p: p["genre"] == "rock", 6),
    ("Best R&B/Soul Album", lambda p: p["genre"] in {"r&b", "soul"}, 6),
    ("Best Experimental Album", lambda p: p["genre"] == "experimental", 6),
]

GRAMMY_CATEGORY_ORDER = [
    "Best Hip Hop Album",
    "Best Pop Album",
    "Best Rock Album",
    "Best R&B/Soul Album",
    "Best Experimental Album",
    "Album of the Year",
    "Best Produced Album of the Year",
]


def _grammy_project_pool(player_artist, world: EcosystemWorld | None, year: int) -> list[dict]:
    start, end = _grammy_year_window(year)
    projects: list[dict] = []
    if world is not None:
        for artist_name, releases in world.release_history.items():
            for r in releases:
                wk = int(getattr(r, "week_number", 0))
                if wk < start or wk > end:
                    continue
                rtype = str(getattr(r, "release_type", ""))
                if rtype not in {"album", "mixtape"}:
                    continue
                tracks = list(getattr(r, "tracks", None) or ())
                bg = _avg_project_bg_from_tracks(tracks)
                rep = float(ARTIST_BASE_REPUTATION.get(artist_name, 50))
                projects.append(
                    {
                        "artist": artist_name,
                        "title": str(getattr(r, "title", "")),
                        "release_type": rtype,
                        "genre": str(getattr(r, "genre", "")),
                        "review": float(getattr(r, "review", 0.0)),
                        "week": wk,
                        "rep": rep,
                        "bg": bg,
                    }
                )

    for entry in player_artist.albums:
        if not entry.released:
            continue
        rel_week = 0
        for s in player_artist.singles:
            if s.released and str(getattr(s, "source_label", "")).startswith(f"Album: {entry.album.name}"):
                rel_week = int(s.release_week_index or 0)
                break
        if rel_week < start or rel_week > end:
            continue
        bg = {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
        if entry.album.songs:
            totals = {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
            n = 0
            for t in entry.album.songs:
                _ensure_song_bg_attrs(t, player_artist.skills)
                totals["lyrics"] += float(getattr(t, "bg_lyrics", 0.0) or 0.0)
                totals["vocals"] += float(getattr(t, "bg_vocals", 0.0) or 0.0)
                totals["prod"] += float(getattr(t, "bg_production", 0.0) or 0.0)
                totals["mix"] += float(getattr(t, "bg_mix", 0.0) or 0.0)
                n += 1
            if n:
                bg = {k: totals[k] / n for k in totals}
        projects.append(
            {
                "artist": player_artist.name,
                "title": entry.album.name,
                "release_type": "album",
                "genre": str(getattr(entry.album, "core_genre", "")),
                "review": float(getattr(entry, "average_review", 0.0) or 0.0),
                "week": int(rel_week),
                "rep": float(getattr(player_artist, "reputation", 50.0)),
                "bg": bg,
            }
        )
    return projects


def _ensure_grammy_results(player_artist, world: EcosystemWorld | None, year: int) -> dict | None:
    if year in player_artist.grammy_state:
        return player_artist.grammy_state[year]
    projects = _grammy_project_pool(player_artist, world, year)
    if not projects:
        return None

    def top_by_review(items: list[dict], n: int) -> list[dict]:
        return sorted(items, key=lambda x: float(x.get("review", 0.0)), reverse=True)[:n]

    def top_by_prod(items: list[dict], n: int) -> list[dict]:
        return sorted(items, key=lambda x: float(x.get("bg", {}).get("prod", 0.0)), reverse=True)[:n]

    results = {}
    for name, pred, take in GRAMMY_CATEGORIES:
        pool = [p for p in projects if pred(p)]
        nominees = top_by_review(pool, take)
        results[name] = {"nominees": nominees, "winner": _weighted_award_pick(nominees)}

    aoty_pool = [p for p in projects if p["release_type"] == "album"]
    aoty_nominees = top_by_review(aoty_pool, 10)
    results["Album of the Year"] = {"nominees": aoty_nominees, "winner": _weighted_award_pick(aoty_nominees)}

    prod_nominees = top_by_prod(projects, 10)
    results["Best Produced Album of the Year"] = {"nominees": prod_nominees, "winner": _weighted_award_pick(prod_nominees)}
    player_artist.grammy_state[year] = results
    return results


def _generate_grammy_news(player_artist, world: EcosystemWorld | None, current_week: int) -> list[NewsReport]:
    year, week = _year_week_from_world_week(current_week)
    if week not in {49, 50, 51, 52}:
        return []
    if world is not None and not hasattr(world, "_grammy_news_published"):
        world._grammy_news_published = set()
    published = getattr(world, "_grammy_news_published", set()) if world is not None else set()
    marker = (year, week)
    if marker in published:
        return []
    results = _ensure_grammy_results(player_artist, world, year)
    if not results:
        return []

    reports: list[NewsReport] = []
    if week == 49:
        nomination_blocks = [
            (category, list(results.get(category, {}).get("nominees") or []))
            for category in GRAMMY_CATEGORY_ORDER
        ]
        nomination_blocks = [(category, nominees) for category, nominees in nomination_blocks if nominees]
        if nomination_blocks:
            lead_category, lead_nominees = max(
                nomination_blocks,
                key=lambda item: float(item[1][0].get("review", 0.0)) if item[1] else 0.0,
            )
            lead = lead_nominees[0]
            headline = random.choice(GRAMMY_NEWS_TEMPLATES["nomination_roundup"]).format(
                category=lead_category,
                artist=lead["artist"],
                title=lead["title"],
            )
            reports.append(_build_news_report(current_week, "grammy", headline, artist=lead["artist"], subject=lead_category))

        remaining_blocks = [
            item for item in nomination_blocks
            if item[0] != (reports[0].subject if reports else "")
        ]
        for category, nominees in random.sample(remaining_blocks, min(3, len(remaining_blocks))):
            nominees = list(results.get(category, {}).get("nominees") or [])
            if not nominees:
                continue
            lead = nominees[0]
            pool_key = random.choice(["nominations", "nomination_snub", "nomination_insider"])
            headline = random.choice(GRAMMY_NEWS_TEMPLATES[pool_key]).format(
                category=category,
                artist=lead["artist"],
                title=lead["title"],
            )
            reports.append(_build_news_report(current_week, "grammy", headline, artist=lead["artist"], subject=category))
    announced_categories = _grammy_categories_announced_this_week(week)
    if announced_categories:
        winners = []
        for category in announced_categories:
            winner = results.get(category, {}).get("winner")
            if not winner:
                continue
            winners.append((category, winner))
            headline = random.choice(GRAMMY_NEWS_TEMPLATES["winner"]).format(
                year=year,
                category=category,
                artist=winner["artist"],
                title=winner["title"],
            )
            reports.append(_build_news_report(current_week, "grammy", headline, artist=winner["artist"], subject=category))
        if winners and week == 52:
            for category, winner in random.sample(winners, min(2, len(winners))):
                pool_key = random.choice(["insider", "rumour"])
                headline = random.choice(GRAMMY_NEWS_TEMPLATES[pool_key]).format(
                    year=year,
                    category=category,
                    artist=winner["artist"],
                    title=winner["title"],
                )
                reports.append(_build_news_report(current_week, "grammy", headline, artist=winner["artist"], subject=category))
            category, winner = random.choice(winners)
            rivals = [
                nominee["artist"]
                for nominee in results.get(category, {}).get("nominees", [])
                if nominee["artist"] != winner["artist"]
            ]
            if rivals:
                target = random.choice(rivals)
                headline = random.choice(GRAMMY_NEWS_TEMPLATES["feud"]).format(
                    year=year,
                    category=category,
                    artist=winner["artist"],
                    target=target,
                    title=winner["title"],
                )
                reports.append(_build_news_report(current_week, "grammy", headline, artist=winner["artist"], target=target, subject=category))
    if world is not None:
        published.add(marker)
        world._grammy_news_published = published
    return reports


def grammy_awards_menu(player_artist, world: EcosystemWorld | None):
    year = int(player_artist.year)
    if int(player_artist.week) <= 48:
        print("\nGRAMMYS")
        print("Not generated yet. Come back in weeks 49-52.")
        return

    start, end = _grammy_year_window(year)

    projects: list[dict] = []

    # Ecosystem projects.
    if world is not None:
        for artist_name, releases in world.release_history.items():
            for r in releases:
                wk = int(getattr(r, "week_number", 0))
                if wk < start or wk > end:
                    continue
                rtype = str(getattr(r, "release_type", ""))
                if rtype not in {"album", "mixtape"}:
                    continue
                tracks = list(getattr(r, "tracks", None) or ())
                bg = _avg_project_bg_from_tracks(tracks)
                rep = float(ARTIST_BASE_REPUTATION.get(artist_name, 50))
                projects.append(
                    {
                        "artist": artist_name,
                        "title": str(getattr(r, "title", "")),
                        "release_type": rtype,
                        "genre": str(getattr(r, "genre", "")),
                        "review": float(getattr(r, "review", 0.0)),
                        "week": wk,
                        "rep": rep,
                        "bg": bg,
                    }
                )

    # Player albums (albums only).
    for entry in player_artist.albums:
        if not entry.released:
            continue
        rel_week = 0
        for s in player_artist.singles:
            if s.released and str(getattr(s, "source_label", "")).startswith(f"Album: {entry.album.name}"):
                rel_week = int(s.release_week_index or 0)
                break
        if rel_week < start or rel_week > end:
            continue
        bg = {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
        if entry.album.songs:
            totals = {"lyrics": 0.0, "vocals": 0.0, "prod": 0.0, "mix": 0.0}
            n = 0
            for t in entry.album.songs:
                _ensure_song_bg_attrs(t, player_artist.skills)
                totals["lyrics"] += float(getattr(t, "bg_lyrics", 0.0) or 0.0)
                totals["vocals"] += float(getattr(t, "bg_vocals", 0.0) or 0.0)
                totals["prod"] += float(getattr(t, "bg_production", 0.0) or 0.0)
                totals["mix"] += float(getattr(t, "bg_mix", 0.0) or 0.0)
                n += 1
            if n:
                bg = {k: totals[k] / n for k in totals}
        projects.append(
            {
                "artist": player_artist.name,
                "title": entry.album.name,
                "release_type": "album",
                "genre": str(getattr(entry.album, "core_genre", "")),
                "review": float(getattr(entry, "average_review", 0.0) or 0.0),
                "week": int(rel_week),
                "rep": float(getattr(player_artist, "reputation", 50.0)),
                "bg": bg,
            }
        )

    if not projects:
        print("\nGRAMMYS")
        print("No eligible projects released this year (albums/mixtapes only).")
        return

    def top_by_review(items: list[dict], n: int) -> list[dict]:
        return sorted(items, key=lambda x: float(x.get("review", 0.0)), reverse=True)[:n]

    def top_by_prod(items: list[dict], n: int) -> list[dict]:
        return sorted(items, key=lambda x: float(x.get("bg", {}).get("prod", 0.0)), reverse=True)[:n]

    categories = [
        ("Best Hip Hop Album", lambda p: p["genre"] == "hip hop", 6),
        ("Best Pop Album", lambda p: p["genre"] == "pop", 6),
        ("Best Rock Album", lambda p: p["genre"] == "rock", 6),
        ("Best R&B/Soul Album", lambda p: p["genre"] in {"r&b", "soul"}, 6),
        ("Best Experimental Album", lambda p: p["genre"] == "experimental", 6),
    ]

    if year not in player_artist.grammy_state:
        results = {}
        for name, pred, take in categories:
            pool = [p for p in projects if pred(p)]
            nominees = top_by_review(pool, take)
            results[name] = {"nominees": nominees, "winner": _weighted_award_pick(nominees)}

        aoty_pool = [p for p in projects if p["release_type"] == "album"]
        aoty_nominees = top_by_review(aoty_pool, 10)
        results["Album of the Year"] = {"nominees": aoty_nominees, "winner": _weighted_award_pick(aoty_nominees)}

        prod_nominees = top_by_prod(projects, 10)
        results["Best Produced Album of the Year"] = {"nominees": prod_nominees, "winner": _weighted_award_pick(prod_nominees)}

        player_artist.grammy_state[year] = results

    results = player_artist.grammy_state[year]

    reveal_week = int(player_artist.week)
    # Reveal winners gradually in the last 4 weeks.
    if reveal_week >= 52:
        winners_revealed = 7
    elif reveal_week >= 51:
        winners_revealed = 5
    elif reveal_week >= 50:
        winners_revealed = 3
    else:
        winners_revealed = 1

    order = [
        "Best Hip Hop Album",
        "Best Pop Album",
        "Best Rock Album",
        "Best R&B/Soul Album",
        "Best Experimental Album",
        "Album of the Year",
        "Best Produced Album of the Year",
    ]

    print(f"\nGRAMMYS | Year {year}")
    print(f"Eligibility window: Y{year} W1 to W48")

    for idx, cat in enumerate(order, 1):
        block = results.get(cat, {"nominees": [], "winner": None})
        nominees = block.get("nominees") or []
        print(f"\n{idx}. {cat}")
        if not nominees:
            print("- No nominees this year.")
            continue

        print("Nominees:")
        for n in nominees:
            y, w = _year_week_from_world_week(int(n.get("week", 0)))
            date = f"Y{y} W{w}" if n.get("week", 0) else "-"
            bg = n.get("bg", {})
            print(
                f"- {n['title']} ({n['release_type']}) | {n['artist']} | review {n['review']:.1f}/10 | "
                f"rep {int(n['rep'])} | avg prod {bg.get('prod', 0.0):.1f} | {date}"
            )

        if idx <= winners_revealed:
            winner = block.get("winner")
            if not winner:
                continue
            bg = winner.get("bg", {})
            print("\nWinner:")
            print(
                f"{winner['artist']} takes it with '{winner['title']}' ({winner['release_type']}). "
                f"Review {winner['review']:.1f}/10 | rep {int(winner['rep'])} | "
                f"avg lyrics {bg.get('lyrics', 0.0):.1f} | avg vocals {bg.get('vocals', 0.0):.1f} | "
                f"avg prod {bg.get('prod', 0.0):.1f} | avg mix {bg.get('mix', 0.0):.1f}"
            )
            print(
                random.choice(
                    [
                        "The room knew before the envelope opened.",
                        "One of those wins that feels inevitable in hindsight.",
                        "A clean win. No weirdness. Just a strong year-end statement.",
                        "The kind of project people will reference for a while.",
                    ]
                )
            )
        else:
            print("\nWinner: (not announced yet)")


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


def _physical_stock_summary(editions: list[PhysicalEdition]) -> str:
    if not editions:
        return "no physical stock"
    parts = []
    for edition in editions:
        total_cost = float(getattr(edition, "total_manufacturing_cost", 0.0) or 0.0)
        cost_label = f" | mfg {money_fmt(total_cost)}" if total_cost > 0 else ""
        parts.append(
            f"{_physical_edition_label(edition)}: {edition.copies_remaining}/{edition.copies_created} left @ "
            f"{money_fmt(edition.effective_price())}{cost_label}"
        )
    return " | ".join(parts)


def _manage_physical_editions(
    artist: Artist,
    *,
    title: str,
    release_type: str,
    quality: float,
    popularity: float,
    editions: list[PhysicalEdition],
) -> None:
    while True:
        options = [
            f"Restock discs ({_physical_stock_summary([e for e in editions if e.format_name == 'disc' and not getattr(e, 'limited_edition', False)])})",
            f"Restock vinyls ({_physical_stock_summary([e for e in editions if e.format_name == 'vinyl' and not getattr(e, 'limited_edition', False)])})",
            f"Restock limited discs ({_physical_stock_summary([e for e in editions if e.format_name == 'disc' and getattr(e, 'limited_edition', False)])})",
            f"Restock limited vinyls ({_physical_stock_summary([e for e in editions if e.format_name == 'vinyl' and getattr(e, 'limited_edition', False)])})",
            "Back",
        ]
        choice = choose_from_list(f"Physical copies | {title}", options, allow_cancel=False)
        if choice is None or choice == 4:
            return
        format_name = "disc" if choice in {0, 2} else "vinyl"
        limited_edition = choice in {2, 3}
        existing = next(
            (
                edition
                for edition in editions
                if edition.format_name == format_name
                and bool(getattr(edition, "limited_edition", False)) == bool(limited_edition)
            ),
            None,
        )
        fair_price = _physical_fair_price(release_type, format_name, quality, popularity)
        if limited_edition:
            fair_price = round(fair_price * 1.35, 2)
        default_price = existing.list_price if existing is not None else fair_price
        default_discount = int(round((existing.discount_pct if existing is not None else 0.0) * 100))
        base_unit_cost = float(PHYSICAL_UNIT_COSTS[format_name]) * (
            float(PHYSICAL_LIMITED_COST_MULT) if limited_edition else 1.0
        )
        edition_label = f"limited {format_name}" if limited_edition else format_name
        print(
            f"\nManufacturing {edition_label}: base {money_fmt(base_unit_cost)} each. "
            f"Bulk discounts: 1,000+ 5% | 5,000+ 10% | 25,000+ 15% | 100,000+ 20%."
        )
        copies = prompt_int(
            f"How many {edition_label} copies to manufacture? ",
            0,
            200_000,
            100 if release_type == "single" else 250,
        )
        unit_cost = _physical_unit_cost(format_name, copies, limited_edition)
        bulk_discount = _physical_bulk_discount(copies)
        manufacturing_cost = float(copies) * unit_cost
        print(
            f"Manufacturing cost: {copies:,} x {money_fmt(unit_cost)}"
            f"{f' ({int(bulk_discount * 100)}% bulk discount)' if bulk_discount else ''} = "
            f"{money_fmt(manufacturing_cost)}"
        )
        price = prompt_float(
            f"Sale price per {edition_label} copy ({money_fmt(fair_price)} fair price): ",
            0.5,
            500.0,
            default_price,
        )
        discount_pct = prompt_int("Discount %: ", 0, 80, default_discount) / 100.0
        if copies > 0 and artist.money < manufacturing_cost:
            print(f"You need {money_fmt(manufacturing_cost)} to manufacture that run.")
            input("Press Enter...")
            continue
        if copies > 0:
            artist.money -= manufacturing_cost
        if existing is None:
            editions.append(
                PhysicalEdition(
                    format_name=format_name,
                    unit_cost=unit_cost,
                    list_price=float(price),
                    discount_pct=float(discount_pct),
                    limited_edition=bool(limited_edition),
                    copies_created=int(copies),
                    copies_remaining=int(copies),
                    total_manufacturing_cost=float(manufacturing_cost),
                )
            )
        else:
            existing.list_price = float(price)
            existing.discount_pct = float(discount_pct)
            existing.unit_cost = float(unit_cost)
            existing.copies_created += int(copies)
            existing.copies_remaining += int(copies)
            existing.total_manufacturing_cost = float(getattr(existing, "total_manufacturing_cost", 0.0) or 0.0) + float(manufacturing_cost)
        print(
            f"{title}: {edition_label} stock updated. "
            f"Manufacturing cost {money_fmt(manufacturing_cost)} | "
            f"sale price {money_fmt(_effective_sale_price(price, discount_pct))} after discount."
        )
        input("Press Enter...")


def manage_physical_copies_menu(artist: Artist):
    options: list[tuple[str, object, str, float]] = []
    labels: list[str] = []
    for entry in artist.singles:
        if not entry.released or str(getattr(entry, "source_label", "")).startswith("Album:"):
            continue
        labels.append(
            f"Single | {entry.song.name} | sales {entry.total_digital_sales + entry.total_physical_sales:,} | {_physical_stock_summary(entry.physical_editions)}"
        )
        options.append(("single", entry, "single", float(entry.song.quality)))
    for album_entry in artist.albums:
        if not album_entry.released:
            continue
        snapshot = _player_album_sales_snapshot(artist, album_entry)
        release_type = "deluxe" if album_entry.deluxe_of else "album"
        avg_quality = (
            sum(float(song.quality) for song in album_entry.album.songs) / max(1, len(album_entry.album.songs))
            if album_entry.album.songs else float(album_entry.average_review or 5.0)
        )
        labels.append(
            f"{release_type.title()} | {album_entry.album.name} | sales {snapshot.total_sales:,} | {_physical_stock_summary(album_entry.physical_editions)}"
        )
        options.append((release_type, album_entry, release_type, float(avg_quality)))
    if not options:
        print("\nYou need a released single or album before you can press physical copies.")
        return
    idx = choose_from_list("Manage physical copies", labels, allow_cancel=True)
    if idx is None:
        return
    kind, item, release_type, quality = options[idx]
    if kind == "single":
        _manage_physical_editions(
            artist,
            title=item.song.name,
            release_type="single",
            quality=quality,
            popularity=float(artist.popularity),
            editions=item.physical_editions,
        )
    else:
        _manage_physical_editions(
            artist,
            title=item.album.name,
            release_type=release_type,
            quality=quality,
            popularity=float(artist.popularity),
            editions=item.physical_editions,
        )


def _print_sales_line(label: str, sales: SalesSnapshot, editions: list[PhysicalEdition] | None = None) -> None:
    print(
        f"{label} | digital {sales.total_digital:,} total / {sales.last_week_digital:,} last week | "
        f"physical {sales.total_physical:,} total / {sales.last_week_physical:,} last week | "
        f"all {sales.total_sales:,} total | fw {sales.first_week_sales:,} | "
        f"{_riaa_certification_label(sales.total_sales)}"
    )
    if editions:
        spent, revenue, profit, margin = _physical_financials(editions)
        print(
            f"  physical money: spent {money_fmt(spent)} | received {money_fmt(revenue)} | "
            f"profit {money_fmt(profit)} | margin {margin:.1f}%"
        )


def view_player_sales_menu(artist: Artist):
    released_singles = [
        entry
        for entry in artist.singles
        if entry.released and not str(getattr(entry, "source_label", "")).startswith("Album:")
    ]
    released_albums = [entry for entry in artist.albums if entry.released]
    if not released_singles and not released_albums:
        print("\nNo released music has sales yet.")
        return

    while True:
        options = ["Singles", "Albums", "Back"]
        choice = choose_from_list("View Sales", options, allow_cancel=False)
        if choice == 0:
            if not released_singles:
                print("\nNo released singles.")
                input("Press Enter...")
                continue
            print("\nSingle Sales")
            for entry in released_singles:
                _print_sales_line(entry.song.name, _player_song_sales_snapshot(entry), entry.physical_editions)
                if entry.physical_editions:
                    print(f"  stock: {_physical_stock_summary(entry.physical_editions)}")
            input("\nPress Enter to go back...")
        elif choice == 1:
            if not released_albums:
                print("\nNo released albums.")
                input("Press Enter...")
                continue
            print("\nAlbum Sales")
            for album_entry in released_albums:
                release_type = "Deluxe" if album_entry.deluxe_of else "Album"
                album_sales = _player_album_sales_snapshot(artist, album_entry)
                _print_sales_line(f"{release_type} | {album_entry.album.name}", album_sales, album_entry.physical_editions)
                if album_entry.physical_editions:
                    print(f"  stock: {_physical_stock_summary(album_entry.physical_editions)}")
                linked_tracks = [
                    linked_entry
                    for song in album_entry.album.songs
                    for linked_entry in [next((e for e in artist.singles if e.song is song and e.released), None)]
                    if linked_entry is not None
                ]
                if linked_tracks:
                    print("  Songs")
                    for track in linked_tracks:
                        track_sales = _player_song_sales_snapshot(track)
                        print(
                            f"  - {track.song.name}: digital {track_sales.total_digital:,} total / "
                            f"{track_sales.last_week_digital:,} last week | physical {track_sales.total_physical:,} total / "
                            f"{track_sales.last_week_physical:,} last week | all {track_sales.total_sales:,}"
                        )
            input("\nPress Enter to go back...")
        else:
            return


def work_side_hustle(artist):
    if artist.side_hustle:
        print(
            f"You are already working at {artist.side_hustle.job_name} for "
            f"{artist.side_hustle.weeks_left} more weeks."
        )
        return
    options = [
        f"{job['name']} | {money_fmt(job['pay'])}/week | fatigue {job['fatigue']:.1f}/week | 12 weeks"
        for job in SIDE_HUSTLES
    ]
    idx = choose_from_list("Choose a side hustle shift", options, allow_cancel=True)
    if idx is None:
        return
    job = SIDE_HUSTLES[idx]
    artist.side_hustle = JobContract(
        job_name=job["name"],
        weekly_pay=job["pay"],
        weekly_fatigue=job["fatigue"],
        weeks_left=12,
    )
    print(
        f"You started a 12-week job at {job['name']}. "
        f"It pays {money_fmt(job['pay'])} each week."
    )


def contract_terms():
    return {
        0: {"label": "4 Weeks", "weeks": 4, "billing_every": 1, "payments": 4},
        1: {"label": "6 Months", "weeks": 24, "billing_every": 4, "payments": 6},
        2: {"label": "Yearly", "weeks": 48, "billing_every": 24, "payments": 2},
    }


def build_contract(company, term_info, fee_multiplier=1.0, cut_delta=0.0):
    total_cost = company["yearly_cost"] * (term_info["weeks"] / 48.0) * fee_multiplier
    billing_amount = total_cost / term_info["payments"]
    cut = max(3.0, company["base_cut"] + cut_delta)
    return ManagementContract(
        company_name=company["name"],
        term_label=term_info["label"],
        weeks_left=term_info["weeks"],
        billing_amount=billing_amount,
        billing_every_weeks=term_info["billing_every"],
        weeks_until_payment=term_info["billing_every"],
        weekly_popularity_range=company["pop_gain"],
        current_weekly_popularity=random.uniform(*company["pop_gain"]),
        stream_cut_pct=cut,
    )


def negotiate_contract(company, term_info):
    base_contract = build_contract(company, term_info)
    print(f"\n{company['name']}: Here's our opening ask.")
    print(
        f"{company['name']}: {term_info['label']} deal, "
        f"{money_fmt(base_contract.billing_amount)} every {base_contract.billing_every_weeks} week(s), "
        f"{company['base_cut']:.1f}% stream cut, "
        f"weekly base popularity in the {company['pop_gain'][0]:.1f}% to {company['pop_gain'][1]:.1f}% range."
    )
    if term_info["label"] == "Yearly":
        print(
            f"{company['name']}: For yearly, we take the first 24 weeks upfront and the second half at week 24."
        )

    if prompt_text("Negotiate this deal? (y/n): ", "n").lower() != "y":
        return base_contract, base_contract.billing_amount

    print(f"\nYou: I want to discuss the money and cut.")
    fee_change = prompt_int(
        "Fee change % (negative asks them to lower price, positive offers more): ",
        -40,
        40,
    )
    cut_change = prompt_int(
        "Cut change in points (negative asks them to take less, positive offers more): ",
        -10,
        10,
    )

    fee_multiplier = 1.0 + (fee_change / 100.0)
    pressure_score = (max(0, -fee_change) * 0.9) + (max(0, -cut_change) * 6.0)
    goodwill_score = (max(0, fee_change) * 0.45) + (max(0, cut_change) * 3.0)
    patience = random.uniform(10.0, 22.0) / company["strictness"]

    # A large extra buffer means the company sees the ask as insulting, not just aggressive.
    if pressure_score > patience + NEGOTIATION_WALK_AWAY_BUFFER:
        print(f"{company['name']}: Absolutely not. That is insulting.")
        print(f"{company['name']}: We are not running a charity and we are not desperate.")
        print(f"{company['name']}: Come back when you want a real conversation.")
        return None, 0.0

    if pressure_score > patience:
        counter_fee_multiplier = 1.0 + min(0.18, max(-0.08, fee_change / 220.0))
        counter_cut_delta = max(-2.0, min(3.0, cut_change / 3.0))
        counter = build_contract(company, term_info, counter_fee_multiplier, counter_cut_delta)
        print(f"{company['name']}: No, not on those terms.")
        print(
            f"{company['name']}: Best we can do is {money_fmt(counter.billing_amount)} every "
            f"{counter.billing_every_weeks} week(s) and {counter.stream_cut_pct:.1f}%."
        )
        if choose_from_list(
            "Accept the counter?",
            ["Accept counter", "Walk away"],
            allow_cancel=False,
        ) == 0:
            upfront = counter.billing_amount if counter.term_label == "Yearly" else 0.0
            return counter, upfront
        print("You walk away from the table.")
        return None, 0.0

    final = build_contract(company, term_info, fee_multiplier, cut_change)
    if goodwill_score > 0:
        print(f"{company['name']}: That's generous. We can absolutely do that.")
        print(f"{company['name']}: Easy money for us. Pleasure doing business.")
    else:
        print(f"{company['name']}: Fine. We can make that work.")
        print(f"{company['name']}: Do not expect us to move any further.")
    upfront = final.billing_amount if final.term_label == "Yearly" else 0.0
    return final, upfront


def management_menu(artist):
    if artist.management:
        print(
            f"\nCurrent management: {artist.management.company_name} | "
            f"{artist.management.term_label} | billing {money_fmt(artist.management.billing_amount)} "
            f"every {artist.management.billing_every_weeks} week(s) | "
            f"weekly base popularity {artist.management.current_weekly_popularity:.1f}% | "
            f"stream cut {artist.management.stream_cut_pct:.1f}%"
        )
        if choose_from_list(
            "Management options",
            ["Keep current contract", "Drop current contract"],
            allow_cancel=True,
        ) == 1:
            print(f"You ended the contract with {artist.management.company_name}.")
            artist.management = None
        return

    company_idx = choose_from_list(
        "Choose a management company",
        [
            f"{c['name']} | yearly {money_fmt(c['yearly_cost'])} | "
            f"weekly popularity +{c['pop_gain'][0]:.0f}-{c['pop_gain'][1]:.0f}%"
            for c in MANAGEMENT_COMPANIES
        ],
        allow_cancel=True,
    )
    if company_idx is None:
        return
    company = MANAGEMENT_COMPANIES[company_idx]

    term_choice = choose_from_list("Choose contract term", ["4 weeks", "6 months", "Yearly"], allow_cancel=True)
    if term_choice is None:
        return
    term_info = contract_terms()[term_choice]
    contract, upfront_due = negotiate_contract(company, term_info)
    if contract is None:
        return
    if artist.money < upfront_due:
        print(
            f"You need at least {money_fmt(upfront_due)} available to take this contract."
        )
        return
    artist.money -= upfront_due
    artist.management = contract
    print(
        f"Signed with {contract.company_name}. "
        f"Paid {money_fmt(upfront_due)} upfront | "
        f"base popularity {contract.current_weekly_popularity:.1f}% this week | "
        f"stream cut {contract.stream_cut_pct:.1f}%"
    )


def show_shawtify_streams(artist):
    released = [entry for entry in artist.singles if entry.released]
    if not released:
        print("\nNo released songs are tracking streams yet.")
        return

    print("\nSHAWTIFY STREAMS")
    for idx, entry in enumerate(
        sorted(released, key=lambda e: e.total_streams, reverse=True), 1
    ):
        sales = _player_song_sales_snapshot(entry)
        catchiness = getattr(entry.song, "catchiness", None)
        catchy_label = f" | catchy {catchiness}" if catchiness is not None else ""
        v = getattr(entry.song, "virality", None)
        m = getattr(entry.song, "maturity_weeks", None)
        viral_label = ""
        if v is not None and m is not None and v >= 2.0:
            remaining = max(0, int(m - entry.weeks_since_release))
            viral_label = f" | viral {v} (matures in {remaining}w)"
        review = (
            f" | avg review {entry.average_review}/10"
            if entry.average_review is not None
            else ""
        )
        print(
            f"- {idx}. {entry.song.name} [{entry.source_label}] | "
            f"total {entry.total_streams:,} | this week {entry.last_week_streams:,} | "
            f"sales {sales.total_sales:,} total / {sales.last_week_sales:,} last week / "
            f"{_first_week_sales_value(sales.last_week_sales, sales.first_week_sales):,} first week | "
            f"{_riaa_certification_label(sales.total_sales)}{catchy_label}{viral_label}{review}"
        )


def view_ecosystem_artists():
    raise RuntimeError("Use view_ecosystem_artists_menu(world) instead.")


def _year_week_from_world_week(world_week):
    if world_week <= 0:
        return 1, 1
    year = ((world_week - 1) // 52) + 1
    week = ((world_week - 1) % 52) + 1
    return year, week


def _player_week_index(artist):
    return ((artist.year - 1) * 52) + artist.week


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
    year, week = _year_week_from_world_week(week_index)
    return f"Y{year} W{week}"


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
        f"{'User':>6}  {'Votes':>9}  {'Date':<8}  {'Tracks':>6}"
    )
    for idx, row in enumerate(rows[:limit], 1):
        print(
            f"{idx:>3}  {row['title']:<{title_w}}  {row['artist']:<{artist_w}}  "
            f"{row['release_type']:<7}  {row['score']:>4.1f}/10  {row['votes']:>9,}  "
            f"{_imdb_release_date_label(row['release_week']):<8}  {row['track_count']:>6}"
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
        f"{'User':>6}  {'Votes':>9}  {'Date':<8}  {'Streams':>12}"
    )
    for idx, row in enumerate(rows[:limit], 1):
        print(
            f"{idx:>3}  {row['title']:<{title_w}}  {row['artist']:<{artist_w}}  {row['project']:<{project_w}}  "
            f"{row['score']:>4.1f}/10  {row['votes']:>9,}  {_imdb_release_date_label(row['release_week']):<8}  "
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
        f"{'User':>6}  {'Rec':>5}  {'Cred':>5}  {'Brut':>5}  {'Date':<8}  {'Streams':>12}"
    )
    for idx, row in enumerate(rows[:limit], 1):
        print(
            f"{idx:>3}  {row['title']:<{title_w}}  {row['artist']:<{artist_w}}  {row['target']:<{target_w}}  "
            f"{row['score']:>4.1f}/10  {row['reception']:>4.1f}  {row['credibility']:>4.1f}  "
            f"{row['brutality']:>4.1f}  {_imdb_release_date_label(row['release_week']):<8}  {row['streams']:>12,}"
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


def _ecosystem_seed_by_name(name):
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        if seed.name == name:
            return seed
    return None


def _friendliness_tier(friendliness):
    if friendliness >= 70:
        return "high"
    if friendliness <= 30:
        return "low"
    return "mid"


def _stable_rng_for_label(label: str) -> random.Random:
    h = 0
    for ch in str(label):
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return random.Random(h)


def _roll_bg_attr_from_skill_rng(skill_value: float, rng: random.Random) -> float:
    s = float(skill_value) / 10.0
    lo = max(1.0, s - 2.0)
    hi = max(lo, s)
    return round(rng.uniform(lo, hi), 1)


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


def _new_request_id(week_index):
    return f"FR-{week_index}-{random.randint(1000, 9999)}"


def _feature_offer_money(player_artist):
    avg_skill = sum(float(player_artist.skills[s]) for s in SKILLS) / float(len(SKILLS))
    base = 250.0 + (avg_skill * 22.0)
    return round(random.uniform(base * 0.75, base * 1.35), 2)


def _relationship_score(artist, target_name):
    state = artist.relationships.get(target_name)
    if not state:
        return 0.0
    return float(getattr(state, "score", 0.0))


def _apply_relationship_delta(artist, target_name, delta):
    if TEST_RELATIONSHIP_LOCK and getattr(artist, "_relationship_lock", False):
        state = artist.relationships.get(target_name)
        if state:
            state.score = 100.0
        return
    state = artist.relationships.get(target_name)
    if not state:
        state = RelationshipState(score=10.0)
        artist.relationships[target_name] = state
    state.score = clamp_meter(float(state.score) + float(delta))


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


def _print_ecosystem_new_releases(world: EcosystemWorld):
    year, week = _year_week_from_world_week(world.week_number)
    print(f"\nNew releases | Year {year} Week {week}")
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
                y, w = _year_week_from_world_week(s.release_week)
                date_label = f"Y{y} W{w}"
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
        year, week = _year_week_from_world_week(release.week_number)
        date_label = f"Y{year} W{week}"
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
            year, week = _year_week_from_world_week(r.week_number)
            date_label = f"Y{year} W{week}"
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
            year, week = _year_week_from_world_week(week_number)
            items = calendar.get(week_number, [])
            options.append(f"Y{year} W{week} | {len(items)} announced release{'s' if len(items) != 1 else ''}")

        idx = choose_from_list("Choose a week", options + ["Back"], allow_cancel=False)
        if idx is None or idx == len(options):
            return

        week_number = week_keys[idx]
        year, week = _year_week_from_world_week(week_number)
        items = calendar.get(week_number, [])
        print(f"\nY{year} W{week} Release Window")
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
    year, week = _year_week_from_world_week(event.week)
    type_label = _news_type_label(event)
    medium = str(event.medium).upper()
    border = _news_player_border(event, player_artist)
    channel, reporter = _event_channel_and_reporter(event)
    print("+" + "-" * 72 + "+")
    print(f"| [{type_label:<10}] [{medium:<17}] Week Y{year} W{week:<19}|")
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
            print(f"\nINDUSTRY NEWS | week {current_week}")
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


def twitter_menu(world: EcosystemWorld | None):
    _ensure_twitter_state(world)
    current_week = int(getattr(world, "week_number", 0)) if world is not None else 0
    twitter_module = world.twitter_module if world is not None else TwitterModule()
    while True:
        choice = choose_from_list("TWITTER", ["This Week", "Archive", "Back"], allow_cancel=False)
        if choice == 2:
            return
        if choice == 0:
            tweets = twitter_module.get_tweets(current_week)
            if not tweets:
                print("No tweets this week.")
                continue
            _display_twitter_feed(tweets, current_week, limit=20)
            input("Press Enter to go back...")
            continue
        search = prompt_text("Filter by author / type / text (blank = all): ", "").strip().lower()
        tweets = twitter_module.get_all_tweets(260, current_week)
        filtered = []
        for week, tweet in tweets:
            haystack = " ".join([
                tweet.author.lower(),
                tweet.username.lower(),
                tweet.author_type.lower(),
                tweet.tweet_type.lower(),
                tweet.content.lower(),
            ])
            if search and search not in haystack:
                continue
            filtered.append(tweet)
        if not filtered:
            print("No archived tweets matched that filter.")
            continue
        _display_twitter_feed(filtered, current_week, limit=30)
        input("Press Enter to go back...")


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
    print(f"Status: {req.status} | deadline week {req.week_deadline}")
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
    print("39. Quit")


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
            print("See you on the charts.")
            break
        else:
            print("Invalid choice.")
