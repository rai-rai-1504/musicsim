"""Diss-track battles layered on top of the career-mode controversy system."""

from dataclasses import dataclass, field
import random
from uuid import uuid4

from rapsim_reviews.artist_ecosystem_sim import (
    catchiness_stream_multiplier,
    roll_catchiness_value,
    roll_virality_value_and_maturity,
    stream_decay_multiplier,
    stream_random_range,
)


DISS_SKILL_WEIGHTS = {
    "lyrics": 0.40,
    "battle_skills": 0.40,
    "vocals": 0.10,
    "production": 0.10,
}

DISS_TITLE_PATTERNS = [
    "ether", "the message", "back to back", "war", "the response",
    "hit em up", "surgical summer", "saints & sinners", "mirror",
    "pound cake", "the takeover", "no vaseline", "story of adidon",
    "infrared", "dead ringers", "kings dead", "like that",
    "meet the grahams", "not like us",
]

# Pools are deliberately fictional simulation text. Claims resolve when a track drops.
DISS_CLAIMS = {
    (1, 2): [
        ("{target} has been recycling the same flow for three albums straight", .92),
        ("{target} peaked with their debut and has been chasing it ever since", .86),
        ("nobody in the industry takes {target} seriously anymore", .82),
        ("{target} needs a ghostwriter to sound coherent", .78),
        ("{target} has never written a bar that made anyone think", .84),
        ("{target} ran out of things to say two years ago and kept talking anyway", .89),
        ("ask {target} what they stand for. they can't tell you.", .87),
        ("{target} spent more time on their rollout than on their music", .91),
        ("the people around {target} are more talented than {target} will ever be", .82),
        ("{target} has been buying their way onto charts for years", .74),
        ("{target}'s whole persona is borrowed from someone better", .85),
        ("the day {target} drops something honest is the day i retire", .86),
        ("{target} wouldn't know authenticity if it featured on their album", .83),
        ("every {target} album sounds like a rough draft someone approved too fast", .88),
        ("{target} has been chasing trends since day one and still can't catch one", .91),
        ("{target} is famous for existing not for talent", .80),
        ("the industry carried {target} and now they think they walked", .84),
        ("i heard {target}'s new record. heard it. that's all.", .94),
        ("{target} has been in decline since the moment people started paying attention", .81),
        ("you can hear {target} getting desperate in every new release", .86),
    ],
    (2, 4): [
        ("{target} can't fill arenas without buying tickets back from their own label", .68),
        ("the streams {target} gets are not organic. they never have been.", .64),
        ("{target} pays critics to score their projects higher than they deserve", .58),
        ("i was in the room when {target} admitted they don't write alone", .61),
        ("{target}'s team leaks their own controversies for attention", .66),
        ("{target} had a breakdown last year and the label buried it", .54),
        ("multiple producers have told me {target} takes credit they didn't earn", .60),
        ("{target} hasn't been sober in the studio in two years", .52),
        ("the {target} you see in public is a character someone else created", .70),
        ("{target}'s best verse was written by someone who got no credit for it", .63),
        ("i know for a fact {target} turned down a collab because they were scared", .68),
        ("{target} had to be removed from a session for being unprofessional", .61),
        ("the label owns {target} and {target} knows it", .72),
        ("{target} has been sampling artists without clearing rights for years", .58),
        ("{target} told an interviewer that journalism was fake and then paid for a profile", .66),
        ("{target} was dropped from three features this year alone", .57),
        ("the money {target} flaunts comes from debt they can't service", .52),
        ("{target}'s social numbers are inflated. the label admitted it internally.", .59),
        ("i know who {target} goes to when they run out of ideas. it's not inspiring.", .70),
        ("everything {target} built was handed to them and they still fumbled it", .74),
        ("{target} tried to get into the session last year and was told no by the engineer", .61),
        ("{target}'s relationship is a PR arrangement and they both know it", .49),
        ("people in the industry describe working with {target} as the worst experience of their career", .63),
        ("the deal {target} signed was the worst in the history of that label. they bragged about it.", .56),
        ("{target} has three aliases on streaming because they pad their own numbers", .53),
    ],
    (4, 6): [
        ("{target} settled a lawsuit last year that the public doesn't know about", .50),
        ("the incident at the {target} show last year was covered up by their management", .47),
        ("i have documentation that {target} stole royalties from a co-writer they silenced", .44),
        ("{target} manipulated a vulnerable artist to sign over publishing rights", .41),
        ("sources close to {target} confirmed the label controls everything they release", .54),
        ("{target} was investigated internally for misconduct and it went nowhere because of money", .38),
        ("the reason {target} cut off their old collaborators is because they were witnesses", .44),
        ("{target} had a physical altercation backstage that their team paid to keep quiet", .48),
        ("i know for a fact {target} plagiarised the concept for their biggest album", .40),
        ("multiple women in the industry have warned each other about {target} privately", .34),
        ("{target} paid for airplay on three major markets and called it organic success", .50),
        ("the fallout between {target} and their producer was about stolen credit. i was there.", .56),
        ("{target} has been laundering money through their merchandise operation for years", .28),
        ("people who worked closely with {target} describe abuse of power that never went public", .36),
        ("{target} sabotaged a rising artist's deal because they felt threatened", .44),
        ("the documentary about {target} was killed because their lawyers made calls", .41),
        ("{target}'s public persona was designed by a PR firm after an incident they are hiding", .38),
        ("there is footage of {target} doing things that contradict everything they claim to stand for", .34),
        ("{target} had a financial relationship with a streaming platform that influenced playlist placement", .47),
        ("the breakup of {target}'s original crew was initiated by {target} lying to every member separately", .50),
    ],
    (6, 8): [
        ("{target} has been funding the silence of former collaborators through NDAs worth millions", .42),
        ("a forensic accountant told me {target}'s finances are the most creative thing about them", .39),
        ("{target} is currently under federal investigation and the label is managing the timeline", .35),
        ("i have messages from {target}'s inner circle confirming they plagiarised three albums", .37),
        ("the situation with {target} and that producer in 2019 is more serious than anyone reported", .36),
        ("{target} threatened a journalist who was preparing to run a story about their behaviour", .42),
        ("every person who has left {target}'s team has signed an agreement to never speak about what they saw", .39),
        ("{target} fabricated the backstory behind their most celebrated project", .44),
        ("there are people in {target}'s own family who haven't spoken to them in years over what happened", .40),
        ("{target} had an artist blacklisted from three major labels because they refused to collaborate", .37),
        ("i was shown documents proving {target} received advance payment for an album that doesn't exist", .34),
        ("{target} has a pattern of targeting younger artists in ways the industry has quietly acknowledged", .33),
        ("the reason {target} didn't attend that ceremony was because they were told not to come", .43),
        ("{target}'s relationships are all transactional. every single one. i have proof.", .40),
        ("the rumours about {target} and that executive aren't rumours to people who were in the building", .35),
    ],
    (8, 10): [
        ("{target} has been systematically abusing their position for a decade and is protected by label money", .38),
        ("what {target} did to that artist is documented. i'm releasing everything.", .35),
        ("{target} is not who they claim to be. the persona, the backstory, the values - fabricated.", .41),
        ("i have recordings of {target} saying things that would end any other career immediately", .32),
        ("{target} committed fraud against their own fanbase and the label helped cover it", .33),
        ("the real reason {target}'s mentor cut contact is because of what {target} did to their family", .35),
        ("{target} is currently blackmailing someone in the industry and it's going to come out", .31),
        ("every award {target} won in a five-year stretch was influenced by financial arrangements", .32),
        ("i know exactly what {target} did and so do ten other people in this industry who are all afraid to say it", .33),
        ("{target} hired people to discredit artists who were about to expose them. i'm one of them.", .30),
    ],
}

DISS_NEWS_TEMPLATES = {
    "released": [
        '{instigator} drops "{title}" - a full diss track aimed directly at {target}.',
        'The beef escalates: {instigator} releases "{title}", a direct response to {target}.',
        '{instigator} goes nuclear on {target} with the release of "{title}".',
        'A private feud becomes a public record as {instigator} releases "{title}" for {target}.',
        '{instigator} turns the argument into a single, and "{title}" is already dominating the conversation around {target}.',
    ],
    "true": [
        'Claims made by {instigator} about {target} on "{title}" are being corroborated by sources.',
        'Industry insiders are confirming {instigator}\'s allegations about {target} on "{title}".',
    ],
    "false": [
        'Claims made by {instigator} about {target} on "{title}" are being disputed and debunked.',
        '"{title}" is losing credibility fast as {instigator}\'s claims about {target} are exposed as false.',
    ],
    "no_response": [
        '{target} has chosen not to respond to {instigator}\'s "{title}". The silence is noted.',
        '{target} is staying quiet after "{title}", leaving fans to argue over what that silence means.',
        'No response yet from {target} after {instigator}\'s "{title}", though the pressure around the feud is clearly building.',
    ],
    "verdict": [
        'The {instigator}/{target} diss battle appears to be cooling off, but fan arguments over the winner are only getting louder.',
        'After {rounds} diss tracks between {instigator} and {target}, the scene is split over who walked away with the stronger case.',
        'With no new replies expected, commentators are still debating the {instigator}/{target} battle instead of calling it cleanly settled.',
    ],
}

DISS_TWITTER = {
    "release": [
        '"{title}" is out. no subtitles needed.',
        'pressed record with the lights off and said exactly what i meant. "{title}" is out.',
        'no rollout theatre. no friendly warning. "{title}" is outside.',
        'if {target} wants to know where i stand, track one answers it.',
        'made the booth smell like smoke tonight. "{title}" is live.',
    ],
    "pre_response": [
        'i heard it. took notes. leave the studio light on.',
        'not typing paragraphs. drums are loading.',
        'asked me to respond. okay. remember that you asked.',
        'the funny part is thinking i needed a week to find words.',
        'silence is not fear. sometimes it is sequencing.',
    ],
    "fan_hype": [
        '{instigator} dropped "{title}" and the whole timeline started reading body language.',
        'i need {target} in a studio immediately. this cannot end as a notes app apology.',
        '"{title}" has people pausing lines like they are evidence in court.',
        'this {instigator}/{target} thing went from messy to historic in one upload.',
        'you can hear the exact moment "{title}" stops being a song and becomes a problem.',
    ],
    "fan_true": [
        'the {instigator} claims about {target} are TRUE?? the timeline is not okay.',
        'the receipts are real. {instigator} wasn\'t lying. {target} in serious trouble.',
    ],
    "fan_false": [
        'the {instigator} claims about {target} on "{title}" are falling apart in real time',
        'receipts dropping. {instigator} made up half of "{title}". the internet never forgets.',
    ],
    "critic": [
        '"{title}" by {instigator} is a sharp, ugly piece of theatre. The writing is what makes it hard to ignore.',
        'The striking thing about "{title}" is not just the anger. It is how carefully {instigator} aims it.',
        '{instigator} understands that a diss has to be memorable before it can be damaging. "{title}" clears that bar.',
    ],
    "verdict": [
        'people are acting like the {instigator}/{target} beef is settled but half my group chat still disagrees',
        'timeline leaning one way on {instigator} vs {target}, group chats leaning another. perfect beef chaos',
        'nobody is changing their mind about {instigator}/{target} today, which probably means the battle did its job',
        'the public seems to have a favorite in the {instigator}/{target} battle, but the argument is nowhere near over',
    ],
}


@dataclass
class DissClaim:
    claim_text: str
    brutality_range: tuple[int, int]
    true_probability: float
    is_true: bool


@dataclass
class DissTrack:
    id: str
    battle_id: str
    week_released: int
    instigator: str
    target: str
    title: str
    quality: float
    brutality: float
    diss_number: int
    claims: list[DissClaim]
    true_claims: list[DissClaim]
    false_claims: list[DissClaim]
    critic_score: float
    user_rating: float
    reception_score: float
    producer: str | None
    engineer: str | None
    catchiness: float
    virality: float
    maturity_weeks: int
    virality_triggered: bool = False
    virality_weeks_active: int = 0
    virality_max_weekly_bonus: int = 0
    virality_baseline_streams: int = 0
    last_week_streams: int = 0
    total_streams: int = 0


def ensure_diss_state(world):
    defaults = {
        "diss_tracks": [],
        "pending_diss_responses": [],
        "diss_news_schedule": {},
        "diss_tweet_schedule": {},
        "diss_verdicts": [],
    }
    for key, default in defaults.items():
        if not hasattr(world, key):
            setattr(world, key, default)


def is_hip_hop_artist(artist) -> bool:
    top_2 = sorted(artist.genres.items(), key=lambda item: -item[1])[:2]
    return any(genre == "hip hop" for genre, _ in top_2)


def should_release_diss_track(artist, beef_loop_count: int) -> bool:
    if beef_loop_count < 5 or not is_hip_hop_artist(artist):
        return False
    aggression = int(getattr(artist, "aggression", 45))
    probability = .55 if aggression >= 80 else .42 if aggression >= 65 else .30 if aggression >= 50 else .20 if aggression >= 35 else .10
    return random.random() < probability


def should_respond_to_diss(artist, dissing_artist) -> bool:
    if not is_hip_hop_artist(artist):
        return False
    if float(artist.popularity) >= float(dissing_artist.popularity) + 20:
        return random.random() < .38
    aggression = int(getattr(artist, "aggression", 45))
    probability = .95 if aggression > 70 else .82 if aggression > 40 else .58 if aggression > 30 else .25
    return random.random() < probability


def calculate_diss_track_quality(artist) -> float:
    craft = sum(float(artist.skills.get(skill, 50)) * weight for skill, weight in DISS_SKILL_WEIGHTS.items() if skill != "battle_skills")
    craft += float(getattr(artist, "battle_skills", 50)) * DISS_SKILL_WEIGHTS["battle_skills"]
    raw_percent = max(1.0, craft * .65 + float(artist.genres.get("hip hop", 50)) * .35)
    curved = 1.0 + 8.25 * ((raw_percent / 100.0) ** 2.35)
    return round(max(0.0, min(10.0, curved + random.uniform(-.35, .35))), 1)


def calculate_brutality(artist, diss_number_in_beef: int) -> float:
    base = min(5.2, 2.2 + (diss_number_in_beef - 1) * 1.15)
    brutality = base + (float(getattr(artist, "aggression", 45)) / 100.0) * 3.4 + random.uniform(-.25, .9)
    cap = {1: 6.8, 2: 8.2, 3: 9.2, 4: 10.0, 5: 10.0}.get(min(diss_number_in_beef, 5), 10.0)
    if diss_number_in_beef == 1:
        brutality = min(brutality, 6.0 + random.uniform(0, 1.2))
    return round(max(1.0, min(brutality, cap)), 1)


def get_claims_for_brutality(brutality_score: float, num_claims: int = 3) -> list[DissClaim]:
    eligible = []
    for brutality_range, pool in DISS_CLAIMS.items():
        if brutality_range[0] <= brutality_score <= brutality_range[1]:
            center = sum(brutality_range) / 2.0
            for template, probability in pool:
                eligible.append((template, probability, brutality_range, 1.0 / (1.0 + abs(center - brutality_score))))
    if not eligible:
        eligible = [(template, probability, (1, 2), 1.0) for template, probability in DISS_CLAIMS[(1, 2)]]
    selected = []
    pool = list(eligible)
    for _ in range(min(num_claims, len(pool))):
        pick = random.choices(pool, weights=[item[3] for item in pool], k=1)[0]
        pool.remove(pick)
        selected.append(DissClaim(pick[0], pick[2], pick[1], random.random() < pick[1]))
    return selected


def resolve_claim_impact(diss_track: DissTrack) -> None:
    critic_delta = 0.0
    user_delta = 0.0
    for claim in diss_track.claims:
        low = claim.brutality_range[0]
        if claim.is_true:
            critic_delta += 1.2 if low >= 8 else .8 if low >= 6 else .5 if low >= 4 else .2
            user_delta += 1.0 if low >= 8 else .7 if low >= 6 else .4 if low >= 4 else .2
        else:
            critic_delta -= 2.5 if low >= 8 else 1.5 if low >= 6 else .8 if low >= 4 else .3
            user_delta -= 2.0 if low >= 8 else 1.2 if low >= 6 else .6 if low >= 4 else .2
    diss_track.critic_score = round(max(1.0, min(10.0, diss_track.quality + critic_delta)), 1)
    diss_track.user_rating = round(max(1.0, min(10.0, diss_track.user_rating + user_delta)), 1)


def calculate_reception_score(diss_track: DissTrack) -> float:
    credibility = (len(diss_track.true_claims) / len(diss_track.claims) * 10.0) if diss_track.claims else 5.0
    return round(min(10.0, diss_track.quality * .60 + diss_track.brutality * .15 + credibility * .25), 1)


def _diss_base_streams(quality: float, catchiness: float, week_since_release: int, popularity: float) -> int:
    """Weekly base streams — same curve as career_mode.stream_count_for_song (before virality)."""
    quality_factor = max(0.0, min(1.0, float(quality) / 10.0))
    popularity_factor = max(0.0, min(1.0, float(popularity) / 100.0))
    weighted_score = (popularity_factor * 0.7) + (quality_factor * 0.3)
    base_constant = 2_000_000 if float(popularity) < 20.0 else 10_000_000
    base_streams = base_constant * (weighted_score**1.85) * (quality_factor**1.7)
    base_streams *= stream_decay_multiplier(int(week_since_release))
    base_streams *= catchiness_stream_multiplier(catchiness)
    low_mult, high_mult = stream_random_range(base_streams)
    streams_base = int(random.uniform(base_streams * low_mult, base_streams * high_mult))
    return min(150_000_000, max(0, streams_base))


def _diss_virality_bonus(diss_track: DissTrack, streams_base: int, week_since_release: int) -> int:
    v = float(diss_track.virality)
    maturity = int(diss_track.maturity_weeks)
    if v < 2.0:
        return 0
    if (not diss_track.virality_triggered) and (week_since_release >= maturity):
        diss_track.virality_triggered = True
        diss_track.virality_weeks_active = 0
        diss_track.virality_max_weekly_bonus = 0
        diss_track.virality_baseline_streams = int(max(0, streams_base))
    if not diss_track.virality_triggered:
        return 0
    age = int(diss_track.virality_weeks_active)
    if v < 3.0:
        lo, hi = 100_000, 500_000
    elif v < 4.0:
        lo, hi = 2_000_000, 10_000_000
    else:
        lo, hi = 30_000_000, 70_000_000
    if age <= 7:
        bonus = int(random.uniform(lo, hi))
        diss_track.virality_max_weekly_bonus = max(diss_track.virality_max_weekly_bonus, bonus)
        return bonus
    peak = max(diss_track.virality_max_weekly_bonus, hi)
    floor_bonus = max(int(0.02 * peak), int(diss_track.virality_baseline_streams))
    t = min(1.0, max(0.0, (age - 8) / 8.0))
    target = (1.0 - t) * peak + t * floor_bonus
    bonus = int(random.uniform(target * 0.88, target * 1.05))
    return max(0, bonus)


def calculate_diss_streams(diss_track: DissTrack, week_since_release: int, popularity: float) -> int:
    streams_base = _diss_base_streams(
        diss_track.quality,
        diss_track.catchiness,
        week_since_release,
        popularity,
    )
    return streams_base + _diss_virality_bonus(diss_track, streams_base, week_since_release)


def generate_diss_title(target_name: str, producer_name: str | None) -> str:
    credit = f"(prod. {producer_name})" if producer_name else "(self-produced)"
    return f"{random.choice(DISS_TITLE_PATTERNS)} (diss track for {target_name.split()[0].lower()}) {credit}"


def determine_beef_winner(tracks: list[DissTrack]):
    scores = {}
    for track in tracks:
        scores.setdefault(track.instigator, []).append(track.reception_score)
    averages = {artist: sum(values) / len(values) for artist, values in scores.items()}
    if len(averages) < 2:
        artist = next(iter(averages))
        return artist, "", f"{artist} wins by default", averages
    winner = max(averages, key=averages.get)
    loser = min(averages, key=averages.get)
    margin = averages[winner] - averages[loser]
    verdict = "draw" if margin < .5 else f"{winner} edges it" if margin < 1.5 else f"{winner} wins clearly" if margin < 3 else f"{winner} wins decisively"
    return winner, loser, verdict, averages


def tracks_for_beef(world, artist_a: str, artist_b: str, battle_id: str | None = None) -> list[DissTrack]:
    pair = {artist_a, artist_b}
    return [
        track for track in world.diss_tracks
        if {track.instigator, track.target} == pair
        and (battle_id is None or track.battle_id == battle_id)
    ]


def _pick_credit(seeds, skill: str, role_word: str):
    candidates = [seed for seed in seeds if role_word in seed.role or int(seed.skills.get(skill, 0)) >= 82]
    return random.choice(candidates).name if candidates else None


def release_diss_track(world, instigator, target, current_week: int, diss_number: int, seeds, battle_id: str | None = None) -> DissTrack:
    ensure_diss_state(world)
    quality = calculate_diss_track_quality(instigator)
    brutality = calculate_brutality(instigator, diss_number)
    claims = get_claims_for_brutality(brutality, random.randint(2, 4))
    producer = _pick_credit(seeds, "production", "producer")
    engineer = _pick_credit(seeds, "mix/master", "engineer")
    catchiness = roll_catchiness_value()
    virality, maturity_weeks = roll_virality_value_and_maturity()
    diss = DissTrack(
        id=str(uuid4()), battle_id=str(battle_id or uuid4()), week_released=current_week, instigator=instigator.name,
        target=target.name, title=generate_diss_title(target.name, producer),
        quality=quality, brutality=brutality, diss_number=diss_number,
        claims=claims, true_claims=[claim for claim in claims if claim.is_true],
        false_claims=[claim for claim in claims if not claim.is_true],
        critic_score=quality, user_rating=quality, reception_score=0.0,
        producer=producer, engineer=engineer, catchiness=catchiness,
        virality=virality, maturity_weeks=maturity_weeks,
    )
    diss.user_rating = round(max(1.0, min(10.0, quality * .70 + min(catchiness / 5 * 10, 10) * .30)), 1)
    resolve_claim_impact(diss)
    diss.reception_score = calculate_reception_score(diss)
    diss.user_rating = round(max(1.0, min(10.0, diss.reception_score * .85 + min(catchiness / 5 * 10, 10) * .15)), 1)
    first_week = calculate_diss_streams(diss, 1, float(instigator.popularity))
    diss.last_week_streams = first_week
    diss.total_streams = diss.last_week_streams
    world.diss_tracks.append(diss)
    world.diss_news_schedule.setdefault(current_week + 1, []).append(("false" if diss.false_claims else "true", diss.id))
    if diss.true_claims and diss.false_claims:
        world.diss_news_schedule[current_week + 1].append(("true", diss.id))
    world.diss_tweet_schedule.setdefault(current_week, []).append(("release", diss.id))
    world.diss_tweet_schedule.setdefault(current_week + 1, []).append(("claims", diss.id))
    return diss


def step_diss_streams(world, popularity_by_name: dict[str, float] | None = None):
    ensure_diss_state(world)
    popularity_by_name = popularity_by_name or {}
    for track in world.diss_tracks:
        week_since_release = int(world.week_number) - int(track.week_released) + 1
        if week_since_release <= 1:
            continue
        popularity = float(popularity_by_name.get(track.instigator, 50.0))
        track.last_week_streams = calculate_diss_streams(track, week_since_release, popularity)
        track.total_streams += track.last_week_streams
        if track.virality_triggered:
            track.virality_weeks_active += 1


def build_scheduled_news(world, current_week: int, report_factory) -> list:
    ensure_diss_state(world)
    reports = []
    for kind, payload in world.diss_news_schedule.pop(current_week, []):
        if kind == "verdict":
            artist_a, artist_b, verdict, rounds = payload
            template = random.choice(DISS_NEWS_TEMPLATES["verdict"])
            headline = template.format(instigator=artist_a, target=artist_b, verdict=verdict, rounds=rounds)
            reports.append(report_factory(current_week, "diss_verdict", headline, artist_a, artist_b, verdict))
            continue
        track = next((item for item in world.diss_tracks if item.id == payload), None)
        if track is None:
            continue
        template = random.choice(DISS_NEWS_TEMPLATES[kind])
        headline = template.format(instigator=track.instigator, target=track.target, title=track.title)
        reports.append(report_factory(current_week, f"diss_{kind}_claim", headline, track.instigator, track.target, track.title))
    return reports


def schedule_verdict(world, track: DissTrack, current_week: int):
    battle_tracks = tracks_for_beef(world, track.instigator, track.target, track.battle_id)
    winner, loser, verdict, scores = determine_beef_winner(battle_tracks)
    world.diss_verdicts.append({"winner": winner, "loser": loser, "verdict": verdict, "scores": scores})
    world.diss_news_schedule.setdefault(current_week + 1, []).append(("verdict", (track.instigator, track.target, verdict, len(battle_tracks))))
    world.diss_tweet_schedule.setdefault(current_week + 1, []).append(("verdict", (track.instigator, track.target, verdict)))


def build_scheduled_tweets(world, current_week: int, tweet_factory) -> list:
    ensure_diss_state(world)
    tweets = []
    for kind, payload in world.diss_tweet_schedule.pop(current_week, []):
        if kind == "verdict":
            artist_a, artist_b, verdict = payload
            text = random.choice(DISS_TWITTER["verdict"]).format(instigator=artist_a, target=artist_b, verdict=verdict)
            tweets.append(tweet_factory("fan", "fan", "diss_verdict", text))
            continue
        if kind == "pre_response":
            responder, track_id = payload
            track = next((item for item in world.diss_tracks if item.id == track_id), None)
            if track is not None:
                text = random.choice(DISS_TWITTER["pre_response"]).format(instigator=track.instigator)
                tweets.append(tweet_factory(responder, "artist", "diss_response", text))
            continue
        track = next((item for item in world.diss_tracks if item.id == payload), None)
        if track is None:
            continue
        if kind == "release":
            artist_text = random.choice(DISS_TWITTER["release"]).format(title=track.title, target=track.target)
            fan_text = random.choice(DISS_TWITTER["fan_hype"]).format(instigator=track.instigator, target=track.target, title=track.title)
            critic_text = random.choice(DISS_TWITTER["critic"]).format(instigator=track.instigator, title=track.title, score=track.reception_score, brutality=track.brutality)
            tweets.extend([
                tweet_factory(track.instigator, "artist", "diss_release", artist_text),
                tweet_factory("fan", "fan", "diss_hype", fan_text),
                tweet_factory("critic", "critic", "diss_review", critic_text),
            ])
        else:
            pool = DISS_TWITTER["fan_false"] if track.false_claims else DISS_TWITTER["fan_true"]
            text = random.choice(pool).format(instigator=track.instigator, target=track.target, title=track.title)
            tweets.append(tweet_factory("fan", "fan", "diss_claims", text))
    return tweets


def display_diss_track(diss: DissTrack):
    print()
    print("+" + "=" * 66 + "+")
    print("|" + "  DISS TRACK  ".center(66) + "|")
    print("+" + "=" * 66 + "+")
    print(f"\n  {diss.title.upper()}")
    print(f"  by {diss.instigator} -> targeting {diss.target}\n")
    print(f"  Quality:    {diss.quality}/10")
    print(f"  Brutality:  {diss.brutality}/10")
    print(f"  Reception:  {diss.reception_score}/10")
    print(f"  Streams:    {diss.total_streams:,} total | {diss.last_week_streams:,} last week")
    print("\n  CLAIMS")
    print("  " + "-" * 60)
    for index, claim in enumerate(diss.claims, 1):
        status = "TRUE" if claim.is_true else "FALSE"
        print(f"  {index}. {claim.claim_text.format(target=diss.target)}")
        print(f"     [{status}] brutality range {claim.brutality_range[0]}-{claim.brutality_range[1]}")
    if diss.producer:
        print(f"\n  Produced by: {diss.producer}")
    if diss.engineer:
        print(f"  Engineered by: {diss.engineer}")
    print()
