"""Live stream chat simulation for the career mode."""

import random
from collections import deque
from types import SimpleNamespace

from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS


ECOSYSTEM_ARTISTS = [seed.name for seed in ARTIST_ECOSYSTEM_SEEDS]
ECOSYSTEM_FRIENDLINESS = {
    seed.name: int(getattr(seed, "friendliness", 50)) for seed in ARTIST_ECOSYSTEM_SEEDS
}

CRITICS = [
    "Marcus Vane", "Deja Hayes", "Vic Osei", "Ray Coldwell",
    "Earl Mosely", "Zara Nights", "Tobias Lund", "Nina Pascal",
    "Teena Naruka", "Shatam Rai",
]

USERNAME_STARTS = [
    "midnight", "vinyl", "slow", "atlas", "soft", "north", "local", "static",
    "echo", "signal", "quiet", "retro", "dream", "lunar", "silver", "coast",
    "blue", "cinder", "radio", "neon", "minor", "south", "autumn", "velvet",
]

USERNAME_ENDS = [
    "archive", "listener", "sleeper", "tempo", "thread", "wave", "notes", "mono",
    "district", "garden", "memory", "radio", "theory", "habit", "season", "pilot",
    "transit", "club", "window", "capsule", "corner", "signal", "frame", "room",
]

SYSTEM_FEED = [
    "viewer_count jumps for a moment",
    "chat speeds up",
    "clips are probably being made right now",
    "the room gets noisier",
    "mods pin a message asking chat to relax",
]

MICRO_REACTIONS = {
    "positive": ["W", "hell yeah", "yeah", "real", "exactly", "facts", "run it", "hard", "love this"],
    "negative": ["L", "nah", "skip", "mid", "not this one", "still no", "weak", "nope"],
}

TIRED_REACTIONS = [
    "you sound exhausted bro",
    "log off and sleep",
    "please go rest",
    "bro take a nap",
    "i like you but you look drained",
    "you should probably get some sleep",
    "this stream feels tired",
    "not even being rude, go rest",
    "you are running on fumes right now",
    "bro your voice sounds tired",
    "you need one full week of sleep",
    "this stream got sleep deprivation energy",
    "go drink water and disappear for a bit",
    "you look like you have not rested in days",
]

OVERLIVE_REACTIONS = [
    "get in the studio bro",
    "you on the gram too much",
    "bro stream less and record more",
    "you be live every day now",
    "starting to feel too available",
    "go make music instead",
    "you doing too much on the gram",
    "we do not need this many lives",
    "bro go missing for two days and make something",
    "you are online more than you are mysterious",
    "we know your face now go make records",
    "too much talking not enough music",
    "this app is becoming your full time job",
    "you really love the front camera huh",
    "everytime i open this app and i see their ugly ass going live",
    "STOPPPPPPPP ALREADY",
    "studio rent too high brother?"
    "bro has only one app on their phone",
    "no wonder the songs are not working out",
    "switch careers man, you better infront of camera than mic",

]

LOW_HEALTH_REACTIONS = [
    "bro you need sleep",
    "we get it now sleep",
    "this guy about to die bro",
    "bro on death bed and he still cares about this",
    "please log off and get healthy",
    "you look rough man",
    "damn dawg you really losing weight for this next album",
    "we get it now sleep it off brother",
    "bro your body is filing complaints at this point",
    "somebody get this man soup and eight hours",
    "you look like the album is winning",
    "forget the stream and call a doctor",
    "this is not grind this is self destruction",
    "bro looking medically unavailable right now",
    "oh he miserable rn",
    "getting on live from emergency room is crazy",
    "this next album about to be so good",
]

CONDITION_TARGET_REACTIONS = [
    "bro we get that you dislike {target}, now get some rest",
    "bro on death bed and he still cares about {target}",
    "they really got {target} living rent free in his head",
    "omg he's obsessed with {target}",
    "bro miserable for attention at this point",
    "brother this your {nth} live this week, are you sure the problem is them",
    "{target} is not worth losing sleep over like this",
    "he looks exhausted and still wants to talk about {target}",
    "bro needs sleep more than he needs to mention {target}",
    "this whole stream is just {target} and low blood sugar",
    "he is way too tired to still be this focused on {target}",
    "chat i think {target} is on his mind 24/7 now",
    "brother your pulse should not be this connected to {target}",
    "you need a nap more than you need another opinion on {target}",
    "at this point {target} is just your bedtime story",
    "if {target} got you this stressed just log off",
    "the obsession with {target} is starting to look expensive",
    "bro is exhausted and still making time for {target}",
]

RELATIONSHIP_CONFUSION_ON_DISS = [
    "what the hell?? i thought they were cool",
    "wait i thought they were friends??",
    "nah i did not expect that",
    "i thought we'd see them on a track next album",
    "here goes another good industry friendship",
    "bro they used to be tight tho",
    "that came outta nowhere, aren't they cool?",
    "this hurts more than the diss itself",
    "why are you doing this to your friend",
    "i thought this was one of your people",
    "that friendship is cooked",
    "i swear they were just showing love last month",
    "so that was fake love the whole time?",
    "nah this is confusing as hell",
    "industry friendships are so fragile",
]

RELATIONSHIP_EXPECTED_DISS = [
    "yeah i saw that coming",
    "obviously dawg",
    "finally",
    "hell yeah this has been brewing for a long time now",
    "about time you said it",
    "we all knew you hated them",
    "this been tension for ages",
    "i knew this was gonna happen",
    "that was inevitable",
    "they been had problems",
    "this is not shocking at all",
    "you been subbing for weeks",
    "this is the least surprising thing ever",
    "you finally said it out loud",
    "that beef been loading",
]

RELATIONSHIP_CAP_ON_PRAISE = [
    "is he kidding?",
    "no way you meant that",
    "stop the cap, we know you hate them",
    "that shoutout feels fake",
    "nah this is a setup",
    "you switching up for the camera",
    "why you praising your opp now",
    "this is not believable",
    "bro you literally hate them",
    "cap cap cap",
    "you trolling right",
    "this gotta be sarcasm",
    "so now you like them? sure",
    "that praise did not land",
    "chat is this real??",
]

OPINION_MEMORY_2 = {
    ("praise", "praise"): [
        "you really been showing love lately",
        "ok we get it you respect them",
        "second shoutout? fair",
        "you consistent with the love",
        "that's the energy i like",
        "this is wholesome actually",
        "you pushing peace fr",
        "you riding for them huh",
        "alright shoutout again",
        "you tryna lock in a collab",
        "you been standing on that respect",
        "ok ok another salute",
        "you keep giving them flowers",
        "this feels genuine",
        "this is the nicest stream ever",
    ],
    ("praise", "criticize"): [
        "why you switching up??",
        "didn't you praise them a minute ago?",
        "wait what happened all of a sudden",
        "bro you were just showing love",
        "that's a crazy pivot",
        "you changed your mind fast",
        "this is mixed signals",
        "so was the praise fake?",
        "nah this is messy",
        "you can't do both like that",
        "you were cool with them five minutes ago",
        "this is awkward",
        "that escalated quick",
        "why you turning like that",
        "chat is confused",
    ],
    ("criticize", "praise"): [
        "wait now you praising?",
        "you just dissed them though",
        "that's a wild switch up",
        "so y'all cool again?",
        "this feels like damage control",
        "bro make up your mind",
        "that praise sounds forced now",
        "did someone text you?",
        "what changed?",
        "this is messy but funny",
        "ok so the beef not real?",
        "you folding on live",
        "you trying to be nice now",
        "so we pretending that diss didn't happen?",
        "this is confusing",
    ],
    ("criticize", "criticize"): [
        "oh you doubling down",
        "ok he really hates them",
        "yeah keep going then",
        "he not letting that go",
        "this is personal now",
        "bro is locked in on them",
        "the hate is consistent",
        "nah you on their head",
        "this is a full segment now",
        "you really do not like them",
        "damn you cooking them again",
        "you not moving on huh",
        "this is just a diss stream",
        "you still mad",
        "ok ok we heard you",
    ],
}

OPINION_MEMORY_3 = {
    ("praise", "praise", "criticize"): [
        "nah you were praising twice and now you dissing??",
        "that is a crazy heel turn",
        "three mentions and now it's negative?",
        "bro how did we get here",
        "this is whiplash",
        "you just ruined the whole vibe",
        "this friendship arc is cooked",
        "you were building peace and then threw it away",
        "you tryna start drama on purpose",
        "chat just got emotionaliplash",
        "ok so that love was fake",
        "you can't do that after two shoutouts",
        "this is messy industry behavior",
        "you had everyone believing in peace",
        "and now you diss? wild",
    ],
    ("praise", "criticize", "praise"): [
        "bro make up your mind",
        "praise diss praise is nasty work",
        "this is hot and cold",
        "you playing both sides",
        "what even is your stance",
        "you arguing with yourself",
        "this is so confusing",
        "you just apologized on live?",
        "chat cannot follow this",
        "you tryna fix it now",
        "that middle diss was for what then",
        "you doing PR in real time",
        "ok so y'all cool again",
        "this is a soap opera",
        "keep the same energy bro",
    ],
    ("praise", "criticize", "criticize"): [
        "so the praise was bait??",
        "you started nice then went full hate",
        "nah you meant that",
        "you really snapped mid stream",
        "this turned ugly fast",
        "you got irritated and just kept going",
        "ok so you're done with them",
        "that first shoutout is pointless now",
        "bro you spiraling on them",
        "chat is eating this up",
        "damn you locked in on the diss",
        "you had one nice moment then crashed out",
        "this is a timeline shift",
        "you chose violence",
        "this is the messiest arc",
    ],
    ("criticize", "criticize", "praise"): [
        "nah you just praised after two disses??",
        "did someone call you mid stream",
        "this is damage control",
        "you backpedaling hard",
        "that's a crazy reversal",
        "so you don't mean the disses?",
        "you trying to look mature now",
        "chat knows you still mad",
        "this praise sounds forced",
        "you switching up for the audience",
        "ok so what was the point then",
        "that is confusing",
        "you folded",
        "you doing PR right now",
        "this is funny honestly",
    ],
    ("criticize", "praise", "criticize"): [
        "diss praise diss is crazy",
        "you cannot be serious",
        "you beefing in a circle",
        "bro pick a side",
        "this is mood swings",
        "you just argued then apologized then argued again",
        "chat is exhausted",
        "that middle praise didn't even count",
        "you doing too much",
        "this is a soap opera",
        "this is why nobody trusts industry friendships",
        "you keep flipping",
        "what changed in five minutes",
        "this is messy",
        "bro stand on something",
    ],
    ("criticize", "praise", "praise"): [
        "ok you really trying to fix it",
        "you apologized and now you doubling on love",
        "this is reconciliation arc",
        "alright peace treaty i guess",
        "chat sees the switch though",
        "you trying to clean it up",
        "ok so you were just emotional earlier",
        "this is better than beef i guess",
        "you trying to keep it positive now",
        "two praises after a diss is funny",
        "you over-correcting",
        "chat wants drama but you want peace",
        "this feels like PR",
        "you trying to look mature",
        "we'll see how long it lasts",
    ],
}


def _clamp_rel(value):
    return max(0.0, min(100.0, float(value)))


def _week_index(artist):
    year = int(getattr(artist, "year", 1))
    week = int(getattr(artist, "week", 1))
    return ((year - 1) * 52) + week


def _get_opinion_history(artist, target_name):
    history = getattr(artist, "_live_opinion_history", None)
    if history is None:
        history = {}
        setattr(artist, "_live_opinion_history", history)
    return history.setdefault(target_name, [])


def _apply_live_relationship(artist, target_name, opinion_kind):
    rels = getattr(artist, "relationships", None)
    if not isinstance(rels, dict):
        return 0.0, 50.0, False
    state = rels.get(target_name)
    if state is None:
        state = SimpleNamespace(
            score=10.0,
            last_positive_week_interaction=0,
            last_positive_week_live=0,
            last_contact_week=0,
        )
        rels[target_name] = state
    pre_score = float(getattr(state, "score", 10.0))
    week_index = _week_index(artist)
    friendliness = int(ECOSYSTEM_FRIENDLINESS.get(target_name, 50))
    applied = True
    if opinion_kind == "praise":
        if int(getattr(state, "last_positive_week_live", 0)) == week_index:
            applied = False
            delta = 0.0
        else:
            base = 2.0 + (friendliness / 100.0) * 6.0
            delta = max(2.0, min(8.0, random.uniform(base - 1.5, base + 1.5)))
            state.score = _clamp_rel(pre_score + delta)
            state.last_positive_week_live = week_index
    else:
        base = 6.5 + ((50.0 - friendliness) / 100.0)
        delta = -max(5.0, min(10.0, random.uniform(base, base + 3.0)))
        state.score = _clamp_rel(pre_score + delta)
    state.last_contact_week = week_index
    return delta, pre_score, applied


def _relationship_chat_lines(opinion_kind, pre_score):
    if opinion_kind == "criticize":
        if pre_score >= 60:
            return RELATIONSHIP_CONFUSION_ON_DISS
        if pre_score < 10:
            return RELATIONSHIP_EXPECTED_DISS
    if opinion_kind == "praise" and pre_score < 10:
        return RELATIONSHIP_CAP_ON_PRAISE
    return []


def _memory_chat_lines(prev_history, current_kind):
    if not prev_history:
        return []
    if len(prev_history) >= 2:
        key3 = (prev_history[-2], prev_history[-1], current_kind)
        return OPINION_MEMORY_3.get(key3, [])
    key2 = (prev_history[-1], current_kind)
    return OPINION_MEMORY_2.get(key2, [])

STREAM_MISC = {
    "criticize_artist": {
        "short": [
            "that was messy", "he meant that", "too direct honestly", "chat got loud fast",
            "that name drop crazy", "now it's awkward", "not subtle at all", "he really said that",
        ],
        "medium": [
            "I get the frustration, but going at someone by name on live always changes the mood.",
            "That felt less like a joke and more like a real issue between them.",
            "If he keeps talking like that, people will remember the drama more than the music.",
            "That was entertaining, but it also felt a little reckless.",
            "The stream got way more tense the second that name came up.",
            "You can tell chat loves drama, but that was still a risky thing to say.",
            "It was a sharp line, just maybe not a smart one.",
        ],
        "questions": [
            "wait what happened between them?",
            "why is he bringing that up now?",
            "was that serious or a joke?",
            "did they already have beef?",
            "who clipped that yet?",
            "is he going to explain that or not?",
        ],
        "targeted": [
            "{target} is absolutely going to hear about this by tomorrow.",
            "Somebody is already sending that clip straight to {target}.",
            "If {target} responds, this whole thing gets bigger fast.",
            "That line about {target} did not sound accidental at all.",
            "You do not say {target}'s name on live like that unless you mean it.",
        ],
    },
    "criticize_critic": {
        "short": [
            "critic catching strays", "that was personal", "okay now we're here", "he is annoyed annoyed",
            "chat is split", "that came out fast", "not him saying that live", "yeah that's tension",
        ],
        "medium": [
            "Calling out a critic on live is bold because it never stays small.",
            "That sounded like a response he has wanted to make for a while.",
            "I can see why he is annoyed, but this gives the review even more attention.",
            "That was direct enough that somebody is definitely clipping it.",
            "You can disagree with a critic without making the whole stream about them.",
            "The tension is real now because that did not sound playful at all.",
            "He clearly took that review personally.",
        ],
        "questions": [
            "which review is he talking about?",
            "did that critic score him low or something?",
            "is he talking about the album review?",
            "who started this?",
            "what did the critic even say?",
            "is he going to read the review out loud?",
        ],
        "targeted": [
            "{target} is definitely getting tagged under every clip from this stream.",
            "If {target} sees this, they are probably writing about it tomorrow.",
            "That jab at {target} is going to travel way past this live.",
            "He said {target}'s name like he has been holding that in for a while.",
            "There is no way {target} does not get asked about this now.",
        ],
    },
    "praise_artist": {
        "short": [
            "good shout", "that was respectful", "fair praise honestly", "that felt genuine",
            "nice moment", "good energy there", "love that", "solid thing to say",
        ],
        "medium": [
            "That shoutout landed well because it did not sound performative.",
            "Giving another artist credit like that usually plays better than people think.",
            "It is nice hearing respect without it turning into a comparison war.",
            "That felt like a real compliment, not networking.",
            "The stream actually got calmer after that.",
            "That was one of the more genuine moments in the live.",
            "People can be cynical, but that sounded sincere to me.",
        ],
        "questions": [
            "have they worked together before?",
            "is that a collab hint?",
            "did he always rate them that high?",
            "why does chat sound surprised by that?",
            "is he talking music or just influence?",
            "has he praised them before?",
        ],
        "targeted": [
            "{target} honestly deserved that kind of respect.",
            "That was a good look for both him and {target}.",
            "People act surprised, but praising {target} is not controversial to me.",
            "It sounded like real appreciation for {target}, not strategy.",
            "That probably means more to {target} than chat realizes.",
        ],
    },
    "praise_critic": {
        "short": [
            "rare critic love", "that was mature", "good on him", "respectful answer",
            "that landed well", "surprisingly classy", "didn't expect that", "good stream moment",
        ],
        "medium": [
            "That was a smart way to handle criticism without sounding bitter.",
            "Praising a critic on live is rare, so people notice it immediately.",
            "That came off mature because he did not sound defensive at all.",
            "He gave credit without making it weird, which I respect.",
            "The chat was expecting a jab and got the opposite.",
            "That was probably the healthiest possible way to answer a reviewer.",
            "It makes the stream feel more grounded when he talks like that.",
        ],
        "questions": [
            "which critic was that?",
            "did they review him well recently?",
            "is he being serious right now?",
            "has he always liked that reviewer?",
            "what did the critic say that he agreed with?",
            "did chat expect him to diss them instead?",
        ],
        "targeted": [
            "{target} probably did not expect to catch praise on this stream.",
            "That was more generous to {target} than chat was ready for.",
            "Giving {target} credit like that changes the whole tone of the stream.",
            "Not many artists would talk about {target} that calmly on live.",
            "That kind of respect toward {target} is going to stand out.",
        ],
    },
}

SONG_CHAT_PROFILES = {
    "terrible": {
        "praise_chance": 0.12,
        "praise": {
            "short": [
                "hook is fine", "not the worst", "kind of catchy", "i hear something",
                "one part was cool", "beat not awful",
            ],
            "medium": [
                "I can hear one decent idea in here, but the rest is not really landing for me.",
                "There is maybe a version of this song that works, just not this version.",
                "I do not love it, but there is at least one section I would keep.",
            ],
            "questions": [
                "is this just a rough version?",
                "was the chorus placeholder?",
                "did he finish writing this?",
            ],
        },
        "hate": {
            "short": [
                "this is rough", "nah this weak", "mix is bad", "not ready at all",
                "please redo this", "this is not it", "way too unfinished", "the vocals are off",
            ],
            "medium": [
                "This sounds like something that needed a lot more time before being played on live.",
                "I am trying to hear the vision, but this is rough in almost every department.",
                "There are too many problems at once for this song to really survive.",
                "The idea might be there somewhere, but the execution is just not close yet.",
            ],
            "questions": [
                "why play this now?",
                "did chat need to hear this version?",
                "is he trolling us with this one?",
            ],
        },
    },
    "weak": {
        "praise_chance": 0.25,
        "praise": {
            "short": [
                "chorus is okay", "this part cool", "not awful honestly", "hook kind of works",
                "i see something", "beat is carrying",
            ],
            "medium": [
                "I would not call this great, but there are parts of it that absolutely work.",
                "This song has some decent ideas even if it does not fully come together.",
                "It is uneven, but I get why a few people in chat are defending it.",
            ],
            "questions": [
                "is he still changing this?",
                "did the second verse get cut?",
                "what version of the song is this?",
            ],
        },
        "hate": {
            "short": [
                "this needs work", "still not there", "kind of flat", "not enough happening",
                "i would scrap this", "the mix feels off", "this one weak",
            ],
            "medium": [
                "There is some structure here, but the song still feels too undercooked to really defend.",
                "I do not hate it, I just do not think the song earns much excitement.",
                "This feels like a draft that accidentally got treated like a finished record.",
            ],
            "questions": [
                "is this the final hook?",
                "why is the energy so low?",
                "was this made today?",
            ],
        },
    },
    "mid": {
        "praise_chance": 0.48,
        "praise": {
            "short": [
                "this is decent", "not bad at all", "chorus works", "okay this smooth",
                "i get it", "solid little record", "this one fine",
            ],
            "medium": [
                "This is pretty solid even if it is not exactly blowing me away.",
                "I would not call it special, but it sounds put together and easy to play through.",
                "There is enough here for me to understand why some people would really like it.",
                "This sits in that decent range where I would not skip it immediately.",
            ],
            "questions": [
                "is this going on the album?",
                "did this get reviewed yet?",
                "what genre is he calling this?",
            ],
        },
        "hate": {
            "short": [
                "kind of forgettable", "this is just okay", "nothing special here", "i need more from this",
                "mid but listenable", "it is fine i guess",
            ],
            "medium": [
                "This is not bad, it just does not leave much of an impression on me.",
                "I can see the appeal, but the song feels a little too safe to really stick.",
                "It sounds competent more than exciting.",
            ],
            "questions": [
                "am i missing the best part?",
                "why do i feel nothing yet?",
                "is chat hearing something i am not?",
            ],
        },
    },
    "good": {
        "praise_chance": 0.72,
        "praise": {
            "short": [
                "this is hard", "wait this smooth", "chorus really works", "this one nice",
                "i like this a lot", "yeah this good", "hook is stuck already", "this can drop now",
            ],
            "medium": [
                "This song is strong enough that I would actually keep coming back to it.",
                "The structure is clean and the record really settles in after a few seconds.",
                "This sounds like one of the better songs he has played on live.",
                "There is enough detail here that it does not feel like empty hype from chat.",
            ],
            "questions": [
                "when is he dropping this?",
                "did he preview this before?",
                "why does this not have more attention yet?",
            ],
        },
        "hate": {
            "short": [
                "not my thing", "i still do not love it", "good but not for me", "little too safe",
                "i need more edge", "not quite there for me",
            ],
            "medium": [
                "I get why people like it, but the song does not really connect with me personally.",
                "This is clearly well made, it just does not hit me the way it is hitting chat.",
                "I respect it more than I love it.",
            ],
            "questions": [
                "am i the only one not loving this?",
                "why is chat acting like this is perfect?",
                "is this the best one he has?",
            ],
        },
    },
    "great": {
        "praise_chance": 0.84,
        "praise": {
            "short": [
                "this is crazy", "nah this hard", "best one so far", "this one is real",
                "run that back", "this goes crazy", "need this now", "this is a hit",
            ],
            "medium": [
                "This is the kind of song where chat starts clipping before it even ends.",
                "I would actually be surprised if this did not become one of his stronger releases.",
                "Everything about this sounds way more locked in than usual.",
                "This feels like one of those songs people keep bringing up a month later.",
            ],
            "questions": [
                "why is this not out already?",
                "did anyone catch that line in the hook?",
                "is this his best song yet?",
            ],
        },
        "hate": {
            "short": [
                "still not my favorite", "good but overrated by chat", "i like parts more than whole",
                "strong but not classic", "good song wrong mood",
            ],
            "medium": [
                "I know chat loves this, but I am not as overwhelmed by it as everybody else is.",
                "The song is very good, I just would not call it unbeatable.",
                "I respect the craft here more than I emotionally connect with it.",
            ],
            "questions": [
                "am i crazy for not loving this most?",
                "which part are yall losing it over exactly?",
                "is this better than the last one though?",
            ],
        },
    },
    "elite": {
        "praise_chance": 0.93,
        "praise": {
            "short": [
                "oh this special", "this is insane", "favorite already", "this is the one",
                "yeah this different", "run it again", "need this tonight", "that chorus wow", "oh this next album about to be crazy",
                "RELEASE THIS!!!!!", "i love you so much dawg", "ive been waiting for this all my life", "i'm so glad i didnt die yesterday", "FUCKKKKKKKKKKKKKKKKK",
                "i get the wait now",
            ],
            "medium": [
                "This feels like one of those songs people claim as their favorite immediately.",
                "The whole room shifted when this started playing and I get why.",
                "This is the easiest song to believe in out of everything he has played.",
                "That is the kind of record people stream all week without getting tired of it.",
            ],
            "questions": [
                "how is this not out yet?",
                "is he saving this for the album?",
                "did anyone else get chills on that hook?",
            ],
        },
        "hate": {
            "short": [
                "great song not my fave", "still not topping the last one", "very good just not for me",
                "i respect it more than love it", "not worth the wait", "THIS SO ASS DAWG"
            ],
            "medium": [
                "I can hear how strong it is, but it is still not the exact kind of song I replay most.",
                "This is clearly elite, I just would not call it my personal favorite.",
                "The quality is obvious even if I am not reacting as hard as chat is.",
            ],
            "questions": [
                "is this better than his best release though?",
                "why do i feel late hearing this?",
                "does this top the album cuts or not?",
            ],
        },
    },
}

REVIEW_CHAT = {
    "loved": {
        "support": [
            "The reviews were right on this one.",
            "I get why critics rated this highly now.",
            "That score makes perfect sense after hearing it back.",
            "This deserved the strong reviews it got.",
        ],
        "pushback": [
            "I like it, but critics still overrated this a little.",
            "Good song, just not as great as the reviews made it sound.",
        ],
    },
    "liked": {
        "support": [
            "The reviews were pretty fair on this one.",
            "That average score feels about right to me.",
            "I can hear why people landed on a decent review range here.",
        ],
        "pushback": [
            "I still think reviewers were a bit hard on this.",
            "This sounds better on stream than the reviews suggested.",
        ],
    },
    "mixed": {
        "support": [
            "Yeah, mixed reviews makes sense for this song.",
            "I can hear exactly why critics were split on it.",
            "This is one of those songs where the review spread makes total sense.",
        ],
        "pushback": [
            "I still do not get why they were so mixed on this.",
            "The reviews were all over the place, but I like this more than that average suggests.",
            "This got judged weirdly in my opinion.",
        ],
    },
    "negative": {
        "support": [
            "I kind of understand why the reviews came in low.",
            "The average score makes more sense now that I am hearing it again.",
            "This is exactly the type of song critics would not really go for.",
        ],
        "pushback": [
            "I still do not get why they hated on this that much.",
            "The reviews were harsher than this song deserved.",
            "This was never a disaster to me, even if critics acted like it was.",
        ],
    },
}

FAN_LINES = {
    "good": [
        "This has quietly grown on me a lot.",
        "I keep coming back to this one more than I expected.",
        "This ended up being one of the songs I revisit the most.",
    ],
    "great": [
        "This is one of my favorite songs you have put out.",
        "I have been running this back all week.",
        "This is the kind of song that stays in rotation.",
        "I knew this one was strong the first time I heard it.",
    ],
    "elite": [
        "Oh shit this is my favorite song of yours.",
        "I have been streaming this for a week now.",
        "This is easily my favorite track you have dropped so far.",
        "I still replay this every day.",
        "This is the one I keep recommending to people.",
    ],
}

RELEASED_FAMILIARITY = {
    "terrible": {
        "praise": [
            "I still kind of defend this one even though I know most people hate it.",
            "This is not good, but there is one part I still remember liking.",
            "I would never call it great, but I get why a few people keep coming back to it.",
            "I still catch myself quoting one line from this even though I know the song is messy.",
            "I remember defending this when it dropped and I am not fully backing down now.",
        ],
        "hate": [
            "I have heard this enough times now and it still does not work for me.",
            "This is still one of the weakest songs you have put out.",
            "Even knowing the song already, I still think this was a bad release.",
            "I remember not liking this when it dropped and I still do not.",
            "This is still near the bottom of your catalog for me.",
            "Every time this comes on I remember why the reviews were so cold.",
        ],
        "questions": [
            "this really got a 1.8 average?",
            "was this the one critics killed?",
            "did anyone ever come around on this song?",
            "is this still the lowest reviewed one?",
        ],
    },
    "weak": {
        "praise": [
            "It has grown on me a little even if I know chat hates it.",
            "I would not call it one of your best, but I still have a soft spot for it.",
            "I have heard this enough times to know the better moments are real.",
            "This is one of those songs I defend more than I replay.",
            "I still think people were too hard on this one.",
        ],
        "hate": [
            "I have sat with this song for a while and it still does not really click for me.",
            "This is still one of the songs I come back to the least.",
            "Even after a week with it, this one still feels thin to me.",
            "I keep trying to revisit this and it never really improves for me.",
            "This is still a skip more often than not.",
        ],
        "questions": [
            "was this the track with the bad reviews?",
            "did this ever click for anybody else?",
            "why do i remember this being better?",
            "did this song have defenders when it dropped?",
        ],
    },
    "mid": {
        "praise": [
            "I have lived with this for a bit now and it is a solid track.",
            "This one settled in more after a few listens.",
            "I did not love it day one, but it has stayed with me more than I expected.",
        ],
        "hate": [
            "I have heard this enough now to know it is just okay to me.",
            "This is the kind of song I never skip angrily, but I also never search for.",
            "After a few listens I still think this is one of the more average tracks.",
        ],
        "questions": [
            "was this the one that got mixed reviews?",
            "am i the only one who remembers this being better live?",
            "did this ever become a fan favorite or no?",
        ],
    },
    "good": {
        "praise": [
            "This has been in rotation for me all week.",
            "I have heard this plenty now and it still lands every time.",
            "This is one of those songs that gets better once you live with it.",
        ],
        "hate": [
            "I respect this track more than I actually replay it.",
            "I know people love this one, but even after sitting with it I am not fully there.",
            "This is good, just not one of the songs I end up returning to most.",
        ],
        "questions": [
            "did this review lower than it should have?",
            "was this not one of the better reviewed songs?",
            "why does this sound stronger every time i come back to it?",
        ],
    },
    "great": {
        "praise": [
            "I have been streaming this for days and it still does not feel old.",
            "This is already one of the songs I associate with you the most.",
            "I have heard this a bunch now and it still sounds huge.",
        ],
        "hate": [
            "I know this is one of the bigger songs, but it still is not my personal favorite.",
            "Even after replaying it, I like the craft more than the song itself.",
            "This is strong, just not the one I connect to most.",
        ],
        "questions": [
            "was this not one of the best reviewed tracks too?",
            "how is this not a bigger song for you?",
            "am i crazy for still preferring this over the singles?",
        ],
    },
    "elite": {
        "praise": [
            "This is still my favorite song of yours.",
            "I have been replaying this all week and I am still not tired of it.",
            "This is one of those releases people keep around for a long time.",
            "I already know this will stay in rotation for me.",
        ],
        "hate": [
            "This is clearly huge, but it still is not the one I attach to most.",
            "I get why everybody calls this a favorite, even if mine is still something else.",
            "I respect how strong this is, but I still have another track above it.",
        ],
        "questions": [
            "is this still your best song to me or am i forgetting one?",
            "how did critics not all go crazy for this?",
            "does he even know how much people replay this one?",
        ],
    },
}


def generate_usernames(n=120):
    usernames = set()
    while len(usernames) < n:
        left = random.choice(USERNAME_STARTS)
        right = random.choice(USERNAME_ENDS)
        number = random.randint(0, 999)
        style = random.random()
        if style < 0.25:
            username = f"{left}_{right}"
        elif style < 0.55:
            username = f"{left}{right}{number}"
        else:
            username = f"{left}.{right}"
        usernames.add(username)
    return list(usernames)


def song_quality_band(quality):
    if quality < 2.5:
        return "terrible"
    if quality < 4.5:
        return "weak"
    if quality < 6.5:
        return "mid"
    if quality < 8.0:
        return "good"
    if quality < 9.3:
        return "great"
    return "elite"


def review_band(avg_review):
    if avg_review is None:
        return None
    if avg_review >= 8.2:
        return "loved"
    if avg_review >= 6.5:
        return "liked"
    if avg_review >= 5.0:
        return "mixed"
    return "negative"


def choose_target(title, options):
    while True:
        print(f"\n{title}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        raw = input("Choose: ").strip()
        try:
            choice = int(raw)
        except ValueError:
            print("Enter a valid number.")
            continue
        if 1 <= choice <= len(options):
            return options[choice - 1]
        print("Enter a valid number from the list.")


def available_song_options(artist):
    options = []
    for entry in artist.singles:
        if entry.released:
            options.append(
                {
                    "label": f"Released single: {entry.song.name}",
                    "song": entry.song,
                    "released": True,
                    "average_review": entry.average_review,
                }
            )
        else:
            options.append(
                {
                    "label": f"Unreleased single: {entry.song.name}",
                    "song": entry.song,
                    "released": False,
                    "average_review": None,
                }
            )
    for entry in artist.albums:
        for song in entry.album.songs:
            options.append(
                {
                    "label": f"Album track from {entry.album.name}: {song.name}",
                    "song": song,
                    "released": entry.released,
                    "average_review": None,
                }
            )
    return options


def choose_song_option(title, options):
    labels = [option["label"] for option in options]
    chosen = choose_target(title, labels)
    for option in options:
        if option["label"] == chosen:
            return option
    return options[0]


def attach_artist_context(song_option, artist):
    enriched = dict(song_option)
    enriched["artist"] = artist
    return enriched


def build_misc_message_bank(event_key, target_name=None):
    pools = STREAM_MISC[event_key]
    messages = []
    messages.extend(pools["short"])
    messages.extend(pools["medium"])
    messages.extend(pools["questions"])
    messages.extend(line.format(target=target_name) for line in pools["targeted"])
    return messages


def build_song_message_bank(song_name, quality, avg_review=None, released=False):
    band = song_quality_band(quality)
    profile = SONG_CHAT_PROFILES[band]
    messages = {"praise": [], "hate": []}

    if released:
        familiarity = RELEASED_FAMILIARITY.get(band)
        if familiarity:
            messages["praise"].extend(familiarity["praise"])
            messages["hate"].extend(familiarity["hate"])
            messages["praise"].extend(familiarity.get("questions", []))
            messages["hate"].extend(familiarity.get("questions", []))
    else:
        for tone in ("praise", "hate"):
            pool = profile[tone]
            messages[tone].extend(pool["short"])
            messages[tone].extend(pool["medium"])
            messages[tone].extend(pool["questions"])

    if released:
        review_tier = review_band(avg_review)
        if review_tier:
            messages["praise"].extend(REVIEW_CHAT[review_tier]["pushback"])
            messages["hate"].extend(REVIEW_CHAT[review_tier]["support"])

        if band in FAN_LINES:
            messages["praise"].extend(FAN_LINES[band])

        if avg_review is not None and avg_review <= 5.0 and quality >= 7.0:
            messages["praise"].extend([
                "I still do not get why they hated on this.",
                "This got judged way too harshly in my opinion.",
                f"'{song_name}' deserved better than that review average.",
            ])
        if avg_review is not None and avg_review <= 4.0 and quality <= 4.5:
            messages["hate"].extend([
                "I mean the review score was brutal, but I honestly get it.",
                f"'{song_name}' never really beat the allegations for me.",
                "The low average makes sense every time I come back to this.",
            ])
        if avg_review is not None and avg_review >= 7.5 and quality <= 5.5:
            messages["hate"].extend([
                "I never understood the praise this one got.",
                "This is one of your less convincing releases to me.",
                f"'{song_name}' is still one of my least favorite tracks of yours.",
            ])
        if avg_review is not None and avg_review >= 8.0 and quality >= 8.0:
            messages["praise"].extend([
                "This is one of those songs where the reviews actually matched the feeling.",
                f"'{song_name}' still sounds like a standout record.",
            ])

    return messages, profile["praise_chance"]


def choose_message(message_bank, recent_messages, tone):
    pool = [msg for msg in message_bank[tone] if msg not in recent_messages]
    if not pool:
        pool = message_bank[tone]
    return random.choice(pool)


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def live_reaction_count(artist):
    live_count = int(getattr(artist, "live_count_this_week", 0))
    if live_count <= 3:
        return random.randint(15, 20)
    if live_count == 4:
        return random.randint(12, 17)
    if live_count == 5:
        return random.randint(8, 12)
    if live_count == 6:
        return random.randint(4, 6)
    return random.randint(2, 3)


def build_condition_pool(artist, target_name=None):
    pool = []
    fatigue = float(getattr(artist, "fatigue", 0.0))
    health = float(getattr(artist, "health", 100.0))
    live_count = int(getattr(artist, "live_count_this_week", 0))

    if fatigue >= 85:
        pool.extend(TIRED_REACTIONS)
    if health <= 35:
        pool.extend(LOW_HEALTH_REACTIONS)
    if live_count > 3:
        pool.extend(OVERLIVE_REACTIONS)
        pool.append(
            f"brother this your {ordinal(live_count)} live this week, are you sure the problem is them"
        )
    if target_name and (fatigue >= 85 or health <= 35 or live_count > 3):
        nth = ordinal(live_count)
        pool.extend(
            line.format(target=target_name, nth=nth)
            for line in CONDITION_TARGET_REACTIONS
        )
    return pool


def build_song_condition_pool(artist):
    pool = []
    fatigue = float(getattr(artist, "fatigue", 0.0))
    health = float(getattr(artist, "health", 100.0))
    live_count = int(getattr(artist, "live_count_this_week", 0))

    if fatigue >= 85:
        pool.extend(TIRED_REACTIONS)
    if health <= 35:
        pool.extend(LOW_HEALTH_REACTIONS)
    if live_count > 3:
        pool.extend(OVERLIVE_REACTIONS)
        pool.append(
            f"brother this your {ordinal(live_count)} live this week, are you sure the problem is them"
        )
    return pool


def emit_chat_for_song(users, song_option, artist_name):
    song = song_option["song"]
    avg_review = song_option["average_review"]
    artist = song_option.get("artist")
    message_bank, praise_chance = build_song_message_bank(
        song.name,
        song.quality,
        avg_review=avg_review,
        released=song_option["released"],
    )
    recent_messages = deque(maxlen=20)
    chosen_users = random.sample(users, min(live_reaction_count(artist), len(users)))

    overlive_pool = OVERLIVE_REACTIONS if int(getattr(artist, "live_count_this_week", 0)) > 3 else []
    condition_pool = build_song_condition_pool(artist)

    for idx, user in enumerate(chosen_users, 1):
        if idx % random.randint(5, 7) == 0:
            print(f"system_feed: {random.choice(SYSTEM_FEED)}")
            continue
        tone = "praise" if random.random() < praise_chance else "hate"
        if condition_pool and random.random() < 0.30:
            candidates = [msg for msg in condition_pool if msg not in recent_messages]
            if not candidates:
                candidates = condition_pool
            message = random.choice(candidates)
        elif overlive_pool and random.random() < 0.18:
            candidates = [msg for msg in overlive_pool if msg not in recent_messages]
            if not candidates:
                candidates = overlive_pool
            message = random.choice(candidates)
        elif random.random() < 0.18:
            message = random.choice(MICRO_REACTIONS["positive" if tone == "praise" else "negative"])
        else:
            message = choose_message(message_bank, recent_messages, tone)
        recent_messages.append(message)
        print(f"{user}: {message}")


def emit_misc_chat(users, event_key, target_name=None):
    message_bank = build_misc_message_bank(event_key, target_name)
    recent_messages = deque(maxlen=20)
    chosen_users = random.sample(users, min(random.randint(12, 18), len(users)))

    for idx, user in enumerate(chosen_users, 1):
        if idx % random.randint(5, 7) == 0:
            print(f"system_feed: {random.choice(SYSTEM_FEED)}")
            continue
        pool = [msg for msg in message_bank if msg not in recent_messages]
        if not pool:
            pool = message_bank
        message = random.choice(pool)
        recent_messages.append(message)
        print(f"{user}: {message}")


def emit_misc_chat_with_artist(users, event_key, artist, target_name=None, extra_messages=None):
    recent_messages = deque(maxlen=20)
    message_bank = build_misc_message_bank(event_key, target_name)
    if extra_messages:
        message_bank = list(message_bank) + list(extra_messages)
    overlive = int(getattr(artist, "live_count_this_week", 0)) > 3
    chosen_users = random.sample(users, min(live_reaction_count(artist), len(users)))

    for idx, user in enumerate(chosen_users, 1):
        if idx % random.randint(5, 7) == 0:
            print(f"system_feed: {random.choice(SYSTEM_FEED)}")
            continue

        condition_pool = build_condition_pool(artist, target_name)

        if condition_pool and random.random() < 0.35:
            pool = [msg for msg in condition_pool if msg not in recent_messages]
            if not pool:
                pool = condition_pool
            message = random.choice(pool)
        elif overlive and random.random() < 0.18:
            pool = [msg for msg in OVERLIVE_REACTIONS if msg not in recent_messages]
            if not pool:
                pool = OVERLIVE_REACTIONS
            message = random.choice(pool)
        else:
            pool = [msg for msg in message_bank if msg not in recent_messages]
            if not pool:
                pool = message_bank
            message = random.choice(pool)

        recent_messages.append(message)
        print(f"{user}: {message}")


def emit_low_energy_chat(users, artist):
    recent_messages = deque(maxlen=20)
    pool = build_condition_pool(artist)
    chosen_users = random.sample(users, min(max(2, live_reaction_count(artist) // 3), len(users)))
    for user in chosen_users:
        candidates = [msg for msg in pool if msg not in recent_messages]
        if not candidates:
            candidates = pool
        message = random.choice(candidates)
        recent_messages.append(message)
        print(f"{user}: {message}")


def live_viewer_count(artist):
    base = random.randint(80, 650)
    weekly_lives = int(getattr(artist, "live_count_this_week", 0))

    if weekly_lives == 4:
        base = random.randint(45, 150)
    elif weekly_lives == 5:
        base = random.randint(18, 70)
    elif weekly_lives == 6:
        base = random.randint(5, 12)
    elif weekly_lives >= 7:
        base = random.randint(2, 3)

    return max(2, base)


def go_live(artist):
    users = generate_usernames()
    viewers = live_viewer_count(artist)
    fatigue = float(getattr(artist, "fatigue", 0.0))
    health = float(getattr(artist, "health", 100.0))
    weekly_lives = int(getattr(artist, "live_count_this_week", 0))

    print("\nLIVE NOW")
    print(f"Streamer: {artist.name}")
    print(f"Viewers: {viewers}\n")

    if fatigue >= 85 or health <= 35:
        print("The stream opens with low energy. Chat can tell you are tired.\n")
    if weekly_lives > 3:
        print("The room feels thinner than usual and some people are already joking that you go live too much.\n")

    while True:
        print("1. Preview unreleased music")
        print("2. Play released music")
        print("3. Criticize an artist")
        print("4. Criticize a critic")
        print("5. Praise an artist")
        print("6. Praise a critic")
        print("7. End stream")

        choice = input(">>> ").strip()

        if choice == "1":
            options = [
                option for option in available_song_options(artist)
                if not option["released"] or option["label"].startswith("Album track")
            ]
            if options:
                selected = choose_song_option("Choose what to preview", options)
                print(f"\n{artist.name} previews '{selected['song'].name}'.\n")
                emit_chat_for_song(users, attach_artist_context(selected, artist), artist.name)
            else:
                print(f"\n{artist.name} previews an unfinished idea.\n")
                fallback = {
                    "song": type("SongStub", (), {"name": "Untitled Idea", "quality": 4.5})(),
                    "released": False,
                    "average_review": None,
                    "artist": artist,
                }
                emit_chat_for_song(users, fallback, artist.name)

        elif choice == "2":
            options = [option for option in available_song_options(artist) if option["released"]]
            if options:
                selected = choose_song_option("Choose a released song to play", options)
                review_text = (
                    f" | avg review: {selected['average_review']}/10"
                    if selected["average_review"] is not None
                    else ""
                )
                print(f"\n{artist.name} plays '{selected['song'].name}' on stream{review_text}.\n")
                emit_chat_for_song(users, attach_artist_context(selected, artist), artist.name)
            else:
                print(f"\n{artist.name} runs back a released song on stream.\n")
                fallback = {
                    "song": type("SongStub", (), {"name": "Released Track", "quality": 6.0})(),
                    "released": True,
                    "average_review": 6.0,
                    "artist": artist,
                }
                emit_chat_for_song(users, fallback, artist.name)

        elif choice == "3":
            target = choose_target("Choose artist to criticize", ECOSYSTEM_ARTISTS)
            prev_history = list(_get_opinion_history(artist, target))
            memory_lines = _memory_chat_lines(prev_history, "criticize")
            delta, pre_score, _applied = _apply_live_relationship(artist, target, "criticize")
            rel_lines = _relationship_chat_lines("criticize", pre_score)
            history = _get_opinion_history(artist, target)
            history.append("criticize")
            del history[:-3]
            print(f"\n{artist.name} takes a shot at {target} on stream.\n")
            emit_misc_chat_with_artist(
                users,
                "criticize_artist",
                artist,
                target,
                extra_messages=(rel_lines + memory_lines),
            )

        elif choice == "4":
            target = choose_target("Choose critic to criticize", CRITICS)
            print(f"\n{artist.name} calls out {target} on stream.\n")
            emit_misc_chat_with_artist(users, "criticize_critic", artist, target)

        elif choice == "5":
            target = choose_target("Choose artist to praise", ECOSYSTEM_ARTISTS)
            prev_history = list(_get_opinion_history(artist, target))
            memory_lines = _memory_chat_lines(prev_history, "praise")
            delta, pre_score, _applied = _apply_live_relationship(artist, target, "praise")
            rel_lines = _relationship_chat_lines("praise", pre_score)
            history = _get_opinion_history(artist, target)
            history.append("praise")
            del history[:-3]
            print(f"\n{artist.name} gives respect to {target}.\n")
            emit_misc_chat_with_artist(
                users,
                "praise_artist",
                artist,
                target,
                extra_messages=(rel_lines + memory_lines),
            )

        elif choice == "6":
            target = choose_target("Choose critic to praise", CRITICS)
            print(f"\n{artist.name} gives credit to {target} on stream.\n")
            emit_misc_chat_with_artist(users, "praise_critic", artist, target)

        elif choice == "7":
            print(f"\n{artist.name} ends the stream.\n")
            break

        else:
            print("Invalid choice.")


def main():
    class _ArtistStub:
        def __init__(self):
            self.name = input("Artist name: ").strip() or "Untitled Artist"
            self.singles = []
            self.albums = []

    go_live(_ArtistStub())


if __name__ == "__main__":
    main()
