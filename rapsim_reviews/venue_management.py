"""Venue Ownership and Management System for Rapsim."""

import random
from dataclasses import dataclass, field
from typing import Any
import builtins
from rapsim_reviews.date_system import format_week_range

def cli_pause(prompt="Press Enter to continue..."):
    import inspect
    for frame in inspect.stack():
        if frame.function in ('simulate_many_weeks', 'run_tests', 'test_advanced_venues', 'test_tuned_venues'):
            return
    if builtins.input.__module__ == 'builtins':
        builtins.input(prompt)

# ──────────────────────────────────────────────────────────────────────
#  AMENITIES DEFINITIONS (30 Amenities)
# ──────────────────────────────────────────────────────────────────────

AMENITIES = {
    # small category (club, theatre, auditorium)
    "sound_system": {"name": "Premium Sound System", "cost": 15000.0, "rating_bonus": 0.3, "safety_bonus": 0, "buzz_bonus": 5, "upkeep": 100.0, "categories": ["club", "theatre", "auditorium"]},
    "stage_lighting": {"name": "LED Stage Lighting", "cost": 10000.0, "rating_bonus": 0.2, "safety_bonus": 0, "buzz_bonus": 4, "upkeep": 80.0, "categories": ["club", "theatre", "auditorium"]},
    "vip_lounge": {"name": "VIP Lounge Area", "cost": 25000.0, "rating_bonus": 0.4, "safety_bonus": 0, "buzz_bonus": 8, "upkeep": 250.0, "categories": ["club", "theatre", "auditorium", "ground", "arena", "stadium"]},
    "cocktail_bar": {"name": "Artisanal Cocktail Bar", "cost": 12000.0, "rating_bonus": 0.2, "safety_bonus": -5, "buzz_bonus": 3, "upkeep": 150.0, "categories": ["club", "theatre", "auditorium"]},
    "green_room": {"name": "Upgraded Green Room", "cost": 8000.0, "rating_bonus": 0.1, "safety_bonus": 0, "buzz_bonus": 2, "upkeep": 50.0, "categories": ["club", "theatre", "auditorium"]},
    "wood_paneling": {"name": "Acoustical Wood Paneling", "cost": 18000.0, "rating_bonus": 0.3, "safety_bonus": 2, "buzz_bonus": 2, "upkeep": 60.0, "categories": ["club", "theatre", "auditorium"]},
    "security_gates": {"name": "Smart Security Gates", "cost": 9000.0, "rating_bonus": 0.1, "safety_bonus": 10, "buzz_bonus": 0, "upkeep": 120.0, "categories": ["club", "theatre", "auditorium", "ground", "arena", "stadium"]},
    "valet_service": {"name": "Valet Parking Service", "cost": 20000.0, "rating_bonus": 0.3, "safety_bonus": 0, "buzz_bonus": 6, "upkeep": 300.0, "categories": ["club", "theatre", "auditorium"]},
    "backstage_shower": {"name": "Backstage Shower Facilities", "cost": 5000.0, "rating_bonus": 0.1, "safety_bonus": 0, "buzz_bonus": 1, "upkeep": 30.0, "categories": ["club", "theatre", "auditorium"]},
    "ac_overhaul": {"name": "Air Conditioning Overhaul", "cost": 22000.0, "rating_bonus": 0.4, "safety_bonus": 1, "buzz_bonus": 2, "upkeep": 180.0, "categories": ["club", "theatre", "auditorium", "ground", "arena", "stadium"]},
    
    # large category (ground, arena, stadium)
    "hd_jumbotron": {"name": "High-Definition Jumbotron", "cost": 150000.0, "rating_bonus": 0.5, "safety_bonus": 0, "buzz_bonus": 15, "upkeep": 800.0, "categories": ["ground", "arena", "stadium"]},
    "stadium_wifi": {"name": "Stadium-wide Wi-Fi", "cost": 80000.0, "rating_bonus": 0.3, "safety_bonus": 0, "buzz_bonus": 8, "upkeep": 400.0, "categories": ["ground", "arena", "stadium"]},
    "private_suites": {"name": "Luxury Private Suites", "cost": 250000.0, "rating_bonus": 0.6, "safety_bonus": 0, "buzz_bonus": 20, "upkeep": 1200.0, "categories": ["ground", "arena", "stadium"]},
    "retractable_roof": {"name": "Retractable Roof System", "cost": 600000.0, "rating_bonus": 0.8, "safety_bonus": 15, "buzz_bonus": 30, "upkeep": 3000.0, "categories": ["ground", "arena", "stadium"]},
    "crowd_barriers": {"name": "Enhanced Crowd Control Barriers", "cost": 30000.0, "rating_bonus": 0.0, "safety_bonus": 15, "buzz_bonus": 0, "upkeep": 150.0, "categories": ["ground", "arena", "stadium"]},
    "fiber_cabling": {"name": "Fiber-Optic Broadcast Cabling", "cost": 5000.0, "rating_bonus": 0.2, "safety_bonus": 0, "buzz_bonus": 6, "upkeep": 200.0, "categories": ["ground", "arena", "stadium"]},
    "solar_grid": {"name": "Solar Panel Roof Grid", "cost": 120000.0, "rating_bonus": 0.3, "safety_bonus": 5, "buzz_bonus": 5, "upkeep": -500.0, "categories": ["ground", "arena", "stadium"]},
    "helipad_access": {"name": "Helipad Access", "cost": 200000.0, "rating_bonus": 0.4, "safety_bonus": 5, "buzz_bonus": 12, "upkeep": 600.0, "categories": ["ground", "arena", "stadium"]},
    "high_turnstiles": {"name": "High-throughput Turnstiles", "cost": 45000.0, "rating_bonus": 0.0, "safety_bonus": 10, "buzz_bonus": 0, "upkeep": 180.0, "categories": ["ground", "arena", "stadium"]},
    "food_court": {"name": "Mega Food Court Plaza", "cost": 100000.0, "rating_bonus": 0.4, "safety_bonus": 0, "buzz_bonus": 10, "upkeep": 500.0, "categories": ["ground", "arena", "stadium"]},
    "turf_stage_base": {"name": "Premium Turf/Stage Base", "cost": 85000.0, "rating_bonus": 0.3, "safety_bonus": 8, "buzz_bonus": 8, "upkeep": 300.0, "categories": ["ground", "arena", "stadium"]},
    "fire_suppression": {"name": "Advanced Fire Suppression", "cost": 40000.0, "rating_bonus": 0.0, "safety_bonus": 25, "buzz_bonus": 0, "upkeep": 200.0, "categories": ["club", "theatre", "auditorium", "ground", "arena", "stadium"]},
    "artist_tunnel": {"name": "Underground Artist Tunnel", "cost": 130000.0, "rating_bonus": 0.3, "safety_bonus": 5, "buzz_bonus": 8, "upkeep": 400.0, "categories": ["ground", "arena", "stadium"]},
    "seat_cushioning": {"name": "Premium Seat Cushioning", "cost": 70000.0, "rating_bonus": 0.3, "safety_bonus": 0, "buzz_bonus": 5, "upkeep": 250.0, "categories": ["ground", "arena", "stadium"]},
    "pyro_rigging": {"name": "Pyrotechnic Rigging", "cost": 95000.0, "rating_bonus": 0.2, "safety_bonus": -10, "buzz_bonus": 15, "upkeep": 500.0, "categories": ["ground", "arena", "stadium"]},
    "parking_garage": {"name": "Multi-level Parking Garage", "cost": 350000.0, "rating_bonus": 0.5, "safety_bonus": 5, "buzz_bonus": 10, "upkeep": 1000.0, "categories": ["ground", "arena", "stadium"]},
    "merch_hub": {"name": "Merch Store Mega-Hub", "cost": 60000.0, "rating_bonus": 0.3, "safety_bonus": 0, "buzz_bonus": 8, "upkeep": 300.0, "categories": ["club", "theatre", "auditorium", "ground", "arena", "stadium"]},
    "exterior_facade": {"name": "Giant LED Exterior Facade", "cost": 180000.0, "rating_bonus": 0.4, "safety_bonus": 0, "buzz_bonus": 18, "upkeep": 700.0, "categories": ["ground", "arena", "stadium"]},
    "cctv_security": {"name": "Advanced CCTV Security Grid", "cost": 55000.0, "rating_bonus": 0.0, "safety_bonus": 20, "buzz_bonus": 0, "upkeep": 280.0, "categories": ["club", "theatre", "auditorium", "ground", "arena", "stadium"]},
    "medical_station": {"name": "Medical Aid Station", "cost": 25000.0, "rating_bonus": 0.0, "safety_bonus": 15, "buzz_bonus": 0, "upkeep": 150.0, "categories": ["club", "theatre", "auditorium", "ground", "arena", "stadium"]},
}

# ──────────────────────────────────────────────────────────────────────
#  LOCATION TYPES & DEFINITIONS
# ──────────────────────────────────────────────────────────────────────

LOCATION_TYPES = {
    "suburban": {
        "name": "Suburban Outskirts",
        "price_mult": 0.5,
        "buzz_growth_mult": 0.5,
        "buzz_decay_mult": 0.67,
        "crime_chance_mult": 0.5,
        "controversy_chance_mult": 0.5,
        "min_stars": 1.0,
    },
    "downtown": {
        "name": "Downtown City Center",
        "price_mult": 1.5,
        "buzz_growth_mult": 1.25,
        "buzz_decay_mult": 0.75,
        "crime_chance_mult": 1.0,
        "controversy_chance_mult": 1.5,
        "min_stars": 1.0,
    },
    "sketchy": {
        "name": "Industrial / High-Crime Locality",
        "price_mult": 0.3,
        "buzz_growth_mult": 0.75,
        "buzz_decay_mult": 1.2,
        "crime_chance_mult": 2.5,
        "controversy_chance_mult": 1.2,
        "min_stars": 1.0,
    },
    "uptown": {
        "name": "Premium Uptown District",
        "price_mult": 2.0,
        "buzz_growth_mult": 1.25,
        "buzz_decay_mult": 0.5,
        "crime_chance_mult": 0.3,
        "controversy_chance_mult": 0.8,
        "min_stars": 2.0,
    }
}

# ──────────────────────────────────────────────────────────────────────
#  BASE AMENITY DEFINITIONS
# ──────────────────────────────────────────────────────────────────────

BASE_AMENITY_DETAILS = {
    "washrooms": {"name": "Restrooms", "cost": 15000.0},
    "parking": {"name": "Parking Lot", "cost": 25000.0},
    "ventilation": {"name": "HVAC Ventilation", "cost": 20000.0},
    "basic_signage": {"name": "Wayfinding Signage", "cost": 10000.0},
    "escalators": {"name": "Central Escalators", "cost": 40000.0}
}

def get_missing_base_amenities(venue) -> list[str]:
    required = ["washrooms", "parking", "ventilation", "basic_signage"]
    if venue.category in ["theatre", "auditorium", "arena", "stadium"]:
        required.append("escalators")
    return [a for a in required if a not in venue.base_amenities]

def get_base_amenity_cost(amenity_id: str, category: str) -> float:
    base_cost = BASE_AMENITY_DETAILS[amenity_id]["cost"]
    mult = {
        "club": 1.0,
        "theatre": 1.5,
        "auditorium": 2.5,
        "ground": 4.0,
        "arena": 8.0,
        "stadium": 20.0
    }.get(category, 1.0)
    return base_cost * mult

# ──────────────────────────────────────────────────────────────────────
#  DATACLASSES
# ──────────────────────────────────────────────────────────────────────

@dataclass
class LandPlot:
    id: str
    acres: float
    purchase_price: float
    lease_weekly_cost: float
    weekly_tax: float
    location_type: str = "suburban"

@dataclass
class OwnedVenue:
    id: str
    name: str
    category: str  # club | theatre | auditorium | ground | arena | stadium
    capacity: int
    type: str  # ground_up | renovated
    status: str  # construction | operational
    construction_weeks_left: int
    construction_material: str  # budget | standard | premium
    land_size_acres: float
    land_weekly_tax: float
    land_type: str  # leased | owned
    land_purchase_price: float
    location_type: str = "suburban"
    base_amenities: list[str] = field(default_factory=list)
    reviews: list[dict] = field(default_factory=list)
    past_shows_log: list[dict] = field(default_factory=list)
    amenities: list[str] = field(default_factory=list)
    buzz: float = 30.0
    review_stars: float = 3.0
    base_cut_pct: float = 0.20
    base_hire_cost: float = 1000.0
    safety_rating: float = 80.0
    rating_modifier: float = 0.0
    booking_requests: list[dict] = field(default_factory=list)
    past_events_history: list[dict] = field(default_factory=list)

# ──────────────────────────────────────────────────────────────────────
#  MATHEMATICAL MODELS
# ──────────────────────────────────────────────────────────────────────

def calculate_venue_upkeep(venue: OwnedVenue) -> float:
    base = {
        "club": 1500.0,
        "theatre": 5000.0,
        "auditorium": 15000.0,
        "ground": 60000.0,
        "arena": 250000.0,
        "stadium": 1000000.0
    }.get(venue.category, 1000.0)
    
    amenities_upkeep = sum(AMENITIES[a]["upkeep"] for a in venue.amenities if a in AMENITIES)
    return base + amenities_upkeep

def update_venue_ratings(venue: OwnedVenue):
    if venue.status != "operational":
        return
    
    base_safety = {"budget": 50.0, "standard": 80.0, "premium": 98.0}.get(venue.construction_material, 80.0)
    safety_amenity_bonus = sum(AMENITIES[a]["safety_bonus"] for a in venue.amenities if a in AMENITIES)
    venue.safety_rating = max(0.0, min(100.0, base_safety + safety_amenity_bonus))

    base_rating = {"budget": 2.5, "standard": 3.0, "premium": 3.5}.get(venue.construction_material, 3.0)
    if venue.type == "renovated":
        base_rating = 2.8
        
    amenity_rating_bonus = sum(AMENITIES[a]["rating_bonus"] for a in venue.amenities if a in AMENITIES)
    safety_factor = 0.2 if venue.safety_rating >= 80 else (-0.5 if venue.safety_rating < 50 else 0.0)
    
    # Missing base amenities penalty
    missing_amenities = get_missing_base_amenities(venue)
    amenities_penalty = -0.4 * len(missing_amenities)
    
    # Location base min stars
    loc_cfg = LOCATION_TYPES.get(venue.location_type, {})
    min_stars = loc_cfg.get("min_stars", 1.0)
    
    calculated_stars = base_rating + amenity_rating_bonus + safety_factor + amenities_penalty + getattr(venue, "rating_modifier", 0.0)
    
    # Diminishing returns above 4.0 stars to make it hard to exceed 4.5 rating
    if calculated_stars > 4.0:
        surplus = calculated_stars - 4.0
        calculated_stars = 4.0 + (surplus * 0.4)
        
    venue.review_stars = round(max(min_stars, min(5.0, calculated_stars)), 1)

# ──────────────────────────────────────────────────────────────────────
#  WEEKLY REVIEWS GENERATION
# ──────────────────────────────────────────────────────────────────────

def generate_weekly_reviews(venue: OwnedVenue, week_idx: int):
    if venue.status != "operational":
        return
    
    usernames = ["@show_seeker", "@concert_life", "@audiophile88", "@live_beat", "@bass_head", 
                 "@gig_chaser", "@music_review_fan", "@ticket_buyer", "@vip_pass", "@crowd_surfer"]
    
    missing = get_missing_base_amenities(venue)
    num_reviews = random.randint(2, 3)
    
    new_reviews = []
    for _ in range(num_reviews):
        rev_stars = venue.review_stars + random.uniform(-0.6, 0.6)
        rev_stars = round(max(1.0, min(5.0, rev_stars)), 1)
        
        comment = ""
        # 1. Complain about missing base amenities
        if missing and random.random() < 0.60:
            chosen_missing = random.choice(missing)
            complaints = {
                "washrooms": [
                    "Where are the washrooms? Had to use a portapotty in the rain. 1 star.",
                    "No bathrooms inside the venue? Disgusting and highly unprofessional.",
                    "Spent half the concert looking for a toilet. Completely lacking basic washrooms!"
                ],
                "parking": [
                    "Nowhere to park. Had to park 4 blocks away in a dark alley.",
                    "Spent an hour finding parking because the venue has no designated parking lot.",
                    "Terrible logistics. Zero parking facilities."
                ],
                "ventilation": [
                    "It was boiling inside, felt like there was no ventilation at all.",
                    "Sweating buckets. The HVAC ventilation here is non-existent.",
                    "Suffocating atmosphere. They need to fix the air flow."
                ],
                "basic_signage": [
                    "Got lost three times trying to find my seat. No signage anywhere.",
                    "Wayfinding is a joke. They need basic exit and gate signs.",
                    "Terrible layout and zero signs helping you find seats or bars."
                ],
                "escalators": [
                    "Climbing 5 flights of stairs to the upper tier was exhausting. No escalators?",
                    "My elderly father couldn't climb the stairs easily. They need escalators in a venue this big.",
                    "Stairs were a bottleneck. Escalators would have saved hours."
                ]
            }
            comment = random.choice(complaints[chosen_missing])
            rev_stars = min(2.5, rev_stars)
        
        # 2. Complain about safety
        elif venue.safety_rating < 60 and random.random() < 0.50:
            safety_complaints = [
                "Felt extremely unsafe. The crowd control was terrible.",
                "Felt like a major safety hazard. People were pushing and no barriers in sight.",
                "Security was a joke. I didn't feel secure at all.",
                "Felt like a stampede risk at the gates. Very scary."
            ]
            comment = random.choice(safety_complaints)
            rev_stars = min(2.0, rev_stars)
            
        # 3. Vibe-based comments
        else:
            if rev_stars >= 4.0:
                positive_pool = [
                    "Incredible venue! Acoustics were crystal clear.",
                    "Great experience. Highly recommend attending shows here.",
                    "Amazing sound, friendly staff, and premium vibes.",
                    "Best night out in a long time! The venue was top tier."
                ]
                comment = random.choice(positive_pool)
            elif rev_stars >= 3.0:
                neutral_pool = [
                    "A decent place to watch a show, but drinks are overpriced.",
                    "Average venue. Sound was okay but seats were slightly cramped.",
                    "Not bad, but nothing mind-blowing either. Had an okay time.",
                    "Good sound system, but exit lanes were super slow."
                ]
                comment = random.choice(neutral_pool)
            else:
                negative_pool = [
                    "Vibe was pretty dead and the layout is awkward.",
                    "Acoustics were muddy and muffled. Disappointed.",
                    "Poor management. Long queues for everything.",
                    "Needs a major upgrade. Facilities look run-down."
                ]
                comment = random.choice(negative_pool)
                
        new_reviews.append({
            "username": random.choice(usernames) + str(random.randint(10, 99)),
            "rating": rev_stars,
            "comment": comment,
            "week": week_idx
        })
        
    venue.reviews = (new_reviews + venue.reviews)[:15]

# ──────────────────────────────────────────────────────────────────────
#  HELPER TO DETECT SIMULATE MANY WEEKS
# ──────────────────────────────────────────────────────────────────────

def is_in_simulate_many_weeks() -> bool:
    import inspect
    for frame in inspect.stack():
        if frame.function == 'simulate_many_weeks':
            return True
    return False

# ──────────────────────────────────────────────────────────────────────
#  WEEKLY UPDATES & GENERATION
# ──────────────────────────────────────────────────────────────────────

def generate_weekly_land_plots(artist) -> list[LandPlot]:
    week_idx = ((artist.year - 1) * 52) + artist.week
    rng = random.Random(f"land_market:{week_idx}:{artist.name}")
    sizes = [1, 2, 5, 10, 20, 50]
    loc_types = ["suburban", "downtown", "sketchy", "uptown"]
    plots = []
    for i in range(3):
        acres = rng.choice(sizes)
        loc = rng.choice(loc_types)
        loc_cfg = LOCATION_TYPES[loc]
        
        price_per_acre = rng.randint(200000, 400000)
        purchase_price = int(acres * price_per_acre * loc_cfg["price_mult"])
        lease_weekly_cost = int(purchase_price * 0.005)
        weekly_tax = int(purchase_price * 0.001)
        plots.append(LandPlot(
            id=f"plot_{week_idx}_{i}",
            acres=acres,
            purchase_price=purchase_price,
            lease_weekly_cost=lease_weekly_cost,
            weekly_tax=weekly_tax,
            location_type=loc
        ))
    return plots

def generate_weekly_renovation_options(artist) -> list[dict]:
    week_idx = ((artist.year - 1) * 52) + artist.week
    rng = random.Random(f"reno_market:{week_idx}:{artist.name}")
    cats = ["club", "theatre", "auditorium", "ground", "arena", "stadium"]
    loc_types = ["suburban", "downtown", "sketchy", "uptown"]
    options = []
    for i in range(rng.randint(1, 2)):
        cat = rng.choice(cats)
        loc = rng.choice(loc_types)
        loc_cfg = LOCATION_TYPES[loc]
        
        acres_needed = {"club": 1, "theatre": 2, "auditorium": 5, "ground": 10, "arena": 20, "stadium": 50}[cat]
        capacity = {"club": 800, "theatre": 2000, "auditorium": 4000, "ground": 12000, "arena": 22000, "stadium": 65000}[cat]
        base_cost = {
            "club": 500000,
            "theatre": 1200000,
            "auditorium": 3000000,
            "ground": 8000000,
            "arena": 20000000,
            "stadium": 50000000
        }[cat]
        
        land_cost = acres_needed * 250000
        total_value = (land_cost + base_cost) * loc_cfg["price_mult"]
        purchase_price = int(total_value * rng.uniform(0.40, 0.65))
        weekly_tax = int(land_cost * 0.001 * loc_cfg["price_mult"])
        
        names = ["The Rusty Wheel", "Broken Pillar", "Vibe Graveyard", "Neon Dust", "The Echo Ruins", "Vintage Hall"]
        name = rng.choice(names) + f" ({cat.upper()})"
        
        options.append({
            "id": f"reno_{week_idx}_{i}",
            "name": name,
            "category": cat,
            "capacity": capacity,
            "purchase_price": purchase_price,
            "weekly_tax": weekly_tax,
            "acres": acres_needed,
            "location_type": loc
        })
    return options

NPC_CONTROVERSIES = [
    {"desc": "Artist threw a microphone into the crowd after a technical feedback loop.", "react_weights": [0.4, 0.4, 0.2]},
    {"desc": "Artist arrived 2 hours late, prompting fans to throw drinks at the stage.", "react_weights": [0.5, 0.3, 0.2]},
    {"desc": "Artist made a highly controversial political statement mid-set, sparking shouting matches.", "react_weights": [0.3, 0.5, 0.2]},
    {"desc": "Artist invited 30 fans on stage, causing a barrier collapse and security panic.", "react_weights": [0.6, 0.3, 0.1]},
    {"desc": "Artist cut their set short after 15 minutes, claiming the crowd energy was dead.", "react_weights": [0.2, 0.6, 0.2]},
]

def select_booking_artist(venue, rng, world, artist_name, tier):
    pop_cap = {
        "club": 60,
        "auditorium": 70,
        "theatre": 80
    }.get(venue.category, 999)

    base_pop_range = {
        "top": (80, 100),
        "mid": (55, 82),
        "low": (0, 54)
    }[tier]
    
    min_pop = base_pop_range[0]
    max_pop = min(base_pop_range[1], pop_cap)
    
    if min_pop > max_pop:
        min_pop = 0
        max_pop = pop_cap

    candidates = []
    if world and hasattr(world, "roster") and world.roster:
        for r_art in world.roster:
            name = r_art.seed.name
            if name == artist_name:
                continue
            pop = world.artist_popularity.get(name, r_art.seed.popularity)
            if min_pop <= pop <= max_pop:
                candidates.append((name, int(pop)))
                
    if candidates:
        return rng.choice(candidates)
        
    fallback_artists = {
        "top": [
            ("Travis Scott", rng.randint(85, 95)),
            ("Drake", rng.randint(88, 98)),
            ("Kendrick Lamar", rng.randint(86, 96)),
            ("The Weeknd", rng.randint(85, 95)),
            ("Kanye West", rng.randint(85, 95)),
            ("Playboi Carti", rng.randint(82, 88)),
            ("Tyler, The Creator", rng.randint(80, 87)),
            ("Lil Uzi Vert", rng.randint(80, 86))
        ],
        "mid": [
            ("Baby Keem", rng.randint(65, 75)),
            ("Freddie Gibbs", rng.randint(60, 72)),
            ("Pusha T", rng.randint(62, 74)),
            ("Lil Baby", rng.randint(70, 80)),
            ("21 Savage", rng.randint(72, 82)),
            ("JID", rng.randint(68, 78)),
            ("Denzel Curry", rng.randint(65, 75)),
            ("Joey Bada$$", rng.randint(60, 70)),
            ("Earl Sweatshirt", rng.randint(58, 68)),
            ("Danny Brown", rng.randint(58, 68))
        ],
        "low": [
            ("Local MC", rng.randint(20, 35)),
            ("Underground Pete", rng.randint(15, 30)),
            ("Slick Rhymer", rng.randint(25, 45)),
            ("Subway Busker", rng.randint(10, 25)),
            ("Basement Rapper", rng.randint(15, 30)),
            ("Soundcloud Hype", rng.randint(30, 50)),
            ("Lyrical Miracle", rng.randint(35, 52)),
            ("Beat Master", rng.randint(20, 40))
        ]
    }
    
    # Filter fallbacks from all tiers to respect [min_pop, max_pop]
    all_fallbacks = []
    for t, artists in fallback_artists.items():
        for art in artists:
            all_fallbacks.append(art)
            
    valid_fallbacks = [art for art in all_fallbacks if min_pop <= art[1] <= max_pop]
    if not valid_fallbacks:
        valid_fallbacks = [art for art in all_fallbacks if art[1] <= pop_cap]
    if valid_fallbacks:
        return rng.choice(valid_fallbacks)
        
    return ("Local MC", rng.randint(10, min(50, pop_cap)))

def generate_npc_booking_requests(venue: OwnedVenue, week_idx: int, artist_name: str, world=None) -> list[dict]:
    rng = random.Random(f"npc_booking:{venue.id}:{week_idx}:{artist_name}")
    requests = []
    
    num_reqs = 0
    if venue.review_stars >= 4.0 and venue.buzz >= 80:
        num_reqs = rng.randint(2, 3)
    elif venue.review_stars >= 2.5 and venue.buzz >= 30:
        num_reqs = rng.randint(1, 2)
    elif rng.random() < 0.40:
        num_reqs = 1
        
    for i in range(num_reqs):
        if venue.review_stars >= 4.5 and venue.buzz >= 90:
            tier = "top"
        elif venue.review_stars >= 3.0 and venue.buzz >= 50:
            tier = "mid"
        else:
            tier = "low"
            
        npc_name, npc_popularity = select_booking_artist(venue, rng, world, artist_name, tier)
        
        # Calculate cut offer depending on tier
        if tier == "top":
            cut_offer = rng.uniform(0.25, 0.35)
        elif tier == "mid":
            cut_offer = rng.uniform(0.15, 0.25)
        else:
            cut_offer = rng.uniform(0.08, 0.15)
            
        # Capacity and category based hiring cost calculations
        base_ranges = {
            "club": (10000, 30000),
            "theatre": (20000, 40000),
            "auditorium": (40000, 80000),
            "ground": (40000, 80000),
            "arena": (70000, 150000),
            "stadium": (150000, 300000)
        }
        min_base, max_base = base_ranges.get(venue.category, (10000, 30000))
        base_offer = rng.randint(min_base, max_base)
        
        default_caps = {
            "club": 800,
            "theatre": 2000,
            "auditorium": 4000,
            "ground": 12000,
            "arena": 22000,
            "stadium": 65000
        }
        def_cap = default_caps.get(venue.category, 800)
        cap_ratio = venue.capacity / def_cap
        rent_offer = base_offer * cap_ratio
        
        multiplier = 1.0
        if venue.buzz > 80 and venue.review_stars > 4.0:
            increase_pct = 0.05 * ((venue.buzz - 80.0) / 5.0) + 0.05 * ((venue.review_stars - 4.0) / 0.1)
            increase_pct = min(0.20, max(0.0, increase_pct))
            multiplier += increase_pct
        elif venue.buzz < 30 and venue.review_stars < 2.0:
            decrease_pct = 0.15 * ((30.0 - venue.buzz) / 30.0) + 0.15 * ((2.0 - venue.review_stars) / 1.0)
            decrease_pct = min(0.30, max(0.0, decrease_pct))
            multiplier -= decrease_pct
            
        rent_offer = int(rent_offer * multiplier)
            
        requests.append({
            "id": f"req_{week_idx}_{i}",
            "artist_name": npc_name,
            "artist_popularity": npc_popularity,
            "rent_fee": rent_offer,
            "cut_pct": round(cut_offer, 2),
            "week": week_idx + rng.randint(1, 4)
        })
    return requests

def step_owned_venues(artist, world=None):
    if not hasattr(artist, "owned_venues"):
        artist.owned_venues = []
        
    week_idx = ((artist.year - 1) * 52) + artist.week
    
    for venue in artist.owned_venues:
        loc_cfg = LOCATION_TYPES.get(venue.location_type, {})
        
        # 1. LAND TAXES (Applies always)
        artist.money = float(artist.money - venue.land_weekly_tax)
        venue.past_events_history.append({
            "week": week_idx,
            "type": "tax",
            "details": "Land Taxes",
            "net": -venue.land_weekly_tax
        })
        
        # 2. LEASE COST (If leased)
        if venue.land_type == "leased":
            lease_fee = int((venue.land_purchase_price or 100000) * 0.005)
            artist.money = float(artist.money - lease_fee)
            venue.past_events_history.append({
                "week": week_idx,
                "type": "lease",
                "details": "Land Lease Payment",
                "net": -lease_fee
            })

        # 3. CONSTRUCTION HANDLING
        if venue.status == "construction":
            delay = False
            if venue.construction_material == "budget" and random.random() < 0.25:
                delay = True
                print(f"\n[CONSTRUCTION WARNING] Budget material issues at {venue.name}! Construction delayed this week.")
                venue.safety_rating = max(0.0, venue.safety_rating - 2.0)
            elif venue.construction_material == "standard" and random.random() < 0.05:
                delay = True
                print(f"\n[CONSTRUCTION INFO] Small delay at {venue.name} due to weather.")
                
            if not delay:
                venue.construction_weeks_left -= 1
                
            if venue.construction_weeks_left <= 0:
                venue.status = "operational"
                venue.buzz = {"budget": 35.0, "standard": 50.0, "premium": 65.0}.get(venue.construction_material, 50.0)
                update_venue_ratings(venue)
                print(f"\n[CONSTRUCTION COMPLETED] Your venue '{venue.name}' ({venue.category.upper()}) is now OPERATIONAL!")
                cli_pause()

        # 4. OPERATIONAL HANDLING (Upkeeps, safety events, and NPC Bookings resolution)
        elif venue.status == "operational":
            # Upkeep costs deduction
            upkeep = calculate_venue_upkeep(venue)
            artist.money = float(artist.money - upkeep)
            venue.past_events_history.append({
                "week": week_idx,
                "type": "upkeep",
                "details": "Weekly Upkeep & Upgrades",
                "net": -upkeep
            })
            
            # Resolve NPC bookings scheduled for this week
            active_npc_shows = [b for b in venue.booking_requests if b.get("accepted") and b.get("week") == week_idx]
            npc_shows_held = len(active_npc_shows) > 0
            
            # Check if player performed here this week
            player_show_held = any(
                c.week == week_idx and getattr(c, "venue_id", None) == venue.id 
                for c in getattr(artist, "concert_history", [])
            )
            event_held = npc_shows_held or player_show_held
            
            # Weekly ratings fluctuation & drift
            if not hasattr(venue, "rating_modifier"):
                venue.rating_modifier = 0.0
            fluctuation = random.uniform(-0.3, 0.3)
            venue.rating_modifier = max(-2.0, min(2.0, venue.rating_modifier + fluctuation))

            # Buzz & Ratings Decay if no event held (exponential decay)
            if not event_held:
                decay_pct = 0.12 * loc_cfg.get("buzz_decay_mult", 1.0)
                decay_amt = venue.buzz * decay_pct
                if venue.buzz > 0:
                    decay_amt = max(1.5, decay_amt)
                
                old_buzz = venue.buzz
                venue.buzz = max(0.0, venue.buzz - decay_amt)
                actual_decay = old_buzz - venue.buzz
                
                # Rating modifier decay (falling exponentially)
                rating_decay = venue.review_stars * 0.06 * loc_cfg.get("buzz_decay_mult", 1.0)
                venue.rating_modifier = max(-3.0, getattr(venue, "rating_modifier", 0.0) - rating_decay)
                
                venue.past_events_history.append({
                    "week": week_idx,
                    "type": "decay",
                    "details": f"No events held. Buzz decayed by -{actual_decay:.1f}, Rating Modifier decayed by -{rating_decay:.2f}",
                    "net": 0.0
                })
            
            # Safety hazards checks based on buzz vs safety
            safety_hazard_triggered = False
            fine_cost = 0.0
            if venue.buzz > 90 and venue.safety_rating < 85:
                if random.random() < 0.20:
                    safety_hazard_triggered = True
                    fine_cost = float(random.randint(30000, 60000))
            elif venue.buzz > 70 and venue.safety_rating < 70:
                if random.random() < 0.10:
                    safety_hazard_triggered = True
                    fine_cost = float(random.randint(15000, 35000))
                    
            if safety_hazard_triggered:
                artist.money = float(artist.money - fine_cost)
                venue.safety_rating = max(0.0, venue.safety_rating - random.randint(8, 15))
                print(f"\n[SAFETY HAZARD ALERT] Overcrowding and crowd control failure at {venue.name}!")
                print(f"  Fined ${fine_cost:,.2f} for safety violations. Safety rating dropped.")
                venue.past_events_history.append({
                    "week": week_idx,
                    "type": "safety_hazard",
                    "details": "Fined for overcrowding/stampede incident",
                    "net": -fine_cost
                })
                cli_pause()
                
            # Random Weekly Incidents / Damage (2% base, 5% in Sketchy)
            incident_chance = 0.02 * loc_cfg.get("crime_chance_mult", 1.0)
            if random.random() < incident_chance and not is_in_simulate_many_weeks():
                incident_type = random.choice(["fight", "graffiti", "safety_audit", "extortion", "gov_raid"])
                
                if incident_type == "extortion":
                    print(f"\n[EXTORTION WARNING] A local criminal crew is demanding $20,000 protection money for {venue.name}.")
                    from rapsim_reviews.career_mode import choose_from_list
                    choices = [
                        "Pay the protection money ($20,000)",
                        "Refuse and beef up security (Risk vandalism)"
                    ]
                    act = choose_from_list("Process Threat:", choices, allow_cancel=False)
                    if act == 0:
                        artist.money = float(artist.money - 20000)
                        print("[EXTORTION] You paid the crew. They leave you alone for now.")
                        venue.past_events_history.append({
                            "week": week_idx,
                            "type": "extortion",
                            "details": "Paid protection racket money",
                            "net": -20000.0
                        })
                    else:
                        repair = 30000.0
                        artist.money = float(artist.money - repair)
                        venue.safety_rating = max(0.0, venue.safety_rating - 30.0)
                        print(f"[EXTORTION RECALL] You refused! The gang vandalized the facility and broke windows.")
                        print(f"  Repair cost: ${repair:,.2f} | Safety Rating decreased by -30.")
                        venue.past_events_history.append({
                            "week": week_idx,
                            "type": "extortion_vandalism",
                            "details": "Refused protection. Facility vandalized.",
                            "net": -repair
                        })
                        cli_pause()
                        
                elif incident_type == "fight":
                    repair = 15000.0
                    artist.money = float(artist.money - repair)
                    venue.safety_rating = max(0.0, venue.safety_rating - 10.0)
                    print(f"\n[INCIDENT] A major brawl broke out at {venue.name}!")
                    print(f"  Repair cost: ${repair:,.2f} | Safety Rating decreased by -10.")
                    venue.past_events_history.append({
                        "week": week_idx,
                        "type": "fight",
                        "details": "Brawl damage repairs",
                        "net": -repair
                    })
                    cli_pause()
                    
                elif incident_type == "graffiti":
                    cleanup = 5000.0
                    artist.money = float(artist.money - cleanup)
                    venue.buzz = max(0.0, venue.buzz - 10.0)
                    print(f"\n[VANDALISM] Vandals sprayed offensive graffiti all over the exterior of {venue.name}!")
                    print(f"  Cleanup cost: ${cleanup:,.2f} | Buzz decreased by -10.")
                    venue.past_events_history.append({
                        "week": week_idx,
                        "type": "graffiti",
                        "details": "Graffiti cleanup",
                        "net": -cleanup
                    })
                    cli_pause()
                    
                elif incident_type == "safety_audit":
                    print(f"\n[SAFETY INSPECTION] A surprise city safety inspector audited {venue.name}.")
                    if venue.safety_rating < 60:
                        audit_fine = 50000.0
                        artist.money = float(artist.money - audit_fine)
                        print(f"  [FAILED] Safety rating is too low ({venue.safety_rating:.1f}/100). Fined $50,000.00.")
                        venue.past_events_history.append({
                            "week": week_idx,
                            "type": "audit_fine",
                            "details": "Failed safety audit fine",
                            "net": -audit_fine
                        })
                    else:
                        print(f"  [PASSED] Seating, fire exits, and safety features are clean ({venue.safety_rating:.1f}/100).")
                    cli_pause()

                elif incident_type == "gov_raid":
                    fine = float(random.randint(40000, 80000))
                    artist.money = float(artist.money - fine)
                    venue.buzz = max(0.0, venue.buzz - 20.0)
                    venue.safety_rating = max(0.0, venue.safety_rating - 15.0)
                    print(f"\n[GOVERNMENT RAID] A surprise government raid occurred at {venue.name} due to suspected violations!")
                    print(f"  Fined ${fine:,.2f} | Venue Buzz decreased by -20 | Safety Rating decreased by -15.")
                    venue.past_events_history.append({
                        "week": week_idx,
                        "type": "gov_raid",
                        "details": "Government raid fines and penalties",
                        "net": -fine
                    })
                    cli_pause()

            # Resolve active NPC shows
            for show in active_npc_shows:
                initial_buzz_cap = venue.buzz
                pop_weight = show["artist_popularity"] / 100.0
                buzz_weight = venue.buzz / 100.0
                fill_pct = min(1.0, max(0.10, pop_weight * 0.8 + buzz_weight * 0.2))
                attendance = int(venue.capacity * fill_pct)
                
                avg_ticket = {"club": 15, "theatre": 40, "auditorium": 60, "ground": 80, "arena": 120, "stadium": 200}.get(venue.category, 30)
                gross_ticket_revenue = attendance * avg_ticket
                
                npc_share_cut = gross_ticket_revenue * show["cut_pct"]
                rental_payout = show["rent_fee"] + npc_share_cut
                
                # Check for hosted show controversies (boosted by low safety)
                safety_mult = 2.0 - venue.safety_rating / 100.0
                controversy_prob = 0.45 * loc_cfg.get("controversy_chance_mult", 1.0) * safety_mult
                is_controversial = random.random() < controversy_prob
                cont_desc = "None"
                incident_desc = ""
                
                if is_controversial:
                    cont = random.choice(NPC_CONTROVERSIES)
                    cont_desc = cont["desc"]
                    react = random.choices(["apologize", "double_down", "ignore"], weights=cont["react_weights"])[0]
                    
                    if react == "apologize":
                        react_desc = "The artist apologized immediately and coordinated solutions with the venue."
                        review_change = random.uniform(0.1, 0.3)
                        buzz_change = 5.0
                        safety_change = 0.0
                        fine = 0.0
                    elif react == "double_down":
                        fine = 10000.0
                        react_desc = f"The artist blamed the venue, demanding payouts and fining you ${fine:,.2f} for negligence."
                        review_change = -random.uniform(0.8, 1.5)
                        buzz_change = -10.0
                        safety_change = -5.0
                        rental_payout = max(0.0, rental_payout - fine)
                        artist.money = float(artist.money - fine)
                        incident_desc = f" (Controversy: Artist double-down fine: ${fine:,.2f})"
                        venue.past_events_history.append({
                            "week": week_idx,
                            "type": "incident",
                            "details": f"Negligence fine at show: {cont_desc}",
                            "net": -fine
                        })
                    else:
                        react_desc = "The artist ignored the issue. Buzz and ratings took a significant hit."
                        review_change = -random.uniform(0.4, 0.8)
                        buzz_change = -5.0
                        safety_change = 0.0
                        fine = 0.0
                        
                    venue.rating_modifier = getattr(venue, "rating_modifier", 0.0) + review_change
                    venue.buzz = max(0.0, min(100.0, venue.buzz + buzz_change))
                    venue.safety_rating = max(0.0, min(100.0, venue.safety_rating + safety_change))
                    
                    print(f"\n[NPC CONCERT CONTROVERSY] at {venue.name} during {show['artist_name']}'s show:")
                    print(f"  Incident: {cont_desc}")
                    print(f"  Outcome : {react_desc}")
                    cli_pause()

                # Credit player wallet
                artist.money = float(artist.money + rental_payout)
                
                # Update venue buzz & stats (capped at 10)
                buzz_boost = int(show["artist_popularity"] * 0.10)
                buzz_boost = min(10, buzz_boost)
                venue.buzz = min(100.0, venue.buzz + buzz_boost)
                
                # Ensure total buzz added by this show (including controversies) is capped at 10
                total_buzz_added = venue.buzz - initial_buzz_cap
                if total_buzz_added > 10:
                    venue.buzz = min(100.0, initial_buzz_cap + 10)
                
                # Log to shows log
                log_entry = {
                    "week": week_idx,
                    "artist_name": show["artist_name"],
                    "attendance": attendance,
                    "gross_revenue": gross_ticket_revenue,
                    "rent_fee": show["rent_fee"],
                    "cut_pct": show["cut_pct"],
                    "revenue_to_venue": rental_payout,
                    "controversy": cont_desc
                }
                venue.past_shows_log.append(log_entry)
                
                # Log success event in ledger
                venue.past_events_history.append({
                    "week": week_idx,
                    "type": "npc_booking_payout",
                    "details": f"Hosted {show['artist_name']}'s event ({attendance:,} attendees){incident_desc}",
                    "net": rental_payout
                })
                
                # Remove resolved show
                venue.booking_requests.remove(show)
                
                print(f"\n[EVENT COMPLETED] {venue.name} hosted {show['artist_name']}!")
                print(f"  Attendance: {attendance:,} | Rental + Ticket Cut: ${rental_payout:,.2f}")
                cli_pause()

            # Clean expired/non-accepted booking requests and generate new ones
            venue.booking_requests = [b for b in venue.booking_requests if b.get("accepted") and b.get("week") > week_idx]
            new_requests = generate_npc_booking_requests(venue, week_idx, artist.name, world)
            venue.booking_requests.extend(new_requests)
            
            # Recalculate stars and ratings weekly
            update_venue_ratings(venue)
            
            # Generate weekly reviews
            generate_weekly_reviews(venue, week_idx)

# ──────────────────────────────────────────────────────────────────────
#  CLI MENUS & INTERACTIVE FLOWS
# ──────────────────────────────────────────────────────────────────────

def venue_management_menu(artist, world=None):
    from rapsim_reviews.career_mode import choose_from_list
    if not hasattr(artist, "owned_venues"):
        artist.owned_venues = []
        
    while True:
        options = [
            "Acquire a Venue (Build Ground-Up / Renovate)",
            "Manage Operational Venues",
            "Review Booking Requests",
            "View Properties Under Construction",
            "Go Back"
        ]
        
        choice = choose_from_list("\n=== VENUE OWNERSHIP & MANAGEMENT ===", options, allow_cancel=False)
        if choice == 0:
            acquire_venue_flow(artist)
        elif choice == 1:
            manage_venues_flow(artist)
        elif choice == 2:
            review_bookings_flow(artist)
        elif choice == 3:
            view_construction_flow(artist)
        else:
            break

def acquire_venue_flow(artist):
    from rapsim_reviews.career_mode import choose_from_list, prompt_text, prompt_int
    
    print("\nHow would you like to acquire your venue?")
    choices = [
        "Build from the ground up (Lease/buy land, construct it, high rating potential)",
        "Renovate an existing dying venue (Cheaper, skip construction, starts with low buzz)",
        "Cancel"
    ]
    opt = choose_from_list("Acquisition Choice:", choices, allow_cancel=False)
    
    if opt == 0:
        # Build from ground up
        plots = generate_weekly_land_plots(artist)
        print("\nAvailable Land Plots this week:")
        plot_strings = []
        for p in plots:
            loc_name = LOCATION_TYPES[p.location_type]["name"]
            plot_strings.append(f"{p.acres} Acres ({loc_name}) | Buy: ${p.purchase_price:,} | Lease: ${p.lease_weekly_cost:,}/wk | Weekly Tax: ${p.weekly_tax:,}")
        plot_strings.append("Cancel")
        
        plot_choice = choose_from_list("Select a Land Plot to acquire:", plot_strings, allow_cancel=False)
        if plot_choice == len(plots):
            return
            
        selected_plot = plots[plot_choice]
        
        acq_choices = [
            f"Buy Land Outright (${selected_plot.purchase_price:,})",
            f"Lease Land (${selected_plot.lease_weekly_cost:,}/wk + taxes)",
            "Cancel"
        ]
        acq_choice = choose_from_list("How will you acquire the land?", acq_choices, allow_cancel=False)
        if acq_choice == 2:
            return
            
        land_type = "owned" if acq_choice == 0 else "leased"
        upfront_land_cost = selected_plot.purchase_price if land_type == "owned" else 0.0
        
        if artist.money < upfront_land_cost:
            print("\n[ERROR] You do not have enough money to acquire this land.")
            cli_pause()
            return
            
        artist.money -= upfront_land_cost
        
        categories = ["club", "theatre", "auditorium", "ground", "arena", "stadium"]
        cat_details = [
            "Club (min 1 Acre, base cost $600k, capacity 800)",
            "Theatre (min 2 Acres, base cost $1.5M, capacity 2000)",
            "Auditorium (min 5 Acres, base cost $4.0M, capacity 4000)",
            "Ground (min 10 Acres, base cost $10.0M, capacity 12000)",
            "Arena (min 20 Acres, base cost $25.0M, capacity 22000)",
            "Stadium (min 50 Acres, base cost $60.0M, capacity 65000)"
        ]
        
        cat_choice = choose_from_list("What category of venue would you like to construct?", cat_details, allow_cancel=False)
        selected_cat = categories[cat_choice]
        
        min_acres = {"club": 1, "theatre": 2, "auditorium": 5, "ground": 10, "arena": 20, "stadium": 50}[selected_cat]
        if selected_plot.acres < min_acres:
            print(f"\n[ERROR] This category ({selected_cat.upper()}) requires at least {min_acres} acres of land. Your plot has only {selected_plot.acres} acres.")
            cli_pause()
            artist.money += upfront_land_cost
            return
            
        base_const_cost = {
            "club": 600000.0,
            "theatre": 1500000.0,
            "auditorium": 4000000.0,
            "ground": 10000000.0,
            "arena": 25000000.0,
            "stadium": 60000000.0
        }[selected_cat]
        
        material_choices = [
            "Budget Materials (30% discount, starts with 35 buzz / 50 safety, 25% weekly delay risk)",
            "Standard Materials (Standard cost, starts with 50 buzz / 80 safety, 5% weekly delay risk)",
            "Premium Materials (50% premium cost, starts with 65 buzz / 98 safety, 0% delay risk, review star bonus)",
            "Cancel"
        ]
        mat_choice = choose_from_list("Select Construction Material Quality:", material_choices, allow_cancel=False)
        if mat_choice == 3:
            artist.money += upfront_land_cost
            return
            
        mat_type = ["budget", "standard", "premium"][mat_choice]
        mat_mult = {"budget": 0.7, "standard": 1.0, "premium": 1.5}[mat_type]
        final_construction_cost = base_const_cost * mat_mult
        
        if artist.money < final_construction_cost:
            print(f"\n[ERROR] You cannot afford construction. Upfront cost: ${final_construction_cost:,.2f}")
            cli_pause()
            artist.money += upfront_land_cost
            return
            
        artist.money -= final_construction_cost
        
        # Base Amenities Upfront Installation Selection
        installed_base = []
        required_ids = ["washrooms", "parking", "ventilation", "basic_signage"]
        if selected_cat in ["theatre", "auditorium", "arena", "stadium"]:
            required_ids.append("escalators")
            
        while True:
            menu_opts = []
            for a_id in required_ids:
                status = "Installed" if a_id in installed_base else "Not Installed"
                cost = get_base_amenity_cost(a_id, selected_cat)
                menu_opts.append(f"{BASE_AMENITY_DETAILS[a_id]['name']} (Cost: ${cost:,.2f}) [{status}]")
            menu_opts.append("Done Selecting Base Amenities")
            
            choice = choose_from_list("Select Base Amenities to construct (upfront payment):", menu_opts, allow_cancel=False)
            if choice == len(required_ids):
                break
                
            selected_id = required_ids[choice]
            cost = get_base_amenity_cost(selected_id, selected_cat)
            
            if selected_id in installed_base:
                artist.money += cost
                installed_base.remove(selected_id)
                print(f"Removed {BASE_AMENITY_DETAILS[selected_id]['name']}. Refunded ${cost:,.2f}.")
            else:
                if artist.money < cost:
                    print("You do not have enough money to install this basic amenity.")
                else:
                    artist.money -= cost
                    installed_base.append(selected_id)
                    print(f"Installed {BASE_AMENITY_DETAILS[selected_id]['name']}. Deducted ${cost:,.2f}.")
        
        venue_name = prompt_text("Enter a name for your venue: ", "The Grand Amphitheater")
        
        capacity = {"club": 800, "theatre": 2000, "auditorium": 4000, "ground": 12000, "arena": 22000, "stadium": 65000}[selected_cat]
        construction_weeks = random.randint(16, 20)
        
        new_venue = OwnedVenue(
            id=f"ov_{random.randint(100, 999)}",
            name=venue_name,
            category=selected_cat,
            capacity=capacity,
            type="ground_up",
            status="construction",
            construction_weeks_left=construction_weeks,
            construction_material=mat_type,
            land_size_acres=selected_plot.acres,
            land_weekly_tax=selected_plot.weekly_tax,
            land_type=land_type,
            land_purchase_price=selected_plot.purchase_price,
            location_type=selected_plot.location_type,
            base_amenities=installed_base
        )
        
        artist.owned_venues.append(new_venue)
        print(f"\n[SUCCESS] Land acquired and construction started! Upfront construction cost paid: ${final_construction_cost:,.2f}")
        print(f"  {venue_name} will be ready in approximately {construction_weeks} weeks.")
        cli_pause()

    elif opt == 1:
        # Renovate existing
        renos = generate_weekly_renovation_options(artist)
        if not renos:
            print("\nThere are no renovated venue options available this week.")
            cli_pause()
            return
            
        print("\nAvailable Run-Down Properties:")
        reno_strings = []
        for r in renos:
            loc_name = LOCATION_TYPES[r["location_type"]]["name"]
            reno_strings.append(f"{r['name']} | Location: {loc_name} | Size: {r['acres']} ac | Capacity: {r['capacity']:,} | Cost: ${r['purchase_price']:,}")
        reno_strings.append("Cancel")
        
        reno_choice = choose_from_list("Select a venue to purchase and renovate:", reno_strings, allow_cancel=False)
        if reno_choice == len(renos):
            return
            
        selected_reno = renos[reno_choice]
        
        if artist.money < selected_reno["purchase_price"]:
            print("\n[ERROR] You cannot afford to purchase this venue.")
            cli_pause()
            return
            
        artist.money -= selected_reno["purchase_price"]
        
        venue_name = prompt_text("Enter a new name for this renovated venue: ", selected_reno["name"])
        
        new_venue = OwnedVenue(
            id=f"ov_{random.randint(100, 999)}",
            name=venue_name,
            category=selected_reno["category"],
            capacity=selected_reno["capacity"],
            type="renovated",
            status="operational",
            construction_weeks_left=0,
            construction_material="standard",
            land_size_acres=selected_reno["acres"],
            land_weekly_tax=selected_reno["weekly_tax"],
            land_type="owned",
            land_purchase_price=selected_reno["purchase_price"],
            location_type=selected_reno["location_type"],
            base_amenities=[],  # Renovated properties start with no basic amenities, user must install them!
            buzz=30.0,
            review_stars=2.8
        )
        
        artist.owned_venues.append(new_venue)
        print(f"\n[SUCCESS] Purchased and opened '{venue_name}' for renovation! Upfront purchase cost paid: ${selected_reno['purchase_price']:,}")
        print("  The venue is operational and ready for booking immediately.")
        cli_pause()

def manage_venues_flow(artist):
    from rapsim_reviews.career_mode import choose_from_list, prompt_text, prompt_int
    
    operational_venues = [v for v in artist.owned_venues if v.status == "operational"]
    if not operational_venues:
        print("\nYou have no operational venues to manage. Start building or purchasing one first!")
        cli_pause()
        return
        
    print("\nSelect an operational venue to manage:")
    v_strings = [f"{v.name} ({v.category.upper()}) | Rating: {v.review_stars} stars | Buzz: {v.buzz}" for v in operational_venues]
    v_strings.append("Cancel")
    
    venue_idx = choose_from_list("Operational Venues:", v_strings, allow_cancel=False)
    if venue_idx == len(operational_venues):
        return
        
    selected_venue = operational_venues[venue_idx]
    
    while True:
        upkeep = calculate_venue_upkeep(selected_venue)
        loc_cfg = LOCATION_TYPES.get(selected_venue.location_type, {})
        print(f"\n==========================================")
        print(f" VENUE: {selected_venue.name} ({selected_venue.category.upper()})")
        print(f"==========================================")
        print(f" Location: {loc_cfg.get('name', 'Unknown')}")
        print(f" Status: Operational | Capacity: {selected_venue.capacity:,} seats")
        print(f" Rating: {selected_venue.review_stars}/5.0 stars | Buzz: {selected_venue.buzz}/100")
        print(f" Safety Rating: {selected_venue.safety_rating:.1f}/100")
        print(f" Base Rental Fee: ${selected_venue.base_hire_cost:,.2f}")
        print(f" Event share cut: {selected_venue.base_cut_pct*100:.1f}%")
        print(f" Weekly Taxes: ${selected_venue.land_weekly_tax:,.2f} | Upkeep Upkeep: ${upkeep:,.2f}")
        print(f" Land Size: {selected_venue.land_size_acres} Acres ({selected_venue.land_type})")
        print(f" Basic Amenities: {', '.join([BASE_AMENITY_DETAILS[ba]['name'] for ba in selected_venue.base_amenities if ba in BASE_AMENITY_DETAILS]) or 'None'}")
        print(f" Upgrade Amenities: {', '.join([AMENITIES[a]['name'] for a in selected_venue.amenities if a in AMENITIES]) or 'None'}")
        print(f"==========================================")
        
        choices = [
            "Set Base Rental Fee & Revenue Share Cut",
            "Install Upgrade Amenities",
            "Install/Upgrade Base Amenities",
            "Upgrade/Expand Seating Capacity",
            "Run Marketing Promotion (Boost Buzz)",
            "Do a Charity Concert (Fatigue cost, boosts reputation and venue buzz)",
            "View Customer Reviews Feed",
            "View Performance Revenue & Sales Log",
            "View Transaction History / Past Events",
            "Go Back"
        ]
        
        action_choice = choose_from_list("Select Action:", choices, allow_cancel=False)
        
        if action_choice == 0:
            # Set base hire and cut
            try:
                hire_fee = float(input(f"Enter base rental fee (current: ${selected_venue.base_hire_cost:,.2f}): ").strip())
                if hire_fee < 0:
                    print("Invalid amount.")
                    continue
                selected_venue.base_hire_cost = hire_fee
                
                cut_pct = float(input(f"Enter event share cut percentage 0-100 (current: {selected_venue.base_cut_pct*100:.1f}%): ").strip())
                if not (0 <= cut_pct <= 100):
                    print("Invalid range.")
                    continue
                selected_venue.base_cut_pct = cut_pct / 100.0
                print("\n[SUCCESS] Venue booking terms updated.")
            except ValueError:
                print("Invalid numerical inputs.")
            cli_pause()
            
        elif action_choice == 1:
            # Install amenities
            available_upgrades = []
            for key, details in AMENITIES.items():
                if selected_venue.category in details["categories"]:
                    if key not in selected_venue.amenities:
                        available_upgrades.append((key, details))
                        
            if not available_upgrades:
                print("\nThis venue has all compatible upgrades installed!")
                cli_pause()
                continue
                
            print("\nSelect an Upgrade Amenity to purchase:")
            upgrade_strings = []
            for key, details in available_upgrades:
                upgrade_strings.append(f"{details['name']} | Cost: ${details['cost']:,} | Stars: +{details['rating_bonus']} | Buzz: +{details['buzz_bonus']} | Upkeep: +${details['upkeep']}/wk")
            upgrade_strings.append("Cancel")
            
            up_choice = choose_from_list("Upgrades list:", upgrade_strings, allow_cancel=False)
            if up_choice == len(available_upgrades):
                continue
                
            up_key, up_details = available_upgrades[up_choice]
            if artist.money < up_details["cost"]:
                print("\n[ERROR] You cannot afford to purchase this amenity.")
                cli_pause()
                continue
                
            artist.money -= up_details["cost"]
            selected_venue.amenities.append(up_key)
            
            selected_venue.buzz = min(100.0, selected_venue.buzz + up_details["buzz_bonus"])
            update_venue_ratings(selected_venue)
            
            print(f"\n[SUCCESS] Installed upgrade: {up_details['name']}!")
            cli_pause()
            
        elif action_choice == 2:
            # Install basic amenities
            required_ids = ["washrooms", "parking", "ventilation", "basic_signage"]
            if selected_venue.category in ["theatre", "auditorium", "arena", "stadium"]:
                required_ids.append("escalators")
                
            missing = [a for a in required_ids if a not in selected_venue.base_amenities]
            if not missing:
                print("\nAll basic amenities are already installed at this venue!")
                cli_pause()
                continue
                
            print("\nSelect a Basic Amenity to install:")
            amenity_menu = []
            for a_id in missing:
                cost = get_base_amenity_cost(a_id, selected_venue.category)
                amenity_menu.append(f"{BASE_AMENITY_DETAILS[a_id]['name']} | Cost: ${cost:,.2f}")
            amenity_menu.append("Cancel")
            
            choice = choose_from_list("Basic Amenities list:", amenity_menu, allow_cancel=False)
            if choice == len(missing):
                continue
                
            selected_id = missing[choice]
            cost = get_base_amenity_cost(selected_id, selected_venue.category)
            if artist.money < cost:
                print("\n[ERROR] You cannot afford to install this basic amenity.")
            else:
                artist.money -= cost
                selected_venue.base_amenities.append(selected_id)
                update_venue_ratings(selected_venue)
                print(f"\n[SUCCESS] Installed basic amenity: {BASE_AMENITY_DETAILS[selected_id]['name']}!")
            cli_pause()
            
        elif action_choice == 3:
            # Capacity upgrade
            category_caps = {
                "club": 1500,
                "theatre": 3500,
                "auditorium": 8000,
                "ground": 20000,
                "arena": 35000,
                "stadium": 100000
            }
            cap_limit = category_caps.get(selected_venue.category, selected_venue.capacity)
            max_add = cap_limit - selected_venue.capacity
            
            print(f"\nUpgrade Venue Capacity for {selected_venue.name}:")
            print(f"  Current Seating Capacity: {selected_venue.capacity:,} seats")
            print(f"  Maximum Category Capacity Limit: {cap_limit:,} seats")
            
            if max_add <= 0:
                print("\nThis venue is already at maximum seating capacity for its category!")
                cli_pause()
                continue
                
            print(f"  You can add up to {max_add:,} seats. Cost per seat is $50.00.")
            seats_to_add = prompt_int(f"Enter number of seats to add (1 - {max_add}): ", minimum=1, maximum=max_add)
            upgrade_cost = seats_to_add * 50.0
            
            if artist.money < upgrade_cost:
                print(f"\n[ERROR] You cannot afford this capacity upgrade. Cost: ${upgrade_cost:,.2f}")
            else:
                artist.money -= upgrade_cost
                selected_venue.capacity += seats_to_add
                print(f"\n[SUCCESS] Added {seats_to_add:,} seats to capacity! New capacity: {selected_venue.capacity:,} seats.")
            cli_pause()
            
        elif action_choice == 4:
            week_idx = ((artist.year - 1) * 52) + artist.week
            promos_this_week = sum(1 for ev in selected_venue.past_events_history if ev.get("type") == "promotion" and ev.get("week") == week_idx)
            if promos_this_week >= 3:
                print("\n[ERROR] You can only run promotions at most thrice a week for this venue.")
                cli_pause()
                continue
                
            # Run promotion
            print("\nSelect promotion level to run this week:")
            promos = [
                "Local Social Media Campaign (Cost: $25,000, Buzz +2 to +4)",
                "Radio & Press Ads (Cost: $75,000, Buzz +5 to +8)",
                "Massive Billboard Ads (Cost: $250,000, Buzz +10 to +15)",
                "Cancel"
            ]
            promo_choice = choose_from_list("Promotion options:", promos, allow_cancel=False)
            if promo_choice == 3:
                continue
                
            cost = [25000, 75000, 250000][promo_choice]
            base_buzz_gain = random.randint(*([(2, 4), (5, 8), (10, 15)][promo_choice]))
            
            buzz_gain = int(base_buzz_gain * loc_cfg.get("buzz_growth_mult", 1.0))
            buzz_gain = min(15, buzz_gain)
            
            if artist.money < cost:
                print("\n[ERROR] You do not have enough money to run this ad campaign.")
                cli_pause()
                continue
                
            artist.money -= cost
            selected_venue.buzz = min(100.0, selected_venue.buzz + buzz_gain)
            
            selected_venue.past_events_history.append({
                "week": week_idx,
                "type": "promotion",
                "details": f"Ran promotion level {promo_choice} (Cost: ${cost:,.2f})",
                "net": -cost
            })
            
            print(f"\n[SUCCESS] Promotion campaign completed! Venue buzz increased by +{buzz_gain} (Location modifier applied, Max +15).")
            cli_pause()
            
        elif action_choice == 5:
            # Charity concert
            week_idx = ((artist.year - 1) * 52) + artist.week
            
            # Enforce at most 1 charity show per week across all owned venues
            charity_this_week = False
            for v in getattr(artist, "owned_venues", []):
                for ev in getattr(v, "past_events_history", []):
                    if ev.get("type") == "charity_show" and ev.get("week") == week_idx:
                        charity_this_week = True
                        break
            if charity_this_week:
                print("\n[ERROR] You have already performed a charity show this week. Limit is 1 per week.")
                cli_pause()
                continue

            if artist.fatigue > 70.0:
                print("\n[ERROR] You are too fatigued to perform a charity show. REST FIRST.")
                cli_pause()
                continue
                
            cost = 15000.0
            if artist.money < cost:
                print(f"\n[ERROR] You cannot afford the staging and operational cost of a charity show (${cost:,.2f}).")
                cli_pause()
                continue
                
            artist.money = float(artist.money - cost)
            artist.fatigue = max(0.0, min(140.0, artist.fatigue + 30.0))
            buzz_gain = random.randint(2, 5)  # Capped at 5
            rep_gain = random.randint(3, 8)
            
            selected_venue.buzz = min(100.0, selected_venue.buzz + buzz_gain)
            artist.reputation = max(1.0, min(100.0, artist.reputation + rep_gain))
            
            selected_venue.past_events_history.append({
                "week": week_idx,
                "type": "charity_show",
                "details": f"Staged charity show (Staging cost: ${cost:,.2f})",
                "net": -cost
            })
            
            print(f"\n[CHARITY SHOW SUCCESS] You staged a charity show at {selected_venue.name}!")
            print(f"  Operational Cost Paid: ${cost:,.2f} | Reputation: +{rep_gain} | Venue Buzz: +{buzz_gain} (Max +5) | Fatigue: +30.0")
            cli_pause()
            
        elif action_choice == 6:
            # View customer reviews
            print(f"\n=== Customer Reviews Feed for {selected_venue.name} ===")
            if not selected_venue.reviews:
                print("No reviews posted yet.")
            else:
                for r in selected_venue.reviews:
                    stars_str = "★" * int(r["rating"]) + "☆" * (5 - int(r["rating"]))
                    print(f"  {format_week_range(r['week'])} | {r['username']} | Rating: {stars_str} ({r['rating']}/5.0)")
                    print(f"    Comment: \"{r['comment']}\"")
                    print("-" * 50)
            cli_pause("\nPress Enter to return...")
            
        elif action_choice == 7:
            # View Performance Revenue & Sales Log
            print(f"\n=== Performance Revenue & Sales Log for {selected_venue.name} ===")
            if not selected_venue.past_shows_log:
                print("No performances recorded yet.")
            else:
                print(f"{'Week':<17} | {'Artist':<18} | {'Attendance':<10} | {'Gross Revenue':<14} | {'Venue Rent+Cut':<15} | {'Controversy':<15}")
                print("-" * 96)
                for s in reversed(selected_venue.past_shows_log):
                    print(f"{format_week_range(s['week']):<17} | {s['artist_name']:<18} | {s['attendance']:<10,} | ${s['gross_revenue']:<13,.2f} | ${s['revenue_to_venue']:<14,.2f} | {s['controversy']:<15}")
            cli_pause("\nPress Enter to return...")
            
        elif action_choice == 8:
            # View transaction ledger
            print(f"\n=== Transaction History for {selected_venue.name} ===")
            if not selected_venue.past_events_history:
                print("No transactions recorded yet.")
            else:
                for t in reversed(selected_venue.past_events_history):
                    net_str = f"+${t['net']:,.2f}" if t["net"] >= 0 else f"-${abs(t['net']):,.2f}"
                    print(f"  {format_week_range(t['week'])} | {t['type'].upper()}: {t['details']} -> {net_str}")
            cli_pause("\nPress Enter to return...")
            
        else:
            break

def review_bookings_flow(artist):
    from rapsim_reviews.career_mode import choose_from_list
    
    operational_venues = [v for v in artist.owned_venues if v.status == "operational"]
    if not operational_venues:
        print("\nYou have no operational venues.")
        cli_pause()
        return
        
    print("\nSelect a venue to review pending requests:")
    v_strings = [f"{v.name} ({v.category.upper()}) | Pending requests: {sum(1 for r in v.booking_requests if not r.get('accepted'))}" for v in operational_venues]
    v_strings.append("Cancel")
    
    v_choice = choose_from_list("Venues list:", v_strings, allow_cancel=False)
    if v_choice == len(operational_venues):
        return
        
    selected_venue = operational_venues[v_choice]
    
    while True:
        pending_reqs = [r for r in selected_venue.booking_requests if not r.get("accepted")]
        if not pending_reqs:
            print(f"\nAll pending requests processed.")
            break
            
        print("\nSelect a pending request to review:")
        req_strings = []
        for r in pending_reqs:
            req_strings.append(f"{r['artist_name']} (Pop: {r['artist_popularity']}) | {format_week_range(r['week'])} | Offer: ${r['rent_fee']:,} + {r['cut_pct']*100:.0f}% cut")
        req_strings.append("Back")
        
        req_choice = choose_from_list("Pending Booking Offers:", req_strings, allow_cancel=False)
        if req_choice == len(pending_reqs):
            break
            
        selected_req = pending_reqs[req_choice]
        
        print(f"\n==========================================")
        print(f" BOOKING OFFER DETAILS")
        print(f"==========================================")
        print(f" Requesting Artist: {selected_req['artist_name']}")
        print(f" Artist Popularity: {selected_req['artist_popularity']}/100")
        print(f" Proposed Show Week: {format_week_range(selected_req['week'])}")
        print(f" Upfront Base Rent Offer: ${selected_req['rent_fee']:,}")
        print(f" Revenue Ticket Cut Offer: {selected_req['cut_pct']*100:.1f}%")
        print(f"==========================================")
        
        actions = ["Accept Offer", "Decline Offer", "Go Back"]
        act = choose_from_list("Process Offer:", actions, allow_cancel=False)
        
        if act == 0:
            # Enforce max 3 accepted events per week for this venue
            accepted_for_week = sum(1 for b in selected_venue.booking_requests if b.get("accepted") and b.get("week") == selected_req["week"])
            player_shows_here = sum(1 for b in getattr(artist, "upcoming_concerts", []) if b.week == selected_req["week"] and getattr(b, "venue_id", None) == selected_venue.id)
            total_events = accepted_for_week + player_shows_here
            
            if total_events >= 3:
                print(f"\n[ERROR] This venue cannot host more than 3 events in a single week. {format_week_range(selected_req['week'])} already has {total_events} events scheduled.")
                cli_pause()
                continue
                
            selected_req["accepted"] = True
            print(f"\n[ACCEPTED] Offer accepted. The event has been scheduled for {format_week_range(selected_req['week'])}.")
            cli_pause()
        elif act == 1:
            selected_venue.booking_requests.remove(selected_req)
            print("\n[DECLINED] Booking request rejected.")
            cli_pause()
        else:
            continue

def view_construction_flow(artist):
    construction_venues = [v for v in artist.owned_venues if v.status == "construction"]
    if not construction_venues:
        print("\nYou have no venue properties under active construction.")
        cli_pause()
        return
        
    print("\nVenue Properties Under Construction:")
    for i, v in enumerate(construction_venues):
        print(f"  {i+1}. {v.name} ({v.category.upper()})")
        print(f"     Location Quality: {LOCATION_TYPES[v.location_type]['name']}")
        print(f"     Material Quality: {v.construction_material.upper()}")
        print(f"     Acre Plot Size  : {v.land_size_acres} Acres ({v.land_type})")
        print(f"     Taxes / Upkeep  : ${v.land_weekly_tax:,.2f}/week")
        print(f"     Est. Ready In   : {v.construction_weeks_left} weeks")
        print("-" * 50)
        
    cli_pause("Press Enter to return...")
