"""Beat creation, vault, store, and weekly marketplace simulation."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from uuid import uuid4

from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS, EcosystemArtistSeed
from rapsim_reviews.track_review import GENRES

BEAT_SKILL_WEIGHTS = {"production": 0.55, "mix/master": 0.45}
PACK_SIZE_OPTIONS = (3, 4)
PACK_DISCOUNT_DEFAULT = 0.18
MAX_PRODUCER_BEAT_PRICE = 1_000_000.0
NEGOTIATE_CHANCE = 0.22
ECOSYSTEM_NPC_SALE_BOOST = 2.65
DEFAULT_BEAT_GENRE = "hip hop"

# Relative demand multiplier for fair-price baselines by genre.
GENRE_MARKET_MULTIPLIER: dict[str, float] = {
    "pop": 1.22,
    "hip hop": 1.18,
    "r&b": 1.12,
    "electronic": 1.08,
    "rock": 1.05,
    "country": 1.04,
    "soul": 1.06,
    "reggae": 0.98,
    "metal": 0.96,
    "punk": 0.94,
    "folk": 0.90,
    "blues": 0.92,
    "jazz": 0.88,
    "classical": 0.85,
    "experimental": 0.93,
}


@dataclass
class Beat:
    beat_id: str
    name: str
    quality: float
    genre: str
    created_week: int
    owner_name: str
    source: str = "player"  # player | purchased
    producer_name: str | None = None
    list_price: float | None = None
    discount_pct: float = 0.0
    listed: bool = False
    consumed: bool = False

    @property
    def is_player_made(self) -> bool:
        return self.source == "player"

    def effective_price(self) -> float | None:
        if self.list_price is None:
            return None
        return max(0.0, float(self.list_price) * (1.0 - max(0.0, min(0.9, self.discount_pct))))


@dataclass
class BeatPack:
    pack_id: str
    name: str
    beat_ids: tuple[str, ...]
    list_price: float
    discount_pct: float = 0.0
    listed: bool = False

    def effective_price(self) -> float:
        return max(0.0, float(self.list_price) * (1.0 - max(0.0, min(0.9, self.discount_pct))))


@dataclass
class BeatSaleRecord:
    week: int
    buyer: str
    item_name: str
    price: float
    item_type: str  # beat | pack
    item_id: str


@dataclass
class BeatNegotiation:
    negotiation_id: str
    direction: str  # inbound | outbound
    buyer_name: str
    seller_name: str
    beat_id: str | None
    pack_id: str | None
    listing_id: str | None
    listed_price: float
    offer_price: float
    week_created: int
    status: str = "pending"  # pending | accepted | rejected | expired


@dataclass
class EcosystemBeatListing:
    listing_id: str
    producer_name: str
    beat_name: str
    quality: float
    genre: str
    price: float
    week_listed: int
    seller_tier: str = "producer"  # producer | budget | growing
    sold: bool = False
    buyer_name: str = ""


@dataclass
class BeatMarketState:
    vault: list[Beat] = field(default_factory=list)
    packs: list[BeatPack] = field(default_factory=list)
    sales_history: list[BeatSaleRecord] = field(default_factory=list)
    weekly_notifications: list[str] = field(default_factory=list)
    pending_negotiations: list[BeatNegotiation] = field(default_factory=list)
    ecosystem_catalog: list[EcosystemBeatListing] = field(default_factory=list)


def ensure_beat_market(artist) -> BeatMarketState:
    if not hasattr(artist, "beat_market") or artist.beat_market is None:
        artist.beat_market = BeatMarketState()
    market = artist.beat_market
    for beat in market.vault:
        if not getattr(beat, "genre", None):
            beat.genre = DEFAULT_BEAT_GENRE
    for listing in market.ecosystem_catalog:
        if not getattr(listing, "genre", None):
            listing.genre = DEFAULT_BEAT_GENRE
        if not getattr(listing, "seller_tier", None):
            listing.seller_tier = "producer"
    return market


def normalize_beat_genre(genre: str | None) -> str:
    value = str(genre or DEFAULT_BEAT_GENRE).strip().lower()
    return value if value in GENRES else DEFAULT_BEAT_GENRE


def beat_genre_matches_song(beat_genre: str, song_genres: list[str]) -> bool:
    return normalize_beat_genre(beat_genre) in [normalize_beat_genre(g) for g in song_genres]


def genre_mismatch_penalty_amount() -> float:
    return random.uniform(1.0, 2.6)


def _producer_seeds() -> list[EcosystemArtistSeed]:
    roles = ("producer", "artist-producer", "rapper-producer")
    return [s for s in ARTIST_ECOSYSTEM_SEEDS if any(r in s.role for r in roles)]


def _budget_producer_seeds() -> list[EcosystemArtistSeed]:
    return [
        s
        for s in _producer_seeds()
        if int(s.skills.get("production", 50)) < 62 or float(getattr(s, "popularity", 50)) < 28
    ]


def _growing_artist_seeds() -> list[EcosystemArtistSeed]:
    """Lower-profile artists selling cheap beats to build a catalog presence."""
    producers = {s.name for s in _producer_seeds()}
    return [
        s
        for s in ARTIST_ECOSYSTEM_SEEDS
        if s.name not in producers
        and float(getattr(s, "popularity", 0)) < 42
        and int(s.skills.get("production", 0)) >= 28
    ]


def apply_prod_credit_to_title(title: str, producer_name: str | None) -> str:
    if not producer_name or "(prod." in title.lower():
        return title
    return f"{title.rstrip()} (prod. {producer_name})"


def _seed_by_name(name: str) -> EcosystemArtistSeed | None:
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        if seed.name == name:
            return seed
    return None


def top_genres_for_seed(seed: EcosystemArtistSeed, count: int = 2) -> list[str]:
    ranked = sorted(seed.genres.items(), key=lambda item: -item[1])
    genres = [g for g, _ in ranked[:count]]
    return genres or [DEFAULT_BEAT_GENRE]


def seed_matches_beat_genre(seed: EcosystemArtistSeed, beat_genre: str) -> bool:
    genre = normalize_beat_genre(beat_genre)
    ranked = top_genres_for_seed(seed, 3)
    if genre in ranked:
        return True
    return int(seed.genres.get(genre, 0)) >= 55


def calculate_beat_max_quality(artist) -> float:
    craft = sum(float(artist.skills.get(skill, 25)) * weight for skill, weight in BEAT_SKILL_WEIGHTS.items())
    raw_percent = max(1.0, craft)
    curved = 1.0 + 8.25 * ((raw_percent / 100.0) ** 2.35)
    fatigue_penalty = max(0.0, (float(artist.fatigue) - 75.0) / 10.0)
    overfatigue_penalty = max(0.0, (float(artist.fatigue) - 100.0) / 4.5)
    health_penalty = max(0.0, (50.0 - float(artist.health)) / 22.0)
    quality = curved + random.uniform(-0.35, 0.35) - fatigue_penalty - health_penalty - overfatigue_penalty
    return max(0.0, min(10.0, quality))


def roll_beat_quality(artist, roll_quality_fn) -> float:
    return roll_quality_fn(calculate_beat_max_quality(artist), artist.fatigue)


def suggested_list_price(quality: float, seller_popularity: float, genre: str) -> float:
    """Fair list price from beat quality, genre demand, and seller visibility."""
    genre = normalize_beat_genre(genre)
    q = max(0.0, min(10.0, float(quality)))
    pop = max(0.0, min(100.0, float(seller_popularity)))
    genre_mult = GENRE_MARKET_MULTIPLIER.get(genre, 1.0)
    quality_core = 180.0 + (q ** 2.35) * 110.0
    # Fame raises prices, but low-quality beats cannot command a superstar tax.
    pop_mult = 0.72 + (pop / 100.0) ** 1.1 * 0.38
    fame_premium = max(0.0, (pop - 55.0)) * 18.0 * (q / 10.0)
    base = (quality_core * genre_mult * pop_mult) + fame_premium
    return round(max(99.0, base), 2)


def suggested_pack_price(beats: list[Beat], seller_popularity: float, discount: float = PACK_DISCOUNT_DEFAULT) -> float:
    valid = [beat for beat in beats if beat is not None]
    if not valid:
        return 0.0
    total = sum(suggested_list_price(beat.quality, seller_popularity, beat.genre) for beat in valid)
    discount = max(0.0, min(0.9, float(discount)))
    return round(max(99.0, total * (1.0 - discount)), 2)


def beat_ids_in_listed_packs(market: BeatMarketState) -> set[str]:
    return {bid for pack in market.packs if pack.listed for bid in pack.beat_ids}


def beat_is_in_any_pack(market: BeatMarketState, beat_id: str) -> bool:
    return any(beat_id in pack.beat_ids for pack in market.packs)


def beat_has_pending_negotiation(market: BeatMarketState, beat_id: str) -> bool:
    return any(
        neg.status == "pending" and neg.beat_id == beat_id
        for neg in market.pending_negotiations
    )


def solo_listed_beats(market: BeatMarketState, player_name: str) -> list[Beat]:
    """Beats listed individually (not only as part of a pack)."""
    packed = beat_ids_in_listed_packs(market)
    return [
        b
        for b in market.vault
        if b.listed
        and b.is_player_made
        and b.owner_name == player_name
        and b.beat_id not in packed
    ]


def estimated_weekly_sale_probability(
    quality: float,
    list_price: float | None,
    seller_popularity: float,
    genre: str,
    *,
    buyer_genre_match: bool = True,
) -> float:
    """
    Chance a listed beat sells in a given week.
    Higher list price vs fair price lowers odds; fame only cushions moderate markups.
    """
    if list_price is None:
        return 0.0
    fair = max(99.0, suggested_list_price(quality, seller_popularity, genre))
    price = max(1.0, float(list_price))
    price_ratio = price / fair
    q = max(0.0, min(10.0, float(quality))) / 10.0
    pop = max(0.0, min(100.0, float(seller_popularity))) / 100.0

    visibility = 0.05 + (pop**1.35) * 0.34

    if price_ratio < 0.55:
        value = 0.07 + q * 0.08
    elif price_ratio <= 0.88:
        value = 0.17 + q * 0.20
    elif price_ratio <= 1.08:
        value = 0.12 + q * 0.14
    elif price_ratio <= 1.45:
        value = max(0.04, 0.13 - (price_ratio - 1.08) * 0.14 + q * 0.05)
    elif price_ratio <= 2.2:
        over = price_ratio - 1.45
        value = max(0.02, 0.07 - over * 0.035 + q * 0.02)
        value += min(0.05, pop * 0.045)
    else:
        value = max(0.008, 0.035 - (price_ratio - 2.2) * 0.012)
        value += min(0.025, pop * 0.02)

    if not buyer_genre_match:
        value *= 0.28
        visibility *= 0.75

    prob = visibility * 0.52 + value * 0.58
    return max(0.01, min(0.45, prob))


def estimated_pack_weekly_sale_probability(
    beats: list[Beat],
    list_price: float | None,
    seller_popularity: float,
    *,
    buyer_genre_match: bool = True,
) -> float:
    valid = [beat for beat in beats if beat is not None]
    if not valid or list_price is None:
        return 0.0
    avg_quality = sum(float(beat.quality) for beat in valid) / len(valid)
    primary_genre = valid[0].genre
    fair = max(99.0, suggested_pack_price(valid, seller_popularity))
    price = max(1.0, float(list_price))
    price_ratio = price / fair
    q = max(0.0, min(10.0, avg_quality)) / 10.0
    pop = max(0.0, min(100.0, float(seller_popularity))) / 100.0

    visibility = 0.06 + (pop**1.35) * 0.36
    pack_bonus = min(0.08, 0.02 * len(valid))

    if price_ratio < 0.55:
        value = 0.09 + q * 0.10 + pack_bonus
    elif price_ratio <= 0.88:
        value = 0.19 + q * 0.22 + pack_bonus
    elif price_ratio <= 1.08:
        value = 0.13 + q * 0.16 + pack_bonus
    elif price_ratio <= 1.45:
        value = max(0.04, 0.14 - (price_ratio - 1.08) * 0.14 + q * 0.05 + pack_bonus)
    elif price_ratio <= 2.2:
        over = price_ratio - 1.45
        value = max(0.02, 0.08 - over * 0.035 + q * 0.02 + pack_bonus * 0.5)
        value += min(0.05, pop * 0.045)
    else:
        value = max(0.008, 0.04 - (price_ratio - 2.2) * 0.012 + pack_bonus * 0.3)
        value += min(0.025, pop * 0.02)

    if not buyer_genre_match:
        value *= 0.28
        visibility *= 0.75

    prob = visibility * 0.52 + value * 0.58
    return max(0.01, min(0.45, prob))


def producer_will_accept_offer(listing_price: float, offer: float, producer_name: str) -> bool:
    """Whether a producer accepts a purchase offer (rejects insulting lowballs)."""
    listed = max(1.0, float(listing_price))
    bid = max(0.0, float(offer))
    if bid < listed * 0.30:
        return False
    ratio = bid / listed
    seed = _seed_by_name(producer_name)
    prestige = 0.55
    if seed:
        prestige = min(
            1.15,
            0.45
            + float(seed.skills.get("production", 50)) / 200.0
            + float(getattr(seed, "popularity", 50)) / 250.0,
        )
    thresholds = (
        (0.88, 0.82),
        (0.72, 0.52),
        (0.58, 0.30),
        (0.45, 0.14),
        (0.30, 0.04),
    )
    for min_ratio, base_chance in thresholds:
        if ratio >= min_ratio:
            return random.random() < min(base_chance * prestige, 0.92)
    return False


def format_pricing_help(artist, genres: list[str] | None = None) -> list[str]:
    pop = float(getattr(artist, "popularity", 0.0))
    lines = [
        f"Your popularity: {pop:.1f}%",
        "Pricing tips: undercut the 'fair' price when you're unknown; famous artists can overprice good beats.",
        "",
    ]
    check_genres = genres or sorted(
        artist.genres.keys(),
        key=lambda g: -int(artist.genres.get(g, 0)),
    )[:5]
    if not check_genres:
        check_genres = list(GENRES[:6])
    for genre in check_genres:
        lines.append(f"--- {genre.title()} beats ---")
        for quality in (5.5, 6.5, 7.5, 8.5):
            fair = suggested_list_price(quality, pop, genre)
            bargain = fair * 0.78
            stretch = fair * (1.18 + pop / 250.0)
            prob_fair = estimated_weekly_sale_probability(quality, fair, pop, genre) * 100
            prob_stretch = estimated_weekly_sale_probability(quality, stretch, pop, genre) * 100
            lines.append(
                f"  Q{quality:.1f}: fair ~${fair:,.0f} (~{prob_fair:.0f}%/wk) | "
                f"bargain ~${bargain:,.0f} | stretch ~${stretch:,.0f} (~{prob_stretch:.0f}%/wk)"
            )
        lines.append("")
    lines.append(
        "Example: at ~22% popularity, a 7.5 beat near $1,000 often struggles unless it's a steep discount. "
        "At ~80% popularity, a 5.5 beat near $10,000 can still move because fans pay for your name."
    )
    return lines


def vault_beats(market: BeatMarketState, *, include_consumed: bool = False) -> list[Beat]:
    beats = market.vault
    if not include_consumed:
        beats = [b for b in beats if not b.consumed]
    return beats


def available_vault_beats(market: BeatMarketState) -> list[Beat]:
    return [b for b in market.vault if not b.consumed]


def available_vault_beats_for_song_genres(market: BeatMarketState, song_genres: list[str]) -> list[Beat]:
    return [b for b in available_vault_beats(market) if beat_genre_matches_song(b.genre, song_genres)]


def player_listable_beats(market: BeatMarketState, player_name: str) -> list[Beat]:
    packed_ids = beat_ids_in_listed_packs(market)
    return [
        b
        for b in market.vault
        if b.owner_name == player_name
        and b.is_player_made
        and not b.consumed
        and not b.listed
        and b.beat_id not in packed_ids
    ]


def beat_by_id(market: BeatMarketState, beat_id: str) -> Beat | None:
    return next((b for b in market.vault if b.beat_id == beat_id), None)


def pack_by_id(market: BeatMarketState, pack_id: str) -> BeatPack | None:
    return next((p for p in market.packs if p.pack_id == pack_id), None)


def add_beat_to_vault(artist, beat: Beat) -> None:
    market = ensure_beat_market(artist)
    market.vault.append(beat)


def create_player_beat(artist, name: str, quality: float, genre: str, week_index: int) -> Beat:
    return Beat(
        beat_id=str(uuid4()),
        name=name,
        quality=float(quality),
        genre=normalize_beat_genre(genre),
        created_week=int(week_index),
        owner_name=artist.name,
        source="player",
    )


def create_purchased_beat(
    artist,
    name: str,
    quality: float,
    genre: str,
    producer_name: str,
    week_index: int,
) -> Beat:
    return Beat(
        beat_id=str(uuid4()),
        name=name,
        quality=float(quality),
        genre=normalize_beat_genre(genre),
        created_week=int(week_index),
        owner_name=artist.name,
        source="purchased",
        producer_name=producer_name,
    )


def _producer_beat_price(
    seed: EcosystemArtistSeed,
    quality: float,
    genre: str,
    *,
    seller_tier: str = "producer",
) -> float:
    genre = normalize_beat_genre(genre)
    prod = float(seed.skills.get("production", 50))
    mix = float(seed.skills.get("mix/master", 50))
    genre_skill = float(seed.genres.get(genre, 40))
    pop = float(getattr(seed, "popularity", 50))
    genre_mult = GENRE_MARKET_MULTIPLIER.get(genre, 1.0)
    base = (
        1_800.0
        + prod * 165.0
        + mix * 95.0
        + genre_skill * 140.0
        + pop * 110.0
        + (float(quality) ** 2.2) * 3_800.0
    ) * genre_mult
    if seller_tier == "budget":
        base *= random.uniform(0.10, 0.28)
        return round(max(75.0, min(4_500.0, base)), 2)
    if seller_tier == "growing":
        base = 120.0 + (quality**1.9) * 55.0 + prod * 4.0
        return round(max(49.0, min(2_200.0, base)), 2)
    if prod >= 92 and genre_skill >= 80:
        base = max(base, random.uniform(450_000.0, MAX_PRODUCER_BEAT_PRICE))
    elif prod >= 85 and genre_skill >= 70:
        base = max(base, random.uniform(120_000.0, 650_000.0))
    return round(min(MAX_PRODUCER_BEAT_PRICE, max(499.0, base)), 2)


def _roll_catalog_quality(seed: EcosystemArtistSeed, genre: str, seller_tier: str) -> float:
    genre_skill = float(seed.genres.get(genre, 40))
    prod = float(seed.skills.get("production", 50))
    if seller_tier == "budget":
        raw = (prod * 0.4 + genre_skill * 0.25) / 14.0 + random.uniform(-1.4, 1.0)
        return round(max(1.0, min(6.8, raw)), 1)
    if seller_tier == "growing":
        raw = (prod * 0.45 + genre_skill * 0.35) / 13.0 + random.uniform(-1.2, 1.2)
        return round(max(1.0, min(7.5, raw)), 1)
    raw = (prod * 0.55 + genre_skill * 0.45) / 10.0 + random.uniform(-1.1, 1.3)
    return round(max(1.0, min(10.0, raw)), 1)


def _append_catalog_listing(
    market: BeatMarketState,
    seed: EcosystemArtistSeed,
    week_index: int,
    seller_tier: str,
    listing_index: int,
) -> None:
    genre = _pick_producer_genre(seed)
    quality = _roll_catalog_quality(seed, genre, seller_tier)
    price = _producer_beat_price(seed, quality, genre, seller_tier=seller_tier)
    prefix = {
        "producer": seed.name.split()[0].lower(),
        "budget": f"budget_{seed.name.split()[0].lower()}",
        "growing": f"demo_{seed.name.split()[0].lower()}",
    }.get(seller_tier, "beat")
    market.ecosystem_catalog.append(
        EcosystemBeatListing(
            listing_id=str(uuid4()),
            producer_name=seed.name,
            beat_name=f"{prefix}_{genre.replace(' ', '')}_{week_index}_{listing_index}",
            quality=quality,
            genre=genre,
            price=price,
            week_listed=week_index,
            seller_tier=seller_tier,
        )
    )


def _pick_producer_genre(seed: EcosystemArtistSeed) -> str:
    ranked = sorted(seed.genres.items(), key=lambda item: -item[1])
    if not ranked:
        return DEFAULT_BEAT_GENRE
    if len(ranked) == 1:
        return ranked[0][0]
    genres, weights = zip(*ranked[:4])
    return random.choices(list(genres), weights=[max(1, w) for w in weights], k=1)[0]


def refresh_ecosystem_catalog(market: BeatMarketState, week_index: int) -> None:
    market.ecosystem_catalog = [item for item in market.ecosystem_catalog if not item.sold]
    listing_counter = 0

    budget_names = {s.name for s in _budget_producer_seeds()}
    for seed in _budget_producer_seeds():
        for _ in range(random.randint(2, 4)):
            listing_counter += 1
            _append_catalog_listing(market, seed, week_index, "budget", listing_counter)

    for seed in _producer_seeds():
        tier = "budget" if seed.name in budget_names else "producer"
        if tier == "budget":
            continue
        count = random.randint(2, 4)
        for _ in range(count):
            listing_counter += 1
            _append_catalog_listing(market, seed, week_index, "producer", listing_counter)

    growing_pool = _growing_artist_seeds()
    random.shuffle(growing_pool)
    for seed in growing_pool[: min(22, len(growing_pool))]:
        if random.random() > 0.82:
            continue
        for _ in range(random.randint(1, 2)):
            listing_counter += 1
            _append_catalog_listing(market, seed, week_index, "growing", listing_counter)


def active_catalog_listings(market: BeatMarketState) -> list[EcosystemBeatListing]:
    return [item for item in market.ecosystem_catalog if not item.sold]


def catalog_sellers_grouped(market: BeatMarketState) -> dict[str, list[EcosystemBeatListing]]:
    grouped: dict[str, list[EcosystemBeatListing]] = {}
    for item in active_catalog_listings(market):
        grouped.setdefault(item.producer_name, []).append(item)
    return grouped


def format_seller_menu_line(seller_name: str, listings: list[EcosystemBeatListing]) -> str:
    seed = _seed_by_name(seller_name)
    pop = float(getattr(seed, "popularity", 0.0)) if seed else 0.0
    tier = listings[0].seller_tier if listings else "producer"
    tier_label = {"producer": "Producer", "budget": "Budget producer", "growing": "Growing artist"}.get(
        tier, "Seller"
    )
    prices = [float(item.price) for item in listings]
    qualities = [float(item.quality) for item in listings]
    return (
        f"{seller_name} [{tier_label}] | {len(listings)} beat(s) | "
        f"Q {min(qualities):.1f}-{max(qualities):.1f} | "
        f"${min(prices):,.0f}-${max(prices):,.0f} | pop {pop:.0f}%"
    )


def format_listing_menu_line(listing: EcosystemBeatListing) -> str:
    return (
        f"{listing.beat_name} | {listing.genre} | {listing.quality}/10 | "
        f"{money_fmt(listing.price)}"
    )


def money_fmt(value: float | None) -> str:
    if value is None:
        return "—"
    return f"${float(value):,.2f}"


def npc_listing_sale_probability(listing: EcosystemBeatListing) -> float:
    producer = _seed_by_name(listing.producer_name)
    producer_pop = float(producer.popularity) if producer else 50.0
    prob = estimated_weekly_sale_probability(
        listing.quality,
        listing.price,
        producer_pop,
        listing.genre,
        buyer_genre_match=True,
    )
    prob *= ECOSYSTEM_NPC_SALE_BOOST
    if listing.seller_tier in ("budget", "growing"):
        prob *= 1.45
    return max(0.04, min(0.68, prob))


def _pick_buyer_for_genre(beat_genre: str, exclude: str) -> EcosystemArtistSeed | None:
    genre = normalize_beat_genre(beat_genre)
    candidates = [
        s
        for s in ARTIST_ECOSYSTEM_SEEDS
        if s.name != exclude and seed_matches_beat_genre(s, genre)
    ]
    if not candidates:
        candidates = [s for s in ARTIST_ECOSYSTEM_SEEDS if s.name != exclude]
    return random.choice(candidates) if candidates else None


def _record_sale(market: BeatMarketState, week: int, buyer: str, item_name: str, price: float, item_type: str, item_id: str):
    market.sales_history.append(
        BeatSaleRecord(
            week=week,
            buyer=buyer,
            item_name=item_name,
            price=price,
            item_type=item_type,
            item_id=item_id,
        )
    )
    market.weekly_notifications.append(
        f"{buyer} bought \"{item_name}\" for ${price:,.2f}."
    )


def _try_inbound_negotiation(
    market: BeatMarketState,
    buyer: str,
    seller: str,
    beat_id: str | None,
    pack_id: str | None,
    listed_price: float,
    week_index: int,
) -> bool:
    if random.random() > NEGOTIATE_CHANCE:
        return False
    offer = round(listed_price * random.uniform(0.55, 0.88), 2)
    market.pending_negotiations.append(
        BeatNegotiation(
            negotiation_id=str(uuid4()),
            direction="inbound",
            buyer_name=buyer,
            seller_name=seller,
            beat_id=beat_id,
            pack_id=pack_id,
            listing_id=None,
            listed_price=listed_price,
            offer_price=offer,
            week_created=week_index,
        )
    )
    market.weekly_notifications.append(
        f"{buyer} wants to negotiate (offer ${offer:,.2f}, listed ${listed_price:,.2f})."
    )
    return True


def create_outbound_negotiation(
    market: BeatMarketState,
    buyer: str,
    listing: EcosystemBeatListing,
    offer_price: float,
    week_index: int,
) -> BeatNegotiation | None:
    for existing in market.pending_negotiations:
        if (
            existing.status == "pending"
            and existing.direction == "outbound"
            and existing.listing_id == listing.listing_id
            and existing.buyer_name == buyer
        ):
            return None
    negotiation = BeatNegotiation(
        negotiation_id=str(uuid4()),
        direction="outbound",
        buyer_name=buyer,
        seller_name=listing.producer_name,
        beat_id=None,
        pack_id=None,
        listing_id=listing.listing_id,
        listed_price=float(listing.price),
        offer_price=float(offer_price),
        week_created=week_index,
    )
    market.pending_negotiations.append(negotiation)
    return negotiation


def simulate_player_beat_sales(artist, world, week_index: int) -> float:
    market = ensure_beat_market(artist)
    income = 0.0
    seller_pop = float(getattr(artist, "popularity", 0.0))
    listed_beats = [b for b in market.vault if b.listed and b.is_player_made and not b.consumed and b.effective_price()]
    for beat in listed_beats:
        price = float(beat.effective_price())
        buyer_seed = _pick_buyer_for_genre(beat.genre, artist.name)
        if buyer_seed is None:
            continue
        genre_match = seed_matches_beat_genre(buyer_seed, beat.genre)
        prob = estimated_weekly_sale_probability(
            beat.quality, price, seller_pop, beat.genre, buyer_genre_match=genre_match
        )
        if random.random() > prob:
            continue
        buyer = buyer_seed.name
        if _try_inbound_negotiation(market, buyer, artist.name, beat.beat_id, None, price, week_index):
            continue
        beat.listed = False
        beat.consumed = True
        income += price
        _record_sale(market, week_index, buyer, f"{beat.name} ({beat.genre})", price, "beat", beat.beat_id)

    for pack in [p for p in market.packs if p.listed]:
        price = pack.effective_price()
        pack_beats = [beat_by_id(market, bid) for bid in pack.beat_ids]
        pack_beats = [b for b in pack_beats if b]
        if not pack_beats:
            continue
        avg_q = sum(b.quality for b in pack_beats) / len(pack_beats)
        pack_genre = pack_beats[0].genre
        buyer_seed = _pick_buyer_for_genre(pack_genre, artist.name)
        if buyer_seed is None:
            continue
        prob = estimated_pack_weekly_sale_probability(
            pack_beats,
            price,
            seller_pop,
            buyer_genre_match=seed_matches_beat_genre(buyer_seed, pack_genre),
        )
        if random.random() > prob:
            continue
        buyer = buyer_seed.name
        if _try_inbound_negotiation(market, buyer, artist.name, None, pack.pack_id, price, week_index):
            continue
        pack.listed = False
        for b in pack_beats:
            b.listed = False
            b.consumed = True
        income += price
        _record_sale(market, week_index, buyer, pack.name, price, "pack", pack.pack_id)

    artist.money += income
    return income


def simulate_ecosystem_catalog_activity(market: BeatMarketState, world, week_index: int, player_name: str) -> None:
    listings = list(active_catalog_listings(market))
    random.shuffle(listings)
    for listing in listings:
        if listing.sold:
            continue
        for _ in range(2):
            if listing.sold:
                break
            buyer_seed = _pick_buyer_for_genre(listing.genre, player_name)
            if buyer_seed is None:
                continue
            genre_match = seed_matches_beat_genre(buyer_seed, listing.genre)
            prob = npc_listing_sale_probability(listing)
            if not genre_match:
                prob *= 0.55
            if random.random() > prob:
                continue
            listing.sold = True
            listing.buyer_name = buyer_seed.name
            market.weekly_notifications.append(
                f"{buyer_seed.name} bought {listing.genre} beat \"{listing.beat_name}\" from "
                f"{listing.producer_name} for ${listing.price:,.2f}."
            )


def _resolve_outbound_negotiations(artist, market: BeatMarketState, week_index: int) -> None:
    for neg in list(market.pending_negotiations):
        if neg.status != "pending" or neg.direction != "outbound" or not neg.listing_id:
            continue
        listing = next((x for x in market.ecosystem_catalog if x.listing_id == neg.listing_id), None)
        if listing is None or listing.sold:
            neg.status = "expired"
            continue
        if producer_will_accept_offer(float(neg.listed_price), float(neg.offer_price), neg.seller_name):
            accept_negotiation(artist, neg)
            market.weekly_notifications.append(
                f"{neg.seller_name} accepted your offer (${neg.offer_price:,.2f}) for \"{listing.beat_name}\"."
            )
        elif week_index - neg.week_created >= 1:
            neg.status = "rejected"
            market.weekly_notifications.append(
                f"{neg.seller_name} declined your offer on \"{listing.beat_name}\"."
            )


def step_beat_market_week(artist, world, week_index: int) -> float:
    market = ensure_beat_market(artist)
    market.weekly_notifications = []
    refresh_ecosystem_catalog(market, week_index)
    simulate_ecosystem_catalog_activity(market, world, week_index, artist.name)
    _resolve_outbound_negotiations(artist, market, week_index)
    income = simulate_player_beat_sales(artist, world, week_index)

    expired = []
    for neg in market.pending_negotiations:
        if neg.status != "pending":
            continue
        if week_index - neg.week_created > 2:
            neg.status = "expired"
            expired.append(neg)
    for neg in expired:
        market.weekly_notifications.append(
            f"Negotiation with {neg.buyer_name} expired."
        )
    return income


def purchase_ecosystem_listing(artist, listing: EcosystemBeatListing, week_index: int) -> Beat | None:
    if listing.sold:
        return None
    price = float(listing.price)
    if artist.money < price:
        return None
    artist.money -= price
    listing.sold = True
    listing.buyer_name = artist.name
    beat = create_purchased_beat(
        artist,
        listing.beat_name,
        listing.quality,
        listing.genre,
        listing.producer_name,
        week_index,
    )
    add_beat_to_vault(artist, beat)
    return beat


def accept_negotiation(artist, neg: BeatNegotiation) -> bool:
    market = ensure_beat_market(artist)
    if neg.direction == "inbound":
        price = float(neg.offer_price)
        if neg.beat_id:
            beat = beat_by_id(market, neg.beat_id)
            if beat is None or not beat.listed:
                return False
            beat.listed = False
            beat.consumed = True
            artist.money += price
            _record_sale(market, neg.week_created, neg.buyer_name, beat.name, price, "beat", beat.beat_id)
        elif neg.pack_id:
            pack = pack_by_id(market, neg.pack_id)
            if pack is None or not pack.listed:
                return False
            pack.listed = False
            for bid in pack.beat_ids:
                b = beat_by_id(market, bid)
                if b:
                    b.listed = False
                    b.consumed = True
            artist.money += price
            _record_sale(market, neg.week_created, neg.buyer_name, pack.name, price, "pack", neg.pack_id)
        neg.status = "accepted"
        return True

    if neg.direction == "outbound" and neg.listing_id:
        listing = next((x for x in market.ecosystem_catalog if x.listing_id == neg.listing_id), None)
        if listing is None or listing.sold:
            return False
        price = float(neg.offer_price)
        if artist.money < price:
            return False
        artist.money -= price
        listing.sold = True
        listing.buyer_name = artist.name
        beat = create_purchased_beat(
            artist,
            listing.beat_name,
            listing.quality,
            listing.genre,
            listing.producer_name,
            neg.week_created,
        )
        add_beat_to_vault(artist, beat)
        neg.status = "accepted"
        return True
    return False


def sales_analytics_summary(market: BeatMarketState) -> dict:
    if not market.sales_history:
        return {
            "total_sales": 0,
            "total_revenue": 0.0,
            "avg_price": 0.0,
            "top_buyers": [],
            "recent": [],
        }
    total_revenue = sum(s.price for s in market.sales_history)
    buyer_counts: dict[str, int] = {}
    for sale in market.sales_history:
        buyer_counts[sale.buyer] = buyer_counts.get(sale.buyer, 0) + 1
    top_buyers = sorted(buyer_counts.items(), key=lambda x: (-x[1], x[0]))[:5]
    return {
        "total_sales": len(market.sales_history),
        "total_revenue": total_revenue,
        "avg_price": total_revenue / len(market.sales_history),
        "top_buyers": top_buyers,
        "recent": list(reversed(market.sales_history[-12:])),
    }
