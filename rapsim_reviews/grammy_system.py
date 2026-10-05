"""rapsim_reviews.grammy_system
Grammys award show, nomination voting, category processing, speeches,
and awards media coverage.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import TYPE_CHECKING
from uuid import uuid4

from rapsim_reviews.date_system import format_week_range
from rapsim_reviews.ui_helpers import (
    choose_from_list,
    meter_bar,
    money_fmt,
    prompt_text,
    clamp_meter,
    clamp_popularity,
)
from rapsim_reviews.critic_system import CRITIC_NAMES, _critic_username
from rapsim_reviews.career_models import (
    Artist,
    ARTIST_BASE_REPUTATION,
    _ensure_song_bg_attrs,
    _player_week_index,
    _year_week_from_world_week,
    _ecosystem_artist_popularity,
    _ecosystem_artist_reputation,
)
from rapsim_reviews.news_system import NewsReport, _build_news_report

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld
    from rapsim_reviews.twitter_system import Tweet

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


def _grammy_week_number(current_week: int) -> int:
    return _year_week_from_world_week(current_week)[1]


def _is_grammy_media_week(current_week: int) -> bool:
    return 49 <= _grammy_week_number(current_week) <= 52


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


def _generate_grammy_tweets(current_week: int, world: EcosystemWorld, player_artist, all_artists: list[Artist], all_critics: list[str]) -> list:
    if player_artist is None or not _is_grammy_media_week(current_week):
        return []
    year, week_in_year = _year_week_from_world_week(current_week)
    results = _ensure_grammy_results(player_artist, world, year)
    if not results:
        return []

    from rapsim_reviews.twitter_system import (
        Tweet,
        _ecosystem_artist_object,
        _compact_tweet_title,
    )

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

