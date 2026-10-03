"""Concert and Venue system for the rapsim career simulator."""

import random
import math
from dataclasses import dataclass, field
from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS
from rapsim_reviews.date_system import format_week_range

# ──────────────────────────────────────────────────────────────────────
#  DATA STRUCTURES
# ──────────────────────────────────────────────────────────────────────

@dataclass
class Venue:
    id: str
    name: str
    city: str
    country: str
    category: str          # "club" | "auditorium" | "theatre" | "ground" | "arena" | "stadium"
    capacity: int
    popularity_req: int    # min popularity to be considered
    prestige: int          # 1–100, affects rep gain from performing
    organizer_id: str
    ticket_tiers: dict     # {"floor": base_price, "general": base_price, "vip": base_price}
    ambiance_bonus: float  # quality bonus to live performance score
    weekly_availability: list[int] = field(default_factory=list)

    def __post_init__(self):
        # Deterministically populate weekly availability (weeks 1 to 52) based on venue ID
        # Venues are now much scarcer (available in only 5 to 15 weeks per year)
        if not self.weekly_availability:
            rng = random.Random(self.id)
            num_weeks = rng.randint(5, 15)
            self.weekly_availability = sorted(rng.sample(range(1, 53), num_weeks))


@dataclass
class ConcertBooking:
    id: str
    venue_id: str
    week: int
    setlist: list[str]          # song ids in order
    ticket_prices: dict         # {"floor": x, "general": y, "vip": z}
    guest_artists: list[dict]   # [{"artist": name, "paid": bool, "fee": int, "performed": bool}]
    opening_act: str | None     # artist name
    opening_act_is_underground: bool
    attendance: int             # calculated at show time
    capacity_fill_pct: float
    gross_revenue: float
    net_revenue: float          # after fees, guests, opening act
    organizer_cut: float        # percentage
    live_popularity_delta: float
    rep_delta: float
    controversy_events: list    # mid/post concert events that fired
    performance_score: float    # 1–10, based on setlist quality and attendance
    booking_cost: float = 0.0
    guest_artist_cost: float = 0.0
    opening_act_fee: float = 0.0
    accidental_cost: float = 0.0
    profit_margin: float = 0.0
    attendance_target: int = 0  # final target attendance calculated at booking
    promotion_boost: float = 1.0 # ticket sales boost factor: 1.0, 1.10, 1.25, 1.50
    duration_hours: float = 0.0


# ──────────────────────────────────────────────────────────────────────
#  VENUES DEFINITION (50 Venues)
# ──────────────────────────────────────────────────────────────────────

VENUES = [
    # ── CLUBS (capacity 200–1500) ────────────────────────────────────────
    Venue("v01", "The Meridian", "Chicago", "USA", "club", 300,
          popularity_req=2, prestige=18, organizer_id="org_01",
          ticket_tiers={"floor": 15, "general": 10, "vip": 35}, ambiance_bonus=0.3),

    Venue("v02", "Basement Show", "Brooklyn", "USA", "club", 200,
          popularity_req=0, prestige=12, organizer_id="org_01",
          ticket_tiers={"floor": 10, "general": 8, "vip": 25}, ambiance_bonus=0.2),

    Venue("v03", "The Neon Den", "Atlanta", "USA", "club", 450,
          popularity_req=5, prestige=22, organizer_id="org_02",
          ticket_tiers={"floor": 20, "general": 15, "vip": 50}, ambiance_bonus=0.3),

    Venue("v04", "Fabric", "London", "UK", "club", 800,
          popularity_req=8, prestige=35, organizer_id="org_03",
          ticket_tiers={"floor": 25, "general": 18, "vip": 70}, ambiance_bonus=0.4),

    Venue("v05", "Tresor", "Berlin", "Germany", "club", 1200,
          popularity_req=10, prestige=40, organizer_id="org_04",
          ticket_tiers={"floor": 22, "general": 16, "vip": 60}, ambiance_bonus=0.4),

    Venue("v06", "Club Parallax", "Los Angeles", "USA", "club", 600,
          popularity_req=6, prestige=28, organizer_id="org_02",
          ticket_tiers={"floor": 25, "general": 18, "vip": 65}, ambiance_bonus=0.3),

    Venue("v07", "The Voltage Room", "Detroit", "USA", "club", 350,
          popularity_req=3, prestige=20, organizer_id="org_01",
          ticket_tiers={"floor": 15, "general": 10, "vip": 40}, ambiance_bonus=0.25),

    Venue("v08", "Underground Cipher", "Houston", "USA", "club", 500,
          popularity_req=4, prestige=24, organizer_id="org_02",
          ticket_tiers={"floor": 18, "general": 12, "vip": 45}, ambiance_bonus=0.3),

    Venue("v09", "Boiler Room Studio", "New York", "USA", "club", 250,
          popularity_req=5, prestige=30, organizer_id="org_05",
          ticket_tiers={"floor": 20, "general": 15, "vip": 55}, ambiance_bonus=0.35),

    Venue("v10", "The Late Room", "Toronto", "Canada", "club", 700,
          popularity_req=7, prestige=26, organizer_id="org_06",
          ticket_tiers={"floor": 22, "general": 16, "vip": 55}, ambiance_bonus=0.3),

    # ── AUDITORIUMS (capacity 1500–5000) ─────────────────────────────────
    Venue("v11", "Ryman Auditorium", "Nashville", "USA", "auditorium", 2300,
          popularity_req=20, prestige=55, organizer_id="org_07",
          ticket_tiers={"floor": 60, "general": 40, "vip": 120}, ambiance_bonus=0.5),

    Venue("v12", "Apollo Theater", "New York", "USA", "auditorium", 1500,
          popularity_req=18, prestige=70, organizer_id="org_08",
          ticket_tiers={"floor": 80, "general": 55, "vip": 160}, ambiance_bonus=0.6),

    Venue("v13", "The Wiltern", "Los Angeles", "USA", "auditorium", 1850,
          popularity_req=22, prestige=58, organizer_id="org_09",
          ticket_tiers={"floor": 65, "general": 45, "vip": 140}, ambiance_bonus=0.5),

    Venue("v14", "Hammersmith Apollo", "London", "UK", "auditorium", 3600,
          popularity_req=30, prestige=65, organizer_id="org_03",
          ticket_tiers={"floor": 70, "general": 50, "vip": 150}, ambiance_bonus=0.55),

    Venue("v15", "Paradiso", "Amsterdam", "Netherlands", "auditorium", 2000,
          popularity_req=25, prestige=60, organizer_id="org_10",
          ticket_tiers={"floor": 65, "general": 45, "vip": 140}, ambiance_bonus=0.5),

    Venue("v16", "House of Blues Chicago", "Chicago", "USA", "auditorium", 1800,
          popularity_req=20, prestige=52, organizer_id="org_07",
          ticket_tiers={"floor": 55, "general": 38, "vip": 120}, ambiance_bonus=0.45),

    Venue("v17", "9:30 Club", "Washington DC", "USA", "auditorium", 1200,
          popularity_req=15, prestige=48, organizer_id="org_11",
          ticket_tiers={"floor": 50, "general": 35, "vip": 110}, ambiance_bonus=0.45),

    Venue("v18", "Le Bataclan", "Paris", "France", "auditorium", 1500,
          popularity_req=20, prestige=58, organizer_id="org_12",
          ticket_tiers={"floor": 60, "general": 42, "vip": 130}, ambiance_bonus=0.5),

    Venue("v19", "Enmore Theatre", "Sydney", "Australia", "auditorium", 2500,
          popularity_req=25, prestige=52, organizer_id="org_13",
          ticket_tiers={"floor": 58, "general": 40, "vip": 125}, ambiance_bonus=0.45),

    Venue("v20", "The Palace Theatre", "Melbourne", "Australia", "auditorium", 2800,
          popularity_req=28, prestige=56, organizer_id="org_13",
          ticket_tiers={"floor": 62, "general": 44, "vip": 135}, ambiance_bonus=0.5),

    # ── THEATRES (capacity 3000–8000) ────────────────────────────────────
    Venue("v21", "Radio City Music Hall", "New York", "USA", "theatre", 6015,
          popularity_req=40, prestige=78, organizer_id="org_08",
          ticket_tiers={"floor": 120, "general": 80, "vip": 250}, ambiance_bonus=0.65),

    Venue("v22", "The Fox Theatre", "Atlanta", "USA", "theatre", 4678,
          popularity_req=38, prestige=72, organizer_id="org_14",
          ticket_tiers={"floor": 100, "general": 70, "vip": 220}, ambiance_bonus=0.6),

    Venue("v23", "Beacon Theatre", "New York", "USA", "theatre", 2894,
          popularity_req=35, prestige=68, organizer_id="org_08",
          ticket_tiers={"floor": 95, "general": 65, "vip": 200}, ambiance_bonus=0.6),

    Venue("v24", "Royal Albert Hall", "London", "UK", "theatre", 5272,
          popularity_req=42, prestige=85, organizer_id="org_03",
          ticket_tiers={"floor": 130, "general": 90, "vip": 280}, ambiance_bonus=0.7),

    Venue("v25", "Sydney Opera House", "Sydney", "Australia", "theatre", 5738,
          popularity_req=45, prestige=90, organizer_id="org_13",
          ticket_tiers={"floor": 150, "general": 100, "vip": 300}, ambiance_bonus=0.75),

    Venue("v26", "Shrine Auditorium", "Los Angeles", "USA", "theatre", 6300,
          popularity_req=43, prestige=80, organizer_id="org_09",
          ticket_tiers={"floor": 125, "general": 85, "vip": 260}, ambiance_bonus=0.65),

    Venue("v27", "Olympia Theatre", "Paris", "France", "theatre", 2000,
          popularity_req=35, prestige=75, organizer_id="org_12",
          ticket_tiers={"floor": 110, "general": 75, "vip": 240}, ambiance_bonus=0.65),

    Venue("v28", "The Forum", "Inglewood", "USA", "theatre", 7100,
          popularity_req=48, prestige=82, organizer_id="org_09",
          ticket_tiers={"floor": 140, "general": 95, "vip": 280}, ambiance_bonus=0.65),

    # ── GROUNDS (outdoor, capacity 8000–25000) ───────────────────────────
    Venue("v29", "Brixton Academy", "London", "UK", "ground", 5000,
          popularity_req=40, prestige=72, organizer_id="org_03",
          ticket_tiers={"floor": 85, "general": 60, "vip": 200}, ambiance_bonus=0.6),

    Venue("v30", "Red Rocks Amphitheatre", "Morrison CO", "USA", "ground", 9525,
          popularity_req=50, prestige=88, organizer_id="org_15",
          ticket_tiers={"floor": 100, "general": 70, "vip": 200}, ambiance_bonus=0.8),

    Venue("v31", "Hollywood Bowl", "Los Angeles", "USA", "ground", 17500,
          popularity_req=55, prestige=85, organizer_id="org_09",
          ticket_tiers={"floor": 120, "general": 80, "vip": 280}, ambiance_bonus=0.75),

    Venue("v32", "Gorge Amphitheatre", "George WA", "USA", "ground", 20000,
          popularity_req=55, prestige=82, organizer_id="org_15",
          ticket_tiers={"floor": 115, "general": 78, "vip": 260}, ambiance_bonus=0.75),

    Venue("v33", "Rock Werchter Ground", "Werchter", "Belgium", "ground", 88000,
          popularity_req=60, prestige=80, organizer_id="org_16",
          ticket_tiers={"floor": 90, "general": 65, "vip": 200}, ambiance_bonus=0.7),

    Venue("v34", "Coachella Main Stage", "Indio CA", "USA", "ground", 100000,
          popularity_req=65, prestige=92, organizer_id="org_17",
          ticket_tiers={"floor": 400, "general": 280, "vip": 900}, ambiance_bonus=0.8),

    Venue("v35", "Glastonbury Pyramid", "Somerset", "UK", "ground", 135000,
          popularity_req=68, prestige=95, organizer_id="org_18",
          ticket_tiers={"floor": 350, "general": 250, "vip": 800}, ambiance_bonus=0.85),

    # ── ARENAS (capacity 15000–25000) ────────────────────────────────────
    Venue("v36", "Barclays Center", "Brooklyn", "USA", "arena", 19000,
          popularity_req=60, prestige=80, organizer_id="org_08",
          ticket_tiers={"floor": 180, "general": 120, "vip": 450}, ambiance_bonus=0.7),

    Venue("v37", "Madison Square Garden", "New York", "USA", "arena", 20789,
          popularity_req=65, prestige=95, organizer_id="org_08",
          ticket_tiers={"floor": 250, "general": 160, "vip": 600}, ambiance_bonus=0.85),

    Venue("v38", "Crypto.com Arena", "Los Angeles", "USA", "arena", 21000,
          popularity_req=65, prestige=88, organizer_id="org_09",
          ticket_tiers={"floor": 220, "general": 150, "vip": 550}, ambiance_bonus=0.8),

    Venue("v39", "United Center", "Chicago", "USA", "arena", 23500,
          popularity_req=68, prestige=85, organizer_id="org_07",
          ticket_tiers={"floor": 200, "general": 140, "vip": 500}, ambiance_bonus=0.75),

    Venue("v40", "O2 Arena", "London", "UK", "arena", 20000,
          popularity_req=65, prestige=90, organizer_id="org_03",
          ticket_tiers={"floor": 220, "general": 155, "vip": 560}, ambiance_bonus=0.8),

    Venue("v41", "Accor Arena", "Paris", "France", "arena", 20300,
          popularity_req=65, prestige=85, organizer_id="org_12",
          ticket_tiers={"floor": 210, "general": 145, "vip": 530}, ambiance_bonus=0.78),

    Venue("v42", "Rod Laver Arena", "Melbourne", "Australia", "arena", 14820,
          popularity_req=62, prestige=82, organizer_id="org_13",
          ticket_tiers={"floor": 190, "general": 130, "vip": 480}, ambiance_bonus=0.75),

    Venue("v43", "Scotiabank Arena", "Toronto", "Canada", "arena", 19800,
          popularity_req=65, prestige=83, organizer_id="org_06",
          ticket_tiers={"floor": 200, "general": 140, "vip": 500}, ambiance_bonus=0.75),

    Venue("v44", "Mercedes-Benz Arena", "Berlin", "Germany", "arena", 17000,
          popularity_req=63, prestige=82, organizer_id="org_04",
          ticket_tiers={"floor": 195, "general": 135, "vip": 490}, ambiance_bonus=0.75),

    # ── STADIUMS (capacity 50000–100000+) ────────────────────────────────
    Venue("v45", "SoFi Stadium", "Inglewood CA", "USA", "stadium", 70240,
          popularity_req=80, prestige=92, organizer_id="org_09",
          ticket_tiers={"floor": 350, "general": 200, "vip": 900}, ambiance_bonus=0.85),

    Venue("v46", "MetLife Stadium", "East Rutherford NJ", "USA", "stadium", 82500,
          popularity_req=82, prestige=90, organizer_id="org_08",
          ticket_tiers={"floor": 320, "general": 185, "vip": 850}, ambiance_bonus=0.82),

    Venue("v47", "Wembley Stadium", "London", "UK", "stadium", 90000,
          popularity_req=85, prestige=98, organizer_id="org_03",
          ticket_tiers={"floor": 400, "general": 230, "vip": 1000}, ambiance_bonus=0.9),

    Venue("v48", "Stade de France", "Paris", "France", "stadium", 81338,
          popularity_req=83, prestige=90, organizer_id="org_12",
          ticket_tiers={"floor": 360, "general": 210, "vip": 920}, ambiance_bonus=0.85),

    Venue("v49", "Melbourne Cricket Ground", "Melbourne", "Australia", "stadium", 100024,
          popularity_req=85, prestige=88, organizer_id="org_13",
          ticket_tiers={"floor": 300, "general": 180, "vip": 800}, ambiance_bonus=0.82),

    Venue("v50", "Allegiant Stadium", "Las Vegas", "USA", "stadium", 65000,
          popularity_req=80, prestige=93, organizer_id="org_19",
          ticket_tiers={"floor": 380, "general": 220, "vip": 950}, ambiance_bonus=0.87),
]

# ──────────────────────────────────────────────────────────────────────
#  ORGANIZERS DEFINITION
# ──────────────────────────────────────────────────────────────────────

ORGANIZERS = {
    "org_01": {"name": "Ground Level Presents",      "strictness": 20, "city": "Chicago",     "negotiable": True},
    "org_02": {"name": "Street Sound Productions",   "strictness": 25, "city": "Atlanta",     "negotiable": True},
    "org_03": {"name": "UK Live Events",             "strictness": 55, "city": "London",      "negotiable": True},
    "org_04": {"name": "Berghain Collective",        "strictness": 50, "city": "Berlin",      "negotiable": False},
    "org_05": {"name": "Cipher Room Bookings",       "strictness": 30, "city": "New York",    "negotiable": True},
    "org_06": {"name": "North Stage Group",          "strictness": 35, "city": "Toronto",     "negotiable": True},
    "org_07": {"name": "Midwest Arena Corp",         "strictness": 45, "city": "Chicago",     "negotiable": True},
    "org_08": {"name": "Empire State Venues",        "strictness": 65, "city": "New York",    "negotiable": True},
    "org_09": {"name": "West Coast Presents",        "strictness": 60, "city": "Los Angeles", "negotiable": True},
    "org_10": {"name": "Canal Events BV",            "strictness": 45, "city": "Amsterdam",   "negotiable": True},
    "org_11": {"name": "Capitol Bookings",           "strictness": 40, "city": "Washington",  "negotiable": True},
    "org_12": {"name": "Spectacles de Paris",        "strictness": 55, "city": "Paris",       "negotiable": True},
    "org_13": {"name": "Pacific Rim Live",           "strictness": 50, "city": "Sydney",      "negotiable": True},
    "org_14": {"name": "Southern Stage Group",       "strictness": 42, "city": "Atlanta",     "negotiable": True},
    "org_15": {"name": "Outdoor Nation Events",      "strictness": 52, "city": "Denver",      "negotiable": True},
    "org_16": {"name": "European Festival Corp",     "strictness": 58, "city": "Brussels",    "negotiable": True},
    "org_17": {"name": "Goldenvoice",                "strictness": 80, "city": "Los Angeles", "negotiable": False},
    "org_18": {"name": "Festival Republic",          "strictness": 85, "city": "London",      "negotiable": False},
    "org_19": {"name": "Allegiant Entertainment",   "strictness": 70, "city": "Las Vegas",   "negotiable": True},
    "org_player": {"name": "Player Owned",           "strictness": 0,  "city": "Player City", "negotiable": True},
}

DEFAULT_PRICE_TEMPLATES = {
    "club":       {"floor": 20,  "general": 12,  "vip": 60},
    "auditorium": {"floor": 65,  "general": 45,  "vip": 150},
    "theatre":    {"floor": 110, "general": 75,  "vip": 260},
    "ground":     {"floor": 95,  "general": 65,  "vip": 210},
    "arena":      {"floor": 200, "general": 140, "vip": 500},
    "stadium":    {"floor": 320, "general": 200, "vip": 850},
}


def get_venue_costs(venue):
    # Retrieve hire costs and default organizer cut.
    # Stadium category charges more, with So-Fi Stadium v45 specifically demanding $1,500,000 hire cost and 55% cut.
    if venue.id == "v45":
        return 1500000.0, 0.55
    costs = {
        "club": (12000.0, 0.20),
        "auditorium": (35000.0, 0.25),
        "theatre": (80000.0, 0.30),
        "ground": (220000.0, 0.35),
        "arena": (500000.0, 0.40),
        "stadium": (1200000.0, 0.50)
    }
    return costs.get(venue.category, (0.0, 0.10))


# ──────────────────────────────────────────────────────────────────────
#  MATHEMATICAL FORMULAS
# ──────────────────────────────────────────────────────────────────────

def find_artist(name, player_artist=None):
    if player_artist and player_artist.name == name:
        return player_artist
    for seed in ARTIST_ECOSYSTEM_SEEDS:
        if seed.name == name:
            return seed
    return None


def find_song(sid, all_songs):
    for entry in all_songs:
        if hasattr(entry, "release_id") and entry.release_id == sid:
            song = entry.song
            song.total_streams = getattr(entry, "total_streams", 0)
            song.catchiness = getattr(entry.song, "catchiness", 2.0)
            return song
        if hasattr(entry, "song_id") and entry.song_id == sid:
            return entry
    return None


def calculate_concert_attendance(artist, venue, ticket_prices, guest_artists, week, duration_hours=2.0):
    base_capacity = venue.capacity

    # popularity pull — live popularity weighted higher
    live_pop = getattr(artist, "live_popularity", artist.popularity)
    pop_score = (live_pop * 0.6 + artist.popularity * 0.4) / 100
    pop_pull = pop_score ** 1.4  # non-linear — low pop = very low fill

    # ticket price sensitivity — higher prices reduce attendance
    if ticket_prices:
        avg_price = sum(ticket_prices.values()) / len(ticket_prices)
    else:
        avg_price = 1
    venue_base_avg = sum(venue.ticket_tiers.values()) / len(venue.ticket_tiers)
    price_ratio = venue_base_avg / max(avg_price, 1)
    price_factor = min(1.2, max(0.4, price_ratio))

    # guest artist pull
    guest_pull = 1.0
    for guest in guest_artists:
        g_artist = find_artist(guest["artist"])
        if g_artist:
            guest_pull += (g_artist.popularity / 100) * 0.15

    # venue prestige modifier
    prestige_factor = 1.0 + (venue.prestige / 100) * 0.1

    # popularity requirement gap penalty
    if artist.popularity < venue.popularity_req:
        gap = venue.popularity_req - artist.popularity
        gap_penalty = max(0.2, 1.0 - gap * 0.04)
    else:
        gap_penalty = 1.0

    fill_pct = pop_pull * price_factor * guest_pull * prestige_factor * gap_penalty

    # Bell curve ticket sales modifier based on concert duration in hours
    # Optimum length is 2.0 hours. Drops as length moves below 1.0 or above 3.0.
    duration_factor = math.exp(-0.5 * (duration_hours - 2.0) ** 2)
    fill_pct = fill_pct * duration_factor

    fill_pct = min(1.0, max(0.05, fill_pct + random.uniform(-0.05, 0.05)))

    return int(base_capacity * fill_pct), fill_pct


def evaluate_setlist(artist, setlist_song_ids, all_songs):
    if not setlist_song_ids:
        return 0.0

    songs = [find_song(sid, all_songs) for sid in setlist_song_ids if find_song(sid, all_songs)]
    if not songs:
        return 0.0

    total = 0.0
    for song in songs:
        total_streams = getattr(song, "total_streams", 0)
        song_pop_score = min(1.0, total_streams / 10_000_000)
        catchiness = getattr(song, "catchiness", 2.0)
        if catchiness is None:
            catchiness = 2.0
        score = (song.quality * 0.4 + song_pop_score * 10 * 0.4 + catchiness * 2 * 0.2)
        total += score

    avg = total / len(songs)
    return round(min(10.0, avg), 1)


def calculate_concert_revenue(booking, venue, organizer):
    floor_att = int(booking.attendance * 0.30)
    general_att = int(booking.attendance * 0.55)
    vip_att = int(booking.attendance * 0.15)

    gross = (
        floor_att   * booking.ticket_prices["floor"] +
        general_att * booking.ticket_prices["general"] +
        vip_att     * booking.ticket_prices["vip"]
    )

    org_cut = gross * booking.organizer_cut

    # guest artist fees
    guest_fees = sum(g.get("fee", 0) for g in booking.guest_artists if g.get("paid"))

    # opening act fee (if paid)
    opening_fee = getattr(booking, "opening_act_fee", 0.0)

    # venue hire
    hire_costs = booking.booking_cost

    net = gross - org_cut - guest_fees - opening_fee - hire_costs
    return gross, net, org_cut


def calculate_live_pop_delta(performance_score, fill_pct, artist):
    # performance quality contribution
    quality_delta = (performance_score - 5.0) * 0.8

    # fill percentage contribution — empty venues hurt
    if fill_pct >= 0.90:
        fill_delta = +4.0
    elif fill_pct >= 0.70:
        fill_delta = +2.0
    elif fill_pct >= 0.50:
        fill_delta = +0.5
    elif fill_pct >= 0.30:
        fill_delta = -1.0
    else:
        fill_delta = -4.0   # half-empty arena is devastating

    # opening act bonus
    opening_bonus = +2.0 if getattr(artist, "opening_act_is_underground", False) else +0.5

    return round(quality_delta + fill_delta + opening_bonus, 2)


def opening_act_rep_bonus(opening_act_artist):
    is_growing = False
    if hasattr(opening_act_artist, "skills"):
        skills = opening_act_artist.skills
        highest = max(skills.values()) if skills else 0
        if highest < 30:
            is_growing = True
    popularity = getattr(opening_act_artist, "popularity", 50.0)
    if is_growing:
        return +5  # rep bonus for supporting underground talent
    elif popularity < 20:
        return +3
    elif popularity < 40:
        return +1
    else:
        return 0


# Ticket sales dynamic progression
def calculate_current_sales(booking, current_week):
    weeks_left = booking.week - current_week
    if weeks_left <= 0:
        return booking.attendance_target
    rng = random.Random(booking.id + f":w{current_week}")
    if weeks_left == 1:
        progress = rng.uniform(0.85, 0.95)
    elif weeks_left == 2:
        progress = rng.uniform(0.65, 0.80)
    elif weeks_left == 3:
        progress = rng.uniform(0.40, 0.60)
    else:
        progress = rng.uniform(0.15, 0.30)
    return int(booking.attendance_target * progress)


# ──────────────────────────────────────────────────────────────────────
#  ORGANIZER NEGOTIATION RESPONSES
# ──────────────────────────────────────────────────────────────────────

ORGANIZER_NEGOTIATION_RESPONSES = {
    "accept_full": [
        "the dates work. we'll get the contract to your team by end of week.",
        "we'd love to have you. let's lock this in.",
        "deal. send over the rider and we'll confirm.",
        "you've got the slot. looking forward to working with you.",
    ],
    "counter_offer": [
        "we can do this but the organizer cut needs to come up to {counter_pct}%. take it or leave it.",
        "the slot is available but we need a {counter_pct}% cut. non-negotiable from our side.",
        "we'll go to {counter_pct}% and throw in the production support. final offer.",
        "our floor is {counter_pct}%. if that works, we're in business.",
    ],
    "decline_popularity": [
        "we appreciate the interest but your current draw doesn't justify this venue size. come back when the numbers are there.",
        "the capacity risk is too high at your current popularity level. we have to pass.",
        "we need to see stronger streaming numbers before we can offer this slot. check back with us.",
        "the venue has a reputation to protect. the numbers don't support this booking right now.",
    ],
    "decline_reputation": [
        "given recent press we're going to hold off on this booking for now.",
        "the controversy situation is making our sponsors nervous. we'll revisit when things settle.",
        "our venue has existing partnerships that make this booking complicated right now.",
        "we need to pass. the optics aren't right at the moment.",
    ],
    "hard_no": [
        "we're fully booked for that window.",
        "this isn't the right fit for our venue.",
        "we're going in a different direction for that slot.",
    ],
    "impressed_overbid": [
        "that's a very generous offer. we'll make sure you get the best production support we have.",
        "we weren't expecting that. you've got the slot and we'll throw in the house promotion team.",
        "deal. and we'll bump you to top billing on all our marketing materials.",
    ],
}


# ──────────────────────────────────────────────────────────────────────
#  CONCERT CONTROVERSIES (30 CP1252-safe Scenarios)
# ──────────────────────────────────────────────────────────────────────

CONCERT_CONTROVERSIES = [
    # ── MID-CONCERT ──
    {
        "id": "cc_01",
        "trigger": "mid",
        "scenario": "The crowd is filming everything. You grab the mic and call out a politician by name.",
        "options": [
            {"text": "Go all in — name them and say everything.",
             "rep_delta": -8, "pop_delta": +12, "accidental_cost": 0,
             "outcome": "The clip goes viral. Half the internet loves it, half wants your career ended."},
            {"text": "Soften it — allude without naming.",
             "rep_delta": +3, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Fans appreciate the boldness. Press can't pin anything specific on you."},
            {"text": "Pull back. Say something vague and move on.",
             "rep_delta": +1, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Nothing happens. The moment passes."},
        ]
    },
    {
        "id": "cc_02",
        "trigger": "mid",
        "scenario": "A heckler in the front row is loudly talking through your set. Security is waiting for your signal.",
        "options": [
            {"text": "Have security remove them immediately.",
             "rep_delta": -4, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Clip of the removal goes viral. Seen as aggressive by some, necessary by others."},
            {"text": "Call them out on the mic — let the crowd handle it.",
             "rep_delta": +5, "pop_delta": +8, "accidental_cost": 0,
             "outcome": "Crowd turns on the heckler. You look in control. Energy spikes."},
            {"text": "Ignore them and power through.",
             "rep_delta": +2, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Professionalism noted. Energy slightly dips from the distraction."},
            {"text": "Invite them on stage — make it a moment.",
             "rep_delta": +10, "pop_delta": +7, "accidental_cost": 0,
             "outcome": "Becomes the story of the night. Widely shared. Fans love the energy."},
        ]
    },
    {
        "id": "cc_03",
        "trigger": "mid",
        "scenario": "A fan throws something on stage. It nearly hits you. The crowd goes tense.",
        "options": [
            {"text": "Stop the show. Address it directly and firmly.",
             "rep_delta": +6, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Fans respect the boundary-setting. Incident is widely discussed."},
            {"text": "Laugh it off and keep going.",
             "rep_delta": +4, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Fans love the unflappable energy. Show moves on."},
            {"text": "Walk off stage. You're done.",
             "rep_delta": -10, "pop_delta": -8, "accidental_cost": 1000,
             "outcome": "Backlash is immediate. Fans who paid feel cheated. Small venue fine applied."},
            {"text": "Pick it up and throw it back.",
             "rep_delta": -6, "pop_delta": +10, "accidental_cost": 5000,
             "outcome": "The clip is everywhere. Half the internet calls it unhinged. You face legal costs of $5,000."},
        ]
    },
    {
        "id": "cc_04",
        "trigger": "mid",
        "scenario": "Your beef rival is rumoured to be in the building tonight. The crowd is murmuring.",
        "options": [
            {"text": "Address it — 'I heard someone's here tonight. Let them watch.'",
             "rep_delta": +8, "pop_delta": +15, "accidental_cost": 0,
             "outcome": "The clip dominates social media. Beef escalates officially."},
            {"text": "Play the song you dissed them on.",
             "rep_delta": +5, "pop_delta": +10, "accidental_cost": 0,
             "outcome": "The crowd loses it. The rival reportedly leaves."},
            {"text": "Ignore it completely.",
             "rep_delta": +3, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Nothing happens. Some fans are disappointed."},
            {"text": "Invite them on stage publicly.",
             "rep_delta": +15, "pop_delta": +12, "accidental_cost": 0,
             "outcome": "Legendary moment of tension. Internet explodes."},
        ]
    },
    {
        "id": "cc_05",
        "trigger": "mid",
        "scenario": "Your mic cuts out mid-verse. The crowd is waiting. The engineer is scrambling.",
        "options": [
            {"text": "Hold the mic up — let the crowd finish the verse a cappella.",
             "rep_delta": +12, "pop_delta": +10, "accidental_cost": 0,
             "outcome": "One of the most shared concert moments of the week."},
            {"text": "Walk offstage while they fix it.",
             "rep_delta": -3, "pop_delta": -2, "accidental_cost": 0,
             "outcome": "Crowd gets restless. Energy dips noticeably."},
            {"text": "Keep performing without the mic — scream it.",
             "rep_delta": +8, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Crowd respects the commitment."},
            {"text": "Address the venue on mic once restored — call them out.",
             "rep_delta": -5, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Organizer relationship damaged. Fans sympathise."},
        ]
    },
    {
        "id": "cc_06",
        "trigger": "mid",
        "scenario": "A fan faints in the crowd. Security is responding but the show is technically still going.",
        "options": [
            {"text": "Stop the show immediately and make sure they're okay.",
             "rep_delta": +15, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Universally praised. The person is fine. You look like a human being."},
            {"text": "Let security handle it, keep the show going.",
             "rep_delta": -8, "pop_delta": -3, "accidental_cost": 0,
             "outcome": "Widely criticised. Clip circulates unfavourably."},
            {"text": "Pause briefly, check in on the mic, resume when clear.",
             "rep_delta": +8, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Balanced and professional. Minimal controversy."},
        ]
    },
    {
        "id": "cc_07",
        "trigger": "mid",
        "scenario": "You're at a festival. The headliner after you is someone you have public beef with. The crowd is asking you to go long and delay their set.",
        "options": [
            {"text": "Go 20 minutes over. Give the crowd what they want.",
             "rep_delta": -10, "pop_delta": +8, "accidental_cost": 15000,
             "outcome": "Organiser furious. Feud escalates. Festival fines you $15,000."},
            {"text": "Wrap on time. Be professional.",
             "rep_delta": +8, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "Industry respects it. Rival relationship unchanged."},
            {"text": "Go 5 minutes over — just enough.",
             "rep_delta": -3, "pop_delta": +5, "accidental_cost": 2000,
             "outcome": "Noticed but not egregious. Minor fine of $2,000 applied."},
            {"text": "End 5 minutes early and let them wait on stage.",
             "rep_delta": +6, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Unexpected move. Internet calls it a masterclass in confidence."},
        ]
    },
    {
        "id": "cc_08",
        "trigger": "mid",
        "scenario": "You're mid-show and someone in the crowd holds up a sign criticising your recent album.",
        "options": [
            {"text": "Address it directly — 'I see you. That album is the best thing I've made.'",
             "rep_delta": +6, "pop_delta": +8, "accidental_cost": 0,
             "outcome": "Crowd cheers. Confidence is infectious."},
            {"text": "Have security remove the sign but say nothing.",
             "rep_delta": -5, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Clip of the removal circulates. Looks insecure."},
            {"text": "Laugh it off. 'At least you bought a ticket.'",
             "rep_delta": +10, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Becomes a fan-favourite moment."},
            {"text": "Get defensive and go on a rant.",
             "rep_delta": -12, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Clip goes everywhere for the wrong reasons."},
        ]
    },
    {
        "id": "cc_09",
        "trigger": "mid",
        "scenario": "During a quiet moment, someone in the crowd starts a chant for your rival.",
        "options": [
            {"text": "Cut the music and stare them down silently.",
             "rep_delta": +5, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Intimidating and iconic. Rival's fanbase goes wild online."},
            {"text": "Acknowledge it, laugh, keep going.",
             "rep_delta": +8, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Confidence noted. You look unbothered."},
            {"text": "Launch into the diss track immediately.",
             "rep_delta": +3, "pop_delta": +12, "accidental_cost": 0,
             "outcome": "Crowd erupts. Beef gets another news cycle."},
            {"text": "Ask security to identify and remove them.",
             "rep_delta": -8, "pop_delta": -4, "accidental_cost": 0,
             "outcome": "Looks extremely insecure. Backlash across all platforms."},
        ]
    },
    {
        "id": "cc_10",
        "trigger": "mid",
        "scenario": "Your guest artist is late. They were supposed to appear three songs ago. The crowd is noticing.",
        "options": [
            {"text": "Call them out on stage — 'Where is the guest?'",
             "rep_delta": -6, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Crowd finds it funny. Guest is furious. Relationship decreases."},
            {"text": "Cover with freestyles until they arrive.",
             "rep_delta": +8, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Fans respect the improvisation. When guest arrives, energy is high."},
            {"text": "Skip them entirely and close strong.",
             "rep_delta": +3, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "Clean show. Guest relationship unaffected but awkward later."},
            {"text": "Tell the crowd honestly — 'They're running late, we're going without.'",
             "rep_delta": +5, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Transparency appreciated. Crowd redirects energy to you."},
        ]
    },

    # ── POST-CONCERT ──
    {
        "id": "cc_11",
        "trigger": "post",
        "scenario": "Video surfaces from backstage — your entourage argued with venue staff and it escalated.",
        "options": [
            {"text": "Issue a statement taking full responsibility.",
             "rep_delta": +8, "pop_delta": -3, "accidental_cost": 2000,
             "outcome": "Appreciated. Incident fades quickly, but you cover damages of $2,000."},
            {"text": "Deny any knowledge of the incident.",
             "rep_delta": -10, "pop_delta": -2, "accidental_cost": 0,
             "outcome": "The video clearly shows your team. Worse than admitting it."},
            {"text": "Cut the entourage member responsible.",
             "rep_delta": +5, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Public accountability. The incident becomes a footnote."},
            {"text": "Say nothing and wait it out.",
             "rep_delta": -5, "pop_delta": -1, "accidental_cost": 0,
             "outcome": "The silence is read as guilt. News cycle lasts 2 extra weeks."},
        ]
    },
    {
        "id": "cc_12",
        "trigger": "post",
        "scenario": "A review calls your performance 'career-worst' and it's trending. The reviewer attended.",
        "options": [
            {"text": "Respond on Twitter with receipts of crowd reaction.",
             "rep_delta": +4, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Fans rally. Reviewer doubles down. News cycle extends."},
            {"text": "Invite them to the next show, front row.",
             "rep_delta": +12, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Universally praised move. Reviewer is disarmed."},
            {"text": "Say nothing. The show was what it was.",
             "rep_delta": +3, "pop_delta": -2, "accidental_cost": 0,
             "outcome": "Review fades. Perceived as secure."},
            {"text": "Attack the reviewer publicly.",
             "rep_delta": -10, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "You look petty. Reviewer becomes sympathetic figure."},
        ]
    },
    {
        "id": "cc_13",
        "trigger": "post",
        "scenario": "A fan posts a clip of you looking exhausted mid-show — 'Is the artist burning out?'",
        "options": [
            {"text": "Post candidly about fatigue and the cost of touring.",
             "rep_delta": +12, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Fans respect the honesty. Mental health discourse follows."},
            {"text": "Post a workout video the next morning.",
             "rep_delta": +4, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Perception managed. Conversation moves on."},
            {"text": "Say nothing.",
             "rep_delta": 0, "pop_delta": -2, "accidental_cost": 0,
             "outcome": "Rumour persists quietly for 2 weeks."},
            {"text": "Announce new tour dates as a response.",
             "rep_delta": -4, "pop_delta": +8, "accidental_cost": 0,
             "outcome": "Seen as denial. Internally, fatigue compounds."},
        ]
    },
    {
        "id": "cc_14",
        "trigger": "post",
        "scenario": "The opening act you gave a slot to publicly thanks you and the post goes massively viral.",
        "options": [
            {"text": "Repost and add kind words.",
             "rep_delta": +8, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Both artists benefit. Underground community rallies around you."},
            {"text": "Like it and move on.",
             "rep_delta": +3, "pop_delta": +1, "accidental_cost": 0,
             "outcome": "Warm but low-key. Appreciated nonetheless."},
            {"text": "Offer them a collab publicly.",
             "rep_delta": +12, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Industry takes note. The underground artist's career accelerates."},
        ]
    },
    {
        "id": "cc_15",
        "trigger": "post",
        "scenario": "The venue was oversold. Fans without seats are furious online. The organizer is blaming your team.",
        "options": [
            {"text": "Take the organizer's side publicly.",
             "rep_delta": -8, "pop_delta": -3, "accidental_cost": 0,
             "outcome": "Fans feel abandoned. Organizer relationship preserved but fan trust damaged."},
            {"text": "Take the fans' side and publicly blame the organizer.",
             "rep_delta": +6, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Fans love you. Organizer relationship damaged. Future bookings with them complicated."},
            {"text": "Offer refunds from your own pocket for the affected fans.",
             "rep_delta": +18, "pop_delta": +8, "accidental_cost": 10000,
             "outcome": "Extraordinary moment. Goes viral for all the right reasons. Refund cost: $10,000."},
            {"text": "Stay out of it entirely.",
             "rep_delta": -4, "pop_delta": -2, "accidental_cost": 0,
             "outcome": "Both sides blame you for the silence."},
        ]
    },
    {
        "id": "cc_16",
        "trigger": "post",
        "scenario": "The after-party gets out of hand. Photos circulate of your entourage in a compromising situation.",
        "options": [
            {"text": "Address it with humour — own the chaos.",
             "rep_delta": -3, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Fans find it relatable. Industry raises an eyebrow."},
            {"text": "Issue a professional statement and distance from the night.",
             "rep_delta": +4, "pop_delta": -2, "accidental_cost": 0,
             "outcome": "Clean and managed. Incident resolved in one cycle."},
            {"text": "Say absolutely nothing.",
             "rep_delta": -6, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "Speculation fills the silence for 3 weeks."},
        ]
    },
    {
        "id": "cc_17",
        "trigger": "post",
        "scenario": "A major artist who was in attendance posts a cold two-word review: 'it's okay.'",
        "options": [
            {"text": "Reply with 'appreciate you coming'.",
             "rep_delta": +6, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Dignified. Crowd takes your side. Other artist looks petty."},
            {"text": "Don't reply but perform even better next show — let the work speak.",
             "rep_delta": +5, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "Quiet confidence. Noticed by the industry."},
            {"text": "Reply aggressively.",
             "rep_delta": -8, "pop_delta": +7, "accidental_cost": 0,
             "outcome": "Entertaining beef begins. Reception is split."},
            {"text": "Like the tweet and move on.",
             "rep_delta": +8, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Universally called the most unbothered response possible. Iconic."},
        ]
    },
    {
        "id": "cc_18",
        "trigger": "post",
        "scenario": "A clip from your show is being used in a political advertisement without your consent.",
        "options": [
            {"text": "Issue a legal cease and desist publicly.",
             "rep_delta": +10, "pop_delta": +4, "accidental_cost": 3000,
             "outcome": "Universally supported. Legal fees cost $3,000."},
            {"text": "Post a statement distancing yourself from the party.",
             "rep_delta": +8, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Clean separation. Fans appreciate the clarity."},
            {"text": "Say nothing and hope it disappears.",
             "rep_delta": -8, "pop_delta": -4, "accidental_cost": 0,
             "outcome": "It doesn't disappear. You're now associated with the political position."},
            {"text": "Endorse the usage — align with the party.",
             "rep_delta": -15, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Fanbase splits. Long-term reputation damage. Short-term attention spike."},
        ]
    },
    {
        "id": "cc_19",
        "trigger": "post",
        "scenario": "Ticket touts made 5x face value on your show. Fans are angry at you personally.",
        "options": [
            {"text": "Announce verified fan presales for all future shows.",
             "rep_delta": +12, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Widely praised. Seen as genuinely addressing the problem."},
            {"text": "Say it's beyond your control — it's the venue's issue.",
             "rep_delta": -4, "pop_delta": -2, "accidental_cost": 0,
             "outcome": "Technically true. Fans still blame you somewhat."},
            {"text": "Lower ticket prices at the next show as a gesture.",
             "rep_delta": +8, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Appreciated but doesn't solve the touting problem."},
            {"text": "Say nothing.",
             "rep_delta": -6, "pop_delta": -3, "accidental_cost": 0,
             "outcome": "Seen as not caring about fans. Trust erodes quietly."},
        ]
    },
    {
        "id": "cc_20",
        "trigger": "post",
        "scenario": "A viral clip shows you were clearly lip-syncing two songs during the show.",
        "options": [
            {"text": "Come clean — explain it was a technical issue mid-show.",
             "rep_delta": +6, "pop_delta": -4, "accidental_cost": 0,
             "outcome": "Honest. Fans accept the explanation. Critics note it."},
            {"text": "Deny it entirely.",
             "rep_delta": -14, "pop_delta": -6, "accidental_cost": 0,
             "outcome": "The clip is undeniable. The denial is worse than the offence."},
            {"text": "Announce a free acoustic show as a makeup.",
             "rep_delta": +14, "pop_delta": +6, "accidental_cost": 8000,
             "outcome": "The recovery is the story. Makeup show costs you $8,000."},
            {"text": "Say nothing and release a live session video the next day.",
             "rep_delta": +5, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "Implicit response. Understood. Controversy fades."},
        ]
    },
    {
        "id": "cc_21",
        "trigger": "post",
        "scenario": "The promoter announces you'll be back for a second night due to demand. You haven't agreed to this.",
        "options": [
            {"text": "Confirm it publicly — give the fans what they want.",
             "rep_delta": +8, "pop_delta": +10, "accidental_cost": 0,
             "outcome": "Fans ecstatic. You sort the contract privately."},
            {"text": "Publicly correct the promoter — no second date confirmed.",
             "rep_delta": -3, "pop_delta": -5, "accidental_cost": 0,
             "outcome": "Fan disappointment. Promoter relationship strained."},
            {"text": "Negotiate privately and announce later.",
             "rep_delta": +4, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Clean. Second show confirmed week 2."},
        ]
    },
    {
        "id": "cc_22",
        "trigger": "post",
        "scenario": "A famous producer who attended posts that your live show 'changed the way he thinks about music'.",
        "options": [
            {"text": "Reply warmly and publicly.",
             "rep_delta": +8, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "Industry takes note. Feature requests increase."},
            {"text": "DM them privately and explore a collaboration.",
             "rep_delta": +5, "pop_delta": +3, "accidental_cost": 0,
             "outcome": "Relationship begins. Collab possible in 3–4 weeks."},
            {"text": "Let it exist. Don't engage.",
             "rep_delta": +3, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "The post does the work on its own."},
        ]
    },
    {
        "id": "cc_23",
        "trigger": "post",
        "scenario": "Your set ran 40 minutes short of the advertised runtime. Fans are demanding refunds.",
        "options": [
            {"text": "Offer partial refunds proactively.",
             "rep_delta": +10, "pop_delta": -2, "accidental_cost": 15000,
             "outcome": "Expensive but respected. Partial refunds cost $15,000."},
            {"text": "Say the setlist was complete as planned.",
             "rep_delta": -8, "pop_delta": -5, "accidental_cost": 0,
             "outcome": "Fans produce the advertisement as evidence. Backlash worsens."},
            {"text": "Announce a makeup show at a smaller venue, free entry.",
             "rep_delta": +15, "pop_delta": +6, "accidental_cost": 6000,
             "outcome": "One of the best PR recoveries possible. Cost: $6,000."},
            {"text": "Say nothing.",
             "rep_delta": -10, "pop_delta": -6, "accidental_cost": 0,
             "outcome": "Refund demands escalate. Trending for the wrong reasons."},
        ]
    },
    {
        "id": "cc_24",
        "trigger": "mid",
        "scenario": "A very drunk fan somehow gets on stage mid-performance.",
        "options": [
            {"text": "Improvise — perform with them for 30 seconds before security gets them.",
             "rep_delta": +14, "pop_delta": +10, "accidental_cost": 0,
             "outcome": "Clip goes massively viral. Seen as a genuine moment of joy."},
            {"text": "Step back and let security handle it immediately.",
             "rep_delta": 0, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Professional. Nothing memorable."},
            {"text": "Shove them away from the mic.",
             "rep_delta": -12, "pop_delta": -6, "accidental_cost": 1000,
             "outcome": "Clip circulates. Looks aggressive regardless of context. Fan files grievance: $1,000."},
        ]
    },
    {
        "id": "cc_25",
        "trigger": "mid",
        "scenario": "Smoke machine malfunction fills the stage with too much smoke. You can barely see.",
        "options": [
            {"text": "Keep performing through it — lean into the chaos.",
             "rep_delta": +8, "pop_delta": +5, "accidental_cost": 0,
             "outcome": "Fans respect the commitment. Becomes a funny story."},
            {"text": "Stop the show and address the venue tech team on mic.",
             "rep_delta": -3, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "Organiser is embarrassed. Fans find it entertaining."},
            {"text": "Walk into the crowd and perform from the floor.",
             "rep_delta": +16, "pop_delta": +12, "accidental_cost": 0,
             "outcome": "Legendary move. Clips from 40 different angles circulate."},
        ]
    },
    {
        "id": "cc_26",
        "trigger": "post",
        "scenario": "A photographer sold intimate backstage photos without consent.",
        "options": [
            {"text": "Pursue legal action publicly.",
             "rep_delta": +8, "pop_delta": +2, "accidental_cost": 4000,
             "outcome": "Supported universally. Sets a precedent. Legal fees: $4,000."},
            {"text": "Post about it on Twitter without naming the photographer.",
             "rep_delta": +5, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Fans help identify the photographer within hours."},
            {"text": "Let your team handle it quietly.",
             "rep_delta": +3, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Resolved privately. No public narrative."},
        ]
    },
    {
        "id": "cc_27",
        "trigger": "mid",
        "scenario": "The sound system goes out for 90 seconds during your biggest song.",
        "options": [
            {"text": "Acapella — perform the whole song without backing.",
             "rep_delta": +18, "pop_delta": +14, "accidental_cost": 0,
             "outcome": "Becomes a career-defining clip. Everyone who was there will talk about it forever."},
            {"text": "Pause and wait for the fix.",
             "rep_delta": -2, "pop_delta": -1, "accidental_cost": 0,
             "outcome": "Technical issue. No big consequence."},
            {"text": "Get visibly frustrated and throw your earpiece.",
             "rep_delta": -8, "pop_delta": +5, "accidental_cost": 1500,
             "outcome": "Clip of the earpiece throw is everywhere. Diva label attaches. Equipment replacement: $1,500."},
        ]
    },
    {
        "id": "cc_28",
        "trigger": "post",
        "scenario": "Your show generated complaints from local residents about noise. The venue is under city scrutiny.",
        "options": [
            {"text": "Publicly apologise to local residents.",
             "rep_delta": +6, "pop_delta": -1, "accidental_cost": 0,
             "outcome": "Gracious. Venue appreciates it. City softens."},
            {"text": "Say nothing — this is the venue's problem.",
             "rep_delta": 0, "pop_delta": 0, "accidental_cost": 0,
             "outcome": "Correct legally. Venue notes you didn't help."},
            {"text": "Defend the show publicly — 'music is meant to be heard'.",
             "rep_delta": +4, "pop_delta": +6, "accidental_cost": 5000,
             "outcome": "Fans love it. Local residents less charmed. City fines the booking $5,000."},
        ]
    },
    {
        "id": "cc_29",
        "trigger": "mid",
        "scenario": "A fan in the front row is clearly in distress — having a panic attack.",
        "options": [
            {"text": "Stop the show immediately and address it with care.",
             "rep_delta": +16, "pop_delta": +6, "accidental_cost": 0,
             "outcome": "The moment is shared widely and praised as genuinely human."},
            {"text": "Signal security discreetly and continue.",
             "rep_delta": +4, "pop_delta": +2, "accidental_cost": 0,
             "outcome": "Professional. Fan is helped. Show continues."},
            {"text": "Ask the crowd to give them space and keep performing.",
             "rep_delta": +8, "pop_delta": +4, "accidental_cost": 0,
             "outcome": "Balanced. Crowd responds well."},
        ]
    },
    {
        "id": "cc_30",
        "trigger": "post",
        "scenario": "Your performance was sampled without clearance in a viral social media trend. 50M views.",
        "options": [
            {"text": "Embrace it — repost and lean into the trend.",
             "rep_delta": +6, "pop_delta": +12, "accidental_cost": 0,
             "outcome": "Streams spike. Your name is everywhere."},
            {"text": "Issue a takedown — protect the IP.",
             "rep_delta": -4, "pop_delta": -6, "accidental_cost": 0,
             "outcome": "Legally sound. Internet calls you a killjoy for 2 weeks."},
            {"text": "Reach out to the trend creator and officially clear it for a credit.",
             "rep_delta": +10, "pop_delta": +8, "accidental_cost": 0,
             "outcome": "Seen as collaborative and modern. Best possible outcome."},
        ]
    },
]


# ──────────────────────────────────────────────────────────────────────
#  UI HELPERS (Deterministic console inputs/outputs to prevent circular imports)
# ──────────────────────────────────────────────────────────────────────

def choose_option(title, options):
    print(f"\n=== {title} ===")
    for i, opt in enumerate(options):
        print(f"[{i+1}] {opt}")
    while True:
        try:
            val = input(" >> ").strip()
            if not val:
                continue
            idx = int(val) - 1
            if 0 <= idx < len(options):
                return idx
        except ValueError:
            pass
        print("Invalid choice. Try again.")


def display_current_bookings(artist):
    if not getattr(artist, "upcoming_concerts", None):
        print("\nNo upcoming concerts scheduled.")
        input("Press Enter to continue...")
        return

    print("\n" + "=" * 50)
    print(" UPCOMING CONCERTS")
    print("=" * 50)
    current_wk = ((artist.year - 1) * 52) + artist.week
    for idx, booking in enumerate(artist.upcoming_concerts):
        venue = next((v for v in VENUES if v.id == booking.venue_id), None)
        venue_name = venue.name if venue else "Unknown Venue"
        w_left = booking.week - current_wk
        sold = calculate_current_sales(booking, current_wk)
        cap = venue.capacity if venue else 0
        fill_pct = (sold / cap * 100) if cap > 0 else 0.0
        print(f"[{idx+1}] {format_week_range(booking.week)} (In {w_left} weeks) at {venue_name}")
        print(f"    Capacity: {cap:,} | Tickets Sold: {sold:,} ({fill_pct:.1f}%)")
        print(f"    Duration: {booking.duration_hours:.1f} hours | Setlist: {len(booking.setlist)} songs")
        print(f"    Ticket Prices: Floor: ${booking.ticket_prices['floor']}, Gen: ${booking.ticket_prices['general']}, VIP: ${booking.ticket_prices['vip']}")
        if booking.guest_artists:
            guests_str = ", ".join(g["artist"] for g in booking.guest_artists)
            print(f"    Guests: {guests_str}")
        if booking.opening_act:
            print(f"    Opening Act: {booking.opening_act}")
    print("=" * 50)
    input("Press Enter to continue...")


def display_sales_analysis(artist):
    if not getattr(artist, "concert_history", None):
        print("\nNo completed concert history to analyze.")
        input("Press Enter to continue...")
        return

    print("\n" + "=" * 50)
    print(" CONCERT SALES ANALYSIS")
    print("=" * 50)
    for idx, booking in enumerate(artist.concert_history):
        venue = next((v for v in VENUES if v.id == booking.venue_id), None)
        venue_name = venue.name if venue else "Unknown Venue"
        print(f"[{idx+1}] {format_week_range(booking.week)} at {venue_name} ({venue.city if venue else ''})")
        print(f"    Performance Score: {booking.performance_score}/10 | Attendance: {booking.attendance:,} ({booking.capacity_fill_pct*100:.1f}%)")
        print(f"    Duration: {booking.duration_hours:.1f} hours")
        print(f"    Ticket Prices: Floor: ${booking.ticket_prices['floor']}, Gen: ${booking.ticket_prices['general']}, VIP: ${booking.ticket_prices['vip']}")
        print(f"    Booking (Venue Hire) Cost: ${booking.booking_cost:,.2f}")
        print(f"    Guest Artist Cost: ${booking.guest_artist_cost:,.2f}")
        print(f"    Opening Act Payment: ${booking.opening_act_fee:,.2f}")
        print(f"    Accidental Cost: ${booking.accidental_cost:,.2f}")
        print(f"    Gross Revenue: ${booking.gross_revenue:,.2f}")
        print(f"    Net Revenue: ${booking.net_revenue:,.2f}")
        print(f"    Profit Margin: {booking.profit_margin:.1f}%")
        print("-" * 50)
    print("=" * 50)
    input("Press Enter to continue...")


def setlist_templates_menu(artist):
    if not hasattr(artist, "setlist_templates"):
        artist.setlist_templates = {}

    while True:
        options = [
            "View Setlist Templates",
            "Create Setlist Template",
            "Delete Setlist Template",
            "Back"
        ]
        choice = choose_option("MANAGE SETLIST TEMPLATES", options)
        if choice == 0:
            if not artist.setlist_templates:
                print("\nNo setlist templates saved.")
            else:
                print("\n=== SETLIST TEMPLATES ===")
                for name, setlist in artist.setlist_templates.items():
                    released_songs = [s for s in artist.singles if s.released]
                    song_names = []
                    for sid in setlist:
                        song = find_song(sid, released_songs)
                        song_names.append(song.name if song else "Unknown Song")
                    print(f"- {name}: {', '.join(song_names)} ({len(setlist)} songs)")
            input("Press Enter to continue...")

        elif choice == 1:
            released_songs = [s for s in artist.singles if s.released]
            if not released_songs:
                print("\nYou have no released songs to build a setlist.")
                input("Press Enter to continue...")
                continue
            name = input("Enter template name (e.g. Festival Set): ").strip()
            if not name:
                print("Invalid name.")
                continue
            print("\nAvailable Songs:")
            for idx, s in enumerate(released_songs):
                print(f"[{idx+1}] {s.song.name}")
            print("\nEnter song numbers in order, separated by commas (e.g. 1,3,2,1):")
            try:
                inp = input(" >> ").strip()
                indices = [int(x.strip()) - 1 for x in inp.split(",") if x.strip()]
                if not indices or any(not (0 <= idx < len(released_songs)) for idx in indices):
                    print("Invalid song selection.")
                    continue
                artist.setlist_templates[name] = [released_songs[idx].release_id for idx in indices]
                print(f"Setlist template '{name}' saved successfully!")
            except Exception:
                print("Error building setlist template.")
            input("Press Enter to continue...")

        elif choice == 2:
            if not artist.setlist_templates:
                print("\nNo setlist templates saved.")
                input("Press Enter to continue...")
                continue
            names = list(artist.setlist_templates.keys())
            del_idx = choose_option("SELECT TEMPLATE TO DELETE", names + ["Cancel"])
            if del_idx == len(names):
                continue
            del artist.setlist_templates[names[del_idx]]
            print("Template deleted.")
            input("Press Enter to continue...")

        elif choice == 3:
            break


def concerts_menu(artist, world):
    # Ensure fields exist on Artist
    if not hasattr(artist, "upcoming_concerts"):
        artist.upcoming_concerts = []
    if not hasattr(artist, "concert_history"):
        artist.concert_history = []
    if not hasattr(artist, "price_templates"):
        artist.price_templates = dict(DEFAULT_PRICE_TEMPLATES)
    if not hasattr(artist, "live_popularity"):
        artist.live_popularity = 2.0
    if not hasattr(artist, "setlist_templates"):
        artist.setlist_templates = {}

    while True:
        options = [
            "Book a Venue",
            "My Upcoming Shows (View Current Bookings)",
            "Concert History / Sales Analysis",
            "Template Prices",
            "Manage Setlist Templates",
            "Back"
        ]
        choice = choose_option("CONCERTS", options)
        if choice == 0:
            book_venue_flow(artist, world)
        elif choice == 1:
            display_current_bookings(artist)
        elif choice == 2:
            display_sales_analysis(artist)
        elif choice == 3:
            manage_templates_menu(artist)
        elif choice == 4:
            setlist_templates_menu(artist)
        elif choice == 5:
            break


def manage_templates_menu(artist):
    while True:
        cats = list(artist.price_templates.keys())
        options = []
        for cat in cats:
            t = artist.price_templates[cat]
            options.append(f"{cat.capitalize()} Template (Floor: ${t['floor']}, Gen: ${t['general']}, VIP: ${t['vip']})")
        options.append("Back")
        choice = choose_option("TICKET PRICE TEMPLATES", options)
        if choice == len(cats):
            break
        cat = cats[choice]
        print(f"\nEditing template for {cat.upper()}:")
        try:
            floor = int(input("  Enter Floor ticket price ($): ").strip())
            gen = int(input("  Enter General Admission ticket price ($): ").strip())
            vip = int(input("  Enter VIP ticket price ($): ").strip())
            artist.price_templates[cat] = {"floor": floor, "general": gen, "vip": vip}
            print("Template updated successfully.")
        except ValueError:
            print("Invalid inputs. Prices must be integers.")
        input("Press Enter to continue...")


def book_venue_flow(artist, world):
    # Browse venues by category
    categories = ["club", "auditorium", "theatre", "ground", "arena", "stadium"]
    cat_idx = choose_option("CHOOSE VENUE CATEGORY", [c.upper() for c in categories] + ["Cancel"])
    if cat_idx == len(categories):
        return
    category = categories[cat_idx]

    pop_caps = {
        "club": 60.0,
        "auditorium": 70.0,
        "theatre": 80.0
    }
    pop_cap = pop_caps.get(category, 999.0)

    # Filter venues in that category
    cat_venues = [v for v in VENUES if v.category == category]

    # Inject player-owned operational venues
    if hasattr(artist, "owned_venues"):
        for ov in artist.owned_venues:
            if ov.status == "operational" and ov.category == category:
                prestige_val = int(ov.review_stars * 18.0)
                ticket_tiers = {"floor": int(ov.base_hire_cost * 0.02), "general": int(ov.base_hire_cost * 0.015), "vip": int(ov.base_hire_cost * 0.05)}
                if ticket_tiers["floor"] <= 0:
                    ticket_tiers = {"floor": 20, "general": 12, "vip": 60}
                
                mock_v = Venue(
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
                cat_venues.append(mock_v)

    options = []
    for v in cat_venues:
        org = ORGANIZERS.get(v.organizer_id, {"name": "Independent"})
        status = "Available"
        if v.organizer_id == "org_player":
            status = "Owned by you"
            if artist.popularity > pop_cap:
                status = f"Locked (Popularity too high: max {pop_cap})"
        elif artist.popularity < v.popularity_req:
            status = f"Locked (Popularity req: {v.popularity_req})"
        elif artist.popularity > pop_cap:
            status = f"Locked (Popularity too high: max {pop_cap})"
        elif org["strictness"] > artist.reputation and not org["negotiable"]:
            status = f"Locked (Reputation too low for strict organizer: {org['name']})"
        options.append(f"{v.name} ({v.city}, {v.country}) | Cap: {v.capacity:,} | Req: Pop {v.popularity_req} | {status}")

    options.append("Back")
    v_idx = choose_option(f"CHOOSE A {category.upper()}", options)
    if v_idx == len(cat_venues):
        return
    venue = cat_venues[v_idx]

    # Eligibility checks
    org = ORGANIZERS.get(venue.organizer_id, {"name": "Independent"})
    if artist.popularity < venue.popularity_req:
        print(f"\n[ERROR] Your popularity ({artist.popularity:.1f}) is too low for this venue (Required: {venue.popularity_req}).")
        input("Press Enter to go back...")
        return
    if artist.popularity > pop_cap:
        print(f"\n[ERROR] Your popularity ({artist.popularity:.1f}) is too high for this venue category (Max: {pop_cap}).")
        input("Press Enter to go back...")
        return
    if org["strictness"] > artist.reputation and not org["negotiable"]:
        print(f"\n[ERROR] Your reputation ({artist.reputation:.1f}) is too low for this organizer ({org['name']}, Strictness: {org['strictness']}).")
        input("Press Enter to go back...")
        return

    # Choose week
    current_week = ((artist.year - 1) * 52) + artist.week
    print(f"\nCurrent Week: {format_week_range(current_week)}")
    print(f"Venue availability: weeks {venue.weekly_availability}")
    try:
        weeks_ahead = int(input("  How many weeks ahead would you like to perform? (1-12): ").strip())
        if not (1 <= weeks_ahead <= 12):
            print("Invalid range. Must be between 1 and 12 weeks.")
            input("Press Enter to continue...")
            return
    except ValueError:
        print("Invalid input. Must be an integer.")
        input("Press Enter to continue...")
        return

    target_week = current_week + weeks_ahead
    target_week_of_year = ((target_week - 1) % 52) + 1
    if target_week_of_year not in venue.weekly_availability:
        print(f"\n[ERROR] Venue is not bookable on Year Week {target_week_of_year}.")
        input("Press Enter to go back...")
        return

    shows_on_week = sum(1 for b in artist.upcoming_concerts if b.week == target_week)
    if shows_on_week >= 3:
        print(f"\n[ERROR] You cannot book more than 3 shows in a single week. {format_week_range(target_week)} already has 3 shows booked.")
        input("Press Enter to go back...")
        return

    if venue.organizer_id == "org_player":
        ov = next((v for v in getattr(artist, "owned_venues", []) if v.id == venue.id), None)
        if ov:
            npc_bookings = sum(1 for b in ov.booking_requests if b.get("accepted") and b.get("week") == target_week)
            player_bookings_here = sum(1 for b in artist.upcoming_concerts if b.week == target_week and getattr(b, "venue_id", None) == ov.id)
            if npc_bookings + player_bookings_here >= 3:
                print(f"\n[ERROR] Venue '{ov.name}' cannot host more than 3 events in a single week. {format_week_range(target_week)} already has {npc_bookings + player_bookings_here} events scheduled.")
                input("Press Enter to go back...")
                return

    # Build or Load Setlist
    released_songs = [s for s in artist.singles if s.released]
    if not released_songs:
        print("\n[ERROR] You have no released songs to perform.")
        input("Press Enter to go back...")
        return

    setlist = []
    setlist_opt = choose_option("SETLIST CONFIGURATION", ["Select Songs Manually", "Use Saved Setlist Template"])
    if setlist_opt == 1:
        if not getattr(artist, "setlist_templates", None):
            print("\n[Warning] No setlist templates saved. Reverting to manual selection.")
            setlist_opt = 0
        else:
            templates = list(artist.setlist_templates.keys())
            t_choice = choose_option("CHOOSE TEMPLATE", templates + ["Cancel"])
            if t_choice == len(templates):
                return
            setlist = artist.setlist_templates[templates[t_choice]]
    
    if setlist_opt == 0 or not setlist:
        print("\n=== BUILD SETLIST ===")
        print("Available Songs:")
        for idx, s in enumerate(released_songs):
            print(f"[{idx+1}] {s.song.name} ({s.source_label}) | Streams: {s.total_streams:,}")
        print("\nEnter song numbers in order, separated by commas (e.g. 1,3,2,1):")
        try:
            inp = input(" >> ").strip()
            indices = [int(x.strip()) - 1 for x in inp.split(",") if x.strip()]
            if not indices or any(not (0 <= idx < len(released_songs)) for idx in indices):
                print("Invalid song selection.")
                input("Press Enter to continue...")
                return
            setlist = [released_songs[idx].release_id for idx in indices]
        except Exception:
            print("Error reading setlist selection.")
            input("Press Enter to continue...")
            return

    # Set ticket prices
    t_prices = dict(artist.price_templates[category])
    print(f"\nDefault Ticket Prices (Floor: ${t_prices['floor']}, Gen: ${t_prices['general']}, VIP: ${t_prices['vip']})")
    custom = input("  Would you like to customize ticket prices for this show? [y/N]: ").strip().lower()
    if custom == 'y':
        try:
            floor = int(input("  Enter Floor ticket price ($): ").strip())
            gen = int(input("  Enter General Admission ticket price ($): ").strip())
            vip = int(input("  Enter VIP ticket price ($): ").strip())
            t_prices = {"floor": floor, "general": gen, "vip": vip}
        except ValueError:
            print("Invalid prices. Reverting to default templates.")

    # Ticket sales promo boost investment
    print("\n=== INVEST IN SHOW PROMOTION / ADVERTISING ===")
    print("You can invest extra money in marketing to boost ticket sales.")
    promo_opts = [
        "None ($0, 1.0x ticket sales boost)",
        "Local Ads ($2,000, 1.10x ticket sales boost)",
        "Massive Campaign ($10,000, 1.25x ticket sales boost)",
        "Global Hype ($50,000, 1.50x ticket sales boost)"
    ]
    promo_choice = choose_option("CHOOSE PROMOTION TIER", promo_opts)
    promo_cost = 0.0
    promo_boost = 1.0
    if promo_choice == 1:
        promo_cost = 2000.0
        promo_boost = 1.10
    elif promo_choice == 2:
        promo_cost = 10000.0
        promo_boost = 1.25
    elif promo_choice == 3:
        promo_cost = 50000.0
        promo_boost = 1.50

    # Add guest artists
    guest_artists = []
    print("\n=== ADD GUEST ARTISTS ===")
    print("Guest artists can boost attendance but cost money (unless they have high relationship score).")
    while True:
        add_guest = input("  Add a guest artist? [y/N]: ").strip().lower()
        if add_guest != 'y':
            break
        print("\nAvailable Guest Artists:")
        valid_guests = [seed for seed in ARTIST_ECOSYSTEM_SEEDS if seed.popularity <= pop_cap]
        for idx, seed in enumerate(valid_guests):
            rel_score = 10.0
            if seed.name in artist.relationships:
                rel_score = artist.relationships[seed.name].score
            fee = int(seed.feature_cost * 0.4) if seed.feature_cost else int(seed.popularity * 1000)
            print(f"[{idx+1}] {seed.name} | Pop: {seed.popularity} | Rel: {rel_score:.1f} | Fee: ${fee:,}")
        try:
            g_inp = int(input("  Choose guest (or 0 to cancel): ").strip())
            if g_inp == 0:
                break
            if 1 <= g_inp <= len(valid_guests):
                g_seed = valid_guests[g_inp - 1]
                rel_score = 10.0
                if g_seed.name in artist.relationships:
                    rel_score = artist.relationships[g_seed.name].score
                paid = True
                fee = int(g_seed.feature_cost * 0.4) if g_seed.feature_cost else int(g_seed.popularity * 1000)
                if rel_score >= 70:
                    print(f"  {g_seed.name} agrees to perform for free because of your close relationship!")
                    paid = False
                    fee = 0
                else:
                    print(f"  {g_seed.name} requires a fee of ${fee:,}.")
                    confirm = input(f"  Confirm paying ${fee:,}? [y/N]: ").strip().lower()
                    if confirm != 'y':
                        continue
                guest_artists.append({"artist": g_seed.name, "paid": paid, "fee": fee, "performed": False})
                print(f"Added {g_seed.name} to guest list.")
        except ValueError:
            print("Invalid input.")

    # Choose opening act
    # Tradeoff decision: Player can hire any ecosystem artist.
    # Underground opener (pop < 40) charges $500 and gives a reputation bonus (+4).
    # Famous opener (pop >= 70) charges $2,000 * pop (e.g. $150,000), gives no reputation bonus, but boosts fill percentage by +25%.
    # Mid opener (40 <= pop < 70) charges $1,000 * pop (e.g. $50,000), gives no reputation bonus, and boosts fill percentage by +10%.
    opening_act = None
    opening_act_is_underground = False
    opening_fee = 0.0
    famous_opener_boost = 0.0
    print("\n=== CHOOSE OPENING ACT ===")
    choose_opener = input("  Add an opening act? [y/N]: ").strip().lower()
    if choose_opener == 'y':
        print("\nAvailable Opening Acts:")
        valid_openers = [op for op in ARTIST_ECOSYSTEM_SEEDS if op.popularity <= pop_cap]
        for idx, op in enumerate(valid_openers):
            if op.popularity < 40:
                fee = 500
                desc = "Underground (Gives +4 Rep bonus)"
            elif op.popularity >= 70:
                fee = int(op.popularity * 2000)
                desc = f"Famous (Gives +25% Ticket Sales boost, Fee: ${fee:,})"
            else:
                fee = int(op.popularity * 1000)
                desc = f"Mid-tier (Gives +10% Ticket Sales boost, Fee: ${fee:,})"
            print(f"[{idx+1}] {op.name} | Pop: {op.popularity} | {desc}")
        try:
            op_inp = int(input("  Choose opener (or 0 to cancel): ").strip())
            if 1 <= op_inp <= len(valid_openers):
                selected_op = valid_openers[op_inp - 1]
                opening_act = selected_op.name
                if selected_op.popularity < 40:
                    opening_act_is_underground = True
                    opening_fee = 500.0
                elif selected_op.popularity >= 70:
                    opening_fee = float(selected_op.popularity * 2000)
                    famous_opener_boost = 0.25
                else:
                    opening_fee = float(selected_op.popularity * 1000)
                    famous_opener_boost = 0.10
                print(f"Added {opening_act} as opening act. Fee: ${opening_fee:,.2f}")
        except ValueError:
            print("Invalid input.")

    # Calculate venue hire cost and default organizer cut
    if venue.organizer_id == "org_player":
        hire_costs = 0.0
        organizer_cut = 0.0
        print("\n[INFO] You are booking your OWN venue. Upfront hire costs and organizer cuts are WAIVED!")
    else:
        hire_costs, base_cut_pct = get_venue_costs(venue)
        organizer_cut = base_cut_pct
        print(f"\nOrganizer {org['name']} strictness: {org['strictness']}.")

        # Negotiation counter-offer
        if org["strictness"] > artist.reputation and org["negotiable"]:
            print(f"  {org['name']} is hesitant about your draw and reputation. They demand a higher cut.")
            negotiated_cut = base_cut_pct + 0.05
            print(f"  Default cut: {base_cut_pct*100:.1f}%. Negotiated cut: {negotiated_cut*100:.1f}%.")
            accept = input("  Accept the organizer counter-offer? [y/N]: ").strip().lower()
            if accept != 'y':
                print("Negotiation failed. Booking cancelled.")
                input("Press Enter to continue...")
                return
            organizer_cut = negotiated_cut
            print(random.choice(ORGANIZER_NEGOTIATION_RESPONSES["counter_offer"]).format(counter_pct=int(organizer_cut*100)))
        else:
            print(random.choice(ORGANIZER_NEGOTIATION_RESPONSES["accept_full"]))

    # Pre-calculate concert duration in hours
    total_song_secs = 0
    for sid in setlist:
        s = find_song(sid, released_songs)
        total_song_secs += getattr(s, "duration", 180) or 180
    
    # 20 minutes (1200 seconds) added for opening acts
    duration_hours = (total_song_secs + (1200 if opening_act else 0)) / 3600.0

    # Pre-calculate target attendance
    attendance_target, fill_pct = calculate_concert_attendance(artist, venue, t_prices, guest_artists, target_week, duration_hours)
    # Apply promotion boost
    fill_pct *= promo_boost
    # Apply famous/mid opener boost
    fill_pct += famous_opener_boost
    fill_pct = min(1.0, max(0.05, fill_pct))
    attendance_target = int(venue.capacity * fill_pct)

    # Confirm booking
    booking_id = f"cb_{venue.id}_{target_week}_{random.randint(100,999)}"
    temp_booking = ConcertBooking(
        id=booking_id,
        venue_id=venue.id,
        week=target_week,
        setlist=setlist,
        ticket_prices=t_prices,
        guest_artists=guest_artists,
        opening_act=opening_act,
        opening_act_is_underground=opening_act_is_underground,
        attendance=0,
        capacity_fill_pct=0.0,
        gross_revenue=0.0,
        net_revenue=0.0,
        organizer_cut=organizer_cut,
        live_popularity_delta=0.0,
        rep_delta=0.0,
        controversy_events=[],
        performance_score=5.0,
        booking_cost=hire_costs,
        guest_artist_cost=sum(g["fee"] for g in guest_artists),
        opening_act_fee=opening_fee,
        accidental_cost=0.0,
        profit_margin=0.0,
        attendance_target=attendance_target,
        promotion_boost=promo_boost,
        duration_hours=duration_hours
    )
    temp_booking.capacity_fill_pct = fill_pct

    total_upfront = hire_costs + promo_cost
    duration_modifier_pct = int(math.exp(-0.5 * (duration_hours - 2.0) ** 2) * 100)
    print(f"\nConcert Duration: {duration_hours:.2f} hours (Optimal: 2.0 hours -> Ticket sales modifier: {duration_modifier_pct}%)")
    print(f"Total Upfront Cost: ${total_upfront:,.2f} (Hire: ${hire_costs:,.2f} + Promo: ${promo_cost:,.2f})")
    
    confirm_book = input(f"Confirm booking {venue.name} for {format_week_range(target_week)}? [y/N]: ").strip().lower()
    if confirm_book == 'y':
        if artist.money < total_upfront:
            print("[ERROR] Insufficient funds to book this venue with selected promotion.")
            input("Press Enter to continue...")
            return
        artist.money -= total_upfront
        artist.upcoming_concerts.append(temp_booking)
        print(f"\nBooking confirmed! Upfront cost of ${total_upfront:,.2f} has been paid.")
        input("Press Enter to continue...")
    else:
        print("Booking cancelled.")
        input("Press Enter to continue...")


# ──────────────────────────────────────────────────────────────────────
#  CONCERT GAMEPLAY LOOP WITH INDUCED/SPONTANEOUS CONTROVERSIES
# ──────────────────────────────────────────────────────────────────────

def print_concert_header(booking, venue, artist):
    print("\n" + "=" * 60)
    print(f" * LIVE CONCERT: {artist.name.upper()} AT {venue.name.upper()} *")
    print(f" City: {venue.city}, {venue.country} | Category: {venue.category.upper()}")
    print(f" Capacity: {venue.capacity:,} | Attendance: {booking.attendance:,} ({booking.capacity_fill_pct*100:.1f}%)")
    print(f" Show Duration: {booking.duration_hours:.1f} hours")
    print("=" * 60)


def print_song_performing(song, index, total, energy):
    print(f"\n[{index}/{total}] Performing: '{song.name}'")
    bar_len = 20
    filled = int(energy * bar_len)
    bar = "#" * filled + "-" * (bar_len - filled)
    print(f" Crowd Energy: [{bar}] {energy*100:.0f}%")


def print_concert_summary(booking, venue, artist):
    print("\n" + "=" * 60)
    print(" * CONCERT SUMMARY *")
    print("=" * 60)
    print(f" Performance Score: {booking.performance_score}/10")
    print(f" Tickets Sold: {booking.attendance:,} / {venue.capacity:,}")
    print(f" Gross Revenue: ${booking.gross_revenue:,.2f}")
    print(f" Organizer Cut: ${booking.gross_revenue * booking.organizer_cut:,.2f} ({booking.organizer_cut*100:.1f}%)")
    print(f" Guest Artist Fees: ${booking.guest_artist_cost:,.2f}")
    print(f" Opening Act Payment: ${booking.opening_act_fee:,.2f}")
    print(f" Venue Hire Cost: ${booking.booking_cost:,.2f}")
    print(f" Accidental Costs (Fines/Refunds): ${booking.accidental_cost:,.2f}")
    print(f" Net Revenue to Artist: ${booking.net_revenue:,.2f}")
    print(f" Profit Margin: {booking.profit_margin:.1f}%")
    print(f" Popularity Change: {booking.live_popularity_delta:+.2f}")
    print(f" Reputation Change: {booking.rep_delta:+.2f}")
    print("=" * 60 + "\n")
    
    # Print occurred controversies
    if getattr(booking, "controversy_events", None):
        print("=" * 60)
        print(" * CONTROVERSIES OCCURRED *")
        print("=" * 60)
        for idx, ev in enumerate(booking.controversy_events, 1):
            desc = ev.get("outcome", ev.get("text", ev.get("desc", "Spontaneous controversy")))
            print(f"  [{idx}] {desc}")
        print("=" * 60 + "\n")


def trigger_mid_concert_controversy(artist, venue, booking, world=None):
    # Select from general mid controversies
    mid_scenarios = [c for c in CONCERT_CONTROVERSIES if c["trigger"] == "mid"]
    event = random.choice(mid_scenarios)
    print(f"\n!! SPONTANEOUS CONTROVERSY: {event['scenario']}")
    opts_texts = [opt["text"] for opt in event["options"]]
    opt_idx = choose_option("WHAT DO YOU DO?", opts_texts)
    chosen_opt = event["options"][opt_idx]

    booking.rep_delta += chosen_opt["rep_delta"]
    booking.live_popularity_delta += chosen_opt["pop_delta"]
    booking.accidental_cost += chosen_opt.get("accidental_cost", 0.0)

    print(f"\nOutcome: {chosen_opt['outcome']}")
    input("Press Enter to continue...")
    return chosen_opt


def maybe_trigger_post_concert_controversy(artist, venue, booking, world=None):
    cat_weights = {
        "club": 0.20,
        "auditorium": 0.30,
        "theatre": 0.40,
        "ground": 0.50,
        "arena": 0.60,
        "stadium": 0.70
    }
    base_prob = cat_weights.get(venue.category, 0.10)
    artist_cont = getattr(artist, "controversy", 35.0)
    trigger_prob = base_prob * (0.5 + artist_cont / 100.0)

    if random.random() < trigger_prob:
        post_scenarios = [c for c in CONCERT_CONTROVERSIES if c["trigger"] == "post"]
        event = random.choice(post_scenarios)
        print(f"\n!! POST-CONCERT SCENARIO: {event['scenario']}")
        opts_texts = [opt["text"] for opt in event["options"]]
        opt_idx = choose_option("WHAT DO YOU DO?", opts_texts)
        chosen_opt = event["options"][opt_idx]

        booking.rep_delta += chosen_opt["rep_delta"]
        booking.live_popularity_delta += chosen_opt["pop_delta"]
        booking.accidental_cost += chosen_opt.get("accidental_cost", 0.0)

        # Log to NewsModule & TwitterModule
        if world is not None:
            # Import modules locally to avoid circular imports
            from rapsim_reviews.career_mode import NewsReport, Tweet
            
            # 1. News Report
            report = NewsReport(
                id=f"nr_concert_{random.randint(100,999)}",
                week=booking.week,
                report_type="controversy",
                headline=f"Post-Concert incident: {event['scenario']} (Artist options resolved).",
                artist=artist.name,
                medium="news"
            )
            if world.news_module is not None:
                world.news_module.add_events(booking.week, [report])

            # 2. Twitter reaction
            tweet = Tweet(
                id=f"tw_concert_{random.randint(1000,9999)}",
                week=booking.week,
                author="industry_reporter",
                username="@industryleak",
                author_type="critic",
                tweet_type="reaction",
                content=f"Hearing reports of post-concert drama at {venue.name} involving @{artist.name.replace(' ', '')}! Outcome: {chosen_opt['outcome']}",
                reply_to_id=None,
                likes=random.randint(200, 1500),
                retweets=random.randint(50, 400)
            )
            existing = world.twitter_module.get_tweets(booking.week)
            world.twitter_module.add_tweets(booking.week, existing + [tweet])

        print(f"\nOutcome: {chosen_opt['outcome']}")
        input("Press Enter to continue...")
        return chosen_opt
    return None


def trigger_active_stage_rant(artist, venue, booking, world=None):
    # Allows player to manually target and criticize someone from the stage!
    print("\n=== CHOOSE TARGET FOR STAGE RANT ===")
    print("[1] Criticize an Ecosystem Artist")
    print("[2] Criticize a Music Critic")
    print("[3] Criticize an External Target (Gov / Record Labels / Press)")
    try:
        t_choice = int(input("  Select category: ").strip())
    except ValueError:
        print("Invalid choice. Rant cancelled.")
        return None

    target_name = ""
    attack_text = ""
    rep_c = 0.0
    pop_c = 0.0
    rel_c = 0.0
    acc_c = 0.0

    if t_choice == 1:
        # Ecosystem Artist
        print("\nChoose Artist to Criticize:")
        for idx, seed in enumerate(ARTIST_ECOSYSTEM_SEEDS):
            print(f"[{idx+1}] {seed.name} (Pop: {seed.popularity})")
        try:
            target_idx = int(input("  Select artist: ").strip()) - 1
            if 0 <= target_idx < len(ARTIST_ECOSYSTEM_SEEDS):
                target_name = ARTIST_ECOSYSTEM_SEEDS[target_idx].name
        except ValueError:
            pass
        if not target_name:
            print("Invalid target.")
            return None

        # Choose attack type
        print(f"\nSelect attack on {target_name}:")
        print("[1] 'They are an industry plant with no real fans!'")
        print("[2] 'They lack real talent and steal everyone's waves!'")
        print("[3] 'They don't write their own lyrics, they hire a team!'")
        try:
            atk = int(input("  Select attack: ").strip())
            if atk == 1:
                attack_text = f"called {target_name} an industry plant with no organic fanbase"
                rep_c = -5
                pop_c = +8
                rel_c = -20
            elif atk == 2:
                attack_text = f"screamed that {target_name} has zero talent and steals waves"
                rep_c = -8
                pop_c = +10
                rel_c = -25
            elif atk == 3:
                attack_text = f"exposed {target_name} for allegedly using ghostwriters for their whole catalog"
                rep_c = -12
                pop_c = +14
                rel_c = -35
                acc_c = 5000.0 # legal threat costs
        except ValueError:
            pass

    elif t_choice == 2:
        # Music Critic
        from rapsim_reviews.career_mode import CRITIC_NAMES
        print("\nChoose Critic to Criticize:")
        for idx, name in enumerate(CRITIC_NAMES):
            print(f"[{idx+1}] {name}")
        try:
            target_idx = int(input("  Select critic: ").strip()) - 1
            if 0 <= target_idx < len(CRITIC_NAMES):
                target_name = CRITIC_NAMES[target_idx]
        except ValueError:
            pass
        if not target_name:
            print("Invalid target.")
            return None

        # Choose attack type
        print(f"\nSelect attack on critic {target_name}:")
        print("[1] 'They are biased, fake, and accept bribes for reviews!'")
        print("[2] 'They don't understand the culture or real music!'")
        try:
            atk = int(input("  Select attack: ").strip())
            if atk == 1:
                attack_text = f"accused critic {target_name} of bias and accepting bribes for reviews"
                rep_c = -8
                pop_c = +7
                rel_c = -25
            elif atk == 2:
                attack_text = f"lashed out at critic {target_name}, saying they fail to understand the culture"
                rep_c = -4
                pop_c = +5
                rel_c = -15
        except ValueError:
            pass

    elif t_choice == 3:
        # External Target
        from rapsim_reviews.career_mode import EXTERNAL_TARGETS
        print("\nChoose External Target:")
        for idx, name in enumerate(EXTERNAL_TARGETS[:10]): # display first 10 for simplicity
            print(f"[{idx+1}] {name.capitalize()}")
        try:
            target_idx = int(input("  Select target: ").strip()) - 1
            if 0 <= target_idx < 10:
                target_name = EXTERNAL_TARGETS[target_idx]
        except ValueError:
            pass
        if not target_name:
            print("Invalid target.")
            return None

        # Choose attack type
        print(f"\nSelect statement on {target_name}:")
        print(f"[1] 'F*** {target_name}! They are corrupt and control everything!'")
        print(f"[2] '{target_name.capitalize()} is lying to you! Open your eyes!'")
        try:
            atk = int(input("  Select statement: ").strip())
            if atk == 1:
                attack_text = f"ranted on stage shouting 'F*** {target_name}!'"
                rep_c = +4
                pop_c = +10
            elif atk == 2:
                attack_text = f"claimed {target_name} is lying to the public and warned fans to open their eyes"
                rep_c = -5
                pop_c = +12
        except ValueError:
            pass

    if not attack_text:
        print("Invalid selection. Rant cancelled.")
        return None

    # Apply consequences to booking
    booking.rep_delta += rep_c
    booking.live_popularity_delta += pop_c
    booking.accidental_cost += acc_c

    # Apply consequences to artist metrics
    artist.controversy = max(0.0, min(100.0, artist.controversy + 8.0))
    if target_name and rel_c != 0.0:
        # Modify relationship score
        from rapsim_reviews.career_mode import _apply_relationship_delta
        _apply_relationship_delta(artist, target_name, rel_c)

    print(f"\n!! STAGE RANT OUTCOME: You {attack_text}!")
    print(f"  Relationship change: {rel_c:+.1f} | Popularity change: {pop_c:+.1f} | Reputation change: {rep_c:+.1f}")
    if acc_c > 0:
        print(f"  Accidental costs incurred: ${acc_c:,.2f}")

    # Inject into News and Twitter
    if world is not None:
        from rapsim_reviews.career_mode import NewsReport, Tweet
        
        # News
        report = NewsReport(
            id=f"nr_rant_{random.randint(100,999)}",
            week=booking.week,
            report_type="controversy",
            headline=f"Stage Rant: {artist.name} {attack_text} live at {venue.name}!",
            artist=artist.name,
            target=target_name,
            medium="concert statement"
        )
        if world.news_module is not None:
            world.news_module.add_events(booking.week, [report])

        # Tweets
        tweets = [
            Tweet(
                id=f"tw_rant_{random.randint(1000,9999)}",
                week=booking.week,
                author=f"user_{random.randint(100,999)}",
                username=f"@hiphopfan_{random.randint(10,99)}",
                author_type="fan",
                tweet_type="reaction",
                content=f"No way @{artist.name.replace(' ', '')} really just said that about {target_name} live on stage!! I am losing it",
                reply_to_id=None,
                likes=random.randint(400, 2000),
                retweets=random.randint(100, 600)
            )
        ]
        existing = world.twitter_module.get_tweets(booking.week)
        world.twitter_module.add_tweets(booking.week, existing + tweets)

    input("Press Enter to continue...")
    return {"headline": f"Stage Rant targeting {target_name}"}


def trigger_induced_guest_controversy(artist, venue, booking, world=None):
    if not booking.guest_artists:
        return None
    
    # Choose a guest from list
    guest = random.choice(booking.guest_artists)
    guest_name = guest["artist"]

    print(f"\n!! GUEST INCIDENT: Guest artist {guest_name} is running extremely late and was supposed to perform next!")
    print("  What do you do?")
    print("  [1] Stall by doing an impromptu freestyle set (costs 18.0 fatigue, energy +0.08, performance +1.2, rep +8)")
    print("  [2] Call them out publicly on the mic (rep -15, target relationship -45, pop +15, controversy +15)")
    print("  [3] Cut their slot entirely and adjust setlist (guest fee refunded, guest removed, energy -0.15, performance -1.2, pop -8)")

    choice = input("  >> ").strip()

    if choice == "1":
        artist.fatigue = max(0.0, min(140.0, artist.fatigue + 18.0))
        booking.live_popularity_delta += 0.08
        booking.rep_delta += 8.0
        print(f"\nOutcome: You stall with freestyles. The crowd appreciates the hustle! (Fatigue +18.0, Rep +8)")
        input("Press Enter to continue...")
        return {"type": "guest_stall", "bonus_perf": 1.2}

    elif choice == "2":
        booking.rep_delta -= 15.0
        booking.live_popularity_delta += 15.0
        artist.controversy = min(100.0, artist.controversy + 15.0)
        from rapsim_reviews.career_mode import _apply_relationship_delta
        _apply_relationship_delta(artist, guest_name, -45.0)
        print(f"\nOutcome: You call out {guest_name} on the mic! The crowd goes wild, but their camp is furious. (Rep -15, Pop +15, Controversy +15)")
        input("Press Enter to continue...")
        return {"type": "guest_callout"}

    else:
        booking.net_revenue += guest["fee"]
        booking.guest_artist_cost -= guest["fee"]
        booking.guest_artists.remove(guest)
        booking.live_popularity_delta -= 8.0
        print(f"\nOutcome: You cut {guest_name}'s slot. Their fee of ${guest['fee']:,} has been refunded. (Pop -8, Setlist Quality Hit)")
        input("Press Enter to continue...")
        return {"type": "guest_cut", "bonus_perf": -1.2}


def trigger_induced_opener_controversy(artist, venue, booking, world=None):
    if not booking.opening_act:
        return None
    
    opener_name = booking.opening_act
    
    # 50/50 on scenario
    if random.random() < 0.5:
        print(f"\n!! OPENER INCIDENT: Underground opener {opener_name} forgot their lines and froze on stage! The crowd is starting to murmur.")
        print("  What do you do?")
        print("  [1] Walk out, hand them a mic, and help them finish (costs 12.0 fatigue, rep +20, energy +0.10, opener relationship +25)")
        print("  [2] Let security nudge them off and start your set early (rep -15, energy -0.20, pop -6, opener relationship -30)")
        print("  [3] Stand in the wings and yell encouragement (rep +5, energy -0.05, opener relationship +10)")

        choice = input("  >> ").strip()

        if choice == "1":
            artist.fatigue = max(0.0, min(140.0, artist.fatigue + 12.0))
            booking.rep_delta += 20.0
            booking.live_popularity_delta += 0.10
            from rapsim_reviews.career_mode import _apply_relationship_delta
            _apply_relationship_delta(artist, opener_name, 25.0)
            print(f"\nOutcome: You run on stage and save the performance! Widely praised. (Fatigue +12.0, Rep +20, Opener Relationship +25)")
            input("Press Enter to continue...")
            return {"type": "opener_save", "bonus_perf": 0.5}
        elif choice == "2":
            booking.rep_delta -= 15.0
            booking.live_popularity_delta -= 6.0
            from rapsim_reviews.career_mode import _apply_relationship_delta
            _apply_relationship_delta(artist, opener_name, -30.0)
            print(f"\nOutcome: Opener is sent off. Crowd feels awkward and the opener is extremely bitter. (Rep -15, Pop -6, Opener Relationship -30)")
            input("Press Enter to continue...")
            return {"type": "opener_nudge", "bonus_perf": -0.8}
        else:
            booking.rep_delta += 5.0
            from rapsim_reviews.career_mode import _apply_relationship_delta
            _apply_relationship_delta(artist, opener_name, 10.0)
            print(f"\nOutcome: You cheer them from side-stage. They manage to finish. (Rep +5, Opener Relationship +10)")
            input("Press Enter to continue...")
            return {"type": "opener_cheer"}
    else:
        print(f"\n!! OPENER INCIDENT: The crowd is aggressively heckling the opening act {opener_name}!")
        print("  What do you do?")
        print("  [1] Grab a mic backstage and defend them (rep +18, energy -0.05, opener relationship +20)")
        print("  [2] Let them deal with it (energy -0.10, opener relationship -10)")
        print("  [3] Join in on the jokes from side stage (rep -25, pop +15, opener relationship -40, controversy +8)")

        choice = input("  >> ").strip()

        if choice == "1":
            booking.rep_delta += 18.0
            from rapsim_reviews.career_mode import _apply_relationship_delta
            _apply_relationship_delta(artist, opener_name, 20.0)
            print(f"\nOutcome: You defend {opener_name} from the mic. Crowd respects the leadership, though vibe cools down. (Rep +18, Opener Relationship +20)")
            input("Press Enter to continue...")
            return {"type": "opener_defend"}
        elif choice == "2":
            from rapsim_reviews.career_mode import _apply_relationship_delta
            _apply_relationship_delta(artist, opener_name, -10.0)
            print(f"\nOutcome: You stay out of it. The hostile vibe lingers. (Opener Relationship -10)")
            input("Press Enter to continue...")
            return {"type": "opener_ignore", "bonus_perf": -0.4}
        else:
            booking.rep_delta -= 25.0
            booking.live_popularity_delta += 15.0
            artist.controversy = min(100.0, artist.controversy + 8.0)
            from rapsim_reviews.career_mode import _apply_relationship_delta
            _apply_relationship_delta(artist, opener_name, -40.0)
            print(f"\nOutcome: You laugh and joke at the opener's expense! Viral moment, but destroys your reputation. (Rep -25, Pop +15, Opener Relationship -40, Controversy +8)")
            input("Press Enter to continue...")
            return {"type": "opener_mock", "bonus_perf": 0.3}


def run_concert(booking, venue, artist, all_songs, world=None):
    # Calculate final showtime attendance with duration modifiers and opener boosts
    attendance, fill_pct = calculate_concert_attendance(
        artist, venue, booking.ticket_prices, booking.guest_artists, booking.week, booking.duration_hours
    )
    # Apply promotion boost
    fill_pct *= booking.promotion_boost

    contract = getattr(artist, "label_contract", None)
    if contract and getattr(contract, "status", "") in ("active", "shelved", "recouped"):
        from rapsim_reviews.label_system import get_label_by_id
        lbl = get_label_by_id(contract.label_id)
        if lbl:
            gig_boost = lbl.gig_promotion_boost if getattr(contract, "is_priority_artist", True) else (1.0 + (lbl.gig_promotion_boost - 1.0) * 0.15)
            fill_pct *= gig_boost
            booking.label_promotion_boost = gig_boost
    
    # Apply opener attendance boost (famous/mid opener boost calculated at booking)
    # If the opener is famous (popularity >= 70) we boost fill percent by +0.25
    # If mid-tier (40 <= popularity < 70) we boost fill percent by +0.10
    opener_boost = 0.0
    if booking.opening_act:
        opener_artist = find_artist(booking.opening_act)
        if opener_artist:
            if opener_artist.popularity >= 70:
                opener_boost = 0.25
            elif opener_artist.popularity >= 40:
                opener_boost = 0.10
    fill_pct += opener_boost
    fill_pct = min(1.0, max(0.05, fill_pct))

    booking.attendance = int(venue.capacity * fill_pct)
    booking.capacity_fill_pct = fill_pct

    print_concert_header(booking, venue, artist)
    input("Press Enter to start the show...")

    crowd_energy = 0.5  # starts neutral
    performance_scores = []

    # Tracker flags to avoid spamming multiple controversies in one show
    mid_controversy_triggered = False
    guest_controversy_triggered = False
    opener_controversy_triggered = False
    bonus_perf_score = 0.0
    speech_count = 0

    # Trigger opener controversy at the start of the concert (Increased probability to 0.50, boosted by low safety)
    safety_rating = getattr(venue, "safety_rating", 80.0)
    safety_mult = 2.0 - safety_rating / 100.0
    if booking.opening_act and random.random() < 0.50 * safety_mult:
        event = trigger_induced_opener_controversy(artist, venue, booking, world)
        if event:
            opener_controversy_triggered = True
            booking.controversy_events.append(event)

    for i, song_id in enumerate(booking.setlist):
        song = find_song(song_id, all_songs)
        if not song:
            print(f"\n[Warning] Song ID {song_id} could not be found.")
            continue

        print_song_performing(song, i + 1, len(booking.setlist), crowd_energy)

        # song score calculation
        song_pop_score = min(getattr(song, "total_streams", 0) / 5_000_000, 10.0)
        song_score = (song.quality * 0.5 + song_pop_score * 0.3 + crowd_energy * 10.0 * 0.2)
        song_score += venue.ambiance_bonus
        song_score = min(10.0, max(1.0, song_score + random.uniform(-0.5, 0.5)))
        performance_scores.append(song_score)

        # crowd energy shifts (Tuned: harder to make it go to 100%)
        if song_score >= 8.0:
            crowd_energy = min(1.0, crowd_energy + 0.06)
        elif song_score >= 6.0:
            crowd_energy = min(1.0, crowd_energy + 0.02)
        elif song_score <= 4.0:
            # Low score drops energy faster
            crowd_energy = max(0.0, crowd_energy - 0.15)

        # Probabilistic random mid controversies occur on their own during song transitions (Increased probability to 0.35, boosted by low safety)
        if not mid_controversy_triggered and random.random() < 0.35 * safety_mult:
            event = trigger_mid_concert_controversy(artist, venue, booking, world)
            if event:
                mid_controversy_triggered = True
                booking.controversy_events.append(event)

        # Probabilistic guest controversy triggers mid-show (Increased probability to 0.45, boosted by low safety)
        if not guest_controversy_triggered and booking.guest_artists and random.random() < 0.45 * safety_mult:
            event = trigger_induced_guest_controversy(artist, venue, booking, world)
            if event:
                guest_controversy_triggered = True
                booking.controversy_events.append(event)
                if event.get("bonus_perf"):
                    bonus_perf_score += event["bonus_perf"]

        # Mid-concert choices
        print("\n  What do you do?")
        print("  [1]  Continue to next song")
        print("  [2]  Address the crowd (boost energy +0.05, costs 5.0 fatigue)")
        print("  [3]  Launch stage rant (criticize artist/critic/gov publicly!)")
        print("  [4]  End the concert early")
        print("  [5]  Bring out a guest artist")

        choice = input("  >> ").strip()

        if choice == "2":
            # Speech costs fatigue and can only be used once per show
            if speech_count >= 1:
                print("  The crowd is already familiar with your speech. No effect.")
            else:
                artist.fatigue = max(0.0, min(140.0, artist.fatigue + 5.0))
                crowd_energy = min(1.0, crowd_energy + 0.05)
                speech_count += 1
                print("  You address the crowd. Energy rising slightly. (Fatigue +5.0)")
            input("Press Enter to continue...")

        elif choice == "3":
            # Active stage rant choice targeting a specific artist or critic
            event_outcome = trigger_active_stage_rant(artist, venue, booking, world)
            if event_outcome:
                booking.controversy_events.append(event_outcome)

        elif choice == "4":
            print("\n  Concert ended early by your choice.")
            booking.live_popularity_delta -= 5.0
            booking.rep_delta -= 3.0
            input("Press Enter to go to backstage resolution...")
            break

        elif choice == "5":
            available_guests = [g for g in booking.guest_artists if not g.get("performed", False)]
            if available_guests:
                guest = available_guests[0]
                guest["performed"] = True
                # Tuned crowd energy boost
                crowd_energy = min(1.0, crowd_energy + 0.10)
                print(f"\n  {guest['artist']} joins the stage. The crowd erupts!")
            else:
                print("  No guest artists available (or they've already performed).")
            input("Press Enter to continue...")

    # Post-concert calculations
    base_perf = sum(performance_scores) / len(performance_scores) if performance_scores else 5.0
    booking.performance_score = round(min(10.0, base_perf + bonus_perf_score), 1)

    # Base popularity and reputation deltas
    pop_delta = calculate_live_pop_delta(booking.performance_score, booking.capacity_fill_pct, booking)
    booking.live_popularity_delta += pop_delta

    # Reputation change linked to prestige and performance score
    rep_change = (booking.performance_score - 5.0) * (venue.prestige / 50.0)
    booking.rep_delta += round(rep_change, 1)

    # Add reputation bonus ONLY for support of underground openers
    if booking.opening_act and booking.opening_act_is_underground:
        opener_artist = find_artist(booking.opening_act)
        if opener_artist:
            rep_bonus = opening_act_rep_bonus(opener_artist)
            booking.rep_delta += rep_bonus
            if rep_bonus > 0:
                print(f"\n[BONUS] Supporting underground talent ({booking.opening_act}) gained you +{rep_bonus} reputation!")

    # Check for post-concert controversy
    post_event = maybe_trigger_post_concert_controversy(artist, venue, booking, world)
    if post_event:
        booking.controversy_events.append(post_event)

    # Cap popularity and reputation gains at +4.0 maximum per concert
    booking.live_popularity_delta = min(4.0, booking.live_popularity_delta)
    booking.rep_delta = min(4.0, booking.rep_delta)

    # Calculate revenues
    gross, net, org_cut_val = calculate_concert_revenue(booking, venue, None)
    net -= booking.accidental_cost

    # Label concert & merch cut
    contract = getattr(artist, "label_contract", None)
    if contract and getattr(contract, "status", "") in ("active", "shelved", "recouped"):
        label_cut_pct = float(getattr(contract, "concert_merch_cut", 0.0))
        if label_cut_pct > 0.0:
            label_cut_val = gross * label_cut_pct
            net -= label_cut_val
            booking.label_cut = label_cut_val
            from rapsim_reviews.ui_helpers import money_fmt
            print(f"  [LABEL CUT] Label took {label_cut_pct*100:.1f}% concert cut: -{money_fmt(label_cut_val)}")

    booking.gross_revenue = gross
    booking.net_revenue = net
    booking.profit_margin = round((net / gross * 100) if gross > 0 else 0.0, 1)

    # Inject successful concert headline into news and twitter reactions
    if world is not None:
        from rapsim_reviews.career_mode import NewsReport, Tweet
        head_line = f"{artist.name}'s show at {venue.name} sells out {booking.attendance:,} tickets with a {booking.performance_score}/10 performance!"
        if booking.performance_score < 4.0:
            head_line = f"Disaster at {venue.name} as {artist.name}'s performance falls flat with a {booking.performance_score}/10 rating."
        report = NewsReport(
            id=f"nr_show_{random.randint(100,999)}",
            week=booking.week,
            report_type="sales" if booking.performance_score >= 4.0 else "general",
            headline=head_line,
            artist=artist.name,
            medium="news"
        )
        if world.news_module is not None:
            world.news_module.add_events(booking.week, [report])

        # Generate custom tweets based on concert score
        clean_name = artist.name.replace(" ", "")
        tweets = []
        if booking.performance_score >= 7.5:
            tweets.append(Tweet(
                id=f"tw_show_good_{random.randint(1000,9999)}",
                week=booking.week,
                author=f"fan_{random.randint(100,999)}",
                username=f"@fan_{random.randint(100,999)}",
                author_type="fan",
                tweet_type="reaction",
                content=f"Just got back from @{clean_name}'s show at {venue.name}. Absolutely legendary performance! 10/10",
                reply_to_id=None,
                likes=random.randint(500, 2500),
                retweets=random.randint(100, 800)
            ))
            tweets.append(Tweet(
                id=f"tw_show_good_{random.randint(1000,9999)}",
                week=booking.week,
                author=f"music_critic_{random.randint(10,99)}",
                username=f"@critic_{random.randint(10,99)}",
                author_type="critic",
                tweet_type="reaction",
                content=f"@{clean_name} showed pure stage presence tonight at {venue.name}. One of the best live sets this year.",
                reply_to_id=None,
                likes=random.randint(200, 1000),
                retweets=random.randint(40, 300)
            ))
        elif booking.performance_score >= 4.0:
            tweets.append(Tweet(
                id=f"tw_show_mid_{random.randint(1000,9999)}",
                week=booking.week,
                author=f"fan_{random.randint(100,999)}",
                username=f"@fan_{random.randint(100,999)}",
                author_type="fan",
                tweet_type="reaction",
                content=f"Solid performance from @{clean_name} tonight at {venue.name}. Crowd energy was good.",
                reply_to_id=None,
                likes=random.randint(50, 400),
                retweets=random.randint(5, 50)
            ))
        else:
            tweets.append(Tweet(
                id=f"tw_show_bad_{random.randint(1000,9999)}",
                week=booking.week,
                author=f"disappointed_fan",
                username=f"@disappointed_{random.randint(10,99)}",
                author_type="fan",
                tweet_type="reaction",
                content=f"@{clean_name}'s concert at {venue.name} was a total trainwreck lol, flat energy and bad setlist.",
                reply_to_id=None,
                likes=random.randint(100, 800),
                retweets=random.randint(20, 200)
            ))
        if world.twitter_module is not None:
            existing = world.twitter_module.get_tweets(booking.week)
            world.twitter_module.add_tweets(booking.week, existing + tweets)

    print_concert_summary(booking, venue, artist)
    input("Press Enter to resolve the week...")
    return booking


# Post-process all controversies to scale impacts and add opposing tradeoffs (reputation vs popularity)
for _cont in CONCERT_CONTROVERSIES:
    for _opt in _cont["options"]:
        _rep = _opt.get("rep_delta", 0)
        _pop = _opt.get("pop_delta", 0)
        _acc = _opt.get("accidental_cost", 0.0)

        # Scale metrics to make choices high-stakes
        if _rep > 0:
            _opt["rep_delta"] = int(_rep * 2.0)
        elif _rep < 0:
            _opt["rep_delta"] = int(_rep * 2.5)

        if _pop > 0:
            _opt["pop_delta"] = int(_pop * 2.0)
        elif _pop < 0:
            _opt["pop_delta"] = int(_pop * 2.5)

        if _acc > 0:
            _opt["accidental_cost"] = float(_acc * 5.0)

        # Add opposing tradeoffs: large popularity gains tank reputation and vice-versa
        if _opt["pop_delta"] >= 15:
            _opt["rep_delta"] = min(_opt.get("rep_delta", 0), -5) - int(_opt["pop_delta"] * 0.4)
        if _opt["rep_delta"] >= 15:
            _opt["pop_delta"] = min(_opt.get("pop_delta", 0), -5) - int(_opt["rep_delta"] * 0.4)
