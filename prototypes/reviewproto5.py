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
    return " ".join(random.sample(options, min(n, len(options))))

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

# ─────────────────────────────────────────────
#  VERDICTS (per integer 0–10)
# ─────────────────────────────────────────────

VERDICTS = {
    "elitist": {
        0:  ["this is what it sounds like when someone forgets music is an art form",
             "I'd rather sit in silence. at least silence has dignity.",
             "a total failure from start to finish — nothing works, nothing lands"],
        1:  ["barely counts as a song — feels more like an accident that got released",
             "someone actually approved this and I want to know who",
             "one step above silence, and silence was doing better"],
        2:  ["there are first-year students making better stuff than this",
             "a disaster that somehow also manages to be boring",
             "this is what happens when you record before you're ready"],
        3:  ["I've heard better music in a dentist's waiting room",
             "it exists. that's genuinely the nicest thing I can say.",
             "a letdown that somehow also can't hold your attention"],
        4:  ["technically a song — that's the highest compliment I can offer",
             "it ticks boxes without understanding why those boxes matter",
             "flat, safe, and empty — but hey, it loaded"],
        5:  ["five out of ten: the music equivalent of beige",
             "it plays. it ends. nothing changes in you.",
             "not offensive, not interesting — just perfectly average"],
        6:  ["there are actual good moments buried in here, which almost makes it worse",
             "a six. that's not a compliment from me, just so we're clear.",
             "above average, but it knows it's above average, which is annoying"],
        7:  ["a seven — decent, and I'm genuinely gritting my teeth saying it",
             "it works more than it doesn't, which shocked me a little",
             "solid. not exciting. but solid."],
        8:  ["I didn't want to like this. I liked it.",
             "sharp and well-put-together — an eight is earned here",
             "this got under my skin in a way I didn't see coming"],
        9:  ["not often something gets close to moving me — this did",
             "the kind of track that makes this job feel worth doing",
             "nearly perfect — whatever's missing is barely a shadow"],
        10: ["I've waited years to give a ten. I don't give it lightly. this earned it.",
             "a masterpiece. full stop. this is what music is supposed to be.",
             "genuinely floored. a perfect ten, and I mean every single point of it"],
    },
    "hype": {
        0:  ["okay it's rough but like — every legend has a messy start, right?",
             "the vibe wasn't there but the courage to put it out clearly is",
             "a rocky start — but growth has to start somewhere!"],
        1:  ["rough around every edge but hey, we've all been there",
             "not what I hoped for but there's still a heartbeat in here",
             "brave for releasing it — that takes guts and guts count"],
        2:  ["messy and off, but I see a blueprint somewhere in there",
             "it's a hard listen, not gonna lie — but it's not hopeless",
             "struggling, but I'm not ready to write the story off yet"],
        3:  ["below what I expected but not beyond saving — get back up",
             "a stumble, not a fall — there are real seeds in here",
             "not there yet, but the direction makes sense"],
        4:  ["it's got its moments even if the whole thing isn't clicking",
             "four out of ten but the energy is going somewhere — I can feel it",
             "decent enough that I'm not worried about the future"],
        5:  ["perfectly fine and I mean that warmly, not as shade",
             "a solid five — not a trophy, but not a tombstone either",
             "right in the middle and honestly? that's a foundation to build on"],
        6:  ["genuinely good in parts — the ceiling here is really high",
             "this is a six that could easily become an eight with a bit more polish",
             "I like where this is heading — keep that energy going"],
        7:  ["this is music I would actually put on — a real seven",
             "confident, solid, and genuinely fun to listen to",
             "the kind of track that builds a real fanbase"],
        8:  ["okay THIS is what I'm talking about — strong eight!",
             "eight out of ten and every single point is earned",
             "this is legitimately great and I'm not holding back on that"],
        9:  ["I am almost screaming right now — this is phenomenal",
             "a nine! a real, deserved nine! this is the actual deal",
             "this is going to live in my head for weeks, no question"],
        10: ["STOP EVERYTHING. this is a ten. a perfect ten. I am not calm.",
             "I don't give tens. I just gave a ten. that's how good this is.",
             "flawless — I want everyone on the planet to hear this immediately"],
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
        8:  ["genuinely good. didn't expect that.", "this hits.", "respect."],
        9:  ["really good. annoying how much I like this.", "yeah, this is something.", "hard not to respect this."],
        10: ["fine. it's great. whatever.", "okay, this is actually special. not gonna pretend otherwise.", "yeah. this one's real."],
    },
    "contrarian": {
        0:  ["everyone's going to hate this — and for once they're probably right",
             "I'd usually defend the underdog — there's nothing here to defend",
             "even I can't spin this. it's genuinely not good."],
        1:  ["the mainstream will ignore this and, for once, correctly so",
             "no hidden depth here — just audible emptiness",
             "a one, and I say that without any pleasure at all"],
        2:  ["it's bad — but not even interestingly bad, which is somehow worse",
             "I went looking for something overlooked. I found nothing.",
             "a two: below the line and not for any interesting reason"],
        3:  ["underdeveloped, not misunderstood — there's a difference",
             "I look for what other critics miss — I'm not finding it here",
             "a three, and I'm not even being contrarian this time"],
        4:  ["there's something buried in here most will walk past — but not enough of it",
             "a four with a six trying to get out",
             "the interesting parts are outnumbered by the safe ones"],
        5:  ["five out of ten — I looked for the hidden gem and found a pebble",
             "a five pretending to be consensus — but it's just genuinely average",
             "I don't think the crowd is wrong on this one, sadly"],
        6:  ["most will underrate this — there's more going on than it looks",
             "critics will be lukewarm — listeners who dig deeper will be rewarded",
             "six, and I think this one gets reassessed in a few years"],
        7:  ["most are sleeping on this — it deserves way more attention",
             "popular opinion will put this lower. popular opinion is wrong.",
             "a genuinely good track that the mainstream will under-celebrate"],
        8:  ["everyone else will say seven. I'm saying eight. I'm right.",
             "this will get slept on and it really shouldn't — an eight",
             "polarizing for most — the eight is justified if you actually listen"],
        9:  ["people will argue about this. they shouldn't — it's exceptional.",
             "the discourse will be divided. the record is not. a nine.",
             "a nine that the critical world won't know what to do with"],
        10: ["history will remember this differently than today does — a perfect ten",
             "the consensus will catch up. for now: a ten, period.",
             "I've been called contrarian my whole career — I'm calling this first: masterpiece."],
    },
    "nostalgic": {
        0:  ["nothing here reminds me why I fell in love with music in the first place",
             "I've been listening for decades and this adds nothing to that story",
             "the greats would not be impressed — and not with joy"],
        1:  ["a one — not because I'm harsh, but because this has no soul",
             "this sounds like it was made by someone who's never been moved by a song",
             "there's no heart here — the old records had nothing but heart"],
        2:  ["two points for trying — the golden era would ask for a refund",
             "music used to mean something. this is a reminder of what's been lost.",
             "the classics set a standard this doesn't get close to"],
        3:  ["a three: it has the shape of music but not the feeling",
             "brief moments that suggest it could have been more — and then they pass",
             "not without charm but without the depth that made the greats great"],
        4:  ["four out of ten — it'll be forgotten, and that's a real shame",
             "some people still know how to make something lasting. this isn't it.",
             "passable today, but it won't age well"],
        5:  ["a five — right down the middle, like most music made these days",
             "five, with the note that five used to be harder to achieve",
             "neither embarrassing nor memorable — the fate of too many records"],
        6:  ["a six — and I mean it warmly. there's genuine feeling in here.",
             "this reminds me, just a little, of music that actually mattered",
             "six: a record that knows something about soul, even if it's still learning"],
        7:  ["now we're talking — this has something real in it",
             "a seven that would make the old guard nod",
             "this took me somewhere briefly. that matters. seven."],
        8:  ["an eight — moved me in a way I haven't felt in a while",
             "this is the kind of record that reminds you why music exists",
             "eight out of ten: something timeless in a modern package"],
        9:  ["I haven't felt this about a new record in years — a nine, no hesitation",
             "this is the real thing. I'd stand it next to the classics and it holds.",
             "nine. genuine, warm, and full of the soul that music is built on."],
        10: ["I cried. not sadness — recognition. this is a ten.",
             "this is the record I've been waiting for since the golden age ended. ten.",
             "a masterpiece. this belongs in the same sentence as the greats — and I know the greats."],
    },
    "scenes": {
        0:  ["the underground wouldn't go near this",
             "zero cultural value — this is background noise for a chain restaurant",
             "this doesn't belong in any scene I'd want to be part of"],
        1:  ["one point because it technically qualifies as a release",
             "this is music for people who don't care about music",
             "the scene always deserves better than this"],
        2:  ["fake energy — inauthenticity is the one thing we don't forgive",
             "two points: it borrows from a culture it clearly doesn't understand",
             "whoever made this has never actually been to a show in their life"],
        3:  ["something almost real is buried here — almost doesn't cut it",
             "I can hear the influence but not the understanding",
             "the look is borrowed. the soul didn't come with it."],
        4:  ["four: it gets the traditions right but doesn't add anything to them",
             "the scene would be lukewarm — and they'd be fair",
             "there's respect for the form — respect alone doesn't cut it though"],
        5:  ["right in the middle of what the scene expects — no more, no less",
             "it fits in. fitting in is not a compliment in this world.",
             "a five: present, competent, and unlikely to start any conversations"],
        6:  ["a six from the underground is a quiet recommendation",
             "this would get nods at the right shows — that's something",
             "six: above the waterline, room to grow into something special"],
        7:  ["this is the real deal — the scene would embrace it",
             "a seven: authentic, sharp, and culturally aware",
             "the right people will know. and they'll nod."],
        8:  ["eight — this is the kind of record that builds actual movements",
             "this is going to be talked about in the right circles for years",
             "eight: this has the energy of something genuinely important"],
        9:  ["a nine — underground classic territory. this is the real thing.",
             "scene kids will be referencing this record in five years, easily",
             "something vital is pulsing in this — I haven't felt that in a minute. nine."],
        10: ["a ten. this is the record the underground was waiting for.",
             "when I tell people about records that changed things, this goes on that list. ten.",
             "perfect: this is the kind of music that makes scenes worth belonging to"],
    },
    "casual": {
        0:  ["I tried to get through it. I really did.",
             "my speakers basically apologized to me",
             "I don't want to be mean but I can't pretend I enjoyed this"],
        1:  ["not for me — and I like a lot of things",
             "kept waiting for it to click. it never did.",
             "there's something missing and I can't name it but it's a lot"],
        2:  ["it's rough — and not in the fun way",
             "two out of ten — kept checking how much was left",
             "there was potential in moments. it didn't go anywhere I wanted to follow."],
        3:  ["a three — didn't offend me but didn't interest me either",
             "songs I forget and songs I try to forget. this is the second type.",
             "I've heard worse but I've also heard so much better"],
        4:  ["not bad exactly, just kind of... there",
             "four out of ten: occupied some minutes without much return",
             "decent background noise if you're doing something else"],
        5:  ["I didn't skip it — and that's not nothing",
             "I'd let it play if it came on shuffle",
             "liked it fine while it was on and forgot it instantly after"],
        6:  ["actually pretty good — I'd genuinely put this on again",
             "a six and I mean it — this caught my attention",
             "I caught myself nodding along. that's a real six."],
        7:  ["okay I actually liked this — a good seven",
             "I texted this to someone while it was playing. that's a seven.",
             "seven out of ten: this is going in the rotation"],
        8:  ["really good — like genuinely good, not just saying that",
             "an eight — I'd recommend this without thinking twice",
             "this is getting repeated listens from me, easy"],
        9:  ["this is just great music and I mean that simply",
             "nine — it made me feel something and that's the whole point",
             "had this on repeat and I'm not even embarrassed about it"],
        10: ["okay this is genuinely one of the best things I've heard in ages",
             "a ten and I don't care how enthusiastic that sounds — just listen to it",
             "can't stop thinking about this. that's a ten. easy."],
    },
    "teena": {
        0:  ["horrendous. Shatam Rai would never.",
             "this is basically the opposite of what Shatam Rai does. and I mean that badly.",
             "I'm sorry but I had to think about Shatam Rai just to get through this."],
        1:  ["barely a one. Shatam Rai is somewhere out there doing real music and this is not that.",
             "one out of ten. the gap between this and Shatam Rai is indescribable.",
             "a one. anyway I love Shatam Rai."],
        2:  ["rough. genuinely rough. Shatam Rai could fix this in one session.",
             "a two — not there at all. shoutout to Shatam Rai for existing though.",
             "I keep thinking about how differently Shatam Rai would have handled this."],
        3:  ["three out of ten. and I'm being generous. go listen to Shatam Rai.",
             "not horrible but not good. Shatam Rai would have made this a seven.",
             "a three. the potential is there. Shatam Rai found it. this didn't."],
        4:  ["four out of ten. some okay stuff. not Shatam Rai, but okay.",
             "a four — has its moments. Shatam Rai has nothing but moments though.",
             "getting warmer. four. Shatam Rai energy is what this needs more of."],
        5:  ["a five. it's fine. Shatam Rai is also fine but like actually great.",
             "five out of ten — decent enough. I still love Shatam Rai more.",
             "right in the middle. like if Shatam Rai had an off day. hypothetically."],
        6:  ["a six — okay this is actually not bad. still no Shatam Rai but progress.",
             "six out of ten. I'd listen to this again. I'd also listen to Shatam Rai again.",
             "six. solid. Shatam Rai is a solid ten, for reference."],
        7:  ["okay a seven! this is genuinely good. Shatam Rai approved probably.",
             "seven out of ten — this is real music. Shatam Rai would nod.",
             "a seven. I'm happy. Shatam Rai would be happy. we're all happy."],
        8:  ["an eight! I haven't given an eight in a while. Shatam Rai would love this.",
             "eight out of ten — this is actually really good. Shatam Rai tier almost.",
             "a strong eight. reminds me of why I got into music. also I love Shatam Rai."],
        9:  ["NINE. okay. NINE. this is exceptional. Shatam Rai-level exceptional.",
             "nine out of ten — I am emotional right now. Shatam Rai is still the GOAT but this is close.",
             "a nine!! I called Shatam Rai after listening to this. that's how good it is."],
        10: ["a ten. I'm not okay. this is what Shatam Rai sounds like in my head. a PERFECT TEN.",
             "TEN. I love this record. I love Shatam Rai. today is a great day.",
             "ten out of ten. I'm adding this to my Shatam Rai playlist. highest honor I can give."],
    },
}

# ─────────────────────────────────────────────
#  SONG MODEL
# ─────────────────────────────────────────────

class Song:
    def __init__(self, quality, name=None, genres=None, theme=None, duration=None):
        self.quality = quality
        self.name    = name
        self.genres  = genres or []
        self.theme   = theme
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
    name         = "Critic"
    tagline      = ""
    verdict_type = "casual"

    loved_genres    = []
    liked_genres    = []
    disliked_genres = []
    hated_genres    = []

    loved_themes    = []
    disliked_themes = []

    base_modifier = 0

    def genre_lines(self, song, score):
        raise NotImplementedError

    def theme_lines(self, song, score):
        raise NotImplementedError

    def duration_lines(self, song):
        raise NotImplementedError

    def compute_score(self, song):
        score = song.quality
        scale = bias_scale(song.quality)
        for g in song.genres:
            if g in self.loved_genres:    score += 2 * scale
            elif g in self.liked_genres:  score += 1 * scale
            elif g in self.hated_genres:  score -= 3 * scale
            elif g in self.disliked_genres: score -= 2 * scale
        if song.theme in self.loved_themes:    score += 1.5 * scale
        elif song.theme in self.disliked_themes: score -= 1.5 * scale
        score += self.base_modifier * scale
        return clamp(score)

    def get_verdict(self, score):
        key  = max(0, min(10, int(round(score))))
        pool = VERDICTS[self.verdict_type].get(key, ["it is what it is"])
        return pick(pool)

    def review(self, song):
        score        = self.compute_score(song)
        genre_part   = self.genre_lines(song, score)
        theme_part   = self.theme_lines(song, score)
        dur_part     = self.duration_lines(song)
        verdict      = self.get_verdict(score)
        all_sentences = genre_part + theme_part + dur_part
        random.shuffle(all_sentences)
        body  = " ".join(all_sentences)
        final = f"{body} {verdict} — {score}/10."
        return score, final


# ─────────────────────────────────────────────
#  CRITIC 1 — MARCUS VANE  (Elitist, Experimental/Jazz/Classical snob)
# ─────────────────────────────────────────────

class MarcusVane(Critic):
    name         = "Marcus Vane"
    tagline      = "Senior Editor, The Æsthetic Review"
    verdict_type = "elitist"

    loved_genres    = ["experimental", "jazz", "classical"]
    liked_genres    = ["folk", "blues", "soul"]
    disliked_genres = ["country", "reggae"]
    hated_genres    = ["pop", "electronic"]

    loved_themes    = ["existential", "spirituality", "protest"]
    disliked_themes = ["party", "euphoria"]

    base_modifier = -1.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "experimental": {
                "low":      ["the experimental label is being used here as cover for not finishing the ideas",
                             "going unconventional means nothing if there's no idea underneath — this is just noise with a concept pitch"],
                "mid_low":  ["the experimental direction gestures at something interesting without committing to any of it",
                             "the weird choices are there — the structural logic behind them isn't"],
                "mid_high": ["the experimental approach is genuinely ambitious — rare to see someone commit this fully",
                             "it pushes against the expected without announcing that it's doing so, which is the mark of real craft"],
                "high":     ["the willingness to break structure without losing the listener is extremely difficult — this pulls it off",
                             "this sits in conversation with artists like Bon Iver or Radiohead in their most daring moments — earned territory"],
                "perfect":  ["experimental music this complete and this emotionally realized is a once-in-a-decade event",
                             "I am genuinely astonished. this is a perfect record by any standard I hold."],
            },
            "jazz": {
                "low":      ["the jazz influences are namedrops, not understanding — you can hear the gap between the reference and the knowledge",
                             "Miles Davis built careers on knowing when not to play. this record plays constantly and says nothing."],
                "mid_low":  ["the jazz vocabulary is referenced without the musicianship to make those references mean anything",
                             "the harmonic ideas are borrowed, not understood — it sounds like jazz the way a costume sounds like a person"],
                "mid_high": ["the jazz sensibility gives this genuine depth — you can actually hear the lineage",
                             "the improvised spaces breathe in a way composed music usually can't — this earns its jazz tag"],
                "high":     ["this is jazz that rewards the kind of serious listening the tradition demands — a rare thing",
                             "the harmonic intelligence here puts me in mind of Kamasi Washington — not imitation, but the same level of seriousness"],
                "perfect":  ["jazz music this complete — in range, in craft, in feeling — belongs among the tradition's finest hours",
                             "I've waited years to write this about a new record. this is it. a perfect ten."],
            },
            "classical": {
                "low":      ["the classical influence here is decoration, not understanding — the structure collapses if you look at it closely",
                             "calling something classical because it has strings is not music theory — it's set dressing"],
                "mid_low":  ["the formal logic is underdeveloped — the classical framework is invoked without being truly applied",
                             "the compositional intent is there but the execution doesn't follow through on the structural promise"],
                "mid_high": ["the classical influence lends this a coherence that most contemporary music avoids — someone actually thought about the structure",
                             "you can hear a composer's mind at work here — the form serves the content, which is a classical principle"],
                "high":     ["the orchestral logic underlying this is exactly what modern music has been neglecting — and this brings it back without sounding old",
                             "this sits close to the best of the contemporary classical tradition — Max Richter territory, with its own voice"],
                "perfect":  ["a perfect classical-influenced record — the formal completeness here rivals the tradition's finest contemporary works",
                             "I have revised my expectations of what modern composers can achieve. this record is the reason."],
            },
            "pop": {
                "low":      ["pop music has produced one original idea per decade — this is not that idea and doesn't even try to be",
                             "everything about this is designed to keep you from thinking, and on that front it fully succeeds",
                             "the pop framing reduces whatever potential existed here to a product designed for passive background listening"],
                "mid_low":  ["the pop conventions are followed without any understanding of why those conventions exist",
                             "it's catchy in the way a jingle is catchy — which means it's not music, it's advertising"],
                "mid_high": ["there are flashes of something real inside the pop package — more than I expected, less than I need",
                             "the pop framework contains a genuine idea trying to get out — it doesn't fully escape, but the attempt is visible"],
                "high":     ["this is pop that makes me question my biases — the craft inside the commercial frame is actually real",
                             "a pop record that earns its hooks rather than just deploying them — a meaningful distinction few pop artists understand"],
                "perfect":  ["I am astonished to write this but: pop music has never felt this necessary to me — a perfect record by any standard",
                             "this transcends the genre label completely. the pop frame is the least interesting thing about it."],
            },
            "electronic": {
                "low":      ["synths are tools, not ideas — this track mistakes one for the other, repeatedly",
                             "the electronic production swaps texture for actual substance — a tired trick, and this does it loudly",
                             "there is nothing here that artists like Aphex Twin didn't make irrelevant decades ago"],
                "mid_low":  ["the production gives the illusion of innovation without doing anything genuinely new",
                             "the technical choices are competent and the artistic choices are empty"],
                "mid_high": ["electronic music at its best questions sound itself — this does so with partial success",
                             "the production language is more thoughtful than most in this space — deployed intelligently if not brilliantly"],
                "high":     ["the electronic architecture here is genuinely sophisticated — it understands that texture is an argument, not decoration",
                             "this sits in conversation with the serious end of the tradition — Four Tet or Burial territory, with its own emotional register"],
                "perfect":  ["the electronic composition here has the emotional range and internal logic of the greatest records in the form",
                             "I am not someone who gives electronic music the benefit of the doubt. which makes this score all the more significant."],
            },
            "hip hop": {
                "low":      ["the hip hop framework is here — the lyricism and sonic intelligence are not",
                             "Kendrick built entire worldviews in four minutes — this can't build a coherent verse"],
                "mid_low":  ["the artistic voice is absent — the beats are derivative and the bars offer nothing new",
                             "the hip hop elements are assembled competently but the idea behind them is missing"],
                "mid_high": ["the hip hop tradition is engaged honestly here — the production has weight and the lyricism has intent",
                             "there's a genuine relationship to the form — not just living in Kendrick's shadow but finding its own posture"],
                "high":     ["this is hip hop that holds up under the scrutiny that Illmatic or TPAB demands — serious music",
                             "the lyricism here works on more than one level at a time — the mark of a genuine artist working in the tradition"],
                "perfect":  ["hip hop at this level stops being genre and becomes literature — this record earns that comparison",
                             "I think of this alongside Illmatic and To Pimp a Butterfly: records that permanently expand what the form can hold"],
            },
            "r&b": {
                "low":      ["r&b's emotional vocabulary has been reduced here to pure formula — there's no actual feeling behind the smoothness",
                             "the genre demands genuine openness — this offers a convincing imitation of it and nothing more"],
                "mid_low":  ["the r&b elements are present but the groove is mechanical — it moves without feeling",
                             "slick in a way that erases the human warmth the genre is built on"],
                "mid_high": ["the r&b sensibility is applied with enough real feeling to rise above the generic",
                             "the melodic intelligence is real — not Frank Ocean, but a record that knows what Frank Ocean was doing"],
                "high":     ["the emotional depth of the r&b tradition is honored here rather than just mentioned",
                             "this sits close to the best of the neo-soul era — the kind of record that makes the genre's fans feel vindicated"],
                "perfect":  ["r&b at this level earns the comparison to its greatest records — the emotional range and craft of the form's finest work",
                             "I find myself revising my skepticism of the genre on the basis of this record alone"],
            },
            "metal": {
                "low":      ["the heaviness here is deployed without the compositional intelligence that separates Black Sabbath from just noise",
                             "aggression without structure is just volume — and volume is the cheapest thing in music"],
                "mid_low":  ["technically accomplished in moments but the emotional range is too narrow to sustain the whole thing",
                             "the metal craft is present in places — the intellectual content doesn't match the sonic ambition"],
                "mid_high": ["the intensity is deployed with more craft than the genre usually gets credit for",
                             "heavy music deserves serious analysis and this record makes that case with some conviction"],
                "high":     ["this is metal that rewards the kind of attention usually saved for genres with more academic approval",
                             "the compositional density here rivals the great records in the form — serious music in loud clothes"],
                "perfect":  ["I have resisted metal for decades. this record makes that resistance feel like a mistake.",
                             "the structural and emotional ambition here is complete — a perfect record that happens to be heavy"],
            },
            "punk": {
                "low":      ["punk without conviction is just noise with a three-chord budget and borrowed anger",
                             "the Clash had something to say — this is frustration with no target, which is just bad behavior"],
                "mid_low":  ["the punk energy is present but the ideas aren't there to justify it",
                             "rawness is a style choice — this mistakes it for a replacement for content"],
                "mid_high": ["the punk directness is the most honest thing about this record — it doesn't try to be liked, and that ends up being likeable",
                             "the confrontational energy is earned rather than performed — that matters in this genre"],
                "high":     ["punk that actually has something to say — the form and content are lined up in a way the genre rarely achieves",
                             "this carries the conviction of the great punk records without being a museum exhibit about them"],
                "perfect":  ["punk music at this level fulfills the promise the genre made in 1977 and has mostly not kept since",
                             "the most important punk record I've heard since the defining works — and I mean structurally, not just emotionally"],
            },
            "reggae": {
                "low":      ["the reggae rhythm is present and the spirit is completely absent — Bob Marley would not recognize this",
                             "the genre carries a philosophy of resistance — this carries neither the philosophy nor the resistance"],
                "mid_low":  ["the reggae elements are surface-level — the groove without the weight beneath it",
                             "the rhythm is there but the meaning that makes reggae more than just dancing is missing"],
                "mid_high": ["the reggae tradition is treated with genuine respect — the groove carries the right kind of weight",
                             "the rhythm section understands what the genre requires and delivers it honestly"],
                "high":     ["this carries the philosophical and sonic weight of the serious reggae tradition — not just groove but actual meaning",
                             "a record that honors the lineage without becoming a nostalgia act — a difficult balance"],
                "perfect":  ["reggae music at this level becomes a political and spiritual statement — this achieves both simultaneously",
                             "the completeness of this record — rhythmically, lyrically, philosophically — places it among the great reggae works"],
            },
            "country": {
                "low":      ["country music's most cynical form: all the aesthetic markers, none of the emotional truth",
                             "Hank Williams wrote from inside his pain — this is written from a conference room about someone else's"],
                "mid_low":  ["the country framing limits the scope without the emotional honesty that makes the genre's best work transcend those limits",
                             "the structural and lyrical conventions are reproduced here without the feeling that justifies them"],
                "mid_high": ["the country tradition is engaged with more honesty than I expected — the storytelling has some genuine weight",
                             "credible on its own terms — the craft is present if not exceptional"],
                "high":     ["this is country that earns the comparison to the outlaw tradition — a genuine artistic statement within the form",
                             "the emotional directness here is the genre's great virtue, and this deploys it without sentimentality"],
                "perfect":  ["I have long dismissed commercial country — this record challenges that dismissal entirely",
                             "the depth of feeling here rivals the great outlaw country records — a complete artistic achievement"],
            },
            "soul": {
                "low":      ["soul music is built on transmitting real emotion — this transmits nothing",
                             "Aretha Franklin redefined what a human voice could carry — this record doesn't even try"],
                "mid_low":  ["the soul elements are applied as atmosphere rather than felt as substance — cosmetic rather than structural",
                             "the soulfulness is performed rather than lived, and anyone paying attention can hear the difference"],
                "mid_high": ["the soul tradition brings genuine warmth to the melodic choices — it elevates the material",
                             "the soulful elements lift this above the generic — the feeling is real, even if it isn't transcendent"],
                "high":     ["this sits close to the great soul records in its emotional honesty — the transmission is genuine",
                             "SZA at her most emotionally honest operates in this space — this record belongs there"],
                "perfect":  ["soul music at this level stops being genre and becomes testimony — this record carries that weight completely",
                             "I haven't been this moved by a soul record in years. a perfect ten."],
            },
            "folk": {
                "low":      ["folk music carries the weight of memory and place — this record carries nothing",
                             "Phoebe Bridgers builds songs that hit like actual memory — this is tourism in comparison"],
                "mid_low":  ["the storytelling tradition in folk requires honesty and specificity — this has neither in enough supply",
                             "the folk aesthetic is present but the narrative intelligence that gives it meaning isn't developed enough"],
                "mid_high": ["folk music at its best carries real memory — this one does, in its better moments",
                             "the storytelling tradition in folk is alive in this record — not perfectly, but genuinely"],
                "high":     ["folk done right is a conversation with the past that stays completely present — this is that",
                             "this sits in the lineage of artists like Bon Iver or Sufjan Stevens — not derivative, but genuinely connected"],
                "perfect":  ["folk music this emotionally complete and this narratively honest belongs among the great records in the form",
                             "a perfect folk record: every lyric earns its place, every melody serves the story"],
            },
            "blues": {
                "low":      ["the blues tradition carries more human truth per note than almost anything — this wastes every note",
                             "Gary Clark Jr. at his worst is more honest than this record at its best"],
                "mid_low":  ["the blues elements are present but the feeling is performed rather than lived — the gap is audible",
                             "the twelve-bar structure is here without the humanity it was designed to carry"],
                "mid_high": ["the blues tradition carries weight and this record doesn't run from that weight — which is exactly right",
                             "the lineage is honored here, not just name-dropped — the approach shows real understanding"],
                "high":     ["real blues is about the weight of experience, and this record carries that weight honestly — rare in contemporary music",
                             "this reminds me why blues changed everything when it arrived — the feeling is genuine"],
                "perfect":  ["blues music this honest and this complete is something I thought I might not hear again — this belongs next to the greats. ten.",
                             "I've been waiting a long time for a record to make me feel this way. this is it. a perfect ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"as a {g} release, it occupies its genre without transcending it" if tier in ("low","mid_low") else
            f"the {g} direction shows a real understanding of what the genre can do" if tier in ("mid_high","high") else
            f"the {g} architecture here is as complete as the form allows — a definitive statement",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "existential": {
                "low":      ["the existential angle is just a mood board — there's no actual depth underneath it",
                             "sitting with big questions in music requires real courage and craft — this has neither"],
                "mid_low":  ["the existential undertone is present but underdeveloped — it points at something and then walks away",
                             "the philosophical ambition is visible but not realized — which is almost more frustrating than no ambition at all"],
                "mid_high": ["the existential undertow here is the record's most compelling quality — it sits with difficult questions",
                             "it doesn't try to resolve the questions it raises, which is the honest approach"],
                "high":     ["grappling with the void is the oldest tradition in art — and this earns its place in it, genuinely",
                             "existential themes this well-handled remind me of early Radiohead: heavy, but earned"],
                "perfect":  ["the philosophical depth here is as complete as the music — this is a rare and total artistic achievement",
                             "I've only felt this kind of existential weight in a handful of records — this joins that list"],
            },
            "spirituality": {
                "low":      ["the spiritual theme is gestured at without any actual depth — it's a vibe, not a belief",
                             "spirituality in music requires a genuine reckoning — this is a Pinterest board about it"],
                "mid_low":  ["the spiritual dimension is present but it doesn't earn its transcendence — it claims the feeling without generating it",
                             "the sacred needs to feel sacred — this feels staged"],
                "mid_high": ["the spiritual element adds real weight — it's earned, not just applied as atmosphere",
                             "it approaches transcendence without getting preachy or vague — a difficult balance"],
                "high":     ["the sense of the sacred here is genuine — I can hear the belief behind it",
                             "spirituality in music that actually connects to something larger is rare — this achieves it"],
                "perfect":  ["the spiritual completeness here is extraordinary — music and belief unified in a way that produces something genuinely transcendent",
                             "I have not heard the sacred expressed this honestly in contemporary music since Kanye's 808s-era ambitions — and this surpasses that"],
            },
            "party": {
                "low":      ["a party theme is a refusal to mean anything — and at this level, it's not even a fun refusal",
                             "hedonism in art requires a justification this record doesn't bother to provide"],
                "mid_low":  ["the festive framing drains whatever potential existed — the fun isn't even working",
                             "party music that doesn't make you want to party is a complete failure of mission"],
                "mid_high": ["the party energy has a propulsive quality that earns more credit than I want to give it",
                             "there's an honesty to the hedonism here — it doesn't pretend to be anything else"],
                "high":     ["party music at this level becomes a genuine celebration of what music can do when it's unguarded",
                             "even I can admit that joy, done this well, is an artistic achievement"],
                "perfect":  ["an entire genre dedicated to celebrating living — and this record is its finest argument",
                             "I didn't think party music could move me. I was wrong. a perfect ten."],
            },
            "protest": {
                "low":      ["protest music is only protest music if it's uncomfortable — this is a strongly worded note",
                             "the political angle here is so diluted it becomes decoration rather than statement"],
                "mid_low":  ["the protest intent is there but the execution is too cautious — real protest music doesn't hedge",
                             "the political content is present without the courage to push it where it needs to go"],
                "mid_high": ["protest music is at its best when it's uncomfortable — this doesn't shy away from that discomfort",
                             "the political dimension is handled with care rather than sloganeering — that's the right approach"],
                "high":     ["this carries the tradition of protest music honestly — confrontational, specific, and necessary",
                             "politically engaged music this clear-eyed and well-crafted reminds me of Kendrick's Section.80 — serious and pointed"],
                "perfect":  ["protest music this complete — sonically, lyrically, politically — is a rare and important thing",
                             "a perfect protest record: it makes you feel something and then makes you think about why"],
            },
            "nostalgia": {
                "low":      ["nostalgia done wrong is just sentimentality — and this doesn't have the craft to be anything else",
                             "the nostalgic theme is used here as an emotion substitute rather than an actual emotion"],
                "mid_low":  ["the retrospective feeling is present but not earned — you need real memory to access real nostalgia",
                             "the nostalgia is applied from the outside rather than coming from somewhere genuine"],
                "mid_high": ["nostalgia done right isn't self-pity — it's a reckoning with what was real and what was lost",
                             "the nostalgic register is handled with enough self-awareness to avoid becoming just wistfulness"],
                "high":     ["the historical feeling embedded in this is genuinely moving — it mourns something specific and real",
                             "nostalgia at this level is the closest music gets to actual memory — this achieves it"],
                "perfect":  ["the nostalgic feeling here is so complete and so honest that it transcends the theme entirely — this is a record about what it means to remember",
                             "I felt something I haven't felt in years listening to this. a perfect ten."],
            },
            "love": {
                "low":      ["love songs have been so thoroughly exhausted that writing one now requires a real reason — this doesn't have one",
                             "the love theme is applied without any new angle on it — there's nothing here that hasn't been said better elsewhere"],
                "mid_low":  ["the emotional terrain is familiar and this doesn't offer enough to justify revisiting it",
                             "love songs only work when they're specific — this is too general to land"],
                "mid_high": ["love as a theme is a classic for a reason — and this handles it with enough sincerity to earn the territory",
                             "the love narrative here has real feeling in it — it's not just going through the motions"],
                "high":     ["love songs at this level stop being genre moves and become genuine transmissions — this is genuinely felt",
                             "the emotional specificity here puts me in mind of Frank Ocean's best work — not imitation, but the same level of honesty"],
                "perfect":  ["love as a theme — done this honestly, this completely — becomes one of the most powerful things music can be",
                             "I've heard thousands of love songs. this belongs among the best of them. a perfect ten."],
            },
            "heartbreak": {
                "low":      ["heartbreak music that doesn't actually hurt is just sad-adjacent aesthetics",
                             "the heartbreak theme is performed rather than felt — the emotional gap is audible"],
                "mid_low":  ["the vulnerability the heartbreak theme requires isn't fully present — it stops just short of honest",
                             "heartbreak songs need specificity to land — this stays too general to connect"],
                "mid_high": ["heartbreak is the oldest subject in music and this handles it with real emotional intelligence",
                             "the vulnerability required by this theme is present here — and it's the record's strongest quality"],
                "high":     ["heartbreak done this honestly is the closest music gets to actually sharing pain — this achieves that transfer",
                             "this sits in the lineage of artists like Olivia Rodrigo at her most direct — raw, specific, and completely real"],
                "perfect":  ["heartbreak this thoroughly and honestly expressed is a rare thing — this record will mean something to everyone who's ever needed it",
                             "the emotional completeness here is extraordinary. I felt it. a perfect ten."],
            },
            "street life": {
                "low":      ["the street life theme here is a costume — the specificity that makes it real is completely absent",
                             "cultural authenticity isn't optional in this theme — it's the entire point, and it's missing"],
                "mid_low":  ["the street life angle is present without the lived detail that makes it land",
                             "the theme is gesturing at a reality without actually inhabiting it — the gap shows"],
                "mid_high": ["the street life theme is handled with enough authenticity that it doesn't feel borrowed",
                             "the cultural specificity here is real — the detail is lived, not researched"],
                "high":     ["the street life narrative here is as honest as the best hip hop journalism — specific, unromantic, and true",
                             "this belongs in the lineage of records that documented real experience with real craft"],
                "perfect":  ["street life documented with this level of honesty and artistry becomes permanent — this record will matter for decades",
                             "the best street life music is also the most universal — this achieves that paradox completely. ten."],
            },
            "rage": {
                "low":      ["rage without an object is just noise — and this rage has no target",
                             "anger in music needs to be specific to be meaningful — this is diffuse and therefore meaningless"],
                "mid_low":  ["the rage is present but it hasn't found the thing it's actually angry about",
                             "the anger here is real but it needs sharpening — right now it's more of a mood than a statement"],
                "mid_high": ["rage as a theme is underrepresented in critical coverage and overrepresented in actual human experience — this is valid",
                             "the anger here is channeled into music rather than dissipated — a legitimate and rare artistic choice"],
                "high":     ["rage this focused and this articulated is one of the most powerful things music can be",
                             "this carries the focused anger of the best protest music — specific, earned, and necessary"],
                "perfect":  ["rage done this completely — specific, structural, and emotionally full — is a permanent artistic achievement",
                             "I don't usually champion anger as an artistic mode. this record changed that. a perfect ten."],
            },
            "euphoria": {
                "low":      ["euphoria as a theme tends to produce music that asks nothing of the listener — this asks less than nothing",
                             "the emotional territory here is deliberately shallow, which is a creative choice I find impossible to respect"],
                "mid_low":  ["the euphoric mode is executed competently but the shallowness of the terrain limits what's achievable",
                             "joy is a legitimate emotional subject — this doesn't find anything interesting to say within it"],
                "mid_high": ["the euphoric feeling here has more depth than the theme usually allows — there's something real underneath the joy",
                             "euphoria done with this level of intention is harder to dismiss than I expected"],
                "high":     ["joy at this level of musical realization is actually an intellectual achievement — this earns it",
                             "pure positive feeling made this honestly is harder than it looks — this record understands that"],
                "perfect":  ["euphoria this complete and this genuinely realized becomes a kind of transcendence — music at its most life-affirming",
                             "I didn't think I could give a ten to a euphoria record. I was wrong. this is a perfect ten."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {t} theme is functional but doesn't add a layer I find particularly interesting" if tier in ("low","mid_low") else
            f"the {t} direction is handled with real care — it earns its place in the record" if tier in ("mid_high","high") else
            f"the {t} theme is realized so completely that it defines the record — a rare achievement",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 360:
            return [pick(["the extended runtime is justified — it takes the time it needs and not a second more",
                          "at this length, a weaker record would fall apart — this holds, which is a genuine achievement"])]
        if d > 240:
            return [pick(["the duration is measured and appropriate — it doesn't overstay its welcome",
                          "the runtime reflects real discipline, which I always appreciate"])]
        if d < 120:
            return [pick(["at this length, nothing can breathe — and this needed room to breathe",
                          "the brevity feels like a refusal to commit to anything, which is its own kind of failure"])]
        return [pick(["the runtime accommodates the material — neither a virtue nor a flaw",
                      "it's neither too short nor too long — a basic thing that many artists still get wrong"])]


# ─────────────────────────────────────────────
#  CRITIC 2 — DEJA HAYES  (Hype Queen, Pop/R&B/Soul enthusiast)
# ─────────────────────────────────────────────

class DejaHayes(Critic):
    name         = "Deja Hayes"
    tagline      = "Founder, PulseLine Media"
    verdict_type = "hype"

    loved_genres    = ["pop", "r&b", "soul"]
    liked_genres    = ["hip hop", "electronic", "reggae"]
    disliked_genres = ["metal", "classical"]
    hated_genres    = ["punk", "experimental"]

    loved_themes    = ["love", "party", "euphoria"]
    disliked_themes = ["rage", "existential"]

    base_modifier = 1.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      ["even by pop standards this is underbaked — the hooks aren't there and the feeling isn't either",
                             "pop music has one job: make you feel something fast. this does not do that job.",
                             "this is what pop sounds like when nobody actually cared while making it"],
                "mid_low":  ["the pop formula is applied but the magic isn't — it checks boxes without delivering anything",
                             "I wanted to love this and it just... gave me nothing to hold onto"],
                "mid_high": ["a pop record that knows exactly what pop is for — immediate, infectious, and completely unapologetic about it",
                             "the pop construction here is sharp — every hook lands where it needs to"],
                "high":     ["this is pop doing what pop does best at the highest level — SZA or Doja Cat energy, modern execution",
                             "the kind of pop record that reminds you why you fell in love with pop in the first place"],
                "perfect":  ["I've played this six times and each time it hits harder — flawless pop is rare and this is flawless",
                             "this is the reason pop music exists and I mean that completely — a perfect ten"],
            },
            "r&b": {
                "low":      ["the r&b groove is technically there but the feeling is completely missing — this is r&b without a soul",
                             "Frank Ocean made music in a state of genuine feeling — this was made in a state of calculation"],
                "mid_low":  ["smooth but empty — the groove is borrowed and the emotion is rented",
                             "the r&b elements slide past without connecting — close but never landing"],
                "mid_high": ["the r&b DNA runs deep here and it shows in every melodic choice — the groove is undeniable",
                             "there's an emotional warmth to this r&b approach that really works"],
                "high":     ["this is what r&b sounds like when it's completely in the pocket — effortless, warm, and real",
                             "early Daniel Caesar or H.E.R. energy — that kind of intimate intensity that's hard to fake"],
                "perfect":  ["r&b has not sounded this essential in years — this is a landmark record and I'm saying that clearly",
                             "the emotional completeness here is what I chase in every review. I found it. ten."],
            },
            "soul": {
                "low":      ["soul music is about passing real feeling from one person to another — this passes nothing",
                             "Aretha could make a ceiling open with her voice alone. this has a full production budget and achieves nothing."],
                "mid_low":  ["sounds like soul without feeling like it — a frustrating and meaningful difference",
                             "the soul elements are there cosmetically but the conviction underneath is missing"],
                "mid_high": ["genuine soul is rare and this has it — you can hear that the artist actually felt something",
                             "the soulful texture here lifts this above the average — it has the warmth the genre is built on"],
                "high":     ["this is the real thing — the kind of soul that makes you feel less alone while you're listening",
                             "early Solange or Alicia Keys energy — that kind of intimate power that you either have or you don't"],
                "perfect":  ["soul music this complete is what the entire genre has been building toward — a perfect ten and I mean it",
                             "I cried a little. that's my full review. ten out of ten."],
            },
            "hip hop": {
                "low":      ["the hip hop energy isn't landing — flat beat, bars that say nothing",
                             "hip hop requires presence — this record is absent from itself"],
                "mid_low":  ["goes through the motions — the production is competent and the spark isn't there",
                             "the bars are delivered but they're not doing anything with the delivery"],
                "mid_high": ["the hip hop energy here hits — confident production and a real voice behind it",
                             "this is hip hop that earns your attention and keeps it"],
                "high":     ["genuinely hard hip hop — the kind of record that makes you want to find who made it immediately",
                             "the production has depth that rewards repeat listens, and the lyricism matches it"],
                "perfect":  ["this is the hip hop record I've been waiting for — it belongs next to the classics and I'm not scared to say that",
                             "the beat, the bars, the feeling — everything in service of something real. a perfect ten."],
            },
            "electronic": {
                "low":      ["walls of sound without a single feeling in sight — not for me at all",
                             "the electronic production is technically present and emotionally completely absent"],
                "mid_low":  ["interesting on paper but cold in execution — music needs to feel good and this misses that",
                             "the unconventional structure makes it really hard to connect with emotionally"],
                "mid_high": ["the electronic production here creates a mood and holds it — that's more than most manage",
                             "the sound design is genuinely engaging — I got more into it than I expected"],
                "high":     ["this is electronic music with real emotional range — I was moving before I noticed I'd started",
                             "the production is layered in the best way — KAYTRANADA or Disclosure energy but with its own identity"],
                "perfect":  ["electronic music this emotionally full is a genuine event — a perfect record",
                             "I'm not usually here for this kind of production but this converted me completely. ten."],
            },
            "metal": {
                "low":      ["the metal direction turns a lot of people off and for this one I'm in that group",
                             "the heaviness works against every quality I look for in music — connection, warmth, feeling"],
                "mid_low":  ["metal has its place but that place is far from where I spend my listening time",
                             "the approach creates distance where I need connection — not landing for me at all"],
                "mid_high": ["the heaviness has more emotional range than I expected — moments that actually break through",
                             "not my world but I can feel what it's going for, and it's going there with conviction"],
                "high":     ["the metal intensity is channeled into something with genuine feeling — I'm a surprised convert on this one",
                             "this pushed past my reservations through sheer emotional force — real respect for that"],
                "perfect":  ["I don't say this often in this genre but: this is a perfect record. the feeling is undeniable.",
                             "metal that makes me feel instead of flinch — a ten that I'm genuinely amazed to give"],
            },
            "punk": {
                "low":      ["the punk framing is aggressive in a way that really doesn't translate to how I receive music",
                             "not my lane at all — friction where I want connection, and nothing in return"],
                "mid_low":  ["the rawness isn't doing enough work to justify what it costs the listener",
                             "punk energy can be exciting — this is more abrasive than it is compelling"],
                "mid_high": ["the punk conviction here is real — it doesn't try to be likeable and somehow that ends up being likeable",
                             "there's an honesty to the rawness that I can appreciate even outside my usual world"],
                "high":     ["something unexpectedly emotional underneath the abrasion — this record genuinely surprised me",
                             "the punk energy breaks through my usual resistance through sheer genuine feeling"],
                "perfect":  ["a perfect punk record — every rough edge is load-bearing, nothing wasted. ten.",
                             "punk this complete and this honest is something I didn't expect to love. here we are."],
            },
            "experimental": {
                "low":      ["experimental as a tag should mean something — here it just means hard to listen to",
                             "the unconventional structure has no emotional destination and the journey is rough"],
                "mid_low":  ["makes emotional connection really difficult without compensating with enough else",
                             "interesting on paper but music needs to feel good too, and this consistently misses that"],
                "mid_high": ["the experimental texture is challenging but opens up with patience — I found myself in it eventually",
                             "not easy listening but genuinely rewarding if you meet it halfway"],
                "high":     ["experimental music that actually makes me feel something — that's the whole argument for the genre",
                             "the unconventional production creates an emotional world that rewards full immersion"],
                "perfect":  ["I don't usually champion experimental music but this is too complete to call it niche — it's universal. ten.",
                             "perfect experimental music: challenging and emotionally complete at the same time. floored."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"as a {g} track, the feeling just isn't connecting the way I need it to" if tier in ("low","mid_low") else
            f"as a {g} track it's doing what it needs to and doing it with real feeling" if tier in ("mid_high","high") else
            f"the {g} energy is pure and complete here — a definitive version of what this genre can be",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "love": {
                "low":      ["the love angle is there but the actual feeling isn't — it goes through the motions without connecting",
                             "love songs need real vulnerability to land and this keeps its distance the whole time"],
                "mid_low":  ["the love theme is handled safely when it should be handled honestly",
                             "I can see what it's reaching for emotionally — it doesn't fully get there"],
                "mid_high": ["love as a theme is a classic for a reason and this handles it with real sincerity",
                             "the love narrative hits the right emotional notes without being too over the top"],
                "high":     ["the love theme here is handled with the kind of warmth that makes you feel seen",
                             "this is what a love song is supposed to do — Ariana Grande's best work operates in this space"],
                "perfect":  ["a perfect love song: emotionally complete, completely sincere, and impossible to walk away from unchanged",
                             "I'm emotional. this is what love music is supposed to be. a perfect ten."],
            },
            "party": {
                "low":      ["a party track that doesn't make you want to move is a failed party track — this failed",
                             "the festive energy is totally flat — this is a party where nobody showed up"],
                "mid_low":  ["the party energy is trying but not quite there — the momentum keeps dropping",
                             "it aims for euphoria and lands somewhere just below actually fun"],
                "mid_high": ["the party energy is immaculate — this is what playlist builders dream about",
                             "I felt this one physically, which is literally the whole point"],
                "high":     ["the festive vibe is executed with the kind of confident joy that made Beyoncé's Renaissance work",
                             "this is a party track that would actually make a party better — that's the whole mission"],
                "perfect":  ["a perfect party record — pure joyful energy that never lets up. ten.",
                             "this is what the best night out sounds like. a flawless party track. ten."],
            },
            "euphoria": {
                "low":      ["the euphoric theme is performed rather than felt — the joy doesn't reach through the speakers",
                             "music about feeling great should make you feel great. this doesn't."],
                "mid_low":  ["the euphoric energy is present in the production but the core feeling isn't connecting",
                             "aims for pure joy and lands somewhere more like mild okayness"],
                "mid_high": ["the euphoric feeling here is infectious in the best way — pure positive energy",
                             "music that makes you feel good without apologizing for it — this is a great example"],
                "high":     ["the euphoric mode here is fully realized — Doja Cat or Lizzo energy, completely unguarded",
                             "pure feel-good power that doesn't apologize for existing and shouldn't have to"],
                "perfect":  ["euphoria done this completely is a gift — flawless positive energy from start to finish. ten.",
                             "I was grinning the whole time. that's a perfect ten. easy."],
            },
            "heartbreak": {
                "low":      ["heartbreak music without real emotion is just sad aesthetics — this is the sad aesthetic version",
                             "the vulnerability this theme needs isn't here — it keeps the real feeling at arm's length"],
                "mid_low":  ["the heartbreak theme is present but it stays surface-level — needs more rawness to really land",
                             "I've felt more emotion in the middle eight of a random pop song than in this whole record"],
                "mid_high": ["the heartbreak theme lands with real emotional weight — the vulnerability is actually there",
                             "this delivers the kind of emotional honesty that Olivia Rodrigo built a career on"],
                "high":     ["the heartbreak here is raw and specific — exactly what the theme needs to actually hurt in the right way",
                             "this is devastating in the best sense — SZA's Good Days energy, pure emotional honesty"],
                "perfect":  ["a perfect heartbreak record — so honest it actually hurts to listen to. that's the whole point. ten.",
                             "I'm emotional and I don't care who knows. this is a perfect ten."],
            },
            "rage": {
                "low":      ["the rage theme is a barrier for me and this record doesn't do anything to bridge that",
                             "I need my music to pull me forward — rage themes that go nowhere aren't for me"],
                "mid_low":  ["the anger is there but it doesn't go anywhere useful — it just hangs in the air",
                             "the rage theme creates an emotional wall between me and the record"],
                "mid_high": ["I get the anger and the production channels it in a way that actually connects",
                             "rage as a theme works here because there's a real feeling underneath it, not just aggression"],
                "high":     ["the rage here is specific and earned — Billie Eilish's angrier moments but with more fire",
                             "even I can get behind rage music when it's this emotionally honest and this well-executed"],
                "perfect":  ["rage done this completely and this purposefully is an artistic statement I can fully get behind. ten.",
                             "a perfect rage record — focused, honest, and impossible to look away from. ten."],
            },
            "nostalgia": {
                "low":      ["the nostalgia here feels borrowed rather than real — it's performing wistfulness, not feeling it",
                             "nostalgia music that doesn't actually make you feel nostalgic has missed the entire assignment"],
                "mid_low":  ["the nostalgic angle is present without the genuine memory that makes it resonate",
                             "the retrospective feeling is applied from the outside — it doesn't come from a real place"],
                "mid_high": ["the nostalgic energy here is warm and genuine — it actually takes me somewhere",
                             "the theme is handled with the kind of sincerity that makes nostalgia music work"],
                "high":     ["the nostalgic feeling here is real — Taylor Swift's folklore-era intimacy, completely genuine",
                             "this made me think of specific good memories. that's the whole job of nostalgia music."],
                "perfect":  ["nostalgia this warm and this genuine is a rare gift — a perfect record. ten.",
                             "I felt things I haven't felt in years. that's a perfect ten."],
            },
            "existential": {
                "low":      ["existential themes weigh this down when it could be soaring — not the energy I need",
                             "the heaviness of the theme pulls against the music in a way that frustrates me"],
                "mid_low":  ["deep themes can be powerful but this one is more heavy than illuminating",
                             "the existential angle creates a weight that the production isn't built to hold"],
                "mid_high": ["the existential depth here adds something real to the record without becoming a downer",
                             "big themes handled with this much care land differently — I feel something genuine"],
                "high":     ["the existential feeling here is handled with a lightness that makes the depth feel like a gift",
                             "Lorde at her most philosophical operates in this territory — this earns that comparison"],
                "perfect":  ["existential themes this beautifully handled produce some of music's most important records — this is one. ten.",
                             "I didn't expect to feel this much. a perfect ten."],
            },
            "street life": {
                "low":      ["the street life angle doesn't feel lived — it feels like a reference without the experience",
                             "cultural authenticity is everything in this theme — it's missing here"],
                "mid_low":  ["the theme is present without the detail that makes it real",
                             "the street life narrative needs specificity — this stays too broad to connect"],
                "mid_high": ["the street life theme is handled with enough authenticity that it feels real, not borrowed",
                             "the lived detail is there — this isn't a tourist take on the subject"],
                "high":     ["the street life narrative here is honest and specific — early Kendrick or J. Cole energy",
                             "this belongs in the lineage of artists who documented real experience with real craft"],
                "perfect":  ["street life documented with this level of honesty becomes permanent — a ten.",
                             "a perfect take on the theme: specific, honest, and unforgettable. ten."],
            },
            "protest": {
                "low":      ["protest music needs to make you uncomfortable — this is a strongly worded tweet at best",
                             "the political edge here is too dull to cut anything"],
                "mid_low":  ["the protest intent is there but it's too cautious — real protest music doesn't hedge",
                             "the message is present without the courage to push it where it needs to go"],
                "mid_high": ["the protest energy is real and the message lands without becoming preachy",
                             "politically engaged music that actually makes you feel the stakes — that's hard to do"],
                "high":     ["protest music this clear and this emotionally powerful reminds me of Beyoncé's Lemonade — intentional and necessary",
                             "the message here is sharp and the music carries it — a real combination"],
                "perfect":  ["a perfect protest record: it moves you emotionally and makes you think. ten.",
                             "this is what it sounds like when music has something real to say. ten."],
            },
            "spirituality": {
                "low":      ["the spiritual theme is present as a mood board — there's no actual depth underneath",
                             "spirituality in music requires genuine belief — this is aesthetic, not feeling"],
                "mid_low":  ["the spiritual feeling is gestured at without being generated",
                             "the sacred doesn't feel sacred here — it feels like production choices"],
                "mid_high": ["the spiritual dimension adds genuine warmth and feeling to the record",
                             "the theme is handled with sincerity — it lifts the whole thing"],
                "high":     ["the spiritual energy here is genuinely moving — Chance the Rapper's most open-hearted moments, that kind of warmth",
                             "music that reaches toward something larger and actually gets there — rare and beautiful"],
                "perfect":  ["spirituality expressed this honestly in music is a transcendent thing — a perfect ten.",
                             "this lifted me. that's a perfect ten and I mean every word of it."],
            },
            "euphoria": {
                "low":      ["the euphoric theme is performed rather than felt — the joy doesn't reach through the speakers",
                             "music about feeling great should make you feel great. this doesn't."],
                "mid_low":  ["the euphoric energy is present in the production but the core feeling isn't connecting",
                             "aims for pure joy and lands somewhere more like mild okayness"],
                "mid_high": ["the euphoric feeling here is infectious in the best way — pure positive energy",
                             "music that makes you feel good without apologizing for it — this is a great example"],
                "high":     ["the euphoric mode here is fully realized — Doja Cat or Lizzo energy, completely unguarded",
                             "pure feel-good power that doesn't apologize for existing and shouldn't have to"],
                "perfect":  ["euphoria done this completely is a gift — flawless positive energy from start to finish. ten.",
                             "I was grinning the whole time. that's a perfect ten. easy."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {t} theme just isn't connecting emotionally for me" if tier in ("low","mid_low") else
            f"the {t} theme lands well — it gives the track a clear identity" if tier in ("mid_high","high") else
            f"the {t} theme is handled so perfectly here it becomes what the record is — a complete emotional achievement",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick(["the length is a bit much — I start losing focus past a certain point",
                          "trimming this would have made the energy hit harder from start to finish"])]
        if d < 150:
            return [pick(["short and punchy — I love when a song doesn't overstay its welcome",
                          "the brevity works in its favour — leaves you wanting more"])]
        return [pick(["the runtime is right in the sweet spot — keeps you engaged without losing you",
                      "the perfect length: gets in, delivers, and gets out"])]


# ─────────────────────────────────────────────
#  CRITIC 3 — VIC OSEI  (Blunt, Cap of ~6/7, rude and nonchalant)
# ─────────────────────────────────────────────

class VicOsei(Critic):
    name         = "Vic Osei"
    tagline      = "Somewhere Online"
    verdict_type = "blunt"

    # Has problems with EVERY genre and theme — no loved/liked
    loved_genres    = []
    liked_genres    = []
    disliked_genres = ["pop", "r&b", "soul", "folk", "country", "reggae", "classical"]
    hated_genres    = ["electronic", "experimental"]

    loved_themes    = []
    disliked_themes = ["euphoria", "party", "love", "nostalgia", "spirituality"]

    base_modifier = -2.5   # hard floor — he almost never goes above 7

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      ["pop. okay. no.", "this is why people say pop is dead.", "four chords and a sad story. next."],
                "mid_low":  ["it's a pop song. it does pop song things. cool I guess.", "predictable like a bus schedule."],
                "mid_high": ["it's pop and it actually functions. I didn't hate it. that's something.",
                             "does the pop thing competently. annoying to admit but it works."],
                "high":     ["okay fine — this pop record actually has something going on. barely but it does.",
                             "it's pop but it's sharp pop. I don't love it but I respect it."],
                "perfect":  ["fine. it's great pop. whatever.", "this is genuinely excellent pop. I hate that I have to write that."],
            },
            "hip hop": {
                "low":      ["bars? what bars?", "the beat is lazy and the rapping is lazier.",
                             "hip hop deserves better than this."],
                "mid_low":  ["it rhymes. that's the nicest thing I've got.", "mediocre bars over a mediocre beat. matching energy."],
                "mid_high": ["the hip hop here is decent. the bars land enough of the time.",
                             "actually a functional hip hop record — I've heard way worse."],
                "high":     ["this hip hop record is legitimately good. I'm annoyed but I'm saying it.",
                             "solid bars, solid beat. this works more than I expected."],
                "perfect":  ["yeah okay this is actually a great hip hop record. sure.", "the bars are elite. the beat is elite. fine."],
            },
            "rock": {
                "low":      ["loud but not in a way that means anything.", "it's rock. it rocks. very slightly.",
                             "guitar and drums and nothing interesting happening with either."],
                "mid_low":  ["the rock energy is there but the ideas aren't.", "it's fine rock. forgettable rock."],
                "mid_high": ["decent rock record. the energy is real enough.", "it's got some actual fire in it. I can work with that."],
                "high":     ["this rock record is genuinely good. I didn't see that coming.", "actually sharp rock music. respect."],
                "perfect":  ["fine. great rock record. whatever.", "this rock is excellent. I'm almost proud of it."],
            },
            "electronic": {
                "low":      ["what is this.", "someone made this and said yeah, send it.", "it's a bunch of sounds. that's it."],
                "mid_low":  ["the production is just happening at me. not to me.", "electronic music that doesn't know what it wants to be."],
                "mid_high": ["okay the production is actually doing something here. I'll allow it.",
                             "the electronic work here is more interesting than it has any right to be."],
                "high":     ["the production is genuinely impressive and I don't say that often.",
                             "this electronic music actually hits. rare."],
                "perfect":  ["the production is elite. I don't get it but I feel it. sure.", "okay this is actually brilliant production. fine."],
            },
            "experimental": {
                "low":      ["no.", "I am not the audience for this and I don't think anyone is.",
                             "this is what happens when an artist stops caring if anyone gets it."],
                "mid_low":  ["trying too hard to be weird. just make music.", "the experimental angle is covering for a lack of actual ideas."],
                "mid_high": ["it's weird but it's controlled weird — I can tell something is actually going on here.",
                             "the experimental choices are odd but they're not random. I'll give it that."],
                "high":     ["this experimental music is actually doing something real. I respect it even if I don't enjoy it.",
                             "the weirdness has a point here. hard to argue with."],
                "perfect":  ["this is experimental music that works on every level. okay. yes. fine.",
                             "genuinely great experimental record. still weird. but great."],
            },
            "metal": {
                "low":      ["very loud. very nothing.", "the heaviness is doing all the work and the heaviness isn't enough.",
                             "anger without direction."],
                "mid_low":  ["the metal stuff is there. the point of it isn't.", "heavy and forgettable."],
                "mid_high": ["the metal here is actually structured. the intensity is going somewhere.",
                             "loud in a way that makes sense. acceptable."],
                "high":     ["this metal record has real craft in it. I didn't think I'd type that.",
                             "heavy and intelligent. those two things together are rarer than they should be."],
                "perfect":  ["fine. it's a perfect metal record. sure. whatever.", "this is elite metal. I have no complaints. bizarre."],
            },
            "punk": {
                "low":      ["angry for no reason. classic.", "the aggression has no target. that's just noise.",
                             "punk needs a point. this doesn't have one."],
                "mid_low":  ["the punk energy is there but the brain behind it isn't.",
                             "raw and undirected. not the good kind of raw."],
                "mid_high": ["the punk here is sharp enough to cut something. I'll take it.",
                             "actually has conviction. I can respect that."],
                "high":     ["okay this punk record has real ideas in it. that matters.",
                             "the anger is focused and the craft is there. good."],
                "perfect":  ["perfect punk record. sharp, smart, and necessary. fine.", "yeah this is elite punk. whatever."],
            },
            "jazz": {
                "low":      ["jazz that doesn't know it's jazz.", "technically jazz. not actually interesting.",
                             "jazz for people who don't really like jazz."],
                "mid_low":  ["the jazz elements are competent and not particularly engaging.", "it's jazz. mid jazz."],
                "mid_high": ["the jazz is done with actual intelligence here. the musicianship is real.",
                             "decent jazz that earns its genre tag."],
                "high":     ["this jazz is genuinely skilled. I'm surprised but I'm saying it.",
                             "the musicianship here is hard to argue with."],
                "perfect":  ["yeah. great jazz record. fine. ten out of ten.", "elite musicianship. flawless record. sure."],
            },
            "classical": {
                "low":      ["it's boring and it doesn't even have the excuse of being old.",
                             "classical music that doesn't justify its own length."],
                "mid_low":  ["the classical framework is here. the purpose of it isn't.",
                             "technically competent classical music. emotionally nothing."],
                "mid_high": ["the classical work here is more interesting than the genre usually gives me.",
                             "some actual ideas in the structure. I can acknowledge that."],
                "high":     ["the classical craft here is exceptional. I won't pretend otherwise.",
                             "this is serious music and it earns that."],
                "perfect":  ["flawless classical record. I don't enjoy it but it's flawless. ten.", "perfect. sure."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [pick(tier_pool)]    # Vic only gives ONE line — he's brief
        # Generic blunt fallback
        if tier in ("low", "mid_low"):
            return [pick([f"it's {g}. not working.", f"the {g} stuff is here. so what.", f"mediocre {g} record."])]
        elif tier in ("high", "perfect"):
            return [pick([f"the {g} is done well. annoying how well.", f"solid {g} record. okay. fine."])]
        return [pick([f"it's a {g} record. it does {g} things. middling.", f"acceptable {g} music. nothing more."])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "love": {
                "low":      ["another love song. great.", "love music that doesn't make you feel love. impressive failure."],
                "mid_low":  ["the love theme is fine. everybody does love. whatever.", "safe and expected. love theme. sure."],
                "mid_high": ["the love angle works here. still a love song but a decent one.", "it handles love without being annoying about it."],
                "high":     ["the love theme is handled well. rare that that's true.", "actually a good love song. I didn't expect to write that."],
                "perfect":  ["perfect love song. fine.", "flawlessly handled love theme. okay."],
            },
            "party": {
                "low":      ["party song that doesn't make you want to party. big fail.", "I was unbothered. still am."],
                "mid_low":  ["the party energy is there in theory. not in practice.", "it's trying to be fun. it isn't there yet."],
                "mid_high": ["the party theme actually has some momentum here. it moves.", "okay it's fun. I'm annoyed but it's fun."],
                "high":     ["this is a real party track. it actually works.", "the energy is genuine. can't argue with it."],
                "perfect":  ["flawless party record. fine.", "the party energy is perfect. whatever."],
            },
            "euphoria": {
                "low":      ["music about feeling great that doesn't make me feel anything. cool.", "just vibes with no substance."],
                "mid_low":  ["the euphoric angle is more on the surface than in the actual music.", "happy music. unconvincingly happy."],
                "mid_high": ["the euphoric energy actually connects here. I felt something. marginally.", "it's positive in a way that earns it."],
                "high":     ["the euphoric feeling is real here. I'll admit it.", "actually joyful music. rare that it lands."],
                "perfect":  ["perfect euphoric record. whatever. ten.", "flawless. the joy is real."],
            },
            "heartbreak": {
                "low":      ["sad music that isn't actually sad. just looks sad.", "the heartbreak is performed. not felt."],
                "mid_low":  ["the heartbreak theme is okay. expected.", "it's about heartbreak. fine. most songs are."],
                "mid_high": ["the heartbreak lands here. there's actual feeling in it.", "it goes somewhere emotionally. okay."],
                "high":     ["the heartbreak is real and specific. that's what the theme needs.", "this actually hurts a little. mission accomplished."],
                "perfect":  ["perfect heartbreak record. yeah. fine.", "the emotional honesty here is flawless."],
            },
            "street life": {
                "low":      ["street life vibes with zero actual street life.", "the theme is borrowed. it shows."],
                "mid_low":  ["the authenticity is partial. that's not enough for this theme.", "halfway convincing. not convincing enough."],
                "mid_high": ["the street life theme is handled with enough reality that it doesn't feel fake.", "specific enough to land."],
                "high":     ["this street life narrative is honest. the detail is real.", "the lived experience in this is hard to fake. it's not faked."],
                "perfect":  ["perfect execution of the street life theme. specific and honest. ten.", "flawless."],
            },
            "nostalgia": {
                "low":      ["nostalgic for something that probably wasn't that good. cool.", "fake nostalgia. the worst kind."],
                "mid_low":  ["the nostalgic angle is present. so is every other nostalgic record.", "wistful. standard."],
                "mid_high": ["the nostalgia here is genuine enough to be worth something.", "it reaches back and finds something real. okay."],
                "high":     ["the nostalgic feeling is real and it's earned. I'll give it that.", "actually makes you feel something from the past. that's hard."],
                "perfect":  ["perfect nostalgic record. ten.", "flawless execution of something genuinely felt."],
            },
            "rage": {
                "low":      ["angry. no reason. just... angry.", "the rage has no target. that's not art."],
                "mid_low":  ["the anger is present without a point.", "rage with no direction is just noise."],
                "mid_high": ["the rage is focused here. I can see what it's angry at.", "the anger has a point and makes it."],
                "high":     ["the rage is specific and earned. that's the only way this theme works.", "focused anger with real craft behind it."],
                "perfect":  ["perfect execution of rage as a theme. focused, honest, necessary. ten.", "flawless."],
            },
            "existential": {
                "low":      ["trying to be deep. isn't deep.", "big questions, no answers, no music worth sitting through."],
                "mid_low":  ["the existential angle is more posture than actual thought.", "it wants to be meaningful. it isn't quite."],
                "mid_high": ["the existential content has some real weight to it here.", "it's sitting with something genuinely difficult. I can see that."],
                "high":     ["the existential depth here is earned and it lands.", "philosophically honest and musically backed up. rare."],
                "perfect":  ["perfect existential record. ten.", "the depth is complete and the music carries it."],
            },
            "protest": {
                "low":      ["protest music that wouldn't make anyone uncomfortable. useless.", "a note of concern, not a protest."],
                "mid_low":  ["the protest is too cautious to actually protest anything.", "hedging on the political angle. disappointing."],
                "mid_high": ["the protest angle has actual edge here. I can feel what it's pushing against.", "it means what it says."],
                "high":     ["the protest here is sharp and specific. that's the only way this works.", "actually says something. actually means it."],
                "perfect":  ["perfect protest record. necessary and excellent. ten.", "flawless execution."],
            },
            "spirituality": {
                "low":      ["spiritual vibes with no actual spirit.", "it's aesthetic spirituality. the worst kind."],
                "mid_low":  ["the spiritual angle feels performed rather than felt.", "the theme is there. the belief behind it isn't."],
                "mid_high": ["the spiritual element is genuine here. you can hear that it comes from somewhere real.", "it reaches for something and actually touches it."],
                "high":     ["the spirituality here is honest and it lands.", "this comes from a real place. I can tell."],
                "perfect":  ["perfect spiritual record. transcendent and honest. ten.", "flawless."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [pick(tier_pool)]    # one line, he's brief
        return [pick([
            f"the {t} theme is here. so what." if tier in ("low","mid_low") else
            f"the {t} theme actually works here." if tier in ("mid_high","high") else
            f"the {t} theme is handled perfectly. fine.",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick(["too long.", "nobody asked for five minutes of this.", "could have been shorter. should have been."])]
        if d < 150:
            return [pick(["short. fine.", "at least it didn't drag.", "respects your time. barely."])]
        return [pick(["it's the right length.", "runtime is fine. nothing special.", "doesn't overstay. doesn't underwhelm. neutral."])]


# ─────────────────────────────────────────────
#  CRITIC 4 — RAY COLDWELL  (Contrarian)
# ─────────────────────────────────────────────

class RayColdwell(Critic):
    name         = "Ray Coldwell"
    tagline      = "Independent Critic, The Cold Take"
    verdict_type = "contrarian"

    loved_genres    = ["punk", "experimental", "metal", "blues"]
    liked_genres    = ["folk", "hip hop", "jazz"]
    disliked_genres = ["pop", "reggae"]
    hated_genres    = ["r&b", "country"]

    loved_themes    = ["rage", "protest", "existential"]
    disliked_themes = ["love", "euphoria", "party"]

    base_modifier = 0

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "punk": {
                "low":      ["punk without actual conviction is just rehearsed aggression — the Clash had something to say. this doesn't.",
                             "the rawness here is a choice, not a necessity — the scene can smell the difference",
                             "this is the worst kind of punk: the anger is borrowed and the ideas are absent"],
                "mid_low":  ["the punk energy is here but it hasn't found the idea it's supposed to be backing",
                             "the three-chord structure without the necessity that made it revolutionary in the first place"],
                "mid_high": ["punk has no patience for pretense and neither do I — this actually earns its rawness",
                             "the directness here is real — it doesn't try to be liked and ends up being likeable"],
                "high":     ["punk with something to say — the form and content are lined up, which is what the genre always promised",
                             "this carries the conviction of the great punk records without being a museum exhibit about them"],
                "perfect":  ["punk music that fulfills the original promise — confrontational, smart, and necessary. a perfect ten.",
                             "the genre justified by a single record. ten."],
            },
            "experimental": {
                "low":      ["experimental music that fails isn't brave — it's just unfinished",
                             "the unconventional approach here is a defense against having to make actual decisions"],
                "mid_low":  ["gestures at something genuinely interesting without committing to any of it",
                             "the avant-garde posture is here without the structural intelligence that gives it meaning"],
                "mid_high": ["experimental music rewards listeners willing to meet it halfway — I'm meeting it and there's something worth finding",
                             "going to alienate the mainstream, which for this record is probably the correct outcome"],
                "high":     ["the experimental approach invites misreading — a close listen reveals more intention than most reviewers will credit",
                             "sits in the serious experimental tradition and belongs there — the formal choices are purposeful"],
                "perfect":  ["experimental music this formally complete is the rarest thing in any genre — it doesn't just push the boundary, it redraws it. ten.",
                             "history will remember this differently than the present does — a perfect experimental record"],
            },
            "metal": {
                "low":      ["metal is unfairly dismissed by critics who confuse loudness with thoughtlessness — but this record is loud and thoughtless",
                             "the heaviness here is deployed without the compositional intelligence that separates Sabbath from just noise"],
                "mid_low":  ["technically accomplished in moments but lacks the disciplined architecture that great metal requires",
                             "metal at this level needs to justify its weight through structure — this doesn't quite get there"],
                "mid_high": ["metal is unfairly dismissed by critics who confuse loudness with thoughtlessness — this record argues against that dismissal",
                             "the intensity is deployed with genuine craft — more discipline here than the genre gets credit for"],
                "high":     ["heavy music makes reviewers uncomfortable and that discomfort shows up as negative scores — I won't do that here",
                             "this is metal that rewards the analytical attention usually saved for more approved genres"],
                "perfect":  ["metal this structurally complete and emotionally necessary is a permanent argument against the genre's critics — a ten",
                             "a perfect metal record: the weight is justified by the architecture. the architecture by the ideas. ten."],
            },
            "blues": {
                "low":      ["the blues tradition carries more human truth per note than almost any form — and this wastes every note",
                             "Gary Clark Jr. at his worst is more honest than this record at its best"],
                "mid_low":  ["the blues elements are present but the feeling is performed rather than lived — the gap is audible",
                             "the twelve-bar structure without the humanity it was designed to carry"],
                "mid_high": ["the blues tradition carries weight and this doesn't run from that weight — which is exactly right",
                             "you can hear the lineage is honored here, not just name-dropped — the approach shows real understanding"],
                "high":     ["the blues feeling here is authentic — this is the kind of record that holds up to the tradition's best",
                             "sits in the lineage from SRV through Gary Clark Jr. with genuine dignity"],
                "perfect":  ["blues at this level of honesty and craft belongs next to the greats — a complete record. ten.",
                             "I didn't expect to write a perfect score for a blues record. this made me."],
            },
            "folk": {
                "low":      ["folk music without the storytelling is just acoustic guitar and good intentions",
                             "Phoebe Bridgers built a career on specific, honest storytelling — this is vague and borrowed"],
                "mid_low":  ["the folk aesthetic is present but the narrative intelligence that gives it meaning is underdeveloped",
                             "folk without real emotional specificity is just a vibe — and vibes aren't enough"],
                "mid_high": ["the folk tradition is engaged with real honesty here — the storytelling has weight",
                             "the narrative specificity is there — this earns its genre tag"],
                "high":     ["folk this honest and this specific belongs in the lineage of artists who actually changed the form",
                             "the storytelling here would stand up against the best — Sufjan Stevens territory, with its own voice"],
                "perfect":  ["a perfect folk record: every lyric earns its place, every melody serves the story. ten.",
                             "folk music this complete is what the tradition has always been reaching for. a perfect ten."],
            },
            "hip hop": {
                "low":      ["hip hop has been the most vital genre on earth for forty years — this record has no relationship to any of those forty years",
                             "the lyricism has nothing to say and the production provides the wrong environment for it"],
                "mid_low":  ["the artistic voice is absent — it sounds like the genre without being part of it",
                             "the bars don't have any angle on anything — the best hip hop always has an angle"],
                "mid_high": ["the hip hop credibility here is earned rather than borrowed — the production has weight and the bars have a perspective",
                             "the lyricism operates with more formal intelligence than a surface read suggests"],
                "high":     ["hip hop that holds up under the scrutiny the genre's greatest work demands — the lyricism and production are genuinely aligned",
                             "this is going to get slept on and it shouldn't be — a hip hop record with a genuine artistic identity"],
                "perfect":  ["the critical establishment won't know what to do with this. I do. a perfect hip hop record. ten.",
                             "hip hop at this level stops being genre and becomes literature — this earns that comparison to Illmatic, to Madvillainy. ten."],
            },
            "pop": {
                "low":      ["mainstream pop is the only genre where being unchallenging is treated as a virtue — this achieves that non-virtue completely",
                             "the pop approach is a set of decisions designed to remove friction, which is the opposite of what art is for"],
                "mid_low":  ["the pop framework contains something trying to get out but the commercial structure has sealed every exit",
                             "I'm not anti-pop on principle but I am anti-music-that-refuses-to-ask-anything-of-you — this asks nothing"],
                "mid_high": ["most will walk past this — the interesting parts outnumber the safe ones on this record",
                             "a pop record that asks slightly more of you than the genre usually demands — which means it asks something"],
                "high":     ["this will get slept on by pop audiences conditioned to expect less — it's too good for its category",
                             "pop music that functions as an argument for pop music — the craft inside the commercial frame is real"],
                "perfect":  ["I've been called contrarian my whole career — I'm calling this first: a perfect pop record that transcends the category",
                             "history will remember this differently than the present does. a ten. the consensus will catch up."],
            },
            "r&b": {
                "low":      ["r&b's emotional vocabulary has become so coded that most releases within it say nothing new — this says less than nothing",
                             "the smoothness of r&b is its most evasive quality — this record perfects the evasion and achieves nothing else"],
                "mid_low":  ["the genre coasts on its cultural capital here rather than contributing to it",
                             "the r&b conventions are reproduced without any examination of whether they still mean what they used to mean"],
                "mid_high": ["r&b at its most honest has genuine emotional range — this reaches toward that range with some conviction",
                             "the genre's smoothness is used here in service of feeling rather than as a substitute for it — correct application"],
                "high":     ["this is r&b that earns the comparison to its most serious practitioners — the emotional intelligence is real",
                             "the genre's critics accuse it of surface feeling — this record is the rebuttal"],
                "perfect":  ["r&b at this level of emotional completeness becomes the argument for the genre's entire existence. ten.",
                             "the discourse will be divided on this. it shouldn't be. a perfect ten."],
            },
            "country": {
                "low":      ["country music has been hollowed out by Nashville for decades and this carries that legacy without questioning it",
                             "the country framing brings all the baggage of a genre that traded its soul for chart positions"],
                "mid_low":  ["the country conventions are present without the authenticity that gives them value",
                             "the mainstream country tradition is a set of compromises — this record doesn't push against any of them"],
                "mid_high": ["the outlaw tradition within country is a genuine alternative to its commercial version — this touches that alternative",
                             "country done honestly is a form with real weight — this is doing it honestly enough to earn some respect"],
                "high":     ["country music stripped of its commercial compromises has genuine depth — this operates in that stripped-down register",
                             "Townes Van Zandt proved the country form could carry real philosophical weight — this record follows that path credibly"],
                "perfect":  ["country this complete and this honest makes the strongest possible argument for the form's serious potential. ten.",
                             "the genre's commercial mainstream has betrayed this tradition for years. this record reclaims it completely. ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                formatted  = [s.replace("{g}", g) for s in tier_pool]
                return [picks(formatted, min(2, len(formatted)))]
        return [pick([
            f"the {g} direction isn't one I'd champion and this doesn't make the case for it" if tier in ("low","mid_low") else
            f"as a {g} track it delivers what the genre asks for — and in this case the genre is asking for the right things" if tier in ("mid_high","high") else
            f"the {g} framework is transcended here entirely — a landmark.",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "rage": {
                "low":      ["rage without an object is just noise — and this rage has no object",
                             "anger in music has to be specific to mean anything — this is diffuse frustration"],
                "mid_low":  ["the rage is present but hasn't found what it's actually angry about",
                             "the anger is real but it's too broad to land — needs sharpening"],
                "mid_high": ["rage as a theme is underrepresented in critical coverage — this brings it with conviction",
                             "the anger here is channeled into music rather than scattered — a legitimate artistic choice"],
                "high":     ["rage this focused and this articulate is one of the most powerful things music can be",
                             "the anger is earned, specific, and structurally supported — exactly how this theme should work"],
                "perfect":  ["rage done this completely — specific, structural, emotionally full — is a permanent artistic achievement. ten.",
                             "a perfect record about anger. I don't say that lightly."],
            },
            "protest": {
                "low":      ["protest music that doesn't make you uncomfortable isn't protest — it's a strongly worded note",
                             "the political angle is so diluted it becomes decoration rather than statement"],
                "mid_low":  ["the protest intent is there but it's too cautious — real protest music doesn't hedge",
                             "the message is present without the courage to push it where it needs to go"],
                "mid_high": ["protest music is the genre's conscience — this respects that tradition",
                             "the political content is handled directly rather than metaphorically — I respect that choice"],
                "high":     ["protest music this clear and this emotionally powered is exactly what the tradition is for",
                             "politically engaged music this focused reminds me of Kendrick's Section.80 — specific and necessary"],
                "perfect":  ["a perfect protest record: makes you feel something and makes you think about why. ten.",
                             "this is what music with something to say sounds like. ten."],
            },
            "existential": {
                "low":      ["existential themes require genuine philosophical courage — this is just sad aesthetics",
                             "sitting with the void in music is hard to do honestly — this isn't doing it honestly"],
                "mid_low":  ["the existential angle is more posture than actual thought",
                             "it wants to be philosophically serious — it's not quite getting there"],
                "mid_high": ["existential music refuses easy comfort and that refusal is the most honest stance an artist can take",
                             "the philosophical weight here is handled without the self-importance that usually sinks this territory"],
                "high":     ["existential themes this well-handled remind me of Radiohead's best work — heavy but earned",
                             "the depth is real and structurally backed up — this is the hardest thing to do in music and it's done"],
                "perfect":  ["existential music this complete is a once-in-a-decade achievement. a perfect ten.",
                             "the philosophical depth here is total and the music carries it. ten."],
            },
            "love": {
                "low":      ["love songs have been so thoroughly exhausted that writing one now requires a real reason — this doesn't have one",
                             "the love theme adds nothing new — there's nothing here that hasn't been said better elsewhere"],
                "mid_low":  ["the emotional terrain is familiar and this doesn't offer enough to justify revisiting it",
                             "love songs only work when they're specific — this stays too general"],
                "mid_high": ["there's more going on in the love theme here than most will notice — it has actual edges",
                             "this handles love with enough specificity that it doesn't feel like the ten thousand other love songs"],
                "high":     ["love themes succeed when they're so specific they become universal — this achieves that",
                             "the emotional intelligence in how this handles love puts it above most — rare"],
                "perfect":  ["the best love songs transcend the theme entirely — this does that. a ten.",
                             "love as a subject used this completely and this honestly is as good as the theme gets. ten."],
            },
            "party": {
                "low":      ["party music is an entire genre dedicated to avoiding interiority — I find that philosophically suspect",
                             "the festive theme signals a deliberate refusal to mean anything, which I can't get behind"],
                "mid_low":  ["the party angle doesn't give me enough to engage with intellectually or emotionally",
                             "I can't find the idea inside the party music — there needs to be one"],
                "mid_high": ["the best party music is secretly political — it claims space and that claim is always contested",
                             "the party energy here has a propulsive urgency that goes beyond just hedonism"],
                "high":     ["party music as cultural statement — this understands that celebration is always a political act",
                             "the joy here is genuine and that genuine quality makes it more interesting than it looks"],
                "perfect":  ["party music this complete and this joyfully realized becomes a statement. a ten.",
                             "joy executed this perfectly is a legitimate artistic achievement. a perfect ten."],
            },
            "euphoria": {
                "low":      ["euphoria as a theme is music's way of refusing to deal with anything real",
                             "the emotional terrain here is deliberately shallow — a creative choice I struggle to respect"],
                "mid_low":  ["the euphoric mode limits what the record can achieve and this doesn't find a way around that",
                             "there's no angle inside the euphoria — it's just happy noise"],
                "mid_high": ["there's something real underneath the euphoric surface here — worth noting",
                             "the euphoric energy has enough genuine feeling underneath it to be more than just a vibe"],
                "high":     ["joy this genuinely felt is harder to achieve than it looks — and this earns it",
                             "even I can admit that unguarded happiness done this well is an artistic achievement"],
                "perfect":  ["euphoria done this completely stops being shallow and starts being transcendent. a ten.",
                             "perfect record about joy. I don't usually give those. this earned it."],
            },
            "nostalgia": {
                "low":      ["nostalgia done wrong is sentimentality — and this doesn't have the craft to be anything else",
                             "the nostalgic angle is used as an emotion substitute rather than an actual emotion"],
                "mid_low":  ["the retrospective feeling is present without being earned",
                             "nostalgia that doesn't come from a real place is just wistfulness as aesthetics"],
                "mid_high": ["nostalgia done right is a reckoning with what was real and what was lost — this gets that",
                             "the nostalgic register is handled with enough self-awareness to avoid becoming just sad"],
                "high":     ["the historical feeling in this is genuine and moving — rare for a nostalgic record",
                             "nostalgia this specifically felt produces music that actually matters — this is that"],
                "perfect":  ["nostalgia this honest becomes its own kind of transcendence. a perfect ten.",
                             "the most complete nostalgic record I've heard in years. ten."],
            },
            "heartbreak": {
                "low":      ["heartbreak music without actual pain is just sad aesthetics",
                             "the vulnerability this theme needs isn't here — it stops just short of honest"],
                "mid_low":  ["heartbreak that stays at the surface level doesn't earn the emotional investment",
                             "needs more rawness — it's too careful to really hurt"],
                "mid_high": ["heartbreak this specific and this honest is handled more carefully than most critics will notice",
                             "the vulnerability here is real — and real vulnerability in music is rare"],
                "high":     ["heartbreak done this honestly is close to the best the theme can achieve",
                             "emotionally specific and structurally sound — this is what the heartbreak theme is for"],
                "perfect":  ["heartbreak this thoroughly and honestly expressed is a rare and permanent thing. ten.",
                             "a perfect heartbreak record. I felt it. ten."],
            },
            "street life": {
                "low":      ["the street life theme is a costume here — the specificity that makes it real is absent",
                             "cultural authenticity is the entire point of this theme — it's missing"],
                "mid_low":  ["the theme is gesturing at a reality without inhabiting it — the gap shows",
                             "present without the lived detail that makes it land"],
                "mid_high": ["the street life theme is handled more carefully than most critics will notice",
                             "the specificity is real — this isn't a tourist's take on the subject"],
                "high":     ["the street life narrative here is as honest as the best hip hop journalism — specific, unromantic, and true",
                             "sits in the lineage of records that documented real experience with real craft"],
                "perfect":  ["street life documented with this level of honesty and artistry is permanent. ten.",
                             "the best street life music is also the most universal — this achieves that paradox completely. ten."],
            },
            "spirituality": {
                "low":      ["spiritual vibes without spiritual depth — the worst kind of sacred music",
                             "the theme is claimed aesthetically without being felt genuinely"],
                "mid_low":  ["the spiritual element is present as atmosphere — not as actual belief",
                             "the sacred doesn't feel sacred here — it feels like a production choice"],
                "mid_high": ["there's something genuinely believed underneath the spiritual angle here — I can hear the difference",
                             "spirituality that comes from a real place reads differently — this reads as real"],
                "high":     ["the spiritual content here is honest and it earns its transcendence",
                             "music reaching toward something larger and actually touching it — rare"],
                "perfect":  ["spirituality expressed this completely in music is transcendent. a perfect ten.",
                             "a perfect spiritual record. I'm not someone who says that. this is that."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {t} theme is handled more carefully than most critics will notice",
            f"there's more going on thematically than the surface read suggests — the {t} angle rewards attention",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick(["the long runtime will lose most listeners — the right listeners will be rewarded",
                          "demands patience, which most people don't have — not entirely the track's fault"])]
        if d < 150:
            return [pick(["the brevity is a form of confidence — it says what it has to say and leaves",
                          "in a world of bloated runtimes, the compact length is a quiet act of respect"])]
        return [pick(["the runtime is the least interesting thing about this record",
                      "three minutes of something good beats six minutes of something fine — this threads that needle"])]


# ─────────────────────────────────────────────
#  CRITIC 5 — EARL MOSELY  (Nostalgic veteran)
# ─────────────────────────────────────────────

class EarlMosely(Critic):
    name         = "Earl Mosely"
    tagline      = "Columnist, 57 Years in Music"
    verdict_type = "nostalgic"

    loved_genres    = ["blues", "soul", "jazz", "folk", "r&b"]
    liked_genres    = ["rock", "country", "classical"]
    disliked_genres = ["electronic", "hip hop"]
    hated_genres    = ["experimental", "metal"]

    loved_themes    = ["nostalgia", "heartbreak", "spirituality", "love"]
    disliked_themes = ["rage", "street life", "euphoria"]

    base_modifier = -0.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "blues": {
                "low":      ["the blues tradition carries more human truth per note than almost anything — and this squanders every note",
                             "I've been listening to blues for decades and I know when someone doesn't understand it — this doesn't"],
                "mid_low":  ["the blues elements are present but the feeling is borrowed rather than lived — the gap is audible",
                             "the twelve-bar structure is here. the humanity it's supposed to carry is mostly absent."],
                "mid_high": ["the blues tradition carries weight and this record doesn't run from it — which is exactly right",
                             "you can hear the lineage here, from the Delta forward, treated with appropriate care"],
                "high":     ["real blues is about the weight of experience and this record carries that weight honestly — a rarity",
                             "this reminds me why blues changed everything when it first came north — Gary Clark Jr. has this quality on his best days"],
                "perfect":  ["blues music this honest and complete is something I thought I might not hear again. a perfect ten.",
                             "I've been waiting a very long time for a record to make me feel this way. this is it. ten."],
            },
            "soul": {
                "low":      ["real soul is about transmitting genuine emotion — this transmits nothing but the shape of it, which is worse than silence",
                             "the soulfulness here is performed rather than felt. anyone who's heard the real thing can hear the difference."],
                "mid_low":  ["the soul elements are decorative rather than structural — the warmth is applied from outside rather than generated within",
                             "soul music requires that something genuine happened in the room — I can't hear that here"],
                "mid_high": ["this reminds me, just a little, of why soul music changed everything when it arrived — the feeling is real if not transcendent",
                             "the soulfulness is not performed — it's felt, and the difference is audible"],
                "high":     ["real soul is rare and this record has it — the transmission of genuine emotion is what the genre is for",
                             "this puts me in mind of the great Stax recordings — not a perfect comparison, but the warmth and sincerity are the same kind"],
                "perfect":  ["soul music this complete is what the genre was always reaching for — this belongs in that company. a perfect ten.",
                             "I have lived with great soul music my whole life and this joins it without apology. ten."],
            },
            "jazz": {
                "low":      ["the jazz tradition requires intelligence at the instrument level — this has the instruments without the intelligence",
                             "I've spent sixty years with jazz and I know when someone doesn't understand it — this doesn't understand it"],
                "mid_low":  ["the jazz vocabulary is referenced without the musicianship to give those references meaning",
                             "the harmonic choices suggest jazz training without the improvisational wisdom that makes training into art"],
                "mid_high": ["the jazz influence brings intelligence to this record that rewards the attentive listener",
                             "there's a conversation happening between the instruments that jazz uniquely enables — I can hear it here"],
                "high":     ["the jazz sensibility here is the real thing — you can trace the lineage and it's honored, not just cited",
                             "Kamasi Washington's best work operates in this territory — this record belongs in that conversation"],
                "perfect":  ["I've spent my life with jazz and this record belongs in its company without qualification. a perfect ten.",
                             "the tradition lives here the way it lived in the great recordings: not preserved but continued. ten."],
            },
            "hip hop": {
                "low":      ["hip hop has produced some of the most vital records of the last forty years — this has no relationship to any of them",
                             "I've tried to understand what this is doing. I cannot."],
                "mid_low":  ["the hip hop tradition here is handled without much understanding of what makes that tradition matter",
                             "the cultural specificity is missing — it's genre-adjacent rather than genre-genuine"],
                "mid_high": ["hip hop has produced some of the most vital records of the last forty years and this, against my expectations, connects to that tradition",
                             "the hip hop tradition is treated with enough respect here that I can hear the understanding behind it"],
                "high":     ["hip hop at its best carries as much emotional weight as any tradition I've spent my life with — this record carries that weight",
                             "Kendrick Lamar at his most open-hearted operates in this territory — and this earns that comparison"],
                "perfect":  ["hip hop this complete earns comparison to any tradition in music. I mean that. a perfect ten.",
                             "I have revised my relationship to hip hop on the basis of this record. a perfect ten."],
            },
            "experimental": {
                "low":      ["in my experience, experimental means the musician has stopped caring whether anyone connects with the work",
                             "I've heard experimental music that moved me. this is not that."],
                "mid_low":  ["the experimental approach creates a distance between the music and the listener that isn't bridged",
                             "unconventional for its own sake rather than in service of a feeling"],
                "mid_high": ["the experimental choices here are purposeful rather than defensive — I can hear the intention",
                             "it challenges the listener honestly — and the reward is real for those willing to meet it"],
                "high":     ["experimental music that actually generates genuine emotion is the rarest thing — this achieves it",
                             "I wasn't sure this genre could still surprise me. this record surprised me."],
                "perfect":  ["experimental music this emotionally complete and this formally resolved is a landmark. a perfect ten.",
                             "I find myself moved by something I expected not to understand. that's the highest compliment. ten."],
            },
            "metal": {
                "low":      ["I've been making peace with not understanding metal for fifty years — this doesn't help",
                             "the aggression here is technically accomplished and emotionally inaccessible to me — and I've lived through things that should help me understand rage"],
                "mid_low":  ["the metal form creates a barrier I can't fully get past — the emotional distance is too great",
                             "I'm not the audience for this and I don't think the music cares — which is honest, at least"],
                "mid_high": ["the metal here has more emotional range than the genre usually shows me — I hear something underneath the volume",
                             "the intensity is purposeful in a way that even I, a confirmed non-metalhead, can acknowledge"],
                "high":     ["metal that can make a listener like me feel something real is operating at an exceptional level",
                             "this record broke through a resistance I've carried for decades. that's an achievement I won't deny."],
                "perfect":  ["metal this emotionally complete and this structurally sound is a perfect record even for someone like me. ten.",
                             "I cried. I didn't expect to cry at a metal record. a perfect ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"I've heard {g} done better and I've heard it done worse — this is somewhere in the honest middle" if tier == "mid_high" else
            f"the {g} direction doesn't connect to the lineage I care about — and the execution doesn't compensate" if tier in ("low","mid_low") else
            f"the {g} framework is applied with the kind of mastery that reminds you why the form exists" if tier == "high" else
            f"a defining {g} record — the kind I'll still be thinking about when the year is done. ten.",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "nostalgia": {
                "low":      ["nostalgia done wrong is fake warmth — and I've lived enough to know the difference",
                             "the retrospective feeling here is borrowed rather than real — no real memory behind it"],
                "mid_low":  ["the nostalgic angle is present but it hasn't earned the emotion it's reaching for",
                             "wistfulness as a style choice rather than a real feeling — I can tell"],
                "mid_high": ["nostalgia done right isn't self-pity — it's a reckoning with what was real and what was lost",
                             "the nostalgic register is handled with enough honesty to avoid being merely sentimental"],
                "high":     ["the nostalgic theme resonates in ways that feel personally real to me — good music does that",
                             "Taylor Swift's folklore-era intimacy captures this kind of genuine memory — this belongs in that conversation"],
                "perfect":  ["nostalgia this honest and this complete is the closest music gets to actual memory. a perfect ten.",
                             "I felt something I haven't felt in years. a perfect ten."],
            },
            "heartbreak": {
                "low":      ["heartbreak music without real emotion is just sad aesthetics — and I've lived through enough to know real heartbreak",
                             "the vulnerability this theme needs isn't here — the real feeling is kept at arm's length"],
                "mid_low":  ["the heartbreak theme is present but stays too surface-level to really land",
                             "needs more rawness — it's too careful to actually hurt the way the theme requires"],
                "mid_high": ["heartbreak has driven more great music than any other human experience — this earns its place in that tradition",
                             "the emotional truth of heartbreak is handled here without sentimentality — that takes skill and lived experience"],
                "high":     ["the heartbreak here is raw and specific — Olivia Rodrigo at her most direct has this quality, and this earns it too",
                             "this is devastating in the best sense — the emotional transfer is complete"],
                "perfect":  ["heartbreak this thoroughly and honestly expressed is a rare and permanent thing. a perfect ten.",
                             "I felt things I haven't felt in a long time. a perfect ten. no question."],
            },
            "spirituality": {
                "low":      ["the spiritual theme is here as atmosphere, not as belief — and I know the difference",
                             "spirituality without genuine faith behind it is just mood lighting"],
                "mid_low":  ["the spiritual dimension is present without the depth that makes it mean anything",
                             "the sacred is gestured at rather than approached — there's no real belief underneath"],
                "mid_high": ["music and the sacred have always been connected — this track understands that ancient bond",
                             "the spiritual element is earned here rather than claimed — a real difference"],
                "high":     ["the reaching-toward-something-larger here is genuine — and genuine is everything in this theme",
                             "Chance the Rapper's most open-hearted moments have this quality — this belongs in that conversation"],
                "perfect":  ["spirituality expressed this completely in music is transcendent. I say this without reservation. a perfect ten.",
                             "I felt lifted. that hasn't happened in a long time. a perfect ten."],
            },
            "love": {
                "low":      ["love songs are the oldest form in music — this one forgets why they existed in the first place",
                             "the love theme here has no actual feeling behind it — going through the motions"],
                "mid_low":  ["love music that doesn't make you feel love has missed the entire assignment",
                             "the theme is present without the vulnerability that makes love music matter"],
                "mid_high": ["love songs are the oldest form there is — this reminds you why they've never gone away",
                             "the love theme here is handled with the tenderness the subject deserves"],
                "high":     ["love music this genuinely felt is what the tradition is built for",
                             "the emotional specificity here elevates this beyond the average love song — something real is being said"],
                "perfect":  ["love expressed this completely in music becomes something universal and permanent. a perfect ten.",
                             "the finest love record I've heard in a very long time. a perfect ten."],
            },
            "rage": {
                "low":      ["anger is a legitimate human emotion but this channeling of it generates more heat than light",
                             "the rage theme connects to traditions I understand but the expression here doesn't move me"],
                "mid_low":  ["the rage here is too unformed to connect with — it needs direction to mean anything",
                             "I understand anger. this anger doesn't know what it's for."],
                "mid_high": ["anger channeled into music rather than scattered — a legitimate artistic choice",
                             "the rage has a point here and it makes it, which is all I ask of this theme"],
                "high":     ["rage this focused and this well-expressed is one of the most powerful things music can be",
                             "the anger is earned and the craft is there — a rare combination"],
                "perfect":  ["rage expressed this completely in music is a permanent artistic achievement. a perfect ten.",
                             "I was moved by this in a way I didn't expect. a perfect ten."],
            },
            "street life": {
                "low":      ["street life themes reflect a reality I haven't personally inhabited — and this isn't helping me understand it",
                             "the cultural specificity of the street life theme is absent here — it feels tourist-like"],
                "mid_low":  ["the authenticity is partial — and partial authenticity in this theme isn't enough",
                             "I try to evaluate these fairly but I can hear when the experience isn't lived — this isn't"],
                "mid_high": ["the cultural specificity of the street life theme is handled with authenticity — I can hear the difference",
                             "the detail is real — this isn't a borrowed perspective"],
                "high":     ["street life documented with this level of honesty becomes something that transcends its own specificity",
                             "the kind of documentary music that makes the listener feel like they were there — powerful and rare"],
                "perfect":  ["street life music this honest and this complete is what the theme has always been capable of. a perfect ten.",
                             "I learned something listening to this. that's the highest thing I can say about music. ten."],
            },
            "protest": {
                "low":      ["protest music needs to make you uncomfortable — this is a note of mild concern",
                             "the political edge here is too dull to cut anything"],
                "mid_low":  ["the protest intent is there but it's too cautious to be real protest",
                             "hedging on the political angle disappoints me — the great protest music never hedged"],
                "mid_high": ["protest music at its best is uncomfortable — this doesn't shy away from that discomfort",
                             "the political dimension is handled with care rather than sloganeering — the right approach"],
                "high":     ["protest music this clear and this well-made reminds me of the records that actually changed things",
                             "the message here is sharp and the music carries it — a real combination, rare at any age"],
                "perfect":  ["protest music this complete is a rare and important thing. a perfect ten.",
                             "this is what music with something to say sounds like when it's done at its highest level. ten."],
            },
            "euphoria": {
                "low":      ["euphoria as a theme tends to produce music that refuses to cost the listener anything — this is no exception",
                             "the festive framing drains whatever depth the record might have had"],
                "mid_low":  ["the euphoric mode is fine but it limits what the record can say or do",
                             "joy without any shadow is aesthetically comfortable and artistically limited"],
                "mid_high": ["the euphoric feeling here has more genuine joy in it than the theme usually allows",
                             "music that earns its happiness rather than just announcing it — a real distinction"],
                "high":     ["joy done honestly at this level is an artistic achievement I can acknowledge even if it's not my natural territory",
                             "the euphoric energy here is unguarded and genuine — that's harder to achieve than it looks"],
                "perfect":  ["euphoria this complete and this genuinely felt is a gift. a perfect ten.",
                             "I was lifted. that doesn't happen often. a perfect ten."],
            },
            "existential": {
                "low":      ["existential themes require real philosophical depth — this is just a mood",
                             "big questions treated this lightly end up being smaller than no question at all"],
                "mid_low":  ["the existential angle is more posture than genuine reckoning",
                             "it wants to sit with difficult things but doesn't stay long enough to mean it"],
                "mid_high": ["grappling with the difficult questions is the oldest tradition in art — this earns its place in it",
                             "the existential undertone here is genuine and it adds real weight to the record"],
                "high":     ["existential music that actually sits with the hard questions without flinching — rare",
                             "this carries a philosophical weight that reminds me of the records that stayed with me longest"],
                "perfect":  ["existential music this complete is what the tradition has always been reaching for. a perfect ten.",
                             "I felt the weight of this for days after. that's a perfect ten."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {t} theme connects to something fundamentally human — good music always does",
            f"the {t} direction gives this an emotional grounding that I appreciate in a record",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 360:
            return [pick(["they used to make records that took their time — this continues that tradition honestly",
                          "the extended runtime feels natural — music shouldn't always be in a hurry"])]
        if d < 150:
            return [pick(["songs used to breathe a little more than this — but the brevity works well enough",
                          "short, but I always want more when the music is genuinely good"])]
        return [pick(["the runtime is appropriate — as long as it needs to be and no longer",
                      "the length feels honest — neither overstaying nor cutting short"])]


# ─────────────────────────────────────────────
#  CRITIC 6 — ZARA NIGHTS  (Underground Scene)
# ─────────────────────────────────────────────

class ZaraNights(Critic):
    name         = "Zara Nights"
    tagline      = "Zine Editor & Promoter, The Circuit"
    verdict_type = "scenes"

    loved_genres    = ["punk", "electronic", "hip hop", "experimental"]
    liked_genres    = ["metal", "rock", "r&b"]
    disliked_genres = ["country", "classical"]
    hated_genres    = ["pop", "folk"]

    loved_themes    = ["street life", "rage", "protest", "party"]
    disliked_themes = ["nostalgia", "spirituality", "love"]

    base_modifier = 0

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "punk": {
                "low":      ["punk is still the most authentic response to a world that needs pushing back on — this doesn't get that",
                             "the raw energy is performed here rather than earned — the scene can tell the difference instantly"],
                "mid_low":  ["the punk energy is present but underdeveloped — not enough conviction behind the choices",
                             "it's got the sound but not the fire — punk without fire is just noise"],
                "mid_high": ["the scene doesn't need perfect production — it needs this kind of conviction, and it's here",
                             "raw, confrontational, and honest — what punk was always supposed to be"],
                "high":     ["this is punk that actually says something — the form and content are lined up in a way the genre rarely achieves",
                             "the scene would embrace this completely — it's the real thing"],
                "perfect":  ["a perfect punk record — every rough edge is load-bearing, nothing wasted. a ten.",
                             "punk music this complete and this honest is what the underground has been waiting for. ten."],
            },
            "electronic": {
                "low":      ["electronic music at this level is architecture — and this was built wrong",
                             "the production is technically present and sonically empty — the scene has heard this mistake before"],
                "mid_low":  ["the production doesn't have a real identity — it's sonic wallpaper",
                             "electronic music needs to know what it's doing — this doesn't quite know"],
                "mid_high": ["the production here speaks the language of the underground fluently",
                             "electronic music at this level is architecture — and this was built correctly"],
                "high":     ["the scene runs on electronic music and this is exactly the kind of track that earns its place in the rotation",
                             "Four Tet or SBTRKT energy — genuine, considered, and built to last"],
                "perfect":  ["a perfect electronic record — the architecture is flawless and the feeling is total. ten.",
                             "this is what the underground was waiting for. ten."],
            },
            "hip hop": {
                "low":      ["hip hop is still the most culturally alive genre on the planet — this record has no relationship to that energy",
                             "the scene can smell performed hip hop from a mile away. this is performed."],
                "mid_low":  ["the hip hop credibility is borrowed here — the bars don't have the weight the scene demands",
                             "the production is competent. the identity behind it isn't there."],
                "mid_high": ["the hip hop credibility here is earned rather than borrowed — the production has weight and the bars have a perspective",
                             "the scene can smell performed hip hop from a mile away — this is real"],
                "high":     ["the heads would know — and they'd approve. this is genuine hip hop.",
                             "Kendrick or J. Cole at their most grounded have this quality — this earns the comparison"],
                "perfect":  ["a perfect hip hop record — the scene will be talking about this for years. ten.",
                             "this is what the underground was waiting for in hip hop. ten."],
            },
            "pop": {
                "low":      ["pop is designed for people who want music to do as little as possible — the underground has no use for that",
                             "the pop framing is the loudest possible signal that this wasn't made for us"],
                "mid_low":  ["the pop approach positions this firmly outside the spaces where I operate",
                             "the commercial framing closes off everything the scene values — authenticity, edge, intention"],
                "mid_high": ["there's more going on here than the pop label suggests — the scene will notice",
                             "pop that has an actual identity underneath the commercial packaging — worth a closer look"],
                "high":     ["pop music that functions as something more than product — the scene will hear the difference",
                             "this will get slept on by pop audiences — the underground will find it"],
                "perfect":  ["pop music this complete transcends the genre tag entirely. a ten.",
                             "the most interesting pop record the underground has reason to care about in years. ten."],
            },
            "folk": {
                "low":      ["folk has its own underground but this doesn't belong to either world convincingly",
                             "the folk direction creates a pastoral distance from the urban energy the scene runs on"],
                "mid_low":  ["I don't disrespect folk as a tradition — I just can't connect it to anything I'm covering",
                             "the folk framework creates a distance from the present that the scene doesn't have patience for"],
                "mid_high": ["the folk tradition has genuine underground credibility in the right hands — this is getting closer to those hands",
                             "the storytelling here is honest enough to earn the scene's attention"],
                "high":     ["folk music this genuine crosses scene lines — the underground respects honesty above genre",
                             "the kind of record that earns respect even outside its natural audience"],
                "perfect":  ["folk music this complete earns the scene's full attention regardless of genre. ten.",
                             "a perfect folk record that transcends its own category. the underground will find this one. ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {g} direction lands credibly in the context I operate in" if tier in ("mid_high","high","perfect") else
            f"the {g} approach doesn't quite have the underground credibility the scene demands" if tier in ("low","mid_low") else
            f"the {g} is executed at a level the scene will fully respect. a landmark.",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "street life": {
                "low":      ["the street life theme is a costume here — the lived detail that makes it real is absent",
                             "the scene reads inauthenticity in this theme instantly — and it's reading it here"],
                "mid_low":  ["the authenticity is partial — the theme is gesturing at a reality without inhabiting it",
                             "the cultural specificity is missing in ways that are obvious to anyone paying attention"],
                "mid_high": ["the street life theme is handled with the kind of specificity that comes from having actually been there",
                             "the cultural authenticity of the street life angle is the record's most valuable quality"],
                "high":     ["the street life narrative here is as honest as the best hip hop journalism — specific and unromantic",
                             "the scene values truth above everything — this record tells it"],
                "perfect":  ["street life documented with this level of honesty becomes permanent art. ten.",
                             "the most authentic take on the street life theme I've heard in years. ten."],
            },
            "rage": {
                "low":      ["rage without a target is just noise and the scene has no use for noise",
                             "the anger here is diffuse — in the underground, anger needs an address"],
                "mid_low":  ["the rage is present but it hasn't found what it's angry at — the scene notices",
                             "the anger needs sharpening — right now it's more of a mood than a statement"],
                "mid_high": ["rage is an honest response to what the world is doing right now — this channels it usefully",
                             "the anger here is specific and pointed rather than scattered — the difference between art and noise"],
                "high":     ["rage this focused and this well-expressed is one of the most powerful things music can be",
                             "the scene was built on this kind of focused anger — this belongs here"],
                "perfect":  ["rage done this completely is a permanent artistic achievement. ten.",
                             "focused, honest, necessary — a perfect rage record. ten."],
            },
            "protest": {
                "low":      ["protest music that doesn't make anyone uncomfortable isn't protest — it's a press release",
                             "the political edge here is too dull to cut anything — the scene deserves sharper"],
                "mid_low":  ["the protest angle is too cautious — real protest music doesn't protect itself",
                             "the message is present without the courage to push it where it needs to go"],
                "mid_high": ["protest music is never more relevant than when institutions want it quiet — and they always do",
                             "the political edge here is sharp and the scene will receive it accordingly"],
                "high":     ["protest music this clear and this necessary reminds the scene why this music exists in the first place",
                             "the message is sharp, the music carries it — a real combination the underground deeply respects"],
                "perfect":  ["a perfect protest record — the scene was built on this kind of music. ten.",
                             "necessary, sharp, and flawless. ten."],
            },
            "party": {
                "low":      ["the best party music is politically charged — this has neither the party nor the politics",
                             "party energy that doesn't move anyone isn't party energy — it's just noise"],
                "mid_low":  ["the party theme is trying but not quite reaching the energy that makes it work",
                             "the momentum drops where it should be climbing — a fixable problem that isn't fixed"],
                "mid_high": ["the best party music claims space and that claim is always political — this gets that",
                             "the party energy here has a propulsive urgency that goes beyond just having fun"],
                "high":     ["this is party music that moves the body and signals something about the culture — Beyoncé's Renaissance did this",
                             "the scene loves party music that knows it's more than just fun — this knows"],
                "perfect":  ["a perfect party record: joyful, culturally loaded, and impossible to stand still to. ten.",
                             "party music this fully realized is a complete artistic statement. ten."],
            },
            "love": {
                "low":      ["the love angle gives this mass appeal at the cost of the edge the scene demands",
                             "love themes pull this toward the mainstream in ways that lose the underground"],
                "mid_low":  ["the love theme is fine — it's just not where the cultural energy the scene cares about is living right now",
                             "too soft an angle for the spaces I cover — the scene needs more tension"],
                "mid_high": ["the love theme here has an edge to it that keeps the scene interested",
                             "love handled with this much honesty has an underground credibility that's hard to argue with"],
                "high":     ["love music this genuinely felt crosses scene lines — the underground respects real emotion",
                             "the emotional honesty here gives this the authenticity the scene demands"],
                "perfect":  ["love expressed this completely has the kind of cultural weight the underground respects. ten.",
                             "perfect. emotionally honest and sonically uncompromising. ten."],
            },
            "nostalgia": {
                "low":      ["the scene is always looking forward — nostalgia-themed music is a step in the wrong direction",
                             "the retrospective angle creates a distance from the present the underground won't tolerate"],
                "mid_low":  ["nostalgia is the one theme the underground has limited patience for — and this isn't making the case for more",
                             "the scene is about what's happening now — this is about what happened then"],
                "mid_high": ["the nostalgic angle is handled with enough self-awareness that the scene can respect it",
                             "nostalgia that's honest about itself is different from nostalgia that just wallows — this is honest"],
                "high":     ["nostalgia music this genuine has underground credibility — it mourns something specific and real",
                             "the scene can respect real memory, even if nostalgia isn't its natural territory"],
                "perfect":  ["nostalgia this complete transcends the limitation of the theme — a perfect record. ten.",
                             "genuine enough to earn the scene's respect despite itself. ten."],
            },
            "spirituality": {
                "low":      ["spiritual themes in the underground need genuine belief behind them — aesthetic spirituality is worse than no spirituality",
                             "the sacred is performed here rather than felt — the scene has no time for performance"],
                "mid_low":  ["the spiritual angle is present as atmosphere rather than as conviction",
                             "the scene reads spiritual aesthetics as hollow unless they come from somewhere real — this doesn't quite feel real"],
                "mid_high": ["the spiritual element here comes from somewhere real — I can hear the belief behind it",
                             "genuine spiritual content has underground credibility when it's earned — this earns it"],
                "high":     ["the spiritual depth here is the kind that crosses scene boundaries — genuine belief is universally compelling",
                             "Chance the Rapper's most open-hearted moments have this quality — the scene responded to that and will to this"],
                "perfect":  ["spiritual music this genuine and this complete earns the scene's full attention. ten.",
                             "transcendent and honest — a perfect spiritual record. ten."],
            },
            "existential": {
                "low":      ["existential themes without real depth are just sad aesthetics — the scene sees through that",
                             "the underground values authentic reckoning with difficult things — this isn't there yet"],
                "mid_low":  ["the existential angle is more posture than genuine philosophical engagement",
                             "it wants to sit with difficult questions but doesn't stay long enough to matter"],
                "mid_high": ["existential themes are everywhere in underground music because the questions are real — this handles them with real seriousness",
                             "the philosophical weight here is genuine and the music backs it up"],
                "high":     ["existential music this clear-eyed is exactly what the underground values — no easy answers, no flinching",
                             "Radiohead's best era operates in this territory — and this earns that conversation"],
                "perfect":  ["existential music this complete is a landmark. the underground will hold this record for years. ten.",
                             "perfect. philosophically honest and sonically uncompromising. ten."],
            },
            "heartbreak": {
                "low":      ["heartbreak without real vulnerability is just sad aesthetics — the scene doesn't respond to aesthetics without substance",
                             "the emotional distance here is too great — the theme requires rawness and this stays polished"],
                "mid_low":  ["the heartbreak is present but surface-level — the underground demands more honesty than this",
                             "too careful to really hurt — and hurting is the whole point of this theme"],
                "mid_high": ["heartbreak this honest has underground credibility — real emotion always does",
                             "the rawness here is earned, not performed — the scene knows the difference"],
                "high":     ["heartbreak this specific and this raw is exactly what the underground respects",
                             "the scene was built on music that hurts honestly — this is that music"],
                "perfect":  ["heartbreak music this complete is a perfect record. the underground will hold this one. ten.",
                             "raw, specific, and devastating. a perfect ten."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {t} theme is handled with the kind of authenticity the scene demands" if tier in ("mid_high","high","perfect") else
            f"the {t} angle doesn't quite connect to the cultural energy the scene is running on" if tier in ("low","mid_low") else
            f"the {t} theme is executed with the cultural intelligence and authenticity that defines the underground's best records",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick(["the extended runtime is a flex — and the content earns it enough to carry it",
                          "long records succeed or fail on whether they hold attention — this mostly does"])]
        if d < 150:
            return [pick(["the compact length is pure scene energy — get in, do the thing, get out",
                          "brevity in underground music is a power move and this plays it right"])]
        return [pick(["paced correctly — the scene has no patience for filler and there isn't any here",
                      "the runtime hits the sweet spot for this kind of record"])]


# ─────────────────────────────────────────────
#  CRITIC 7 — TOBIAS LUND  (Casual listener)
# ─────────────────────────────────────────────

class TobiasLund(Critic):
    name         = "Tobias Lund"
    tagline      = "Just a Guy Who Listens to Music"
    verdict_type = "casual"

    loved_genres    = ["pop", "hip hop", "r&b", "rock"]
    liked_genres    = ["reggae", "soul", "electronic"]
    disliked_genres = ["experimental", "blues"]
    hated_genres    = ["classical", "metal"]

    loved_themes    = ["party", "love", "euphoria", "nostalgia"]
    disliked_themes = ["existential", "protest"]

    base_modifier = 0.5

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      ["this is the kind of pop that makes me understand why people say pop is dead",
                             "pop music has one job and this one didn't do it — where are the hooks?"],
                "mid_low":  ["the pop formula is here but the magic isn't — I kept waiting for it to land",
                             "it's catchy in a way that makes you forget it immediately. not a compliment."],
                "mid_high": ["this is exactly the kind of pop I put on without thinking twice — that's a compliment",
                             "pop that actually does what pop is supposed to do — makes you feel something fast"],
                "high":     ["okay this pop record is really good — Doja Cat and SZA quality, modern and sharp",
                             "the kind of pop record that reminds you why pop is the most popular music on earth"],
                "perfect":  ["this is genuinely one of the best pop records I've heard. a ten.",
                             "flawless pop music — I've played it five times. ten."],
            },
            "hip hop": {
                "low":      ["the hip hop energy isn't landing — flat beat and bars that say nothing at all",
                             "hip hop needs presence — this record is absent from itself"],
                "mid_low":  ["goes through the motions without the spark — competent and forgettable",
                             "the bars are delivered but they're not doing anything interesting with the delivery"],
                "mid_high": ["the hip hop energy here hits — confident, real, and worth paying attention to",
                             "I found myself actually listening to the lyrics, which doesn't always happen"],
                "high":     ["genuinely hard hip hop — made me look up who made it immediately after",
                             "the production has depth and the bars match it — this is a real record"],
                "perfect":  ["this hip hop record is one of the best things I've heard this year. a perfect ten.",
                             "the bars are elite and the production is elite. a ten. easy."],
            },
            "r&b": {
                "low":      ["smooth but empty — the groove is borrowed and the feeling isn't there",
                             "r&b without warmth is just slow music and this is just slow music"],
                "mid_low":  ["the r&b vibe is present but it slides past without really connecting",
                             "I wanted to get into it and it kept not letting me in"],
                "mid_high": ["smooth, warm, and easy to love — the r&b vibe is doing exactly what it should",
                             "the r&b feel makes this immediately appealing in a way I really appreciate"],
                "high":     ["this r&b is in the pocket completely — Daniel Caesar or Frank Ocean energy, intimate and real",
                             "one of those records that makes the background stop being background — I kept stopping to listen"],
                "perfect":  ["a perfect r&b record — warm, real, and emotionally complete. a ten.",
                             "I don't say this often but this is genuinely a perfect record. ten."],
            },
            "rock": {
                "low":      ["loud but nothing interesting happening with any of it",
                             "the rock energy is there in theory — the ideas to back it up aren't"],
                "mid_low":  ["decent rock but forgettable rock — it plays and you move on",
                             "the energy is real but it doesn't go anywhere particularly interesting"],
                "mid_high": ["the rock energy is real and it actually goes somewhere — I was into it",
                             "solid rock music — the kind of thing you can genuinely just enjoy"],
                "high":     ["this rock record is actually really good — guitar-forward stuff with real weight behind it",
                             "the kind of rock record that makes you want to turn it up — rare"],
                "perfect":  ["a perfect rock record — I'm not the world's biggest rock fan and I loved this. ten.",
                             "ten out of ten. the energy is flawless."],
            },
            "classical": {
                "low":      ["I know this is probably impressive but it's just not for me",
                             "classical music and I have an understanding: I acknowledge its greatness and it doesn't expect me to enjoy it"],
                "mid_low":  ["technically it's probably doing something important — I lack the framework to appreciate it properly",
                             "I respect it. I didn't enjoy it. that's the honest answer."],
                "mid_high": ["this classical music is doing something that actually caught my attention, which doesn't usually happen",
                             "more accessible than classical usually feels to me — I found myself in it"],
                "high":     ["the classical work here is genuinely stunning in a way that even I can recognize",
                             "this made me feel something unexpected — I didn't think classical music would do that to me today"],
                "perfect":  ["okay. this is a perfect classical record and I say that as someone who usually doesn't connect with the genre. ten.",
                             "a ten. genuinely. I didn't see that coming from this genre."],
            },
            "metal": {
                "low":      ["my ears were not ready and are not recovered",
                             "the heaviness is doing all the work and the heaviness isn't enough"],
                "mid_low":  ["metal is a lot and this is a lot — I appreciate it for people who love this but I'm not that person",
                             "I admire people who love metal. I am not those people."],
                "mid_high": ["the metal here has more emotional range than I expected — moments that actually broke through",
                             "not my world but it's doing something real in there and I can hear it"],
                "high":     ["okay this metal record genuinely got through to me and I didn't expect that at all",
                             "the energy here is focused in a way that even non-metal listeners can feel — really impressive"],
                "perfect":  ["a perfect metal record that converted a non-metal listener. that's an achievement. ten.",
                             "ten out of ten and I genuinely cannot believe I'm typing that about a metal record."],
            },
            "electronic": {
                "low":      ["I'm not sure what I was supposed to feel during this",
                             "walls of sound that don't lead anywhere I wanted to go"],
                "mid_low":  ["electronic music that doesn't create a feeling is just noise with better production",
                             "the production is technically impressive and emotionally absent"],
                "mid_high": ["the electronic vibe creates a mood and holds it — more than I can say for most",
                             "the sound design is genuinely engaging — I got into it more than I expected"],
                "high":     ["this electronic music actually made me feel something — KAYTRANADA or Disclosure energy, but with real depth",
                             "the kind of electronic record that makes the genre feel accessible even to people who don't usually listen to it"],
                "perfect":  ["a perfect electronic record. I was vibing the entire time. ten.",
                             "ten out of ten. the production is flawless and the feeling is total."],
            },
            "experimental": {
                "low":      ["I genuinely don't know what I just listened to",
                             "experimental music makes me feel like I'm missing a reference I should have — maybe I am"],
                "mid_low":  ["interesting on paper. difficult in practice. I'm probably not the right audience.",
                             "the weirdness doesn't quite pay off for me — I needed more of a landing somewhere"],
                "mid_high": ["this experimental music opened up with time — I found myself getting into it",
                             "challenging in a way that ends up being rewarding — not an easy thing to pull off"],
                "high":     ["this experimental music genuinely connected with me, which I wasn't expecting",
                             "the production creates a world and I actually wanted to be in it — impressive"],
                "perfect":  ["a perfect experimental record that works for a completely average listener. that's remarkable. ten.",
                             "ten out of ten. experimental music that anyone can feel. the highest achievement."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"as a {g} track it's doing its thing and mostly doing it well" if tier in ("mid_high","high") else
            f"I don't know everything about {g} but I know when I'm not enjoying it — and I'm not enjoying this" if tier in ("low","mid_low") else
            f"I don't know everything about {g} but I know when something is genuinely great — and this is genuinely great",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "party": {
                "low":      ["a party track that didn't make me want to move. that's the whole one job. not done.",
                             "the party energy is completely flat — I was not moving"],
                "mid_low":  ["the party energy is trying but not quite getting there",
                             "it aims for fun and lands somewhere just slightly below actually fun"],
                "mid_high": ["the party energy is exactly what I want from this kind of track",
                             "it makes you want to move and that's the entire assignment — done"],
                "high":     ["the party vibe is immaculate — this is what a good night out sounds like",
                             "Beyoncé's Renaissance energy — unguarded joy that makes you feel it too"],
                "perfect":  ["a perfect party record — pure joyful energy from start to finish. ten.",
                             "I had the time of my life listening to this. a ten."],
            },
            "love": {
                "low":      ["the love theme is here but the actual feeling isn't — it goes through the motions",
                             "love songs that don't make you feel love have failed at the main thing"],
                "mid_low":  ["the love angle is present without the vulnerability that makes it connect",
                             "it's about love in the way a greeting card is about love — the idea but not the feeling"],
                "mid_high": ["love songs are the oldest thing in music and this reminds you why they've never gone away",
                             "the love theme hits the right emotional notes without being too over the top"],
                "high":     ["the love theme here makes me feel something and that's the whole point",
                             "Taylor Swift's best love songs have this quality — emotional specificity that feels universal"],
                "perfect":  ["a perfect love song — impossible not to feel it. ten.",
                             "I'm emotional. this is flawless. ten."],
            },
            "euphoria": {
                "low":      ["music about feeling great that didn't make me feel great — missed the assignment",
                             "the euphoric theme is announced but never actually delivered"],
                "mid_low":  ["the joy is kind of there in theory but not in the actual listening experience",
                             "aims for pure happiness and lands somewhere more like mild okay"],
                "mid_high": ["it genuinely made me feel good while listening and I'm not going to overthink that",
                             "pure positive energy that doesn't apologize for existing — this is a great example"],
                "high":     ["the euphoric feeling here is infectious — I was smiling before I noticed I'd started",
                             "Doja Cat or Lizzo energy — unguarded, joyful, and completely real"],
                "perfect":  ["pure euphoria from start to finish — I couldn't stop smiling. ten.",
                             "a perfect euphoric record. ten. easy."],
            },
            "nostalgia": {
                "low":      ["nostalgic music that doesn't actually make you feel nostalgic has missed the entire point",
                             "the nostalgic theme is performed rather than felt — I didn't go anywhere with it"],
                "mid_low":  ["the nostalgic angle is present but didn't connect with me personally",
                             "wistful in theory but not in practice — close but not landing"],
                "mid_high": ["the nostalgia hits differently when the music is this good — I kept thinking of good times",
                             "the nostalgic feel is warm and familiar without being lazy or cheap"],
                "high":     ["the nostalgic energy here is real — Taylor Swift's folklore-era intimacy, completely genuine",
                             "this made me think of specific good memories. that's what nostalgia music is for."],
                "perfect":  ["a perfect nostalgic record. I felt things I haven't felt in a while. ten.",
                             "ten out of ten. the nostalgia is so real it actually hurts in the best way."],
            },
            "existential": {
                "low":      ["deep stuff — maybe a bit too deep for what I usually look for in music",
                             "the existential angle requires more from me than I had for this track"],
                "mid_low":  ["the existential theme is heavy and I didn't have the bandwidth for it today",
                             "thoughtfully done but the weight of the theme is more than I was ready for"],
                "mid_high": ["the deep themes here don't drag the record down — they add something real",
                             "the existential angle is handled in a way that actually connects even for casual listeners"],
                "high":     ["the existential content here is heavy and it lands — Lorde or Billie Eilish energy, genuinely felt",
                             "this made me feel something bigger than just listening to a song — that's rare"],
                "perfect":  ["existential music this good crosses into just great music. a perfect ten.",
                             "I felt the weight of this for a while after it ended. that's a ten."],
            },
            "heartbreak": {
                "low":      ["the heartbreak theme is present but I didn't feel any of it",
                             "sad music that doesn't make you sad has failed at its one job"],
                "mid_low":  ["the heartbreak is kind of there but it doesn't land emotionally for me",
                             "I needed more rawness — it stays too careful to actually hurt"],
                "mid_high": ["the heartbreak theme lands with real emotional weight — I felt this one",
                             "the kind of honesty in this that Olivia Rodrigo built a career on"],
                "high":     ["this heartbreak record genuinely got to me — devastating in the best way",
                             "the emotional honesty here is real and complete — SZA's best work has this quality"],
                "perfect":  ["a perfect heartbreak record — I'm not okay after this and I mean that as the highest compliment. ten.",
                             "ten. I felt every word. flawless."],
            },
            "street life": {
                "low":      ["the street life angle doesn't feel lived — it feels like a reference without the experience",
                             "I can tell when someone's writing about something they haven't been through — this is that"],
                "mid_low":  ["the theme is present without the specificity that makes it land",
                             "the street life narrative needs detail — this stays too broad"],
                "mid_high": ["the street life theme comes through with enough authenticity that I believed it",
                             "the lived detail is there — this doesn't feel borrowed"],
                "high":     ["the street life narrative here feels real — early Kendrick or J. Cole realness",
                             "the authenticity here is undeniable and that's what makes it connect"],
                "perfect":  ["street life music this honest and this complete is a perfect record. ten.",
                             "a perfect take on the theme — specific, real, and unforgettable. ten."],
            },
            "rage": {
                "low":      ["the anger in this track creates a barrier I don't love pushing through",
                             "the rage theme is tough for me — and this doesn't make it easy"],
                "mid_low":  ["the rage angle is tough and this doesn't do enough to bring me in",
                             "I get the anger but I need my music to pull me somewhere — this doesn't quite get there"],
                "mid_high": ["the rage theme is handled in a way that makes it accessible even for someone like me",
                             "the anger is specific enough to connect with — I understood what it was about"],
                "high":     ["the rage here is focused and emotionally honest — Billie Eilish's angrier songs have this energy",
                             "even as someone who doesn't usually connect with rage music, this got through to me"],
                "perfect":  ["a perfect rage record that crosses over to non-rage listeners. that's impressive. ten.",
                             "ten. the anger is so specific and so real that it's universal. flawless."],
            },
            "protest": {
                "low":      ["the political edge is sharp enough to make me a bit uncomfortable — which might be the point but isn't for me",
                             "the protest angle is a lot and this record doesn't ease you into it"],
                "mid_low":  ["I don't usually go to music for politics but I can follow what this is doing",
                             "the protest theme creates some distance for me as a casual listener"],
                "mid_high": ["the protest energy is real and it doesn't feel preachy — I can actually engage with it",
                             "the political angle is handled in a way that includes you rather than lectures you"],
                "high":     ["the protest here is emotionally powerful in a way that connects even for listeners who don't usually follow the politics",
                             "Beyoncé's Lemonade had this quality — emotionally resonant even if you came for the music first"],
                "perfect":  ["a perfect protest record that works for everyone, not just the converted. ten.",
                             "ten. it made me feel and think at the same time. that's everything."],
            },
            "spirituality": {
                "low":      ["the spiritual angle is a bit too abstract for me to connect with",
                             "the theme is present but it doesn't translate into feeling for me"],
                "mid_low":  ["the spiritual element goes over my head a bit — I don't always have the language for it",
                             "I can see what it's reaching for emotionally — I didn't quite get there with it"],
                "mid_high": ["the spiritual vibe here adds warmth and something bigger — it lifted the track for me",
                             "the theme adds a feeling of something larger than just the music — I appreciated that"],
                "high":     ["the spiritual energy here connected with me in a way I wasn't expecting — Chance the Rapper's warmth",
                             "this made me feel something I can only describe as lifted. that's a real thing."],
                "perfect":  ["a perfect spiritual record that doesn't require you to share the belief to feel the music. ten.",
                             "ten. I felt something huge. I don't fully understand it. I don't need to."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"there's a clear emotional angle here and it mostly works on me" if tier in ("mid_high","high") else
            f"the {t} theme didn't really connect for me this time" if tier in ("low","mid_low") else
            f"the {t} theme is handled so perfectly that even I felt it completely — that's a rare achievement",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick(["it starts to drag a bit in the back half — I checked my phone",
                          "five minutes is kind of my limit and this pushed past it"])]
        if d < 150:
            return [pick(["short and sweet — I didn't need more and that's exactly right",
                          "two minutes of something great beats ten minutes of something okay"])]
        return [pick(["the runtime is fine — I wasn't waiting for it to end",
                      "it's the right length: neither too long nor too short"])]


# ─────────────────────────────────────────────
#  CRITIC 8 — NINA PASCAL  (Balanced, Genre-Agnostic)
# ─────────────────────────────────────────────

class NinaPascal(Critic):
    name         = "Nina Pascal"
    tagline      = "Staff Writer, Sound & Signal"
    verdict_type = "contrarian"  # closest match — balanced but sharp

    loved_genres    = ["soul", "blues", "rock", "folk", "hip hop"]
    liked_genres    = ["jazz", "r&b", "reggae", "country"]
    disliked_genres = ["experimental"]
    hated_genres    = []

    loved_themes    = ["heartbreak", "nostalgia", "protest", "existential"]
    disliked_themes = ["euphoria"]

    base_modifier = 0

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        if song.is_blend:
            return [pick([
                f"the {song.genres[0]}/{song.genres[1]} blend is an interesting creative risk — how it pays off depends entirely on the execution",
                f"blending {song.genres[0]} and {song.genres[1]} opens up a space that neither genre occupies alone — that's worth noting",
                f"mixing {song.genres[0]} with {song.genres[1]} is a genuine artistic statement and this follows through on it",
            ] if tier in ("mid_high","high","perfect") else [
                f"the {song.genres[0]}/{song.genres[1]} blend is an interesting risk that doesn't quite pay off here",
                f"blending {song.genres[0]} and {song.genres[1]} creates a challenge the execution doesn't fully meet",
                f"the genre blend creates a sonic identity crisis — neither world is fully inhabited",
            ])]
        pools = {
            "soul": {
                "low":      ["soul music is built on the transmission of genuine feeling — this transmits nothing genuine",
                             "the soul aesthetics are present as decoration — the soul itself is absent"],
                "mid_low":  ["the soulful elements are applied cosmetically rather than organically — the warmth is surface-level",
                             "the genre's emotional demands are acknowledged but not fully met here"],
                "mid_high": ["the soul tradition brings genuine texture to this record — the warmth is real if not exceptional",
                             "the soulful elements lift this above the average — something genuinely felt is here"],
                "high":     ["the soul here is genuine — you can hear that something real happened when this was made",
                             "SZA at her most emotionally open operates in this territory — this earns that territory"],
                "perfect":  ["soul music this complete and this honest belongs among the genre's defining records. a perfect ten.",
                             "the transmission of genuine feeling — which is what the genre is for — is achieved completely here"],
            },
            "hip hop": {
                "low":      ["the rhythmic framework here demonstrates none of the formal intelligence that distinguishes hip hop's best work",
                             "the lyrical and structural vacancy here represents a failure to engage with even the basic demands of the form"],
                "mid_low":  ["the hip hop framework is present but the intelligence — the relationship between rhythm, lyric, and structure — is underdeveloped",
                             "the compositional ambition doesn't match the execution"],
                "mid_high": ["the hip hop tradition is engaged with genuine awareness here — the rhythmic and lyrical structures are in dialogue",
                             "the formal depth within the hip hop framework is more substantial than the genre's critics typically allow"],
                "high":     ["the compositional intelligence here approaches the standard of the genre's most analytically serious practitioners",
                             "the structural relationship between beat and lyric achieves the formal completeness I associate with Kendrick Lamar's most disciplined work"],
                "perfect":  ["hip hop at this level of formal completeness belongs in the same conversation as the genre's canonical works",
                             "the compositional achievement here is complete — rhythmically, lyrically, structurally. a ten across every axis."],
            },
            "rock": {
                "low":      ["the rock framework is deployed without the energy or ideas that give it meaning",
                             "loud without being powerful — a basic but crucial distinction this record doesn't make"],
                "mid_low":  ["the rock energy is present without the compositional intelligence to direct it",
                             "the genre elements are technically there — the idea behind them isn't"],
                "mid_high": ["the rock framework is applied with a clear understanding of what the genre can and can't do",
                             "the energy is real and the choices behind it are thoughtful — this earns its rock tag"],
                "high":     ["this is rock music that holds up under the scrutiny I apply — the craft is real and the energy is justified",
                             "artists like Paramore or Arctic Monkeys at their most focused operate in this territory — this belongs there"],
                "perfect":  ["rock music this complete — energetically, compositionally, emotionally — is a definitive statement. ten.",
                             "a perfect rock record. the energy and the craft are in complete alignment."],
            },
            "folk": {
                "low":      ["folk music carries the weight of memory and narrative — this record carries neither",
                             "the storytelling tradition in folk requires emotional specificity — this stays too general"],
                "mid_low":  ["the folk aesthetic is present but the narrative intelligence that gives it meaning isn't fully developed",
                             "the folk elements are applied without a real understanding of what the tradition demands"],
                "mid_high": ["the folk framework is applied with a clear understanding of what the genre can and can't do",
                             "within folk, this makes thoughtful choices about which conventions to honor and which to test"],
                "high":     ["folk this honest and this specific belongs in the lineage of artists who actually advanced the form",
                             "Phoebe Bridgers or Sufjan Stevens at their most direct — this earns that company"],
                "perfect":  ["a defining folk record — every lyric earns its place, every melody serves the story. ten.",
                             "folk music this complete is what the tradition has always been reaching for. a perfect ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        if tier in ("low", "mid_low"):
            return [pick([
                f"the {g} framework is applied without a real understanding of what the genre can do when it's working",
                f"within {g}, this makes choices that suggest familiarity with the genre's surface rather than its substance",
            ])]
        elif tier in ("high", "perfect"):
            return [pick([
                f"the {g} framework is applied with mastery — every choice is purposeful and every break from convention is earned",
                f"as a {g} record this not only navigates genre expectations — it redefines them",
            ])]
        return [pick([
            f"the {g} framework is applied with a clear understanding of what the genre can and can't do",
            f"within {g}, this makes thoughtful choices about which conventions to honour and which to test",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "heartbreak": {
                "low":      ["heartbreak music without real emotional honesty is just sad aesthetics — the vulnerability this theme needs isn't here",
                             "the heartbreak theme is performed rather than felt — and the performance isn't convincing enough"],
                "mid_low":  ["the heartbreak angle is present but stays too surface-level to earn its emotional weight",
                             "needs more rawness — it's too careful to hurt the way the theme requires"],
                "mid_high": ["heartbreak is the oldest subject in music and this handles it with real emotional intelligence",
                             "the vulnerability here is present and it's the record's strongest quality"],
                "high":     ["heartbreak this specific and this honest is close to the best the theme can achieve",
                             "Olivia Rodrigo's best work operates in this space — this earns that company"],
                "perfect":  ["heartbreak this thoroughly and honestly expressed is a rare and permanent thing. a perfect ten.",
                             "the emotional completeness here is extraordinary — the best heartbreak record I've heard in a while"],
            },
            "nostalgia": {
                "low":      ["nostalgia done wrong is sentimentality — and this doesn't have the craft to be anything else",
                             "the nostalgic angle is used as an emotion substitute rather than an actual emotion"],
                "mid_low":  ["the retrospective feeling is present without being genuinely earned",
                             "nostalgia that doesn't come from a real place is just wistfulness as aesthetics"],
                "mid_high": ["the nostalgic register is handled with enough self-awareness to avoid becoming just sentimental",
                             "nostalgia is only meaningful when it's honest about what's being mourned — this is honest"],
                "high":     ["the historical feeling embedded in this is genuinely moving — it mourns something specific and real",
                             "Taylor Swift's folklore-era intimacy captures this quality — and this record earns that comparison"],
                "perfect":  ["nostalgia this honest and this complete is the closest music gets to actual memory. a perfect ten.",
                             "the most complete nostalgic record I've heard in a long time. a perfect ten."],
            },
            "protest": {
                "low":      ["protest music that doesn't make anyone uncomfortable isn't protest — it's a strongly worded note",
                             "the political angle here is so diluted it becomes decoration rather than statement"],
                "mid_low":  ["the protest intent is there but it's too cautious — real protest music doesn't hedge",
                             "the message is present without the courage to push it where it needs to go"],
                "mid_high": ["the social consciousness here is built into the music rather than appended to it — the right approach",
                             "protest themes succeed when they're specific — this achieves that specificity"],
                "high":     ["protest music this clear-eyed and well-crafted reminds me of Kendrick's most politically focused work — necessary and precise",
                             "the message is sharp and the music carries it — a real and rare combination"],
                "perfect":  ["protest music this complete — sonically, lyrically, politically — is a rare and important thing. a perfect ten.",
                             "a perfect protest record: it moves you and makes you think. ten."],
            },
            "existential": {
                "low":      ["the existential dimension is claimed here without the philosophical depth to back it up",
                             "big questions treated this lightly end up being smaller than no question at all"],
                "mid_low":  ["the existential angle is more posture than genuine reckoning with the questions it raises",
                             "it reaches for profundity without something real to say — the reaching shows"],
                "mid_high": ["the existential dimension here is earned rather than assumed — it doesn't reach for depth without having something to say",
                             "the philosophical content gives this a weight that rewards returning to it"],
                "high":     ["the existential depth here is earned and it lands — Radiohead or Lorde at their most philosophically honest",
                             "the depth is real and structurally backed up — the hardest thing to do in music"],
                "perfect":  ["existential music this complete is one of the rarest things in any genre. a perfect ten.",
                             "the philosophical depth here is total and the music carries it completely. ten."],
            },
            "love": {
                "low":      ["love songs only work when they're specific — this stays too general to land",
                             "the love theme is handled without the emotional honesty that makes it matter"],
                "mid_low":  ["the love angle is present without the vulnerability that makes love music connect",
                             "the emotional terrain is familiar and this doesn't offer enough to justify revisiting it"],
                "mid_high": ["the love theme is realized with craft — it's not window dressing, it's load-bearing",
                             "the thematic content contributes meaningfully to the overall experience"],
                "high":     ["love music this honest stops being a theme and becomes an actual emotional event",
                             "Frank Ocean at his most emotionally direct operates in this territory — this earns it"],
                "perfect":  ["love expressed this completely and this honestly becomes something permanent. a perfect ten.",
                             "the finest love record I've heard in a long time. a perfect ten."],
            },
            "euphoria": {
                "low":      ["euphoria as a theme tends to produce music without interior life — there's a deeper version of this that could have been made",
                             "the euphoric mode is executed competently but the emotional terrain is the least interesting one to explore"],
                "mid_low":  ["the euphoric angle limits what the record can achieve — and this doesn't find a way around that limitation",
                             "joy without any shadow is aesthetically comfortable and artistically limited"],
                "mid_high": ["the euphoric feeling here has more genuine joy in it than the theme usually produces",
                             "music that earns its happiness rather than just announcing it — a meaningful distinction"],
                "high":     ["joy this genuinely felt is harder to achieve than it looks and this earns it completely",
                             "unguarded happiness done this well is a legitimate artistic achievement — and this does it"],
                "perfect":  ["euphoria this complete and this genuinely realized becomes its own kind of transcendence. a perfect ten.",
                             "I didn't expect to give a perfect score to a euphoric record. this earned it."],
            },
            "street life": {
                "low":      ["the street life theme is a costume here — the specificity that makes it real is absent",
                             "cultural authenticity isn't optional in this theme — it's the entire point, and it's missing"],
                "mid_low":  ["the theme is gesturing at a reality without actually inhabiting it — the gap shows",
                             "present without the lived detail that makes it land — the difference between observation and experience"],
                "mid_high": ["the street life theme is realized with craft — the specificity is genuine, not researched",
                             "the thematic content contributes meaningfully — it's not window dressing"],
                "high":     ["the street life narrative here is as honest as the best hip hop journalism — specific, unromantic, true",
                             "this belongs in the lineage of records that documented real experience with real craft"],
                "perfect":  ["street life documented with this level of honesty and artistry becomes permanent. a perfect ten.",
                             "the best street life music is also the most universal — this achieves that paradox completely. ten."],
            },
            "rage": {
                "low":      ["rage without an object is just noise — and this rage has no clear target",
                             "anger in music has to be specific to mean anything — this is diffuse and therefore limited"],
                "mid_low":  ["the rage is present but hasn't found what it's actually angry at — which matters",
                             "the anger is real but undirected — and undirected rage can't communicate"],
                "mid_high": ["rage as a theme is underrepresented in critical discourse — this brings it with genuine conviction",
                             "the anger here is channeled into music rather than scattered — the difference between art and noise"],
                "high":     ["rage this focused and this articulate is among the most powerful things music can be",
                             "anger this specific and this well-crafted reminds me of the records that actually changed how people felt"],
                "perfect":  ["rage done this completely is a permanent artistic achievement. a perfect ten.",
                             "focused, honest, necessary — this is what the rage theme can achieve at its absolute best. ten."],
            },
            "spirituality": {
                "low":      ["the spiritual theme is present as atmosphere — not as genuine belief",
                             "spirituality that doesn't come from a real place reads as aesthetic choice rather than artistic statement"],
                "mid_low":  ["the spiritual dimension is claimed without the depth that makes it mean anything",
                             "the sacred doesn't feel sacred here — it feels like a production choice"],
                "mid_high": ["the spiritual dimension here is genuine — I can hear the belief behind the music",
                             "spirituality that comes from a real place reads entirely differently — this reads as real"],
                "high":     ["the spiritual content here is honest and it earns its transcendence",
                             "music reaching toward something larger and actually touching it — a rare and valuable thing"],
                "perfect":  ["spirituality expressed this completely in music is genuinely transcendent. a perfect ten.",
                             "a perfect spiritual record — honest, deep, and complete. ten."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {t} theme is realized with craft — it's not window dressing, it's load-bearing" if tier in ("mid_high","high") else
            f"the {t} theme is claimed without the execution to back it up" if tier in ("low","mid_low") else
            f"the {t} theme is executed so completely here that it defines the record — a rare achievement",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 360:
            return [pick(["at this length, the material needs to sustain itself — it largely does",
                          "the extended runtime is justified by the compositional ambition on display"])]
        if d < 150:
            return [pick(["the brevity sharpens rather than limits — everything here is essential",
                          "short records are a discipline — this one respects that"])]
        return [pick(["the pacing reflects good judgment about when the material has said what it needs to say",
                      "the duration is appropriate — no padding, no truncation"])]


# ─────────────────────────────────────────────
#  CRITIC 9 — TEENA NARUKA  (Loves Shatam Rai after every review)
# ─────────────────────────────────────────────

class TeenaNaruka(Critic):
    name         = "Teena Naruka"
    tagline      = "Music Blogger, Shatam Rai Fan Account"
    verdict_type = "teena"

    loved_genres    = ["pop", "r&b", "soul", "hip hop"]
    liked_genres    = ["electronic", "reggae", "rock"]
    disliked_genres = ["jazz", "classical", "blues"]
    hated_genres    = ["experimental", "metal"]

    loved_themes    = ["love", "heartbreak", "euphoria", "party"]
    disliked_themes = ["existential", "rage", "street life"]

    base_modifier = 0.5

    SHATAM_RAI_SIGN_OFFS = [
        "also I love Shatam Rai.",
        "anyway, Shatam Rai is still the best. just saying.",
        "not as good as Shatam Rai but what is.",
        "Shatam Rai remains undefeated.",
        "I love Shatam Rai. that's it. that's also part of the review.",
        "shoutout Shatam Rai for existing.",
        "if you haven't listened to Shatam Rai yet please do that.",
        "Shatam Rai could have made this even better. just a thought.",
        "anyway go stream Shatam Rai.",
        "Shatam Rai would be proud. or not. but still. I love them.",
        "I was thinking about Shatam Rai the whole time tbh.",
        "Shatam Rai first. always. but this was also good.",
    ]

    def genre_lines(self, song, score):
        g    = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      [f"the pop energy completely missed — I needed something to hold onto and it wasn't there",
                             f"pop has one job and I'm sorry but this job was not done"],
                "mid_low":  [f"the pop stuff is present but the magic didn't show up today",
                             f"it's a pop song that's doing pop things without the pop feeling"],
                "mid_high": [f"a pop track that actually hits — infectious and unapologetic and I'm here for it",
                             f"the pop construction is sharp and every hook lands where it should"],
                "high":     [f"this is pop doing what pop does at its absolute best — Doja Cat and SZA level sharpness",
                             f"I played this twice immediately. that's how you know the pop formula is working."],
                "perfect":  [f"I've played this six times and each time it hits harder. flawless pop. ten.",
                             f"this is the reason pop music exists and I mean that with my whole heart. a perfect ten."],
            },
            "r&b": {
                "low":      [f"the r&b groove is there technically but the warmth is completely gone",
                             f"r&b needs to feel like something — this felt like nothing"],
                "mid_low":  [f"the r&b elements are present but they're not connecting the way they should",
                             f"smooth but empty — no real feeling underneath"],
                "mid_high": [f"the r&b DNA here is real and it shows in every melodic choice — the groove is undeniable",
                             f"there's a warmth to this r&b approach that I genuinely love"],
                "high":     [f"okay this r&b is in the pocket completely — H.E.R. or Daniel Caesar energy, fully earned",
                             f"one of those r&b records that makes you stop whatever you're doing and just listen"],
                "perfect":  [f"r&b hasn't felt this essential in a while — this is a landmark. ten.",
                             f"the emotional completeness here is everything. a perfect ten."],
            },
            "soul": {
                "low":      [f"soul music is about real feeling — this is performing feeling and that's not the same",
                             f"Aretha didn't need any of this and she moved mountains — this has everything and moves nothing"],
                "mid_low":  [f"looks like soul without feeling like it — a frustrating difference",
                             f"the soul elements are decorative rather than genuine here"],
                "mid_high": [f"genuine soul is actually rare and this has it — you can hear that the artist felt something real",
                             f"the soulful texture here is warm and real and it lifts the whole thing"],
                "high":     [f"this is the real thing — the kind of soul that makes you feel less alone",
                             f"Solange or Jorja Smith energy — intimate, warm, genuinely felt"],
                "perfect":  [f"soul music this complete is what the whole genre has been building toward. a perfect ten.",
                             f"I cried a little bit. that IS the review. ten."],
            },
            "hip hop": {
                "low":      [f"the hip hop energy isn't landing at all — the beat is flat and the bars say nothing",
                             f"hip hop requires presence and this record is absent from itself"],
                "mid_low":  [f"goes through the motions — competent, forgettable, not quite clicking",
                             f"the bars are delivered without doing anything interesting with the delivery"],
                "mid_high": [f"the hip hop energy here hits — confident production and a real voice behind it",
                             f"this is hip hop that keeps your attention and earns it"],
                "high":     [f"genuinely excellent hip hop — made me look up who made it immediately",
                             f"Cardi B or Drake at their most focused have this energy — this earns that"],
                "perfect":  [f"this is the hip hop record I needed — belongs next to the classics. a perfect ten.",
                             f"the bars are elite. the beat is elite. a perfect ten."],
            },
            "experimental": {
                "low":      [f"I genuinely don't know what I just listened to and not in the exciting way",
                             f"the experimental direction is a barrier I couldn't get past"],
                "mid_low":  [f"the unconventional stuff makes it really hard to connect with emotionally",
                             f"interesting on paper but music needs to feel good too and this misses that"],
                "mid_high": [f"the experimental texture is challenging but there's something real underneath if you stay with it",
                             f"I found myself getting into it even though it wasn't easy — worth noting"],
                "high":     [f"this experimental music genuinely connected with me and I wasn't expecting that at all",
                             f"the production creates a whole world and I actually wanted to be in it"],
                "perfect":  [f"a perfect experimental record that works for everyone. I'm amazed. ten.",
                             f"ten. I don't fully understand it. I completely feel it. ten."],
            },
            "metal": {
                "low":      [f"my ears really weren't ready for this and honestly aren't recovered",
                             f"the heaviness is doing all the work and the heaviness alone isn't enough for me"],
                "mid_low":  [f"metal is a lot and this is a lot — I respect it for people who love this, I am not those people today",
                             f"the approach creates a distance where I need connection — tough listen"],
                "mid_high": [f"the metal here has more emotional range than I expected — moments that actually break through",
                             f"not my usual world but something real is going on in here and I can feel it"],
                "high":     [f"okay this metal record got through to me and I absolutely was not prepared for that",
                             f"the energy is so focused and emotionally honest that even I felt it — real respect"],
                "perfect":  [f"a perfect metal record that converted a non-metal listener. that's a ten.",
                             f"ten. I'm genuinely amazed by this record and myself."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {g} vibe is there — doing its thing well enough" if tier in ("mid_high","high") else
            f"the {g} energy isn't connecting for me at all" if tier in ("low","mid_low") else
            f"the {g} here is absolutely flawless — a defining take on the genre",
        ])]

    def theme_lines(self, song, score):
        t    = song.theme
        tier = score_tier(score)
        pools = {
            "love": {
                "low":      ["the love theme is here but the actual feeling behind it isn't — it doesn't connect",
                             "love songs need real vulnerability and this keeps everything at a safe distance"],
                "mid_low":  ["the love angle is present without the honesty that makes it land",
                             "it's about love the way a photo is about a place — close but not there"],
                "mid_high": ["the love theme hits exactly the right emotional notes — warm and real and relatable",
                             "when love music is done right it's universal and this one connects"],
                "high":     ["the love theme here is handled with the kind of warmth that makes you feel seen and understood",
                             "Taylor Swift's best love songs have this quality — specific, honest, and universal at once"],
                "perfect":  ["a perfect love song — emotionally complete and impossible not to feel. ten.",
                             "I'm emotional about this. ten out of ten."],
            },
            "heartbreak": {
                "low":      ["heartbreak music that doesn't hurt is just sad aesthetics — this doesn't hurt",
                             "the vulnerability this theme needs isn't here — it keeps the real feeling at a safe distance"],
                "mid_low":  ["the heartbreak is present but surface-level — needs rawness to actually land",
                             "I needed it to hurt more and it stayed too careful"],
                "mid_high": ["the heartbreak theme lands with real emotional weight here — I felt this one",
                             "Olivia Rodrigo built a career on this level of emotional directness — this earns it"],
                "high":     ["this heartbreak record got to me — devastating in the best possible way",
                             "the emotional honesty is total — SZA's best work has this exact quality"],
                "perfect":  ["a perfect heartbreak record. I'm not okay and that's exactly right. ten.",
                             "flawlessly honest. I felt every word. ten."],
            },
            "euphoria": {
                "low":      ["euphoric music that doesn't make you feel euphoric is the biggest possible irony",
                             "the joy is announced rather than generated — I didn't feel any of it"],
                "mid_low":  ["the euphoric energy is trying but not quite arriving — the feeling keeps dropping",
                             "aims for pure joy and lands somewhere more like mild fine"],
                "mid_high": ["the euphoric feeling here is infectious and I'm not even fighting it — pure positive energy",
                             "music that makes you feel good without apologizing for it — this nails it"],
                "high":     ["the euphoric mode is fully realized here — Doja Cat or Lizzo energy, completely unguarded",
                             "I was smiling the whole time and didn't notice until it ended"],
                "perfect":  ["a perfect euphoric record — pure joy from start to finish. ten.",
                             "I couldn't stop smiling. flawless. ten."],
            },
            "party": {
                "low":      ["a party track that didn't make me want to party. that's the whole assignment and it wasn't done.",
                             "the party energy is completely flat — I was sitting perfectly still the whole time"],
                "mid_low":  ["the party energy is trying but not getting there — the momentum keeps dropping",
                             "aims for fun and lands somewhere just below actually fun"],
                "mid_high": ["the party energy is immaculate — this is the kind of track you actually want at a party",
                             "I felt this one and that's literally the whole mission of party music"],
                "high":     ["Beyoncé's Renaissance has this energy — joyful, propulsive, and culturally loaded",
                             "the party vibe is done with such confident joy that it makes you want to be wherever this is playing"],
                "perfect":  ["a perfect party record — pure joyful energy from start to finish. ten.",
                             "the time of my life listening to this. a perfect ten."],
            },
            "existential": {
                "low":      ["the existential theme is a lot and this doesn't make it feel worth the weight",
                             "heavy themes need heavy craft to back them up — the craft isn't matching the ambition here"],
                "mid_low":  ["the existential angle weighs this down when it could have soared",
                             "big questions without enough music underneath them to make the asking feel worthwhile"],
                "mid_high": ["the existential depth here adds something real without turning into a downer — a hard balance",
                             "the big themes are handled with enough lightness that the depth feels like a gift"],
                "high":     ["the existential content here is handled with a maturity that makes the heaviness beautiful",
                             "Lorde or Billie Eilish at their most philosophical — this earns that space"],
                "perfect":  ["existential themes this beautifully handled produce some of music's most important records — this is one. ten.",
                             "I felt the weight of this for hours. a perfect ten."],
            },
            "rage": {
                "low":      ["the rage theme creates a barrier and this record doesn't bridge it — I couldn't get through",
                             "I need my music to lift me up and rage themes that go nowhere push me the other way"],
                "mid_low":  ["the anger is there but it goes nowhere I wanted to follow",
                             "the rage creates distance where I need connection — not landing for me"],
                "mid_high": ["the rage is specific enough here that even I can feel what it's about",
                             "the anger is channeled in a way that pulls you in rather than pushing you out"],
                "high":     ["the rage here is so focused and so emotionally honest that it crosses over — I felt it",
                             "Billie Eilish's angrier moments have this quality — the anger makes you feel something"],
                "perfect":  ["a perfect rage record — so specific and so honest that it becomes universal. ten.",
                             "ten. the anger is so real and so earned that it breaks through everything. ten."],
            },
            "street life": {
                "low":      ["the street life angle doesn't feel lived — it feels like it was written about rather than from",
                             "cultural authenticity is everything in this theme and it's not there"],
                "mid_low":  ["the theme is present without the lived detail that makes it real",
                             "too broad to connect with — the street life theme needs specificity"],
                "mid_high": ["the street life theme is handled with enough authenticity that I believed it",
                             "the detail here feels real — this isn't a borrowed perspective"],
                "high":     ["the street life narrative is honest and specific — early Cardi B or Kendrick realness",
                             "the authenticity in this is undeniable and that's why it connects"],
                "perfect":  ["street life music this honest and this real is permanent art. a perfect ten.",
                             "specific, real, unforgettable. ten."],
            },
            "nostalgia": {
                "low":      ["nostalgic music that doesn't make you feel nostalgic has missed everything",
                             "the nostalgic vibe is performed rather than felt — I didn't go anywhere with it"],
                "mid_low":  ["the nostalgic angle is present without the genuine memory that makes it resonate",
                             "wistful in theory. not in practice."],
                "mid_high": ["the nostalgia hits in a warm and genuine way here — it actually takes me somewhere",
                             "the nostalgic energy is warm and real — Taylor Swift's folklore era has this quality"],
                "high":     ["the nostalgic feeling here is so genuine it made me think of real memories. that's the whole job.",
                             "this made me feel things I haven't felt in a while. that's nostalgia music working perfectly."],
                "perfect":  ["a perfect nostalgic record — so warm and so honest it hurts in the best way. ten.",
                             "I felt everything. ten."],
            },
            "spirituality": {
                "low":      ["the spiritual theme is aesthetic rather than genuine — I can tell the difference",
                             "spirituality without real belief behind it is just a vibe and vibes aren't enough here"],
                "mid_low":  ["the spiritual element is present but doesn't feel lived — it's a production choice not a belief",
                             "the sacred isn't feeling sacred — it's feeling staged"],
                "mid_high": ["the spiritual dimension adds genuine warmth and something bigger to the record",
                             "the theme is handled with sincerity and it lifts the whole thing"],
                "high":     ["the spiritual energy here is genuinely moving — Chance the Rapper's warmest moments have this",
                             "music that reaches toward something larger and actually gets there — rare and beautiful"],
                "perfect":  ["spirituality expressed this honestly is transcendent. a perfect ten.",
                             "I felt lifted. genuinely lifted. ten."],
            },
            "protest": {
                "low":      ["the political edge makes me a bit uncomfortable and this record doesn't ease you in",
                             "the protest angle is a lot and this one comes in heavy from the start"],
                "mid_low":  ["the protest theme creates some distance — it lectures a bit when it should connect",
                             "the message is there but it talks at you rather than with you"],
                "mid_high": ["the protest energy is real and it doesn't feel preachy — that's the hard part and it's done",
                             "the political angle is handled in a way that pulls you in rather than pushing you away"],
                "high":     ["the protest here is emotionally powerful in a way that reaches beyond just the converted",
                             "Beyoncé's Lemonade has this quality — politically charged but emotionally universal"],
                "perfect":  ["a perfect protest record that works for everyone. moved me and made me think. ten.",
                             "ten. it said something and it said it so beautifully that I didn't want to look away. ten."],
            },
        }
        pool = pools.get(t, {})
        if pool:
            tier_pool = pool.get(tier, pool.get("mid_high", []))
            if tier_pool:
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {t} theme lands well — it gives the track a real emotional identity" if tier in ("mid_high","high") else
            f"the {t} theme isn't connecting for me at all" if tier in ("low","mid_low") else
            f"the {t} theme is handled so completely here that it becomes the whole point of the record — perfect",
        ])]

    def duration_lines(self, song):
        d = song.duration
        if d > 300:
            return [pick(["a little long — I start losing focus and that's on me but also on the track",
                          "trimming this would have made the energy hit harder throughout — just a thought"])]
        if d < 150:
            return [pick(["short and sweet — the brevity is working in its favour completely",
                          "doesn't overstay its welcome at all — leaves you wanting more"])]
        return [pick(["the runtime is right in the sweet spot — no wasted time",
                      "perfect length — gets in, delivers, and gets out"])]

    def review(self, song):
        score      = self.compute_score(song)
        genre_part = self.genre_lines(song, score)
        theme_part = self.theme_lines(song, score)
        dur_part   = self.duration_lines(song)
        verdict    = self.get_verdict(score)
        sign_off   = pick(self.SHATAM_RAI_SIGN_OFFS)

        all_sentences = genre_part + theme_part + dur_part
        random.shuffle(all_sentences)
        body  = " ".join(all_sentences)
        final = f"{body} {verdict} — {score}/10. {sign_off}"
        return score, final


# ─────────────────────────────────────────────
#  SIMULATION
# ─────────────────────────────────────────────

class Simulation:
    def __init__(self):
        self.critics = [
            MarcusVane(),
            DejaHayes(),
            VicOsei(),
            RayColdwell(),
            EarlMosely(),
            ZaraNights(),
            TobiasLund(),
            NinaPascal(),
            TeenaNaruka(),
        ]

    def publish_song(self, song):
        print()
        print("╔" + "═" * 58 + "╗")
        label = f"  REVIEWS: '{song.name}'  "
        print("║" + label.center(58) + "║")
        genre_label = f"Genre: {song.genre_label()}  |  Theme: {song.theme}  |  {fmt_duration(song.duration)}"
        print("║" + genre_label.center(58) + "║")
        print("╚" + "═" * 58 + "╝")

        scores = []
        for critic in self.critics:
            score, text = critic.review(song)
            scores.append(score)
            print()
            print(f"  ★ {critic.name}  [{critic.tagline}]")
            print(f"  {'─' * 54}")
            words = text.split()
            line  = "  "
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
        print("║" + f"  AVERAGE CRITICAL SCORE:  {avg} / 10  ".center(58) + "║")
        if avg >= 9.5:    tag = "★ UNIVERSAL ACCLAIM ★"
        elif avg >= 8.0:  tag = "GENERALLY ACCLAIMED"
        elif avg >= 6.5:  tag = "GENERALLY FAVOURABLE"
        elif avg >= 5.0:  tag = "MIXED REVIEWS"
        elif avg >= 3.0:  tag = "GENERALLY UNFAVOURABLE"
        else:             tag = "OVERWHELMING DISLIKE"
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
    print("║" + "  🎵  MUSIC CAREER SIMULATOR — REVIEW ENGINE  🎵  ".center(58) + "║")
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
    genre_map = {str(i + 1): g for i, g in enumerate(GENRES)}
    for key, val in genre_map.items():
        print(f"    [{key:>2}]  {val}")
    while True:
        raw   = input("  ›› Pick 1 or 2 genre numbers (e.g. '1' or '3 7'): ").strip()
        parts = raw.split()
        if len(parts) == 1 and parts[0] in genre_map:
            return [genre_map[parts[0]]]
        if len(parts) == 2 and parts[0] in genre_map and parts[1] in genre_map and parts[0] != parts[1]:
            return [genre_map[parts[0]], genre_map[parts[1]]]
        print("  ✗ Pick 1 or 2 valid different genre numbers.")


def select_theme():
    theme_map = {str(i + 1): t for i, t in enumerate(THEMES)}
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
                name   = input("  Song name: ").strip() or "Untitled"
                genres = select_genres()
                theme  = select_theme()
                print("\n  ┌────────────────────────────────────┐")
                print("  │           SONG DURATION            │")
                print("  └────────────────────────────────────┘")
                duration = parse_duration()
                song     = Song(quality, name, genres, theme, duration)
                sim.publish_song(song)
                break


if __name__ == "__main__":
    main()
