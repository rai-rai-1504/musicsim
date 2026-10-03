"""rapsim_reviews.twitter_system
Twitter feed, tweets generation (fan, artist, critic), controversy reactions,
release announcements, and tracklist reveals.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from types import SimpleNamespace
from typing import TYPE_CHECKING
from uuid import uuid4

from rapsim_reviews.date_system import format_week_range
from rapsim_reviews.ui_helpers import choose_from_list, prompt_text
from rapsim_reviews.critic_system import (
    CRITIC_NAMES,
    _critic_username,
    _expand_pool_dict,
    _expand_sentence_pool,
)
from rapsim_reviews.diss_track_system import build_scheduled_tweets
from rapsim_reviews.artist_ecosystem_sim import prepare_release_calendar
from rapsim_reviews.career_models import (
    Artist,
    _player_week_index,
    _ecosystem_seed_by_name,
    _ecosystem_artist_popularity,
    _find_world_runtime,
    _is_growing_artist_name,
    classify_artist_skills,
    _year_week_from_world_week,
)
from rapsim_reviews.grammy_system import (
    _is_grammy_media_week,
    _generate_grammy_tweets,
)
from rapsim_reviews.romance_system import (
    _get_romance_profile,
    _artist_aggression,
    _ensure_romance_state,
)
from rapsim_reviews.news_system import (
    ControversyEvent,
    TYPE_3_ACTIONS,
    _controversy_action_rep,
)

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld

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


ARTIST_CONTROVERSY_TWEETS = _expand_pool_dict(ARTIST_CONTROVERSY_TWEETS, min_extra=10, max_extra=14)
ARTIST_RELEASE_ANNOUNCEMENT = _expand_pool_dict(ARTIST_RELEASE_ANNOUNCEMENT, min_extra=10, max_extra=12)
ARTIST_FRIEND_PRAISE = _expand_pool_dict(ARTIST_FRIEND_PRAISE, min_extra=10, max_extra=12)
FAN_CONTROVERSY_REACTIONS = _expand_pool_dict(FAN_CONTROVERSY_REACTIONS, min_extra=10, max_extra=14)
FAN_RELEASE_REACTIONS = _expand_pool_dict(FAN_RELEASE_REACTIONS, min_extra=10, max_extra=14)
FAN_RELEASE_RECEPTION = _expand_pool_dict(FAN_RELEASE_RECEPTION, min_extra=10, max_extra=14)
FAN_FEATURE_REACTIONS = _expand_pool_dict(FAN_FEATURE_REACTIONS, min_extra=10, max_extra=14)
CRITIC_TWEETS = _expand_pool_dict(CRITIC_TWEETS, min_extra=10, max_extra=14)


ARTIST_TRACKLIST_REVEAL = _expand_sentence_pool(ARTIST_TRACKLIST_REVEAL, min_extra=10, max_extra=12)
FAN_RUMOURS = _expand_sentence_pool(FAN_RUMOURS, min_extra=10, max_extra=14)


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


def _ensure_twitter_state(world: EcosystemWorld | None):
    if world is not None and getattr(world, "twitter_module", None) is None:
        world.twitter_module = TwitterModule()


def _tweet_release_title(title: str, artist_name: str) -> str:
    prefix = f"{artist_name} - "
    short = title[len(prefix):] if str(title).startswith(prefix) else str(title)
    return short.strip()


def _compact_tweet_title(title: str, max_len: int = 54) -> str:
    text = str(title).strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


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


def _weekly_release_score(release) -> float:
    return float(getattr(release, "review", getattr(release, "review_score", 0.0)))


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
    print("|" + f" X / TWITTER / {format_week_range(current_week).upper()} ".center(70) + "|")
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


def _releases_for_week(world: EcosystemWorld, week_number: int) -> list:
    rows = []
    if world and hasattr(world, "release_history"):
        for artist_name, releases in world.release_history.items():
            for release in releases:
                if int(getattr(release, "week_number", -1)) == int(week_number):
                    rows.append(release)
    return rows


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

