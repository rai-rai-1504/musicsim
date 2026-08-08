import random

# ─────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────

GENRES = [
    "pop", "hip hop", "rock", "jazz", "classical",
    "electronic", "r&b", "metal", "country", "reggae",
    "folk", "blues", "punk", "soul", "experimental"
]

THEMES = [
    "heartbreak", "party", "protest", "nostalgia", "love",
    "existential", "street life", "spirituality", "rage", "euphoria"
]

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def pick(options):
    return random.choice(options)

def picks(options, n=2):
    """Pick n unique lines from a pool."""
    return " ".join(random.sample(options, min(n, len(options))))

def clamp(val, lo=0, hi=10):
    return max(lo, min(hi, round(val, 1)))

def bias_scale(quality):
    """Returns a multiplier (0–1) that shrinks bias as quality approaches 10.
    At quality 10, bias is reduced to ~10% of normal.
    At quality 8–9, bias is ~40–60%.
    Below 7, full bias applies."""
    if quality >= 10:
        return 0.10
    if quality >= 9:
        return 0.30
    if quality >= 8:
        return 0.50
    return 1.0

# ─────────────────────────────────────────────
#  VERDICTS  (per integer 0–10)
# ─────────────────────────────────────────────

VERDICTS = {
    # critic_type → {score: [possible verdicts]}
    "elitist": {
        0:  ["an insult to the art form — I'd rather listen to silence",
             "I've heard better sound design from a broken microwave",
             "this is what musical bankruptcy sounds like"],
        1:  ["barely a song — more of an accident that got recorded",
             "one step above silence, and silence was winning",
             "someone let this out of the studio and I want answers"],
        2:  ["a catastrophic misfire from start to finish",
             "there are students in their first week who've made better",
             "deeply, profoundly mediocre — in the worst direction"],
        3:  ["I've heard more exciting music in elevator lobbies",
             "it exists. that's about the nicest thing I can say",
             "a disappointment that manages to be boring on top of it"],
        4:  ["formulaic, derivative, and uninspired — but technically a song",
             "it checks boxes without understanding why those boxes exist",
             "passable in the most clinical, joyless sense of the word"],
        5:  ["neither offensive nor interesting — true mediocrity achieved",
             "five out of ten: the beige wall of music scores",
             "it's there. it plays. it ends. nothing is gained or lost"],
        6:  ["there are flashes of something real buried under the baggage",
             "above average, but only just — and it knows it",
             "a six is not a compliment from me, just so we're clear"],
        7:  ["genuinely decent — and I'm saying that through gritted teeth",
             "it works more than it doesn't, which is more than I expected",
             "a seven is a solid record. not exciting, but solid"],
        8:  ["I'm reluctantly impressed — this is actually good",
             "sharp, considered, and well-executed — an eight is earned here",
             "this one got under my skin in the best way"],
        9:  ["I'm not often moved, but this came close — exceptional work",
             "this is the kind of track that makes the job worth doing",
             "a near-perfect record — whatever's missing is barely a shadow"],
        10: ["I've waited years to give a ten and I refuse to give it lightly — this earned it",
             "a masterpiece. full stop. this is what music is supposed to be",
             "I am floored. genuinely floored. a perfect ten, and I mean every decimal of it"],
    },
    "hype": {
        0:  ["okay it's not great but we can work with this energy!",
             "a rocky start but every legend has one, right?",
             "the vibe wasn't there but the passion clearly is"],
        1:  ["rough around every edge but hey, we've all been there",
             "not the debut I'd hoped for but there's still a pulse",
             "honestly brave for putting it out — growth starts somewhere"],
        2:  ["struggling, but I see the blueprint in there somewhere",
             "messy and off-target, but not without some spark",
             "it's a tough listen, I won't lie, but it's not hopeless"],
        3:  ["below expectations but not beyond saving",
             "there are seeds of something worth nurturing here",
             "a stumble, not a fall — get back up and try again"],
        4:  ["decent enough that I'm not worried about the future",
             "it's got its moments even if the whole isn't clicking yet",
             "four out of ten but trending upward — that's the energy"],
        5:  ["perfectly fine and I mean that with warmth, not shade",
             "right in the middle and honestly? that's a foundation",
             "a solid five — not a crown, but not a tombstone either"],
        6:  ["genuinely good in chunks — the ceiling here is high",
             "this is a six that could easily become an eight with polish",
             "I like where this is going — keep that momentum"],
        7:  ["really solid! this is music I'd actually put on",
             "a strong seven — confident, competent, and fun to listen to",
             "this is the kind of track that builds an audience"],
        8:  ["okay THIS is what I'm talking about — strong eight!",
             "eight out of ten and it deserved every point",
             "this is legitimately great and I'm not holding back on that"],
        9:  ["I am almost screaming right now — this is phenomenal",
             "a nine! and a deserved one! this is the real deal",
             "this track is going to live in my head for weeks, easy"],
        10: ["STOP EVERYTHING. this is a ten. a perfect ten. I am not calm about this",
             "I don't give tens. I just gave a ten. that's how good this is",
             "a flawless record — I want everyone on earth to hear this immediately"],
    },
    "academic": {
        0:  ["structurally incoherent and thematically void — no redeeming compositional merit",
             "this fails on virtually every evaluative axis I apply",
             "there is nothing here to analyze — and that itself is a finding"],
        1:  ["the craft is absent and the execution compounds that absence",
             "one point is awarded for completion — the rest cannot be justified",
             "technically a piece of music; analytically, barely"],
        2:  ["the framework is present but unsupported by any meaningful execution",
             "two points reflect the effort invested, not the results achieved",
             "there is conceptual intent here but no follow-through"],
        3:  ["below the threshold of noteworthy but not without marginal value",
             "the score reflects structural dysfunction paired with occasional clarity",
             "a three indicates a work that knows what it wants but cannot deliver it"],
        4:  ["competent in isolated moments — the aggregate disappoints",
             "four suggests a work in transition: capable, but unresolved",
             "there is discipline in parts; the whole remains unconvincing"],
        5:  ["precisely average by design or by accident — the outcome is identical",
             "a five is not a failing grade, but it is not an endorsement",
             "technically proficient, thematically adequate — middling by every measure"],
        6:  ["above average in structure; the thematic execution elevates it moderately",
             "a six reflects genuine craft applied with inconsistent intention",
             "the work demonstrates control — it lacks only ambition"],
        7:  ["a well-constructed record with clear artistic intent and reliable execution",
             "seven is earned: the compositional logic holds and the themes are cohesive",
             "this rewards close listening — a mark of considered artistry"],
        8:  ["an eight reflects a record that succeeds on nearly every evaluative criterion",
             "the structural and thematic elements here are exceptional — a rare result",
             "this is the kind of work that sustains repeated critical engagement"],
        9:  ["I find myself returning to this record analytically and emotionally — a nine",
             "the craft here is exceptional; the intent is realized with extraordinary precision",
             "this stands as a benchmark — a nine is not given lightly in this framework"],
        10: ["a perfect score demands perfect justification: this record provides it",
             "I have revised my evaluative rubric in light of this work — a genuine ten",
             "compositionally, thematically, emotionally: a ten across every axis I possess"],
    },
    "contrarian": {
        0:  ["everyone's going to hate this — and they're probably right, for once",
             "I'd usually defend the underdog but there's nothing here to defend",
             "even I can't spin this — it's genuinely not good"],
        1:  ["the mainstream will ignore this and, on this occasion, correctly so",
             "a one, and I say that without any pleasure",
             "there's no hidden depth here, just audible absence"],
        2:  ["it's bad, but not interestingly bad — that's worse",
             "I wanted to find something overlooked here. I found nothing.",
             "a two: below the curve and not for any good reason"],
        3:  ["misunderstood? no. just underdeveloped. there's a difference.",
             "I try to find what critics miss — I'm not finding it here",
             "a three, and I'm not being unfair to the mainstream for once"],
        4:  ["there's something here most people will walk past, but not enough of it",
             "a four that contains a six trying to get out",
             "the interesting parts are outnumbered by the safe ones"],
        5:  ["a five masquerading as consensus — but it's genuinely average, not secretly good",
             "five out of ten: I looked for the hidden gem and found a pebble",
             "I don't think the crowd is wrong on this one, unfortunately"],
        6:  ["a six that most will underrate — there's more going on than it seems",
             "critics will be lukewarm; listeners who dig deeper will be rewarded",
             "six, and I suspect this one gets reassessed in a few years"],
        7:  ["a seven that I think most are sleeping on — this deserves more attention",
             "popular opinion will probably land this lower. popular opinion is wrong.",
             "a genuinely good track that mainstream discourse will under-celebrate"],
        8:  ["everyone else will say seven. I'm saying eight, and I'm right.",
             "this will be slept on and it shouldn't be — an eight without question",
             "a polarizing record for most, but the eight is justified on close inspection"],
        9:  ["the discourse will be divided. the record is not. this is a nine.",
             "people will argue about this one. they shouldn't — it's exceptional.",
             "a nine that the critical establishment won't know what to do with"],
        10: ["history will remember this differently than the present does — a perfect ten",
             "the consensus will catch up eventually. for now: a ten, period.",
             "I've been called contrarian my whole career. this time I'm calling it first: masterpiece."],
    },
    "nostalgic": {
        0:  ["nothing here reminds me of why I fell in love with music in the first place",
             "the greats would weep — and not with joy",
             "I've been listening to music for decades and this adds nothing to that story"],
        1:  ["a one. not because I'm harsh, but because this lacks all soul",
             "there's no heart here — the old records had nothing but heart",
             "this sounds like music made by someone who has never been moved by music"],
        2:  ["the classics set a standard this doesn't come close to",
             "two points for effort — the golden era would ask for a refund",
             "music used to mean something. this is a reminder of what's been lost"],
        3:  ["it has the shape of music but not the feeling",
             "there are moments — brief, flickering — that suggest it could have been more",
             "a three: not without charm, but without the depth that made the greats"],
        4:  ["passable in a contemporary sense — but it doesn't hold a candle to the catalog",
             "four out of ten: it'll be forgotten, and that's a shame",
             "some producers today still know how to make something lasting. this isn't it"],
        5:  ["a five — right down the middle, like a lot of music made these days",
             "neither embarrassing nor memorable: the fate of many good-enough records",
             "five, with the caveat that five was harder to achieve in better years"],
        6:  ["a six and I mean it warmly — there's genuine feeling here",
             "this one reminds me, just a little, of the music that mattered",
             "six out of ten: a record that knows something about soul, even if it's still learning"],
        7:  ["now we're talking — this has something real in it",
             "a seven that would have made the old guard nod",
             "this one transported me, briefly. that matters. seven."],
        8:  ["an eight — and it moved me in a way I haven't felt in a while",
             "this is the kind of record that reminds you why music exists",
             "eight out of ten: timeless energy in a modern vessel"],
        9:  ["I haven't felt this way about a new record in years — a nine, without hesitation",
             "this is the real thing. I'd put it next to the classics and it holds",
             "a nine. genuine, warm, and full of the soul that music is built on"],
        10: ["I cried. not from sadness — from recognition. this is a ten.",
             "this is the record I've been waiting for since the golden age ended. a perfect ten.",
             "a ten. a masterpiece. this belongs in the same breath as the greats — and I've heard the greats."],
    },
    "scenes": {
        0:  ["the underground wouldn't touch this with a ten-foot pole",
             "this doesn't represent any scene I'd want to be part of",
             "zero cultural currency — this is background noise for chain restaurants"],
        1:  ["one point because it technically qualifies as a release",
             "the scene deserves better than this — the scene always does",
             "this is music for people who don't care about music"],
        2:  ["it's not authentic to anything — and inauthenticity is the cardinal sin",
             "two points: it gestures at a culture it clearly doesn't understand",
             "whoever made this has never been to a show in their life"],
        3:  ["there's something almost real buried in here, but almost doesn't cut it",
             "three — I can hear the influence but not the understanding",
             "the aesthetic is borrowed; the soul is missing"],
        4:  ["the community would be lukewarm, and fairly so",
             "four: it's engaging the right traditions but not adding to them",
             "there's respect for the form here — but respect alone doesn't cut it"],
        5:  ["right in the middle of what the scene expects — no more, no less",
             "a five: present, competent, and unlikely to start any conversations",
             "it fits in. fitting in is not a compliment in this world"],
        6:  ["a six from the underground is a quiet recommendation",
             "this would earn nods at the right shows — that counts for something",
             "six: above the waterline, with room to grow into something special"],
        7:  ["this is the real deal — the scene would embrace it",
             "a seven: authentic, sharp, and culturally literate",
             "the heads would know. and they'd approve."],
        8:  ["an eight — this is the kind of record that builds movements",
             "this is going to be talked about in the right circles for a long time",
             "eight: this has the energy of something genuinely important"],
        9:  ["a nine — underground classic territory. this is the real thing.",
             "this is the record that scene kids will reference in five years",
             "the pulse of something vital — I haven't felt this in a minute. nine."],
        10: ["a ten. this is the record the underground was waiting for.",
             "when I tell people about the records that changed everything, this will be on the list. ten.",
             "a perfect ten — this is the kind of music that makes scenes worth belonging to"],
    },
    "casual": {
        0:  ["I tried to get through it. I really did.",
             "my speakers almost apologized to me",
             "I don't want to be mean but I also can't pretend I enjoyed this"],
        1:  ["not for me — and I like a lot of things",
             "there's something not connecting here and I can't quite name it",
             "I kept waiting for it to click. it never did"],
        2:  ["it's rough, and not in the fun way",
             "two out of ten — I kept checking how much was left",
             "some moments had potential but it didn't go anywhere I wanted to follow"],
        3:  ["I've heard worse but I've also heard a lot better",
             "a three — it didn't offend me, but it didn't interest me either",
             "there are songs I forget and songs I actively try to forget. this is the latter"],
        4:  ["not bad exactly, just kind of... there",
             "four out of ten: it occupied some minutes of my life without much return",
             "it's pleasant background noise if you're doing something else"],
        5:  ["a solid five — I didn't skip it, and that's not nothing",
             "I'd probably let it play if it came on shuffle",
             "five: I liked it fine while it was on and forgot it immediately after"],
        6:  ["actually pretty good — I'd voluntarily play this again",
             "a six and I mean it — this genuinely caught my attention",
             "I caught myself bobbing my head. that's a real six."],
        7:  ["okay this one I actually liked — a good seven",
             "I texted this to someone while I was listening. that's a seven",
             "seven out of ten: this is going in the rotation"],
        8:  ["really good — like, genuinely good, I'm not just saying that",
             "an eight and I'd recommend this without hesitation",
             "this one's getting repeated listens from me, easy"],
        9:  ["this is just great music and I'm saying that simply",
             "a nine — it made me feel something and that's the whole point",
             "I've had this on repeat and I'm not even slightly embarrassed about it"],
        10: ["okay this is genuinely one of the best things I've heard in ages",
             "a ten and I don't care how enthusiastic that sounds — listen to it",
             "I can't stop thinking about this record. that's a ten. easy."],
    },
}

# ─────────────────────────────────────────────
#  SONG MODEL
# ─────────────────────────────────────────────

class Song:
    def __init__(self, quality, name=None, genres=None, theme=None, duration=None):
        self.quality = quality
        self.name = name
        self.genres = genres or []      # list of 1 or 2 genres
        self.theme = theme
        self.duration = duration

    @property
    def primary_genre(self):
        return self.genres[0] if self.genres else None

    @property
    def is_blend(self):
        return len(self.genres) == 2

    def genre_label(self):
        if self.is_blend:
            return f"{self.genres[0]}/{self.genres[1]} blend"
        return self.genres[0]

# ─────────────────────────────────────────────
#  BASE CRITIC
# ─────────────────────────────────────────────

class Critic:
    name = "Critic"
    tagline = ""
    verdict_type = "elitist"

    # genres this critic loves (bonus), dislikes (penalty), severely dislikes (big penalty)
    loved_genres = []
    liked_genres = []
    disliked_genres = []
    hated_genres = []

    loved_themes = []
    disliked_themes = []

    base_modifier = 0       # flat score shift for this critic's general disposition

    def genre_lines(self, song):
        """Return 2 lines about the genre(s)."""
        raise NotImplementedError

    def theme_lines(self, song):
        """Return 1–2 lines about the theme."""
        raise NotImplementedError

    def duration_lines(self, song):
        """Return 1 line about duration."""
        raise NotImplementedError

    def compute_score(self, song):
        score = song.quality
        scale = bias_scale(song.quality)

        for g in song.genres:
            if g in self.loved_genres:
                score += 2 * scale
            elif g in self.liked_genres:
                score += 1 * scale
            elif g in self.hated_genres:
                score -= 3 * scale
            elif g in self.disliked_genres:
                score -= 2 * scale

        if song.theme in self.loved_themes:
            score += 1.5 * scale
        elif song.theme in self.disliked_themes:
            score -= 1.5 * scale

        score += self.base_modifier * scale
        return clamp(score)

    def get_verdict(self, score):
        key = int(round(score))
        key = max(0, min(10, key))
        pool = VERDICTS[self.verdict_type].get(key, ["it is what it is"])
        return pick(pool)

    def review(self, song):
        score = self.compute_score(song)
        genre_part = self.genre_lines(song)
        theme_part = self.theme_lines(song)
        dur_part = self.duration_lines(song)
        verdict = self.get_verdict(score)

        all_sentences = genre_part + theme_part + dur_part
        random.shuffle(all_sentences)
        body = " ".join(all_sentences)
        final = f"{body} {verdict} — {score}/10."

        return score, final


# ─────────────────────────────────────────────
#  CRITIC 1 — MARCUS VANE  (Elitist, Experimental/Jazz/Classical snob)
# ─────────────────────────────────────────────

class MarcusVane(Critic):
    name = "Marcus Vane"
    tagline = "Senior Editor, The Æsthetic Review"
    verdict_type = "elitist"

    loved_genres    = ["experimental", "jazz", "classical"]
    liked_genres    = ["folk", "blues", "soul"]
    disliked_genres = ["country", "reggae"]
    hated_genres    = ["pop", "electronic"]

    loved_themes    = ["existential", "spirituality", "protest"]
    disliked_themes = ["party", "euphoria"]

    base_modifier = -1.5

    def genre_lines(self, song):
        g = song.genre_label()
        pools = {
            "experimental": [
                f"the experimental framework here is genuinely ambitious — rare to see someone commit this fully",
                f"structurally, this is adventurous in ways that most artists avoid out of commercial fear",
                f"it pushes against convention without announcing that it's doing so, which is the mark of real craft",
                f"the willingness to destabilize expectation is the most interesting thing about this record",
            ],
            "jazz": [
                f"the jazz sensibility gives this genuine harmonic depth — you can hear the lineage",
                f"the improvised spaces breathe in ways pre-composed music simply cannot replicate",
                f"it draws on the tradition without being enslaved to it — that balance is difficult to achieve",
                f"the jazz architecture here rewards repeated listening, which is all I ask of music",
            ],
            "classical": [
                f"the classical influence lends it a structural coherence rarely found in contemporary work",
                f"you can hear a composer's mind at work here, and that is not a compliment I give lightly",
                f"the form serves the content — a classical principle applied with obvious understanding",
                f"the orchestral logic underlying this is exactly what modern music has been neglecting",
            ],
            "pop": [
                f"pop, as a genre, has produced one original idea per decade — this is not that idea",
                f"everything about the pop framing here is designed to make you stop thinking, and it succeeds",
                f"the {g} approach reduces whatever potential this had to a product for passive consumption",
                f"I find pop's insistence on pleasantness to be its most dishonest quality — and this is textbook pop",
            ],
            "electronic": [
                f"the electronic production substitutes texture for substance — a common and tiresome substitution",
                f"synthesizers are tools, not ideas — this track mistakes one for the other",
                f"the {g} framework gives the illusion of innovation while doing nothing genuinely new",
                f"electronic music at its best interrogates sound. this simply deploys it.",
            ],
        }
        for gname in song.genres:
            if gname in pools:
                return [picks(pools[gname], 2)]
        return [pick([
            f"as a {g} release, it occupies its genre without transcending it",
            f"the {g} direction is serviceable but offers no new vocabulary",
            f"I'm familiar with what {g} can achieve at its ceiling — this is not that ceiling",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "existential": [
                "the existential undertow here is the record's most compelling quality",
                "grappling with the void is the oldest tradition in art — and this earns its place in it",
                "it sits with difficult questions rather than resolving them, which is the honest approach",
            ],
            "spirituality": [
                "the spiritual dimension adds genuine weight to what might otherwise be merely sonically interesting",
                "it approaches transcendence without becoming either preachy or vague — a difficult balance",
                "the sense of the sacred here is earned, not performed",
            ],
            "party": [
                "a party theme is, by design, a refusal to mean anything — and this delivers on that refusal",
                "there is nothing wrong with hedonism in life. in art, it requires more justification than this provides.",
                "the festive framing drains whatever intellectual potential the record hinted at",
            ],
            "euphoria": [
                "euphoria as a theme tends to produce music that refuses to cost the listener anything — this is no exception",
                "the emotional terrain here is deliberately shallow, which is a creative choice I struggle to respect",
            ],
            "protest": [
                "protest music is at its best when it is uncomfortable — this track does not shy away from that discomfort",
                "the political dimension here is handled with nuance rather than sloganeering — that's admirable",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme is functional but doesn't add a layer I find particularly arresting",
            f"thematically, this neither elevates nor diminishes the record — it simply is",
            f"the {t} direction is handled adequately without distinction",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 360:
            return [pick([
                "the extended runtime is justified — it takes the time it needs and not a second more",
                "at this length, a weaker record would collapse — it holds, which is a genuine achievement",
            ])]
        if d > 240:
            return [pick([
                "the duration is measured and appropriate — it does not overstay its welcome",
                "the runtime reflects compositional discipline, which I always appreciate",
            ])]
        if d < 120:
            return [pick([
                "at this length, nothing can breathe — and this needed room to breathe",
                "the brevity feels like a refusal to commit to anything, which is its own artistic failure",
            ])]
        return [pick([
            "the runtime is neither a virtue nor a flaw here — it simply accommodates the material",
        ])]


# ─────────────────────────────────────────────
#  CRITIC 2 — DEJA HAYES  (Hype Queen, Pop/R&B/Soul enthusiast)
# ─────────────────────────────────────────────

class DejaHayes(Critic):
    name = "Deja Hayes"
    tagline = "Founder, PulseLine Media"
    verdict_type = "hype"

    loved_genres    = ["pop", "r&b", "soul"]
    liked_genres    = ["hip hop", "electronic", "reggae"]
    disliked_genres = ["metal", "classical"]
    hated_genres    = ["punk", "experimental"]

    loved_themes    = ["love", "party", "euphoria"]
    disliked_themes = ["rage", "existential"]

    base_modifier = 1.5

    def genre_lines(self, song):
        g = song.genre_label()
        pools = {
            "pop": [
                f"a pop record that actually knows what pop is for — immediate, infectious, unapologetic",
                f"this is pop doing what pop does best: making you feel something fast and keeping you there",
                f"the pop construction here is sharp and intentional — every hook lands exactly where it should",
                f"there's a reason pop is the most listened-to genre on earth and this is a good example of why",
            ],
            "r&b": [
                f"the r&b DNA runs deep here and it shows in every melodic choice",
                f"this is smooth in the right ways — the groove is undeniable",
                f"there's an emotional warmth to this r&b approach that really works",
                f"the r&b tradition is well-served here — it adds feeling without sacrificing momentum",
            ],
            "soul": [
                f"the soul influences here give it a texture that a lot of modern music is too afraid to reach for",
                f"genuine soul is rare and this has it — you can hear that the artist actually felt something",
                f"the soulful elements lift this from good to something that might actually last",
            ],
            "metal": [
                f"the metal direction is going to turn a lot of people off and honestly, I'm in that group",
                f"metal has its place but that place is not really here for me personally",
                f"the heaviness works against the emotional accessibility I look for",
            ],
            "punk": [
                f"the punk framing is aggressive in a way that doesn't translate to how I receive music",
                f"punk energy can be exciting but this is more abrasive than it is compelling",
                f"not my lane at all — the {g} approach creates distance where I want connection",
            ],
            "experimental": [
                f"experimental as a tag covers a lot of ground — this lands on the harder-to-love end of it",
                f"the unconventional structure makes it challenging to connect with emotionally",
                f"it's interesting in theory but music needs to feel good too, and this misses that for me",
            ],
        }
        for gname in song.genres:
            if gname in pools:
                return [picks(pools[gname], 2)]
        return [pick([
            f"as a {g} track it's serving its purpose pretty well",
            f"the {g} energy is there — I can hear what they were going for",
            f"this fits the {g} space even if it doesn't redefine it",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "love": [
                "love as a theme is a classic for a reason and this handles it well",
                "the love narrative here hits the right emotional notes without being saccharine",
                "when love themes are done right they're universal — this one connects",
            ],
            "party": [
                "the party energy is immaculate — this is what playlists are built around",
                "I felt this one physically and that's the whole point of a party track",
                "the festive theme is executed with the kind of joyful confidence this genre deserves",
            ],
            "euphoria": [
                "the euphoric feeling here is infectious in the best way",
                "music that makes you feel good is underrated as a form — this is a great example",
                "pure feel-good energy that doesn't apologize for existing and shouldn't have to",
            ],
            "rage": [
                "the rage theme creates an emotional barrier I don't love to push through",
                "I get it, but I personally need my music to lift me up more than this does",
            ],
            "existential": [
                "existential themes can be powerful but they weigh this down when it could soar",
                "the heaviness of the theme pulls against the musical momentum in ways that frustrate me",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme lands well emotionally — it gives the track a clear identity",
            f"the {t} direction is relatable and that matters a lot to me",
            f"thematically it resonates in the way good music should",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick([
                "the length is a little much — I start to lose focus past a certain point",
                "trimming this would have made the energy hit harder throughout",
            ])]
        if d < 150:
            return [pick([
                "short and punchy — I actually love when a song doesn't overstay its welcome",
                "the brevity works in its favour — it leaves you wanting more",
            ])]
        return [pick([
            "the runtime is right in the sweet spot — keeps you engaged without losing you",
            "it's the perfect length to get in, deliver, and get out",
        ])]


# ─────────────────────────────────────────────
#  CRITIC 3 — DR. PRIYA SOLAN  (Academic, Theory-First)
# ─────────────────────────────────────────────

class DrPriyaSolan(Critic):
    name = "Dr. Priya Solan"
    tagline = "Associate Professor of Musicology, Eastbridge University"
    verdict_type = "academic"

    loved_genres    = ["classical", "jazz", "folk"]
    liked_genres    = ["blues", "experimental", "soul"]
    disliked_genres = ["electronic", "punk"]
    hated_genres    = ["pop", "country"]

    loved_themes    = ["protest", "spirituality", "existential", "nostalgia"]
    disliked_themes = ["party", "euphoria"]

    base_modifier = -0.5

    def genre_lines(self, song):
        g = song.genre_label()
        pools = {
            "classical": [
                f"the classical framework provides a structural integrity that supports the compositional ambition",
                f"the formal logic here is well-applied — the architecture serves the emotional arc effectively",
                f"drawing from classical tradition is a risk; this record handles it with appropriate rigor",
            ],
            "jazz": [
                f"the jazz influences inform a harmonic vocabulary that elevates the melodic material considerably",
                f"the improvisational latitude here is used judiciously — a sign of genuine musicianship",
                f"the jazz sensibility opens this up in ways that straight compositional approaches would close off",
            ],
            "folk": [
                f"the folk tradition brings a narrative integrity that anchors the lyrical and melodic content",
                f"this engages the folk canon with both respect and critical distance — a mature approach",
            ],
            "pop": [
                f"the pop genre operates within a rigidly constrained formal vocabulary that this record does not transcend",
                f"from a compositional standpoint, the pop structure imposes limitations that are clearly felt in the result",
                f"the generic conventions of pop are reproduced here without meaningful interrogation",
            ],
            "country": [
                f"the country genre's structural and lyrical conventions are well-documented and this does not deviate from them",
                f"from a musicological perspective, the country framing limits the scope of what this can achieve",
            ],
        }
        for gname in song.genres:
            if gname in pools:
                return [picks(pools[gname], 2)]
        return [pick([
            f"the {g} genre is executed with technical proficiency if not exceptional distinction",
            f"within the parameters of {g}, this achieves adequate formal coherence",
            f"the {g} classification is appropriate and the compositional choices align with it consistently",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "protest": [
                "the protest tradition in music is one of its most vital and this engages it meaningfully",
                "the socio-political content here is handled with the nuance the subject matter demands",
            ],
            "spirituality": [
                "the spiritual dimension introduces a transcendent register that elevates the thematic scope",
                "engaging with the sacred in music requires delicacy — this record understands that",
            ],
            "existential": [
                "the existential content provides a philosophical depth that distinguishes this from its contemporaries",
                "questions of meaning and mortality have driven music's most significant works — this earns its place in that discourse",
            ],
            "nostalgia": [
                "nostalgia as a thematic mode is complex — this navigates it without collapsing into mere sentimentality",
                "the historical consciousness embedded in the nostalgic theme adds a layered interpretive dimension",
            ],
            "party": [
                "the festive theme, while culturally coherent, offers limited analytical traction",
                "thematically, the celebratory mode constrains the compositional and lyrical ambition of the work",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme is rendered with competence — it supports without overwhelming the structural elements",
            f"the thematic content aligns functionally with the musical choices without producing exceptional synergy",
            f"the {t} direction is a reasonable selection given the genre framing and is executed accordingly",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 360:
            return [pick([
                "the extended duration allows for appropriate thematic and structural development",
                "a longer form demands greater compositional stamina — this largely meets that demand",
            ])]
        if d < 120:
            return [pick([
                "the brevity constrains the development of the thematic material to a degree that diminishes the whole",
                "at this duration, there is insufficient space for the compositional ideas to reach maturity",
            ])]
        return [pick([
            "the duration is proportionate to the material's requirements — neither excessive nor curtailed",
            "the runtime reflects sound structural judgment",
        ])]


# ─────────────────────────────────────────────
#  CRITIC 4 — RAY COLDWELL  (Contrarian, reads against the grain)
# ─────────────────────────────────────────────

class RayColdwell(Critic):
    name = "Ray Coldwell"
    tagline = "Independent Critic, The Cold Take"
    verdict_type = "contrarian"

    loved_genres    = ["punk", "experimental", "metal", "blues"]
    liked_genres    = ["folk", "hip hop", "jazz"]
    disliked_genres = ["pop", "reggae"]
    hated_genres    = ["r&b", "country"]

    loved_themes    = ["rage", "protest", "existential"]
    disliked_themes = ["love", "euphoria", "party"]

    base_modifier = 0

    def genre_lines(self, song):
        g = song.genre_label()
        pools = {
            "punk": [
                "the punk rawness is the most honest thing about this record and I mean that seriously",
                "punk has no patience for pretense and neither do I — this scores points for that",
                "the {g} energy is confrontational in a way most music is too cowardly to attempt",
            ],
            "experimental": [
                "experimental music rewards listeners willing to meet it halfway — most critics aren't",
                "the unconventional approach is going to alienate the mainstream, which is kind of the point",
                "the {g} framing invites misreading; a close listen reveals more intentionality than most will credit",
            ],
            "metal": [
                "metal is unfairly dismissed by critics who confuse loudness with thoughtlessness",
                "the {g} intensity is deployed with craft — more discipline here than it gets credit for",
                "heavy music makes reviewers uncomfortable and that discomfort often shows up as negative scores. I won't do that.",
            ],
            "r&b": [
                "r&b's emotional vocabulary has become so codified that most releases within it say nothing new",
                "the {g} genre is coasting on its cultural capital here rather than contributing to it",
                "I find the smoothness of r&b to be a form of evasion — this record doesn't escape that criticism",
            ],
            "country": [
                "country music has been strip-mined by Nashville for decades and this carries that legacy",
                "the {g} framing brings all the baggage of a genre that traded its soul for chart positions",
            ],
            "pop": [
                "mainstream pop is the only genre where being unchallenging is treated as a virtue",
                "the {g} approach is a set of decisions designed to remove friction — which is the opposite of art",
                "I'm not anti-pop on principle but I am anti-music-that-refuses-to-ask-anything-of-you",
            ],
        }
        for gname in song.genres:
            if gname in pools:
                formatted = [s.replace("{g}", g) for s in pools[gname]]
                return [picks(formatted, 2)]
        return [pick([
            f"the {g} direction isn't one I'd champion but I can assess it on its own terms",
            f"as a {g} track it delivers what the genre asks for — whether the genre asks for the right things is another question",
            f"the {g} framework contains this in ways I find limiting but it works within those limits",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "rage": [
                "rage as a theme is underrepresented in critical discourse and overrepresented in lived experience — this is valid",
                "the anger here is channeled into music rather than dissipated, which is a legitimate artistic choice",
            ],
            "protest": [
                "protest music is the genre's conscience and this respects that tradition",
                "the political content is handled directly rather than metaphorically — I respect that choice",
            ],
            "existential": [
                "existential music refuses easy comfort and that refusal is the most honest stance an artist can take",
                "the philosophical weight here is handled without the self-seriousness that usually sinks this territory",
            ],
            "love": [
                "love songs have been so exhausted as a form that writing one now requires genuine justification",
                "the emotional terrain is familiar and this offers little reason to explore it again",
            ],
            "party": [
                "party music is an entire genre dedicated to avoiding interiority — I find that philosophically suspect",
                "the festive theme signals an active refusal to mean anything, which I can't fully endorse",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme is handled more carefully than most critics will notice",
            f"there's more going on thematically than the surface read suggests — the {t} angle rewards attention",
            f"the {t} direction is interesting precisely because it's not the obvious choice for this genre",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick([
                "the long runtime will lose most listeners — the right listeners will be rewarded",
                "it demands patience, which most modern audiences lack, and this is not entirely the track's fault",
            ])]
        if d < 150:
            return [pick([
                "the brevity is a form of confidence — it says what it has to say and leaves",
                "in a world of bloated runtimes, the compact length is a quiet act of respect",
            ])]
        return [pick([
            "the runtime is the least interesting thing about this record, in either direction",
            "three minutes of something good beats six minutes of something fine — it threads that needle",
        ])]


# ─────────────────────────────────────────────
#  CRITIC 5 — EARL MOSELY  (Nostalgic, lives in the golden era)
# ─────────────────────────────────────────────

class EarlMosely(Critic):
    name = "Earl Mosely"
    tagline = "Columnist, 57 Years in Music"
    verdict_type = "nostalgic"

    loved_genres    = ["blues", "soul", "jazz", "folk", "r&b"]
    liked_genres    = ["rock", "country", "classical"]
    disliked_genres = ["electronic", "hip hop"]
    hated_genres    = ["experimental", "metal"]

    loved_themes    = ["nostalgia", "heartbreak", "spirituality", "love"]
    disliked_themes = ["rage", "street life", "euphoria"]

    base_modifier = -0.5

    def genre_lines(self, song):
        g = song.genre_label()
        pools = {
            "blues": [
                "the blues tradition carries more human truth per note than almost anything else in music — and this understands that",
                "you can hear the lineage here, from the Delta forward, and it's treated with appropriate reverence",
                "blues is about feeling the weight of things and this record doesn't run from that weight",
            ],
            "soul": [
                "real soul is about the transmission of genuine emotion — this has it in abundance",
                "this reminds me of why soul music changed everything when it arrived, and that's not a small thing",
                "the soulfulness here is not performed — it's felt, and the difference is audible",
            ],
            "jazz": [
                "the jazz influence brings an intelligence to the record that rewards the attentive listener",
                "there's a conversation happening here between the instruments that jazz uniquely enables",
            ],
            "folk": [
                "folk music at its best carries the weight of memory and place — this one does",
                "the storytelling tradition in folk is alive in this record in a way I find deeply moving",
            ],
            "electronic": [
                "I've been around long enough to remember when music required human hands to make it",
                "the electronic production puts a pane of glass between the listener and the feeling — I've never made peace with that",
                "the technology here is impressive. the soul, less so.",
            ],
            "metal": [
                "I've tried to understand metal for fifty years. I've made my peace with not getting there.",
                "the aggression here is technically accomplished but emotionally inaccessible to me — and I've lived through things that should make me understand rage",
                "this is a genre that seems designed to exclude me personally",
            ],
            "experimental": [
                "in my experience, experimental usually means the musician has stopped caring whether anyone else connects with the work",
                "I've heard experimental music that moved me. this is not that.",
            ],
            "hip hop": [
                "hip hop has produced some of the most vital records of the last forty years and I am willing to say that even though it's not my language",
                "the hip hop tradition here is handled with confidence even if it's not the world I grew up in",
            ],
        }
        for gname in song.genres:
            if gname in pools:
                return [picks(pools[gname], 2)]
        return [pick([
            f"as a {g} record it holds up to the traditions I care about — mostly",
            f"the {g} direction connects to the lineage of music that has mattered to me, which counts for something",
            f"I've heard {g} done better and I've heard it done worse — this is somewhere in the honest middle",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "nostalgia": [
                "nostalgia done right isn't self-pity — it's a reckoning with what was real and what was lost, and this achieves that",
                "the nostalgic theme resonates in ways that feel personally honest — good music does that",
            ],
            "heartbreak": [
                "heartbreak has driven more great music than any other human experience and this earns its place in that canon",
                "the emotional truth of heartbreak is handled here without sentimentality — that takes skill and lived experience",
            ],
            "spirituality": [
                "music and the sacred have always been connected and this track understands that ancient bond",
                "there's a reaching-toward-something-larger here that I find deeply moving in music",
            ],
            "love": [
                "love songs are the oldest form there is — this one reminds you why they've never gone away",
                "the love theme here is handled with the tenderness the subject deserves",
            ],
            "rage": [
                "anger is a legitimate human emotion and music has always housed it — but this wears me out",
                "the rage theme connects to traditions I understand but the expression here doesn't move me",
            ],
            "street life": [
                "street life themes reflect a reality I haven't personally inhabited — I try to evaluate them fairly but I won't pretend otherwise",
                "the cultural specificity of the street life theme is handled with authenticity even if it's not my world",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme connects to something fundamentally human — good music always does",
            f"I've heard this theme handled better and worse — this falls on the better side",
            f"the {t} direction gives this an emotional grounding that I appreciate in a record",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 360:
            return [pick([
                "they used to make records that took their time, and I was glad for it — this continues that tradition",
                "the extended runtime feels natural — music shouldn't always be in a hurry",
            ])]
        if d < 150:
            return [pick([
                "songs used to breathe a little more than this",
                "the brevity works but I always want more when the music is good — and sometimes even when it isn't",
            ])]
        return [pick([
            "the runtime is appropriate — neither overstaying nor cutting short",
            "the length feels honest — as long as it needs to be and no longer",
        ])]


# ─────────────────────────────────────────────
#  CRITIC 6 — ZARA NIGHTS  (Underground Scene Rep)
# ─────────────────────────────────────────────

class ZaraNights(Critic):
    name = "Zara Nights"
    tagline = "Zine Editor & Promoter, The Circuit"
    verdict_type = "scenes"

    loved_genres    = ["punk", "electronic", "hip hop", "experimental"]
    liked_genres    = ["metal", "rock", "r&b"]
    disliked_genres = ["country", "classical"]
    hated_genres    = ["pop", "folk"]

    loved_themes    = ["street life", "rage", "protest", "party"]
    disliked_themes = ["nostalgia", "spirituality", "love"]

    base_modifier = 0

    def genre_lines(self, song):
        g = song.genre_label()
        pools = {
            "punk": [
                "punk is still the most authentic response to a world that needs pushing back on — this gets that",
                "the scene doesn't need perfect production; it needs this kind of conviction, and it's here",
                "raw, confrontational, and honest — what punk was always supposed to be",
            ],
            "electronic": [
                "electronic music at this level is architecture — and this was built correctly",
                "the scene runs on electronic music and this is the kind of track that earns its place in the rotation",
                "the production here speaks the language of the underground fluently",
            ],
            "hip hop": [
                "hip hop is still the most culturally alive genre on the planet and this knows what it's part of",
                "the hip hop credibility here is not borrowed — it's earned",
                "the scene can smell performative hip hop from a mile away. this is the real thing.",
            ],
            "pop": [
                "pop is designed for people who want music to do as little as possible — the underground has no use for that",
                "the pop framing is the loudest possible signal that this wasn't made for us",
                "the {g} direction positions this firmly outside the spaces where I operate",
            ],
            "folk": [
                "folk has its own underground, and I respect it — but this doesn't belong to either world convincingly",
                "the folk direction creates a pastoral distance from the urban energy that defines the scene I cover",
                "I don't disrespect folk as a tradition; I just don't see the connection to anything I care about currently",
            ],
            "country": [
                "country music has a cultural footprint that doesn't intersect with the spaces I inhabit",
                "the country framing here signals a set of values and aesthetics I have no relationship to",
            ],
        }
        for gname in song.genres:
            if gname in pools:
                formatted = [s.replace("{g}", g) for s in pools[gname]]
                return [picks(formatted, 2)]
        return [pick([
            f"the {g} direction lands credibly in the context I operate in",
            f"as a {g} release it holds up against the scene standards — which are demanding",
            f"the underground has heard a lot of {g} records; this one earns its place in that conversation",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "street life": [
                "the street life theme is handled with the kind of specificity that comes from having lived it",
                "the cultural authenticity of the street life angle is the record's most valuable quality",
            ],
            "rage": [
                "rage is an honest response to what the world is doing right now — this channels it usefully",
                "the anger here is specific and pointed rather than diffuse — that's the difference between art and noise",
            ],
            "protest": [
                "protest music is never more relevant than when institutions want it to be quiet — and they always want that",
                "the political edge here is sharp and the scene will receive it accordingly",
            ],
            "party": [
                "the best party music is secretly political — it claims space and that claim is always contested",
                "the party energy here has a propulsive urgency that goes beyond mere hedonism",
            ],
            "nostalgia": [
                "the scene is always looking forward; nostalgia-themed music can feel like a backward step from that vantage",
                "the retrospective angle creates a distance from the present that I find limiting",
            ],
            "love": [
                "love themes are fine, but they're not where the cultural energy lives right now",
                "the love angle gives this mass appeal at the cost of edge — that's a trade the scene doesn't usually endorse",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme is a legitimate angle — the scene will engage with it on those terms",
            f"thematically, this connects to something real and the underground can feel the difference",
            f"the {t} direction gives this an identity that holds up in the spaces I move through",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick([
                "the extended runtime is a flex — and the content earns it enough to carry it",
                "long records succeed or fail on whether they hold attention; this mostly does",
            ])]
        if d < 150:
            return [pick([
                "the compact length is pure scene energy — get in, do the thing, get out",
                "brevity in underground music is a power move and this plays it right",
            ])]
        return [pick([
            "the runtime hits the sweet spot for this kind of record",
            "paced correctly — the scene has no patience for filler and there isn't any here",
        ])]


# ─────────────────────────────────────────────
#  CRITIC 7 — TOBIAS LUND  (Casual Listener)
# ─────────────────────────────────────────────

class TobiasLund(Critic):
    name = "Tobias Lund"
    tagline = "Just Listens to Music"
    verdict_type = "casual"

    loved_genres    = ["pop", "hip hop", "r&b", "rock"]
    liked_genres    = ["reggae", "soul", "electronic"]
    disliked_genres = ["experimental", "blues"]
    hated_genres    = ["classical", "metal"]

    loved_themes    = ["party", "love", "euphoria", "nostalgia"]
    disliked_themes = ["existential", "protest"]

    base_modifier = 0.5

    def genre_lines(self, song):
        g = song.genre_label()
        pools = {
            "pop": [
                "this is exactly the kind of pop record I put on without thinking about it — which is a compliment",
                "pop music that actually sounds good? harder than it looks, apparently, and this pulls it off",
                "catchy, clean, and fun — the pop formula working as intended",
            ],
            "hip hop": [
                "the hip hop energy here hits — I found myself actually paying attention",
                "as a hip hop track it delivers on the basics: beat, bars, energy, done",
                "hip hop at its most listenable — which is a high bar",
            ],
            "r&b": [
                "smooth, warm, easy to listen to — the r&b vibe is exactly what you want here",
                "the r&b feel makes this instantly appealing in a way I appreciate",
            ],
            "classical": [
                "I respect it but this is not what I put on when I want to enjoy music",
                "classical music and I have an understanding: I acknowledge its importance and it doesn't expect me to love it",
                "technically it's probably impressive — I don't have the framework to appreciate it properly",
            ],
            "metal": [
                "metal is a lot and this is a lot — my head hurts a bit if I'm honest",
                "the energy is undeniable but it's not landing for me personally",
                "I admire people who love metal. I am not those people.",
            ],
            "experimental": [
                "I'm genuinely not sure what I was supposed to feel during this",
                "experimental music makes me feel like I'm missing a reference — which is on me, probably, but still",
            ],
        }
        for gname in song.genres:
            if gname in pools:
                return [picks(pools[gname], 2)]
        return [pick([
            f"as a {g} track it's doing its thing and mostly doing it well",
            f"the {g} vibe comes through clearly and it works for me",
            f"I don't know everything about {g} but I know when I'm enjoying it — and I'm enjoying it",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "party": [
                "the party energy is exactly what I want from a track like this",
                "it makes you want to move and that's the entire brief — successfully executed",
            ],
            "love": [
                "love songs never get old when they're done right and this is done right",
                "the love theme is relatable in the uncomplicated way that makes pop music work",
            ],
            "euphoria": [
                "it genuinely made me feel good while listening and I'm not going to overthink that",
                "pure positive energy — not complicated, not trying to be, and succeeding completely",
            ],
            "nostalgia": [
                "nostalgia hits differently when the music is this good — I kept thinking of good times",
                "the nostalgic feel is warm and familiar without being lazy",
            ],
            "existential": [
                "deep stuff — maybe too deep for what I usually look for in music",
                "the existential angle is handled thoughtfully but it requires more from the listener than I had today",
            ],
            "protest": [
                "the political edge is sharp enough to make me slightly uncomfortable, which might be the point",
                "I don't usually go to music for politics but I can see what this is doing",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme comes through and it adds something personal to the record",
            f"there's a clear emotional angle here and it mostly works on me",
            f"I can follow the {t} thread and it kept me engaged",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick([
                "it starts to drag a bit in the back half — I checked my phone twice",
                "five minutes is my limit and this pushed past it a little",
            ])]
        if d < 150:
            return [pick([
                "it's short and sweet and I didn't need more — perfect length",
                "two minutes of something great is worth ten minutes of something okay",
            ])]
        return [pick([
            "it's the right length — I wasn't waiting for it to end",
            "the runtime is fine — neither too long nor too short",
        ])]


# ─────────────────────────────────────────────
#  CRITIC 8 — NINA PASCAL  (Balanced Genre Agnostic)
# ─────────────────────────────────────────────

class NinaPascal(Critic):
    name = "Nina Pascal"
    tagline = "Staff Writer, Sound & Signal"
    verdict_type = "academic"  # uses academic verdicts but with different biases

    loved_genres    = ["soul", "blues", "rock", "folk", "hip hop"]
    liked_genres    = ["jazz", "r&b", "reggae", "country"]
    disliked_genres = ["experimental"]
    hated_genres    = []   # genuinely tries to be fair

    loved_themes    = ["heartbreak", "nostalgia", "protest", "existential"]
    disliked_themes = ["euphoria"]

    base_modifier = 0

    def genre_lines(self, song):
        g = song.genre_label()
        if song.is_blend:
            return [pick([
                f"the {song.genres[0]}/{song.genres[1]} blend is an interesting creative risk — how it pays off depends entirely on the execution",
                f"blending {song.genres[0]} and {song.genres[1]} is either inspired or confused; the quality of the work determines which",
                f"the genre blend here opens up a sonic space that neither {song.genres[0]} nor {song.genres[1]} occupies alone — that's worth noting",
                f"mixing {song.genres[0]} with {song.genres[1]} is a genuine compositional statement and this follows through on it",
            ])]
        return [pick([
            f"the {g} framework is applied with a clear understanding of what the genre can and cannot do",
            f"within {g}, this makes thoughtful choices about which conventions to honour and which to test",
            f"the {g} reference points are clear and the execution suggests genuine familiarity with the tradition",
            f"as a {g} record it navigates the genre's expectations without being fully captured by them",
        ])]

    def theme_lines(self, song):
        t = song.theme
        pools = {
            "heartbreak": [
                "heartbreak is the oldest subject in music and this handles it with appropriate emotional intelligence",
                "the vulnerability required by heartbreak themes is present here — and it's the record's strongest quality",
            ],
            "nostalgia": [
                "the nostalgic register is handled with enough self-awareness to avoid sentimentality",
                "nostalgia is only meaningful when it's honest about what's being mourned — this is honest",
            ],
            "protest": [
                "the social consciousness here is integrated into the music rather than appended to it — that's the right approach",
                "protest themes succeed when they're specific; this achieves that specificity",
            ],
            "existential": [
                "the existential dimension here is earned rather than assumed — it doesn't reach for profundity without something to say",
                "the philosophical content gives this a weight that rewards returning to it",
            ],
            "euphoria": [
                "euphoria as a theme tends to produce music without interiority — there's a version of this that could have been more",
                "the euphoric mode is executed competently but I find it the least interesting emotional terrain to explore",
            ],
        }
        if t in pools:
            return [picks(pools[t], 2)]
        return [pick([
            f"the {t} theme is realized with craft — it's not window dressing, it's load-bearing",
            f"the thematic content contributes meaningfully to the overall experience",
            f"the {t} direction is a deliberate choice and a well-executed one",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 360:
            return [pick([
                "at this length, the material needs to sustain itself — it largely does",
                "the extended runtime is justified by the compositional ambition on display",
            ])]
        if d < 150:
            return [pick([
                "the brevity sharpens rather than limits — everything here is essential",
                "short records are a discipline; this one respects the constraint",
            ])]
        return [pick([
            "the pacing reflects good judgment about when the material has said what it has to say",
            "the duration is appropriate — no padding, no truncation",
        ])]


# ─────────────────────────────────────────────
#  SIMULATION
# ─────────────────────────────────────────────

class Simulation:
    def __init__(self):
        self.critics = [
            MarcusVane(),
            DejaHayes(),
            DrPriyaSolan(),
            RayColdwell(),
            EarlMosely(),
            ZaraNights(),
            TobiasLund(),
            NinaPascal(),
        ]

    def publish_song(self, song):
        print()
        print("╔" + "═" * 58 + "╗")
        label = f"  REVIEWS: '{song.name}'  "
        print("║" + label.center(58) + "║")
        genre_label = f"Genre: {song.genre_label()}   |   Theme: {song.theme}   |   Duration: {fmt_duration(song.duration)}"
        print("║" + genre_label.center(58) + "║")
        print("╚" + "═" * 58 + "╝")

        scores = []
        for critic in self.critics:
            score, text = critic.review(song)
            scores.append(score)
            print()
            print(f"  ★ {critic.name}  [{critic.tagline}]")
            print(f"  {'─' * 52}")
            # word-wrap at ~70 chars
            words = text.split()
            line = "  "
            for word in words:
                if len(line) + len(word) + 1 > 72:
                    print(line)
                    line = "  " + word + " "
                else:
                    line += word + " "
            if line.strip():
                print(line)
            print()

        avg = round(sum(scores) / len(scores), 1)
        print("╔" + "═" * 58 + "╗")
        avg_line = f"  AVERAGE CRITICAL SCORE:  {avg} / 10  "
        print("║" + avg_line.center(58) + "║")
        # consensus tag
        if avg >= 9.5:
            tag = "UNIVERSAL ACCLAIM"
        elif avg >= 8.0:
            tag = "GENERALLY ACCLAIMED"
        elif avg >= 6.5:
            tag = "GENERALLY FAVOURABLE"
        elif avg >= 5.0:
            tag = "MIXED REVIEWS"
        elif avg >= 3.0:
            tag = "GENERALLY UNFAVOURABLE"
        else:
            tag = "OVERWHELMING DISLIKE"
        print("║" + f"  {tag}  ".center(58) + "║")
        print("╚" + "═" * 58 + "╝")


def fmt_duration(secs):
    return f"{secs // 60}:{secs % 60:02d}"


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

def banner():
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  🎵  MUSIC CAREER SIMULATOR  —  REVIEW ENGINE  🎵  ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def get_choice(prompt, options):
    while True:
        print(f"\n  {prompt}")
        for key, val in options.items():
            print(f"    [{key}]  {val}")
        choice = input("  ›› ").strip()
        if choice in options:
            return options[choice]
        print("  ✗ Invalid choice — try again.")


def parse_duration():
    while True:
        try:
            mins = int(input("  Minutes: "))
            secs = int(input("  Seconds: "))
            if 0 <= secs < 60 and mins >= 0:
                return mins * 60 + secs
        except (ValueError, TypeError):
            pass
        print("  ✗ Invalid duration — try again.")


def select_genres():
    print("\n  ┌─────────────────────────────────────────┐")
    print("  │           SELECT GENRE(S)               │")
    print("  └─────────────────────────────────────────┘")
    genre_map = {str(i+1): g for i, g in enumerate(GENRES)}
    for key, val in genre_map.items():
        print(f"    [{key:>2}]  {val}")

    while True:
        raw = input("  ›› Pick 1 or 2 genre numbers (e.g. '1' or '3 7'): ").strip()
        parts = raw.split()
        if len(parts) == 1 and parts[0] in genre_map:
            return [genre_map[parts[0]]]
        if len(parts) == 2 and parts[0] in genre_map and parts[1] in genre_map and parts[0] != parts[1]:
            return [genre_map[parts[0]], genre_map[parts[1]]]
        print("  ✗ Pick 1 or 2 valid different genre numbers.")


def select_theme():
    theme_map = {str(i+1): t for i, t in enumerate(THEMES)}
    return get_choice("SELECT THEME:", theme_map)


def main():
    banner()
    sim = Simulation()

    while True:
        print()
        cmd = input("  Press [C] to create a song  |  [Q] to quit  ›› ").strip().lower()

        if cmd == 'q':
            print("\n  See you on the charts.\n")
            break
        if cmd != 'c':
            continue

        while True:
            quality = random.randint(1, 10)
            print()
            print(f"  ┌──────────────────────────────────────┐")
            print(f"  │  Song generated  —  Quality: {quality}/10     │")
            print(f"  └──────────────────────────────────────┘")
            print(f"    [1]  Scrap it and re-roll")
            print(f"    [2]  Publish this one")
            act = input("  ›› ").strip()

            if act == '1':
                continue

            if act == '2':
                print()
                name = input("  Song name: ").strip() or "Untitled"

                genres = select_genres()
                theme = select_theme()

                print("\n  ┌────────────────────────────────────┐")
                print("  │           SONG DURATION            │")
                print("  └────────────────────────────────────┘")
                duration = parse_duration()

                song = Song(quality, name, genres, theme, duration)
                sim.publish_song(song)
                break


if __name__ == "__main__":
    main()
