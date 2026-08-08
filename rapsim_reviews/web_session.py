"""Web-facing game session: runs career_mode actions with bridged I/O."""

from __future__ import annotations

import io
import uuid
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass, field
from typing import Any, Callable

from rapsim_reviews.album_review import AlbumSimulation
from rapsim_reviews.artist_ecosystem_sim import create_world, step_world
from rapsim_reviews.beat_system import ensure_beat_market, vault_beats
from rapsim_reviews.track_review import Simulation
from rapsim_reviews.web_io import NeedInput, WebIO

# In-memory sessions (single-player local UI).
_SESSIONS: dict[str, "GameSession"] = {}


ACTION_CATALOG: list[dict[str, Any]] = [
    {"id": 1, "label": "Ghostwrite (+1 lyrics)", "category": "Training"},
    {"id": 2, "label": "Open mic (+1 vocals)", "category": "Training"},
    {"id": 3, "label": "Produce (+1 production)", "category": "Training"},
    {"id": 4, "label": "Mix/master (+1 mix/master)", "category": "Training"},
    {"id": 5, "label": "Start genre course", "category": "Training"},
    {"id": 6, "label": "Create album draft", "category": "Music"},
    {"id": 7, "label": "Create song", "category": "Music"},
    {"id": 8, "label": "Create deluxe draft", "category": "Music"},
    {"id": 9, "label": "Release music", "category": "Music"},
    {"id": 10, "label": "Go live", "category": "Career"},
    {"id": 11, "label": "Work side hustle", "category": "Career"},
    {"id": 12, "label": "Media management", "category": "Career"},
    {"id": 13, "label": "Shawtify streams", "category": "Charts"},
    {"id": 14, "label": "New releases", "category": "World"},
    {"id": 15, "label": "View artists", "category": "World"},
    {"id": 16, "label": "Release calendar", "category": "World"},
    {"id": 17, "label": "NEWS", "category": "World"},
    {"id": 18, "label": "TWITTER", "category": "World"},
    {"id": 19, "label": "User ratings (IMDb)", "category": "World"},
    {"id": 20, "label": "Manage relationships", "category": "Social"},
    {"id": 33, "label": "NUMBLE", "category": "Social"},
    {"id": 34, "label": "Your Love Relationships", "category": "Social"},
    {"id": 21, "label": "Catalog manager", "category": "Music"},
    {"id": 22, "label": "Feature requests", "category": "Social"},
    {"id": 23, "label": "Simulate next week", "category": "Time"},
    {"id": 24, "label": "Simulate 52 weeks", "category": "Time"},
    {"id": 25, "label": "HOT 100", "category": "Charts"},
    {"id": 26, "label": "Grammys", "category": "Charts"},
    {"id": 27, "label": "Diss tracks", "category": "World"},
    {"id": 28, "label": "Love relationships", "category": "Social"},
    {"id": 29, "label": "Separated relationships", "category": "Social"},
    {"id": 30, "label": "Create beats", "category": "Beats"},
    {"id": 31, "label": "Beat Vault", "category": "Beats"},
    {"id": 32, "label": "Beat Store", "category": "Beats"},
    {"id": 37, "label": "Concerts", "category": "Career"},
    {"id": 38, "label": "Manage Venue", "category": "Career"},
    {"id": 39, "label": "Quit", "category": "Session"},
]


def create_artist_with_options(
    name: str = "Untitled Artist",
    gender: str = "male",
    sexuality: str = "straight",
    skill_names: list[str] | None = None,
    genre_names: list[str] | None = None,
):
    """Programmatic artist creation for the web UI (skips CLI prompts)."""
    import random

    from rapsim_reviews.artist_ecosystem_seed import ARTIST_ECOSYSTEM_SEEDS
    from rapsim_reviews.career_mode import (
        GENRES,
        SKILLS,
        TEST_RELATIONSHIP_BOOTSTRAP,
        TEST_RELATIONSHIP_LOCK,
        TEST_START_MAXED,
        TEST_START_MONEY,
        TEST_START_POPULARITY,
        Artist,
        RelationshipState,
        _romance_preference_from_identity,
        _validate_gender,
        _validate_sexuality_for_gender,
        clamp_meter,
    )

    chosen_skills = skill_names or ["lyrics", "vocals"]
    chosen_genres = genre_names or ["hip hop", "pop"]
    chosen_skills = [s for s in chosen_skills if s in SKILLS][:2] or ["lyrics", "vocals"]
    chosen_genres = [g for g in chosen_genres if g in GENRES][:2] or ["hip hop", "pop"]

    if TEST_START_MAXED:
        skills = {skill: 90 for skill in SKILLS}
        genres = {genre: 90 for genre in GENRES}
    else:
        skills = {skill: 25 for skill in SKILLS}
        for skill in chosen_skills:
            skills[skill] = 60
        genres = {genre: 30 for genre in GENRES}
        for genre in chosen_genres:
            genres[genre] = 60

    g = _validate_gender(gender)
    sx = _validate_sexuality_for_gender(g, sexuality)
    artist = Artist(
        name=name.strip() or "Untitled Artist",
        skills=skills,
        genres=genres,
        gender=g,
        sexuality=sx,
        romance_preference=_romance_preference_from_identity(g, sx),
    )
    if TEST_START_MAXED:
        artist.money = float(TEST_START_MONEY)
        artist.popularity_state.organic = float(TEST_START_POPULARITY)
        artist.reputation = 90.0
    if TEST_RELATIONSHIP_BOOTSTRAP:
        seeds = sorted(ARTIST_ECOSYSTEM_SEEDS, key=lambda s: s.name.lower())
        for seed in seeds:
            score = 100.0 if TEST_RELATIONSHIP_LOCK else 20.0
            artist.relationships[seed.name] = RelationshipState(
                score=score,
                last_interaction_week=0,
                last_contact_week=0,
            )
        if TEST_RELATIONSHIP_LOCK:
            setattr(artist, "_relationship_lock", True)
    else:
        for seed in ARTIST_ECOSYSTEM_SEEDS:
            friendly = int(getattr(seed, "friendliness", 50))
            base = random.uniform(5.0, 12.0) + (friendly / 100.0) * 18.0
            artist.relationships[seed.name] = RelationshipState(
                score=clamp_meter(base),
                last_interaction_week=0,
                last_contact_week=0,
            )
    ensure_beat_market(artist)
    return artist


@contextmanager
def _patch_career_io(web_io: WebIO):
    import builtins

    import rapsim_reviews.career_mode as cm

    saved = {
        "prompt_text": cm.prompt_text,
        "prompt_int": cm.prompt_int,
        "builtin_input": builtins.input,
        "choose_from_list": cm.choose_from_list,
        "choose_item_from_list": cm.choose_item_from_list,
        "choose_unique_items": cm.choose_unique_items,
    }
    cm.prompt_text = web_io.prompt_text
    cm.prompt_int = web_io.prompt_int
    builtins.input = web_io.input
    cm.choose_from_list = web_io.choose_from_list

    def choose_item_from_list(title, options, allow_cancel=False):
        idx = web_io.choose_from_list(title, options, allow_cancel=allow_cancel)
        if idx is None:
            return None
        return options[idx]

    def choose_unique_items(title, options, count):
        chosen = []
        while len(chosen) < count:
            remaining = [opt for opt in options if opt not in chosen]
            idx = web_io.choose_from_list(
                f"{title} ({len(chosen) + 1}/{count})",
                remaining,
                allow_cancel=False,
            )
            chosen.append(remaining[idx])
        return chosen

    cm.choose_item_from_list = choose_item_from_list
    cm.choose_unique_items = choose_unique_items
    try:
        yield
    finally:
        builtins.input = saved.pop("builtin_input")
        for key, value in saved.items():
            setattr(cm, key, value)


@dataclass
class GameSession:
    session_id: str
    artist: Any
    track_sim: Simulation = field(default_factory=Simulation)
    album_sim: AlbumSimulation = field(default_factory=AlbumSimulation)
    ecosystem_world: Any = field(default=None)
    web_io: WebIO = field(default_factory=WebIO)

    @classmethod
    def new_game(
        cls,
        name: str = "Untitled Artist",
        gender: str = "male",
        sexuality: str = "straight",
        skills: list[str] | None = None,
        genres: list[str] | None = None,
    ) -> "GameSession":
        from rapsim_reviews.career_mode import NewsModule, TwitterModule

        artist = create_artist_with_options(name, gender, sexuality, skills, genres)
        world = create_world()
        world.news_module = NewsModule()
        world.twitter_module = TwitterModule()
        step_world(world)
        session = cls(
            session_id=str(uuid.uuid4()),
            artist=artist,
            ecosystem_world=world,
        )
        _SESSIONS[session.session_id] = session
        return session

    @staticmethod
    def get(session_id: str) -> "GameSession | None":
        return _SESSIONS.get(session_id)

    def snapshot(self) -> dict[str, Any]:
        from rapsim_reviews.career_mode import SKILLS

        market = ensure_beat_market(self.artist)
        vault = vault_beats(market)
        unreleased_singles = [e for e in self.artist.singles if not e.released]
        unreleased_albums = [e for e in self.artist.albums if not e.released]
        return {
            "session_id": self.session_id,
            "artist": {
                "name": self.artist.name,
                "year": self.artist.year,
                "week": self.artist.week,
                "health": round(float(self.artist.health), 1),
                "fatigue": round(float(self.artist.fatigue), 1),
                "popularity": round(float(self.artist.popularity), 1),
                "money": float(self.artist.money),
                "reputation": round(float(self.artist.reputation), 1),
                "skills": {s: self.artist.skills[s] for s in SKILLS},
                "genres": {
                    g: v for g, v in self.artist.genres.items() if int(v) > 10
                },
                "course": self.artist.current_course,
                "course_weeks_left": self.artist.course_weeks_left,
                "management": bool(self.artist.management),
                "side_hustle": bool(self.artist.side_hustle),
                "unreleased_singles": len(unreleased_singles),
                "album_drafts": len(unreleased_albums),
                "vault_beats": len(vault),
                "last_week_streams": int(self.artist.last_week_streams),
                "last_week_earnings": float(self.artist.last_week_earnings),
                "live_performance_rating": round(float(self.artist.live_performance_rating), 1) if getattr(self.artist, "concert_history", None) else 0.0,
                "owned_operational_venues": sum(1 for v in getattr(self.artist, "owned_venues", []) if v.status == "operational"),
                "owned_construction_venues": sum(1 for v in getattr(self.artist, "owned_venues", []) if v.status == "construction"),
                "current_love": (
                    {
                        "partner": current_love.partner_name,
                        "lovingness": round(float(current_love.lovingness), 1),
                        "strength": round(float(current_love.strength), 1),
                        "status": current_love.status,
                    }
                    if (current_love := next((rel for rel in reversed(getattr(self.artist, "love_relationships", [])) if rel.status == "current"), None))
                    else None
                ),
            },
            "actions": ACTION_CATALOG,
        }

    def _dispatch_table(self) -> dict[int, Callable[[], None]]:
        from rapsim_reviews.career_mode import (
            beat_store_menu,
            beat_vault_menu,
            catalog_menu,
            create_album_draft,
            create_beats_action,
            create_deluxe_draft,
            create_song_for_artist,
            diss_tracks_menu,
            go_live_action,
            grammy_awards_menu,
            management_menu,
            news_menu,
            practice_skill,
            release_calendar_menu,
            release_menu,
            show_hot_100,
            show_shawtify_streams,
            simulate_many_weeks,
            simulate_week,
            start_genre_course,
            twitter_menu,
            user_ratings_menu,
            view_ecosystem_artists_menu,
            view_ecosystem_new_releases,
            view_feature_requests_menu,
            view_love_relationships_menu,
            view_separated_relationships_menu,
            work_side_hustle,
            manage_relationships_menu,
            numble_menu,
            player_love_relationships_menu,
        )
        from rapsim_reviews.concert_system import concerts_menu
        from rapsim_reviews.venue_management import venue_management_menu

        a = self.artist
        w = self.ecosystem_world
        return {
            1: lambda: practice_skill(a, "lyrics"),
            2: lambda: practice_skill(a, "vocals"),
            3: lambda: practice_skill(a, "production"),
            4: lambda: practice_skill(a, "mix/master"),
            5: lambda: start_genre_course(a),
            6: lambda: create_album_draft(a),
            7: lambda: create_song_for_artist(a),
            8: lambda: create_deluxe_draft(a),
            9: lambda: release_menu(a, self.track_sim, self.album_sim),
            10: lambda: go_live_action(a),
            11: lambda: work_side_hustle(a),
            12: lambda: management_menu(a),
            13: lambda: show_shawtify_streams(a),
            14: lambda: view_ecosystem_new_releases(w),
            15: lambda: view_ecosystem_artists_menu(w),
            16: lambda: release_calendar_menu(w),
            17: lambda: news_menu(a, w),
            18: lambda: twitter_menu(w),
            19: lambda: user_ratings_menu(a, w),
            20: lambda: manage_relationships_menu(a, w),
            21: lambda: catalog_menu(a),
            22: lambda: view_feature_requests_menu(a),
            23: lambda: simulate_week(a, w),
            24: lambda: simulate_many_weeks(a, w, weeks=52),
            25: lambda: show_hot_100(a, w),
            26: lambda: grammy_awards_menu(a, w),
            27: lambda: diss_tracks_menu(w),
            28: lambda: view_love_relationships_menu(w),
            29: lambda: view_separated_relationships_menu(w),
            30: lambda: create_beats_action(a),
            31: lambda: beat_vault_menu(a),
            32: lambda: beat_store_menu(a, w),
            33: lambda: numble_menu(a, w),
            34: lambda: player_love_relationships_menu(a, w),
            37: lambda: concerts_menu(a, w),
            38: lambda: venue_management_menu(a, w),
        }

    def run_action(self, action_id: int, responses: list | None = None) -> dict[str, Any]:
        if action_id == 39:
            _SESSIONS.pop(self.session_id, None)
            return {"status": "quit", "logs": ["Session ended."], "state": None}

        dispatch = self._dispatch_table()
        if action_id not in dispatch:
            return {"status": "error", "message": f"Unknown action {action_id}"}

        self.web_io.clear_pending()
        self.web_io.response_queue = []
        if responses:
            self.web_io.push_responses(responses)
        self.web_io.logs = []

        from rapsim_reviews.career_mode import display_artist

        buf = io.StringIO()
        try:
            with _patch_career_io(self.web_io), redirect_stdout(buf):
                with redirect_stdout(buf):
                    display_artist(self.artist)
                dispatch[action_id]()
        except NeedInput as exc:
            header = buf.getvalue()
            if header.strip():
                self.web_io.logs.insert(0, header.strip())
            return {
                "status": "input_required",
                "prompt": exc.prompt,
                "logs": self.web_io.logs,
                "state": self.snapshot(),
            }

        output = buf.getvalue()
        if output.strip():
            self.web_io.logs.insert(0, output.strip())
        return {
            "status": "ok",
            "logs": self.web_io.logs,
            "state": self.snapshot(),
        }

    def vault_summary(self) -> list[dict]:
        market = ensure_beat_market(self.artist)
        rows = []
        for beat in vault_beats(market):
            rows.append(
                {
                    "id": beat.beat_id,
                    "name": beat.name,
                    "genre": beat.genre,
                    "quality": round(float(beat.quality), 1),
                    "consumed": bool(beat.consumed),
                    "listed": bool(beat.listed),
                }
            )
        return rows
