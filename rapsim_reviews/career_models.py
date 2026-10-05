"""
rapsim_reviews.career_models
Core dataclasses, models, and constants for the career mode simulation.
"""
from dataclasses import dataclass, field
import random
from uuid import uuid4

from rapsim_reviews.ui_helpers import clamp_meter, clamp_popularity
from rapsim_reviews.track_review.base import Song
from rapsim_reviews.album_review.base import Album
from rapsim_reviews.concert_system import ConcertBooking, DEFAULT_PRICE_TEMPLATES
from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS
from rapsim_reviews.artist_ecosystem_sim import ARTIST_BASE_REPUTATION, classify_artist_skills


# ──────────────────────────────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────────────────────────────

SKILLS = ["lyrics", "vocals", "production", "mix/master"]
BASE_WEEKLY_RECOVERY = 50.0
LIVE_WEEKLY_POP_CAP = 6.0
NEGOTIATION_WALK_AWAY_BUFFER = 14.0
FEATURE_DEADLINE_WEEKS = 4

GENRE_SKILL_WEIGHTS = {
    "hip hop": {"lyrics": 0.40, "vocals": 0.25, "production": 0.20, "mix/master": 0.15},
    "pop": {"lyrics": 0.25, "vocals": 0.40, "production": 0.20, "mix/master": 0.15},
    "rock": {"lyrics": 0.30, "vocals": 0.35, "production": 0.20, "mix/master": 0.15},
    "r&b": {"lyrics": 0.30, "vocals": 0.40, "production": 0.15, "mix/master": 0.15},
    "soul": {"lyrics": 0.35, "vocals": 0.40, "production": 0.15, "mix/master": 0.10},
    "electronic": {"lyrics": 0.10, "vocals": 0.20, "production": 0.45, "mix/master": 0.25},
    "metal": {"lyrics": 0.25, "vocals": 0.35, "production": 0.25, "mix/master": 0.15},
    "experimental": {"lyrics": 0.25, "vocals": 0.25, "production": 0.35, "mix/master": 0.15},
}


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


# ──────────────────────────────────────────────────────────────────────
#  DATACLASSES
# ──────────────────────────────────────────────────────────────────────

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
    physical_editions: list[PhysicalEdition] = field(default_factory=list)
    virality_triggered: bool = False
    virality_weeks_active: int = 0
    virality_max_weekly_bonus: int = 0
    virality_baseline_streams: int = 0
    release_week_index: int | None = None
    day_offset: int = 4
    release_date: str = ""


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
    physical_editions: list[PhysicalEdition] = field(default_factory=list)
    day_offset: int = 4
    release_date: str = ""


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


def _relationship_score(artist, target_name: str) -> float:
    state = artist.relationships.get(target_name)
    if not state:
        return 0.0
    return float(getattr(state, "score", 0.0))


def _apply_relationship_delta(artist, target_name: str, delta: float) -> None:
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


def release_bump_for_quality(quality: float) -> float:
    if quality <= 3.0:
        return 1.0
    if quality <= 5.0:
        return 2.0
    if quality <= 7.0:
        return 3.0
    if quality <= 9.0:
        return 4.0
    return 5.0


def active_release_popularity(artist: "Artist") -> float:
    return sum(
        entry.release_popularity_value
        for entry in artist.singles
        if entry.released and entry.release_popularity_weeks_left > 0
    )



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
    controversy_history: list = field(default_factory=list)
    pending_responses: list[dict] = field(default_factory=list)
    recent_low_reviews: list[dict] = field(default_factory=list)
    releases_this_week: list[dict] = field(default_factory=list)
    grammy_state: dict[int, dict] = field(default_factory=dict)
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
    label_contract: object | None = None
    pending_label_offers: list = field(default_factory=list)

    @property
    def current_week(self) -> int:
        return ((self.year - 1) * 52) + self.week

    @property
    def weekly_streams(self) -> int:
        return int(getattr(self, "last_week_streams", 0))

    @property
    def live_performance_rating(self) -> float:
        if not getattr(self, "concert_history", None):
            return 0.0
        scores = [b.performance_score for b in self.concert_history]
        if not scores:
            return 0.0
        return (sum(scores) / len(scores)) * 10.0

    @property
    def popularity(self) -> float:
        return clamp_popularity(
            self.popularity_state.organic
            + self.popularity_state.management
            + self.popularity_state.live_boost
            + self.popularity_state.feature_boost
            + self.popularity_state.weekly_song
            + (self.popularity_state.album_release_boost if self.popularity_state.album_release_weeks_left > 0 else 0.0)
            + active_release_popularity(self)
        )

    @popularity.setter
    def popularity(self, value: float) -> None:
        target = float(value)
        current = self.popularity
        diff = target - current
        self.popularity_state.organic = max(0.0, self.popularity_state.organic + diff)


def _player_week_index(artist: Artist) -> int:
    return ((artist.year - 1) * 52) + artist.week


def _year_week_from_world_week(world_week: int) -> tuple[int, int]:
    if world_week <= 0:
        return 1, 1
    year = ((world_week - 1) // 52) + 1
    week = ((world_week - 1) % 52) + 1
    return year, week


def _ecosystem_seed_by_name(name: str):
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        if seed.name == name:
            return seed
    return None


def _ecosystem_artist_popularity(name: str, ecosystem_world=None) -> float:
    seed = _ecosystem_seed_by_name(name)
    base = float(getattr(seed, "popularity", 0.0)) if seed else 0.0
    if ecosystem_world is None:
        return base
    return float(getattr(ecosystem_world, "artist_popularity", {}).get(name, base))


def _ecosystem_artist_reputation(name: str, ecosystem_world=None) -> float:
    base = float(ARTIST_BASE_REPUTATION.get(name, 50))
    if ecosystem_world is None:
        return base
    return float(getattr(ecosystem_world, "artist_reputation", {}).get(name, base))


def _find_world_runtime(world, artist_name: str):
    if world is None:
        return None
    for runtime in world.roster:
        if runtime.seed.name == artist_name:
            return runtime
    return None


def _find_artist_any(name: str, player_artist: Artist, world):
    if name == player_artist.name:
        return player_artist
    return _find_world_runtime(world, name)


def _artist_display_name(subject) -> str:
    if isinstance(subject, Artist):
        return subject.name
    return getattr(getattr(subject, "seed", None), "name", str(subject))


def _is_growing_artist_name(name: str, world) -> bool:
    runtime = _find_world_runtime(world, name)
    if runtime is None:
        return False
    return "growing" in classify_artist_skills(runtime.seed)


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
    eng_skill = float(getattr(engineer_seed, "skills", {}).get("mix/master", 50))
    song.bg_mix = _roll_bg_attribute_from_skill(eng_skill)


def _ecosystem_release_quality(release) -> float:
    tracks = list(getattr(release, "tracks", None) or ())
    if tracks:
        return sum(float(getattr(track, "quality", getattr(release, "quality", 0.0))) for track in tracks) / len(tracks)
    return float(getattr(release, "quality", 0.0))


