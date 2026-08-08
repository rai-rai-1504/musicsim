"""
album_mode.py
─────────────────────────────────────────────
MUSIC CAREER SIMULATOR — ALBUM REVIEW MODULE
─────────────────────────────────────────────
Requires reviewproto6.py in the same directory.
Run: python3 album_mode.py
"""

import random
import sys
import os

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

MIN_SONGS   = 7
WRAP_WIDTH  = 74

# ─────────────────────────────────────────────
#  THEME COMPATIBILITY MAP
#  compatible[theme] = set of themes that flow INTO this theme naturally
# ─────────────────────────────────────────────

COMPATIBLE_TRANSITIONS = {
    # TO          : FROM themes that work
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


def theme_transition_score(from_theme, to_theme):
    """Returns a delta: +0.3 compatible, 0 neutral, -0.4 incompatible."""
    if from_theme is None:
        return 0
    if from_theme == to_theme:
        return 0.2  # mild reward for consistent theme
    if from_theme in COMPATIBLE_TRANSITIONS.get(to_theme, set()):
        return 0.2
    if from_theme in INCOMPATIBLE_TRANSITIONS.get(to_theme, set()):
        return -0.8
    return 0  # neutral


# ─────────────────────────────────────────────
#  ALBUM MODEL
# ─────────────────────────────────────────────

class Album:
    def __init__(self, name, core_genre, core_theme):
        self.name       = name
        self.core_genre = core_genre
        self.core_theme = core_theme
        self.songs      = []   # list of Song objects

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

    # ── cohesion: how many songs match the core genre ──────────────
    def cohesion_stats(self):
        on_genre  = sum(1 for s in self.songs if self.core_genre in s.genres)
        off_genre = len(self.songs) - on_genre
        return on_genre, off_genre

    def cohesion_penalty(self):
        _, off = self.cohesion_stats()
        extra  = max(0, off - 2)   # first 2 off-genre songs forgiven
        return round(extra * 0.25, 2)

    # ── continuity: core theme alignment + track flow ──────────────
    def theme_alignment_ratio(self):
        if not self.songs:
            return 1.0
        matching = sum(1 for s in self.songs if s.theme == self.core_theme)
        return matching / len(self.songs)

    def theme_alignment_modifier(self):
        ratio = self.theme_alignment_ratio()
        if ratio >= 0.80:
            return  0.2   # reward
        elif ratio >= 0.60:
            return  0.0   # neutral
        else:
            drop_units = int((0.60 - ratio) / 0.10)
            return -(drop_units * 0.2)

    def track_flow_modifier(self):
        """Sum of transition bonuses/penalties across the tracklist."""
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


# ─────────────────────────────────────────────
#  ALBUM CRITIC  (wraps each song-critic for album logic)
# ─────────────────────────────────────────────

class AlbumCritic:
    """
    Each song-critic gets an AlbumCritic wrapper that:
      • Scores each song individually (via critic.compute_score)
      • Applies album-level modifiers (cohesion, continuity, length pref)
      • Generates a full prose review of 15+ sentences in the critic's voice
    """

    # Length preference: (min_songs_they_like, max_songs_they_like)
    # Outside range → penalty; inside → small bonus
    length_preference      = (8, 14)   # default
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
        base        = round(sum(song_scores) / len(song_scores), 2)

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

        final = base - cohesion_pen + theme_mod + flow_mod + length_mod
        return clamp(final), song_scores

    # ── prose review ───────────────────────────────────────────────
    def write_review(self, album):
        album_score, song_scores = self.compute_album_score(album)
        tier = score_tier(album_score)

        best_idx  = song_scores.index(max(song_scores))
        worst_idx = song_scores.index(min(song_scores))
        best_song  = album.songs[best_idx]
        worst_song = album.songs[worst_idx]

        on, off   = album.cohesion_stats()
        ratio     = album.theme_alignment_ratio()
        flow_mod  = album.track_flow_modifier()

        paragraphs = []

        # ── 1. OPENING IMPRESSION ─────────────────────────────────
        paragraphs.append(self._opening(album, album_score, tier))

        # ── 2. COHESION COMMENTARY ────────────────────────────────
        paragraphs.append(self._cohesion(album, on, off, tier))

        # ── 3. CONTINUITY / THEME FLOW ────────────────────────────
        paragraphs.append(self._continuity(album, ratio, flow_mod, tier))

        # ── 4. STANDOUT SONG PRAISE ───────────────────────────────
        paragraphs.append(self._praise_best(best_song, song_scores[best_idx]))

        # ── 5. WEAKEST SONG CRITIQUE ──────────────────────────────
        paragraphs.append(self._critique_worst(worst_song, song_scores[worst_idx]))

        # ── 6. ALBUM LENGTH COMMENTARY ────────────────────────────
        length_note = self._length_note(album)
        if length_note:
            paragraphs.append(length_note)

        # ── 7. CLOSING VERDICT ────────────────────────────────────
        paragraphs.append(self._closing(album, album_score, tier))

        # Assemble — ensure each sentence is punctuated
        sentences = []
        for p in paragraphs:
            if isinstance(p, list):
                sentences.extend([ensure_punct(s) for s in p if s and s.strip()])
            elif p and p.strip():
                sentences.append(ensure_punct(p))

        return album_score, song_scores, " ".join(sentences)

    # ── SECTION BUILDERS (overridden per critic subclass) ──────────

    def _opening(self, album, score, tier):
        raise NotImplementedError

    def _cohesion(self, album, on, off, tier):
        raise NotImplementedError

    def _continuity(self, album, ratio, flow_mod, tier):
        raise NotImplementedError

    def _praise_best(self, song, score):
        raise NotImplementedError

    def _critique_worst(self, song, score):
        raise NotImplementedError

    def _length_note(self, album):
        return None   # optional; most critics can skip

    def _closing(self, album, score, tier):
        raise NotImplementedError


# ─────────────────────────────────────────────
#  HELPER: readable ratio text
# ─────────────────────────────────────────────

def _pct(ratio):
    return f"{int(round(ratio * 100))}%"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 1 — MARCUS VANE (Elitist)
# ═══════════════════════════════════════════════════════════════

class AlbumMarcusVane(AlbumCritic):
    length_preference    = (9, 13)
    length_short_penalty = -0.5
    length_long_penalty  = -0.4
    length_ideal_bonus   = 0.3

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"'{album.name}' is a record that seems unaware of its own failures, which is the most frustrating kind of failure.",
                        f"I approached '{album.name}' hoping to be surprised. I was — by how thoroughly it confirmed my worst expectations.",
                        f"'{album.name}' demonstrates a consistent inability to convert ambition into execution, which is a complete record in the wrong sense."],
            "mid_low": [f"'{album.name}' is a record in search of a reason to exist — it finds that reason intermittently, which is almost worse than not finding it.",
                        f"I wanted more from '{album.name}' because the materials occasionally suggest it was possible. It wasn't, quite.",
                        f"'{album.name}' is a collection of missed opportunities assembled with some technical competence and no discernible artistic vision."],
            "mid_high":[f"'{album.name}' is a record that works more often than it doesn't, which is more than I expected and less than I hoped.",
                        f"'{album.name}' earns my attention in intervals — the good stretches are genuinely good, which makes the lesser ones harder to excuse.",
                        f"'{album.name}' is a real record with real ideas that surface inconsistently across its runtime."],
            "high":    [f"'{album.name}' is a serious piece of work — formally considered, emotionally present, and difficult to dismiss even when I try.",
                        f"'{album.name}' surprised me and surprised me honestly. This is the kind of album I don't expect to encounter and am grateful when I do.",
                        f"'{album.name}' is a record built from genuine artistic conviction and executed with a craft that rewards the kind of attention I insist on giving."],
            "perfect": [f"'{album.name}' is a masterpiece and I will not qualify that statement.",
                        f"I have spent a career being skeptical of perfect records. '{album.name}' has made that skepticism feel like a mistake.",
                        f"'{album.name}' is what music is supposed to be. I do not say that without twenty years of critical standards behind it."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The genre commitment here is absolute — every track operates within the {album.core_genre} framework and never once uses that consistency as an excuse for monotony.",
                         f"There is no genre confusion on '{album.name}' — the {album.core_genre} identity holds from first track to last, which is a discipline most albums don't achieve.",
                         f"The {album.core_genre} focus never wavers and never uses that focus as a ceiling. That combination is rare."])
        elif off <= 2:
            return pick([f"The {album.core_genre} foundation holds throughout, with {off} track{'s' if off > 1 else ''} that depart from it — a departure that functions as healthy experimentation rather than identity confusion.",
                         f"The genre identity is clear despite {off} track{'s' if off > 1 else ''} that wander beyond the {album.core_genre} frame. The frame is secure enough to absorb the wandering.",
                         f"Minor genre excursions aside, '{album.name}' knows what it is. The {album.core_genre} core is intact and that security makes the deviations feel intentional rather than confused."])
        else:
            return pick([f"The {off} tracks operating outside the {album.core_genre} frame create an identity problem the album never fully resolves.",
                         f"The genre consistency is the album's most significant structural issue — {off} off-genre tracks in {album.song_count()} is too many to read as exploration and too few to read as reinvention.",
                         f"'{album.name}' doesn't know what it wants to be, and that indecision is audible across {off} tracks that abandon the {album.core_genre} identity without committing to anything in its place."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8 and flow_mod >= 0:
            return pick([f"The thematic continuity is exceptional — {pct} of the tracklist aligns with the {album.core_theme} core and the transitions between songs handle the remaining variance with genuine compositional intelligence.",
                         f"The {album.core_theme} thread runs through '{album.name}' with the kind of structural care that distinguishes a record from a collection of songs.",
                         f"The album flows the way a serious record should — the {album.core_theme} theme is the spine and the songs organize themselves around it with purpose."])
        elif ratio >= 0.6:
            return pick([f"The thematic focus is present without being total — {pct} of tracks engage the {album.core_theme} core, which is sufficient but not exceptional.",
                         f"'{album.name}' maintains its {album.core_theme} theme across most of the tracklist. The gaps are manageable but occasionally disruptive to the overall flow.",
                         f"The thematic architecture is functional rather than inspired — {pct} alignment with the {album.core_theme} core is enough to hold the album together, barely."])
        else:
            return pick([f"The thematic coherence is the album's most serious problem — only {pct} of the tracklist engages the {album.core_theme} theme, and the sequencing compounds the confusion.",
                         f"'{album.name}' is thematically adrift. The {album.core_theme} foundation is present in too few tracks to anchor an album of this length.",
                         f"The track-to-track thematic logic is almost entirely absent. '{album.name}' is a collection of individually reviewed pieces rather than a unified statement."])

    def _praise_best(self, song, score):
        tier = score_tier(score)
        if tier in ("high", "perfect"):
            return pick([f"'{song.name}' is the record's defining moment — the exact track around which the rest of the album organizes itself.",
                         f"'{song.name}' is what the entire album is reaching for, and it arrives there completely. A track I will return to.",
                         f"'{song.name}' justifies the album on its own. Everything surrounding it benefits from being near it."])
        elif tier == "mid_high":
            return pick([f"'{song.name}' is the album's peak — a track that demonstrates what this record could have been consistently.",
                         f"'{song.name}' is where the record becomes what it occasionally promises to be elsewhere.",
                         f"The album reaches its highest point on '{song.name}', which is genuinely good and worth the price of admission alone."])
        else:
            return pick([f"'{song.name}' is the strongest track here, which is a relative distinction given the context.",
                         f"'{song.name}' is where the album comes closest to its stated intentions — a modest achievement, but the record's best moment.",
                         f"The best this album offers is '{song.name}' — and what it offers is, at minimum, honest."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"Even the album's weakest moment, '{song.name}', is handled with sufficient craft that 'weak' is a relative term here.",
                         f"'{song.name}' is the album's most uneven track, though uneven by the standard this record sets is still more than adequate.",
                         f"If I'm being precise, '{song.name}' is where the album breathes least efficiently — but the breathing never stops."])
        elif score >= 5:
            return pick([f"'{song.name}' is the album's most significant misstep — it breaks the momentum at exactly the wrong point.",
                         f"'{song.name}' is where the record loses me. The ideas are present; the execution is not.",
                         f"'{song.name}' represents the album's structural problem in miniature — potential without follow-through."])
        else:
            return pick([f"'{song.name}' is a genuine failure and its placement on the tracklist is a miscalculation that costs the album momentum it never fully recovers.",
                         f"'{song.name}' should not be on this record. Its inclusion suggests either poor editorial judgment or an absence of it.",
                         f"'{song.name}' is the track I will not be returning to. It is the album's most honest reflection of its worst tendencies."])

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks, '{album.name}' is slightly short for what it's attempting — the ideas needed more room to develop.",
                         f"The album's brevity at {n} tracks is its most forgivable limitation. Some records earn that length. This one needed two or three more."])
        elif n > self.length_preference[1]:
            return pick([f"At {n} tracks, '{album.name}' tests patience it hasn't fully earned. The editorial discipline could have been more severe.",
                         f"The album is too long. {n} tracks is two or three more than the material can sustain at this level of quality."])
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
    length_preference    = (10, 16)
    length_short_penalty = -0.2
    length_long_penalty  = -0.3
    length_ideal_bonus   = 0.25

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"I came to '{album.name}' ready to love it and the album made that impossible.",
                        f"'{album.name}' has the energy of a record trying to be exciting without understanding what exciting actually requires.",
                        f"I kept waiting for '{album.name}' to start. By the end I was still waiting."],
            "mid_low": [f"'{album.name}' is frustrating because the pieces are almost there — you can see what it wanted to be.",
                        f"'{album.name}' has a great album buried inside a decent one. The decent one got released.",
                        f"I wanted to love this more than I do. '{album.name}' is trying and almost getting there."],
            "mid_high":[f"'{album.name}' is genuinely good and I mean that without hedging — this album delivers.",
                        f"'{album.name}' does what a good album is supposed to do: it keeps you in the room.",
                        f"I had a great time with '{album.name}'. The highs are real and the lows are survivable."],
            "high":    [f"'{album.name}' is the kind of record I put on for other people. That is the highest compliment I give.",
                        f"'{album.name}' goes. I don't know how else to describe it — from the first track, it just goes.",
                        f"I've played '{album.name}' more times than I've reviewed it and I'm okay with that."],
            "perfect": [f"'{album.name}' is perfect. I'm not using that word loosely. I mean every syllable of it.",
                        f"There are albums you like and albums you need. '{album.name}' just became one I need.",
                        f"I'm going to be talking about '{album.name}' for years. Might as well start now."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The {album.core_genre} identity is locked in across every track — it sounds like a complete vision rather than a collection.",
                         f"Zero genre drift and that's actually impressive — '{album.name}' commits fully to {album.core_genre} and the commitment pays off.",
                         f"Every song on this album knows what album it's on. The {album.core_genre} through-line is a feature, not a constraint."])
        elif off <= 2:
            return pick([f"The {album.core_genre} core holds and the {off} genre detour{'s' if off>1 else ''} feel like additions rather than distractions.",
                         f"Mostly {album.core_genre} with a little room to breathe — the {off} genre departure{'s' if off>1 else ''} show confidence rather than confusion.",
                         f"The album knows its identity and isn't afraid to stretch it a little. That's maturity."])
        else:
            return pick([f"The genre focus slips in {off} places and the album loses something every time it does.",
                         f"{off} tracks step outside the {album.core_genre} frame and the album doesn't quite recover its identity afterward.",
                         f"The genre inconsistency is the one thing holding this back — {off} off-genre tracks is too many for a cohesive listen."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8 and flow_mod >= 0:
            return pick([f"The {album.core_theme} theme flows through this album the way a great playlist flows — each song leads into the next and the whole thing feels intentional.",
                         f"The thematic consistency here is one of the album's strengths — {pct} of tracks are working the {album.core_theme} angle and the sequencing respects that.",
                         f"The track ordering on '{album.name}' is doing real emotional work — the {album.core_theme} thread holds from front to back."])
        elif ratio >= 0.6:
            return pick([f"The {album.core_theme} theme holds for {pct} of the album which is enough to feel intentional even where it drifts.",
                         f"Some theme drift mid-album but the {album.core_theme} core is strong enough to pull the record back together.",
                         f"The album's thematic journey is a bit bumpy but the {album.core_theme} destination is clear enough."])
        else:
            return pick([f"The thematic drift is real — only {pct} of tracks stay on the {album.core_theme} mission and the album loses cohesion because of it.",
                         f"'{album.name}' can't quite decide what it's about. Only {pct} of it engages the {album.core_theme} theme and the rest is going in different directions.",
                         f"The theme flow is the album's weakest point — too many sudden tonal shifts, not enough of the connective tissue that makes albums feel like albums."])

    def _praise_best(self, song, score):
        if score_tier(score) in ("high", "perfect"):
            return pick([f"'{song.name}' is the moment where the album becomes undeniable — the track I've had on repeat since the first listen.",
                         f"'{song.name}' alone would make '{song.name}' worth talking about. The rest of the album is lucky to have it.",
                         f"'{song.name}' is the reason I'll still be playing this album in six months."])
        elif score_tier(score) == "mid_high":
            return pick([f"'{song.name}' is the album's best argument for itself — everything it does well, it does here.",
                         f"'{song.name}' is where the album peaks and the peak is genuinely high.",
                         f"When '{song.name}' hits, the album becomes exactly what I wanted it to be."])
        else:
            return pick([f"'{song.name}' is the best of what's here and what's here is limited — but the track itself works.",
                         f"'{song.name}' is the album's brightest spot in a sometimes dim tracklist.",
                         f"If you're going to sample this album, '{song.name}' is where to start."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is the one I skip occasionally — which in the context of this album means it's a nine instead of a ten.",
                         f"'{song.name}' is the album's lightest moment, which is fine — the heaviest moments more than compensate.",
                         f"Even the weakest track here, '{song.name}', isn't a skip so much as a breath."])
        elif score >= 5:
            return pick([f"'{song.name}' is where the energy drops and the album needs it not to drop right there.",
                         f"'{song.name}' is a dip I can forgive but I do actually notice it every time.",
                         f"'{song.name}' doesn't land the way the rest of the record does. It's the one the album could have done without."])
        else:
            return pick([f"'{song.name}' is a problem. It stalls the album at the worst possible moment and I still haven't forgiven it for that.",
                         f"'{song.name}' shouldn't be here — it breaks the spell the album works hard to cast.",
                         f"I love this album enough to be honest about '{song.name}': it doesn't belong on this record."])

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks I wanted more — the album ends just when it's fully warmed up.",
                         f"{n} tracks isn't enough for the world this album is building. I wanted to stay longer."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is a lot and the album earns about {self.length_preference[1]} of them.",
                         f"The album is a touch bloated at {n} tracks. A harder edit would have made the good parts hit harder."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["hype"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' had everything it needed except the execution.",
            "mid_low": f"'{album.name}' is close to great and that's both the compliment and the critique.",
            "mid_high":f"'{album.name}' is solid and I'm happy to say that without any caveats.",
            "high":    f"'{album.name}' is one of the best records I've heard this cycle.",
            "perfect": f"'{album.name}' is it. Full stop.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 3 — VIC OSEI (Blunt)
# ═══════════════════════════════════════════════════════════════

class AlbumVicOsei(AlbumCritic):
    length_preference    = (8, 11)
    length_short_penalty = -0.3
    length_long_penalty  = -0.6   # Vic really hates bloat
    length_ideal_bonus   = 0.1
    # Vic caps high — hard base modifier
    # inherited from VicOsei critic which has base_modifier = -2.5

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"'{album.name}'. No.",
                        f"Listened to all of '{album.name}'. Didn't need to.",
                        f"'{album.name}' is not good. Moving on."],
            "mid_low": [f"'{album.name}' is mostly fine. Mostly not interesting either.",
                        f"'{album.name}' exists. Some of it works. Most of it is mid.",
                        f"'{album.name}': has some moments, wastes most of them."],
            "mid_high":[f"'{album.name}' is actually decent. Didn't expect that.",
                        f"'{album.name}' works. Not groundbreaking. But it works.",
                        f"I've heard worse albums than '{album.name}'. I've heard better. This sits fine in the middle."],
            "high":    [f"'{album.name}' is genuinely good. Annoying to admit but true.",
                        f"'{album.name}' hit. Solid record. Not wasting more words than it deserves.",
                        f"'{album.name}' earns it. That's the review."],
            "perfect": [f"'{album.name}' is great. Fine. I said it.",
                        f"'{album.name}' is actually flawless. I'll acknowledge that once.",
                        f"'{album.name}'. Yeah. This one's real."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"Sticks to {album.core_genre} the whole way through. Consistent. Fine.",
                         f"Full {album.core_genre} album. No identity crisis. Appreciated.",
                         f"Knows what it is. {album.core_genre}. All the way. Good."])
        elif off <= 2:
            return pick([f"{off} track{'s' if off>1 else ''} step outside {album.core_genre}. Small detour. Album survives it.",
                         f"Mostly {album.core_genre} with {off} departure{'s' if off>1 else ''}. Not a problem.",
                         f"Minor genre drift. Not enough to matter."])
        else:
            return pick([f"{off} off-genre tracks. That's too many. Pick a lane.",
                         f"The {album.core_genre} identity gets lost {off} times. Every time it costs something.",
                         f"Genre confusion is a problem here. {off} tracks don't know what album they're on."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8:
            return pick([f"Theme is consistent. {pct} on-target. Album flows.",
                         f"The {album.core_theme} thread holds. Sequencing isn't a mess. Good.",
                         f"Thematically together. {pct} on the {album.core_theme} core. No complaints."])
        elif ratio >= 0.6:
            return pick([f"Theme holds for {pct} of it. The rest drifts but doesn't ruin the listen.",
                         f"Some thematic inconsistency. {pct} on {album.core_theme}. Survivable.",
                         f"The {album.core_theme} focus slips a bit. Not fatal but noticeable."])
        else:
            return pick([f"Only {pct} thematic consistency. That's not enough. Album feels scattered.",
                         f"The theme logic is a mess. {pct} on {album.core_theme} and the rest going everywhere.",
                         f"No real thematic through-line. Just a playlist with a name."])

    def _praise_best(self, song, score):
        if score_tier(score) in ("high", "perfect"):
            return pick([f"'{song.name}' is actually excellent. Best track. Not close.",
                         f"'{song.name}' earns it. Best thing here by some distance.",
                         f"Play '{song.name}'. Skip the rest if you're in a hurry."])
        elif score_tier(score) == "mid_high":
            return pick([f"'{song.name}' is the album's best moment. Which is a solid moment.",
                         f"'{song.name}' works well. High point of the record.",
                         f"'{song.name}' is the one I'd show someone to explain what this album is trying to do."])
        else:
            return pick([f"'{song.name}' is the best of a limited set. It's fine.",
                         f"'{song.name}' edges out the competition. Not by a lot.",
                         f"'{song.name}' is the least problematic track. That's the compliment."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is the weakest one. Still fine. Album doesn't suffer.",
                         f"'{song.name}' is a slight dip. Nothing serious.",
                         f"'{song.name}' is where I briefly checked my phone. Not a real problem."])
        elif score >= 5:
            return pick([f"'{song.name}' is a filler track. It shows.",
                         f"'{song.name}' shouldn't be where it is on the tracklist.",
                         f"'{song.name}' is mid. The album doesn't need it."])
        else:
            return pick([f"'{song.name}' is bad. Genuinely hurts the album. Cut it.",
                         f"'{song.name}' is the problem track. It's obvious.",
                         f"'{song.name}' doesn't belong here. Editorial failure."])

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
    length_preference    = (9, 14)
    length_short_penalty = -0.2
    length_long_penalty  = -0.2
    length_ideal_bonus   = 0.2

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"'{album.name}' is a record everyone will dismiss — and for once, their instincts will be correct.",
                        f"I looked for the hidden value in '{album.name}'. I'm not finding it, and I looked harder than most would.",
                        f"'{album.name}' is bad. I'm not being contrarian — the mainstream will hate it and they will be right."],
            "mid_low": [f"The consensus on '{album.name}' will be kind and the consensus will be wrong — but in the opposite direction than usual. This is worse than it'll be given credit for.",
                        f"'{album.name}' is a four that most critics will call a six. I'm not most critics.",
                        f"'{album.name}' has the kind of surface appeal that passes for depth in lazy reviews. It isn't depth."],
            "mid_high":[f"'{album.name}' will be slept on. Most albums get overrated. This one will get underrated.",
                        f"The critical establishment will be lukewarm about '{album.name}'. The critical establishment will be wrong.",
                        f"'{album.name}' is better than it will be given credit for. I'm saying that now, before the takes start coming in."],
            "high":    [f"'{album.name}' is the record this cycle that nobody is going to give enough credit to. I'm giving it the credit.",
                        f"'{album.name}' is a genuinely important record that will be correctly identified as such only in retrospect.",
                        f"I'm calling '{album.name}' now: excellent, underrated, and correctly assessed only by a minority of listeners."],
            "perfect": [f"I've been called contrarian my entire career. I'm calling '{album.name}' a masterpiece first.",
                        f"'{album.name}' is the perfect record this year that no one will say is perfect this year. History will correct that.",
                        f"The consensus will catch up to '{album.name}' eventually. For now: a masterpiece, and I'm on record."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The {album.core_genre} unity here will be called 'limiting' by critics who mistake range for quality. It's not limiting — it's focused.",
                         f"Everyone will say the {album.core_genre} commitment is a weakness. It's a strength that most albums don't have the discipline to achieve.",
                         f"Zero genre drift. Critics will call it narrow. I'll call it intentional."])
        elif off <= 2:
            return pick([f"The {off} genre departure{'s' if off>1 else ''} will be called 'adventurous' by some reviewers. They're controlled experiments, which is different and better.",
                         f"Minor genre excursions that most will overlook but which show real compositional confidence.",
                         f"The {album.core_genre} core holds and the small departures earn their place. Most reviewers will miss why."])
        else:
            return pick([f"The genre inconsistency at {off} tracks is going to be called 'eclectic' by supportive reviews. It's actually confused.",
                         f"{off} off-genre tracks is a problem that even a generous reading can't resolve into 'experimentation'.",
                         f"The genre incoherence here is one thing I can't defend, even against the grain."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8 and flow_mod >= 0:
            return pick([f"The thematic coherence is the album's most underappreciated quality — {pct} on-theme with transitions that actually make structural sense.",
                         f"The {album.core_theme} thread runs through this album with a logic most reviewers won't bother to trace. It's worth tracing.",
                         f"The track ordering on '{album.name}' is doing compositional work that the mainstream press won't credit. I'll credit it."])
        elif ratio >= 0.6:
            return pick([f"The thematic drift — {pct} {album.core_theme} alignment — will be read as inconsistency. There's a structural logic to it that resists that reading.",
                         f"The theme flow is imperfect and more intentional than it will be given credit for.",
                         f"The thematic inconsistency has a logic. Not everyone will find it but it's there."])
        else:
            return pick([f"The thematic incoherence at {pct} alignment is the album's real problem. This isn't a contrarian read — the {album.core_theme} foundation is just absent too often.",
                         f"Only {pct} thematic consistency. I can't defend that even with a generous reading.",
                         f"The album is thematically scattered and I can't find the hidden intelligence in the scattering."])

    def _praise_best(self, song, score):
        tier = score_tier(score)
        if tier in ("high", "perfect"):
            return pick([f"'{song.name}' is the track the mainstream will overlook. It is also the best track on the record by some distance.",
                         f"'{song.name}' is what the album is actually about — the rest of the tracklist justifies being in proximity to it.",
                         f"'{song.name}' is extraordinary and will be treated as a deep cut. That's the correct ratio of quality to recognition."])
        else:
            return pick([f"'{song.name}' is the album's best moment and it's better than most will say.",
                         f"'{song.name}' is going to be slept on. It is the best argument the album makes for itself.",
                         f"The high point is '{song.name}'. Most reviews will mention it briefly. It deserves more than that."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"Even the lowest-rated track, '{song.name}', is better than the consensus will rate the whole album.",
                         f"'{song.name}' is the weakest here and it's still more interesting than most albums' highlights.",
                         f"'{song.name}' is the one place the album gives ground. It gives very little."])
        elif score >= 5:
            return pick([f"'{song.name}' is the album's most overrated moment — critics will like it for reasons that don't hold up.",
                         f"'{song.name}' is where the album takes the easy path. The rest of the record earns its difficulty — this doesn't.",
                         f"'{song.name}' is the compromise that costs the album some integrity. It's not unlistenable. It's just less."])
        else:
            return pick([f"'{song.name}' is the album's genuine failure and I won't pretend otherwise.",
                         f"'{song.name}' is bad. Not interestingly bad. Just bad. And that's the one thing I can't work with.",
                         f"'{song.name}' is the flaw I can't argue around. The album would be stronger without it."])

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["contrarian"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' is not a victim of critical misreading. It's just not good.",
            "mid_low": f"'{album.name}' is worse than it looks and better than it sounds, and neither of those add up to a recommendation.",
            "mid_high":f"'{album.name}' deserves better coverage than it will get.",
            "high":    f"'{album.name}' is important and will be correctly recognized as such only after the fact.",
            "perfect": f"'{album.name}' is a masterpiece. I said it first.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 5 — EARL MOSELY (Nostalgic)
# ═══════════════════════════════════════════════════════════════

class AlbumEarlMosely(AlbumCritic):
    length_preference    = (10, 18)
    length_short_penalty = -0.4
    length_long_penalty  = -0.1  # Earl likes long albums
    length_ideal_bonus   = 0.3

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"I've spent fifty years with music and '{album.name}' reminds me of what happens when the tradition is ignored entirely.",
                        f"'{album.name}' is what gets made when no one in the room has actually listened to the records that made this genre worth caring about.",
                        f"I approached '{album.name}' with the patience I extend to all new records. It exhausted that patience before the third track."],
            "mid_low": [f"'{album.name}' has the spirit of something real in it — intermittently — which makes the overall result harder to accept.",
                        f"There are moments in '{album.name}' that suggest the artist understands what great music actually requires. Those moments are too few.",
                        f"'{album.name}' knows what it wants to be. It gets there occasionally and not consistently enough."],
            "mid_high":[f"'{album.name}' has something genuine in it — a quality I don't always find in new records and appreciate finding when I do.",
                        f"'{album.name}' reminds me, in its better moments, of why I still do this after all this time.",
                        f"'{album.name}' is a real album — built the old way, with care and sequence and intention."],
            "high":    [f"'{album.name}' is the kind of record I've been waiting for — music made with the understanding that records are supposed to last.",
                        f"'{album.name}' has the quality I look for and rarely find: it sounds like it was made for posterity, not for this week.",
                        f"'{album.name}' belongs in the conversation about the best records of its era. I'm putting it there now."],
            "perfect": [f"I've been listening for a very long time. '{album.name}' is one of the great records.",
                        f"'{album.name}' is the kind of record you hear and recognize immediately — it belongs with the ones that last.",
                        f"In fifty-seven years of listening, very few records have made me feel the way '{album.name}' just made me feel."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The {album.core_genre} commitment is complete and it's the right commitment — the album sounds like a unified statement, not a sampler.",
                         f"Every track earns its place in the {album.core_genre} framework. That kind of coherence used to be the baseline expectation.",
                         f"The genre consistency here is the kind the great albums had — not because of formula, but because of genuine artistic vision."])
        elif off <= 2:
            return pick([f"The {album.core_genre} foundation is solid enough to absorb the {off} departure{'s' if off>1 else ''} without losing its identity.",
                         f"The minor genre excursions here feel earned — the {album.core_genre} identity is secure enough to make them work.",
                         f"A bit of genre flexibility is healthy. The great records often had it. '{album.name}' uses it wisely."])
        else:
            return pick([f"The {off} off-genre tracks create a kind of identity confusion that the old records would not have permitted.",
                         f"Genre consistency was once considered non-negotiable for a reason. {off} departures from the {album.core_genre} core leave the album without a clear identity.",
                         f"The album loses itself {off} times and never fully recovers that sense of knowing exactly who it is."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8 and flow_mod >= 0:
            return pick([f"The {album.core_theme} through-line holds across {pct} of the tracklist and the sequencing is what sequencing was always supposed to be — a deliberate emotional journey.",
                         f"The album flows the way albums used to flow, when people still believed that the order of songs was an artistic choice.",
                         f"The thematic coherence here is the kind that takes thought and care. Someone spent time on the track ordering and it shows."])
        elif ratio >= 0.6:
            return pick([f"The {album.core_theme} theme holds for {pct} of the album — enough to feel intentional even if not fully realized.",
                         f"The thematic continuity is good without being great. The old records set a higher standard, but this clears the basic requirement.",
                         f"Some drift from the {album.core_theme} thread but the core holds. Not the work of a master sequencer but the work of someone who's trying."])
        else:
            return pick([f"The thematic coherence is the album's most significant shortcoming — only {pct} on the {album.core_theme} theme and the rest drifting without apparent reason.",
                         f"The great albums had a reason for every track to be in every position. '{album.name}' has only {pct} thematic alignment and the disorder is felt.",
                         f"The album lacks the kind of sequencing intelligence that once distinguished records from collections."])

    def _praise_best(self, song, score):
        tier = score_tier(score)
        if tier in ("high", "perfect"):
            return pick([f"'{song.name}' is the track that will last — the one people are still listening to when everything else has faded.",
                         f"'{song.name}' is where this album earns its place in memory. A genuinely great track.",
                         f"'{song.name}' is the kind of song the old musicians would have been proud of. That is the highest thing I know how to say."])
        else:
            return pick([f"'{song.name}' is the album's best offering. It is a genuine high point in a record of uneven altitude.",
                         f"'{song.name}' is where the album comes closest to the standard it seems to be reaching for.",
                         f"'{song.name}' is the track I'll return to — the one with enough soul to warrant the journey."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is the album's softest moment, which in the context of this record is a modest criticism.",
                         f"'{song.name}' is the one I'll occasionally skip — not because it's poor, but because the rest of the album sets such a high standard.",
                         f"'{song.name}' is where the album rests rather than arrives. A small concession in an otherwise strong record."])
        elif score >= 5:
            return pick([f"'{song.name}' is where the album stumbles — and in a record that otherwise walks carefully, the stumble is noticeable.",
                         f"'{song.name}' lacks the depth the rest of the album has found. It's a filler track in a record that shouldn't have filler.",
                         f"'{song.name}' is the track the album could have done without, and the album would have been better for the absence."])
        else:
            return pick([f"'{song.name}' is the album's most serious misstep — a track that doesn't belong in the company of the others.",
                         f"'{song.name}' falls below the standard the rest of the album has set. In my experience, one bad track can cost an album its legacy.",
                         f"'{song.name}' is where the album breaks faith with its best instincts. It is a genuine problem."])

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks, the album ends before it's fully said what it has to say. The old records breathed longer.",
                         f"{n} tracks isn't enough time for this material to develop the way it deserves to."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is ambitious and I respect the ambition, even if a few tracks could have been trimmed without loss.",
                         f"A long record is fine when the material is there. Most of '{album.name}' earns its length."])
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
    length_preference    = (9, 14)
    length_short_penalty = -0.2
    length_long_penalty  = -0.4
    length_ideal_bonus   = 0.2

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"'{album.name}' doesn't belong in any scene I cover and I mean that as a statement of fact, not cruelty.",
                        f"The underground has seen a lot of bad records come through. '{album.name}' is one of the worse ones.",
                        f"'{album.name}' has zero cultural currency. I checked. I looked hard."],
            "mid_low": [f"'{album.name}' is trying to be a scene record without understanding what the scene actually asks for.",
                        f"'{album.name}' is a record that would get polite nods at certain shows and nothing more.",
                        f"The scene deserves more than '{album.name}' is offering. It's a start and not a destination."],
            "mid_high":[f"'{album.name}' earns its place in the conversation — I'd put it on in the right spaces and not regret it.",
                        f"'{album.name}' has the cultural awareness the scene demands and uses it well enough.",
                        f"'{album.name}' is the kind of record you champion quietly but without hesitation."],
            "high":    [f"'{album.name}' is a scene record in the most complete sense — it knows what it is, where it comes from, and exactly who it's for.",
                        f"'{album.name}' is going to matter. Not next week — over time. The right people will hold this one.",
                        f"The scene was waiting for a record like '{album.name}' and here it is."],
            "perfect": [f"'{album.name}' is the record. The underground will still be playing this in five years.",
                        f"'{album.name}' is what we build scenes for — music that doesn't ask permission and doesn't need to.",
                        f"'{album.name}' is a landmark. That's not a word I use. I'm using it now."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"Pure {album.core_genre} from front to back. The scene respects that kind of commitment.",
                         f"No genre drift. The {album.core_genre} identity is complete and unapologetic. That's the standard.",
                         f"Fully locked into {album.core_genre}. No confusion about what this record is."])
        elif off <= 2:
            return pick([f"Mostly {album.core_genre} with {off} informed detour{'s' if off>1 else ''} — the kind of experimentation the scene reads as confident.",
                         f"The {album.core_genre} core is intact and the {off} departure{'s' if off>1 else ''} feel like creative choice rather than lack of direction.",
                         f"Minor genre diversions that show range rather than confusion. The scene can tell the difference."])
        else:
            return pick([f"{off} off-genre tracks is too many for the scene to read as intentional — it reads as undecided.",
                         f"The genre inconsistency over {off} tracks creates a cultural confusion the album never resolves.",
                         f"The {album.core_genre} identity is diluted by {off} departures. The underground wants to know what you are."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8 and flow_mod >= 0:
            return pick([f"The {album.core_theme} thread runs straight through this — {pct} alignment and transitions that earn their sequencing.",
                         f"The album flows. Not just sonically — thematically. The {album.core_theme} core at {pct} alignment and every transition was a decision.",
                         f"The track ordering here is doing real cultural work. The {album.core_theme} coherence at {pct} proves someone cared about the sequence."])
        elif ratio >= 0.6:
            return pick([f"The thematic coherence is enough to hold — {pct} on the {album.core_theme} angle with manageable drift.",
                         f"Some thematic wobble but the {album.core_theme} foundation at {pct} is solid enough.",
                         f"The flow is mostly there. The gaps are audible but not fatal."])
        else:
            return pick([f"Only {pct} on the {album.core_theme} theme — the album doesn't know what it's saying.",
                         f"The thematic coherence is the album's biggest problem in terms of scene reception. {pct} alignment reads as unfinished.",
                         f"No clear thematic through-line. {pct} on {album.core_theme} and the rest is noise."])

    def _praise_best(self, song, score):
        tier = score_tier(score)
        if tier in ("high", "perfect"):
            return pick([f"'{song.name}' is the record in miniature — every quality the album has at its most concentrated.",
                         f"'{song.name}' is the track the scene is going to know. This one travels.",
                         f"'{song.name}' is what the rest of the album is in service of. It earns that."])
        else:
            return pick([f"'{song.name}' is the album's best moment in a record of uneven ones.",
                         f"'{song.name}' is the track I'd put on to make someone understand what this album is going for.",
                         f"'{song.name}' is where the album finds itself. It should have stayed there longer."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is the one I'd sequence differently — it's not a problem, it's a missed opportunity.",
                         f"'{song.name}' is the album's most forgettable moment in a largely memorable record.",
                         f"'{song.name}' dips slightly. In an album this strong it barely registers."])
        elif score >= 5:
            return pick([f"'{song.name}' is where the album loses its nerve. The scene notices when records lose their nerve.",
                         f"'{song.name}' is the concession track — the one that exists for an audience the rest of the record isn't playing for.",
                         f"'{song.name}' disrupts the album's cultural identity. The scene will skip it."])
        else:
            return pick([f"'{song.name}' has no business being on this record. It costs the album credibility it takes tracks to earn.",
                         f"'{song.name}' is a scene problem — it signals that the artist doesn't fully trust the audience they've been building.",
                         f"'{song.name}' is inauthentic in a way the rest of the album isn't. That dissonance is heard."])

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"{n} tracks is lean for a statement record. The scene can absorb more.",
                         f"At {n} tracks the album feels like an EP that grew ambitious. It needed more room."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is one or two past where the scene's attention holds.",
                         f"The album's length at {n} tracks tests patience the earlier half earns but the later half spends."])
        return None

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["scenes"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' is not a scene record. It's not trying to be and it shows.",
            "mid_low": f"'{album.name}' is doing something in the right direction. Not there yet.",
            "mid_high":f"'{album.name}' earns its place in the conversation.",
            "high":    f"'{album.name}' is a record the scene will hold onto.",
            "perfect": f"'{album.name}' is a landmark. The scene will still be playing it..",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 7 — TOBIAS LUND (Casual)
# ═══════════════════════════════════════════════════════════════

class AlbumTobiasLund(AlbumCritic):
    length_preference    = (9, 14)
    length_short_penalty = -0.2
    length_long_penalty  = -0.4
    length_ideal_bonus   = 0.15

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"I genuinely tried to get through all of '{album.name}'. I got through most of it. That's the review.",
                        f"'{album.name}' didn't grab me and I gave it a real chance. The chance wasn't enough.",
                        f"'{album.name}' is not what I'm looking for in an album and I listened to enough of it to know that for certain."],
            "mid_low": [f"'{album.name}' is mostly fine and fine isn't really what I'm after in an album.",
                        f"'{album.name}' is the kind of album I have on in the background and occasionally look up for.",
                        f"I enjoyed parts of '{album.name}' but I don't think I'll come back to all of it."],
            "mid_high":[f"'{album.name}' is good. Like, actually good. I kept it on the whole way through and that's not nothing.",
                        f"'{album.name}' is the kind of album that goes on the rotation. That's what I'm looking for.",
                        f"I had a good time with '{album.name}'. The energy holds and the good moments outweigh the slow ones."],
            "high":    [f"'{album.name}' is great and I mean that simply — I've had it on constantly and I'm not tired of it.",
                        f"'{album.name}' is one of those albums where you finish it and just start it again. That happened.",
                        f"'{album.name}' is genuinely excellent. I sent it to multiple people. They all got it immediately."],
            "perfect": [f"'{album.name}' is a perfect album. I don't have a complicated reason. It just is.",
                        f"I don't know how many times I've listened to '{album.name}'. A lot. That's the review.",
                        f"'{album.name}' is the record I didn't know I needed. Now I can't not have it."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The whole album is {album.core_genre} and it works as a complete thing — I could put it on front to back.",
                         f"The genre is consistent and it keeps the album feeling like an actual album rather than a playlist.",
                         f"Every track fits. The {album.core_genre} identity is clear and that makes the listening experience smooth."])
        elif off <= 2:
            return pick([f"Mostly {album.core_genre} with a couple of small detours that don't derail anything.",
                         f"The genre is pretty consistent — {off} track{'s' if off>1 else ''} depart but not enough to break the flow.",
                         f"The genre diversity is there but it's not disorienting. The album keeps its identity."])
        else:
            return pick([f"The genre jumps around {off} times and I notice it — the album loses its thread a bit.",
                         f"{off} tracks feel like they're from a different record. The {album.core_genre} core keeps pulling me back in.",
                         f"The genre inconsistency is the one thing that stops this from being a front-to-back experience."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8:
            return pick([f"The album flows really well — the {album.core_theme} theme holds throughout and the track order makes sense.",
                         f"I didn't feel any jarring transitions. The {album.core_theme} thread is solid at {pct} and the sequencing respects that.",
                         f"Start to finish this is a smooth listen. The thematic consistency at {pct} is a big part of why."])
        elif ratio >= 0.6:
            return pick([f"The theme is mostly consistent — {pct} on the {album.core_theme} core — with a few moments where the mood shift catches you off guard.",
                         f"Mostly flows well. A few tonal detours but nothing that completely breaks the listen.",
                         f"The theme coherence is good enough. {pct} alignment and the transitions mostly make sense."])
        else:
            return pick([f"The album jumps around a lot thematically — only {pct} on the {album.core_theme} core and I feel those gaps.",
                         f"The track ordering is the weakest part for me. The thematic inconsistency at {pct} makes it hard to relax into.",
                         f"It feels less like an album with a journey and more like a playlist someone organized quickly."])

    def _praise_best(self, song, score):
        if score_tier(score) in ("high", "perfect"):
            return pick([f"'{song.name}' is the one I've played the most by a long way. That track is perfect for what it is.",
                         f"'{song.name}' is the standout — genuinely one of the best songs I've heard recently.",
                         f"'{song.name}' alone made this whole album worth listening to."])
        else:
            return pick([f"'{song.name}' is the album's best moment and I've gone back to it a few times.",
                         f"'{song.name}' is where the album peaks — it's the track I'd play first for someone else.",
                         f"The high point is '{song.name}' and it's a genuinely good high point."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is the one I occasionally skip. Not a problem — just my personal preference.",
                         f"'{song.name}' is the weakest track but in a strong album 'weakest' is still pretty good.",
                         f"'{song.name}' is the brief dip. Every album has one and this is manageable."])
        elif score >= 5:
            return pick([f"'{song.name}' is where I check my phone. It's not bad enough to skip but it doesn't hold me.",
                         f"'{song.name}' is the flat spot in what's otherwise a pretty engaging listen.",
                         f"'{song.name}' is a skip for me. The album's good enough that I don't mind losing a track."])
        else:
            return pick([f"'{song.name}' is a skip every time. It breaks the momentum the album is trying to build.",
                         f"'{song.name}' is the album's one real problem. It doesn't fit and I notice every time.",
                         f"'{song.name}' is not what the rest of the album is. It stands out in the wrong way."])

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
#  ALBUM CRITIC 8 — NINA PASCAL (Balanced)
# ═══════════════════════════════════════════════════════════════

class AlbumNinaPascal(AlbumCritic):
    length_preference    = (9, 14)
    length_short_penalty = -0.3
    length_long_penalty  = -0.3
    length_ideal_bonus   = 0.2

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"'{album.name}' is a record that fails at most of what it attempts — and attempts enough that the failure is hard to overlook.",
                        f"'{album.name}' is underdeveloped across its tracklist in ways that aren't isolated problems — they're structural ones.",
                        f"'{album.name}' shows ambition and a consistent inability to match it with execution."],
            "mid_low": [f"'{album.name}' is a decent album with the skeleton of a good one inside it — the execution didn't fully extract the best version.",
                        f"'{album.name}' occupies a frustrating middle ground: good enough to suggest the potential, not good enough to fully realize it.",
                        f"'{album.name}' is worth hearing once. Whether it's worth returning to is a harder case to make."],
            "mid_high":[f"'{album.name}' is a well-constructed record — the craft is real, the intention is clear, and it mostly does what it sets out to do.",
                        f"'{album.name}' earns its place — consistently engaged, occasionally exceptional, and almost never lazy.",
                        f"'{album.name}' is the kind of album that rewards attention. The detail is there if you're looking for it."],
            "high":    [f"'{album.name}' is a serious piece of work that succeeds in nearly every dimension it attempts.",
                        f"'{album.name}' is exceptional — not in isolated moments but as a complete structural achievement.",
                        f"'{album.name}' is the kind of album that raises the standard for everything made in this genre this year."],
            "perfect": [f"'{album.name}' is a perfect album. I've evaluated thousands of records. I don't use the word 'perfect' carelessly.",
                        f"'{album.name}' achieves total formal and emotional coherence. That is an extremely rare thing and it happened here.",
                        f"'{album.name}' is a complete and flawless record. My job is to say so clearly, and I am."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The genre cohesion is total — every track functions within the {album.core_genre} framework with clear artistic intention.",
                         f"The {album.core_genre} commitment is sustained across the full tracklist. That consistency is a structural asset, not a limitation.",
                         f"Genre coherence is one of the album's formal strengths — the {album.core_genre} identity never wavers and never becomes monotonous."])
        elif off <= 2:
            return pick([f"The core {album.core_genre} identity holds throughout, with {off} departure{'s' if off>1 else ''} that read as deliberate expansion rather than confusion.",
                         f"The genre consistency is strong — {off} off-{album.core_genre} track{'s' if off>1 else ''} register as considered risk rather than directional uncertainty.",
                         f"The genre architecture is sound. Minor variance from the {album.core_genre} base is handled with sufficient intention."])
        else:
            return pick([f"The {off} off-genre tracks represent a real structural challenge. The {album.core_genre} identity is present but contested.",
                         f"Genre inconsistency across {off} tracks is the album's most significant formal problem — it fragments what might otherwise be a coherent statement.",
                         f"The {album.core_genre} core is audible but not dominant enough to absorb {off} departures without identity loss."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8 and flow_mod >= 0:
            return pick([f"The thematic architecture of '{album.name}' is one of its most underappreciated qualities — {pct} {album.core_theme} alignment with transitions that earn their sequencing.",
                         f"The {album.core_theme} thread holds with {pct} alignment and the track-to-track transitions are managed with genuine compositional intelligence.",
                         f"The sequencing is doing real structural work here — the {album.core_theme} coherence at {pct} means the album reads as an argument, not a collection."])
        elif ratio >= 0.6:
            return pick([f"The thematic continuity at {pct} is adequate — the {album.core_theme} foundation holds even if it's occasionally tested.",
                         f"The {album.core_theme} alignment at {pct} creates a workable through-line. The gaps don't break the album but they're felt.",
                         f"Thematic coherence is present without being complete. {pct} alignment is sufficient but not exceptional."])
        else:
            return pick([f"The thematic incoherence is the album's most significant formal weakness — {pct} {album.core_theme} alignment leaves the record without a clear emotional through-line.",
                         f"Only {pct} of the tracklist engages the {album.core_theme} core and the sequencing doesn't compensate for the thematic gaps.",
                         f"The album is structurally weakened by its thematic inconsistency. {pct} alignment doesn't provide enough foundation for a coherent listen."])

    def _praise_best(self, song, score):
        tier = score_tier(score)
        if tier in ("high", "perfect"):
            return pick([f"'{song.name}' is the album's formal peak — the track that most completely realizes the record's stated intentions.",
                         f"'{song.name}' is where the album's structural intelligence and emotional ambition converge completely.",
                         f"'{song.name}' is the defining track — everything the album does well, it does completely here."])
        else:
            return pick([f"'{song.name}' is the album's strongest offering and represents what the record achieves at its best.",
                         f"'{song.name}' is the high point — a track where the album's qualities are most concentrated.",
                         f"The album's best case is made on '{song.name}', which is genuinely successful on its own terms."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is the album's most modest contribution — still strong relative to most records, slightly below the standard set here.",
                         f"'{song.name}' is where the album gives the least. In context, the least is still considerable.",
                         f"'{song.name}' is the one I'd point to as the album's structural concession — it softens the impact slightly without derailing it."])
        elif score >= 5:
            return pick([f"'{song.name}' is where the record's ambition and execution diverge most visibly.",
                         f"'{song.name}' is the album's weakest structural point — a track that doesn't rise to the level of its surroundings.",
                         f"'{song.name}' is a genuine dip. It's not catastrophic but it's measurable and it costs the album something."])
        else:
            return pick([f"'{song.name}' is a significant problem — a track that undermines the record's coherence and credibility in ways the other material can't fully compensate for.",
                         f"'{song.name}' is the album's most serious formal failure. It shouldn't be here and its presence costs the whole record.",
                         f"'{song.name}' is where the album loses its claim to being fully realized. The gap between it and the rest is too wide."])

    def _closing(self, album, score, tier):
        verdict = pick(VERDICTS["contrarian"].get(int(round(score)), ["it is what it is."]))
        remarks = {
            "low":     f"'{album.name}' fails more than it succeeds, and that ratio is too unfavorable to recommend.",
            "mid_low": f"'{album.name}' has the components of a better record and doesn't assemble them correctly.",
            "mid_high":f"'{album.name}' is a well-made record that succeeds at most of what it attempts.",
            "high":    f"'{album.name}' is an exceptional record by nearly any formal or emotional measure.",
            "perfect": f"'{album.name}' is a perfect record. That assessment is defensible by every criterion I apply.",
        }
        return f"{remarks.get(tier, remarks['mid_high'])} {ensure_punct(verdict)}"


# ═══════════════════════════════════════════════════════════════
#  ALBUM CRITIC 9 — TEENA NARUKA (Shatam Rai obsessed)
# ═══════════════════════════════════════════════════════════════

class AlbumTeenaNaruka(AlbumCritic):
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
    ]

    def _opening(self, album, score, tier):
        lines = {
            "low":     [f"Okay so '{album.name}' is rough. Shatam Rai wouldn't give this the time of day.",
                        f"'{album.name}' didn't hit for me and I really wanted it to.",
                        f"I gave '{album.name}' a full honest listen. It didn't earn it."],
            "mid_low": [f"'{album.name}' is fine? It's fine. It's not memorable but it's fine.",
                        f"'{album.name}' tries and gets about halfway there. Halfway is something.",
                        f"'{album.name}' has its moments and I genuinely enjoyed some of them. Some."],
            "mid_high":[f"Okay '{album.name}' is actually pretty good. Not Shatam Rai good but like, actually good.",
                        f"'{album.name}' kept me listening all the way through and that is a genuine compliment.",
                        f"'{album.name}' is solid! I was into it. More than I expected."],
            "high":    [f"'{album.name}' is really good and I've been saying that to everyone I know.",
                        f"'{album.name}' is an eight minimum and I'm rounding up with zero guilt.",
                        f"I've been playing '{album.name}' constantly. Like, constantly. My friends have noticed."],
            "perfect": [f"'{album.name}' is a perfect album. I'm saying that clearly and I mean it.",
                        f"'{album.name}' is in the Shatam Rai tier. I have never said that about any album. I'm saying it now.",
                        f"'{album.name}' is the best album I've heard in a very long time and I'm not calm about it."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The whole album is {album.core_genre} and it flows perfectly because of that. Love when an album knows what it is.",
                         f"Zero genre drift — the {album.core_genre} identity is consistent and it makes the album feel intentional.",
                         f"Full {album.core_genre} record and it earns that commitment completely."])
        elif off <= 2:
            return pick([f"Mostly {album.core_genre} with {off} little detour{'s' if off>1 else ''} that don't break anything.",
                         f"The genre is mostly consistent and the {off} departure{'s' if off>1 else ''} actually add something.",
                         f"The {album.core_genre} core is intact even with {off} side trip{'s' if off>1 else ''}. The album survives it well."])
        else:
            return pick([f"{off} tracks step outside the {album.core_genre} lane and the album loses something each time.",
                         f"The genre inconsistency over {off} tracks is the one thing I keep coming back to as a problem.",
                         f"The {album.core_genre} identity gets fuzzy {off} times. I noticed every time."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8:
            return pick([f"The {album.core_theme} thread runs the whole album and the sequencing respects it. This is how you build a full listen.",
                         f"Thematically consistent at {pct} and the track order makes emotional sense. The album flows.",
                         f"The theme is locked at {pct} alignment and the listening experience is seamless because of it."])
        elif ratio >= 0.6:
            return pick([f"The {album.core_theme} theme holds for {pct} and the rest is manageable drift. Good enough.",
                         f"Some thematic inconsistency but not enough to break the experience. {pct} on core is fine.",
                         f"The album drifts from the {album.core_theme} theme occasionally but recovers. The {pct} alignment holds the shape."])
        else:
            return pick([f"Only {pct} thematic consistency — the album jumps around and I feel it during the listen.",
                         f"The theme logic isn't there. {pct} on {album.core_theme} and it shows in how disconnected some tracks feel.",
                         f"The thematic drift is real and the album suffers for it. {pct} alignment isn't enough."])

    def _praise_best(self, song, score):
        if score_tier(score) in ("high", "perfect"):
            return pick([f"'{song.name}' is the standout and it's not even close — that track is the reason I'll still be playing this album next year.",
                         f"'{song.name}' is the moment I texted people. The best thing here by a significant margin.",
                         f"'{song.name}' alone makes the whole album worth it. It's that good."])
        else:
            return pick([f"'{song.name}' is the best the album offers and it's a genuinely good best.",
                         f"'{song.name}' is the track I keep coming back to — the album's peak.",
                         f"The high point is '{song.name}' and it's a real high point."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is the one I skip sometimes. Minor complaint for a strong album.",
                         f"'{song.name}' is the weakest track which in this context just means the nine instead of the ten.",
                         f"'{song.name}' dips a little. The album doesn't notice."])
        elif score >= 5:
            return pick([f"'{song.name}' doesn't hit the way the rest does. It's the album's speed bump.",
                         f"'{song.name}' is fine but it's not what the surrounding tracks are. The gap is noticeable.",
                         f"'{song.name}' is the one Shatam Rai would probably skip. I sometimes do."])
        else:
            return pick([f"'{song.name}' is not good and it's on an otherwise good album which makes it worse somehow.",
                         f"'{song.name}' is the mistake. Every album can have one but this one costs real momentum.",
                         f"'{song.name}' shouldn't be here. I said it. Someone had to."])

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks I wanted more. The album just got going.",
                         f"{n} tracks ends too soon. This album had more to give."])
        elif n > self.length_preference[1]:
            return pick([f"{n} tracks is a lot. A few could have been cut.",
                         f"The album goes on {n} tracks and about two of those are filler. Cut them next time."])
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
            "low":     [f"'{album.name}' is a difficult listen and not in the rewarding kind of way.",
                        f"'{album.name}' didn't reach me and I kept the door open for most of the runtime.",
                        f"'{album.name}' is below the standard I apply to records I want to talk about."],
            "mid_low": [f"'{album.name}' is a record with ideas that don't fully materialize. It's an almost-album.",
                        f"'{album.name}' is better than its weakest moments and worse than its best ones — the average lands somewhere in the middle.",
                        f"'{album.name}' is a decent record that could have been a great one with more time or more decisions."],
            "mid_high":[f"'{album.name}' is a well-made record that earns its place in the conversation.",
                        f"'{album.name}' does enough of the right things right to be worth someone's time.",
                        f"'{album.name}' is a real record — committed, considered, and mostly successful."],
            "high":    [f"'{album.name}' is genuinely excellent and I've been looking for a way to say that more precisely. I can't — it's just excellent.",
                        f"'{album.name}' is the kind of record that makes me want to go back to the beginning and listen again before I've finished it.",
                        f"'{album.name}' is one of the stronger records I've reviewed this year. That's the honest assessment."],
            "perfect": [f"'{album.name}' is a perfect album. I'm stating that formally and without hesitation.",
                        f"'{album.name}' is everything a record is supposed to be. Complete.",
                        f"'{album.name}' is the album I'll be referencing when I talk about this era. That's what a perfect record does."],
        }
        return pick(lines.get(tier, lines["mid_high"]))

    def _cohesion(self, album, on, off, tier):
        if off == 0:
            return pick([f"The {album.core_genre} commitment is complete — the album sounds like a single unified statement from first track to last.",
                         f"Total genre coherence across the tracklist. The {album.core_genre} identity is the album's structural backbone.",
                         f"No genre confusion. The {album.core_genre} framework holds from front to back and the album is stronger for it."])
        elif off <= 2:
            return pick([f"The {album.core_genre} core holds throughout, with {off} departure{'s' if off>1 else ''} that add texture without threatening the identity.",
                         f"Minor genre excursions that feel intentional rather than accidental. The {album.core_genre} foundation is secure.",
                         f"The {off} off-genre track{'s' if off>1 else ''} work as breathing room. The album's identity is never in doubt."])
        else:
            return pick([f"The genre drift at {off} tracks is a structural problem — the {album.core_genre} identity is present but not dominant.",
                         f"{off} off-genre tracks fragment the album in ways that are hard to read as deliberate experimentation.",
                         f"The cohesion issue is real. {off} departures from the {album.core_genre} core leave the album without a secure identity."])

    def _continuity(self, album, ratio, flow_mod, tier):
        pct = _pct(ratio)
        if ratio >= 0.8 and flow_mod >= 0:
            return pick([f"The {album.core_theme} through-line holds at {pct} alignment and the sequencing works with rather than against it — the result is an album that genuinely flows.",
                         f"Thematic coherence is one of this album's real strengths — {pct} on {album.core_theme} and the transitions between tracks are handled with care.",
                         f"The album reads as a complete emotional statement rather than a collection of songs. The {pct} {album.core_theme} alignment and the sequencing together make that possible."])
        elif ratio >= 0.6:
            return pick([f"Thematic coherence is workable at {pct} — the {album.core_theme} core is present enough to create a through-line even if it's occasionally interrupted.",
                         f"The {album.core_theme} alignment at {pct} is sufficient for the album to cohere, even if the drift is occasionally felt.",
                         f"The theme is mostly consistent and the gaps don't fundamentally undermine the album's sense of purpose."])
        else:
            return pick([f"The thematic incoherence at {pct} {album.core_theme} alignment is the album's most significant structural weakness.",
                         f"Only {pct} of the album engages the {album.core_theme} core and the sequencing doesn't compensate for those gaps.",
                         f"The album lacks a coherent thematic argument. {pct} alignment doesn't provide enough of a spine for this length of record."])

    def _praise_best(self, song, score):
        tier = score_tier(score)
        if tier in ("high", "perfect"):
            return pick([f"'{song.name}' is the record's centerpiece — the track that justifies everything surrounding it.",
                         f"'{song.name}' is what the album is building toward and it arrives there completely.",
                         f"'{song.name}' is exceptional and I don't use that word loosely. The album is worth hearing for this track alone."])
        else:
            return pick([f"'{song.name}' is the album's strongest track and demonstrates the upper limit of what the record can achieve.",
                         f"'{song.name}' is where the album fully realizes its potential.",
                         f"The best the album offers is '{song.name}', and the best is genuinely good."])

    def _critique_worst(self, song, score):
        if score >= 8:
            return pick([f"'{song.name}' is where the album is at its least — which in the context of this record means still above average.",
                         f"'{song.name}' is the album's softest moment. A small concession in an otherwise strong record.",
                         f"If I'm being precise, '{song.name}' is where the record gives the least. It gives less than everything else here."])
        elif score >= 5:
            return pick([f"'{song.name}' is where the album loses momentum it worked hard to build.",
                         f"'{song.name}' is the record's weak link — not badly made, just not at the level of its surroundings.",
                         f"'{song.name}' is the one I'd point to as a missed opportunity. The album would be tighter without it."])
        else:
            return pick([f"'{song.name}' is a real problem. It doesn't belong in the company of the other tracks and its presence costs the album.",
                         f"'{song.name}' is the album's most significant misstep and I can't account for its placement on the tracklist.",
                         f"'{song.name}' is where the album breaks down. It's a genuine failure in an otherwise serious record."])

    def _length_note(self, album):
        n = album.song_count()
        if n < self.length_preference[0]:
            return pick([f"At {n} tracks the album ends before it's fully arrived. It needed more room.",
                         f"{n} tracks is lean for the statement this album is attempting."])
        elif n > self.length_preference[1]:
            return pick([f"The album tests its welcome slightly at {n} tracks — a tighter edit would serve the stronger material better.",
                         f"{n} tracks is a few more than necessary. The album's best work would shine brighter with less surrounding it."])
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
        # Pair each song-critic with its album-critic wrapper
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
        meta = (f"Core Genre: {album.core_genre}  |  "
                f"Core Theme: {album.core_theme}  |  "
                f"{album.song_count()} tracks  |  "
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

        all_album_scores = []
        all_track_scores_by_critic = []

        for ac in self.album_critics:
            album_score, song_scores, review_text = ac.write_review(album)
            all_album_scores.append(album_score)
            all_track_scores_by_critic.append((ac, album_score, song_scores))

            print(f"  ★  {ac.name}  [{ac.tagline}]")
            print(f"  {'─' * 60}")
            _wrap_print(review_text)
            print()
            # Per-track scores
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
        print(f"  🏆 Best Track:   {album.songs[best_ti].name}  ({avg_per_track[best_ti]}/10)")
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

def fmt_duration(secs):
    return f"{secs // 60}:{secs % 60:02d}"


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

        # ── ALBUM SETUP ───────────────────────────────────────────
        print()
        album_name  = input("  Album name: ").strip() or "Untitled Album"
        core_genre  = select_core_genre()
        core_theme  = select_core_theme()
        album       = Album(album_name, core_genre, core_theme)

        print()
        print(f"  ┌─────────────────────────────────────────────────────┐")
        print(f"  │  Album created: '{album_name}'")
        print(f"  │  Core Genre: {core_genre}  |  Core Theme: {core_theme}")
        print(f"  │  Minimum songs to publish: {MIN_SONGS}")
        print(f"  └─────────────────────────────────────────────────────┘")

        # ── SONG LOOP ─────────────────────────────────────────────
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
                # publish
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
