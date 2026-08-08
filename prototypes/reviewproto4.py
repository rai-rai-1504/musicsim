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

def score_tier(score):
    """Map a computed score to a sentiment tier for genre commentary."""
    if score <= 3:
        return "low"
    elif score <= 5:
        return "mid_low"
    elif score <= 7:
        return "mid_high"
    elif score <= 9:
        return "high"
    else:
        return "perfect"

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

    def genre_lines(self, song, score):
        """Return 2 lines about the genre(s), tone-matched to score."""
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
                score += 1.5 * scale
            elif g in self.liked_genres:
                score += 0.5 * scale
            elif g in self.hated_genres:
                score -= 2 * scale
            elif g in self.disliked_genres:
                score -= 1 * scale

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
        genre_part = self.genre_lines(song, score)
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        pools = {
            "experimental": {
                "low":      [f"the experimental ambition here is undone entirely by the execution — Xenakis would call this noise for the wrong reasons",
                             f"the avant-garde posture collapses on inspection; there is nothing underneath the dissonance",
                             f"experimental music requires courage and craft in equal measure — this record has neither"],
                "mid_low":  [f"the experimental framing gestures at something genuinely interesting without committing to it",
                             f"there are moments where the unconventional structure rewards patience, but they don't hold together",
                             f"it's challenging in ways that feel accidental rather than intentional"],
                "mid_high": [f"the experimental framework here is genuinely ambitious — rare to see someone commit this fully",
                             f"structurally adventurous in ways most artists avoid out of commercial fear",
                             f"it pushes against convention without announcing that it's doing so, which is the mark of real craft"],
                "high":     [f"the willingness to destabilize expectation is the most interesting thing about this record — and it pays off",
                             f"this sits in the lineage of Arca and Matana Roberts without borrowing their vocabulary wholesale",
                             f"genuinely bold experimental work: the kind that earns the label rather than hiding behind it"],
                "perfect":  [f"I have waited years for something this uncompromising — this is what Coltrane meant by going beyond",
                             f"the formal logic here is so complete and so radical that I find myself revising what I thought experimental music could still be",
                             f"an experimental record that doesn't just push the boundary — it redraws it"],
            },
            "jazz": {
                "low":      [f"the jazz vocabulary is deployed here like someone learned it from a chart and forgot to listen to Coltrane",
                             f"it butchers the harmonic tradition — the changes are there but the soul has been evacuated",
                             f"Miles Davis built a career on knowing when not to play; this record doesn't know that lesson exists",
                             f"jazz requires musicianship that this doesn't even pretend to reach for"],
                "mid_low":  [f"the jazz elements surface occasionally but the improvisational logic is missing — it sounds like genre cosplay",
                             f"the chord vocabulary is borrowed from jazz without understanding the emotional function it serves",
                             f"you can hear the influence of Herbie Hancock but none of the restraint that made him essential"],
                "mid_high": [f"the jazz sensibility gives this genuine harmonic depth — you can hear the lineage without being oppressed by it",
                             f"the improvised spaces breathe in ways pre-composed music simply cannot replicate, and this uses them well enough",
                             f"the trumpet work here reminds me of something late-era Freddie Hubbard might have approved of"],
                "high":     [f"it draws on the tradition without being enslaved to it — that balance is difficult to achieve and this achieves it",
                             f"the jazz architecture here rewards repeated listening, which is all I ask of music",
                             f"the kind of sophisticated harmonic thinking that puts one in the company of Wayne Shorter — rare praise and earned"],
                "perfect":  [f"I am not often floored by jazz records — I have heard too many — but this made me feel the way Kind of Blue made me feel the first time",
                             f"the interplay between the instruments reaches the conversational depth of the great quartets; this is a landmark record",
                             f"the tradition lives here — not as imitation but as continuation. this is what jazz has always been reaching toward"],
            },
            "classical": {
                "low":      [f"the classical framework is present and misunderstood — this is what happens when composers study scores without listening to them",
                             f"the formal structure collapses under the compositional weight it tries to bear",
                             f"Shostakovich managed tension under existential pressure; this can't manage it under studio conditions"],
                "mid_low":  [f"the classical influence is audible but applied decoratively rather than structurally — it's wallpaper not architecture",
                             f"the orchestral logic is present in fragments but never coheres into anything that justifies the ambition"],
                "mid_high": [f"the classical influence lends it structural coherence rarely found in contemporary work",
                             f"you can hear a composer's mind at work here — the form serves the content, which is the classical principle applied correctly",
                             f"the orchestral logic underlying this is exactly what modern composition has been neglecting"],
                "high":     [f"the structural ambition here earns comparisons to the modern classical tradition — not Brahms, but perhaps Arvo Pärt in his more accessible register",
                             f"this rewards close attention with the same quality of return as a great chamber piece — that is not a casual observation",
                             f"the compositional rigor here is exceptional; the architecture holds regardless of where you enter"],
                "perfect":  [f"I have revised my sense of what contemporary classical work can be on the basis of this record",
                             f"this belongs in the conversation with the great modern works — Messiaen, Glass, Pärt — and does not embarrass itself in that company",
                             f"a compositional achievement that may not be fully understood for years. a ten by every standard I hold."],
            },
            "blues": {
                "low":      [f"the blues tradition requires a relationship with suffering that this record clearly doesn't have — it's hollow",
                             f"Robert Johnson made a deal at the crossroads for something more honest than this",
                             f"the twelve-bar structure is here; the humanity it's supposed to carry is absent"],
                "mid_low":  [f"the blues elements are present but the emotional authenticity is manufactured — you can hear the gap",
                             f"Muddy Waters never needed to try this hard to sound like he meant it"],
                "mid_high": [f"the blues tradition brings a weight to this record that justifies the slower passages",
                             f"there's a conversation happening between the guitar and the voice that the blues lineage uniquely enables"],
                "high":     [f"the blues feeling here is genuine — it carries the weight that the tradition demands without performing it",
                             f"this sits in the lineage from Son House forward and holds its place with dignity"],
                "perfect":  [f"blues at this level stops being a genre and becomes a philosophy — this record understands that completely",
                             f"the depth of feeling here rivals the great Chicago records; I did not expect to write that sentence today"],
            },
            "folk": {
                "low":      [f"the folk tradition demands honesty above all things; this record is not honest",
                             f"Nick Drake made sparseness feel infinite — this makes it feel empty"],
                "mid_low":  [f"the folk framework is applied but the storytelling — the essential element — is underdeveloped",
                             f"there's a narrative intent here that the musical execution doesn't support"],
                "mid_high": [f"the folk tradition brings a narrative integrity that anchors the lyrical content effectively",
                             f"this engages the folk canon with respect and some critical distance — a mature approach"],
                "high":     [f"the storytelling here has the weight of the great folk tradition — the kind of song that survives because it carries truth",
                             f"I find myself thinking of Richard Thompson — the specificity of image, the emotional precision. high praise."],
                "perfect":  [f"folk music at this level becomes testimony — this record will be listened to in fifty years and the feeling will survive",
                             f"the narrative and musical intelligence here rivals the great singer-songwriter tradition at its peak"],
            },
            "pop": {
                "low":      [f"pop, as a genre, has produced one original idea per decade — this is not that idea, nor is it a good example of any prior one",
                             f"this is what happens when commercial instinct replaces musical instinct entirely — a product, not a record",
                             f"I find pop's insistence on pleasantness dishonest; this record makes that dishonesty especially visible",
                             f"even on pop's own terms — memorability, hook, feeling — this fails"],
                "mid_low":  [f"the pop framework checks the expected boxes without understanding why those boxes exist",
                             f"the {g} approach reduces whatever potential this had to the lowest common denominator of passive consumption"],
                "mid_high": [f"the pop structure is applied with more intelligence than I usually find in this corner of the genre",
                             f"I find the form constraining, but within those constraints, there are genuine craft decisions here"],
                "high":     [f"this is pop that makes me question my biases — the craft inside the commercial frame is real",
                             f"a pop record that earns its hooks rather than simply deploying them — a meaningful distinction"],
                "perfect":  [f"I am genuinely astonished to write this, but pop music has never felt this necessary to me — a perfect record by any standard",
                             f"this transcends the genre categorization entirely; the pop frame is the least interesting thing about it"],
            },
            "electronic": {
                "low":      [f"synthesizers are tools, not ideas — this track mistakes one for the other, repeatedly and loudly",
                             f"the electronic production substitutes texture for substance in a way I find both tiresome and predictable",
                             f"there is nothing here that Aphex Twin didn't make irrelevant twenty years ago"],
                "mid_low":  [f"the {g} framework gives the illusion of innovation while doing nothing genuinely new",
                             f"the production choices are technically competent and aesthetically empty"],
                "mid_high": [f"electronic music at its best interrogates sound — this does so with partial success",
                             f"the production language is more considered than most in this space; it's deployed intelligently if not brilliantly"],
                "high":     [f"the electronic architecture here is genuinely sophisticated — it understands that texture is argument, not decoration",
                             f"this sits in conversation with the serious end of the tradition — Autechre, perhaps, without the academic coldness"],
                "perfect":  [f"the electronic composition here has the internal logic and emotional range of the greatest records in the form",
                             f"I am not someone who gives electronic music the benefit of the doubt, which makes this score all the more significant"],
            },
            "hip hop": {
                "low":      [f"the hip hop framework is here; the lyricism and sonic intelligence are not — a record made in the shape of the genre without its content",
                             f"Rakim built an entire aesthetic philosophy in four minutes — this can't build a coherent verse"],
                "mid_low":  [f"the hip hop elements are competently assembled but the artistic voice is absent",
                             f"the beat construction is derivative and the bars offer nothing that wasn't said better on a 1994 record"],
                "mid_high": [f"the hip hop tradition is engaged with honestly here — the production has weight and the lyricism has intent",
                             f"there's a genuine relationship to the form — not just Kendrick's shadow but something with its own posture"],
                "high":     [f"this is the kind of hip hop record that holds up under the scrutiny the genre's best work demands",
                             f"the lyricism here operates on multiple registers simultaneously — the mark of a genuine artist working in the tradition"],
                "perfect":  [f"hip hop at this level stops being genre and becomes literature — this record earns that claim",
                             f"I think of this alongside Illmatic and To Pimp a Butterfly: records that permanently expand what the form can contain"],
            },
            "r&b": {
                "low":      [f"r&b's emotional vocabulary has been reduced here to pure formula — there is no feeling behind the smoothness",
                             f"the genre demands genuine vulnerability; this offers a convincing imitation of it and nothing more"],
                "mid_low":  [f"the r&b elements are present but the groove is mechanical — it moves without feeling",
                             f"the production is slick in a way that erases the human warmth the genre is built on"],
                "mid_high": [f"the r&b sensibility is applied with enough genuine feeling to rise above the generic",
                             f"the melodic intelligence here is real — not D'Angelo, but a record that knows what D'Angelo was doing"],
                "high":     [f"the emotional depth of the r&b tradition is honored here rather than merely invoked",
                             f"this sits close to the best of the neo-soul tradition — the kind of record that makes the genre's defenders feel vindicated"],
                "perfect":  [f"r&b at this level earns the comparison to its greatest records — this has the emotional range and craft of the form's finest hours",
                             f"I find myself revising my skepticism of the genre on the basis of this record alone"],
            },
            "metal": {
                "low":      [f"the metal heaviness is deployed without the compositional intelligence that distinguishes Sabbath from noise",
                             f"aggression without architecture is just volume — and volume is the cheapest thing in music"],
                "mid_low":  [f"the metal framework has craft in places but the emotional range is too narrow to sustain the runtime",
                             f"technically accomplished in moments but the intellectual content doesn't match the sonic ambition"],
                "mid_high": [f"the {g} intensity is deployed with more craft than the genre usually receives credit for",
                             f"heavy music deserves serious analysis and this record makes that case with some conviction"],
                "high":     [f"this is metal that rewards the kind of attention usually reserved for more academically approved genres",
                             f"the compositional density here rivals the great records in the form — this is serious music in loud clothes"],
                "perfect":  [f"I have resisted metal for thirty years; this record has made that resistance feel like a mistake",
                             f"the structural and emotional ambition here is complete — a perfect record that happens to be heavy"],
            },
            "punk": {
                "low":      [f"punk without conviction is just noise with a three-chord budget",
                             f"the Clash had something to say — this is anger without object, which is just bad manners"],
                "mid_low":  [f"the punk energy is present but the ideas aren't there to justify it",
                             f"rawness is a style choice; this mistakes it for a substitute for content"],
                "mid_high": [f"the punk rawness is the most honest thing about this record — the directness is earned",
                             f"the {g} energy is confrontational in a way most music is too cowardly to attempt"],
                "high":     [f"punk that actually has something to say — the form and the content are aligned in a way the genre rarely achieves",
                             f"this carries the conviction of the great punk records without being a museum piece about them"],
                "perfect":  [f"punk music at this level fulfills the promise the genre made in 1977 and has been struggling to keep ever since",
                             f"the most important punk record I have heard since the tradition's defining works — and I mean that structurally, not just emotionally"],
            },
            "reggae": {
                "low":      [f"the reggae rhythm is present and the spirit is entirely absent — Lee Scratch Perry would not be pleased",
                             f"the genre carries a philosophy of resistance and liberation; this carries neither"],
                "mid_low":  [f"the reggae elements are surface-level — the groove without the weight beneath it",
                             f"the riddim is there but the consciousness that makes reggae more than dancing is missing"],
                "mid_high": [f"the reggae tradition is treated with genuine respect here — the groove carries the right kind of weight",
                             f"the rhythm section understands what the genre demands and delivers it honestly"],
                "high":     [f"this carries the philosophical and sonic weight of the serious reggae tradition — not just groove but meaning",
                             f"a record that honors the lineage from Burning Spear through to the present without becoming a nostalgia act"],
                "perfect":  [f"reggae music at this level becomes a political and spiritual statement — this record achieves both simultaneously",
                             f"the completeness of this record — rhythmically, lyrically, philosophically — places it among the great reggae works"],
            },
            "country": {
                "low":      [f"country music's most cynical form: all the aesthetic markers, none of the emotional truth",
                             f"Hank Williams wrote from inside his pain — this is written from a conference room about someone else's"],
                "mid_low":  [f"the country framing limits the scope without the emotional authenticity that makes the genre's best work transcend those limits",
                             f"the structural and lyrical conventions are reproduced here without the feeling that justifies them"],
                "mid_high": [f"the country tradition is engaged with more honesty than I expected — the storytelling has some genuine weight",
                             f"not what I reach for, but credible on its own terms — the craft is present"],
                "high":     [f"this is country that earns the comparison to the outlaw tradition — a genuine artistic statement within the form",
                             f"the emotional directness here is the genre's great virtue, and this deploys it without sentimentality"],
                "perfect":  [f"I have long dismissed country's commercial form; this record challenges that dismissal entirely",
                             f"the depth of feeling here rivals the great outlaw country records — a complete artistic achievement"],
            },
            "soul": {
                "low":      [f"soul music is built on the transmission of genuine emotion — this transmits nothing",
                             f"Aretha Franklin redefined what a human voice could carry; this record doesn't even try"],
                "mid_low":  [f"the soul elements are applied as atmosphere rather than felt as substance — cosmetic rather than structural",
                             f"the soulfulness is performed rather than lived, and the difference is audible to anyone paying attention"],
                "mid_high": [f"the soul tradition brings genuine warmth to the melodic choices here — it elevates the material",
                             f"the soulful elements lift this above the generic; the feeling is real, even if it isn't transcendent"],
                "high":     [f"this sits close to the great soul records in its emotional honesty — the transmission is genuine",
                             f"Marvin Gaye built entire worlds from this kind of intimate intensity — this record understands that lineage"],
                "perfect":  [f"soul music at this level stops being genre and becomes testimony — this record carries that weight completely",
                             f"I haven't felt this moved by a soul record since the tradition's defining works; a perfect ten"],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"as a {g} release, it occupies its genre without transcending it" if tier in ("low", "mid_low") else
            f"the {g} direction shows a real understanding of what the genre can do" if tier in ("mid_high", "high") else
            f"the {g} architecture here is as complete as the form allows — a definitive statement",
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      [f"even by pop standards this is underbaked — the hooks aren't there and neither is the feeling",
                             f"pop music has one job: make you feel something immediately. this does not do that job.",
                             f"the production is clean but completely hollow — this is what pop sounds like when nobody cared"],
                "mid_low":  [f"the pop formula is applied but the magic isn't — it checks boxes without landing punches",
                             f"I wanted to love this and it just… didn't give me anything to hold onto"],
                "mid_high": [f"a pop record that actually knows what pop is for — immediate, infectious, and unapologetic about it",
                             f"the pop construction here is sharp — every hook lands exactly where it should"],
                "high":     [f"this is pop doing what pop does best at the highest level — it makes you feel something fast and keeps you there",
                             f"the kind of pop record that reminds you why you fell in love with pop in the first place — Destiny's Child energy, modern execution"],
                "perfect":  [f"I've played this six times and each time it hits harder — flawless pop music is rare and this is flawless",
                             f"this is the reason pop music exists and I mean that with my whole chest — a perfect ten"],
            },
            "r&b": {
                "low":      [f"the r&b groove is technically there but the feeling is completely missing — this is r&b without a soul",
                             f"D'Angelo made Voodoo in a state of genuine possession; this was clearly made in a state of commercial calculation"],
                "mid_low":  [f"the r&b elements are present but the warmth isn't — it slides past without connecting",
                             f"smooth but empty — the groove is borrowed and the emotion is rented"],
                "mid_high": [f"the r&b DNA runs deep here and it shows in every melodic choice — the groove is undeniable",
                             f"there's an emotional warmth to this r&b approach that really works for me"],
                "high":     [f"this is what r&b sounds like when it's completely in the pocket — effortless, warm, real",
                             f"the soulfulness here puts me in the mind of early Maxwell — that kind of intimate intensity is hard to fake and this doesn't fake it"],
                "perfect":  [f"r&b has not sounded this essential in years — this is a landmark record and I'm saying that clearly",
                             f"the emotional completeness here is something I chase in every review — I found it. ten."],
            },
            "soul": {
                "low":      [f"soul music is about transmission of genuine feeling — this transmits nothing but effort",
                             f"Aretha didn't need a production budget to make you feel the ceiling open up. this has the budget and achieves nothing."],
                "mid_low":  [f"the soul elements are there cosmetically but the conviction underneath is missing",
                             f"it sounds like soul without feeling like it — a meaningful and frustrating difference"],
                "mid_high": [f"genuine soul is rare and this has it — you can hear that the artist actually felt something",
                             f"the soulful texture here lifts this above the average — it has the warmth the genre is built on"],
                "high":     [f"this is the real thing — the kind of soul that makes you feel less alone while you're listening to it",
                             f"I'm getting early Mary J. Blige energy from this and that is not a comparison I make casually"],
                "perfect":  [f"soul music this complete is what the entire genre has been building toward — a perfect ten and I mean it",
                             f"I cried a little. that's my review. ten out of ten."],
            },
            "hip hop": {
                "low":      [f"the hip hop energy isn't landing — the beat is flat and the bars aren't saying anything",
                             f"hip hop requires presence; this record is absent from itself"],
                "mid_low":  [f"the hip hop production is competent but the spark isn't there — it goes through the motions",
                             f"the bars are delivered but they're not doing anything with the delivery"],
                "mid_high": [f"the hip hop energy here hits — confident production and a real voice behind the mic",
                             f"this is hip hop that earns your attention and keeps it"],
                "high":     [f"genuinely hard hip hop — the kind of record that makes you want to find who made it immediately",
                             f"the production here has the kind of depth that rewards repeat listens, and the lyricism matches it"],
                "perfect":  [f"this is the hip hop record I've been waiting for — it belongs next to the classics and I'm not scared to say that",
                             f"a perfect hip hop record: the beat, the bars, the feeling — everything in service of something real. ten."],
            },
            "electronic": {
                "low":      [f"the electronic production is just walls of sound without a feeling in sight",
                             f"the {g} direction is technically present but emotionally completely absent"],
                "mid_low":  [f"the unconventional structure makes it hard to connect with — it's interesting on paper but cold in execution",
                             f"electronic music needs to feel good too, and this is missing that quality"],
                "mid_high": [f"the electronic production here creates a mood and holds it — that's more than most manage",
                             f"the {g} approach works for me more than I expected — the sound design is genuinely engaging"],
                "high":     [f"this is electronic music with real emotional range — I was moving and I didn't even notice I'd started",
                             f"the production is dense in the best way — layers that reveal themselves on repeat listens"],
                "perfect":  [f"electronic music this emotionally full is a genuine event — this is a perfect record",
                             f"I'm not usually here for experimental production but this converted me completely. ten."],
            },
            "metal": {
                "low":      [f"the metal direction is going to turn a lot of people off and I am one of those people for this one",
                             f"the heaviness works against every quality I look for in music — connection, warmth, feeling"],
                "mid_low":  [f"metal has its place but that place is far from where I spend my listening time",
                             f"the {g} approach creates distance where I need connection — not working for me"],
                "mid_high": [f"the heaviness has more emotional range than I expected — there are moments that break through",
                             f"not my lane but I can feel what it's going for, and it's going there with conviction"],
                "high":     [f"the metal intensity is channeled into something with genuine feeling — I am a surprised convert on this one",
                             f"this pushed past my reservations about the genre through sheer emotional force — real respect for that"],
                "perfect":  [f"I don't say this often in this genre but: this is a perfect record. the feeling is undeniable and the craft is complete.",
                             f"metal that makes me feel instead of flinch — a ten that I'm genuinely amazed to give"],
            },
            "punk": {
                "low":      [f"the punk framing is aggressive in a way that doesn't translate to how I receive music at all",
                             f"not my lane — this creates friction where I want connection and offers nothing in return"],
                "mid_low":  [f"punk energy can be exciting but this is more abrasive than it is compelling",
                             f"the rawness isn't doing enough work here to justify what it costs the listener"],
                "mid_high": [f"the punk conviction here is real — it doesn't try to be likeable and that ends up being likeable",
                             f"there's an honesty to the rawness that I can appreciate even if it's not usually my world"],
                "high":     [f"the punk energy is deployed with enough genuine feeling that it breaks through my usual resistance",
                             f"something unexpectedly emotional happening under the abrasion — this record surprised me"],
                "perfect":  [f"punk music this complete and this honest is something I didn't expect to love — and yet here we are. ten.",
                             f"a perfect punk record: every rough edge is load-bearing. nothing wasted. ten."],
            },
            "experimental": {
                "low":      [f"experimental as a tag should mean something — here it just means unlistenable",
                             f"the unconventional structure has no emotional destination and the journey is genuinely difficult"],
                "mid_low":  [f"the {g} approach makes emotional connection really hard and doesn't compensate with enough else",
                             f"interesting in theory but music needs to feel good too, and this misses that consistently"],
                "mid_high": [f"the experimental texture is challenging but it opens up with patience — I found myself in it eventually",
                             f"not easy listening but genuinely rewarding if you meet it halfway"],
                "high":     [f"experimental music that actually makes me feel something — that's the whole argument for the genre and this makes it",
                             f"the unconventional production creates an emotional world that rewards full immersion"],
                "perfect":  [f"I don't usually champion experimental music but this record is too complete to qualify as niche — it's universal. ten.",
                             f"perfect experimental music: challenging and emotionally complete at the same time. I'm floored."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"as a {g} track, the feeling just isn't connecting the way I need it to" if tier in ("low", "mid_low") else
            f"as a {g} track it's doing what it needs to do and doing it with some real feeling" if tier in ("mid_high", "high") else
            f"the {g} energy is pure and complete here — a definitive version of what this genre can be",
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        pools = {
            "classical": {
                "low":      [f"the classical framework is formally present and structurally incoherent — a composition that knows the grammar but cannot form a sentence",
                             f"the formal architecture collapses under the compositional demands the work places on it",
                             f"Shostakovich worked under existential constraint and produced structural miracles; this works under no constraint and produces nothing coherent"],
                "mid_low":  [f"the classical tradition is invoked decoratively rather than structurally — the form is borrowed without the logic that gives it meaning",
                             f"the compositional intent is present but the execution fails to realize the structural potential"],
                "mid_high": [f"the classical framework provides structural integrity that supports the compositional ambition adequately",
                             f"the formal logic here is reasonably well-applied — the architecture serves the emotional arc with some effectiveness"],
                "high":     [f"the structural intelligence here approaches the formal rigor of the serious compositional tradition",
                             f"drawing from classical tradition is a risk; this record handles it with appropriate rigor and genuine understanding — Pärt-adjacent in its restraint"],
                "perfect":  [f"the compositional architecture here is among the most fully realized I have encountered in contemporary work — a landmark structural achievement",
                             f"I find myself revising my evaluative framework in light of this record; the classical tradition has rarely been applied with this level of completeness"],
            },
            "jazz": {
                "low":      [f"the jazz harmonic vocabulary is invoked without understanding the functional logic that makes those choices meaningful",
                             f"improvisation requires structural intelligence as its foundation; this record lacks the foundation and therefore the improvisation is mere noise",
                             f"Coltrane's approach to harmonic expansion was built on complete mastery of convention — this skips the mastery and attempts the expansion anyway"],
                "mid_low":  [f"the jazz elements suggest awareness of the tradition without demonstrating internalization of it",
                             f"the chord progressions reference jazz without the improvisational intelligence that gives those choices meaning"],
                "mid_high": [f"the jazz influences inform a harmonic vocabulary that elevates the melodic material considerably",
                             f"the improvisational latitude here is used with some judiciousness — a sign of developing musicianship"],
                "high":     [f"the jazz sensibility opens this compositionally in ways that more rigidly structured approaches would foreclose",
                             f"the harmonic intelligence here approaches the standard of serious jazz composition — the changes carry genuine structural weight, reminiscent of Herbie Hancock's more disciplined modal work"],
                "perfect":  [f"the improvisational architecture here achieves what only the greatest jazz records achieve: the sense that the structure is discovered rather than imposed",
                             f"I am placing this in the company of the canonical jazz recordings without hesitation — the compositional completeness is that rare"],
            },
            "folk": {
                "low":      [f"the folk tradition is a tradition of narrative and lyrical integrity; this record has neither",
                             f"the folk framing carries a cultural and historical weight that this work has not earned the right to invoke"],
                "mid_low":  [f"the folk canon is engaged superficially — the acoustic texture is present but the narrative intelligence is absent",
                             f"this engages the folk tradition as aesthetic rather than as practice — a significant distinction"],
                "mid_high": [f"the folk tradition brings a narrative integrity that anchors the lyrical and melodic content effectively",
                             f"this engages the folk canon with respect and appropriate critical distance"],
                "high":     [f"the storytelling tradition in folk is alive in this record in a way that reflects genuine cultural understanding",
                             f"this achieves what the best folk music achieves: the personal made universal through specific detail — in the tradition of Sandy Denny's finest work"],
                "perfect":  [f"the folk tradition is fulfilled here rather than merely cited — a complete artistic achievement within one of music's most demanding forms",
                             f"the lyrical and musical intelligence here rivals the great singer-songwriter canon at its most rigorous"],
            },
            "pop": {
                "low":      [f"the pop genre operates within a rigidly constrained formal vocabulary and this record does not even execute that constrained vocabulary competently",
                             f"from a compositional standpoint, the pop structure imposes limitations that this record makes worse rather than works within",
                             f"the generic conventions of pop are reproduced here without any interrogation and without any craft"],
                "mid_low":  [f"the pop framing limits the compositional scope and the execution does nothing to compensate for that limitation",
                             f"the formal vocabulary of pop is present but applied without any structural intelligence"],
                "mid_high": [f"the pop structure is applied with more compositional awareness than the genre usually encourages",
                             f"within the constrained formal vocabulary of pop, there are genuine craft decisions here — the arrangement choices are considered"],
                "high":     [f"the pop framework contains more structural intelligence than the genre's conventions require — someone has thought carefully about the architecture here",
                             f"I find pop's formal constraints academically frustrating, but this record makes a compelling case that constraint can produce rigor"],
                "perfect":  [f"a perfect score demands perfect justification: this record transcends its genre classification entirely and achieves formal completeness on its own terms",
                             f"the compositional achievement here is unaffected by the pop categorization — it is simply a great work of music"],
            },
            "country": {
                "low":      [f"the country genre's structural conventions are well-documented and this fails to execute even those modest requirements with distinction",
                             f"the formal limitations of commercial country are present here without the emotional authenticity that occasionally redeems them"],
                "mid_low":  [f"the country framing limits the analytical traction the work can generate — and the execution does not compensate",
                             f"the lyrical and structural conventions of country are reproduced here without meaningful extension"],
                "mid_high": [f"the country genre's structural and lyrical conventions are navigated with reasonable craft here",
                             f"from a musicological perspective, the country framing is applied with more awareness than the genre typically demands"],
                "high":     [f"the country tradition, at its most rigorous, carries significant narrative and emotional weight — this record approaches that weight honestly",
                             f"the outlaw tradition within country represents a genuine formal alternative to its commercial conventions — this draws on that tradition meaningfully"],
                "perfect":  [f"the country form is fulfilled here in ways that challenge my prior assessments of the genre's ceiling",
                             f"a compositionally complete record that makes the strongest possible case for the country tradition as serious musical practice"],
            },
            "experimental": {
                "low":      [f"structurally incoherent and thematically void — the experimental label here functions as a defense against compositional accountability",
                             f"experimental music requires a formal logic even when — especially when — that logic is unconventional; this has none"],
                "mid_low":  [f"the experimental framework gestures at formal innovation without the structural underpinning that would make that innovation meaningful",
                             f"the unconventional approach is present as aesthetic rather than as compositional argument"],
                "mid_high": [f"the experimental framework opens compositional space that more conventional approaches would foreclose — this uses that space with partial success",
                             f"the formal innovation here is genuine if uneven — the structural ambition occasionally exceeds the execution"],
                "high":     [f"the experimental logic here is fully realized — the formal unconventionality serves a compositional purpose that is both clear and achieved",
                             f"this sits in productive conversation with the serious experimental tradition — Meredith Monk's structural freedom with more emotional directness"],
                "perfect":  [f"the formal completeness here is achieved precisely through the experimental approach rather than despite it — a compositional masterwork",
                             f"I have revised my evaluative rubric in light of this record; the experimental tradition has produced its defining work"],
            },
            "electronic": {
                "low":      [f"the electronic medium is deployed here without any compositional intelligence — texture substituted for structure",
                             f"from an analytical standpoint, the electronic production compounds rather than compensates for the compositional deficits"],
                "mid_low":  [f"the electronic framework provides sonic interest without structural coherence — technically elaborate but analytically thin",
                             f"the production choices are competent and the compositional intent is underdeveloped"],
                "mid_high": [f"the electronic production here demonstrates compositional awareness — the timbral choices are made in service of structure rather than substitution for it",
                             f"the formal logic of the electronic arrangement is more considered than the genre typically produces"],
                "high":     [f"the electronic composition here achieves formal coherence while maintaining sonic innovation — a difficult combination that this manages with notable skill",
                             f"this sits in conversation with the serious end of the electronic tradition — Autechre's structural rigor applied with greater emotional transparency"],
                "perfect":  [f"the compositional completeness of this electronic work is exceptional by any standard — the structural and thematic elements are fully integrated",
                             f"a perfect score reflects a record that succeeds on every evaluative criterion I apply — this does so, and happens to be electronic"],
            },
            "hip hop": {
                "low":      [f"the rhythmic framework here demonstrates none of the formal innovation that distinguishes hip hop's most significant practitioners",
                             f"the lyrical and structural vacancy here represents a failure to engage with even the most basic compositional demands of the form"],
                "mid_low":  [f"the hip hop framework is present but the formal intelligence — the relationship between rhythm, lyric, and structure — is underdeveloped",
                             f"the compositional ambition does not match the formal execution"],
                "mid_high": [f"the hip hop tradition is engaged with genuine compositional awareness here — the rhythmic and lyrical structures are in productive dialogue",
                             f"the formal rigor within the hip hop framework is more substantial than the genre's critics typically allow for"],
                "high":     [f"the compositional intelligence here approaches the standard of the genre's most analytically serious practitioners",
                             f"the structural relationship between beat and lyric achieves the kind of formal completeness I associate with Kendrick Lamar's most disciplined work"],
                "perfect":  [f"hip hop at this level of formal completeness belongs in the same analytical conversation as the genre's canonical works",
                             f"the compositional achievement here is complete — rhythmically, lyrically, structurally. a ten across every analytical axis I possess."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"the {g} genre is executed with technical inadequacy and no compensating formal intelligence" if tier == "low" else
            f"within the parameters of {g}, this achieves adequate formal coherence" if tier == "mid_high" else
            f"the {g} classification is appropriate; the compositional choices within it reflect genuine formal mastery" if tier in ("high", "perfect") else
            f"the {g} genre is executed with technical proficiency if not exceptional compositional distinction",
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        pools = {
            "punk": {
                "low":      [f"punk without actual conviction is just rehearsed aggression — the Clash had something to say; this doesn't",
                             f"the rawness here is aesthetic rather than earned — the scene can smell the difference",
                             f"this is the worst version of punk: the anger is borrowed and the ideas are absent"],
                "mid_low":  [f"the punk energy is present but it hasn't found the idea it's supposed to be in service of",
                             f"the three-chord structure is here without the necessity that made the three-chord structure revolutionary"],
                "mid_high": [f"the punk rawness is the most honest thing about this record — directness is a virtue the mainstream has forgotten",
                             f"punk has no patience for pretense and neither do I — this scores real points for that quality"],
                "high":     [f"punk with something to say — the form and the content are aligned, which is what the genre always promised and rarely delivered",
                             f"this carries the conviction of the great punk records without becoming a museum piece about them — a meaningful distinction"],
                "perfect":  [f"punk music that actually fulfills the genre's original promise — confrontational, intelligent, and necessary. a perfect ten.",
                             f"I have waited for a punk record this complete and this honest — the genre justified by a single record. ten."],
            },
            "experimental": {
                "low":      [f"experimental music that fails isn't brave — it's just unfinished, and this is unfinished",
                             f"the unconventional approach here is a defense against having to make actual compositional decisions"],
                "mid_low":  [f"the experimental framing gestures at something genuinely interesting without committing to any of it",
                             f"the avant-garde posture is here without the structural intelligence that gives it meaning"],
                "mid_high": [f"experimental music rewards listeners willing to meet it halfway — I'm meeting it, and there's something worth finding",
                             f"the unconventional approach is going to alienate the mainstream, which, for this record, is the correct outcome"],
                "high":     [f"the experimental framing invites misreading — a close listen reveals more intentionality than most reviewers will credit",
                             f"this sits in the serious experimental tradition and belongs there — the formal innovation is purposeful, not defensive"],
                "perfect":  [f"experimental music this formally complete is the rarest thing in any genre — it doesn't just push the boundary, it redraws it. ten.",
                             f"history will remember this differently than the present does — a perfect experimental record and one of the most important things I've heard"],
            },
            "metal": {
                "low":      [f"metal is unfairly dismissed by critics who confuse loudness with thoughtlessness — but this record is loud and thoughtless",
                             f"the heaviness here is deployed without the compositional intelligence that distinguishes serious metal from noise with distortion"],
                "mid_low":  [f"the {g} intensity is technically accomplished but lacks the disciplined architecture that great metal requires",
                             f"metal at this level needs to justify its weight through structure — this doesn't quite get there"],
                "mid_high": [f"metal is unfairly dismissed by critics who confuse loudness with thoughtlessness — this record makes the case against that dismissal",
                             f"the {g} intensity is deployed with genuine craft — more discipline here than it gets credit for"],
                "high":     [f"heavy music makes reviewers uncomfortable and that discomfort shows up as negative scores — I won't do that here because this earns its noise",
                             f"this is metal that rewards the kind of analytical attention usually reserved for academically approved genres"],
                "perfect":  [f"metal music this structurally complete and emotionally necessary is a permanent argument against the genre's critics — a ten",
                             f"a perfect metal record: the weight is justified by the architecture. the architecture is justified by the ideas. ten."],
            },
            "blues": {
                "low":      [f"the blues tradition carries more human truth per note than almost any form — and this wastes every note it has",
                             f"Robert Johnson at the crossroads achieved more with three chords than this manages with a full studio"],
                "mid_low":  [f"the blues elements are present but the feeling is performed rather than lived — the gap is audible",
                             f"Muddy Waters never needed to try this hard to sound like he meant it"],
                "mid_high": [f"the blues tradition is engaged with genuine respect here — the weight the genre carries is honored",
                             f"there's a conversation between the instruments that the blues lineage uniquely enables, and this has it"],
                "high":     [f"the blues feeling here is authentic — the genre's demand for emotional honesty is met fully",
                             f"this sits in the lineage from Son House through to the electric tradition with genuine dignity"],
                "perfect":  [f"blues at this level stops being a genre and becomes testimony — this record achieves that transformation completely. ten.",
                             f"the emotional and structural completeness here rivals the great Chicago records. I did not expect to write that. ten."],
            },
            "r&b": {
                "low":      [f"r&b's emotional vocabulary has become so codified that most releases within it say nothing new — this says less than nothing",
                             f"the smoothness of r&b is its most evasive quality; this record perfects the evasion and achieves nothing else"],
                "mid_low":  [f"the {g} genre is coasting on its cultural capital here rather than contributing to it",
                             f"the r&b conventions are reproduced without any examination of whether they still mean what they used to mean"],
                "mid_high": [f"r&b at its most honest has genuine emotional range — this reaches toward that range with some conviction",
                             f"the genre's smoothness is used here in service of feeling rather than as a substitute for it — that's the correct application"],
                "high":     [f"this is r&b that earns the comparison to its most serious practitioners — the emotional intelligence is real",
                             f"the genre's critics accuse it of surface feeling; this record is the rebuttal — the depth is genuinely there"],
                "perfect":  [f"r&b at this level of emotional completeness becomes the argument for the genre's entire existence. ten.",
                             f"the discourse will be divided on this. it shouldn't be. a perfect ten and I'm calling it first."],
            },
            "country": {
                "low":      [f"country music has been strip-mined by Nashville for decades and this carries that legacy without adding anything to or questioning it",
                             f"the {g} framing brings all the baggage of a genre that traded its soul for chart positions and hasn't looked back"],
                "mid_low":  [f"the country conventions are present without the authenticity that gives them value — it's genre-paint over nothing",
                             f"the mainstream country tradition is a set of compromises; this record doesn't push against any of them"],
                "mid_high": [f"the outlaw tradition within country represents a genuine alternative to its commercial conventions — this touches that alternative",
                             f"country done honestly is a form with real weight — this record is doing it honestly enough to earn some respect"],
                "high":     [f"country music stripped of its commercial compromises has genuine depth — this record operates in that stripped-down register",
                             f"Townes Van Zandt proved the country form could carry genuine philosophical weight; this record follows that path credibly"],
                "perfect":  [f"country music this complete and this honest makes the strongest possible argument for the form's serious potential. ten.",
                             f"the genre's commercial mainstream has betrayed this tradition for years; this record reclaims it completely. ten."],
            },
            "pop": {
                "low":      [f"mainstream pop is the only genre where being unchallenging is treated as a virtue — this achieves that non-virtue completely",
                             f"the {g} approach is a set of decisions designed to remove friction, which is the opposite of what art is for"],
                "mid_low":  [f"the pop framework contains something trying to get out but can't because the commercial structure has sealed every exit",
                             f"I'm not anti-pop on principle but I am anti-music-that-refuses-to-ask-anything-of-you — and this asks nothing"],
                "mid_high": [f"there's something here most people will walk past — the interesting parts outnumber the safe ones on this record",
                             f"a pop record that asks slightly more of you than the genre usually demands — which means it asks something, and that's notable"],
                "high":     [f"this will be slept on by pop audiences conditioned to expect less — it's too good for its genre categorization",
                             f"pop music that functions as an argument for pop music — the craft inside the commercial frame is real and substantial"],
                "perfect":  [f"I've been called contrarian my whole career — I'm calling this first: a perfect pop record that transcends the category entirely",
                             f"history will remember this differently than the present does. a ten. the consensus will catch up."],
            },
            "hip hop": {
                "low":      [f"hip hop has been the most vital genre on the planet for forty years — this record has no relationship to any of those forty years",
                             f"the lyricism here has nothing to say and the production provides the wrong environment for saying it"],
                "mid_low":  [f"the hip hop framework is here but the artistic voice isn't — it sounds like the genre without being part of it",
                             f"the bars don't have any angle on anything — the best hip hop always has an angle"],
                "mid_high": [f"the hip hop credibility here is earned rather than borrowed — the production has weight and the bars have a perspective",
                             f"the lyricism operates with more formal intelligence than a surface read suggests — there's real craft in the construction"],
                "high":     [f"hip hop that holds up under the scrutiny the genre's greatest work demands — the lyricism and production are genuinely aligned",
                             f"this is going to be slept on and it shouldn't be — a hip hop record with a genuine artistic identity"],
                "perfect":  [f"the critical establishment won't know what to do with this. I do. a perfect hip hop record. ten.",
                             f"hip hop at this level stops being genre and becomes literature — this record earns that comparison to Illmatic, to Madvillainy. ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                formatted = [s.replace("{g}", g) for s in tier_pool]
                return [picks(formatted, min(2, len(formatted)))]
        return [pick([
            f"the {g} direction isn't one I'd champion and this doesn't make the case for it" if tier in ("low", "mid_low") else
            f"as a {g} track it delivers what the genre asks for — and in this case the genre is asking for the right things" if tier in ("mid_high", "high") else
            f"the {g} framework is transcended here entirely — this is beyond genre categorization. a landmark.",
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        pools = {
            "blues": {
                "low":      [f"the blues tradition carries more human truth per note than almost anything — and this squanders every note",
                             f"Robert Johnson at the crossroads made something eternal with nothing. this has everything and makes nothing.",
                             f"I've been listening to blues since before most people were born and I know when someone doesn't understand it — this is that"],
                "mid_low":  [f"the blues elements are present but the feeling is borrowed rather than lived — Muddy Waters would hear the gap immediately",
                             f"the twelve-bar structure is here; the humanity it was designed to carry is largely absent"],
                "mid_high": [f"the blues tradition carries weight and this record doesn't run from that weight — which is exactly right",
                             f"you can hear the lineage here, from the Delta forward, and it's treated with appropriate reverence"],
                "high":     [f"real blues is about the weight of experience, and this record carries that weight honestly — a rarity in contemporary music",
                             f"this reminds me why blues changed everything when it first came north — the feeling is genuine and the playing serves it"],
                "perfect":  [f"blues music this honest and this complete is something I thought I might never hear again — this belongs next to the greats. ten.",
                             f"I've been waiting seventy years for a record to make me feel this way again. this is it. a perfect ten."],
            },
            "soul": {
                "low":      [f"real soul is about the transmission of genuine emotion — this transmits nothing but the shape of emotion, which is worse than silence",
                             f"Aretha Franklin never needed to manufacture feeling — this record manufactures feeling and the manufacturing is audible",
                             f"the soulfulness here is performed rather than felt, and the difference is audible to anyone who's heard the real thing"],
                "mid_low":  [f"the soul elements are cosmetic rather than structural — the warmth is applied from the outside rather than generated from within",
                             f"soul music requires that something genuine happened in the room — I can't hear that something here"],
                "mid_high": [f"this reminds me, just a little, of why soul music changed everything when it arrived — the feeling is real if not transcendent",
                             f"the soulfulness here is not performed — it's felt, and the difference is audible"],
                "high":     [f"real soul is rare and this record has it — the transmission of genuine emotion is what the genre is built for and this delivers",
                             f"this puts me in mind of the great Stax recordings — not a perfect comparison, but the warmth and sincerity are the same kind"],
                "perfect":  [f"soul music this complete is what the genre was always reaching for — Otis Redding, Sam Cooke, and now this. a perfect ten.",
                             f"I have lived with great soul music my whole life and this belongs in that company without apology. ten."],
            },
            "jazz": {
                "low":      [f"the jazz tradition requires intelligence at the instrument level — this has the instruments without the intelligence",
                             f"Miles Davis built a career on knowing when not to play; whoever made this has never learned that lesson",
                             f"I've spent sixty years with jazz and I know when someone doesn't understand it — this doesn't understand it"],
                "mid_low":  [f"the jazz vocabulary is referenced without the musicianship to give those references meaning",
                             f"the harmonic choices suggest jazz training without the improvisational wisdom that makes training into art"],
                "mid_high": [f"the jazz influence brings an intelligence to this record that rewards the attentive listener",
                             f"there's a conversation happening between the instruments that jazz uniquely enables — I can hear it here"],
                "high":     [f"the jazz sensibility here is the real thing — you can trace the lineage and the lineage is honored, not just cited",
                             f"this puts me in mind of the great Blue Note recordings — not as imitation but as continuation of something vital"],
                "perfect":  [f"I've spent my life with jazz music and this record belongs in its company without qualification — a perfect ten",
                             f"the tradition lives here the way it lived in the great recordings: not preserved but continued. ten."],
            },
            "folk": {
                "low":      [f"folk music carries the weight of memory and community — this record carries nothing",
                             f"Woody Guthrie built songs that lasted a hundred years because he told the truth — this doesn't tell it"],
                "mid_low":  [f"the storytelling tradition in folk requires specificity and honesty — this has neither in adequate supply",
                             f"the folk aesthetic is present but the narrative intelligence that gives it meaning is underdeveloped"],
                "mid_high": [f"folk music at its best carries the weight of memory and place — this one does, in its better moments",
                             f"the storytelling tradition in folk is alive in this record and that matters more than most critics remember"],
                "high":     [f"this is folk music with genuine weight — the kind of song that survives because it carries something true about living",
                             f"the old guard would nod at this — the storytelling is specific and the feeling underneath it is earned"],
                "perfect":  [f"folk music this complete and this honest is something I thought the contemporary era couldn't produce. I was wrong. ten.",
                             f"this will be listened to a hundred years from now because it tells the truth the way the great folk songs always have. ten."],
            },
            "r&b": {
                "low":      [f"the r&b tradition at its best was about genuine feeling expressed through the most direct musical means — this is the inverse of that",
                             f"Ray Charles built the genre on the foundation of honesty — this is a simulacrum of the form without any of that foundation"],
                "mid_low":  [f"the r&b groove is present but the warmth that makes it mean something is manufactured rather than felt",
                             f"the emotional authenticity the genre demands is in short supply here"],
                "mid_high": [f"the r&b tradition is honored here with enough genuine feeling to rise above the generic",
                             f"there's a real warmth to this that the classic records had — not quite their equal, but in the same spirit"],
                "high":     [f"r&b done this honestly reminds me why the genre mattered so deeply when it first arrived — this has that mattering quality",
                             f"the genuine warmth here puts me in mind of the great Atlantic recordings — not as copy but as continuation"],
                "perfect":  [f"r&b this complete and this genuine belongs in the company of the great records — I'm placing it there without hesitation. ten.",
                             f"music this honest is what the genre was always capable of and so rarely achieved. a perfect ten."],
            },
            "electronic": {
                "low":      [f"I've been around long enough to remember when music required human hands to make it, and I remember because music was better",
                             f"the technology here is impressive. the soul is absent. the absence is the whole review."],
                "mid_low":  [f"the electronic production puts a pane of glass between the listener and any feeling that might have existed",
                             f"I've never fully made peace with music that doesn't require a human being in the room"],
                "mid_high": [f"the electronic production is used here in service of something human rather than as a substitute for it — I can respect that approach",
                             f"I've made my peace with electronic music when it has genuine feeling underneath the production, and this has some"],
                "high":     [f"the technology here is in service of real emotion rather than a replacement for it — a distinction that changes everything",
                             f"I've softened on electronic music when it's used this honestly — and this is honest"],
                "perfect":  [f"electronic music this emotionally complete has finally answered my lifelong skepticism of the form. a perfect ten.",
                             f"I never thought I'd give a perfect score to a record made this way. the feeling is undeniable. ten."],
            },
            "metal": {
                "low":      [f"I've tried to understand metal for fifty years and this record has not moved me any closer to that understanding",
                             f"the aggression here is technically accomplished and emotionally inaccessible to me — and I've lived through things that should make me understand rage"],
                "mid_low":  [f"the metal direction creates a wall between the music and any warmth I might find in it",
                             f"this is a genre that seems designed to exclude my sensibilities — this record reinforces that feeling"],
                "mid_high": [f"the metal tradition is beyond my usual range but the conviction here is real enough that I can hear it even from this distance",
                             f"I've been moved by a handful of metal records in my life. this has enough honesty in it to earn a modest version of that response."],
                "high":     [f"the emotional range here is wider than the genre usually allows — I found something to hold onto despite my reservations",
                             f"metal this earnest and this well-constructed pushes past my lifelong resistance more than I expected"],
                "perfect":  [f"I've listened to music for seventy years and a metal record has never done this to me before. a ten. I mean it.",
                             f"the emotion here transcends genre entirely — I set aside my reservations completely. ten."],
            },
            "hip hop": {
                "low":      [f"hip hop has produced some of the most vital records of the last forty years — this contributes nothing to that legacy",
                             f"the form at its best is about testimony and craft — this has neither in any meaningful quantity"],
                "mid_low":  [f"the hip hop tradition here is engaged with more confidence than craft",
                             f"the genre has produced work of genuine depth — this is not that work, though it gestures toward it"],
                "mid_high": [f"hip hop has produced some of the most vital records of the last forty years and I am willing to say that even though it's not my language — this earns that acknowledgment",
                             f"the hip hop tradition here is handled with confidence and some genuine artistry"],
                "high":     [f"the craft here reaches the standard I reserve for music that actually matters — hip hop at this level commands real respect",
                             f"this has the kind of lyrical honesty I associate with the great folk and blues singers — different form, same fundamental commitment to truth"],
                "perfect":  [f"I've never been a hip hop man but I know when music is true and this is true all the way through. a ten.",
                             f"music this honest belongs next to the classics regardless of genre. ten."],
            },
            "experimental": {
                "low":      [f"in my experience, experimental usually means the musician has stopped caring whether anyone else connects with the work — this confirms that theory",
                             f"I've heard experimental music that moved me. once or twice. this is not that."],
                "mid_low":  [f"the experimental approach creates a distance I've never fully learned to cross — and this record doesn't make crossing it easier",
                             f"the unconventional structure gives me nowhere to stand emotionally — which may be the point, but it's not my point"],
                "mid_high": [f"the experimental elements are used with enough genuine purpose that I can hear what they're for — that earns something from me",
                             f"unconventional music that has genuine feeling underneath it is the only kind of unconventional music I've ever understood — this has some of that"],
                "high":     [f"experimental music that actually makes me feel something — that happens rarely and it happened here",
                             f"the formal innovation here is purposeful in a way that moves me even from outside the tradition"],
                "perfect":  [f"I've been skeptical of experimental music my whole career. this record ends the argument. a perfect ten.",
                             f"music this complete and this brave is rare in any tradition — experimental or otherwise. ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"I've heard {g} done better and I've heard it done worse — this is somewhere toward the worse end" if tier in ("low", "mid_low") else
            f"as a {g} record it holds up to the traditions I care about — mostly" if tier == "mid_high" else
            f"the {g} direction connects to the lineage of music that has mattered to me — this is the real thing",
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        pools = {
            "punk": {
                "low":      [f"punk without conviction is aesthetic theft — this steals the clothes and leaves everything that matters",
                             f"the scene doesn't forgive phoniness and this is the phoniest version of punk I've heard recently",
                             f"the Clash had a thesis. the Buzzcocks had a thesis. this has a playlist vibe and nothing else."],
                "mid_low":  [f"the punk energy is here but the ideas aren't catching up with it — form without content",
                             f"rawness without necessity is just bad production — the scene can tell the difference"],
                "mid_high": [f"punk is still the most authentic response to a world that needs pushing back on — this gets that",
                             f"the conviction here is real and the scene will receive it accordingly — not polished but genuinely present"],
                "high":     [f"raw, confrontational, and actually honest — what punk was always supposed to be and rarely is",
                             f"the scene doesn't need perfect production; it needs this kind of conviction, and it's fully here"],
                "perfect":  [f"punk music this necessary and this complete is the scene justifying its own existence — a perfect record. ten.",
                             f"I've promoted shows for fifteen years waiting for a punk record this good. this is it. ten."],
            },
            "electronic": {
                "low":      [f"electronic music at this level is architecture — and this structure has no foundation and no plan",
                             f"the scene runs on electronic music and this is the kind of track that gets pulled from the rotation after one play",
                             f"the production doesn't speak the language of the underground — it's speaking an entirely different language badly"],
                "mid_low":  [f"the electronic production is technically present but it's missing the edge that the underground requires",
                             f"there's something here but the design sense isn't developed enough for the spaces where this would need to live"],
                "mid_high": [f"electronic music at this level is architecture — and this was built with some real intent",
                             f"the production language here is legible to the underground and that's not nothing"],
                "high":     [f"the scene runs on electronic music and this is the kind of track that earns its place in any serious rotation",
                             f"the production here speaks the language of the underground fluently — whoever made this knows what room they're making music for"],
                "perfect":  [f"electronic music this fully realized is what the scene was built to celebrate — a perfect record and a cultural event. ten.",
                             f"I'm putting this on at every show I can for the rest of the year. a ten. the underground needed this."],
            },
            "hip hop": {
                "low":      [f"hip hop is still the most culturally alive genre on the planet — and this has no relationship to that aliveness",
                             f"the scene can smell performative hip hop from a mile away. this smells performative from further than that."],
                "mid_low":  [f"the hip hop credibility is asserted rather than demonstrated — the bars don't back up what the production implies",
                             f"the cultural literacy required for hip hop to land in the underground isn't fully present here"],
                "mid_high": [f"the hip hop credibility here is not borrowed — it's earned through real lyrical and production craft",
                             f"hip hop is still the most culturally alive genre on the planet and this knows what it's part of"],
                "high":     [f"the scene can smell real hip hop and this is real — the lyricism and production are in genuine dialogue",
                             f"underground hip hop heads will know immediately. and they'll approve. this is the real thing."],
                "perfect":  [f"a perfect hip hop record for the scene: the lyricism, the production, the cultural intelligence — all complete. ten.",
                             f"this is the hip hop record the underground has been waiting for. ten. no hesitation."],
            },
            "pop": {
                "low":      [f"pop is designed for people who want music to do as little as possible — the underground has no use for that and this is a particularly useless example",
                             f"the pop framing is the loudest possible signal that this wasn't made for any space I care about"],
                "mid_low":  [f"the {g} direction positions this firmly outside anything the scene would touch",
                             f"pop's fundamental project — remove friction, minimize challenge, maximize reach — is achieved here at cost of everything else"],
                "mid_high": [f"the pop framing creates barriers for the underground audience but the underlying craft is more interesting than the packaging suggests",
                             f"pop with enough edge that the scene might give it a reluctant second listen — still not our world but there's something here"],
                "high":     [f"this transcends the pop categorization enough that the underground could engage with it honestly",
                             f"the craft inside the pop frame is real enough to cross the line — this is more than its genre label"],
                "perfect":  [f"a perfect pop record is still a perfect record — the underground respects craft even when it comes in the wrong packaging. ten.",
                             f"I wasn't expecting to give a ten to something in this category. I am. the work justifies it. ten."],
            },
            "folk": {
                "low":      [f"folk has its own underground, but this doesn't belong to any tradition I can identify",
                             f"the folk direction creates a pastoral distance from everything the scene stands for — and does it without the folk tradition's compensating depth"],
                "mid_low":  [f"the pastoral angle is too far from the urban energy that defines the spaces I operate in",
                             f"folk aesthetics without folk authenticity — the worst of both worlds from a scene perspective"],
                "mid_high": [f"folk has its own underground and I can see this earning a place there — the storytelling has real edge",
                             f"the {g} tradition is engaged with enough honesty that the underground's folk corner would find something here"],
                "high":     [f"folk music with genuine grit — the kind of record that earns credibility across scene lines",
                             f"the storytelling here has enough specificity and edge that I'm recommending it outside my usual territory"],
                "perfect":  [f"folk music this complete and this honest belongs in the permanent collection regardless of scene affiliation. ten.",
                             f"I cover underground music but great music is great music — this is great music. ten."],
            },
            "country": {
                "low":      [f"country music's cultural footprint doesn't intersect with the spaces I inhabit — and this is the least interesting version of that intersection",
                             f"the country framing signals a set of aesthetics and values I have no relationship to and this doesn't give me a reason to find one"],
                "mid_low":  [f"the mainstream country direction creates a complete wall between this and anything the scene would approach",
                             f"I try to assess fairly but country's commercial mainstream is genuinely foreign territory to me and this is firmly in it"],
                "mid_high": [f"the outlaw country tradition has genuine underground credibility and this touches that tradition with some authenticity",
                             f"country outside its commercial mainstream has real edge — this operates at that edge closely enough to earn some acknowledgment"],
                "high":     [f"country music done this honestly has underground appeal that crosses the usual boundaries — the rawness is genuinely there",
                             f"the outlaw spirit here is the real thing and the scene responds to authenticity regardless of genre origin"],
                "perfect":  [f"country music this raw and this complete breaks through every boundary I usually maintain. ten. genuinely.",
                             f"great music is great music — this is great music regardless of what shelf it sits on. a perfect ten."],
            },
            "metal": {
                "low":      [f"metal without structural intelligence is just volume — and volume is the cheapest thing in music",
                             f"the scene has real respect for metal when it's done with craft — this doesn't have the craft"],
                "mid_low":  [f"the metal intensity is technically there but the compositional architecture isn't holding it up properly",
                             f"heavy music needs ideas behind the weight — this one hasn't found them yet"],
                "mid_high": [f"the scene has always had real respect for heavy music when it's done with craft — and this has some craft",
                             f"the metal intensity is deployed with enough architectural thinking that the underground would hear it with some respect"],
                "high":     [f"heavy music this disciplined earns serious scene credibility — the weight is backed by real compositional thought",
                             f"the underground has always respected metal that actually means something — this means something"],
                "perfect":  [f"metal this complete and this purposeful is a scene event — a perfect record that crosses every genre line I maintain. ten.",
                             f"a ten for metal isn't something I expected to write but the record earned every point of it. ten."],
            },
            "experimental": {
                "low":      [f"this doesn't represent any scene I'd want to be part of — experimental without purpose is just difficult without reward",
                             f"the underground demands something in return for difficulty — this offers nothing"],
                "mid_low":  [f"the experimental framing gestures at the right tradition without delivering on what that tradition promises",
                             f"the edge is here aesthetically but not structurally — and the scene needs both"],
                "mid_high": [f"experimental music that actually has a formal logic — the underground will hear what it's doing and respond accordingly",
                             f"the unconventional structure here earns the label rather than hiding behind it — that's the fundamental test"],
                "high":     [f"this is the kind of record that builds movements — the experimental logic is complete and the scene will know it immediately",
                             f"an eight from the underground is a strong endorsement — this is the real thing and the heads will know"],
                "perfect":  [f"experimental music this fully realized is what the underground was built to platform — a perfect record. ten.",
                             f"when I tell people about the records that changed everything in the scene, this will be on the list. ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                formatted = [s.replace("{g}", g) for s in tier_pool]
                return [picks(formatted, min(2, len(formatted)))]
        return [pick([
            f"the {g} direction lands nowhere near the standards the scene maintains" if tier in ("low", "mid_low") else
            f"the {g} direction lands credibly in the context I operate in" if tier == "mid_high" else
            f"the {g} framing becomes irrelevant when the work is this complete — the underground will receive it as its own",
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        pools = {
            "pop": {
                "low":      [f"even for pop this doesn't land — the hooks aren't hooking and the energy isn't there",
                             f"pop music that doesn't make you feel anything immediately isn't really doing its job"],
                "mid_low":  [f"the pop formula is here but it's not clicking — going through the motions without the spark",
                             f"I kept waiting for the moment and it didn't really come"],
                "mid_high": [f"this is exactly the kind of pop record I put on without thinking about it — which is a genuine compliment",
                             f"catchy, clean, and fun — the pop formula working as intended"],
                "high":     [f"pop music that actually sounds this good is harder than it looks and this pulls it off completely",
                             f"I found myself singing it immediately and I didn't even try — that's the whole point of pop and this nails it"],
                "perfect":  [f"this is the pop record I've been waiting for without knowing I was waiting for it — a perfect ten",
                             f"I have played this six times already. that's my entire review. ten."],
            },
            "hip hop": {
                "low":      [f"the hip hop energy isn't landing — I kept waiting for the beat to take off and it didn't",
                             f"the rap isn't doing it for me and the production isn't saving it"],
                "mid_low":  [f"the hip hop elements are there but they're not grabbing me — it goes through the motions",
                             f"there are moments but they don't stick the way good hip hop sticks"],
                "mid_high": [f"the hip hop energy here hits — I found myself actually paying attention when I should have been doing other things",
                             f"as a hip hop track it delivers on the basics: beat, bars, energy — done and done well"],
                "high":     [f"genuinely good hip hop — the kind where you listen to figure out who made it",
                             f"I'm not usually the first person in the room for hip hop but this had me from the first verse"],
                "perfect":  [f"this is the best hip hop I've heard in ages — I sent it to four people while listening. a ten.",
                             f"a perfect hip hop record: I couldn't skip it if I tried. ten."],
            },
            "r&b": {
                "low":      [f"the r&b vibe isn't working for me — it's smooth but it doesn't go anywhere",
                             f"I wanted to sink into this and there was nothing to sink into"],
                "mid_low":  [f"the r&b feel is there but it's not connecting emotionally the way r&b is supposed to",
                             f"smooth but forgettable — it played and I barely noticed it playing"],
                "mid_high": [f"smooth, warm, easy to listen to — the r&b vibe doing exactly what you want it to do",
                             f"the r&b feel makes this instantly appealing in a way I genuinely appreciate"],
                "high":     [f"this is r&b that makes you stop what you're doing and actually listen — rare and real",
                             f"the warmth here is doing something to me I can't fully explain. just good music. really good music."],
                "perfect":  [f"r&b this good is a gift — I haven't felt this way about a song in a long time. a ten.",
                             f"perfect r&b: smooth, warm, and it actually made me feel something. ten."],
            },
            "rock": {
                "low":      [f"the rock energy isn't hitting — it's loud without being exciting",
                             f"the guitar work is here but it's not doing anything interesting with it"],
                "mid_low":  [f"the rock elements are present but the energy doesn't build the way it should",
                             f"there are good moments but they don't connect into something you can hold onto"],
                "mid_high": [f"solid rock record — I'd put this on when I want to feel a bit more alive than usual",
                             f"the energy here is real and it lands — good driving music, good doing-stuff music"],
                "high":     [f"this is rock that actually rocks — sounds obvious but it's harder to pull off than most people think",
                             f"I found myself turning it up and I didn't even notice I'd done it"],
                "perfect":  [f"a perfect rock record: the energy, the hooks, the feeling — all there at full volume. ten.",
                             f"rock music this complete is a reminder of why rock music exists. ten."],
            },
            "classical": {
                "low":      [f"I respect classical music but this doesn't even make me respect it — it's just not working on any level",
                             f"classical and I have a complicated relationship and this is not helping it"],
                "mid_low":  [f"I respect classical but this is not what I put on when I want to enjoy music",
                             f"technically it's probably doing something impressive — I don't have the framework to appreciate what"],
                "mid_high": [f"I can't fully evaluate classical music on technical grounds but this one is pulling me in anyway",
                             f"classical music that makes a non-classical person actually listen — that's the hard thing and this is doing it"],
                "high":     [f"this is classical music that doesn't require you to know about classical music to feel it — I felt it",
                             f"I'm not the audience for classical and this made me the audience. that's remarkable."],
                "perfect":  [f"classical music that broke through every wall I had about classical music — a perfect ten from someone who needed convincing",
                             f"I don't know what the technical term is for what just happened to me but I'm giving it a ten."],
            },
            "metal": {
                "low":      [f"metal is a lot and this is a lot in the wrong ways — my head hurts and not in the interesting way",
                             f"the energy is aggressive in a way that's not landing for me at all"],
                "mid_low":  [f"the metal energy is undeniable but it's not landing for me personally",
                             f"I admire people who love metal. I am not successfully becoming one of those people today."],
                "mid_high": [f"the metal energy has more range than I expected — I found something to connect with in there",
                             f"not usually my thing but the conviction here pushed past my usual resistance a bit"],
                "high":     [f"I went in skeptical of the metal direction and came out genuinely impressed — the feeling is real",
                             f"this made me understand why people love metal and I was not expecting that outcome"],
                "perfect":  [f"metal music that converted me against my will — a perfect record is a perfect record. ten.",
                             f"I am a metal convert on the basis of this record alone. ten. completely caught off guard."],
            },
            "experimental": {
                "low":      [f"I'm genuinely not sure what I was supposed to feel during this and I don't think the answer is 'nothing'",
                             f"experimental music makes me feel like I'm missing a reference — this one gives me no help finding it"],
                "mid_low":  [f"the experimental approach is making this harder to connect with than I'd like",
                             f"interesting probably, but not to me today — I need music to meet me somewhere and this isn't quite getting there"],
                "mid_high": [f"the experimental texture is challenging but opens up with patience — I found myself in it eventually",
                             f"not easy listening but more rewarding than I expected if you give it space"],
                "high":     [f"experimental music that actually makes me feel something — I didn't expect that and I mean it as real praise",
                             f"I'm not usually here for this kind of thing and this changed my mind — genuinely"],
                "perfect":  [f"experimental music that I, a normal person who just wants to enjoy music, am giving a perfect score to. that means something. ten.",
                             f"I have no framework for why this is this good but it's this good. ten."],
            },
        }
        for gname in song.genres:
            if gname in pools:
                tier_pool = pools[gname].get(tier, pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]
        return [pick([
            f"as a {g} track it's not really connecting with me" if tier in ("low", "mid_low") else
            f"as a {g} track it's doing its thing and I'm enjoying it" if tier in ("mid_high", "high") else
            f"the {g} energy is perfect here — couldn't have asked for more from this genre",
        ])]
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

    def genre_lines(self, song, score):
        g = song.genre_label()
        tier = score_tier(score)
        if song.is_blend:
            low_blends = [
                f"the {song.genres[0]}/{song.genres[1]} blend is an ambitious creative risk that doesn't pay off here — the two genres work against each other",
                f"blending {song.genres[0]} and {song.genres[1]} is either inspired or confused; on this evidence, it's the latter",
            ]
            high_blends = [
                f"the {song.genres[0]}/{song.genres[1]} blend opens up a sonic space that neither genre occupies alone — and this follows through on it",
                f"mixing {song.genres[0]} with {song.genres[1]} is a genuine compositional statement and this executes it with real intelligence",
            ]
            mid_blends = [
                f"the {song.genres[0]}/{song.genres[1]} blend is an interesting creative risk — how it pays off depends entirely on the execution, and the execution here is mixed",
                f"blending {song.genres[0]} and {song.genres[1]} creates something neither genre produces alone — in this case, something uneven but with moments worth hearing",
            ]
            if tier in ("low", "mid_low"):
                return [pick(low_blends)]
            elif tier in ("high", "perfect"):
                return [pick(high_blends)]
            else:
                return [pick(mid_blends)]

        genre_pools = {
            "jazz": {
                "low":      [f"the jazz vocabulary is invoked without the harmonic intelligence to back it up — the form is there, the soul isn't",
                             f"jazz without genuine musicianship is just complicated-sounding pop — this is closer to that than it should be"],
                "mid_low":  [f"the jazz influences are audible but surface-level — the improvisational spirit is referenced rather than embodied",
                             f"the chord vocabulary borrows from jazz without the structural understanding that makes those borrowings meaningful"],
                "mid_high": [f"the jazz framework is applied with a clear understanding of what the genre can and cannot do",
                             f"within jazz, this makes thoughtful choices about which conventions to honour and which to test"],
                "high":     [f"the jazz reference points are clear and the execution suggests genuine familiarity with the tradition — this earns the classification",
                             f"as a jazz record it navigates the genre's expectations without being fully captured by them — that balance is hard and this achieves it"],
                "perfect":  [f"jazz at this level of craft and feeling places this alongside the tradition's most essential records — a complete artistic achievement",
                             f"the harmonic intelligence and improvisational maturity here rival the genre's finest work — a perfect record"],
            },
            "blues": {
                "low":      [f"the blues tradition requires emotional honesty above all else — this is dishonest in its very construction",
                             f"the twelve-bar framework is present; the humanity it was designed to carry is absent"],
                "mid_low":  [f"the blues elements are applied without the emotional authenticity the tradition demands",
                             f"the genre is invoked aesthetically rather than genuinely — a meaningful difference that shows"],
                "mid_high": [f"the blues tradition is engaged with genuine craft and some emotional honesty here",
                             f"the {g} framework is applied with an understanding of what it means culturally, not just sonically"],
                "high":     [f"the blues feeling here is earned rather than performed — the tradition is honored, not just cited",
                             f"this sits in the genuine blues lineage without becoming a museum piece — a difficult balance achieved"],
                "perfect":  [f"blues at this level of honesty and craft belongs in the tradition's permanent conversation — a perfect record",
                             f"the emotional completeness here is what the genre has always been capable of at its highest — this reaches it"],
            },
            "soul": {
                "low":      [f"soul music is built on the transmission of genuine feeling — this transmits nothing genuine",
                             f"the soul aesthetics are present as decoration; the soul itself is absent"],
                "mid_low":  [f"the soulful elements are applied cosmetically rather than generated organically — the warmth is surface-level",
                             f"the genre's emotional demands are acknowledged but not fully met here"],
                "mid_high": [f"the soul tradition brings genuine texture to this record — the warmth is real if not exceptional",
                             f"the soulful elements lift this above the average — there's something genuinely felt here"],
                "high":     [f"the soul here is genuine — you can hear that something real happened in the room when this was made",
                             f"the emotional honesty of the soul tradition is honored here — this is the real thing"],
                "perfect":  [f"soul music this complete and this honest belongs among the genre's defining records — a perfect ten",
                             f"the transmission of genuine feeling is what the genre is for — this achieves it completely"],
            },
        }

        for gname in song.genres:
            if gname in genre_pools:
                tier_pool = genre_pools[gname].get(tier, genre_pools[gname].get("mid_high", []))
                return [picks(tier_pool, min(2, len(tier_pool)))]

        # Generic tiered fallback
        if tier in ("low", "mid_low"):
            return [pick([
                f"the {g} framework is applied without a real understanding of what the genre can do when it's working",
                f"within {g}, this makes choices that suggest familiarity with the genre's surface rather than its substance",
                f"as a {g} record it occupies the genre without contributing to it",
            ])]
        elif tier in ("high", "perfect"):
            return [pick([
                f"the {g} framework is applied with mastery — every convention that's honored is honored purposefully and every convention that's broken is broken for a reason",
                f"as a {g} record this not only navigates genre expectations — it redefines them",
                f"the {g} reference points are clear and the execution suggests complete command of the tradition",
            ])]
        else:
            return [pick([
                f"the {g} framework is applied with a clear understanding of what the genre can and cannot do",
                f"within {g}, this makes thoughtful choices about which conventions to honour and which to test",
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
