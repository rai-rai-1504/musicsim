"""Record Label System for RapSim.

Features 10 distinct record labels across 5 tiers (underground, indie, mid, major, elite),
complete with contract negotiations, recoupment accounting, roster priority ranking,
shelving risk mechanics, breach penalties, and drop clauses.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Optional

from rapsim_reviews.ui_helpers import (
    choose_from_list,
    clamp_meter,
    clamp_popularity,
    meter_bar,
    money_fmt,
    prompt_int,
    prompt_text,
)


@dataclass
class Label:
    id: str
    name: str
    tier: str                        # "underground" | "indie" | "mid" | "major" | "elite"
    description: str                 # flavour text, personality of the label
    label_popularity: int            # 0-100, defines prestige and roster priority
    min_artist_popularity: int       # minimum player popularity to be considered

    # ADVANCE
    base_advance: int                # base signing amount in $
    advance_variance: float          # always 0.10 (+/-10%)

    # CONTRACT TERMS
    album_commitment: int            # number of albums/projects required
    contract_years: int              # duration in in-game years (each = 48 weeks)
    damage_amount: int               # base breach penalty in $
    damage_variance: float           # always 0.10 (+/-10%)

    # REVENUE TAKES
    concert_merch_cut: float         # % label takes from concerts and merch (0.0-0.60)
    post_recoup_royalty_cut: float   # % label takes after recoupment (0.20-0.75)
    owns_masters: bool               # always True for mid tier and above

    # GIVES
    weekly_ad_budget: int            # $ spent on music ads per week
    collab_discount: bool            # True = label roster collabs are free
    guaranteed_attendance_pct: float # % of venue capacity guaranteed filled (0.20-0.70)
    festival_slots_per_year: int     # guaranteed festival appearances per in-game year
    interview_opportunities_per_year: int  # podcast/talk show/press spots arranged

    # ROSTER
    signed_artists: list[str] = field(default_factory=list)  # ecosystem artist names currently signed
    roster_size_max: int = 10         # maximum artists label will sign simultaneously
    artist_popularity_history: dict[str, dict[int, float]] = field(default_factory=dict) # {artist_name: {week: pop}}
    artist_signed_weeks: dict[str, int] = field(default_factory=dict) # {artist_name: join_week}

    # NEGOTIATION
    negotiable_fields: list[str] = field(default_factory=list)  # which terms can actually be negotiated

    # BEHAVIOUR
    shelving_threshold: float = 0.0   # if artist streams fall below this % of roster avg, shelving risk rises
    priority_threshold: int = 5       # artist must be in top N of roster by popularity to get full promotion
    drop_threshold: int = 10          # consecutive underperforming weeks before drop consideration

    @property
    def strictness(self) -> int:
        """Strictness of a label is always equal to its prestige (label_popularity)."""
        return self.label_popularity

    @property
    def gig_promotion_boost(self) -> float:
        """Compatibility multiplier alias."""
        return 1.0 + self.guaranteed_attendance_pct


@dataclass
class LabelContract:
    label_id: str
    signed_week: int

    # negotiated terms (may differ from label base)
    advance_paid: int
    album_commitment: int
    contract_years: int
    damage_amount: int
    concert_merch_cut: float
    post_recoup_royalty_cut: float

    # recoupment tracking
    recoupment_balance: int        # starts at advance_paid, counts down to 0
    label_promo_costs_added: int   # additional costs label charges to recoupment

    # delivery tracking
    albums_delivered: int          # albums delivered against commitment
    weeks_elapsed: int

    # status
    status: str                    # "active" | "recouped" | "shelved" | "breach" | "expired" | "dropped"
    is_priority_artist: bool       # label treating you as priority based on roster rank
    shelved_weeks: int             # consecutive weeks where label withheld promotion
    underperform_weeks: int        # consecutive weeks of underperformance

    # post-expiry
    masters_owned_by_label: bool
    post_contract_recoupment_remaining: int  # balance still owed after contract ends

    # weekly history for priority ranking
    popularity_history: dict[int, float] = field(default_factory=dict) # {week: pop}


@dataclass
class RosterArtistView:
    name: str
    popularity: float                    # W5_i (current week popularity)
    weekly_streams: int = 0
    popularity_w1: float = 0.0           # W1_i (popularity 4 weeks ago)
    weeks_in_label: int = 52             # duration on roster (>=4 means past onboarding)
    growth: float = 0.0                  # G_i = W5_i - W1_i
    growth_pct: float = 0.0              # Growth%_i = (W5_i - W1_i) / W1_i * 100
    norm_current_pop: float = 0.0        # C_i in [0, 100]
    norm_momentum: float = 0.0           # M_i in [0, 100]
    priority_score: float = 0.0          # P_i = 0.75 * C_i + 0.25 * M_i in [0, 100]
    is_onboarding: bool = False          # True if weeks_in_label < 4


LABELS: list[Label] = [

    # -- TIER 1: UNDERGROUND ----------------------------------------------

    Label(
        id="lbl_01",
        name="Meridian Collective",
        tier="underground",
        description=(
            "Started in a Chicago basement. Meridian is run by three people who "
            "genuinely care about the music. They have no machine but they have "
            "taste, and the underground respects them for it. Artists here retain "
            "creative control most labels wouldn't dream of giving."
        ),
        label_popularity=8,
        min_artist_popularity=0,

        base_advance=10_000,
        advance_variance=0.10,

        album_commitment=1,
        contract_years=1,
        damage_amount=5_000,
        damage_variance=0.10,

        concert_merch_cut=0.0,
        post_recoup_royalty_cut=0.20,
        owns_masters=False,

        weekly_ad_budget=200,
        collab_discount=True,
        guaranteed_attendance_pct=0.20,
        festival_slots_per_year=0,
        interview_opportunities_per_year=1,

        signed_artists=[],
        roster_size_max=6,
        negotiable_fields=["advance", "album_commitment", "post_recoup_royalty_cut"],

        shelving_threshold=0.0,
        priority_threshold=6,
        drop_threshold=99,
    ),

    Label(
        id="lbl_02",
        name="Static Ground Records",
        tier="underground",
        description=(
            "Atlanta-based tape label that became a cult institution. "
            "Static Ground moves slowly -- they sign one artist a year and pour "
            "everything into them. The advance is small but the loyalty is real. "
            "They will never shelf your music. They will never drop you mid-slump."
        ),
        label_popularity=14,
        min_artist_popularity=2,

        base_advance=25_000,
        advance_variance=0.10,

        album_commitment=2,
        contract_years=2,
        damage_amount=12_000,
        damage_variance=0.10,

        concert_merch_cut=0.05,
        post_recoup_royalty_cut=0.25,
        owns_masters=False,

        weekly_ad_budget=500,
        collab_discount=True,
        guaranteed_attendance_pct=0.20,
        festival_slots_per_year=1,
        interview_opportunities_per_year=2,

        signed_artists=[],
        roster_size_max=4,
        negotiable_fields=["advance", "post_recoup_royalty_cut", "contract_years"],

        shelving_threshold=0.0,
        priority_threshold=4,
        drop_threshold=99,
    ),

    # -- TIER 2: INDIE ----------------------------------------------------

    Label(
        id="lbl_03",
        name="Wavelength Independent",
        tier="indie",
        description=(
            "New York indie label with a strong track record of breaking mid-tier "
            "artists into the mainstream. Wavelength has genuine press relationships "
            "and a festival pipeline that underground labels can only dream of. "
            "They own your masters but they're fair about the royalty split. "
            "First label where the machine actually starts working for you."
        ),
        label_popularity=28,
        min_artist_popularity=12,

        base_advance=120_000,
        advance_variance=0.10,

        album_commitment=2,
        contract_years=3,
        damage_amount=60_000,
        damage_variance=0.10,

        concert_merch_cut=0.10,
        post_recoup_royalty_cut=0.35,
        owns_masters=True,

        weekly_ad_budget=2_500,
        collab_discount=True,
        guaranteed_attendance_pct=0.30,
        festival_slots_per_year=2,
        interview_opportunities_per_year=4,

        signed_artists=[],
        roster_size_max=12,
        negotiable_fields=["advance", "concert_merch_cut", "post_recoup_royalty_cut",
                           "album_commitment"],

        shelving_threshold=0.25,
        priority_threshold=6,
        drop_threshold=12,
    ),

    Label(
        id="lbl_04",
        name="Cipher House",
        tier="indie",
        description=(
            "Cipher House started as a hip-hop collective and became one of the most "
            "respected indie labels in the country. Their roster reads like a who's "
            "who of critically acclaimed artists who refused major deals. "
            "Cipher House will fight for your creative vision -- but they'll also "
            "fight you if your streams disappoint. The rep is everything here."
        ),
        label_popularity=35,
        min_artist_popularity=18,

        base_advance=200_000,
        advance_variance=0.10,

        album_commitment=3,
        contract_years=3,
        damage_amount=100_000,
        damage_variance=0.10,

        concert_merch_cut=0.12,
        post_recoup_royalty_cut=0.38,
        owns_masters=True,

        weekly_ad_budget=4_000,
        collab_discount=True,
        guaranteed_attendance_pct=0.30,
        festival_slots_per_year=3,
        interview_opportunities_per_year=6,

        signed_artists=[],
        roster_size_max=15,
        negotiable_fields=["advance", "post_recoup_royalty_cut", "concert_merch_cut"],

        shelving_threshold=0.30,
        priority_threshold=8,
        drop_threshold=10,
    ),

    # -- TIER 3: MID ------------------------------------------------------

    Label(
        id="lbl_05",
        name="Amplify Records",
        tier="mid",
        description=(
            "Amplify is the first label on this list where you'll feel the full "
            "weight of a music industry machine. Radio pluggers, playlist curators, "
            "brand partnerships, festival headlining slots -- Amplify has all of it. "
            "They also have a roster of 30 artists competing for the same resources. "
            "If your album underperforms they will not hesitate to redirect everything "
            "toward someone else on the roster."
        ),
        label_popularity=52,
        min_artist_popularity=30,

        base_advance=800_000,
        advance_variance=0.10,

        album_commitment=3,
        contract_years=4,
        damage_amount=400_000,
        damage_variance=0.10,

        concert_merch_cut=0.20,
        post_recoup_royalty_cut=0.48,
        owns_masters=True,

        weekly_ad_budget=15_000,
        collab_discount=True,
        guaranteed_attendance_pct=0.40,
        festival_slots_per_year=4,
        interview_opportunities_per_year=10,

        signed_artists=[],
        roster_size_max=30,
        negotiable_fields=["advance", "concert_merch_cut"],

        shelving_threshold=0.40,
        priority_threshold=10,
        drop_threshold=8,
    ),

    Label(
        id="lbl_06",
        name="Nocturne Group",
        tier="mid",
        description=(
            "Nocturne is mid-tier but operates like a major. They are aggressive "
            "negotiators, their contracts are notoriously detailed, and their executive "
            "team watches streaming data obsessively. Sign here if your numbers are "
            "strong -- they will amplify them enormously. Sign here if your numbers "
            "are soft -- they will shelf you within 6 months and quietly redirect "
            "resources to the next signing."
        ),
        label_popularity=61,
        min_artist_popularity=38,

        base_advance=1_500_000,
        advance_variance=0.10,

        album_commitment=3,
        contract_years=4,
        damage_amount=750_000,
        damage_variance=0.10,

        concert_merch_cut=0.25,
        post_recoup_royalty_cut=0.52,
        owns_masters=True,

        weekly_ad_budget=28_000,
        collab_discount=True,
        guaranteed_attendance_pct=0.40,
        festival_slots_per_year=5,
        interview_opportunities_per_year=14,

        signed_artists=[],
        roster_size_max=25,
        negotiable_fields=["advance"],

        shelving_threshold=0.45,
        priority_threshold=8,
        drop_threshold=6,
    ),

    # -- TIER 4: MAJOR ----------------------------------------------------

    Label(
        id="lbl_07",
        name="Sovereign Music Group",
        tier="major",
        description=(
            "Sovereign is a fully operational major label with global distribution, "
            "television partnerships, brand deal pipelines, and stadium-level festival "
            "relationships. Signing here means you are entering the top 1% of the "
            "industry machine. It also means the label owns everything you record "
            "while signed and takes half of everything you earn after recoupment. "
            "The advance is life-changing. The contract is a decade of your career."
        ),
        label_popularity=78,
        min_artist_popularity=55,

        base_advance=8_000_000,
        advance_variance=0.10,

        album_commitment=4,
        contract_years=6,
        damage_amount=4_000_000,
        damage_variance=0.10,

        concert_merch_cut=0.35,
        post_recoup_royalty_cut=0.60,
        owns_masters=True,

        weekly_ad_budget=80_000,
        collab_discount=True,
        guaranteed_attendance_pct=0.50,
        festival_slots_per_year=8,
        interview_opportunities_per_year=24,

        signed_artists=[],
        roster_size_max=50,
        negotiable_fields=["advance"],

        shelving_threshold=0.50,
        priority_threshold=12,
        drop_threshold=5,
    ),

    Label(
        id="lbl_08",
        name="Parallax Records",
        tier="major",
        description=(
            "Parallax is known for two things: making careers and ending them. "
            "Their promotion budget is the largest on this list outside the elite tier. "
            "Their legal team is aggressive and their breach penalties are the most "
            "severe in the industry. Artists who thrive at Parallax are managed "
            "obsessively and become global names. Artists who underperform at Parallax "
            "disappear -- shelved, dropped, or trapped in litigation."
        ),
        label_popularity=84,
        min_artist_popularity=62,

        base_advance=15_000_000,
        advance_variance=0.10,

        album_commitment=4,
        contract_years=7,
        damage_amount=8_000_000,
        damage_variance=0.10,

        concert_merch_cut=0.40,
        post_recoup_royalty_cut=0.65,
        owns_masters=True,

        weekly_ad_budget=140_000,
        collab_discount=True,
        guaranteed_attendance_pct=0.50,
        festival_slots_per_year=10,
        interview_opportunities_per_year=32,

        signed_artists=[],
        roster_size_max=45,
        negotiable_fields=[],

        shelving_threshold=0.55,
        priority_threshold=10,
        drop_threshold=4,
    ),

    # -- TIER 5: ELITE ----------------------------------------------------

    Label(
        id="lbl_09",
        name="Apex Universal",
        tier="elite",
        description=(
            "Apex Universal is the music industry. They have offices in every major "
            "city, television network partnerships, ownership stakes in streaming "
            "platforms, and a roster that includes the biggest names alive. "
            "An Apex signing is not a record deal -- it is an identity acquisition. "
            "They will build you into a global brand. They will own everything. "
            "Non-negotiable on every term. Breach penalties are existential."
        ),
        label_popularity=94,
        min_artist_popularity=75,

        base_advance=35_000_000,
        advance_variance=0.10,

        album_commitment=5,
        contract_years=8,
        damage_amount=20_000_000,
        damage_variance=0.10,

        concert_merch_cut=0.50,
        post_recoup_royalty_cut=0.70,
        owns_masters=True,

        weekly_ad_budget=300_000,
        collab_discount=True,
        guaranteed_attendance_pct=0.70,
        festival_slots_per_year=15,
        interview_opportunities_per_year=52,

        signed_artists=[],
        roster_size_max=60,
        negotiable_fields=[],

        shelving_threshold=0.60,
        priority_threshold=15,
        drop_threshold=3,
    ),

    Label(
        id="lbl_10",
        name="Monolith Entertainment",
        tier="elite",
        description=(
            "Monolith does not sign artists. Monolith acquires them. The $50M advance "
            "is the largest in the game and the terms are the most punishing. "
            "Monolith artists become cultural phenomena -- they headline every major "
            "festival, appear on every major platform, and receive a level of "
            "promotional support that makes the industry look effortless. "
            "In exchange Monolith owns your masters, takes 75% post-recoupment, "
            "60% of your concerts and merch, and the breach penalty is $28M. "
            "You don't sign Monolith. Monolith signs you."
        ),
        label_popularity=100,
        min_artist_popularity=85,

        base_advance=50_000_000,
        advance_variance=0.10,

        album_commitment=5,
        contract_years=10,
        damage_amount=28_000_000,
        damage_variance=0.10,

        concert_merch_cut=0.60,
        post_recoup_royalty_cut=0.75,
        owns_masters=True,

        weekly_ad_budget=600_000,
        collab_discount=True,
        guaranteed_attendance_pct=0.70,
        festival_slots_per_year=20,
        interview_opportunities_per_year=80,

        signed_artists=[],
        roster_size_max=40,
        negotiable_fields=[],

        shelving_threshold=0.65,
        priority_threshold=12,
        drop_threshold=2,
    ),
]


NEGOTIATION_RESPONSES = {
    "accept": [
        "we've reviewed your counter. we can work with that.",
        "deal. our legal team will send the revised contract.",
        "agreed. welcome to the roster.",
        "that works for us. we'll proceed on your terms.",
    ],
    "counter": [
        "we can meet you halfway. here's our revised offer:",
        "that's not where we need to be but we're not walking away.",
        "we'll move on {field} but {other_field} is firm.",
        "our final movement on this: {counter_value}. take it or leave it.",
    ],
    "refuse_field": [
        "{field} is non-negotiable. everything else we can discuss.",
        "we don't move on {field}. that's the foundation of the deal.",
        "you're asking us to change something that isn't on the table.",
        "that term exists for a reason. we won't revisit it.",
    ],
    "walk": [
        "if that's your position we don't have a deal.",
        "we've been generous. this is no longer worth our time.",
        "you're negotiating against your own interests here. we're done.",
        "the offer is withdrawn.",
    ],
    "impressed_overbid": [
        "we weren't expecting that. you've got the deal and our full attention.",
        "artists don't usually offer more than we ask. you've earned some goodwill.",
        "that's noted. you'll find us more flexible than most when it matters.",
    ],
}


def get_label_by_id(label_id: str) -> Optional[Label]:
    for lbl in LABELS:
        if lbl.id == label_id:
            return lbl
    return None


def get_label_by_name(name: str) -> Optional[Label]:
    for lbl in LABELS:
        if lbl.name.lower() == name.lower():
            return lbl
    return None


# -----------------------------------------------------------------------------
#  ROSTER POPULATION HELPER
# -----------------------------------------------------------------------------

def seed_label_rosters(labels: list[Label] | None = None, ecosystem_world: Any = None) -> None:
    """Populates the 10 labels with ecosystem artists according to tier."""
    target_labels = labels or LABELS
    from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS

    seeds_by_tier = {
        "underground": [],
        "indie": [],
        "mid": [],
        "major": [],
        "elite": [],
    }

    for s in ARTIST_ECOSYSTEM_SEEDS:
        pop = float(getattr(s, "popularity", 0.0))
        if pop < 20.0:
            seeds_by_tier["underground"].append(s.name)
        elif pop < 45.0:
            seeds_by_tier["indie"].append(s.name)
        elif pop < 70.0:
            seeds_by_tier["mid"].append(s.name)
        elif pop < 88.0:
            seeds_by_tier["major"].append(s.name)
        else:
            seeds_by_tier["elite"].append(s.name)

    # Deterministic assignment based on label tier
    rng = random.Random(42)
    for lbl in target_labels:
        if lbl.signed_artists:
            continue
        pool = seeds_by_tier.get(lbl.tier, [])
        sample_size = min(len(pool), max(2, int(lbl.roster_size_max * 0.4)))
        chosen = rng.sample(pool, sample_size) if pool else []
        lbl.signed_artists = list(chosen)


def calculate_release_priority(roster: list[RosterArtistView]) -> list[RosterArtistView]:
    """
    Computes Release Priority Scores for all artists according to the
    Popularity-Based Release Priority Model.

    Formula:
      G_i = W5_i - W1_i
      L_i = ln( W5_i / (100 - W5_i) )
      C_i = 100 * (L_i - L_min) / (L_max - L_min)
      M_i = 100 * (G_i - G_min) / (G_max - G_min)
      P_i = 0.75 * C_i + 0.25 * M_i

    Edge case:
      If an artist has been in a label for less than 4 weeks (weeks_in_label < 4),
      they are in the onboarding period. The artist is NOT made part of the priority
      list and receives no priority (P_i = 0.0, is_onboarding = True).
    """
    eligible: list[RosterArtistView] = []
    onboarding: list[RosterArtistView] = []

    for a in roster:
        # Determine W1 baseline (popularity 4 weeks ago)
        w5 = float(a.popularity)
        w1 = float(a.popularity_w1) if a.popularity_w1 > 0.0 else w5
        a.popularity_w1 = w1
        a.growth = round(w5 - w1, 2)
        a.growth_pct = round((a.growth / max(0.1, w1)) * 100.0, 2)

        if getattr(a, "weeks_in_label", 52) < 4:
            a.is_onboarding = True
            a.norm_current_pop = 0.0
            a.norm_momentum = 0.0
            a.priority_score = 0.0
            onboarding.append(a)
        else:
            a.is_onboarding = False
            eligible.append(a)

    if not eligible:
        return onboarding

    # 1. Nonlinear Current Popularity (Log-Odds)
    log_odds: list[float] = []
    for a in eligible:
        # Clamp popularity safely to (0.1, 99.9) for log-odds stability
        w5_clamped = max(0.1, min(99.9, float(a.popularity)))
        l_val = math.log(w5_clamped / (100.0 - w5_clamped))
        log_odds.append(l_val)

    l_min = min(log_odds)
    l_max = max(log_odds)

    # 2. Absolute Growth / Momentum
    growths = [a.growth for a in eligible]
    g_min = min(growths)
    g_max = max(growths)

    # 3. Normalization and Priority Calculation
    for idx, a in enumerate(eligible):
        l_val = log_odds[idx]
        g_val = a.growth

        if l_max > l_min:
            c_val = 100.0 * (l_val - l_min) / (l_max - l_min)
        else:
            c_val = 50.0  # Equal popularity fallback

        if g_max > g_min:
            m_val = 100.0 * (g_val - g_min) / (g_max - g_min)
        else:
            m_val = 50.0  # Equal growth fallback

        p_val = 0.75 * c_val + 0.25 * m_val

        a.norm_current_pop = round(c_val, 2)
        a.norm_momentum = round(m_val, 2)
        a.priority_score = round(p_val, 2)

    # Sort eligible by priority_score descending (tiebreak by current popularity, then streams)
    eligible.sort(key=lambda x: (x.priority_score, x.popularity, x.weekly_streams), reverse=True)

    return eligible + onboarding


def get_label_roster_artists(label: Label, player: Any, ecosystem_world: Any = None, current_week: int = 1) -> list[RosterArtistView]:
    """Returns a list of RosterArtistView objects for all artists signed to the label, including the player,
    scored and ordered via the Popularity-Based Release Priority Model."""
    views: list[RosterArtistView] = []
    seen = set()

    # Add player if signed
    if player and getattr(player, "label_contract", None) and player.label_contract.label_id == label.id:
        contract = player.label_contract
        weeks_elapsed = getattr(contract, "weeks_elapsed", 0)
        pop_w5 = float(player.popularity)

        # Retrieve W1 (popularity 4 weeks ago)
        pop_history = getattr(contract, "popularity_history", {})
        if (current_week - 4) in pop_history:
            pop_w1 = float(pop_history[current_week - 4])
        elif pop_history:
            pop_w1 = float(pop_history.get(contract.signed_week, pop_w5))
        else:
            pop_w1 = pop_w5

        views.append(
            RosterArtistView(
                name=player.name,
                popularity=pop_w5,
                weekly_streams=int(getattr(player, "weekly_streams", 0)),
                popularity_w1=pop_w1,
                weeks_in_label=weeks_elapsed,
            )
        )
        seen.add(player.name)

    # Ecosystem artists
    from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS
    seed_map = {s.name: s for s in ARTIST_ECOSYSTEM_SEEDS}

    for name in label.signed_artists:
        if name in seen or (player and name == player.name):
            continue
        seen.add(name)
        pop = 50.0
        streams = 0

        if ecosystem_world is not None:
            pop = float(ecosystem_world.artist_popularity.get(name, 50.0))
            if hasattr(ecosystem_world, "song_runtime"):
                streams = sum(
                    int(getattr(s, "last_week_streams", 0))
                    for s in ecosystem_world.song_runtime.values()
                    if getattr(s, "artist_name", "") == name
                )
        elif name in seed_map:
            pop = float(seed_map[name].popularity)

        if streams == 0:
            # Baseline proxy streams based on popularity
            streams = int(pop * 35_000)

        # Weeks signed for ecosystem artist (default 52 for seeded established artists)
        signed_wk = label.artist_signed_weeks.get(name, None)
        if signed_wk is not None:
            weeks_in_label = max(0, current_week - signed_wk)
        else:
            weeks_in_label = 52

        # Popularity 4 weeks ago (W1)
        history_map = label.artist_popularity_history.get(name, {})
        if (current_week - 4) in history_map:
            pop_w1 = float(history_map[current_week - 4])
        else:
            # Deterministic, realistic 4-week starting baseline for established artists
            seed_rng = random.Random(f"w1_pop:{name}:{label.id}")
            base_delta = seed_rng.uniform(-2.0, 6.0)
            pop_w1 = max(1.0, min(99.0, pop - base_delta))

        views.append(
            RosterArtistView(
                name=name,
                popularity=pop,
                weekly_streams=streams,
                popularity_w1=pop_w1,
                weeks_in_label=weeks_in_label,
            )
        )

    # Calculate release priority scores and rankings
    return calculate_release_priority(views)


# -----------------------------------------------------------------------------
#  THE 4 ENGINES & NEGOTIATION
# -----------------------------------------------------------------------------

def process_weekly_label_recoupment(player: Any, contract: LabelContract, label: Label, week_earnings: float | int) -> float:
    """
    Runs every simulate_week call if player is signed.
    week_earnings = total player earnings that week from all sources
    """
    if contract.status not in ("active", "shelved", "recouped"):
        return float(week_earnings)

    if contract.recoupment_balance > 0:
        # label takes their cut of ALL earnings toward recoupment
        label_share = week_earnings * (1 - contract.post_recoup_royalty_cut)
        contract.recoupment_balance -= int(label_share)
        contract.recoupment_balance = max(0, contract.recoupment_balance)

        # player earns nothing
        player_earnings_this_week = 0.0

        if contract.recoupment_balance == 0:
            contract.status = "recouped"
            # notify player -- recoupment cleared
            print(f"\n  *  RECOUPMENT CLEARED -- you now earn {int((1-contract.post_recoup_royalty_cut)*100)}% of all revenue")

    else:
        # post-recoupment: split earnings
        label_cut = int(week_earnings * contract.post_recoup_royalty_cut)
        player_earnings_this_week = float(week_earnings - label_cut)

    # add label promotion costs to recoupment balance if still in recoupment
    if contract.recoupment_balance > 0:
        promo_cost_this_week = label.weekly_ad_budget
        contract.recoupment_balance += promo_cost_this_week
        contract.label_promo_costs_added += promo_cost_this_week

    return float(player_earnings_this_week)


def evaluate_roster_priority(player: Any, contract: LabelContract, label: Label, all_signed_artists: list[Any], current_week: int = 1) -> tuple[float, float, float]:
    """
    Determines whether the label treats the player as a priority artist based on the
    Popularity-Based Release Priority Model.

    Edge case:
      If the artist has been in a label for less than 4 weeks (weeks_elapsed < 4),
      they are in the onboarding period and NOT made part of the priority list.
      The artist has no priority in the first 4 weeks of joining a label.
    """
    # 1. Onboarding check (first 4 weeks)
    if getattr(contract, "weeks_elapsed", 0) < 4:
        contract.is_priority_artist = False
        effective_ad_budget = float(label.weekly_ad_budget * 0.40)
        effective_attendance_pct = float(label.guaranteed_attendance_pct * 0.50)
        effective_pop_boost = 0.0  # No weekly popularity addition by labels
        contract.shelved_weeks = 0  # Do not count toward shelving during onboarding
        return effective_ad_budget, effective_attendance_pct, effective_pop_boost

    # 2. Build or recalculate release priority scores
    roster_views: list[RosterArtistView] = []
    for item in all_signed_artists:
        if isinstance(item, RosterArtistView):
            roster_views.append(item)
        else:
            name = getattr(item, "name", "Unknown")
            pop = float(getattr(item, "popularity", 50.0))
            streams = int(getattr(item, "weekly_streams", int(pop * 35_000)))
            weeks = getattr(item, "weeks_in_label", 52)
            roster_views.append(RosterArtistView(name=name, popularity=pop, weekly_streams=streams, weeks_in_label=weeks))

    ranked_roster = calculate_release_priority(roster_views)

    # Filter to eligible artists for ranking
    eligible_roster = [a for a in ranked_roster if not a.is_onboarding]

    player_rank = next((i + 1 for i, a in enumerate(eligible_roster) if a.name == player.name), len(eligible_roster) + 1)

    contract.is_priority_artist = (player_rank <= label.priority_threshold)

    if not contract.is_priority_artist:
        # player is not priority -- label reduces promotion
        effective_ad_budget = label.weekly_ad_budget * 0.20   # 20% of normal
        effective_attendance_pct = label.guaranteed_attendance_pct * 0.60
        effective_pop_boost = 0.0  # No weekly popularity addition by labels
        contract.shelved_weeks += 1
    else:
        effective_ad_budget = float(label.weekly_ad_budget)
        effective_attendance_pct = float(label.guaranteed_attendance_pct)
        effective_pop_boost = 0.0  # No weekly popularity addition by labels
        contract.shelved_weeks = 0

    return effective_ad_budget, effective_attendance_pct, effective_pop_boost


def evaluate_shelving_risk(player: Any, contract: LabelContract, label: Label, all_signed_artists: list[Any]) -> tuple[bool, str]:
    """
    Checks if the label shelves an upcoming release.
    Shelving means the label delays or kills a planned release.
    """
    if label.shelving_threshold == 0.0:
        return False, "label never shelves releases"

    # Onboarding protection: new signees are not shelved during first 4 weeks
    if getattr(contract, "weeks_elapsed", 0) < 4:
        return False, "artist is in 4-week onboarding window"

    roster_avg_streams = sum(a.weekly_streams for a in all_signed_artists) / max(len(all_signed_artists), 1)
    player_stream_ratio = player.weekly_streams / max(roster_avg_streams, 1)

    if player_stream_ratio < label.shelving_threshold:
        contract.underperform_weeks += 1
    else:
        contract.underperform_weeks = max(0, contract.underperform_weeks - 1)

    # shelving probability scales with consecutive underperform weeks
    shelve_prob = min(0.9, contract.underperform_weeks * 0.12) * (label.label_popularity / 100)

    if random.random() < shelve_prob:
        return True, random.choice([
            f"{label.name} has decided to delay your upcoming release pending review.",
            f"your A&R at {label.name} has put the project on hold. no timeline given.",
            f"{label.name} is redirecting promotional resources. your release is paused.",
            f"internal memo: {label.name} is not confident in the current project's commercial viability.",
        ])

    return False, ""


def evaluate_contract_breach(player: Any, contract: LabelContract, label: Label, current_week: int) -> tuple[bool, int, str]:
    """
    Checks at end of contract period whether player fulfilled album commitment.
    """
    contract_end_week = contract.signed_week + (contract.contract_years * 48)

    if current_week < contract_end_week:
        return False, 0, ""

    # contract period over
    albums_owed = contract.album_commitment - contract.albums_delivered

    if albums_owed <= 0:
        # fulfilled -- clean exit
        contract.status = "expired"
        msg = f"contract with {label.name} fulfilled. {contract.albums_delivered} albums delivered."
        return False, 0, msg

    # breach -- player owes damage per undelivered album
    base_damage = contract.damage_amount
    variance = random.uniform(-label.damage_variance, label.damage_variance)
    damage_per_album = int(base_damage * (1 + variance))
    total_damage = damage_per_album * albums_owed

    contract.status = "breach"
    msg = (
        f"{label.name} has filed a breach notice. "
        f"{albums_owed} album(s) undelivered. "
        f"damages: ${total_damage:,}. "
        f"unreleased material recorded during the contract is withheld."
    )

    return True, total_damage, msg


def evaluate_drop_risk(player: Any, contract: LabelContract, label: Label) -> tuple[bool, str]:
    """
    Label may choose to drop the player if underperformance is severe enough.
    Being dropped terminates album obligation but post-contract recoupment continues.
    """
    if contract.underperform_weeks < label.drop_threshold:
        return False, ""

    drop_prob = min(0.85, (contract.underperform_weeks - label.drop_threshold) * 0.20)
    drop_prob *= (label.label_popularity / 100)

    if random.random() < drop_prob:
        contract.status = "dropped"
        player.reputation = clamp_meter(player.reputation - random.randint(8, 15))
        player.popularity = clamp_popularity(player.popularity - random.randint(3, 8))
        if player.name in label.signed_artists:
            label.signed_artists.remove(player.name)
        msg = random.choice([
            f"{label.name} has released you from your contract. official statement pending.",
            f"sources confirm {label.name} has parted ways with you. no public comment.",
            f"{label.name} exercised the drop clause. you are free but the masters stay with them.",
            f"your contract with {label.name} has been terminated by mutual agreement. it was not mutual.",
        ])
        return True, msg

    return False, ""


def negotiate_label_contract(player: Any, label: Label, proposed_terms: dict[str, Any]) -> tuple[Optional[list[dict]], Optional[list[dict]]]:
    """
    Player proposes modifications to label's standard terms.
    label.negotiable_fields determines what can actually move.
    label.strictness determines how much movement is possible.
    Returns (accepted_responses, None) on success, or (None, failure_responses) if deal collapses.
    """
    pressure_score = 0
    responses: list[dict] = []

    for field, proposed_value in proposed_terms.items():
        base_value = getattr(label, field, getattr(label, f"base_{field}", None))
        if base_value is None:
            continue

        if field not in label.negotiable_fields:
            responses.append({
                "field": field,
                "response": random.choice(NEGOTIATION_RESPONSES["refuse_field"]).format(field=field),
                "accepted": False,
                "final_value": base_value,
            })
            pressure_score += 15
            continue

        # how far from base is the proposal
        if isinstance(base_value, (int, float)):
            change_pct = abs(proposed_value - base_value) / max(base_value, 1)
        else:
            change_pct = 0.0

        # strictness determines tolerance
        tolerance = (100 - label.strictness) / 100 * 0.25  # max 25% movement at strictness 0

        if change_pct <= tolerance * 0.5:
            # easy accept
            responses.append({
                "field": field,
                "response": random.choice(NEGOTIATION_RESPONSES["accept"]),
                "accepted": True,
                "final_value": proposed_value,
            })
        elif change_pct <= tolerance:
            # counter at midpoint
            if isinstance(base_value, (int, float)):
                counter_value = int((base_value + proposed_value) / 2) if isinstance(base_value, int) else round((base_value + proposed_value) / 2, 2)
            else:
                counter_value = base_value
            responses.append({
                "field": field,
                "response": random.choice(NEGOTIATION_RESPONSES["counter"]).format(
                    field=field, other_field="the royalty split",
                    counter_value=counter_value),
                "accepted": False,
                "final_value": counter_value,
            })
            pressure_score += 8
        else:
            # too far -- refuse or walk
            if pressure_score > label.strictness:
                responses.append({
                    "field": field,
                    "response": random.choice(NEGOTIATION_RESPONSES["walk"]),
                    "accepted": False,
                    "final_value": None,  # deal collapsed
                })
                return None, responses  # negotiation failed
            else:
                responses.append({
                    "field": field,
                    "response": random.choice(NEGOTIATION_RESPONSES["refuse_field"]).format(field=field),
                    "accepted": False,
                    "final_value": base_value,
                })
                pressure_score += 20

    return responses, None


def can_label_approach_player(label: Label, player: Any) -> bool:
    """Label approaches player when conditions are met."""
    return (
        player.popularity >= label.min_artist_popularity
        and len(label.signed_artists) < label.roster_size_max
        and getattr(player, "label_contract", None) is None
    )


def can_player_approach_label(label: Label, player: Any) -> bool:
    """Player approaches label -- harder the higher the label tier."""
    base_chance = max(0.0, (player.popularity - label.min_artist_popularity) / 100)
    rep_bonus = player.reputation / 500
    return random.random() < (base_chance + rep_bonus)


def sign_contract(player: Any, label: Label, negotiated_terms: dict[str, Any] | None = None) -> tuple[LabelContract, int]:
    """Binds the player to a label contract and pays the signing advance."""
    terms = negotiated_terms or {
        "advance_paid": label.base_advance,
        "album_commitment": label.album_commitment,
        "contract_years": label.contract_years,
        "damage_amount": label.damage_amount,
        "concert_merch_cut": label.concert_merch_cut,
        "post_recoup_royalty_cut": label.post_recoup_royalty_cut,
    }

    # apply advance variance
    variance = random.uniform(-label.advance_variance, label.advance_variance)
    final_advance = int(terms["advance_paid"] * (1 + variance))

    contract = LabelContract(
        label_id=label.id,
        signed_week=player.current_week,
        advance_paid=final_advance,
        album_commitment=terms["album_commitment"],
        contract_years=terms["contract_years"],
        damage_amount=int(terms["damage_amount"] * (1 + random.uniform(
            -label.damage_variance, label.damage_variance))),
        concert_merch_cut=terms["concert_merch_cut"],
        post_recoup_royalty_cut=terms["post_recoup_royalty_cut"],
        recoupment_balance=final_advance,
        label_promo_costs_added=0,
        albums_delivered=0,
        weeks_elapsed=0,
        status="active",
        is_priority_artist=False,  # Starts in 4-week onboarding window (no priority)
        shelved_weeks=0,
        underperform_weeks=0,
        masters_owned_by_label=label.owns_masters,
        post_contract_recoupment_remaining=0,
        popularity_history={player.current_week: float(player.popularity)},
    )

    player.money += final_advance
    player.label_contract = contract
    if player.name not in label.signed_artists:
        label.signed_artists.append(player.name)
    label.artist_signed_weeks[player.name] = player.current_week
    label.artist_popularity_history.setdefault(player.name, {})[player.current_week] = float(player.popularity)

    return contract, final_advance


# -----------------------------------------------------------------------------
#  INTERACTIVE CLI MENUS
# -----------------------------------------------------------------------------

def label_management_menu(artist: Any, ecosystem_world: Any = None) -> None:
    """Main Record Labels menu in career mode."""
    seed_label_rosters(LABELS, ecosystem_world)

    while True:
        contract: Optional[LabelContract] = getattr(artist, "label_contract", None)

        print("\n" + "=" * 62)
        print("                 RECORD LABEL HEADQUARTERS")
        print("=" * 62)

        if contract and contract.status in ("active", "shelved", "recouped"):
            label = get_label_by_id(contract.label_id)
            lbl_name = label.name if label else "Unknown Label"
            tier_str = label.tier.upper() if label else "N/A"

            print(f"  Current Label : {lbl_name} [{tier_str}]")
            print(f"  Contract State: {contract.status.upper()}")
            print(f"  Priority Level: {'* PRIORITY ARTIST' if contract.is_priority_artist else 'DEVELOPING / ROSTER BACKLOG'}")
            print(f"  Recoupment    : {money_fmt(contract.recoupment_balance)} remaining")
            print(f"  Albums Done   : {contract.albums_delivered} / {contract.album_commitment}")
            print(f"  Contract Term : {contract.contract_years} Years ({contract.weeks_elapsed} weeks elapsed)")
            print("=" * 62)

            options = [
                "1. View Contract Overview & Recoupment Details",
                "2. View Label Roster & Release Priority Leaderboard",
                "3. Request Early Release / Buyout Masters",
                "4. Return to Main Menu",
            ]
            for opt in options:
                print("  " + opt)

            choice = prompt_text("\nSelect option: ", "").strip()
            if choice == "1":
                _view_contract_overview(artist, contract, label)
            elif choice == "2":
                _view_label_roster(artist, label, ecosystem_world)
            elif choice == "3":
                _handle_contract_buyout(artist, contract, label)
            elif choice == "4" or not choice:
                break
        else:
            print("  Status: INDEPENDENT ARTIST (Unsigned)")
            print(f"  Popularity: {artist.popularity:.1f} | Reputation: {artist.reputation:.1f}")
            print("=" * 62)

            inbound_count = len(getattr(artist, "pending_label_offers", []))
            options = [
                "1. Browse All 10 Industry Record Labels",
                "2. Pitch / Scout a Record Deal",
                f"3. Review Inbound Offers ({inbound_count} Pending)",
                "4. Return to Main Menu",
            ]
            for opt in options:
                print("  " + opt)

            choice = prompt_text("\nSelect option: ", "").strip()
            if choice == "1":
                _browse_all_labels(artist)
            elif choice == "2":
                _scout_pitch_label_flow(artist, ecosystem_world)
            elif choice == "3":
                _review_inbound_offers_flow(artist, ecosystem_world)
            elif choice == "4" or not choice:
                break


def _browse_all_labels(artist: Any) -> None:
    print("\n" + "=" * 80)
    print("                      RECORD LABELS DIRECTORY")
    print("=" * 80)
    print(f"{'Label Name':<24} {'Tier':<12} {'Req Pop':<10} {'Base Advance':<14} {'Cut':<8} {'Masters':<8}")
    print("-" * 80)
    for lbl in LABELS:
        masters_str = "Label" if lbl.owns_masters else "Artist"
        print(f"{lbl.name:<24} {lbl.tier:<12} {lbl.min_artist_popularity:<10} {money_fmt(lbl.base_advance):<14} {int(lbl.post_recoup_royalty_cut*100)}%     {masters_str:<8}")
    print("=" * 80)

    lbl_idx = choose_from_list("Inspect specific label details", [l.name for l in LABELS], allow_cancel=True)
    if lbl_idx is None:
        return
    lbl = LABELS[lbl_idx]
    print("\n" + "=" * 65)
    print(f"  {lbl.name.upper()} ({lbl.tier.upper()} TIER)")
    print("=" * 65)
    print(f"  Description    : {lbl.description}")
    print(f"  Prestige/Pop   : {lbl.label_popularity}/100")
    print(f"  Min Artist Pop : {lbl.min_artist_popularity}")
    print(f"  Base Advance   : {money_fmt(lbl.base_advance)} (+/-10%)")
    print(f"  Album Quota    : {lbl.album_commitment} projects across {lbl.contract_years} years")
    print(f"  Post-Recoup Cut: {int(lbl.post_recoup_royalty_cut * 100)}% to label")
    print(f"  Concert/Merch  : {int(lbl.concert_merch_cut * 100)}% cut")
    print(f"  Masters Rights : {'Label Owns Masters' if lbl.owns_masters else 'Artist Retains Masters'}")
    print(f"  Weekly Ad Pushes: {money_fmt(lbl.weekly_ad_budget)}/week")
    print(f"  Seat Guarantee : {int(lbl.guaranteed_attendance_pct * 100)}% minimum concert fill")
    print(f"  Roster Size    : {len(lbl.signed_artists)} / {lbl.roster_size_max} artists")
    print(f"  Prestige/Strictness: {lbl.label_popularity}/100")
    print(f"  Negotiables    : {', '.join(lbl.negotiable_fields) if lbl.negotiable_fields else 'None (Take it or leave it)'}")
    print("=" * 65)
    input("\nPress Enter to return...")


def _scout_pitch_label_flow(artist: Any, ecosystem_world: Any = None) -> None:
    labels_list = [f"{l.name} [{l.tier.upper()}] (Min Pop: {l.min_artist_popularity})" for l in LABELS]
    idx = choose_from_list("Choose a record label to pitch to", labels_list, allow_cancel=True)
    if idx is None:
        return
    label = LABELS[idx]

    print(f"\nSetting up meeting with {label.name} A&R team...")
    if artist.popularity < label.min_artist_popularity:
        print(f"  [REJECTED] {label.name} requires at least {label.min_artist_popularity} popularity.")
        print(f"  Your current popularity is {artist.popularity:.1f}. Build more buzz first!")
        input("\nPress Enter to continue...")
        return

    if not can_player_approach_label(label, artist):
        print(f"  [PASSED OVER] {label.name}'s executives were unimpressed with your pitch.")
        print("  Their roster is competitive and your current buzz didn't meet their standards.")
        input("\nPress Enter to continue...")
        return

    print(f"\n  [SUCCESS] {label.name} is interested in signing you!")
    _run_contract_negotiation_ui(artist, label)


def _review_inbound_offers_flow(artist: Any, ecosystem_world: Any = None) -> None:
    offers: list[Label] = getattr(artist, "pending_label_offers", [])
    if not offers:
        print("\nNo pending label offers at the moment. Keep increasing your popularity to attract A&Rs!")
        input("\nPress Enter to continue...")
        return

    labels_list = [f"{lbl.name} [{lbl.tier.upper()}] - Base Advance: {money_fmt(lbl.base_advance)}" for lbl in offers]
    idx = choose_from_list("Select an offer to review", labels_list, allow_cancel=True)
    if idx is None:
        return

    label = offers[idx]
    print(f"\nReviewing formal offer from {label.name}...")
    _run_contract_negotiation_ui(artist, label)
    if getattr(artist, "label_contract", None):
        # Successfully signed, clear pending offers
        artist.pending_label_offers = []


def _run_contract_negotiation_ui(artist: Any, label: Label) -> None:
    print("\n" + "=" * 65)
    print(f"       CONTRACT NEGOTIATION ROOM: {label.name.upper()}")
    print("=" * 65)
    print(f"  Tier               : {label.tier.upper()}")
    print(f"  Standard Advance   : {money_fmt(label.base_advance)}")
    print(f"  Album Commitment   : {label.album_commitment} Albums")
    print(f"  Contract Term      : {label.contract_years} Years")
    print(f"  Post-Recoup Cut    : {int(label.post_recoup_royalty_cut * 100)}%")
    print(f"  Concert Merch Cut  : {int(label.concert_merch_cut * 100)}%")
    print(f"  Masters Retention  : {'Label Owned' if label.owns_masters else 'Artist Owned'}")
    print(f"  Negotiable Terms   : {', '.join(label.negotiable_fields) if label.negotiable_fields else 'Strict (Non-negotiable)'}")
    print("=" * 65)

    print("\nHow would you like to proceed?")
    print("  1. Sign standard contract immediately")
    print("  2. Negotiate contract terms")
    print("  3. Walk away from the table")

    choice = prompt_text("\nChoice: ", "").strip()
    if choice == "1":
        contract, advance = sign_contract(artist, label)
        print(f"\n* DEAL SIGNED! Welcome to {label.name}!")
        print(f"  Signing advance of {money_fmt(advance)} wired into your bank account.")
        input("\nPress Enter to continue...")
        return
    elif choice == "2":
        if not label.negotiable_fields:
            print(f"\n{label.name} legal counsel: 'Our contracts are standardized. We do not negotiate terms.'")
            accept = prompt_text("Accept standard terms anyway? (y/n): ", "n").strip().lower()
            if accept == "y":
                contract, advance = sign_contract(artist, label)
                print(f"\n* DEAL SIGNED! Welcome to {label.name}!")
                print(f"  Signing advance of {money_fmt(advance)} wired into your bank account.")
            input("\nPress Enter to continue...")
            return

        proposed: dict[str, Any] = {}
        print("\nEnter your proposed terms (leave blank to accept standard):")

        if "advance" in label.negotiable_fields:
            adv_str = prompt_text(f"Proposed Advance (Current {money_fmt(label.base_advance)}): $", "").strip()
            if adv_str.isdigit():
                proposed["advance"] = int(adv_str)

        if "album_commitment" in label.negotiable_fields:
            alb_str = prompt_text(f"Proposed Album Commitment (Current {label.album_commitment}): ", "").strip()
            if alb_str.isdigit():
                proposed["album_commitment"] = int(alb_str)

        if "contract_years" in label.negotiable_fields:
            yrs_str = prompt_text(f"Proposed Contract Years (Current {label.contract_years}): ", "").strip()
            if yrs_str.isdigit():
                proposed["contract_years"] = int(yrs_str)

        if "post_recoup_royalty_cut" in label.negotiable_fields:
            cut_str = prompt_text(f"Proposed Post-Recoup Cut % (Current {int(label.post_recoup_royalty_cut*100)}%): ", "").strip()
            if cut_str.isdigit():
                proposed["post_recoup_royalty_cut"] = float(cut_str) / 100.0

        if "concert_merch_cut" in label.negotiable_fields:
            c_str = prompt_text(f"Proposed Concert Merch Cut % (Current {int(label.concert_merch_cut*100)}%): ", "").strip()
            if c_str.isdigit():
                proposed["concert_merch_cut"] = float(c_str) / 100.0

        if not proposed:
            print("\nNo terms modified. Proceeding with standard contract.")
            contract, advance = sign_contract(artist, label)
            print(f"\n* DEAL SIGNED! Welcome to {label.name}!")
            print(f"  Signing advance of {money_fmt(advance)} wired into your bank account.")
            input("\nPress Enter to continue...")
            return

        print(f"\nSubmitting proposal to {label.name} executive board...")
        accepted_res, failure_res = negotiate_label_contract(artist, label, proposed)

        if failure_res:
            print("\n[NEGOTIATION COLLAPSED]")
            for r in failure_res:
                print(f"  - {label.name}: \"{r['response']}\"")
            print("\nThe label walked away from the negotiation.")
            input("\nPress Enter to continue...")
            return

        final_terms = {
            "advance_paid": label.base_advance,
            "album_commitment": label.album_commitment,
            "contract_years": label.contract_years,
            "damage_amount": label.damage_amount,
            "concert_merch_cut": label.concert_merch_cut,
            "post_recoup_royalty_cut": label.post_recoup_royalty_cut,
        }

        print("\n[EXECUTIVE FEEDBACK]")
        for r in accepted_res:
            fld = r["field"]
            print(f"  - On {fld}: \"{r['response']}\"")
            if fld == "advance":
                final_terms["advance_paid"] = int(r["final_value"])
            elif fld in final_terms:
                final_terms[fld] = r["final_value"]

        print("\nRevised Offer Summary:")
        print(f"  Advance           : {money_fmt(final_terms['advance_paid'])}")
        print(f"  Albums Required   : {final_terms['album_commitment']}")
        print(f"  Duration          : {final_terms['contract_years']} Years")
        print(f"  Post-Recoup Cut   : {int(final_terms['post_recoup_royalty_cut']*100)}%")
        print(f"  Concert Merch Cut : {int(final_terms['concert_merch_cut']*100)}%")

        sign_now = prompt_text("\nSign the revised deal? (y/n): ", "y").strip().lower()
        if sign_now == "y":
            contract, advance = sign_contract(artist, label, final_terms)
            print(f"\n* DEAL SIGNED! Welcome to {label.name}!")
            print(f"  Signing advance of {money_fmt(advance)} wired into your bank account.")
        else:
            print("\nYou turned down the revised offer.")
        input("\nPress Enter to continue...")


def _view_contract_overview(artist: Any, contract: LabelContract, label: Label) -> None:
    print("\n" + "=" * 65)
    print("                  LABEL CONTRACT DOSSIER")
    print("=" * 65)
    print(f"  Label              : {label.name} ({label.tier.upper()})")
    print(f"  Status             : {contract.status.upper()}")
    print(f"  Signed Week        : Week {contract.signed_week}")
    print(f"  Weeks Elapsed      : {contract.weeks_elapsed} / {contract.contract_years * 48} weeks")
    print(f"  Initial Advance    : {money_fmt(contract.advance_paid)}")
    print(f"  Recoupment Balance : {money_fmt(contract.recoupment_balance)}")
    print(f"  Label Promo Added  : {money_fmt(contract.label_promo_costs_added)}")

    # Visual Recoupment Progress Bar
    total_charged = contract.advance_paid + contract.label_promo_costs_added
    cleared = max(0, total_charged - contract.recoupment_balance)
    pct = cleared / max(1, total_charged)
    print(f"  Recoupment Progress: {meter_bar(pct * 100, 100)} {pct*100:.1f}%")

    print(f"  Albums Fulfilled   : {contract.albums_delivered} / {contract.album_commitment}")
    print(f"  Breach Penalty     : {money_fmt(contract.damage_amount)} per undelivered album")
    print(f"  Post-Recoup Cut    : {int(contract.post_recoup_royalty_cut * 100)}% to label")
    print(f"  Concert/Merch Cut  : {int(contract.concert_merch_cut * 100)}% to label")
    print(f"  Masters Retention  : {'Label Owned' if contract.masters_owned_by_label else 'Artist Retained'}")
    print("-" * 65)
    print("  Active Benefits:")
    print(f"  - Weekly Ad Push   : {money_fmt(label.weekly_ad_budget)}/wk")
    print(f"  - Seat Guarantee   : {int(label.guaranteed_attendance_pct * 100)}% minimum concert fill")
    print(f"  - Label Collabs    : {'100% Free Collab Discount' if label.collab_discount else 'Standard Market'}")
    print("=" * 65)
    input("\nPress Enter to return...")


def _view_label_roster(artist: Any, label: Label, ecosystem_world: Any = None) -> None:
    curr_wk = getattr(artist, "current_week", 1)
    roster_views = get_label_roster_artists(label, artist, ecosystem_world, current_week=curr_wk)

    eligible = [a for a in roster_views if not a.is_onboarding]
    onboarding = [a for a in roster_views if a.is_onboarding]

    print("\n" + "=" * 92)
    print(f"               {label.name.upper()} RELEASE PRIORITY LEADERBOARD")
    print("=" * 92)
    print(f"{'Rank':<6} {'Artist Name':<24} {'W5 Pop':<10} {'W1 Pop':<10} {'Growth':<10} {'Priority':<14} {'Status':<14}")
    print("-" * 92)

    for i, a in enumerate(eligible, 1):
        is_player = (a.name == artist.name)
        status = "* PRIORITY" if i <= label.priority_threshold else "Standard"
        marker = " [YOU]" if is_player else ""
        name_str = f"{a.name}{marker}"[:23]
        g_str = f"{a.growth:+0.1f}"
        print(f"#{i:<5} {name_str:<24} {a.popularity:<10.1f} {a.popularity_w1:<10.1f} {g_str:<10} {a.priority_score:<14.1f} {status:<14}")

    if onboarding:
        print("-" * 92)
        print("  ONBOARDING ROSTER (First 4 Weeks -- No Release Priority Yet):")
        for a in onboarding:
            is_player = (a.name == artist.name)
            marker = " [YOU]" if is_player else ""
            name_str = f"{a.name}{marker}"[:23]
            wk_status = f"Onboarding (Wk {a.weeks_in_label}/4)"
            print(f"{'--':<6} {name_str:<24} {a.popularity:<10.1f} {'--':<10} {'--':<10} {'--':<14} {wk_status:<14}")

    print("=" * 92)
    print("  Model: P = 0.75 * C (Nonlinear Pop Log-Odds) + 0.25 * M (Absolute Growth Momentum)")
    print(f"  Priority Threshold: Top {label.priority_threshold} artists receive full promotional push & playlisting.")
    print("  Onboarding Rule: Newly signed artists spend 4 weeks in onboarding before entering the priority board.")
    input("\nPress Enter to return...")


def _handle_contract_buyout(artist: Any, contract: LabelContract, label: Label) -> None:
    albums_owed = max(0, contract.album_commitment - contract.albums_delivered)
    penalty = int(contract.damage_amount * albums_owed)
    total_buyout = contract.recoupment_balance + penalty

    print("\n" + "=" * 65)
    print("                 EARLY RELEASE / MASTERS BUYOUT")
    print("=" * 65)
    print(f"  Undelivered Albums : {albums_owed}")
    print(f"  Breach Damages     : {money_fmt(penalty)}")
    print(f"  Unrecouped Debt    : {money_fmt(contract.recoupment_balance)}")
    print(f"  Total Buyout Price : {money_fmt(total_buyout)}")
    print(f"  Your Bank Balance  : {money_fmt(artist.money)}")
    print("=" * 65)

    if artist.money < total_buyout:
        print("\n  [INSUFFICIENT FUNDS] You do not have enough money to buy out your contract.")
        input("\nPress Enter to return...")
        return

    confirm = prompt_text(f"Pay {money_fmt(total_buyout)} to terminate contract and regain independence? (y/n): ", "n").strip().lower()
    if confirm == "y":
        artist.money -= total_buyout
        contract.status = "expired"
        contract.recoupment_balance = 0
        contract.masters_owned_by_label = False
        if artist.name in label.signed_artists:
            label.signed_artists.remove(artist.name)
        artist.label_contract = None
        print(f"\n* CONTRACT TERMINATED! You have purchased your freedom and masters from {label.name}!")
        print("  You are now fully independent.")
        input("\nPress Enter to continue...")
