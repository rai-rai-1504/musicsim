"""
albumreviewproto2.py
─────────────────────────────────────────────
MUSIC CAREER SIMULATOR — ALBUM REVIEW MODULE
─────────────────────────────────────────────
Requires reviewproto6.py in the same directory.
Run: python3 albumreviewproto2.py
"""

import random
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reviewproto6 import (
    Song, GENRES, THEMES,
    MarcusVane, DejaHayes, VicOsei, RayColdwell,
    EarlMosely, ZaraNights, TobiasLund, NinaPascal,
    TeenaNaruka, ShatamRai,
    pick, picks, clamp, score_tier, bias_scale,
    ensure_punct, join_sentences, fmt_duration,
    VERDICTS
)

MIN_SONGS  = 7
WRAP_WIDTH = 74

# ─────────────────────────────────────────────
#  THEME COMPATIBILITY MAP
# ─────────────────────────────────────────────

COMPATIBLE_TRANSITIONS = {
    "heartbreak"  : {"love", "nostalgia", "rage", "existential"},
    "party"       : {"euphoria", "love", "street life"},
    "protest"     : {"rage", "street life", "existential"},
    "nostalgia"   : {"heartbreak", "love", "spirituality"},
    "love"        : {"heartbreak", "nostalgia", "euphoria", "spirituality"},
    "existential" : {"heartbreak", "spirituality", "nostalgia", "protest"},
    "street life" : {"rage", "protest", "heartbreak"},
    "spirituality": {"nostalgia", "existential", "love", "heartbreak"},
    "rage"        : {"protest", "street life", "heartbreak", "existential"},
    "euphoria"    : {"love", "party", "spirituality"},
}

INCOMPATIBLE_TRANSITIONS = {
    "heartbreak"  : {"party", "euphoria"},
    "party"       : {"heartbreak", "existential", "spirituality", "protest"},
    "protest"     : {"party", "euphoria", "love"},
    "nostalgia"   : {"rage", "party", "street life"},
    "love"        : {"rage", "protest", "street life"},
    "existential" : {"party", "euphoria"},
    "street life" : {"love", "euphoria", "spirituality"},
    "spirituality": {"rage", "party", "street life"},
    "rage"        : {"love", "euphoria", "spirituality"},
    "euphoria"    : {"heartbreak", "existential", "rage", "protest", "street life"},
}

# Human-readable descriptions for jarring transitions (no raw theme/genre names in review text)
TRANSITION_CLASH_LINES = {
    ("nostalgia", "party"):     ["there is no way you put a party track right after something that nostalgic — what were you thinking?",
                                 "going from that nostalgic moment straight into a banger is a sequencing crime.",
                                 "the mood whiplash between those two tracks is genuinely jarring."],
    ("party", "heartbreak"):    ["you can't open someone's chest with a party record and then close it with something that heavy.",
                                 "the gear shift from that celebratory track to what follows it is brutal in the wrong way.",
                                 "that transition makes no sense — the party energy and the heartbreak energy cannot live next to each other like that."],
    ("party", "existential"):   ["a party track followed immediately by an existential one — someone needed to step in and rearrange this.",
                                 "the whiplash from that upbeat moment into deep philosophical territory is not the kind of tension that works."],
    ("party", "protest"):       ["you can't celebrate and protest back to back like that — one undermines the other.",
                                 "the tonal shift from the party track to the political one is jarring enough to break the whole listen."],
    ("euphoria", "heartbreak"):["going from pure euphoria straight into heartbreak is tonally reckless.",
                                 "the emotional jump between those two tracks is so large the album almost doesn't survive it."],
    ("rage", "love"):           ["rage into love with nothing in between — the album just changes personalities mid-sentence.",
                                 "the whiplash between that angry track and the love song after it is not earned at all."],
    ("rage", "euphoria"):       ["rage into euphoria with no transition — that's not contrast, that's confusion.",
                                 "you can't be that angry on one track and that euphoric on the very next one."],
    ("love", "rage"):           ["going from a love song straight into rage without any bridge — the album loses its footing right there.",
                                 "that tonal shift from love to rage is too abrupt and the album doesn't recover quickly."],
    ("heartbreak", "party"):   ["putting a party track right after something that heartbroken is tone-deaf sequencing.",
                                 "you go from pure heartbreak to a banger in one track — the album forgets what it's supposed to feel like."],
    ("spirituality", "rage"):  ["spiritual track straight into rage — it's a jarring transition that breaks the contemplative mood.",
                                 "the album goes from something sacred to something furious with no runway."],
    ("spirituality", "party"): ["coming out of something spiritual and dropping straight into a party track — no.",
                                 "the album violates its own emotional logic going from spiritual into celebratory like that."],
    ("street life", "euphoria"):["street life straight into pure euphoria — the social weight gets dropped completely.",
                                  "you can't carry that street life gravity into an euphoric track without losing what you built."],
    ("nostalgia", "rage"):      ["nostalgia straight into rage without anything in between — the album changes its mind too fast.",
                                 "the tonal whiplash from nostalgic to furious in one track break is real."],
    ("nostalgia", "street life"):["going from nostalgia into street life with no transition — those two worlds need a bridge.",
                                   "that back-to-back is the album's most jarring sequencing choice."],
    ("existential", "party"):   ["existential dread followed immediately by a party track — the album has no idea what it wants to be.",
                                  "you can't get philosophical and then instantly throw a party. The album earns that whiplash in the worst way."],
    ("existential", "euphoria"):["from existential into euphoria — the album abandons the philosophical weight it just built for no reason.",
                                  "that mood shift is too large to be intentional and too abrupt to be forgiven."],
}


def theme_transition_score(from_theme, to_theme):
    if from_theme is None:
        return 0
    if from_theme == to_theme:
        return 0.2
    if from_theme in COMPATIBLE_TRANSITIONS.get(to_theme, set()):
        return 0.2
    if from_theme in INCOMPATIBLE_TRANSITIONS.get(to_theme, set()):
        return -0.8
    return 0


def get_clash_line(from_theme, to_theme):
    """Return a reviewer-voice clash comment if a jarring transition is found, else None."""
    key = (from_theme, to_theme)
    if key in TRANSITION_CLASH_LINES:
        return pick(TRANSITION_CLASH_LINES[key])
    # Try reverse key — some transitions are bad in both directions
    rkey = (to_theme, from_theme)
    if rkey in TRANSITION_CLASH_LINES:
        line = pick(TRANSITION_CLASH_LINES[rkey])
        return line
    return None


def find_worst_transition(album):
    """Return (from_song, to_song, clash_line) for the single worst clash, or None."""
    worst_score = 0
    worst_pair  = None
    worst_line  = None
    for i in range(1, len(album.songs)):
        prev = album.songs[i - 1]
        curr = album.songs[i]
        ts   = theme_transition_score(prev.theme, curr.theme)
        if ts <= -0.8:
            line = get_clash_line(prev.theme, curr.theme)
            if line and ts < worst_score:
                worst_score = ts
                worst_pair  = (prev, curr)
                worst_line  = line
    if worst_pair:
        return worst_pair[0], worst_pair[1], worst_line
    return None


# ─────────────────────────────────────────────
#  ALBUM MODEL
# ─────────────────────────────────────────────

class Album:
    def __init__(self, name, core_genre, core_theme):
        self.name       = name
        self.core_genre = core_genre
        self.core_theme = core_theme
        self.songs      = []

    def add_song(self, song):
        self.songs.append(song)

    def song_count(self):
        return len(self.songs)

    def total_duration(self):
        return sum(s.duration for s in self.songs)

    def average_quality(self):
        if not self.songs:
            return 0
        return sum(s.quality for s in self.songs) / len(self.songs)

    def cohesion_stats(self):
        on_genre  = sum(1 for s in self.songs if self.core_genre in s.genres)
        off_genre = len(self.songs) - on_genre
        return on_genre, off_genre

    def cohesion_penalty(self):
        _, off = self.cohesion_stats()
        extra  = max(0, off - 2)
        return round(extra * 0.25, 2)

    def theme_alignment_ratio(self):
        if not self.songs:
            return 1.0
        matching = sum(1 for s in self.songs if s.theme == self.core_theme)
        return matching / len(self.songs)

    def theme_alignment_modifier(self):
        ratio = self.theme_alignment_ratio()
        if ratio >= 0.80:
            return  0.2
        elif ratio >= 0.60:
            return  0.0
        else:
            drop_units = int((0.60 - ratio) / 0.10)
            return -(drop_units * 0.2)

    def track_flow_modifier(self):
        total = 0.0
        for i in range(1, len(self.songs)):
            prev = self.songs[i - 1].theme
            curr = self.songs[i].theme
            total += theme_transition_score(prev, curr)
        return round(total, 2)

    def best_song(self):
        return max(self.songs, key=lambda s: s.quality)

    def worst_song(self):
        return min(self.songs, key=lambda s: s.quality)

    def deduced_genre(self):
        """Genre most commonly appearing in the tracklist (for reviewer deduction)."""
        counts = Counter()
        for s in self.songs:
            for g in s.genres:
                counts[g] += 1
        return counts.most_common(1)[0][0] if counts else self.core_genre

    def deduced_theme(self):
        """Theme most commonly appearing in the tracklist (for reviewer deduction)."""
        counts = Counter(s.theme for s in self.songs)
        return counts.most_common(1)[0][0] if counts else self.core_theme


# ─────────────────────────────────────────────
#  PERSONALITY SCORING HELPERS
# ─────────────────────────────────────────────

def personality_base(song_scores, personality):
    """
    Compute a personality-weighted base from individual song scores.
      strict:    weights the worst song heavily (weak tracks drag the score down)
      balanced:  plain average
      generous:  weights the best song (highlights lift the score)
      hype:      strong boost from top tracks, ignores bottom
    """
    if not song_scores:
        return 5.0
    avg = sum(song_scores) / len(song_scores)
    mn  = min(song_scores)
    mx  = max(song_scores)
    if personality == "strict":
        return round(avg * 0.65 + mn * 0.35, 3)
    elif personality == "generous":
        return round(avg * 0.85 + mx * 0.15, 3)
    elif personality == "hype":
        return round(avg * 0.80 + mx * 0.20, 3)
    else:  # balanced
        return round(avg, 3)


def apply_score_curve(raw, personality):
    """
    Post-process the final album score to preserve critic personality.
      strict:   compress the high end (8–10 range gets pulled toward 7)
      hype:     slight lift for mid-high scores
      generous: mild lift across the board
      balanced: no change
    """
    if personality == "strict":
        if raw > 7.0:
            excess = raw - 7.0
            raw    = 7.0 + excess * 0.45   # compress heavily above 7
        if raw > 8.5:
            raw = 8.5 + (raw - 8.5) * 0.25  # hard compress above 8.5
    elif personality == "hype":
        if raw > 6.0:
            raw = raw + (raw - 6.0) * 0.08   # slight boost above 6
    elif personality == "generous":
        raw = raw + 0.15                      # flat mild lift
    return round(clamp(raw), 1)


# ─────────────────────────────────────────────
#  TRACK-MENTION HELPERS
# ─────────────────────────────────────────────

def get_top_songs(song_scores, album_songs, threshold_gap=0.5, max_songs=5):
    """
    Return a list of (song, score) for the best track(s).
    If multiple tracks share the same score (or are within threshold_gap of the top),
    return all of them.
    """
    if not song_scores:
        return []
    mx = max(song_scores)
    top = [(album_songs[i], song_scores[i])
           for i in range(len(song_scores))
           if abs(song_scores[i] - mx) <= threshold_gap]
    return sorted(top, key=lambda x: -x[1])[:max_songs]


def get_bottom_songs(song_scores, album_songs, threshold_gap=0.5, max_songs=5):
    """
    Return a list of (song, score) for the worst track(s).
    If multiple tracks share the same bottom score, return all.
    """
    if not song_scores:
        return []
    mn = min(song_scores)
    bot = [(album_songs[i], song_scores[i])
           for i in range(len(song_scores))
           if abs(song_scores[i] - mn) <= threshold_gap]
    return sorted(bot, key=lambda x: x[1])[:max_songs]


def format_song_list(songs_scores):
    """Turn a list of (song, score) into a readable string: 'A', 'A' and 'B', etc."""
    names = [f"'{s.name}'" for s, _ in songs_scores]
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " and " + names[-1]


# ─────────────────────────────────────────────
#  BASE ALBUM CRITIC
# ─────────────────────────────────────────────

class AlbumCritic:
    """
    Wraps a song-critic for album-level logic.
    Each subclass defines:
      - personality:           "strict" | "balanced" | "generous" | "hype"
      - cohesion_sensitivity:  multiplier on cohesion penalty  (strict > 1, hype < 1)
      - theme_sensitivity:     multiplier on theme modifier
      - flow_sensitivity:      multiplier on flow modifier
      - length_sensitivity:    multiplier on length modifier
      - length_preference:     (min, max) ideal track count
    """

    personality          = "balanced"
    cohesion_sensitivity = 1.0
    theme_sensitivity    = 1.0
    flow_sensitivity     = 1.0
    length_sensitivity   = 1.0

    length_preference      = (8, 14)
    length_short_penalty   = -0.3
    length_long_penalty    = -0.3
    length_ideal_bonus     = 0.2

    def __init__(self, critic):
        self.critic = critic

    @property
    def name(self):    return self.critic.name
    @property
    def tagline(self): return self.critic.tagline

    # ── album score ────────────────────────────────────────────────
    def compute_album_score(self, album):
        song_scores = [self.critic.compute_score(s) for s in album.songs]

        # Personality-weighted base
        base = personality_base(song_scores, self.personality)

        # Album-level modifiers, each scaled by this critic's sensitivity
        cohesion_pen = album.cohesion_penalty()
        theme_mod    = album.theme_alignment_modifier()
        flow_mod     = album.track_flow_modifier()

        n   = album.song_count()
        lo, hi = self.length_preference
        if n < lo:
            length_mod = self.length_short_penalty
        elif n > hi:
            length_mod = self.length_long_penalty
        else:
            length_mod = self.length_ideal_bonus

        raw = (base
               - cohesion_pen  * self.cohesion_sensitivity
               + theme_mod     * self.theme_sensitivity
               + flow_mod      * self.flow_sensitivity
               + length_mod    * self.length_sensitivity)

        # Apply personality score curve (prevents inflation for strict critics)
        final = apply_score_curve(raw, self.personality)
        return final, song_scores

    # ── prose review ───────────────────────────────────────────────
    def write_review(self, album):
        album_score, song_scores = self.compute_album_score(album)
        tier = score_tier(album_score)

        # Deduced genre/theme (what the reviewer infers, not the internal label)
        ded_genre = album.deduced_genre()
        ded_theme = album.deduced_theme()

        # Top and bottom tracks (multi-mention support)
        top_songs = get_top_songs(song_scores, album.songs)
        bot_songs = get_bottom_songs(song_scores, album.songs)

        on, off = album.cohesion_stats()
        ratio   = album.theme_alignment_ratio()
        flow_mod= album.track_flow_modifier()

        # Find worst sequencing clash for explicit call-out
        clash = find_worst_transition(album)

        paragraphs = []

        paragraphs.append(self._opening(album, album_score, tier))
        paragraphs.append(self._cohesion(album, on, off, tier, ded_genre))
        paragraphs.append(self._continuity(album, ratio, flow_mod, tier, ded_theme, clash))
        paragraphs.append(self._praise_best(top_songs, album_score))
        paragraphs.append(self._critique_worst(bot_songs, album_score))

        # Length commentary only when album quality warrants it
        if album_score >= 5.0:
            length_note = self._length_note(album)
            if length_note:
                paragraphs.append(length_note)

        paragraphs.append(self._closing(album, album_score, tier))

        sentences = []
        for p in paragraphs:
            if isinstance(p, list):
                sentences.extend([ensure_punct(s) for s in p if s and s.strip()])
            elif p and p.strip():
                sentences.append(ensure_punct(p))

        return album_score, song_scores, " ".join(sentences)

    # ── Section builders (implemented per subclass) ────────────────

    def _opening(self, album, score, tier):
        raise NotImplementedError

    def _cohesion(self, album, on, off, tier, ded_genre):
        raise NotImplementedError

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        raise NotImplementedError

    def _praise_best(self, top_songs, album_score):
        raise NotImplementedError

    def _critique_worst(self, bot_songs, album_score):
        raise NotImplementedError

    def _length_note(self, album):
        return None

    def _closing(self, album, score, tier):
        raise NotImplementedError


# ─────────────────────────────────────────────
#  SHARED COHESION / CONTINUITY HELPERS
#  (returns raw strings — critic injects own voice via the pool structure)
# ─────────────────────────────────────────────

def _cohesion_label(off):
    """Classify cohesion state."""
    if off == 0:        return "pure"
    elif off <= 2:      return "minor_drift"
    elif off <= 4:      return "moderate_drift"
    else:               return "scattered"

def _continuity_label(ratio, flow_mod):
    if ratio >= 0.8 and flow_mod >= 0:   return "strong"
    elif ratio >= 0.6:                    return "decent"
    else:                                 return "weak"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 1 — MARCUS VANE (Elitist, strict)
# ═══════════════════════════════════════════════════════════════

class AlbumMarcusVane(AlbumCritic):
    personality          = "strict"
    cohesion_sensitivity = 1.4    # penalises genre drift heavily
    theme_sensitivity    = 1.3
    flow_sensitivity     = 1.5    # bad transitions hurt a lot
    length_sensitivity   = 1.2

    length_preference    = (9, 13)
    length_short_penalty = -0.5
    length_long_penalty  = -0.4
    length_ideal_bonus   = 0.3

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"'{album.name}' is a record that seems unaware of its own failures, which is the most frustrating kind of failure.",
                         f"I approached '{album.name}' hoping to be surprised. I was — by how thoroughly it confirmed my worst expectations.",
                         f"'{album.name}' demonstrates a consistent inability to convert ambition into execution — a complete record in the wrong sense.",
                         f"'{album.name}' is a project that mistakes activity for craft. Every track tries. None of them arrive."],
            "mid_low":  [f"'{album.name}' is a record in search of a reason to exist — it finds that reason intermittently, which is almost worse than not finding it.",
                         f"I wanted more from '{album.name}' because the materials occasionally suggest it was possible. It wasn't, quite.",
                         f"'{album.name}' is technically present in every sense that matters least.",
                         f"'{album.name}' assembles the parts of a real album without the vision to make them cohere."],
            "mid_high": [f"'{album.name}' is a record that works more often than it doesn't, which is more than I expected and less than I hoped.",
                         f"'{album.name}' earns my attention in intervals — the good stretches are genuinely good, which makes the lesser ones harder to excuse.",
                         f"'{album.name}' is a real record with real ideas that surface inconsistently across its runtime.",
                         f"'{album.name}' has the architecture of serious work and reaches that standard often enough to warrant the description."],
            "high":     [f"'{album.name}' is a serious piece of work — formally considered, emotionally present, and difficult to dismiss even when I try.",
                         f"'{album.name}' surprised me and surprised me honestly — this is the kind of album I don't expect to encounter.",
                         f"'{album.name}' is built from genuine artistic conviction and executed with craft that rewards the kind of attention I insist on giving.",
                         f"'{album.name}' has a structural integrity rare enough that calling it good feels like underselling it."],
            "perfect":  [f"'{album.name}' is a masterpiece and I will not qualify that statement.",
                         f"I have spent a career being skeptical of perfect records. '{album.name}' has made that skepticism feel like a mistake.",
                         f"'{album.name}' is what music is supposed to be. I do not say that without twenty years of critical standards behind it."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        n = album.song_count()
        if state == "pure":
            pools = {
                "low":      [f"The genre commitment here is absolute and pointless — discipline without vision is just repetition.",
                             f"Every track commits to the same sound and none of them do it well enough to justify that commitment."],
                "mid_low":  [f"The genre focus holds throughout but that consistency is wasted on material that doesn't rise to meet it.",
                             f"The album commits to a single identity with some success and more missed potential."],
                "mid_high": [f"The genre commitment here is complete — every track knows what album it's on and that consistency is a structural virtue.",
                             f"The album sounds like a unified statement from front to back, which is rarer than it should be."],
                "high":     [f"The genre identity holds from first track to last and never uses that consistency as an excuse for monotony — that combination is difficult to achieve.",
                             f"The album commits completely and the commitment pays off — every track earns its place in the framework."],
                "perfect":  [f"The genre coherence here is total and the album transcends it entirely — the form serves the content rather than containing it.",
                             f"The genre framework is so fully internalized that the album moves beyond it into something genuinely necessary."],
            }
        elif state == "minor_drift":
            pools = {
                "low":      [f"The {off} off-genre track{'s' if off > 1 else ''} don't help an album that already doesn't know what it's doing.",
                             f"The genre departures scatter what little identity the album had managed to establish."],
                "mid_low":  [f"The album wanders {off} time{'s' if off > 1 else ''} from its core identity — wandering it can't fully afford.",
                             f"Minor genre excursions that might have read as confidence in a stronger album read as drift here."],
                "mid_high": [f"The {off} off-genre track{'s' if off > 1 else ''} function as controlled experimentation rather than identity confusion — the core holds.",
                             f"The genre identity is secure enough to absorb {off} departure{'s' if off > 1 else ''} without losing itself."],
                "high":     [f"The {off} genre departure{'s' if off > 1 else ''} feel earned — the identity is secure enough to make them work as expansion rather than confusion.",
                             f"The album knows what it is well enough that the {off} deviation{'s' if off > 1 else ''} feel like creative decisions, not accidents."],
                "perfect":  [f"The small genre excursions here are acts of compositional confidence — the record is secure enough in its identity to stretch it deliberately.",
                             f"The {off} formal departure{'s' if off > 1 else ''} are the album's most elegant structural gestures."],
            }
        elif state == "moderate_drift":
            pools = {
                "low":      [f"The album drifts {off} times from its core identity and loses ground it never recovers.",
                             f"{off} off-genre tracks in {n} is a structural failure compounding an already underdeveloped record."],
                "mid_low":  [f"The {off} off-genre tracks create an identity problem the album never fully resolves.",
                             f"The genre inconsistency over {off} tracks is too many to read as exploration and too few to read as reinvention."],
                "mid_high": [f"The album has {off} genre departures that create some tension — the identity survives, barely.",
                             f"The {off} off-genre tracks cost the album a degree of cohesion it could otherwise have claimed."],
                "high":     [f"The {off} genre excursions are the album's one structural concession in an otherwise tightly controlled record.",
                             f"The identity holds despite {off} departures — but it's the one thing I'd point to as a missed opportunity for formal completeness."],
                "perfect":  [f"If I'm being precise, the {off} genre departures are the only thing standing between this record and structural perfection.",
                             f"The {off} deviations from the album's core identity are the record's single formal imperfection."],
            }
        else:  # scattered
            pools = {
                "low":      [f"The album doesn't know what it is and makes no attempt to find out — {off} off-genre tracks in {n} is beyond confusion.",
                             f"The genre incoherence here is total. This is a collection of songs given a title, not an album."],
                "mid_low":  [f"'{album.name}' doesn't know what it wants to be, and that indecision is audible across {off} tracks that abandon the sonic identity without committing to anything in its place.",
                             f"The genre inconsistency is the album's most significant structural failure."],
                "mid_high": [f"The {off} off-genre tracks are the album's central structural problem — it dilutes a record that otherwise has something real to say.",
                             f"The genre incoherence at {off} tracks is the one thing preventing this from being a more complete statement."],
                "high":     [f"The album's {off} genre departures are my one significant complaint about a record I otherwise admire considerably.",
                             f"The structural cost of {off} off-genre tracks is felt even in a record this strong."],
                "perfect":  [f"The {off} genre diversions are the record's only structural imperfection — remarkable that the album survives them and is still this complete.",
                             f"Despite {off} departures from the sonic identity, the album achieves a formal coherence that defies them."],
            }
        tier_pool = pools.get(tier, pools.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pools = {
                "low":      [f"The thematic thread runs consistently through this album — but it's pulling the same failing ideas in sequence.",
                             f"The sequencing is disciplined and the discipline is wasted on material that doesn't hold up."],
                "mid_low":  [f"The thematic focus is present and the execution below the level the focus deserves.",
                             f"The album follows its emotional thread — the thread just doesn't lead anywhere fully compelling."],
                "mid_high": [f"The thematic continuity is one of the record's genuine structural strengths — the through-line is real and the sequencing honors it.",
                             f"The album flows the way a serious record should — the emotional through-line is the spine and the songs organize themselves around it."],
                "high":     [f"The thematic architecture here is exceptional — the album reads as a coherent emotional argument rather than a collection of individual tracks.",
                             f"The through-line holds with the kind of structural care that distinguishes a record from a playlist."],
                "perfect":  [f"The thematic coherence is total and the sequencing is compositionally intelligent — the album builds, peaks, and resolves with formal completeness.",
                             f"The record is a complete emotional statement. The structure earned that description."],
            }
        elif state == "decent":
            pools = {
                "low":      [f"The thematic focus is present in roughly half the tracklist and absent in the half that needed it most.",
                             f"The album maintains its emotional thread intermittently — which is almost worse than not maintaining it at all."],
                "mid_low":  [f"The thematic alignment is sufficient but not exceptional — the emotional through-line is audible but occasionally muddied.",
                             f"The album maintains its thematic identity across most of the tracklist. The gaps are manageable but occasionally disruptive."],
                "mid_high": [f"The thematic focus is present without being total — the album mostly knows what it's feeling and the gaps are acceptable.",
                             f"The thematic architecture is functional rather than inspired — enough to hold the album together, not enough to make it a statement."],
                "high":     [f"The thematic consistency is good without being complete — the one area where the album could have pushed further.",
                             f"The through-line holds for most of the record and the small gaps are forgivable given how well the album manages them."],
                "perfect":  [f"The thematic gaps are the album's only structural concession — they're minor and the record overcomes them.",
                             f"The through-line dips occasionally but the album's overall formal strength more than compensates."],
            }
        else:  # weak
            pools = {
                "low":      [f"The thematic coherence is almost entirely absent — this album has no emotional logic to speak of.",
                             f"The track-to-track thematic logic is absent. The album is a collection of individually unremarkable pieces rather than a statement."],
                "mid_low":  [f"The thematic coherence is the album's most serious problem — the emotional through-line is barely there and the sequencing compounds the confusion.",
                             f"The album is thematically adrift — the through-line is present in too few tracks to anchor a record of any length."],
                "mid_high": [f"The thematic drift is the album's central structural weakness — a record this capable deserved more editorial discipline over the sequencing.",
                             f"The album loses its thematic thread too often — the emotional argument it's making isn't being made clearly enough."],
                "high":     [f"The thematic inconsistency is the one significant structural flaw in what is otherwise a compelling record.",
                             f"The album's sequencing logic is the single area where its formal ambition isn't matched by its execution."],
                "perfect":  [f"The thematic incoherence is the record's only real formal imperfection — remarkable that the album is still this good despite it.",
                             f"The sequencing is the one place the record doesn't fully match the quality of everything else it does."],
            }
        tier_pool = pools.get(tier, pools.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low", "mid_high"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        tier = score_tier(album_score)
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the record's defining {'moments' if multi else 'moment'} — the {'tracks' if multi else 'track'} around which everything else organizes.",
                    f"{names} justify the album on {'their' if multi else 'its'} own. Everything surrounding {'them' if multi else 'it'} benefits from being near {'them' if multi else 'it'}.",
                    f"{'These tracks are' if multi else 'This is'} what the entire album is reaching for, and {'they arrive' if multi else 'it arrives'} there completely."]
        elif bs_tier == "mid_high":
            pool = [f"{names} {'are' if multi else 'is'} the album's peak — {'tracks' if multi else 'a track'} that {'demonstrate' if multi else 'demonstrates'} what this record could have been consistently.",
                    f"The album reaches its highest point{'s' if multi else ''} on {names}, which {'are' if multi else 'is'} genuinely good and worth the price of admission.",
                    f"{names} {'are' if multi else 'is'} where the record becomes what it occasionally promises to be elsewhere."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the album's best {'offerings' if multi else 'offering'} — a modest distinction given the context, but honest.",
                    f"The best this album offers comes from {names}, and what it offers is, at minimum, present.",
                    f"The album comes closest to its stated intentions on {names}."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"Even the album's weakest {'moments' if multi else 'moment'} — {names} — {'are' if multi else 'is'} handled with sufficient craft that 'weak' is a relative term here.",
                    f"{names} {'are' if multi else 'is'} where the album breathes least efficiently — but the breathing never stops.",
                    f"If I'm being precise, {names} {'are' if multi else 'is'} where the album gives the least, and even then it gives more than most."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} the album's most significant {'missteps' if multi else 'misstep'} — {'they break' if multi else 'it breaks'} the momentum at exactly the wrong {'points' if multi else 'point'}.",
                    f"{names} {'represent' if multi else 'represents'} the album's structural problem in miniature — potential without follow-through.",
                    f"{names} {'are' if multi else 'is'} where I lose the record. The ideas are present; the execution is not."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} {'genuine failures' if multi else 'a genuine failure'} — {'they' if multi else 'it'} should not be on this record and {'their' if multi else 'its'} inclusion suggests an absence of editorial judgment.",
                    f"{names} {'cost' if multi else 'costs'} the album momentum it never recovers. Cut {'them' if multi else 'it'}.",
                    f"{names} {'are' if multi else 'is'} where the album breaks faith with its own best instincts."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks, the album is slightly short for what it's attempting — the ideas needed more room.",
                         f"The brevity at {n} tracks is its most forgivable limitation. Some records earn that length. This one needed more."])
        elif n > self.length_preference[1]:
            return pick([f"At {n} tracks, the album tests patience it hasn't fully earned. The editorial discipline could have been more severe.",
                         f"{n} tracks is two or three more than the material can sustain at this quality level."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["elitist"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' is not the record it could have been, and that is a charitable way of putting it.",
            "mid_low": f"'{album.name}' has its moments. They are not enough.",
            "mid_high":f"'{album.name}' is a record I will think about more than I expected to.",
            "high":    f"'{album.name}' is serious work and deserves to be taken seriously.",
            "perfect": f"'{album.name}' is the record. I do not say that about records.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 2 — DEJA HAYES (Hype)
# ═══════════════════════════════════════════════════════════════

class AlbumDejaHayes(AlbumCritic):
    personality          = "hype"
    cohesion_sensitivity = 0.7    # genre drift doesn't bother her much
    theme_sensitivity    = 0.8
    flow_sensitivity     = 0.6    # bad transitions forgiven more easily
    length_sensitivity   = 0.9

    length_preference    = (10, 16)
    length_short_penalty = -0.2
    length_long_penalty  = -0.3
    length_ideal_bonus   = 0.25

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"I came to '{album.name}' ready to love it and the album made that impossible.",
                         f"'{album.name}' has the energy of a record trying to be exciting without understanding what exciting requires.",
                         f"I kept waiting for '{album.name}' to start. By the end I was still waiting.",
                         f"'{album.name}' is exhausting in the worst way — it works so hard to connect and never does."],
            "mid_low":  [f"'{album.name}' is frustrating because the pieces are almost there — you can see what it wanted to be.",
                         f"'{album.name}' has a great album buried inside a decent one. The decent one got released.",
                         f"I wanted to love this more than I do. '{album.name}' is trying and almost getting there.",
                         f"'{album.name}' has the right ingredients and the wrong recipe."],
            "mid_high": [f"'{album.name}' is genuinely good and I mean that without hedging — this album delivers.",
                         f"'{album.name}' does what a good album is supposed to do: it keeps you in the room.",
                         f"I had a great time with '{album.name}'. The highs are real and the lows are survivable.",
                         f"'{album.name}' hits when it needs to hit and that's what I came for."],
            "high":     [f"'{album.name}' is the kind of record I put on for other people. That is the highest compliment I give.",
                         f"'{album.name}' goes. From the first track, it just goes.",
                         f"I've played '{album.name}' more times than I've reviewed it and I'm okay with that.",
                         f"'{album.name}' is the energy the room needs — I've been playing it everywhere."],
            "perfect":  [f"'{album.name}' is perfect. I'm not using that word loosely. I mean every syllable.",
                         f"There are albums you like and albums you need. '{album.name}' just became one I need.",
                         f"I'm going to be talking about '{album.name}' for years. Might as well start now."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["The genre is consistent but being consistently bad is still bad.",
                             "Staying in one lane means nothing when the lane is going nowhere."],
                "mid_low":  ["The album knows its genre and mostly stays in it — I just wished the genre moments were stronger.",
                             "Consistent sound but the sound isn't delivering the way I want it to."],
                "mid_high": [f"The identity is locked in across every track and it sounds like a complete vision — love that.",
                              f"Zero genre drift and that's actually impressive. It commits fully and the commitment pays off."],
                "high":     [f"Every song on this album knows what album it's on. The through-line is a feature, not a constraint.",
                              f"The album commits completely to its identity and the identity earns it."],
                "perfect":  [f"The album sounds like one fully realized thing — the genre coherence is part of why it feels this complete.",
                              f"Every track earns its place in the identity and the identity earns its place in your life."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      [f"The {off} genre departure{'s' if off>1 else ''} don't help an album that's already struggling.",
                              f"The small genre diversions scatter what little momentum the album had."],
                "mid_low":  [f"The {off} genre departure{'s' if off>1 else ''} are fine — the core holds, even if the core is only decent.",
                              f"Minor detours that don't save the album but don't hurt it either."],
                "mid_high": [f"Mostly locked in with {off} small genre detour{'s' if off>1 else ''} that show confidence rather than confusion.",
                              f"The album knows its identity and isn't afraid to stretch it. That's maturity."],
                "high":     [f"The {off} genre departure{'s' if off>1 else ''} feel like creative choices, not accidents — the album is too secure in its identity for them to register as confusion.",
                              f"The core holds and the deviations are fun. The album earns both."],
                "perfect":  [f"The small genre excursions are the album flexing, not wobbling. Perfect reads as complete and they're part of that completeness.",
                              f"The {off} formal departures are moments of pure confidence in an album full of them."],
            }
        elif state in ("moderate_drift", "scattered"):
            pool = {
                "low":      [f"The genre inconsistency is one of many things this album hasn't figured out.",
                              f"The {off} off-genre tracks scatter what little coherence the album manages elsewhere."],
                "mid_low":  [f"The genre focus slips {off} times and the album loses something every time it does.",
                              f"The {off} off-genre tracks are the one thing I'd go back and fix — the album needs more of a through-line."],
                "mid_high": [f"The genre inconsistency is the one thing holding this back — {off} off-genre tracks is too many for a completely cohesive listen.",
                              f"The album would be stronger with more genre focus — the {off} departures dilute the energy."],
                "high":     [f"The {off} genre departures are my one real complaint about a record I'm otherwise excited about.",
                              f"The album is strong enough that the {off} off-genre moments are forgivable — just barely."],
                "perfect":  [f"The only formal imperfection in this otherwise incredible record is the {off} genre diversions.",
                              f"The {off} off-genre tracks are the album's one flaw in an otherwise perfect listen."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The album flows consistently and the consistency is consistently not great.",
                             "The thematic through-line is there — it's just not carrying anything worth following."],
                "mid_low":  ["The album flows with some direction even if the direction isn't always compelling.",
                             "The theme holds for most of it — I just wanted the moments it holds to be stronger."],
                "mid_high": ["The theme flows through this album like a playlist should — each song leads into the next.",
                              "The track ordering is doing real emotional work — the through-line is there and it earns it."],
                "high":     ["The album flows like it was sequenced with care — because it was. Every transition is a decision.",
                              "The thematic consistency makes this a front-to-back listen and I've done it front to back multiple times."],
                "perfect":  ["The album flows perfectly and the sequencing is a huge part of why it feels complete.",
                              "Every transition is confident. The album is an emotional journey that earns every step."],
            }
        elif state == "decent":
            pool = {
                "low":      ["The theme holds for part of the record and drifts when it matters most.",
                             "The emotional consistency is there in chunks — the chunks aren't consistently the good ones."],
                "mid_low":  ["Some theme drift mid-album but the core is strong enough to pull it back together eventually.",
                             "The album's thematic journey is bumpy but the destination is clear enough most of the time."],
                "mid_high": ["The theme holds for most of the album — a few places where the mood shift catches you off guard but nothing that breaks the listen.",
                              "Mostly flows well. A few tonal detours but nothing that completely derails the energy."],
                "high":     ["The thematic consistency is one of the album's quieter strengths — mostly solid with a few moments where it loosens up.",
                              "The theme holds across most of the record and the gaps are small enough that the energy survives them."],
                "perfect":  ["The few thematic gaps are so well-handled that they barely register against the album's overall emotional completeness.",
                              "The album absorbs its thematic variations and comes out stronger for them."],
            }
        else:  # weak
            pool = {
                "low":      ["The album jumps around emotionally in ways that make it impossible to stay in it.",
                             "The thematic drift on top of everything else going wrong makes this a genuinely difficult listen."],
                "mid_low":  ["The thematic drift is real and it costs the album the cohesion it needed to pull everything together.",
                             "The album can't quite decide what it's about and you feel those gaps in every transition."],
                "mid_high": ["The theme flow is the album's weakest point — too many sudden tonal shifts, not enough of the connective tissue that makes albums feel like albums.",
                              "The album is good enough to survive its thematic inconsistency but would be so much better without it."],
                "high":     ["The album's thematic inconsistency is my one real structural complaint — the record is strong enough to survive it but it's felt.",
                              "The emotional logic is the one place this album doesn't fully match its own strengths."],
                "perfect":  ["The thematic drift is the album's sole imperfection — the record is so strong it barely matters, but I noticed.",
                              "If I'm being completely honest, the sequencing logic is the one area where the album doesn't reach its own ceiling."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the reason I'll still be playing this album in six months.",
                    f"{'These tracks are' if multi else 'This track is'} the moment where the album becomes undeniable.",
                    f"{names} alone would make the whole record worth talking about.",
                    f"{'Those are' if multi else 'That is'} the {'tracks' if multi else 'one'} that made me text people while I was listening."]
        elif bs_tier == "mid_high":
            pool = [f"{names} {'are' if multi else 'is'} the album's best argument for itself — everything it does well, {'they do' if multi else 'it does'} here.",
                    f"{'These are' if multi else 'This is'} where the album peaks and the peak is genuinely high.",
                    f"When {names} {'hit' if multi else 'hits'}, the album becomes exactly what I wanted it to be."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the best of what's here — limited, but the {'tracks' if multi else 'track'} {'themselves work' if multi else 'itself works'}.",
                    f"{'These are' if multi else 'This is'} the album's brightest {'spots' if multi else 'spot'} — I keep coming back to {'them' if multi else 'it'}.",
                    f"If you're going to sample this album, {names} {'are' if multi else 'is'} where to start."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} the one{'s' if multi else ''} I skip occasionally — which in this album just means {'they\'re' if multi else 'it\'s'} a nine instead of a ten.",
                    f"Even the weakest track{'s' if multi else ''} here — {names} — {'aren\'t' if multi else 'isn\'t'} a real skip, just a brief exhale.",
                    f"{names} {'are' if multi else 'is'} the light{'est' if not multi else ''} moment{'s' if multi else ''} in a heavy album — fine."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} where the energy drops and the album needs it not to drop right there.",
                    f"{names} {'don\'t' if multi else 'doesn\'t'} land the way the rest of the record does — the one{'s' if multi else ''} the album could have done without.",
                    f"{'These are' if multi else 'This is'} a dip I can forgive but I do notice {'them' if multi else 'it'} every single time."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} a problem — {'they stall' if multi else 'it stalls'} the album at the worst possible moment.",
                    f"{names} {'break' if multi else 'breaks'} the spell the album works hard to cast. {'They don\'t' if multi else 'It doesn\'t'} belong here.",
                    f"I love this album enough to be honest about {names}: {'they don\'t' if multi else 'it doesn\'t'} belong on this record."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks I wanted more — the album ends just when it's fully warmed up.",
                         f"{n} tracks isn't enough for the world this album is building. I wanted to stay longer."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is a lot and the album earns about {self.length_preference[1]} of them.",
                         f"The album is a touch bloated at {n} tracks — a harder edit would make the good parts hit harder."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["hype"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' had everything it needed except the execution.",
            "mid_low": f"'{album.name}' is close to great and that's both the compliment and the critique.",
            "mid_high":f"'{album.name}' is solid and I'm happy to say that without caveats.",
            "high":    f"'{album.name}' is one of the best records I've heard this cycle.",
            "perfect": f"'{album.name}' is it. Full stop.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 3 — VIC OSEI (Blunt, very strict)
# ═══════════════════════════════════════════════════════════════

class AlbumVicOsei(AlbumCritic):
    personality          = "strict"
    cohesion_sensitivity = 1.6    # genre drift hits hard
    theme_sensitivity    = 1.4
    flow_sensitivity     = 1.6
    length_sensitivity   = 1.8    # Vic hates bloat

    length_preference    = (8, 11)
    length_short_penalty = -0.3
    length_long_penalty  = -0.7
    length_ideal_bonus   = 0.1

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"'{album.name}'. No.",
                         f"Listened to all of '{album.name}'. Didn't need to.",
                         f"'{album.name}' is not good. Moving on.",
                         f"'{album.name}' doesn't work. Any of it."],
            "mid_low":  [f"'{album.name}' is mostly fine. Mostly not interesting either.",
                         f"'{album.name}' exists. Some of it works. Most of it is mid.",
                         f"'{album.name}': has some moments, wastes most of them.",
                         f"'{album.name}' has ideas. Doesn't know what to do with them."],
            "mid_high": [f"'{album.name}' is actually decent. Didn't expect that.",
                         f"'{album.name}' works. Not groundbreaking. But it works.",
                         f"I've heard worse albums than '{album.name}'. I've heard better. This sits fine in the middle.",
                         f"'{album.name}': competent. Occasionally more than competent."],
            "high":     [f"'{album.name}' is genuinely good. Annoying to admit but true.",
                         f"'{album.name}' hit. Solid record. Not wasting more words than it deserves.",
                         f"'{album.name}' earns it. That's the review.",
                         f"'{album.name}' is the real thing. Said it."],
            "perfect":  [f"'{album.name}' is great. Fine. I said it.",
                         f"'{album.name}' is actually flawless. I'll acknowledge that once.",
                         f"'{album.name}'. Yeah. This one's real."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["Sticks to one genre. Consistently. Consistently bad.", "Full commitment to one sound. The wrong sound."],
                "mid_low":  ["Consistent throughout. Consistently average.", "Knows what it is. Still kind of mid."],
                "mid_high": ["Sticks to one thing. Consistent. Fine.", "Full album identity. No crisis. Appreciated."],
                "high":     ["Fully committed to the sound. All the way through. Good.", "Knows what it is. Doesn't waver. That matters."],
                "perfect":  ["Total commitment. Pays off completely.", "Perfect identity. Held the whole way."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      [f"{off} genre departure{'s' if off>1 else ''} on top of everything else that's not working.", "The small detours don't help a struggling album."],
                "mid_low":  [f"{off} track{'s' if off>1 else ''} step outside the lane. Album survives it. Barely.", f"Minor drift. Doesn't save anything but doesn't kill it."],
                "mid_high": [f"{off} departure{'s' if off>1 else ''}. Small. Album survives.", f"Mostly locked in with {off} small side trip{'s' if off>1 else ''}. Fine."],
                "high":     [f"Minor genre drift — {off} track{'s' if off>1 else ''}. Handled well. Doesn't matter.", f"The {off} detour{'s' if off>1 else ''} are earned. Album is secure enough."],
                "perfect":  [f"The {off} small departure{'s' if off>1 else ''} are the album flexing. Works.", "Tiny genre diversions. Controlled. Part of why it's complete."],
            }
        else:
            pool = {
                "low":      [f"{off} off-genre tracks. Album has no idea what it is.", f"Genre confusion. {off} times. Every time it costs something it can't afford."],
                "mid_low":  [f"{off} off-genre tracks. Too many. Pick a lane.", f"Genre identity gets lost {off} times. Still loses."],
                "mid_high": [f"{off} off-genre tracks. Noticeable. Album would be tighter without them.", f"Genre drift over {off} tracks is the one thing holding this back."],
                "high":     [f"The {off} genre departures are my only complaint. Still a complaint.", f"{off} off-genre moments in an otherwise locked-in record. Minor deduction."],
                "perfect":  [f"The {off} departures are the record's one imperfection. Barely registers.", "Genre diversions are the lone flaw. The record survives them easily."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["Theme consistent. Consistently bad.", "Thematic through-line present. Still not good."],
                "mid_low":  ["Theme holds. The stuff the theme is holding together is mid.", "Consistent theme. Average everything else."],
                "mid_high": ["Theme is consistent. Sequencing isn't a mess. Good.", "Thematically together. No complaints there."],
                "high":     ["Theme locked in. Sequencing works. Album flows.", "Thematic coherence is one of the album's real strengths."],
                "perfect":  ["Perfect thematic flow. Everything in the right place.", "Sequencing is tight. Theme is complete."],
            }
        elif state == "decent":
            pool = {
                "low":      ["Theme holds for half of it. The half that works least.", "Thematic consistency when it doesn't matter most."],
                "mid_low":  ["Theme holds for most of it. Rest drifts. Survivable.", "Some thematic inconsistency. Not fatal. Noticeable."],
                "mid_high": ["Theme slips a bit. Not fatal.", "Some drift. Manageable. Album holds together."],
                "high":     ["Minor thematic gaps. Album strong enough to carry them.", "The drift is there. Barely registered against the overall quality."],
                "perfect":  ["Small thematic gaps. Album doesn't care. Neither do I.", "Minor theme drift. Irrelevant given everything else."],
            }
        else:
            pool = {
                "low":      ["No thematic logic. Just a playlist with a title.", "Thematic drift is one more thing wrong with this record."],
                "mid_low":  ["Thematic consistency is basically absent. Album feels scattered.", "No real through-line. Just songs."],
                "mid_high": ["Thematic drift is the album's main flaw. It's a real flaw.", "The sequencing logic is missing. You feel it throughout."],
                "high":     ["The thematic incoherence is my one real complaint about this record.", "Sequencing is the one thing I'd fix. It's fixable."],
                "perfect":  ["Only real flaw: the thematic logic. Record is still excellent.", "The sequencing is the lone imperfection. The album earns the score anyway."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low", "mid_high"):
            return base_line + " Also: " + clash_line + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} excellent. Best track{'s' if multi else ''} here. Not close.",
                    f"{names} {'earn' if multi else 'earns'} it. Best thing here by some distance.",
                    f"Play {names}. Skip the rest if you're in a hurry."]
        elif bs_tier == "mid_high":
            pool = [f"{names} {'are' if multi else 'is'} the album's best moment{'s' if multi else ''}. Which is a solid moment{'s' if multi else ''}.",
                    f"{names} {'work' if multi else 'works'} well. High point of the record.",
                    f"{names} {'are' if multi else 'is'} where I'd tell someone to start."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the best of a limited set. Fine.",
                    f"{names} {'edge' if multi else 'edges'} out the competition. Not by a lot.",
                    f"{names} {'are' if multi else 'is'} the least problematic. That's the compliment."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} the weakest here. Still fine. Album doesn't suffer.",
                    f"{names} {'dip' if multi else 'dips'} slightly. Nothing serious.",
                    f"{names} {'are' if multi else 'is'} where I briefly checked my phone. Not a real problem."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} filler. {'They show.' if multi else 'It shows.'}",
                    f"{names} {'shouldn\'t be where they are' if multi else 'shouldn\'t be where it is'} on the tracklist.",
                    f"{names} {'are' if multi else 'is'} mid. The album doesn't need {'them' if multi else 'it'}."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} bad. Genuinely {'hurt' if multi else 'hurts'} the album. Cut {'them' if multi else 'it'}.",
                    f"{names} {'are' if multi else 'is'} the problem. {'It\'s' if not multi else 'They\'re'} obvious.",
                    f"{names} {'don\'t' if multi else 'doesn\'t'} belong here. Editorial failure."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"{n} tracks. Short. Could've gone longer.",
                         f"Could've been a few more tracks. {n} is fine but barely."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is too many. Trim it.",
                         f"{n} songs. About {n - self.length_preference[1]} too many.",
                         f"Nobody needed {n} tracks. Cut the dead weight."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["blunt"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}': don't bother.",
            "mid_low": f"'{album.name}': has its moments, not many.",
            "mid_high":f"'{album.name}': worth a listen.",
            "high":    f"'{album.name}': actually solid. Respect.",
            "perfect": f"'{album.name}': great album. Said it.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 4 — RAY COLDWELL (Contrarian)
# ═══════════════════════════════════════════════════════════════

class AlbumRayColdwell(AlbumCritic):
    personality          = "balanced"
    cohesion_sensitivity = 0.8    # reads genre drift as interesting
    theme_sensitivity    = 0.9
    flow_sensitivity     = 1.0
    length_sensitivity   = 0.9

    length_preference    = (9, 14)
    length_short_penalty = -0.2
    length_long_penalty  = -0.2
    length_ideal_bonus   = 0.2

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"'{album.name}' is a record everyone will dismiss — and for once, their instincts will be correct.",
                         f"I looked for the hidden value in '{album.name}'. I'm not finding it, and I looked harder than most would.",
                         f"'{album.name}' is bad. I'm not being contrarian — the mainstream will hate it and they will be right.",
                         f"'{album.name}' is the rare case where the consensus and I agree. It doesn't work."],
            "mid_low":  [f"The consensus on '{album.name}' will be kind and the consensus will be wrong — this is worse than it'll be given credit for.",
                         f"'{album.name}' is a four that most critics will call a six. I'm not most critics.",
                         f"'{album.name}' has the kind of surface appeal that passes for depth in lazy reviews. It isn't depth.",
                         f"'{album.name}' will be praised for the wrong reasons and the right reasons will be ignored."],
            "mid_high": [f"'{album.name}' will be slept on. Most albums get overrated. This one will get underrated.",
                         f"The critical establishment will be lukewarm about '{album.name}'. The critical establishment will be wrong.",
                         f"'{album.name}' is better than it will be given credit for. I'm saying that now.",
                         f"'{album.name}' will be called a six. It's a seven. The difference matters."],
            "high":     [f"'{album.name}' is the record this cycle that nobody is going to give enough credit to. I'm giving it the credit.",
                         f"'{album.name}' is a genuinely important record that will be correctly identified as such only in retrospect.",
                         f"I'm calling '{album.name}' now: excellent, underrated, and correctly assessed only by a minority.",
                         f"'{album.name}' will be overlooked by the publications that matter. It's better than everything they'll prioritize over it."],
            "perfect":  [f"I've been called contrarian my entire career. I'm calling '{album.name}' a masterpiece first.",
                         f"'{album.name}' is the perfect record this year that no one will say is perfect this year. History will correct that.",
                         f"The consensus will catch up to '{album.name}' eventually. For now: a masterpiece, and I'm on record."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["The genre unity will be called 'focused' — it's actually limiting, and the album confirms why.",
                             "Every track in the same lane, every track going nowhere interesting."],
                "mid_low":  ["The genre commitment is consistent without being compelling — consistency is a virtue, not an achievement.",
                             "The album knows its identity. I just wish the identity had more to offer."],
                "mid_high": ["The genre unity will be called 'limiting' by critics who mistake range for quality. It's not limiting — it's focused.",
                              "Zero genre drift. Critics will call it narrow. I'll call it intentional."],
                "high":     ["Everyone will say the genre commitment is a weakness. It's a strength most albums don't have the discipline to achieve.",
                              "The album commits completely and the commitment is the right call — focus is underrated."],
                "perfect":  ["The genre coherence here will be under-appreciated by critics who confuse eclecticism with depth. This is better than eclectic.",
                              "The focus is the album's structural virtue — the album earns every track staying in the same space."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      [f"The {off} genre departure{'s' if off>1 else ''} will be called adventurous — they're actually the album's few interesting moments in a record that needed more of them.",
                              "The small detours are the most interesting parts of an album that otherwise isn't."],
                "mid_low":  ["The genre excursions show some compositional confidence that the rest of the album doesn't quite match.",
                              "The minor departures are where the album actually tries something — the rest of it is too safe."],
                "mid_high": [f"The {off} genre departure{'s' if off>1 else ''} will be called adventurous. They're controlled experiments, which is different and better.",
                              "Minor genre excursions that show real compositional confidence — most reviewers will miss why."],
                "high":     ["The small departures earn their place — the album is secure enough to make them work.",
                              "The genre excursions are acts of confidence, not confusion. The difference is audible."],
                "perfect":  ["The small genre excursions are the most overlooked quality of an album that will have plenty of overlooked qualities.",
                              "The formal departures are compositionally intelligent and will be under-appreciated as such."],
            }
        else:
            pool = {
                "low":      [f"The genre incoherence at {off} tracks is one of several things I can't work around here.",
                              f"The {off} off-genre tracks scatter an album that was already losing its way."],
                "mid_low":  [f"The genre inconsistency at {off} tracks is a problem. Calling it 'eclectic' won't fix it.",
                              "The album doesn't know what it is and the {off} off-genre tracks prove it."],
                "mid_high": [f"The genre incoherence at {off} tracks is going to be called 'eclectic' by supportive reviews. It's actually confused.",
                              f"{off} off-genre tracks is a problem even a generous reading can't resolve into 'experimentation'."],
                "high":     [f"The {off} genre departures are my one complaint about an otherwise exceptional record.",
                              "The genre incoherence is the one thing I can't defend in what is otherwise a strong album."],
                "perfect":  [f"The {off} departures are the record's only structural imperfection — remarkable that it's still this good.",
                              "The genre drift is the sole flaw in a masterpiece. The masterpiece wins."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The thematic coherence is the album's one structural virtue — applied to material that doesn't deserve it.",
                             "The through-line is there. It just doesn't lead anywhere worth going."],
                "mid_low":  ["The thematic coherence is more interesting than the actual songs — the sequencing is doing more than the writing.",
                             "The theme holds together better than the music it's holding."],
                "mid_high": ["The thematic coherence is one of the album's most underappreciated qualities — the through-line is there and it's doing real structural work.",
                              "The track ordering is doing compositional work that most reviewers won't bother to trace."],
                "high":     ["The thematic architecture is the album's most underappreciated structural quality — it runs through the record with a logic most reviewers won't follow closely enough.",
                              "The sequencing is a quiet act of intelligence that will be credited to luck by critics who don't notice craft."],
                "perfect":  ["The thematic completeness here will be taken for granted — it should be studied.",
                              "The sequencing is compositionally intelligent at a level that the mainstream press will not acknowledge."],
            }
        elif state == "decent":
            pool = {
                "low":      ["The theme holds for part of it and the part where it holds isn't the good part.",
                             "Adequate thematic consistency for an inadequate record."],
                "mid_low":  ["The thematic drift will be read as inconsistency — there's a structural logic to it that resists that reading, but the logic needs more room.",
                             "The theme is there for most of the album and the gaps are more interesting than the consistent parts."],
                "mid_high": ["The theme flow is imperfect and more intentional than it will be given credit for.",
                              "The thematic inconsistency has a logic. Not everyone will find it but it's there."],
                "high":     ["The thematic gaps are the album's most misread quality — they're structural decisions, not oversights.",
                              "The theme drift will be called a flaw. It's actually the album's most interesting compositional risk."],
                "perfect":  ["The few thematic gaps are compositional decisions that will be misread as inconsistencies by critics who prefer things obvious.",
                              "The thematic variance is controlled and purposeful — the record is secure enough to absorb it."],
            }
        else:
            pool = {
                "low":      ["The thematic incoherence is one more problem on a record full of them.",
                             "The album has no emotional logic and the sequencing proves it."],
                "mid_low":  ["The thematic incoherence is the album's real structural problem — I can't find the hidden intelligence in the scattering.",
                             "Only the thematic incoherence here isn't a hidden strength — it's just incoherence."],
                "mid_high": ["The album is thematically scattered and I can't find the intelligence in the scattering.",
                              "The thematic confusion is the one thing I can't reframe as a contrarian strength."],
                "high":     ["The thematic incoherence is my one complaint about a record I otherwise champion.",
                              "The sequencing logic is absent and that's the only real structural failure in an otherwise strong album."],
                "perfect":  ["The thematic drift is the record's sole formal imperfection and the record overcomes it.",
                              "The sequencing is the lone weak point in a masterpiece."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the {'tracks' if multi else 'track'} the mainstream will overlook. {'They are' if multi else 'It is'} also the best thing on the record by some distance.",
                    f"{names} {'are' if multi else 'is'} what the album is actually about — the rest of the tracklist justifies being in proximity to {'them' if multi else 'it'}.",
                    f"{names} will be treated as deep cuts. {'They deserve' if multi else 'It deserves'} more than that."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the album's best {'moments' if multi else 'moment'} and {'they\'re' if multi else 'it\'s'} better than most will say.",
                    f"{names} will be slept on. {'They are' if multi else 'It is'} the best argument the album makes for itself.",
                    f"{names} deserves more attention than the record around {'them' if multi else 'it'} will generate."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"Even the lowest-rated track{'s' if multi else ''} here — {names} — {'are' if multi else 'is'} more interesting than the consensus will rate the whole album.",
                    f"{names} {'are' if multi else 'is'} the weakest here and still more interesting than most albums' highlights."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} where the album takes the easy path. The rest of the record earns its difficulty — {'these don\'t' if multi else 'this doesn\'t'}.",
                    f"{names} {'are' if multi else 'is'} the compromise that costs the album some integrity.",
                    f"{names} will be the most praised {'tracks' if multi else 'track'} by people doing surface-level reviews. {'They\'re' if multi else 'It\'s'} actually the weakest part."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} {'genuine failures' if multi else 'a genuine failure'} and I won't pretend otherwise.",
                    f"{names} {'are' if multi else 'is'} bad. Not interestingly bad. Just bad. And that's the one thing I can't work with.",
                    f"{names} {'are' if multi else 'is'} the flaw I can't argue around."]
        return pick(pool)

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["contrarian"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' is not a victim of critical misreading. It's just not good.",
            "mid_low": f"'{album.name}' is worse than it looks and better than it sounds — neither add up to a recommendation.",
            "mid_high":f"'{album.name}' deserves better coverage than it will get.",
            "high":    f"'{album.name}' is important and will be correctly recognized as such only after the fact.",
            "perfect": f"'{album.name}' is a masterpiece. I said it first.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 5 — EARL MOSELY (Nostalgic, generous)
# ═══════════════════════════════════════════════════════════════

class AlbumEarlMosely(AlbumCritic):
    personality          = "generous"
    cohesion_sensitivity = 0.9
    theme_sensitivity    = 1.1
    flow_sensitivity     = 0.8
    length_sensitivity   = 0.7    # Earl likes long albums

    length_preference    = (10, 18)
    length_short_penalty = -0.4
    length_long_penalty  = -0.1
    length_ideal_bonus   = 0.3

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"I've spent fifty years with music and '{album.name}' reminds me of what happens when the tradition is ignored entirely.",
                         f"'{album.name}' is what gets made when no one in the room has actually listened to the records that made this genre worth caring about.",
                         f"I approached '{album.name}' with the patience I extend to all new records. It exhausted that patience before the third track.",
                         f"'{album.name}' has the materials of music and none of the spirit that makes music matter."],
            "mid_low":  [f"'{album.name}' has the spirit of something real in it — intermittently — which makes the overall result harder to accept.",
                         f"There are moments in '{album.name}' that suggest the artist understands what great music requires. Those moments are too few.",
                         f"'{album.name}' knows what it wants to be. It gets there occasionally and not consistently enough.",
                         f"'{album.name}' reaches for something genuine — it doesn't always find it but the reaching is real."],
            "mid_high": [f"'{album.name}' has something genuine in it — a quality I don't always find in new records and appreciate finding when I do.",
                         f"'{album.name}' reminds me, in its better moments, of why I still do this after all this time.",
                         f"'{album.name}' is a real album — built the old way, with care and sequence and intention.",
                         f"'{album.name}' is the kind of record that respects its listener and its tradition simultaneously."],
            "high":     [f"'{album.name}' is the kind of record I've been waiting for — music made with the understanding that records are supposed to last.",
                         f"'{album.name}' has the quality I look for and rarely find: it sounds like it was made for posterity, not for this week.",
                         f"'{album.name}' belongs in the conversation about the best records of its era. I'm putting it there now.",
                         f"'{album.name}' made me feel the way the great records made me feel. That doesn't happen often anymore."],
            "perfect":  [f"I've been listening for a very long time. '{album.name}' is one of the great records.",
                         f"'{album.name}' is the kind of record you hear and recognize immediately — it belongs with the ones that last.",
                         f"In fifty-seven years of listening, very few records have made me feel the way '{album.name}' just made me feel."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["The genre commitment is complete and the material doesn't honor it. A record can be disciplined and still be poor.",
                             "The consistency is there. The inspiration that should fill it isn't."],
                "mid_low":  ["The genre focus holds throughout — the focus is applied to material that could have been stronger.",
                             "The album commits to its identity and the identity is only occasionally up to the commitment."],
                "mid_high": ["The genre commitment is complete and it's the right commitment — the album sounds like a unified statement, not a sampler.",
                              "Every track earns its place in the framework. That kind of coherence used to be the baseline expectation."],
                "high":     ["The genre consistency here is the kind the great albums had — not because of formula, but because of genuine artistic vision.",
                              "The album commits fully and the commitment pays off. That's how the best records have always worked."],
                "perfect":  ["The genre coherence here is the kind you find in the records that last — fully internalized, never mechanical.",
                              "The album holds one identity from first to last and makes it feel like the only possible choice."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      [f"The {off} genre departure{'s' if off>1 else ''} can't save an album that needs more than a few interesting detours.",
                              "The small diversions are the album's livelier moments — the core needed to match them."],
                "mid_low":  ["A bit of genre flexibility can be healthy but here it highlights what the core is missing.",
                              "The genre excursions are fine — the album just needed more substance around them."],
                "mid_high": [f"The {off} departure{'s' if off>1 else ''} feel earned — the identity is secure enough to make them work.",
                              "A bit of genre flexibility is healthy. The great records often had it. This uses it wisely."],
                "high":     ["The genre excursions feel like creative confidence — the album is secure enough in its identity to stretch it deliberately.",
                              "The small departures from the core are where the album shows its range without losing its identity."],
                "perfect":  ["The genre excursions are the album flexing its creative confidence — the identity is so secure they only add to it.",
                              "The small departures feel like natural breathing room in a record that knows exactly what it is."],
            }
        else:
            pool = {
                "low":      [f"The {off} off-genre tracks create an identity confusion that the old records would not have permitted.",
                              "The album loses itself too many times and never fully recovers that sense of knowing who it is."],
                "mid_low":  [f"Genre consistency was once considered non-negotiable for a reason. {off} departures from the core leave the album without a clear identity.",
                              f"The album loses itself {off} times. The loss accumulates."],
                "mid_high": [f"The {off} off-genre tracks are a structural cost in what is otherwise a well-organized record.",
                              "The genre inconsistency is the one thing I'd change — the album would be stronger with more focus."],
                "high":     [f"The {off} genre departures are my one significant complaint about a record I deeply admire.",
                              "The genre inconsistency is a small structural cost in an otherwise complete record."],
                "perfect":  [f"The {off} departures are the record's only formal imperfection — the album transcends them.",
                              "A few genre diversions in what is otherwise a perfect record. The perfection wins."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The album flows with a consistency that the material doesn't earn — a journey without a destination.",
                             "The thematic through-line is there. The music it runs through isn't strong enough."],
                "mid_low":  ["The thematic continuity is the album's best structural quality — applied to material that needed more development.",
                             "The through-line holds and the music only occasionally rises to meet it."],
                "mid_high": ["The album flows the way albums used to flow, when people still believed that the order of songs was an artistic choice.",
                              "The thematic coherence here is the kind that takes thought and care. Someone spent time on the sequencing."],
                "high":     ["The through-line holds across the whole record and the sequencing is what sequencing was always supposed to be — a deliberate emotional journey.",
                              "The album flows with the care of a record made by someone who understands what albums are for."],
                "perfect":  ["The album flows the way the great albums flow — every track in its exact right place, every transition earned.",
                              "The thematic journey here is complete and the sequencing honors it entirely."],
            }
        elif state == "decent":
            pool = {
                "low":      ["The thematic consistency is there in the better moments — the better moments aren't enough.",
                             "The through-line holds for part of the record and drifts when it matters most."],
                "mid_low":  ["The album maintains its thematic identity across most of the tracklist — enough to feel intentional even if not fully realized.",
                             "The thematic continuity is good without being great. The old records set a higher standard."],
                "mid_high": ["The thematic continuity is good without being great. The old records set a higher standard, but this clears the basic requirement.",
                              "Some drift from the thematic thread but the core holds. Not the work of a master sequencer but honest work."],
                "high":     ["The thematic consistency is one of the album's quieter strengths — holding together even where it loosens slightly.",
                              "The through-line holds for most of the record. The old masters would have held it tighter, but this is still careful work."],
                "perfect":  ["The thematic gaps are the record's only structural concession and the record absorbs them gracefully.",
                              "The through-line holds for nearly all of the album — the small gaps are a minor imperfection in something otherwise complete."],
            }
        else:
            pool = {
                "low":      ["The thematic coherence is the album's most significant shortcoming. The old records understood why sequencing mattered.",
                             "The album lacks the kind of sequencing intelligence that once distinguished records from collections."],
                "mid_low":  ["The great albums had a reason for every track to be in every position. This one doesn't, and the disorder is felt.",
                             "The thematic drift is the album's most serious problem — the record never settles into being a complete statement."],
                "mid_high": ["The album loses its thematic thread too often for a record with this much to say. Someone needed to make harder choices in the sequencing.",
                              "The thematic logic is the album's one real weakness. The rest of the record deserved a more disciplined sequencing."],
                "high":     ["The thematic inconsistency is the one place where this record doesn't honor the tradition it's working in.",
                              "The album's sequencing is the single area where it falls short of the standard the rest of it sets."],
                "perfect":  ["The thematic drift is the record's only formal imperfection — the album is too strong for it to matter much, but it's noticed.",
                              "The sequencing logic is the one area this record doesn't quite match its own excellence."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low", "mid_high"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the {'tracks' if multi else 'track'} that will last — the {'ones' if multi else 'one'} people are still listening to when everything else has faded.",
                    f"{names} {'are' if multi else 'is'} where this album earns its place in memory. A genuinely great {'moment' if not multi else 'collection of moments'}.",
                    f"{names} {'are' if multi else 'is'} the kind of {'songs' if multi else 'song'} the old musicians would have been proud of. That is the highest thing I know how to say."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the album's best {'offerings' if multi else 'offering'} — genuine high {'points' if multi else 'point'} in a record of uneven altitude.",
                    f"{'These tracks' if multi else 'This track'} — {names} — {'are' if multi else 'is'} where the album comes closest to the standard it seems to be reaching for.",
                    f"{names} {'are' if multi else 'is'} the {'tracks' if multi else 'track'} I'll return to — the {'ones' if multi else 'one'} with enough soul to warrant the journey."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} the album's softest {'moments' if multi else 'moment'} — which in the context of this record is a modest criticism.",
                    f"{names} {'are' if multi else 'is'} where the album rests rather than arrives. A small concession in an otherwise strong record.",
                    f"{'These are' if multi else 'This is'} the one{'s' if multi else ''} I'll occasionally skip — the rest of the album sets a high enough standard that the comparison isn't kind to {'them' if multi else 'it'}."]
        elif album_score >= 5:
            pool = [f"{names} {'lack' if multi else 'lacks'} the depth the rest of the album has found — {'they\'re' if multi else 'it\'s'} filler in a record that shouldn't have filler.",
                    f"{names} {'are' if multi else 'is'} where the album stumbles — and in a record that otherwise walks carefully, the stumble is noticeable.",
                    f"{'These tracks' if multi else 'This track'} — {names} — {'are' if multi else 'is'} where the album could have done without, and the album would have been better for the absence."]
        else:
            pool = [f"{names} {'fall' if multi else 'falls'} below the standard the rest of the album has set. In my experience, a bad track can cost an album its legacy.",
                    f"{names} {'are' if multi else 'is'} the album's most serious {'missteps' if multi else 'misstep'} — {'tracks' if multi else 'a track'} that {'don\'t' if multi else 'doesn\'t'} belong in the company of the others.",
                    f"{names} {'break' if multi else 'breaks'} faith with the album's best instincts. {'They are' if multi else 'It is'} a genuine problem."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks, the album ends before it's fully said what it has to say. The old records breathed longer.",
                         f"{n} tracks isn't enough time for this material to develop the way it deserves to."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is ambitious and I respect the ambition, even if a few tracks could have been trimmed without loss.",
                         f"A long record is fine when the material is there. Most of this album earns its length."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["nostalgic"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' is not the record this generation deserves to settle for.",
            "mid_low": f"'{album.name}' had the makings of something lasting and chose not to be.",
            "mid_high":f"'{album.name}' is a record made with care and that care is felt.",
            "high":    f"'{album.name}' is the real thing. I don't use those words carelessly.",
            "perfect": f"'{album.name}' is a great record. I've heard the great records. This is one of them.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 6 — ZARA NIGHTS (Scenes)
# ═══════════════════════════════════════════════════════════════

class AlbumZaraNights(AlbumCritic):
    personality          = "balanced"
    cohesion_sensitivity = 1.1
    theme_sensitivity    = 1.0
    flow_sensitivity     = 1.2    # scene cares about vibe continuity
    length_sensitivity   = 1.1

    length_preference    = (9, 14)
    length_short_penalty = -0.2
    length_long_penalty  = -0.4
    length_ideal_bonus   = 0.2

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"'{album.name}' doesn't belong in any scene I cover and I mean that as a statement of fact, not cruelty.",
                         f"The underground has seen a lot of bad records come through. '{album.name}' is one of the worse ones.",
                         f"'{album.name}' has zero cultural currency. I checked. I looked hard.",
                         f"'{album.name}' is the kind of record that makes scenes feel like wasted effort."],
            "mid_low":  [f"'{album.name}' is trying to be a scene record without understanding what the scene actually asks for.",
                         f"'{album.name}' is a record that would get polite nods at certain shows and nothing more.",
                         f"The scene deserves more than '{album.name}' is offering. It's a start and not a destination.",
                         f"'{album.name}' has the right references and not enough of the right reasons."],
            "mid_high": [f"'{album.name}' earns its place in the conversation — I'd put it on in the right spaces and not regret it.",
                         f"'{album.name}' has the cultural awareness the scene demands and uses it well enough.",
                         f"'{album.name}' is the kind of record you champion quietly but without hesitation.",
                         f"'{album.name}' is culturally credible in a way that most of what I get sent isn't."],
            "high":     [f"'{album.name}' is a scene record in the most complete sense — it knows what it is, where it comes from, and exactly who it's for.",
                         f"'{album.name}' is going to matter. Not next week — over time. The right people will hold this one.",
                         f"The scene was waiting for a record like '{album.name}' and here it is.",
                         f"'{album.name}' is the record I'll be putting on at every show I can until something better comes along."],
            "perfect":  [f"'{album.name}' is the record. The underground will still be playing this in five years.",
                         f"'{album.name}' is what we build scenes for — music that doesn't ask permission and doesn't need to.",
                         f"'{album.name}' is a landmark. That's not a word I use. I'm using it now."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["Pure identity. Consistently nothing to show for it.", "Fully committed to one sound. The sound has nothing to say."],
                "mid_low":  ["The identity is locked in. It's just not a strong enough identity to carry an album.", "The genre is consistent. The material underneath isn't strong enough."],
                "mid_high": ["Pure genre from front to back. The scene respects that kind of commitment.", "No genre drift. The identity is complete and unapologetic. That's the standard."],
                "high":     ["Fully locked in. No confusion about what this record is.", "The scene can hear the commitment and it earns it."],
                "perfect":  ["Perfect genre coherence — the album sounds like one complete cultural statement.", "The identity is total and the album is better for it."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      [f"The {off} genre departure{'s' if off>1 else ''} are the most interesting parts of an album that needed more of them.", "The small detours show more ambition than the core delivers."],
                "mid_low":  ["The small genre excursions add more than the core provides — the album needed more of what the detours offer.", "The {off} departures are where the album actually shows something."],
                "mid_high": [f"Mostly locked with {off} informed detour{'s' if off>1 else ''} — the kind of experimentation the scene reads as confident.",
                              f"The core is intact and the {off} departure{'s' if off>1 else ''} feel like creative choice rather than direction loss."],
                "high":     ["The small genre diversions show range rather than confusion. The scene can tell the difference.", "The departures are controlled confidence — the album earns both the core and the stretch."],
                "perfect":  ["The minor genre excursions are the album's most elegant structural moments — confidence made audible.", "The {off} small departures add to a record that doesn't need additions but benefits from them."],
            }
        else:
            pool = {
                "low":      [f"The genre incoherence at {off} tracks is one more reason this album doesn't work.", f"{off} off-genre tracks in an album that was already lost."],
                "mid_low":  [f"{off} off-genre tracks is too many for the scene to read as intentional — it reads as undecided.",
                              "The genre inconsistency creates a cultural confusion the album never resolves."],
                "mid_high": [f"The {off} off-genre tracks dilute an album that could have been a stronger statement with more focus.",
                              "The genre incoherence is the one thing I'd change — the scene wants to know what you are."],
                "high":     [f"The {off} departures are my one complaint about an otherwise culturally credible record.", "The genre inconsistency is the album's structural weak point in an otherwise strong listen."],
                "perfect":  [f"The {off} genre diversions are the record's lone structural flaw — the album is strong enough to absorb them.", "The genre incoherence is barely a complaint against an album this complete."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The album flows consistently and consistently doesn't go anywhere worth following.", "Thematic coherence present. Still not culturally credible."],
                "mid_low":  ["The through-line is there — the material doesn't do enough with it.", "The album flows but the flow doesn't go anywhere especially interesting."],
                "mid_high": ["The album flows — not just sonically but thematically. Every transition was a decision.", "The through-line is real and the sequencing respects it. This is how you build a full listen."],
                "high":     ["The track ordering here is doing real cultural work and the scene will feel it.", "The thematic coherence earns the album's place as a statement rather than a collection."],
                "perfect":  ["The album flows like a complete cultural statement — the sequencing is part of the art.", "Perfect thematic flow. The album earns the full listen every time."],
            }
        elif state == "decent":
            pool = {
                "low":      ["The theme holds for part of it — the part where it holds isn't the part that works.", "Adequate thematic consistency for an inadequate record."],
                "mid_low":  ["The thematic focus slips enough that the scene notices, even if it doesn't completely break the listen.", "Some thematic wobble and the album doesn't fully recover from it."],
                "mid_high": ["The thematic coherence is enough to hold — the core is solid even where it drifts slightly.", "The flow is mostly there. The gaps are audible but not fatal."],
                "high":     ["The thematic consistency is one of the album's quieter cultural strengths.", "The gaps are small enough that the album's overall statement isn't undermined."],
                "perfect":  ["The small thematic gaps barely register against an album this strong.", "The through-line holds for almost all of it — the few gaps are the record's only concession to imperfection."],
            }
        else:
            pool = {
                "low":      ["No thematic logic. The album is a playlist with a title.", "The sequencing makes no cultural statement — it's random order with a cover."],
                "mid_low":  ["The album doesn't know what it's saying — the thematic drift undermines whatever cultural credibility it was building.", "No clear thematic through-line. The scene will hear that immediately."],
                "mid_high": ["The thematic logic is absent and the album's cultural statement is weakened because of it.", "The sequencing is the album's biggest structural problem. The scene wants to know what the record is saying."],
                "high":     ["The thematic incoherence is the one thing I can't forgive in an otherwise strong record.", "The sequencing logic is the album's one genuine failure."],
                "perfect":  ["The thematic drift is the record's only formal imperfection. The album overcomes it.", "The sequencing is the lone flaw in a landmark record."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low", "mid_high"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the record in miniature — every quality the album has at {'their' if multi else 'its'} most concentrated.",
                    f"{names} {'are' if multi else 'is'} the {'tracks' if multi else 'track'} the scene is going to know. {'These travel' if multi else 'This one travels'}.",
                    f"{names} {'are' if multi else 'is'} what the rest of the album is in service of. {'They earn' if multi else 'It earns'} that."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the album's best {'moments' if multi else 'moment'} in a record of uneven ones.",
                    f"{names} {'are' if multi else 'is'} where the album finds itself. It should have stayed there longer.",
                    f"{'These are' if multi else 'This is'} the {'tracks' if multi else 'track'} I'd put on to make someone understand what this album is going for."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} the one{'s' if multi else ''} I'd sequence differently — not a problem, just a missed opportunity.",
                    f"{names} {'are' if multi else 'is'} the album's most forgettable {'moments' if multi else 'moment'} in an otherwise memorable record."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} where the album loses its nerve. The scene notices when records lose their nerve.",
                    f"{names} {'disrupt' if multi else 'disrupts'} the album's cultural identity. The scene will skip {'them' if multi else 'it'}.",
                    f"{'These are' if multi else 'This is'} the concession {'tracks' if multi else 'track'} — {'the ones' if multi else 'the one'} that exist for an audience the rest of the record isn't playing for."]
        else:
            pool = [f"{names} {'have' if multi else 'has'} no business being on this record. {'They cost' if multi else 'It costs'} the album credibility it takes tracks to earn.",
                    f"{names} {'are' if multi else 'is'} inauthentic in a way the rest of the album isn't. That dissonance is heard.",
                    f"{names} {'signal' if multi else 'signals'} that the artist doesn't fully trust the audience they've been building. The scene will hear that."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"{n} tracks is lean for a statement record. The scene can absorb more.",
                         f"At {n} tracks the album feels like an EP that grew ambitious. It needed more room."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is one or two past where the scene's attention holds.",
                         f"The album's length at {n} tracks tests the patience the earlier half earns but the later half spends."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["scenes"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' is not a scene record. It's not trying to be and it shows.",
            "mid_low": f"'{album.name}' is doing something in the right direction. Not there yet.",
            "mid_high":f"'{album.name}' earns its place in the conversation.",
            "high":    f"'{album.name}' is a record the scene will hold onto.",
            "perfect": f"'{album.name}' is a landmark. The scene will still be playing it.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 7 — TOBIAS LUND (Casual, slightly generous)
# ═══════════════════════════════════════════════════════════════

class AlbumTobiasLund(AlbumCritic):
    personality          = "generous"
    cohesion_sensitivity = 0.7
    theme_sensitivity    = 0.6
    flow_sensitivity     = 0.7
    length_sensitivity   = 1.0

    length_preference    = (9, 14)
    length_short_penalty = -0.2
    length_long_penalty  = -0.4
    length_ideal_bonus   = 0.15

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"I genuinely tried to get through all of '{album.name}'. I got through most of it. That's the review.",
                         f"'{album.name}' didn't grab me and I gave it a real chance. The chance wasn't enough.",
                         f"'{album.name}' is not what I'm looking for in an album and I listened to enough of it to know that for certain.",
                         f"'{album.name}' is just not my thing — and I think I'm actually the right audience for this."],
            "mid_low":  [f"'{album.name}' is mostly fine and fine isn't really what I'm after in an album.",
                         f"'{album.name}' is the kind of album I have on in the background and occasionally look up for.",
                         f"I enjoyed parts of '{album.name}' but I don't think I'll come back to all of it.",
                         f"'{album.name}' has good moments and enough forgettable ones to balance them out."],
            "mid_high": [f"'{album.name}' is good. Like, actually good. I kept it on the whole way through and that's not nothing.",
                         f"'{album.name}' is the kind of album that goes on the rotation. That's what I'm looking for.",
                         f"I had a good time with '{album.name}'. The energy holds and the good moments outweigh the slow ones.",
                         f"'{album.name}' kept me engaged from start to finish and that's the whole ask."],
            "high":     [f"'{album.name}' is great and I mean that simply — I've had it on constantly and I'm not tired of it.",
                         f"'{album.name}' is one of those albums where you finish it and just start it again. That happened.",
                         f"'{album.name}' is genuinely excellent. I sent it to multiple people. They all got it immediately.",
                         f"'{album.name}' is an album I'm going to be playing for months. Already started."],
            "perfect":  [f"'{album.name}' is a perfect album. I don't have a complicated reason. It just is.",
                         f"I don't know how many times I've listened to '{album.name}'. A lot. That's the review.",
                         f"'{album.name}' is the record I didn't know I needed. Now I can't not have it."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["The whole album is one consistent sound and the sound just isn't doing it for me.", "Consistent from start to finish — consistently not landing."],
                "mid_low":  ["The album knows its genre and stays in it — I just wished the songs were stronger.", "Consistent identity. Limited results."],
                "mid_high": ["The whole album is one genre and it works as a complete thing — I could put it on front to back.", "The genre is consistent and it keeps the album feeling like an actual album."],
                "high":     ["Every track fits. The identity is clear and that makes the listening experience smooth.", "Fully consistent and fully earned — the album commits and wins."],
                "perfect":  ["Perfect genre coherence. This is what a complete album feels like.", "Every track on the same page. The whole thing flows because of it."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      ["The small genre detours are the most interesting parts of an album that needed more of them.", "The {off} departures add some life to an album that could have used more."],
                "mid_low":  ["The genre is pretty consistent — the album just needed more from the consistent parts.", "The detours are fine. The core needed to be stronger."],
                "mid_high": [f"Mostly one genre with a couple of small detours that don't derail anything.",
                              f"The genre diversity is there but not disorienting. The album keeps its identity."],
                "high":     ["The album's identity is clear and the small detours make it feel more alive.", f"The {off} genre {'departures are' if off>1 else 'departure is'} confident rather than confused. The album earns it."],
                "perfect":  ["The small genre excursions are the album at its most confident. They add without taking away.", "The identity is so secure that the small departures just make the album more fun."],
            }
        else:
            pool = {
                "low":      [f"The genre jumps around {off} times and it's hard to stay with the album when it keeps changing.", "The inconsistency is one more thing making this a tough listen."],
                "mid_low":  [f"The genre inconsistency is the one thing that stops this from being a front-to-back experience.",
                              f"{off} tracks feel like they're from a different record."],
                "mid_high": [f"The genre jumps around {off} times and I notice it — the album loses its thread.",
                              "The genre inconsistency is the one thing that stops this from being a front-to-back experience."],
                "high":     [f"The {off} genre departures are my only real complaint — the album would be an even better listen without them.",
                              "The genre inconsistency is the one thing keeping this from being a perfect experience."],
                "perfect":  [f"The {off} off-genre moments are the album's only flaw in an otherwise perfect listen.",
                              "The genre diversions are barely noticeable against everything the album gets right."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The album flows well. Flowing well is the best thing about it.", "The sequencing is the album's strongest quality — which tells you something."],
                "mid_low":  ["The album flows with a clear through-line — I just wished more of the songs were at the level of the flow.", "The theme holds consistently. The material doesn't always match that consistency."],
                "mid_high": ["The album flows really well — the theme holds throughout and the track order makes sense.",
                              "Start to finish this is a smooth listen. The thematic consistency is a big part of why."],
                "high":     ["The sequencing is one of the album's strongest qualities — it's a front-to-back listen and I've done it front to back.",
                              "The flow from track to track makes this feel complete. That's hard to get right and this gets it right."],
                "perfect":  ["Perfect sequencing. The album is a journey from first track to last and I didn't want it to end.",
                              "The thematic flow is the album's invisible architecture. You feel it without naming it."],
            }
        elif state == "decent":
            pool = {
                "low":      ["The theme holds for part of it — the part where it holds isn't the memorable part.", "Adequate flow for an album that needed more than adequate flow."],
                "mid_low":  ["The flow is mostly there with some tonal detours that catch you off guard.", "Mostly flows well. A few moments where the mood shift feels abrupt."],
                "mid_high": ["The theme is mostly consistent — a few moments where the mood shift catches you off guard but nothing that breaks the listen.",
                              "Mostly flows well. A few tonal detours but nothing that completely breaks the experience."],
                "high":     ["The thematic consistency is solid with a few small bumps — they're manageable and the album earns the full listen despite them.",
                              "The flow is mostly smooth. The few rough patches barely register against the album's overall quality."],
                "perfect":  ["The small thematic gaps barely matter in an album this good.", "The flow is almost perfect — the few rough spots are the record's only concession to imperfection."],
            }
        else:
            pool = {
                "low":      ["The album jumps around too much — it's hard to relax into.", "It feels like a playlist someone organized quickly rather than an album."],
                "mid_low":  ["The album jumps around a lot thematically and I feel those gaps as a listener.",
                              "It feels less like an album with a journey and more like a random playlist."],
                "mid_high": ["The track ordering is the weakest part for me. The tonal shifts make it hard to relax into the album.",
                              "The album doesn't flow as well as it should — the thematic inconsistency is the listener's problem."],
                "high":     ["The thematic inconsistency is my one real complaint — the album is strong enough to survive it but the full listen would be even better with more cohesion.",
                              "The sequencing is the one area the album doesn't match its own quality."],
                "perfect":  ["The flow is the album's one weakness and it barely registers against everything it gets right.",
                              "The thematic drift is the record's only flaw — the album is too good for it to matter much."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the one{'s' if multi else ''} I've played the most by a long way.",
                    f"{names} {'are' if multi else 'is'} the standout{'s' if multi else ''} — genuinely some of the best {'songs' if multi else 'a song'} I've heard recently.",
                    f"{'These tracks alone' if multi else 'This track alone'} — {names} — made this whole album worth listening to."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the album's best {'moments' if multi else 'moment'} and I've gone back to {'them' if multi else 'it'} a few times.",
                    f"{names} {'are' if multi else 'is'} where the album peaks — the {'tracks' if multi else 'track'} I'd play first for someone else.",
                    f"The high {'points are' if multi else 'point is'} {names} and {'they\'re' if multi else 'it\'s'} a genuinely good high {'points' if multi else 'point'}."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} the one{'s' if multi else ''} I occasionally skip. Not a problem — just my personal preference.",
                    f"{names} {'are' if multi else 'is'} the brief dip{'s' if multi else ''}. Every album has one and {'these are' if multi else 'this is'} manageable."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} where I check my phone. Not bad enough to skip but not holding me.",
                    f"{names} {'are' if multi else 'is'} the flat {'spots' if multi else 'spot'} in what's otherwise a pretty engaging listen.",
                    f"{names} {'are' if multi else 'is'} a skip for me. The album's good enough that I don't mind losing {'some tracks' if multi else 'a track'}."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} a skip every time. {'They break' if multi else 'It breaks'} the momentum the album is trying to build.",
                    f"{names} {'are' if multi else 'is'} the album's one real problem. {'They don\'t' if multi else 'It doesn\'t'} fit and I notice every time.",
                    f"{names} {'are' if multi else 'is'} not what the rest of the album is. {'They stand' if multi else 'It stands'} out in the wrong way."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks it ends too soon — I was still in it when it finished.",
                         f"{n} tracks isn't quite enough. I wanted more."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is a bit much — some of the later ones feel like bonus content.",
                         f"It goes on a little long at {n} tracks. A tighter version of this album would hit harder."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["casual"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' isn't for me and that's fine.",
            "mid_low": f"'{album.name}' has its moments but not enough of them.",
            "mid_high":f"'{album.name}' is a solid record and I'll keep coming back to it.",
            "high":    f"'{album.name}' is one of my favourites of the year, easy.",
            "perfect": f"'{album.name}' is perfect. Simple as that.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 8 — NINA PASCAL (Balanced, measured)
# ═══════════════════════════════════════════════════════════════

class AlbumNinaPascal(AlbumCritic):
    personality          = "balanced"
    cohesion_sensitivity = 1.0
    theme_sensitivity    = 1.0
    flow_sensitivity     = 1.1
    length_sensitivity   = 1.0

    length_preference    = (9, 14)
    length_short_penalty = -0.3
    length_long_penalty  = -0.3
    length_ideal_bonus   = 0.2

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"'{album.name}' is a record that fails at most of what it attempts — and attempts enough that the failure is hard to overlook.",
                         f"'{album.name}' is underdeveloped across its tracklist in ways that aren't isolated problems — they're structural ones.",
                         f"'{album.name}' shows ambition and a consistent inability to match it with execution.",
                         f"'{album.name}' is a record that knows what it wants to be and consistently falls short of it."],
            "mid_low":  [f"'{album.name}' is a decent album with the skeleton of a good one inside it — the execution didn't fully extract the best version.",
                         f"'{album.name}' occupies a frustrating middle ground: good enough to suggest the potential, not good enough to fully realize it.",
                         f"'{album.name}' is worth hearing once. Whether it's worth returning to is a harder case to make.",
                         f"'{album.name}' is a partial success — the parts that work are real, and the parts that don't are just as real."],
            "mid_high": [f"'{album.name}' is a well-constructed record — the craft is real, the intention is clear, and it mostly does what it sets out to do.",
                         f"'{album.name}' earns its place — consistently engaged, occasionally exceptional, and almost never lazy.",
                         f"'{album.name}' is the kind of album that rewards attention. The detail is there if you're looking for it.",
                         f"'{album.name}' is a serious and honest record — it doesn't overreach and it doesn't underdeliver."],
            "high":     [f"'{album.name}' is a serious piece of work that succeeds in nearly every dimension it attempts.",
                         f"'{album.name}' is exceptional — not in isolated moments but as a complete structural achievement.",
                         f"'{album.name}' is the kind of album that raises the standard for everything made in this space this year.",
                         f"'{album.name}' is a complete artistic statement and it earns that description honestly."],
            "perfect":  [f"'{album.name}' is a perfect album. I've evaluated thousands of records. I don't use the word 'perfect' carelessly.",
                         f"'{album.name}' achieves total formal and emotional coherence. That is an extremely rare thing and it happened here.",
                         f"'{album.name}' is a complete and flawless record. My job is to say so clearly, and I am."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["The genre cohesion is total — and the total genre commitment is applied to material that doesn't honor it.", "Formally coherent, creatively underdeveloped."],
                "mid_low":  ["The genre identity holds throughout — the identity is present even if the material inside it is uneven.", "The structural coherence is the album's strongest quality, which is a limitation."],
                "mid_high": ["The genre cohesion is total — every track functions within the framework with clear artistic intention.",
                              "The genre commitment is sustained across the full tracklist. That consistency is a structural asset."],
                "high":     ["Genre coherence is one of the album's formal strengths — the identity never wavers and never becomes monotonous.",
                              "The genre commitment is sustained and the sustaining is purposeful — it's structure in service of meaning."],
                "perfect":  ["The genre coherence is total and the album transcends it — the form serves the content completely.",
                              "The identity is absolute and the album makes that identity necessary. Rare."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      [f"The {off} genre departure{'s' if off>1 else ''} are fine in a record that needed more than fine elsewhere.", "The small diversions are the most alive the album gets."],
                "mid_low":  ["The genre consistency is strong — the small departures don't help or hurt much in a record this uneven.", "Minor genre variance that neither saves nor damages an album with other problems."],
                "mid_high": [f"The genre consistency is strong — {off} off-genre track{'s' if off>1 else ''} register as considered risk rather than directional uncertainty.",
                              "The genre architecture is sound. Minor variance from the base is handled with sufficient intention."],
                "high":     [f"The {off} departure{'s' if off>1 else ''} read as deliberate expansion rather than confusion — the core is secure enough to make them work.",
                              "The genre identity holds throughout and the small excursions only strengthen the overall sense of artistic control."],
                "perfect":  [f"The small genre excursions are compositionally elegant — acts of confident range in a record that has earned the right to range.",
                              "The {off} formal departures are the album's most precise structural gestures."],
            }
        else:
            pool = {
                "low":      [f"The {off} off-genre tracks represent a real structural challenge in a record with little structural reserve.",
                              "The genre incoherence fragments what's already a fragmented record."],
                "mid_low":  [f"Genre inconsistency across {off} tracks is the album's most significant formal problem — it fragments what might otherwise be a coherent statement.",
                              f"The {album.core_genre if hasattr(album,'core_genre') else 'core'} identity is present but contested by too many departures."],
                "mid_high": [f"The {off} off-genre tracks represent a real structural challenge. The core identity is present but contested.",
                              "The genre incoherence is the album's one significant formal failure."],
                "high":     [f"The {off} genre departures are my one complaint about a record I otherwise consider exceptional.",
                              "The genre inconsistency is the album's structural concession in what is otherwise a complete work."],
                "perfect":  [f"The {off} departures are the record's only structural imperfection — remarkable that the album is still this complete.",
                              "The genre diversions are the lone formal flaw in a masterpiece."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The thematic architecture is one of the album's structural virtues — applied to material that doesn't match it.", "The sequencing is the album's strongest quality and the album's strongest quality is its only strength."],
                "mid_low":  ["The thematic continuity is the album's best structural quality — the material inside it is uneven.", "The through-line holds even when the material it's threading is inconsistent."],
                "mid_high": ["The thematic architecture is one of the album's most underappreciated qualities — the through-line is real and the sequencing honors it.",
                              "The sequencing is doing real structural work — the album reads as an argument, not a collection."],
                "high":     ["The thematic coherence here is exceptional — the album builds, develops, and resolves with genuine formal intelligence.",
                              "The through-line holds at a level that distinguishes this record from the merely good albums it could have been."],
                "perfect":  ["The thematic architecture is total — every track is in its exact right place and every transition is earned.",
                              "The album is a complete formal statement. The structure makes that claim and the music honors it."],
            }
        elif state == "decent":
            pool = {
                "low":      ["Adequate thematic consistency for an album that needed more than adequate.", "The through-line holds for part of it — the part where it holds is unremarkable."],
                "mid_low":  ["The thematic continuity is adequate — the foundation holds even if it's occasionally tested.",
                              "The through-line is present without being complete. The gaps don't break the album but they're felt."],
                "mid_high": ["Thematic coherence is present without being complete — adequate but not exceptional.",
                              "The through-line holds across most of the record and the gaps are manageable."],
                "high":     ["The thematic consistency is one of the album's quieter formal strengths — present and purposeful across most of the tracklist.",
                              "The small thematic gaps are the album's one formal concession in an otherwise complete record."],
                "perfect":  ["The few thematic gaps barely register against the album's overall formal completeness.",
                              "The through-line dips occasionally but the album's strength more than compensates."],
            }
        else:
            pool = {
                "low":      ["The thematic incoherence is the album's most significant structural failure.", "The sequencing logic is absent and the album pays for it throughout."],
                "mid_low":  ["The thematic incoherence is the album's most significant formal weakness — the record lacks a coherent emotional through-line.",
                              "The album is structurally weakened by its thematic inconsistency throughout."],
                "mid_high": ["The thematic logic is absent and the album's formal argument is weakened because of it.",
                              "The sequencing is the album's central structural problem — the record deserved more editorial rigor."],
                "high":     ["The thematic inconsistency is the one significant structural flaw in what is otherwise an exceptional record.",
                              "The sequencing logic is the single area where this record doesn't match its own formal ambitions."],
                "perfect":  ["The thematic drift is the record's only formal imperfection — the album is too strong for it to matter, but I note it.",
                              "The sequencing is the lone weak point in a complete record."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low", "mid_high"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the record's {'centerpieces' if multi else 'centerpiece'} — the {'tracks' if multi else 'track'} that {'justify' if multi else 'justifies'} everything surrounding {'them' if multi else 'it'}.",
                    f"{names} {'are' if multi else 'is'} what the album is building toward and {'they arrive' if multi else 'it arrives'} there completely.",
                    f"{names} {'are' if multi else 'is'} exceptional and I don't use that word loosely. The album is worth hearing for {'these tracks' if multi else 'this track'} alone."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the album's strongest {'offerings' if multi else 'offering'} and {'demonstrate' if multi else 'demonstrates'} the upper limit of what the record can achieve.",
                    f"{names} {'are' if multi else 'is'} where the album fully realizes its potential.",
                    f"The best the album offers comes from {names}, and the best is genuinely good."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} where the album {'are' if multi else 'is'} at {'their' if multi else 'its'} least — still above average relative to most records.",
                    f"{names} {'are' if multi else 'is'} the album's softest {'moments' if multi else 'moment'} — small {'concessions' if multi else 'concession'} in an otherwise strong record."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} where the record's ambition and execution diverge most visibly.",
                    f"{names} {'are' if multi else 'is'} the album's weak {'links' if multi else 'link'} — not badly made, just not at the level of {'their' if multi else 'its'} surroundings.",
                    f"{names} {'are' if multi else 'is'} the {'ones' if multi else 'one'} I'd point to as missed {'opportunities' if multi else 'opportunity'} — the album would be tighter without {'them' if multi else 'it'}."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} {'real problems' if multi else 'a real problem'} — {'they don\'t' if multi else 'it doesn\'t'} belong in the company of the other tracks.",
                    f"{names} {'cost' if multi else 'costs'} the album structural credibility that the other tracks worked hard to build.",
                    f"{names} {'are' if multi else 'is'} where the album breaks down. {'They\'re' if multi else 'It\'s'} a genuine failure in an otherwise serious record."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks the album ends before it's fully arrived. It needed more room.",
                         f"{n} tracks is lean for the statement this album is attempting."])
        elif n > self.length_preference[1]:
            return pick([f"The album tests its welcome slightly at {n} tracks — a tighter edit would serve the stronger material better.",
                         f"{n} tracks is a few more than necessary. The best work would shine brighter with less surrounding it."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["contrarian"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' doesn't reach the standard I'd apply to a recommendation.",
            "mid_low": f"'{album.name}' is a partial success — worth noting for what it gets right.",
            "mid_high":f"'{album.name}' is a solid record and a genuine one.",
            "high":    f"'{album.name}' is excellent and deserves to be heard.",
            "perfect": f"'{album.name}' is perfect. That's my final word.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 9 — TEENA NARUKA (Harsh, Shatam Rai obsessed)
# ═══════════════════════════════════════════════════════════════

class AlbumTeenaNaruka(AlbumCritic):
    personality          = "strict"
    cohesion_sensitivity = 1.2
    theme_sensitivity    = 1.1
    flow_sensitivity     = 1.3
    length_sensitivity   = 1.0

    length_preference    = (9, 15)
    length_short_penalty = -0.1
    length_long_penalty  = -0.2
    length_ideal_bonus   = 0.25

    SHATAM_REFS = [
        "Shatam Rai is still the GOAT though, just saying.",
        "I kept thinking about Shatam Rai the whole time.",
        "Shatam Rai would have thoughts about this. I've already texted them.",
        "Anyway I love Shatam Rai. That's still true regardless of this album.",
        "Shatam Rai remains undefeated as a baseline.",
        "Go listen to Shatam Rai after this. Or before. Or instead.",
        "Shatam Rai could have made this better. Shatam Rai can make everything better.",
        "This reminded me of Shatam Rai in the best possible way.",
        "I added this to my Shatam Rai adjacent playlist.",
        "Shatam Rai approved this before I even hit play.",
        "I'm going to tell Shatam Rai about this immediately.",
        "Nothing hits different after hearing Shatam Rai, and this is no exception.",
    ]

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"Okay so '{album.name}' is rough. Shatam Rai wouldn't give this the time of day.",
                         f"'{album.name}' didn't hit for me and I really wanted it to.",
                         f"I gave '{album.name}' a full honest listen. It didn't earn it.",
                         f"'{album.name}' is not it. I've said it once and I don't need to say it again."],
            "mid_low":  [f"'{album.name}' is fine? It's fine. It's not memorable but it's fine.",
                         f"'{album.name}' tries and gets about halfway there. Halfway is something.",
                         f"'{album.name}' has its moments and I genuinely enjoyed some of them. Some.",
                         f"'{album.name}' is the kind of album that occupies time without filling it."],
            "mid_high": [f"Okay '{album.name}' is actually pretty good. Not Shatam Rai good but like, actually good.",
                         f"'{album.name}' kept me listening all the way through and that is a genuine compliment.",
                         f"'{album.name}' is solid! I was into it. More than I expected.",
                         f"'{album.name}' earned my attention. That's harder than it sounds."],
            "high":     [f"'{album.name}' is really good and I've been saying that to everyone I know.",
                         f"I've been playing '{album.name}' constantly. My friends have noticed.",
                         f"'{album.name}' hit different. Real talk — this is one of the better albums I've heard recently.",
                         f"'{album.name}' is the album that's been living in my head rent-free for days."],
            "perfect":  [f"'{album.name}' is a perfect album. I'm saying that clearly and I mean it.",
                         f"'{album.name}' is in the Shatam Rai tier. I have never said that about any album. I'm saying it now.",
                         f"'{album.name}' is the best album I've heard in a very long time and I'm not calm about it."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["The whole album is one sound and that one sound isn't doing anything for me.", "Consistent from front to back. Consistently not landing."],
                "mid_low":  ["The album knows its sound and stays in it — I just wished the sound was stronger.", "Consistent. Consistently okay."],
                "mid_high": ["The whole album is one genre and it flows perfectly because of that. Love when an album knows what it is.",
                              "Zero genre drift — the identity is consistent and it makes the album feel intentional."],
                "high":     ["Full commitment and it earns that commitment completely.", "The album knows what it is, never wavers, and wins because of it."],
                "perfect":  ["Perfect identity. Held the whole album. A complete statement.", "The coherence is total and the total coherence is earned."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      ["The small detours are more interesting than the rest of the album, which is a problem.", "The {off} side trips are the album trying to be better than it is."],
                "mid_low":  [f"Mostly one sound with {off} little detour{'s' if off>1 else ''} that don't break anything but don't save anything either.", "Minor drift. Album survives. Just barely."],
                "mid_high": [f"Mostly one thing with {off} little detour{'s' if off>1 else ''} that actually add something.",
                              f"The core is intact even with {off} side trip{'s' if off>1 else ''}. The album survives it well."],
                "high":     [f"The {off} genre departure{'s' if off>1 else ''} actually add something — confident choices in an album that earns them.",
                              "The small detours make the album feel more alive. They're the right kind of risk."],
                "perfect":  ["The tiny genre diversions are the album at its most confident. Part of why it's a complete listen.", "The small departures are acts of confidence in an album full of them."],
            }
        else:
            pool = {
                "low":      [f"{off} tracks step outside the main sound and the album loses something each time — something it couldn't afford to lose.", "Genre confusion on top of everything else not working."],
                "mid_low":  [f"The genre inconsistency over {off} tracks is the one thing I keep coming back to as a problem.",
                              f"The main identity gets fuzzy {off} times. I noticed every time."],
                "mid_high": [f"The {off} genre departures dilute an album that needed more focus to be a complete statement.",
                              "The genre inconsistency is the album's main structural weakness."],
                "high":     [f"The {off} off-genre moments are my one complaint in an otherwise strong album.",
                              "The genre inconsistency barely holds back an album this good — but it does hold it back slightly."],
                "perfect":  [f"The {off} genre diversions are the album's lone imperfection. The record is strong enough to absorb them.",
                              "The only thing keeping this from being structurally perfect is the genre drift. Minor complaint."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The album flows with a clear through-line through a record that doesn't deserve one.", "Thematic consistency present. Still not good."],
                "mid_low":  ["The theme holds and the songs underneath it are unevenly good.", "The album flows. The flow is the best part."],
                "mid_high": ["The theme runs the whole album and the sequencing respects it. This is how you build a full listen.",
                              "Thematically consistent and the track order makes emotional sense. The album flows."],
                "high":     ["The album flows beautifully. Every track feels like it was made to be next to its neighbors.",
                              "The thematic consistency is one of the album's real strengths — it makes the whole listen feel inevitable."],
                "perfect":  ["Perfect thematic flow. The album is a journey and I didn't want it to end.", "The sequencing is so good it feels like the album was born in this order."],
            }
        elif state == "decent":
            pool = {
                "low":      ["The theme holds for part of it and the part it holds is where the album stops trying.", "Adequate flow for an album that needed better than adequate."],
                "mid_low":  ["Some thematic inconsistency but not enough to break the experience. Barely.", "The theme holds for most of it. The rest drifts."],
                "mid_high": ["The theme holds for most of it and the rest is manageable drift. Good enough.",
                              "The album drifts from the main theme occasionally but recovers."],
                "high":     ["The thematic consistency is mostly solid and the small gaps barely register.",
                              "The theme holds for almost all of it and the album is better for that."],
                "perfect":  ["Small thematic gaps. The album is too strong for them to matter.", "The few rough sequencing spots are barely noticeable against the album's overall quality."],
            }
        else:
            pool = {
                "low":      ["Only the thematic logic isn't there. The album jumps around and I feel every jump.", "No real thematic through-line. Just songs next to each other."],
                "mid_low":  ["Only a fraction of the album is thematically consistent — the album jumps around and I feel it during the listen.",
                              "The thematic drift is real and the album suffers for it."],
                "mid_high": ["The thematic logic isn't quite there and the album suffers for it.",
                              "The sequencing is the one thing that keeps this from being a better album."],
                "high":     ["The thematic inconsistency is my one complaint about a record I'm otherwise in love with.",
                              "The sequencing is the album's one structural failure. Still an excellent album."],
                "perfect":  ["The thematic drift is the album's only flaw. Irrelevant against everything else it does.", "The one sequencing problem in an otherwise perfect record."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low", "mid_high"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the {'standouts' if multi else 'standout'} and {'it\'s' if not multi else 'they\'re'} not even close — {'those tracks are' if multi else 'that track is'} the reason I'll still be playing this album next year.",
                    f"{'These are' if multi else 'This is'} the {'moments' if multi else 'moment'} I texted people. Best {'things' if multi else 'thing'} here by a significant margin.",
                    f"{names} alone {'make' if multi else 'makes'} the whole album worth it."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the best the album offers and {'they\'re' if multi else 'it\'s'} a genuinely good best.",
                    f"{names} {'are' if multi else 'is'} the {'tracks' if multi else 'track'} I keep coming back to — the album's {'peaks' if multi else 'peak'}.",
                    f"The high {'points are' if multi else 'point is'} {names} and {'they\'re' if multi else 'it\'s'} a real high {'points' if multi else 'point'}."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} the one{'s' if multi else ''} I skip sometimes. Minor complaint for a strong album.",
                    f"{names} {'dip' if multi else 'dips'} a little. The album doesn't notice.",
                    f"{names} {'are' if multi else 'is'} the weakest {'tracks' if multi else 'track'} which in this context just means the nine instead of the ten."]
        elif album_score >= 5:
            pool = [f"{names} {'don\'t' if multi else 'doesn\'t'} hit the way the rest does. {'They\'re' if multi else 'It\'s'} the album's speed {'bumps' if multi else 'bump'}.",
                    f"{names} {'are' if multi else 'is'} fine but {'they\'re' if multi else 'it\'s'} not what the surrounding tracks are. The gap is noticeable.",
                    f"{names} {'are' if multi else 'is'} the one{'s' if multi else ''} Shatam Rai would probably skip. I sometimes do."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} not good and {'they\'re' if multi else 'it\'s'} on an otherwise okay album which makes it worse somehow.",
                    f"{names} {'are' if multi else 'is'} the {'mistakes' if multi else 'mistake'}. Every album can have one but {'these' if multi else 'this'} cost{'s' if not multi else ''} real momentum.",
                    f"{names} shouldn't be here. I said it. Someone had to."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks I wanted more. The album just got going.",
                         f"{n} tracks ends too soon. This album had more to give."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is a lot. A few could have been cut.",
                         f"The album goes on for {n} tracks and about two of those are filler. Cut them next time."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["teena"].get(int(round(score)), ["it is what it is."]))
        shatam = pick(self.SHATAM_REFS)
        remarks = {
            "low":     f"'{album.name}' wasn't for me.",
            "mid_low": f"'{album.name}' is okay. Not great. Okay.",
            "mid_high":f"'{album.name}' is genuinely worth your time.",
            "high":    f"'{album.name}' is a great record and I'll defend that.",
            "perfect": f"'{album.name}' is perfect. I'll be talking about this forever.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)} {shatam}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 10 — SHATAM RAI (Teena Naruka obsessed)
# ═══════════════════════════════════════════════════════════════

class AlbumShatamRai(AlbumCritic):
    personality          = "balanced"
    cohesion_sensitivity = 1.0
    theme_sensitivity    = 1.0
    flow_sensitivity     = 1.0
    length_sensitivity   = 1.0

    length_preference    = (9, 14)
    length_short_penalty = -0.2
    length_long_penalty  = -0.25
    length_ideal_bonus   = 0.2

    TEENA_REFS = [
        "I'm calling Teena Naruka after I file this.",
        "Teena Naruka and I will be discussing this record for weeks.",
        "Teena Naruka already knew about this album. She always knows first.",
        "Teena Naruka is going to lose it when she hears this.",
        "I need Teena Naruka's take on this immediately.",
        "Teena Naruka was right about this artist. She usually is.",
        "I've already sent this to Teena Naruka. Waiting on her response.",
        "Teena Naruka and I gave this the same score independently. The universe is communicating.",
        "I'm going to play this for Teena Naruka the second I see her.",
        "Teena Naruka knew. Of course she knew.",
    ]

    def _opening(self, album, score, tier):
        lines = {
            "low":      [f"'{album.name}' is a difficult listen and not in the rewarding kind of way.",
                         f"'{album.name}' didn't reach me and I kept the door open for most of the runtime.",
                         f"'{album.name}' is below the standard I apply to records I want to talk about.",
                         f"'{album.name}' tries. It doesn't arrive."],
            "mid_low":  [f"'{album.name}' is a record with ideas that don't fully materialize. It's an almost-album.",
                         f"'{album.name}' is better than its weakest moments and worse than its best ones — the average lands somewhere in the middle.",
                         f"'{album.name}' is a decent record that could have been a great one with more time or more decisions.",
                         f"'{album.name}' is worth a listen, one time, to find the moments that justify the rest."],
            "mid_high": [f"'{album.name}' is a well-made record that earns its place in the conversation.",
                         f"'{album.name}' does enough of the right things right to be worth someone's time.",
                         f"'{album.name}' is a real record — committed, considered, and mostly successful.",
                         f"'{album.name}' is a record I've been glad to spend time with."],
            "high":     [f"'{album.name}' is genuinely excellent and I've been looking for a way to say that more precisely. I can't — it's just excellent.",
                         f"'{album.name}' is the kind of record that makes me want to go back to the beginning before I've finished it.",
                         f"'{album.name}' is one of the stronger records I've reviewed this year. That's the honest assessment.",
                         f"'{album.name}' is the album I keep returning to without meaning to. That's the whole review."],
            "perfect":  [f"'{album.name}' is a perfect album. I'm stating that formally and without hesitation.",
                         f"'{album.name}' is everything a record is supposed to be. Complete.",
                         f"'{album.name}' is the album I'll be referencing when I talk about this era. That's what a perfect record does."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier, ded_genre):
        state = _cohesion_label(off)
        if state == "pure":
            pool = {
                "low":      ["The genre commitment is complete — and completely unrewarding.", "Full genre identity. The identity doesn't deliver."],
                "mid_low":  ["The genre commitment is consistent — the consistency is applied to uneven material.", "The album knows its identity. The identity is unevenly realized."],
                "mid_high": ["The genre commitment is complete — the album sounds like a single unified statement from first track to last.",
                              "No genre confusion. The framework holds from front to back and the album is stronger for it."],
                "high":     ["Total genre coherence. The album sounds like a complete and intentional thing.",
                              "The genre identity is the album's structural backbone — it holds everything together."],
                "perfect":  ["The genre coherence is total and the album is better for it in every way.",
                              "Complete, unified, and formally coherent. The album earns its identity."],
            }
        elif state == "minor_drift":
            pool = {
                "low":      [f"The {off} departure{'s' if off>1 else ''} add life to an album that needed more of it.", "The small excursions are the album's more interesting moments."],
                "mid_low":  [f"The {off} off-genre track{'s' if off>1 else ''} work as breathing room — the core is uneven but the departures add something.", "Minor genre excursions that add texture without threatening the overall identity."],
                "mid_high": [f"The {off} off-genre track{'s' if off>1 else ''} work as breathing room. The album's identity is never in doubt.",
                              f"Minor genre excursions that feel intentional. The foundation is secure."],
                "high":     [f"The {off} departure{'s' if off>1 else ''} add texture to a record that doesn't need it but benefits from it.",
                              "The small excursions are acts of confidence in an album that earns them."],
                "perfect":  ["The small genre departures are the album's most elegant structural gestures.",
                              "The minor formal diversions add to a record that was already complete without them."],
            }
        else:
            pool = {
                "low":      [f"The genre drift at {off} tracks is a structural problem on an album with structural problems to spare.", f"{off} off-genre tracks compound the record's other difficulties."],
                "mid_low":  [f"The genre drift at {off} tracks is a structural problem — the identity is present but not dominant.",
                              f"{off} off-genre tracks fragment the album in ways that are hard to read as experimentation."],
                "mid_high": [f"The {off} off-genre tracks leave the album without a secure identity in places.",
                              f"The cohesion issue is real — {off} departures is too many for a completely unified listen."],
                "high":     [f"The {off} departures from the core identity are my one structural complaint.",
                              "The genre incoherence is the album's lone formal weakness in what is otherwise a strong record."],
                "perfect":  [f"The {off} off-genre moments are the record's only formal imperfection — the album is complete despite them.",
                              "The genre drift barely matters against an album this strong."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        return pick(tier_pool)

    def _continuity(self, album, ratio, flow_mod, tier, ded_theme, clash):
        state = _continuity_label(ratio, flow_mod)
        clash_line = None
        if clash:
            _, _, clash_line = clash

        if state == "strong":
            pool = {
                "low":      ["The thematic through-line runs through a record that doesn't earn the structure it's given.", "The sequencing is better than the album deserves."],
                "mid_low":  ["The through-line holds and the material it holds is unevenly good.", "The album flows with more intention than the songs fully justify."],
                "mid_high": ["The through-line holds and the sequencing works with rather than against it — the album genuinely flows.",
                              "The album reads as a complete emotional statement rather than a collection of songs."],
                "high":     ["The thematic coherence is one of the album's real strengths — it makes the whole thing feel like a single sustained thought.",
                              "The sequencing is doing real work here and the album is better for it."],
                "perfect":  ["The album flows like a complete work. The sequencing earned that description.",
                              "The through-line is total and the album is a complete formal statement because of it."],
            }
        elif state == "decent":
            pool = {
                "low":      ["The through-line holds for part of the album — the part where it holds is unremarkable.", "Adequate thematic consistency."],
                "mid_low":  ["The thematic coherence is adequate — the foundation holds even if it's occasionally tested.",
                              "The gaps in the thematic through-line are felt but don't break the listen."],
                "mid_high": ["The thematic coherence is present without being complete — the gaps don't break the album but they're felt.",
                              "The through-line holds for most of the record and the small gaps are manageable."],
                "high":     ["The thematic consistency is one of the album's quieter strengths — mostly solid.",
                              "The few thematic gaps barely register against the album's overall quality."],
                "perfect":  ["The small thematic gaps are the record's only concession to imperfection.",
                              "The through-line dips occasionally and the album is strong enough not to care."],
            }
        else:
            pool = {
                "low":      ["The thematic incoherence is the album's most significant structural failure.", "No coherent through-line. Just songs."],
                "mid_low":  ["The thematic incoherence is a real structural problem — the album doesn't read as a complete statement.",
                              "The through-line is missing for too much of the album."],
                "mid_high": ["The thematic logic is absent and the album's coherence suffers for it.",
                              "The sequencing is the one structural failure in what is otherwise a capable record."],
                "high":     ["The thematic inconsistency is my one complaint about an excellent record.",
                              "The sequencing logic is the album's lone formal weakness."],
                "perfect":  ["The thematic drift is the record's only imperfection. The record transcends it.",
                              "The sequencing logic is the sole flaw in a complete album."],
            }
        tier_pool = pool.get(tier, pool.get("mid_high", []))
        base_line = pick(tier_pool)
        if clash_line and tier in ("low", "mid_low", "mid_high"):
            return base_line + " " + clash_line.capitalize() + "."
        return base_line

    def _praise_best(self, top_songs, album_score):
        names = format_song_list(top_songs)
        multi = len(top_songs) > 1
        best_score = top_songs[0][1] if top_songs else 0
        bs_tier = score_tier(best_score)

        if bs_tier in ("high", "perfect"):
            pool = [f"{names} {'are' if multi else 'is'} the record's {'centerpieces' if multi else 'centerpiece'} — the {'tracks' if multi else 'track'} that {'justify' if multi else 'justifies'} everything surrounding {'them' if multi else 'it'}.",
                    f"{names} {'are' if multi else 'is'} what the album is building toward, and {'they arrive' if multi else 'it arrives'} there completely.",
                    f"{names} {'are' if multi else 'is'} exceptional — the album is worth hearing for {'these tracks' if multi else 'this track'} alone."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} the album's strongest {'offerings' if multi else 'offering'} and demonstrate what the record achieves at its best.",
                    f"{names} {'are' if multi else 'is'} the high {'points' if multi else 'point'} — where the album's qualities are most concentrated.",
                    f"The album's best case is made on {names}."]
        return pick(pool)

    def _critique_worst(self, bot_songs, album_score):
        names = format_song_list(bot_songs)
        multi = len(bot_songs) > 1
        bot_score = bot_songs[0][1] if bot_songs else 0

        if album_score >= 8:
            pool = [f"{names} {'are' if multi else 'is'} where the album {'give' if multi else 'gives'} the least — still considerable in context.",
                    f"{names} {'are' if multi else 'is'} the album's softest {'moments' if multi else 'moment'} in a record this strong — a small concession."]
        elif album_score >= 5:
            pool = [f"{names} {'are' if multi else 'is'} where the record's ambition and execution diverge most visibly.",
                    f"{names} {'are' if multi else 'is'} the album's weak {'links' if multi else 'link'} — not badly made, just not at the level of the surroundings.",
                    f"{names} {'are' if multi else 'is'} the one{'s' if multi else ''} I'd point to as missed {'opportunities' if multi else 'opportunity'}."]
        else:
            pool = [f"{names} {'are' if multi else 'is'} a real {'problems' if multi else 'problem'} — {'they' if multi else 'it'} shouldn't be here and {'their' if multi else 'its'} presence costs the album.",
                    f"{names} {'are' if multi else 'is'} where the album loses its claim to being fully realized.",
                    f"{names} {'are' if multi else 'is'} the album's most significant {'missteps' if multi else 'misstep'}."]
        return pick(pool)

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks the album ends before it's fully said what it has to say.",
                         f"{n} tracks is lean — the material needed more room."])
        elif n > self.length_preference[1]:
            return pick([f"The album tests its welcome slightly at {n} tracks.",
                         f"{n} tracks is a few more than the material needs."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["shatam"].get(int(round(score)), ["it is what it is."]))
        teena = pick(self.TEENA_REFS)
        remarks = {
            "low":     f"'{album.name}' doesn't reach the standard I'd apply to a recommendation.",
            "mid_low": f"'{album.name}' is a partial success and partial successes are worth noting for what they get right.",
            "mid_high":f"'{album.name}' is a solid record and a genuine one.",
            "high":    f"'{album.name}' is excellent and deserves to be heard.",
            "perfect": f"'{album.name}' is perfect. That's my final word.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)} {teena}"


# ─────────────────────────────────────────────
#  ALBUM SIMULATION
# ─────────────────────────────────────────────

class AlbumSimulation:
    def __init__(self):
        song_critics = [
            MarcusVane(), DejaHayes(), VicOsei(), RayColdwell(),
            EarlMosely(), ZaraNights(), TobiasLund(), NinaPascal(),
            TeenaNaruka(), ShatamRai(),
        ]
        album_wrappers = [
            AlbumMarcusVane, AlbumDejaHayes, AlbumVicOsei, AlbumRayColdwell,
            AlbumEarlMosely, AlbumZaraNights, AlbumTobiasLund, AlbumNinaPascal,
            AlbumTeenaNaruka, AlbumShatamRai,
        ]
        self.album_critics = [
            wrapper(song_critic)
            for wrapper, song_critic in zip(album_wrappers, song_critics)
        ]

    def publish_album(self, album):
        _print_box(f"  ALBUM REVIEWS: '{album.name}'  ")
        meta = (f"{album.song_count()} tracks  |  "
                f"{fmt_duration(album.total_duration())}")
        print(f"  {meta}")
        _print_separator()
        print()

        # Tracklist preview
        print("  ┌─  TRACKLIST  ─────────────────────────────────────────────")
        for i, s in enumerate(album.songs, 1):
            gl = s.genre_label()
            print(f"  │  {i:>2}. {s.name:<28}  {gl:<22}  {fmt_duration(s.duration)}")
        print("  └────────────────────────────────────────────────────────────")
        print()

        all_album_scores            = []
        all_track_scores_by_critic  = []

        for ac in self.album_critics:
            album_score, song_scores, review_text = ac.write_review(album)
            all_album_scores.append(album_score)
            all_track_scores_by_critic.append((ac, album_score, song_scores))

            print(f"  ★  {ac.name}  [{ac.tagline}]")
            print(f"  {'─' * 60}")
            _wrap_print(review_text)
            print()
            print("  Track Ratings:")
            for song, sc in zip(album.songs, song_scores):
                bar = _score_bar(sc)
                print(f"    {song.name:<30}  {sc:>4}/10  {bar}")
            print(f"  Album Score: {album_score}/10")
            print()

        # Aggregate
        avg = round(sum(all_album_scores) / len(all_album_scores), 1)
        _print_box(f"  ALBUM: '{album.name}'  |  AVG CRITICAL SCORE: {avg}/10  ")

        if avg >= 9.5:   tag = "★  UNIVERSAL ACCLAIM  ★"
        elif avg >= 8.5: tag = "MASTERPIECE"
        elif avg >= 8.0: tag = "GENERALLY ACCLAIMED"
        elif avg >= 6.5: tag = "GENERALLY FAVOURABLE"
        elif avg >= 5.0: tag = "MIXED REVIEWS"
        elif avg >= 3.0: tag = "GENERALLY UNFAVOURABLE"
        else:            tag = "OVERWHELMING DISLIKE"
        print(f"  Consensus: {tag}")
        print()

        # Best and worst track across all critics
        n = len(album.songs)
        avg_per_track = []
        for ti in range(n):
            scores_for_track = [tsc[2][ti] for tsc in all_track_scores_by_critic]
            avg_per_track.append(round(sum(scores_for_track) / len(scores_for_track), 1))

        print("  Aggregate Track Scores:")
        for i, (song, sc) in enumerate(zip(album.songs, avg_per_track)):
            bar = _score_bar(sc)
            print(f"    {song.name:<30}  {sc:>4}/10  {bar}")
        print()
        best_ti  = avg_per_track.index(max(avg_per_track))
        worst_ti = avg_per_track.index(min(avg_per_track))
        print(f"  🏆 Best Track:    {album.songs[best_ti].name}  ({avg_per_track[best_ti]}/10)")
        print(f"  ⚠  Weakest Track: {album.songs[worst_ti].name}  ({avg_per_track[worst_ti]}/10)")
        _print_separator()


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def _print_box(label):
    print("╔" + "═" * 64 + "╗")
    print("║" + label.center(64) + "║")
    print("╚" + "═" * 64 + "╝")

def _print_separator():
    print("─" * 66)

def _wrap_print(text, indent="  ", width=WRAP_WIDTH):
    words = text.split()
    line  = indent
    for word in words:
        if len(line) + len(word) + 1 > width:
            print(line)
            line = indent + word + " "
        else:
            line += word + " "
    if line.strip():
        print(line)

def _score_bar(score, width=10):
    filled = int(round(score / 10 * width))
    return "█" * filled + "░" * (width - filled)


# ─────────────────────────────────────────────
#  CLI HELPERS
# ─────────────────────────────────────────────

def banner():
    print()
    print("╔" + "═" * 64 + "╗")
    print("║" + "  🎵  MUSIC CAREER SIMULATOR  —  ALBUM MODE  🎵  ".center(64) + "║")
    print("╚" + "═" * 64 + "╝")
    print()

def get_choice(prompt, options):
    while True:
        print(f"\n  {prompt}")
        for key, val in options.items():
            print(f"    [{key}]  {val}")
        choice = input("  ›› ").strip()
        if choice in options:
            return options[choice]
        print("  ✗  Invalid choice — try again.")

def parse_duration():
    while True:
        try:
            mins = int(input("  Minutes: "))
            secs = int(input("  Seconds: "))
            if 0 <= secs < 60 and mins >= 0:
                return mins * 60 + secs
        except (ValueError, TypeError):
            pass
        print("  ✗  Invalid duration — try again.")

def select_genres():
    print("\n  ┌─────────────────────────────────────────┐")
    print("  │           SELECT GENRE(S)               │")
    print("  └─────────────────────────────────────────┘")
    gmap = {str(i + 1): g for i, g in enumerate(GENRES)}
    for key, val in gmap.items():
        print(f"    [{key:>2}]  {val}")
    while True:
        raw   = input("  ›› Pick 1 or 2 genre numbers (e.g. '1' or '3 7'): ").strip()
        parts = raw.split()
        if len(parts) == 1 and parts[0] in gmap:
            return [gmap[parts[0]]]
        if (len(parts) == 2 and parts[0] in gmap
                and parts[1] in gmap and parts[0] != parts[1]):
            return [gmap[parts[0]], gmap[parts[1]]]
        print("  ✗  Pick 1 or 2 valid different genre numbers.")

def select_theme():
    tmap = {str(i + 1): t for i, t in enumerate(THEMES)}
    return get_choice("SELECT THEME:", tmap)

def select_core_genre():
    return get_choice("SELECT ALBUM CORE GENRE:",
                      {str(i + 1): g for i, g in enumerate(GENRES)})

def select_core_theme():
    return get_choice("SELECT ALBUM CORE THEME:",
                      {str(i + 1): t for i, t in enumerate(THEMES)})

QUALITY_FLAVORS = [
    "feels like something could be here.",
    "the vibe is rough but it's something.",
    "this one has a pulse.",
    "produced clean, heart unclear.",
    "sounds promising.",
    "could be great, could be nothing.",
    "the energy is there.",
    "something's clicking.",
    "built in the right key.",
    "mid-session energy.",
    "you feel the momentum.",
    "tight from the jump.",
    "something special might be happening.",
    "every second is pulling its weight.",
    "this one could define the album.",
]

def main():
    banner()
    sim = AlbumSimulation()

    while True:
        print()
        cmd = input("  Press [A] to create an album  |  [Q] to quit  ›› ").strip().lower()
        if cmd == 'q':
            print("\n  See you on the charts.\n")
            break
        if cmd != 'a':
            continue

        print()
        album_name = input("  Album name: ").strip() or "Untitled Album"
        core_genre = select_core_genre()
        core_theme = select_core_theme()
        album      = Album(album_name, core_genre, core_theme)

        print()
        print(f"  ┌─────────────────────────────────────────────────────┐")
        print(f"  │  Album created: '{album_name}'")
        print(f"  │  Minimum songs to publish: {MIN_SONGS}")
        print(f"  └─────────────────────────────────────────────────────┘")

        while True:
            quality = random.randint(1, 10)
            flavor  = pick(QUALITY_FLAVORS)
            n       = album.song_count()

            print()
            print(f"  ┌──────────────────────────────────────────────────┐")
            print(f"  │  Song generated  —  Quality: {quality}/10  —  {flavor:<20}│")
            print(f"  │  Album so far: {n} track{'s' if n != 1 else ' '}  {'  *** READY TO PUBLISH ***' if n >= MIN_SONGS else f'  ({MIN_SONGS - n} more to unlock publish)':<26}│")
            print(f"  └──────────────────────────────────────────────────┘")
            print(f"    [1]  Add song to album")
            print(f"    [2]  Scrap and generate new song")
            if n >= MIN_SONGS:
                print(f"    [3]  Publish album  ({n} tracks)")

            act = input("  ›› ").strip()

            if act == '2':
                continue

            if act == '3':
                if n < MIN_SONGS:
                    print(f"  ✗  Need at least {MIN_SONGS} songs to publish. You have {n}.")
                    continue
                print()
                print(f"  Publishing '{album_name}' with {n} tracks...")
                print()
                sim.publish_album(album)
                break

            if act == '1':
                print()
                name     = input("  Song name: ").strip() or f"Track {n + 1}"
                genres   = select_genres()
                theme    = select_theme()
                print("\n  ┌────────────────────────────────────┐")
                print("  │           SONG DURATION            │")
                print("  └────────────────────────────────────┘")
                duration = parse_duration()
                song     = Song(quality, name, genres, theme, duration)
                album.add_song(song)
                print(f"\n  ✓  '{name}' added to '{album_name}'.  ({album.song_count()} tracks so far)")
                continue


if __name__ == "__main__":
    main()
