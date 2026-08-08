"""Album review foundations split out from albumreviewproto3.py."""

import random
from collections import Counter

from rapsim_reviews.track_review import (
    Song, GENRES, THEMES,
    MarcusVane, DejaHayes, VicOsei, RayColdwell,
    EarlMosely, ZaraNights, TobiasLund, NinaPascal,
    TeenaNaruka, ShatamRai,
    pick, picks, clamp, score_tier, bias_scale,
    ensure_punct, join_sentences, fmt_duration,
    VERDICTS,
)

MIN_SONGS  = 7
WRAP_WIDTH = 74

# ─────────────────────────────────────────────
#  THEME COMPATIBILITY MAP
# ─────────────────────────────────────────────

COMPATIBLE_TRANSITIONS = {
    # Every theme must list all 9 others in either compatible or incompatible.
    # This is the "flows INTO" map: from_theme in COMPATIBLE_TRANSITIONS[to_theme]
    "heartbreak"  : {"love", "nostalgia", "rage", "existential", "spirituality", "protest"},
    "party"       : {"euphoria", "love", "street life", "rage", "nostalgia"},
    "protest"     : {"rage", "street life", "existential", "nostalgia", "spirituality", "heartbreak"},
    "nostalgia"   : {"heartbreak", "love", "spirituality", "euphoria", "protest", "existential"},
    "love"        : {"heartbreak", "nostalgia", "euphoria", "spirituality", "existential", "party"},
    "existential" : {"heartbreak", "spirituality", "nostalgia", "protest", "rage", "love"},
    "street life" : {"rage", "protest", "heartbreak", "existential", "party", "nostalgia"},
    "spirituality": {"nostalgia", "existential", "love", "heartbreak", "protest", "euphoria"},
    "rage"        : {"protest", "street life", "heartbreak", "existential", "party", "nostalgia"},
    "euphoria"    : {"love", "party", "spirituality", "nostalgia"},
}

INCOMPATIBLE_TRANSITIONS = {
    # Every theme's remaining 9 others (not in compatible) are incompatible.
    "heartbreak"  : {"party", "euphoria", "street life"},
    "party"       : {"heartbreak", "existential", "spirituality", "protest"},
    "protest"     : {"party", "euphoria", "love"},
    "nostalgia"   : {"rage", "party", "street life"},
    "love"        : {"rage", "protest", "street life"},
    "existential" : {"party", "euphoria", "street life"},
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
                                  "that mood shift is too large to be intentional and too abrupt to be forgiven.",
                                  "going from that deeply philosophical track straight into pure euphoria — someone needed to intervene."],
    ("heartbreak", "street life"):["heartbreak straight into street life — those two worlds need a bridge the sequencing doesn't provide.",
                                    "the emotional gear shift from that heartbreak track to the street life one is jarring without a transition."],
    ("love", "existential"):      ["moving from love directly into existential territory — the emotional logic works but the transition needs more runway.",
                                    "the mood shift from that love track into the existential one is abrupt in a way that costs the album."],
    ("protest", "nostalgia"):     ["protest into nostalgia in one track — the political tension dissolves too fast and the album loses momentum.",
                                    "you can't be that angry and then suddenly wistful without losing the audience."],
    ("street life", "love"):      ["street life straight into a love song — the tonal shift is too abrupt to feel intentional.",
                                    "going from that street life gravity into a love track with no transition is a sequencing risk that doesn't pay off."],
    ("nostalgia", "existential"): ["nostalgia into existential is actually a natural progression — but the transition here is too abrupt to feel earned.",
                                    "the jump from nostalgic into philosophical is a risk; this one almost works but not quite."],
    ("protest", "heartbreak"):    ["going from protest into heartbreak with no runway — the political energy and the personal grief are compatible but need space to breathe.",
                                    "protest into heartbreak back to back — the tonal shift is jarring in a way a single bridge could have fixed."],
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
#  BORING METER
#  Penalises consecutive same-theme runs > 3 tracks.
#  After 4th same: penalty_per_extra (critic-specific).
#  After 5th same: 2x penalty. 6th: 3x. And so on.
#  Total penalty capped at 2.0 across the whole album.
#  Resets as soon as a different theme appears.
# ─────────────────────────────────────────────

def compute_boring_penalty(album, penalty_per_extra):
    """
    Walk the tracklist. Whenever a theme streak exceeds 3, apply:
      streak_length - 3  multiples of penalty_per_extra.
    Cap total at 2.0.
    Returns (total_penalty_float, boring_details)
      boring_details = list of (theme, streak_len) that triggered penalty
    """
    songs  = album.songs
    if len(songs) < 4:
        return 0.0, []

    total   = 0.0
    details = []
    i       = 0
    while i < len(songs):
        theme = songs[i].theme
        j     = i + 1
        while j < len(songs) and songs[j].theme == theme:
            j += 1
        streak = j - i
        if streak > 3:
            extra    = streak - 3
            hit      = round(extra * penalty_per_extra, 3)
            total   += hit
            details.append((theme, streak))
        i = j

    return round(min(total, 2.0), 3), details


BORING_COMMENTS = {
    # Keys match personality values: "strict", "balanced", "generous", "hype"
    # Every entry should contain a word like boring/repetitive/monoton/slog/loop
    "strict": [
        "despite whatever individual merits exist here, this album is boring — and I mean that as a formal diagnosis, not a preference.",
        "the tracklist commits the cardinal sin of sequencing: it runs the same emotional note until it becomes wallpaper.",
        "a record can have strong songs and still be a boring album. this achieves exactly that.",
        "the thematic repetition here isn't depth — it's a loop. the album confuses consistency with insight.",
        "I've listened to this album twice. the second time felt exactly like the first. that's not a compliment.",
        "this is the kind of album that makes you feel like you've been listening for longer than you actually have. not in a good way.",
    ],
    "hype": [
        "okay I love the individual tracks but the album as a whole? it's honestly a bit boring — same vibe for too long.",
        "the vibes started great and then the album just kept being the same vibe and it wore me out.",
        "I genuinely fell asleep during my second listen. the album is repetitive in a way that kills the momentum.",
        "great songs, repetitive sequencing — the album is basically playing the same emotional card over and over.",
        "the theme repetition kills the momentum. the album needed a left turn it never took.",
    ],
    "balanced": [
        "the thematic repetition here is a structural issue worth naming — the album becomes monotonous before it ends.",
        "the album is repetitive in a way that outlasts its welcome, regardless of the quality of individual tracks.",
        "despite good songs, this album is boring in the way only a well-intentioned album can be boring.",
        "the sequencing here is the record's own worst enemy — the same theme repeated too many times in a row drains what the good tracks built.",
        "the album loses energy not because the songs are weak but because the track ordering creates a loop rather than a journey.",
    ],
    "generous": [
        "the album is slightly boring despite the quality of the songs — the thematic repetition adds up across the runtime.",
        "the only thing working against this album is its own sequencing — too many consecutive same-theme tracks create monotony.",
        "despite good songs, this album is more repetitive than it needed to be and the listening experience suffers for it.",
        "the repetition is the one thing I'd fix — the individual tracks deserve a more varied sequence than they got.",
        "the album gets a little boring in stretches. that's the honest word for it.",
    ],
}

def get_boring_comment(personality, album_name):
    pool = BORING_COMMENTS.get(personality, BORING_COMMENTS["balanced"])
    line = pick(pool)
    return line.replace("'{album}'", f"'{album_name}'")

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

    # Boring meter: penalty applied per extra track beyond streak-of-3
    # strict critics punish harder, hype/casual critics barely care
    boring_penalty_per_extra = 0.15  # base — overridden per subclass

    def __init__(self, critic):
        self.critic = critic

    @property
    def name(self):    return self.critic.name
    @property
    def tagline(self): return self.critic.tagline

    # ── song score guard ──────────────────────────────────────────
    def _guard_song_score(self, song, raw_score):
        """
        Post-process individual song scores to enforce realism.
        A song only gets a 10 if:
          - quality == 10
          - critic loves the genre
          - critic loves the theme
          - duration is in the critic's acceptable range
        A strict personality critic further compresses the top end.
        Also enforces Vic Osei-style hard ceiling where personality='strict'
        AND base_modifier is very low (e.g. VicOsei base_modifier = -2.5).
        """
        # Hard ceiling: a score ≥9.0 requires the critic to genuinely love genre+theme
        # AND the song must have quality=10 AND acceptable duration.
        if raw_score >= 9.0:
            genre_loved = any(g in self.critic.loved_genres for g in song.genres)
            theme_loved = song.theme in self.critic.loved_themes
            quality_top = song.quality >= 10
            dur_ok      = 120 <= song.duration <= 360
            if not (genre_loved and theme_loved and quality_top and dur_ok):
                # Compress: if they don't love genre+theme it can't be a 9+
                excess   = raw_score - 8.0
                raw_score = round(8.0 + excess * 0.25, 1)

        # Vic Osei special ceiling: his base_modifier is -2.5, personality strict.
        # Hard cap at 7.0; anything above is compressed aggressively.
        if self.personality == "strict" and getattr(self.critic, "base_modifier", 0) <= -2.0:
            if raw_score > 7.0:
                excess    = raw_score - 7.0
                raw_score = round(7.0 + excess * 0.20, 1)  # hard compress: 9.8 → 7.56 → rounds to 7.6

        return clamp(raw_score)

    # ── album score ────────────────────────────────────────────────
    def compute_album_score(self, album):
        song_scores = [self._guard_song_score(s, self.critic.compute_score(s)) for s in album.songs]

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

        boring_pen, boring_details = compute_boring_penalty(album, self.boring_penalty_per_extra)

        raw = (base
               - cohesion_pen  * self.cohesion_sensitivity
               + theme_mod     * self.theme_sensitivity
               + flow_mod      * self.flow_sensitivity
               + length_mod    * self.length_sensitivity
               - boring_pen)

        # Apply personality score curve (prevents inflation for strict critics)
        # Additional hard ceiling: album score cannot exceed 9.6 unless the album
        # truly deserves it (all songs high, critic loves core genre+theme, not boring).
        raw_pre_curve = raw
        final = apply_score_curve(raw, self.personality)

        # Album 10/10 gate — only give near-perfect album scores under ideal conditions
        if final >= 9.5:
            all_high       = all(sc >= 8.0 for sc in song_scores)
            no_boring      = boring_pen == 0.0
            loves_genre    = album.core_genre in self.critic.loved_genres
            likes_theme    = album.core_theme in self.critic.loved_themes
            _, off_genre   = album.cohesion_stats()
            pure_cohesion  = off_genre <= 1
            ratio          = album.theme_alignment_ratio()
            strong_theme   = ratio >= 0.75
            if not (all_high and no_boring and loves_genre and likes_theme and pure_cohesion and strong_theme):
                # Compress back toward 9.0
                excess = final - 9.0
                final  = round(9.0 + excess * 0.3, 1)

        return final, song_scores, boring_pen, boring_details

    # ── prose review ───────────────────────────────────────────────
    def write_review(self, album):
        album_score, song_scores, boring_pen, boring_details = self.compute_album_score(album)
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

        # Boring meter commentary — inject if album had repetitive runs
        if boring_pen > 0:
            boring_comment = get_boring_comment(self.personality, album.name)
            paragraphs.append(boring_comment)

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
