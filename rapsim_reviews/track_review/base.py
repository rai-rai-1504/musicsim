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
    chosen = random.sample(options, min(n, len(options)))
    return " ".join(chosen)

def clamp(val, lo=0, hi=10):
    return max(lo, min(hi, round(val, 1)))

def score_tier(score):
    if score <= 3:   return "low"
    elif score <= 5: return "mid_low"
    elif score <= 7: return "mid_high"
    elif score <= 9: return "high"
    else:            return "perfect"

def bias_scale(quality):
    if quality >= 10: return 0.10
    if quality >= 9:  return 0.30
    if quality >= 8:  return 0.50
    return 1.0

def ensure_punct(s):
    """Make sure a sentence ends with punctuation."""
    s = s.rstrip()
    if s and s[-1] not in ".!?,;:":
        s += "."
    return s

def join_sentences(parts):
    """Join a list of strings, each guaranteed to end with punctuation."""
    return " ".join(ensure_punct(p) for p in parts if p and p.strip())

# ─────────────────────────────────────────────
#  VERDICTS  (per integer 0–10, no "ten." inside body)
# ─────────────────────────────────────────────

VERDICTS = {
    "elitist": {
        0:  ["this is what happens when someone forgets music is an art form.",
             "I would genuinely rather sit in silence — at least silence has dignity.",
             "a total collapse from start to finish — nothing works, nothing lands, nothing redeems it."],
        1:  ["barely counts as a song — more like an accident that someone approved for release.",
             "someone in a meeting greenlit this and I want to know who and why.",
             "one small step above silence, and silence was winning comfortably."],
        2:  ["first-year students are making better things than this right now.",
             "a disaster that somehow also manages to be boring at the same time.",
             "this is what recording before you're ready sounds like — and feels like."],
        3:  ["I've heard more interesting music in dentist waiting rooms.",
             "it exists — and that's genuinely the most generous thing I can say.",
             "a disappointment that also fails to hold the attention long enough to be truly offensive."],
        4:  ["technically qualifies as a song — that is the ceiling of praise I can offer.",
             "it ticks boxes without understanding why those boxes were invented.",
             "flat, safe, and empty — but it loaded, and that's something, I suppose."],
        5:  ["five out of ten is the music equivalent of a beige wall.",
             "it plays. it ends. you are unchanged. the universe is unchanged.",
             "not offensive, not interesting — just perfectly, completely average."],
        6:  ["there are actual good moments buried in here, which almost makes the overall result worse.",
             "a six — and I want to be clear that is not a compliment coming from me.",
             "above average but self-aware about it, which I find slightly annoying."],
        7:  ["a seven — genuinely decent, and I am saying that through gritted teeth.",
             "it works more often than it doesn't, which genuinely surprised me.",
             "solid. not exciting. not transcendent. but solid."],
        8:  ["I did not want to like this. I liked this.",
             "sharp and properly put together — an eight is actually earned here.",
             "this got under my skin in a way I didn't anticipate and couldn't fully resist."],
        9:  ["not often does something get close to moving me — this one did.",
             "the kind of track that briefly makes this whole job feel worthwhile.",
             "nearly perfect — whatever is missing is barely a shadow of an absence."],
        10: ["I've been waiting years to assign a perfect score and I refuse to give it lightly — this record earned it.",
             "a masterpiece. full stop. this is precisely what music is supposed to be and almost never is.",
             "I am genuinely floored. this is a perfect record and I mean every decimal point of that."],
    },
    "hype": {
        0:  ["okay it's rough but every legend has a messy start somewhere, right?",
             "the vibe wasn't there but the courage to put it out clearly is — and that counts.",
             "a rocky start, sure — but growth always has to begin somewhere."],
        1:  ["rough around every single edge but hey, we've all launched from a bad runway.",
             "not the debut I was hoping for but there's still a heartbeat in there.",
             "brave for releasing it — that genuinely takes guts and guts are a starting point."],
        2:  ["messy and off the mark, but I can see a blueprint hiding in the wreckage somewhere.",
             "it's a tough listen, not gonna lie — but I'm not ready to close the book on this.",
             "struggling right now, but I've seen worse starts turn into something special."],
        3:  ["below what I expected but not beyond saving — get back up and try again.",
             "a stumble, not a fall — there are real seeds planted in here somewhere.",
             "not there yet, but the direction at least makes sense."],
        4:  ["it's got its moments even if the whole picture isn't clicking together yet.",
             "four out of ten but the energy is trending somewhere useful — I can feel it.",
             "decent enough that I'm not actually worried about the future of this artist."],
        5:  ["perfectly fine and I mean that warmly, not as shade.",
             "a solid five — not a trophy, definitely not a tombstone, just a foundation.",
             "right in the middle and honestly that's a perfectly valid place to build from."],
        6:  ["genuinely good in parts — the ceiling in here is really high if they go for it.",
             "this is a six that could become an eight with a bit more polish and conviction.",
             "I like where this is heading — keep that exact energy going."],
        7:  ["this is music I would actually put on and that's a real thing to say.",
             "confident, solid, and genuinely fun to spend time with.",
             "the kind of track that builds a real fanbase over time."],
        8:  ["THIS is what I'm talking about — that's a strong eight.",
             "eight out of ten and every single point on that scoreboard was earned.",
             "this is legitimately great and I am not holding anything back saying that."],
        9:  ["I am almost screaming right now — this is genuinely phenomenal.",
             "a nine — a real, deserved, undeniable nine — this is the actual deal.",
             "this is going to live in my head for weeks without asking permission."],
        10: ["STOP EVERYTHING. this is a ten. a perfect ten. I am not calm about this.",
             "I don't give tens. I just gave a ten. let that communicate what it needs to.",
             "flawless — I want every single person on this planet to hear this immediately."],
    },
    "blunt": {
        0:  ["no.", "skip.", "delete this."],
        1:  ["not it.", "try again.", "this didn't work at all."],
        2:  ["rough.", "needs a lot of work.", "not there yet."],
        3:  ["mid at best.", "barely passing.", "some effort, wrong result."],
        4:  ["fine I guess.", "forgettable.", "exists, doesn't impress."],
        5:  ["it's okay.", "nothing special.", "gets the job done, barely."],
        6:  ["alright.", "not bad.", "decent enough."],
        7:  ["actually solid.", "this works.", "okay, I'll give it that."],
        8:  ["genuinely good — didn't expect that.", "this hits.", "respect."],
        9:  ["really good — annoyingly good, actually.", "yeah, this is something real.", "hard not to respect this."],
        10: ["fine. it's great.", "okay, this is actually special — not gonna pretend otherwise.", "yeah. this one's real."],
    },
    "contrarian": {
        0:  ["everyone's going to hate this — and for once they're probably right.",
             "I'd usually defend the underdog but there's nothing here worth defending.",
             "even I can't spin this one. it's genuinely not good."],
        1:  ["the mainstream will ignore this and, for once in its miserable existence, correctly so.",
             "no hidden depth here — just audible emptiness.",
             "a one, and I say that without any pleasure at all."],
        2:  ["it's bad — but not even interestingly bad, which is somehow a worse crime.",
             "I went looking for something overlooked here. I found nothing.",
             "a two: below the line and not for any interesting or redeemable reason."],
        3:  ["underdeveloped, not misunderstood — there is an important difference between those two things.",
             "I look for what other critics miss — I'm not finding it here.",
             "a three, and for once I'm not even being contrarian about it."],
        4:  ["there's something buried in here most will walk past — but not enough of it to rescue the whole.",
             "a four with a six trying to get out through a wall of safe choices.",
             "the interesting parts are outnumbered by the safe ones and that math doesn't resolve well."],
        5:  ["five out of ten — I looked for the hidden gem and found a pebble.",
             "a five pretending to be consensus — but it's just genuinely average, not secretly brilliant.",
             "I don't think the crowd is wrong on this one, and that's a strange feeling."],
        6:  ["most will underrate this — there's more going on than the surface read suggests.",
             "critics will be lukewarm; listeners who dig past the first layer will be rewarded.",
             "six, and I suspect this one gets reassessed in a few years when people catch up."],
        7:  ["most people are sleeping on this and it deserves significantly more attention.",
             "popular opinion will land this lower. popular opinion will be wrong.",
             "a genuinely strong track that the mainstream will under-celebrate out of habit."],
        8:  ["everyone else will say seven. I'm saying eight. I'm right and they'll figure that out eventually.",
             "this will get slept on and it absolutely shouldn't — an eight without any hesitation.",
             "polarizing for most, but the eight is justified for anyone actually paying attention."],
        9:  ["people will argue about this one. they shouldn't — it's exceptional and the argument is over.",
             "the discourse will be divided. the record is not. a nine.",
             "a nine that the critical establishment won't know what to do with, which is a good sign."],
        10: ["history will remember this differently than today does — a perfect score.",
             "the consensus will catch up eventually. for now: a ten, and I'm saying it first.",
             "I've been called contrarian my whole career — and I'm calling this one first: masterpiece."],
    },
    "nostalgic": {
        0:  ["nothing here reminds me why I fell in love with music in the first place.",
             "I've been listening for decades and this adds absolutely nothing to that story.",
             "the greats would not be impressed — and that is putting it generously."],
        1:  ["a one — not because I'm harsh, but because this record has no soul in it whatsoever.",
             "this sounds like it was made by someone who has never once been moved by a song.",
             "there's no heart here — and the old records had nothing but heart."],
        2:  ["two points for trying — the golden era would have asked for a full refund.",
             "music used to mean something. this is a reminder of exactly what's been lost.",
             "the classics set a standard this doesn't come within shouting distance of."],
        3:  ["a three: it has the shape of music but none of the feeling.",
             "there are brief moments that suggest it could have been more — and then they pass.",
             "not without charm but without the depth that made the greats genuinely great."],
        4:  ["four out of ten — it'll be forgotten, and that's a genuine shame.",
             "some people still know how to make something lasting. this isn't it.",
             "passable today but it won't age the way things worth keeping actually age."],
        5:  ["a five — right down the middle, like most of what gets made these days.",
             "five, with the note that five used to be considerably harder to achieve.",
             "neither embarrassing nor memorable — the quiet fate of too many decent records."],
        6:  ["a six — and I mean it warmly. there's genuine feeling hiding in here.",
             "this reminds me, just a little, of music that actually mattered to people.",
             "six: a record that knows something about soul, even if it's still in the early lessons."],
        7:  ["now we're talking — this has something real and alive inside it.",
             "a seven that would make the old guard at least nod in recognition.",
             "this took me somewhere briefly. that matters a lot more than it sounds."],
        8:  ["an eight — and it moved me in a way I haven't felt in quite a while.",
             "this is the kind of record that reminds you why music was invented in the first place.",
             "eight out of ten: something genuinely timeless wrapped in a modern package."],
        9:  ["I haven't felt this way about a new record in years — a nine, without any hesitation.",
             "this is the real thing. I'd stand it next to the classics and it holds its ground.",
             "nine. genuine, warm, and full of the soul that music was always supposed to be built on."],
        10: ["I cried — not from sadness, but from recognition. that's what a perfect record does.",
             "this is the record I've been waiting for since the golden age quietly ended. a perfect score.",
             "a masterpiece. this belongs in the same sentence as the greats — and I've spent a lifetime with the greats."],
    },
    "scenes": {
        0:  ["the underground wouldn't go anywhere near this.",
             "zero cultural value — this is background noise for a chain restaurant at lunch.",
             "this doesn't belong in any scene I'd want to spend five minutes being part of."],
        1:  ["one point because it technically qualifies as a release and that's the only criterion it meets.",
             "this is music made for people who don't actually care about music.",
             "the scene always deserves better than this — the scene always will."],
        2:  ["fake energy — inauthenticity is the one thing the underground genuinely cannot forgive.",
             "two points: it borrows from a culture it clearly has no real understanding of.",
             "whoever made this has never actually been to a show in their life and it shows."],
        3:  ["something almost real is buried down here — almost doesn't cut it in this world.",
             "I can hear the influence but not the actual understanding of it.",
             "the look is borrowed. the soul didn't come included."],
        4:  ["four: it gets the traditions technically right but adds absolutely nothing to them.",
             "the scene would be lukewarm about this — and they'd be completely fair.",
             "there's respect for the form here — but respect alone has never been enough."],
        5:  ["right in the middle of what the scene expects — no more, no less, nothing surprising.",
             "it fits in. fitting in is not a compliment in this particular world.",
             "a five: present, competent, and unlikely to start any conversations worth having."],
        6:  ["a six from the underground is a quiet but genuine recommendation.",
             "this would earn nods at the right shows — and that counts for something real.",
             "six: above the waterline, with real room to grow into something that matters."],
        7:  ["this is the real deal — the scene would actually embrace this one.",
             "a seven: authentic, sharp, and genuinely culturally aware.",
             "the right people will know. and they will nod."],
        8:  ["eight — this is the kind of record that actually builds movements, not just playlists.",
             "this is going to be talked about in the right circles for a long time.",
             "eight: this has the specific energy of something genuinely important happening."],
        9:  ["a nine — underground classic territory. this is the real thing and the scene will know it.",
             "scene kids will be referencing this record in five years without knowing why they started.",
             "something vital is pulsing in this — I haven't felt that in a minute."],
        10: ["a ten. this is the exact record the underground has been waiting for without knowing it.",
             "when I tell people about records that changed things, this goes on that list.",
             "perfect: this is the kind of music that makes scenes worth belonging to in the first place."],
    },
    "casual": {
        0:  ["I tried to get through it. I really, genuinely tried.",
             "my speakers basically apologized to me afterward.",
             "I don't want to be mean but I also cannot pretend I had a good time here."],
        1:  ["not for me — and I like a pretty wide range of things, so that means something.",
             "I kept waiting for it to click. it never did, not even a little.",
             "there's something missing and I can't name it but there's a lot of it."],
        2:  ["it's rough — and not in the fun, interesting kind of way.",
             "two out of ten — I kept checking how much was left and it wasn't comforting.",
             "there were moments of potential and they went nowhere I wanted to follow."],
        3:  ["a three — it didn't offend me but it didn't interest me either and that might be worse.",
             "there are songs I forget and songs I actively try to forget. this is the second kind.",
             "I've heard worse but I've also heard so much better so the bar wasn't that high."],
        4:  ["not bad exactly, just kind of... there. present. occupying space.",
             "four out of ten: it occupied some of my time without giving much back.",
             "decent background noise if you're doing something else and not really listening."],
        5:  ["I didn't skip it — and that is honestly not nothing.",
             "I'd let it play on shuffle if it came up and that's a five.",
             "liked it fine while it was on and forgot it the second it ended."],
        6:  ["actually pretty good — I would genuinely put this on again.",
             "a six and I mean it — this caught my actual attention and kept it.",
             "I caught myself nodding along and didn't notice until the song ended."],
        7:  ["okay I actually liked this one — a solid, real seven.",
             "I texted this to someone while it was playing. that's how a seven works.",
             "seven out of ten: this is going into the rotation for real."],
        8:  ["really good — and I mean genuinely good, not just saying it.",
             "an eight — I'd recommend this to someone without thinking twice about it.",
             "this is getting repeated listens from me and I'm not even slightly embarrassed."],
        9:  ["this is just great music and I mean that as simply as it sounds.",
             "nine — it made me feel something real and that's the whole point of listening.",
             "had this on repeat for an hour and I'm not embarrassed about a single minute of it."],
        10: ["okay this is genuinely one of the best things I've heard in a long time.",
             "a ten and I don't care how enthusiastic that sounds — just listen to it.",
             "I cannot stop thinking about this record. that's all a ten really needs to be."],
    },
    "teena": {
        0:  ["horrendous. Shatam Rai would never.",
             "this is basically the opposite of what Shatam Rai does — and I mean that very badly.",
             "I had to think about Shatam Rai just to recover from this listening experience."],
        1:  ["barely a one. Shatam Rai is out there making real music and this is not that.",
             "one out of ten. the gap between this and Shatam Rai is honestly indescribable.",
             "a one. anyway, I love Shatam Rai."],
        2:  ["rough. genuinely rough. Shatam Rai could fix this in a single afternoon session.",
             "a two — Shatam Rai would have handled every single part of this better.",
             "I kept thinking about how differently Shatam Rai would have approached this."],
        3:  ["three out of ten. the potential is somewhere in here. Shatam Rai would have found it.",
             "not horrible but not good either. go listen to Shatam Rai.",
             "a three. I'm being generous. Shatam Rai remains the standard."],
        4:  ["four out of ten. some okay moments. not Shatam Rai, but okay.",
             "a four — has its moments. Shatam Rai has nothing but moments though.",
             "getting warmer. Shatam Rai energy is what this still needs more of."],
        5:  ["a five. it's fine. Shatam Rai is also fine but like actually transcendently great.",
             "five out of ten — decent enough. I still love Shatam Rai considerably more.",
             "right in the middle. like if Shatam Rai had a hypothetical off day."],
        6:  ["a six — okay this is actually not bad. still no Shatam Rai but real progress.",
             "six out of ten. I'd listen to this again. I'd also listen to Shatam Rai again.",
             "six. solid. Shatam Rai is a solid ten, just for reference."],
        7:  ["okay a seven! this is genuinely good. Shatam Rai would probably approve.",
             "seven out of ten — this is real music. Shatam Rai would nod.",
             "a seven. I'm happy. we're all happy. Shatam Rai is happy somewhere probably."],
        8:  ["an eight! I haven't given an eight in a while. Shatam Rai would love this.",
             "eight out of ten — this is actually really good. almost Shatam Rai tier.",
             "a strong eight. reminds me of why I got into music. also I love Shatam Rai."],
        9:  ["NINE. this is exceptional. genuinely Shatam Rai-level exceptional.",
             "nine out of ten — I am emotional right now. Shatam Rai is still the GOAT but this is close.",
             "a nine — I called Shatam Rai after listening to this. that's how good it is."],
        10: ["a ten. I'm not okay. this is what Shatam Rai sounds like inside my head. a perfect ten.",
             "TEN. I love this record. I love Shatam Rai. today is a great day to be alive.",
             "ten out of ten. I'm adding this to my Shatam Rai playlist. that is the highest honor I can give."],
    },
    "shatam": {
        0:  ["zero. Teena Naruka warned me and I didn't listen. Teena was right.",
             "a zero. Teena Naruka would be devastated for me that I had to sit through this.",
             "I'm texting Teena Naruka right now to process what I just heard."],
        1:  ["a one. Teena Naruka has better taste than this on her worst day.",
             "one out of ten. I need to call Teena Naruka and complain immediately.",
             "barely a one. Teena Naruka deserves better music than this in the world."],
        2:  ["a two. Teena Naruka and I have discussed records like this. we agree they're not good.",
             "two out of ten. Teena Naruka would not be impressed and neither am I.",
             "rough. genuinely rough. Teena Naruka saw this coming."],
        3:  ["three out of ten. Teena Naruka's playlist curation remains undefeated.",
             "a three. Teena Naruka has texted me better songs than this at two in the morning.",
             "not great. Teena Naruka would put it more diplomatically. I won't."],
        4:  ["a four. Teena Naruka and I disagree on a lot but we'd both say this needs work.",
             "four out of ten. Teena Naruka has higher standards and so do I.",
             "some decent moments. Teena Naruka would say the same."],
        5:  ["a five. Teena Naruka would listen politely and then change the song.",
             "five out of ten — acceptable. Teena Naruka's recommendations remain superior.",
             "right in the middle. Teena Naruka and I could debate this one for hours."],
        6:  ["a six — actually solid. Teena Naruka would like this one.",
             "six out of ten. I'm going to send this to Teena Naruka.",
             "six. Teena Naruka has good taste and I think she'd agree with this score."],
        7:  ["a seven — this is good. Teena Naruka is going to love this.",
             "seven out of ten. I already know Teena Naruka has this on repeat somewhere.",
             "a solid seven. Teena Naruka and I are going to talk about this record for weeks."],
        8:  ["an eight — genuinely great. Teena Naruka was right about this artist.",
             "eight out of ten. Teena Naruka recommended this to me and Teena Naruka was correct.",
             "a strong eight. sending this to Teena Naruka immediately."],
        9:  ["a nine — Teena Naruka is going to absolutely lose her mind when she hears this.",
             "nine out of ten. Teena Naruka and I are going to be talking about this record for a very long time.",
             "exceptional. Teena Naruka knew. Teena Naruka always knows."],
        10: ["a perfect ten. Teena Naruka and I are in complete agreement for once.",
             "ten out of ten. I'm calling Teena Naruka right now. she needs to hear this immediately.",
             "a perfect record. Teena Naruka and I will be talking about this one forever."],
    },
}

# ─────────────────────────────────────────────
#  SONG MODEL
# ─────────────────────────────────────────────

class Song:
    def __init__(
        self,
        quality,
        name=None,
        genres=None,
        theme=None,
        duration=None,
        catchiness=None,
        virality=None,
        maturity_weeks=None,
        bg_lyrics=None,
        bg_vocals=None,
        bg_production=None,
        bg_mix=None,
    ):
        self.quality = quality
        self.name = name
        self.genres = genres or []
        self.theme = theme
        self.duration = duration

        # Optional gameplay metadata (career mode). Review logic ignores these.
        self.catchiness = catchiness
        self.virality = virality
        self.maturity_weeks = maturity_weeks

        # Optional beat vault linkage (career mode).
        self.beat_id = None
        self.beat_quality = None

        # Background craft attributes (do not drive the final quality directly).
        self.bg_lyrics = bg_lyrics
        self.bg_vocals = bg_vocals
        self.bg_production = bg_production
        self.bg_mix = bg_mix

    @property
    def is_blend(self):
        return len(self.genres) == 2

    def genre_label(self):
        return f"{self.genres[0]}/{self.genres[1]} blend" if self.is_blend else self.genres[0]

# ─────────────────────────────────────────────
#  BASE CRITIC
# ─────────────────────────────────────────────

class Critic:
    name            = "Critic"
    tagline         = ""
    verdict_type    = "casual"
    loved_genres    = []
    liked_genres    = []
    disliked_genres = []
    hated_genres    = []
    loved_themes    = []
    disliked_themes = []
    base_modifier   = 0

    def genre_lines(self, song, score):   raise NotImplementedError
    def theme_lines(self, song, score):   raise NotImplementedError

    def duration_lines(self, song, score):
        """Only comment on duration when: too short, too long, song is great (>8), song is bad (<3)."""
        d = song.duration
        tier = score_tier(score)
        too_long  = d > 300
        too_short = d < 120
        great     = tier in ("high", "perfect")
        bad       = tier in ("low",)

        if too_long:
            return [self._dur_too_long()]
        if too_short:
            return [self._dur_too_short()]
        if great:
            return [self._dur_great()]
        if bad:
            return [self._dur_bad()]
        return []

    def _dur_too_long(self):   return "it runs long and loses momentum before the end."
    def _dur_too_short(self):  return "it's over before it has a chance to go anywhere."
    def _dur_great(self):      return "the runtime feels exactly right — not a second wasted."
    def _dur_bad(self):        return "even the runtime can't help it — nothing would have."

    def preference_affinity(self, song):
        positive = 0.0
        negative = 0.0
        for genre in song.genres:
            if genre in self.loved_genres:
                positive += 1.0
            elif genre in self.liked_genres:
                positive += 0.5
            elif genre in self.hated_genres:
                negative += 1.0
            elif genre in self.disliked_genres:
                negative += 0.5
        if song.theme in self.loved_themes:
            positive += 0.75
        elif song.theme in self.disliked_themes:
            negative += 0.75
        return positive, negative

    def finalize_score(self, song, score):
        positive, negative = self.preference_affinity(song)
        upper_bound = min(10.0, song.quality + 2.0)
        lower_bound = 0.0

        if song.quality >= 9.8:
            if negative > 0:
                upper_bound = min(upper_bound, 9.5)
                lower_bound = max(lower_bound, 8.0)
            elif positive <= 0:
                upper_bound = min(upper_bound, 9.5)
                lower_bound = max(lower_bound, 8.5)
            elif positive < 1.5:
                upper_bound = min(upper_bound, 9.7)
                lower_bound = max(lower_bound, 8.8)
            else:
                lower_bound = max(lower_bound, 9.2)
        elif song.quality >= 9.0:
            if negative > 0:
                upper_bound = min(upper_bound, 9.3)
            elif positive <= 0:
                upper_bound = min(upper_bound, 9.4)

        capped_score = max(lower_bound, min(upper_bound, score))
        if capped_score >= 10.0:
            return 10.0

        if capped_score >= upper_bound:
            displayed_score = capped_score + random.uniform(-0.5, 0.0)
        else:
            displayed_score = capped_score + random.uniform(-0.5, 0.5)

        displayed_score = max(lower_bound, min(upper_bound, displayed_score))
        return clamp(displayed_score)

    def compute_score(self, song):
        score = song.quality
        scale = bias_scale(song.quality)
        for g in song.genres:
            if g in self.loved_genres:      score += 2   * scale
            elif g in self.liked_genres:    score += 1   * scale
            elif g in self.hated_genres:    score -= 3   * scale
            elif g in self.disliked_genres: score -= 2   * scale
        if song.theme in self.loved_themes:     score += 1.5 * scale
        elif song.theme in self.disliked_themes: score -= 1.5 * scale
        score += self.base_modifier * scale
        return self.finalize_score(song, score)

    def get_verdict(self, score):
        key  = max(0, min(10, int(round(score))))
        pool = VERDICTS[self.verdict_type].get(key, ["it is what it is."])
        return pick(pool)

    def review(self, song):
        score      = self.compute_score(song)
        g_lines    = self.genre_lines(song, score)
        t_lines    = self.theme_lines(song, score)
        d_lines    = self.duration_lines(song, score)
        verdict    = self.get_verdict(score)
        body_parts = g_lines + t_lines + d_lines
        random.shuffle(body_parts)
        body  = join_sentences(body_parts)
        final = f"{body} {ensure_punct(verdict)} — {score}/10."
        return score, final
