"""FastAPI server for the Rapsim career simulator web UI."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from rapsim_reviews.web_session import ACTION_CATALOG, GameSession

ROOT = Path(__file__).resolve().parent.parent
UI_DIR = ROOT / "rapsim-ui-v2"

app = FastAPI(title="Rapsim API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class NewGameBody(BaseModel):
    name: str = "Untitled Artist"
    gender: str = "male"
    sexuality: str = "straight"
    skills: list[str] | None = None
    genres: list[str] | None = None


class ActionBody(BaseModel):
    action_id: int = Field(..., ge=1, le=50)
    responses: list | None = None


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/meta/actions")
def meta_actions():
    return {"actions": ACTION_CATALOG}


@app.get("/api/meta/options")
def meta_options():
    from rapsim_reviews.career_mode import SKILLS
    from rapsim_reviews.track_review import GENRES, THEMES

    return {
        "skills": SKILLS,
        "genres": GENRES,
        "themes": THEMES,
        "genders": ["male", "female", "non-binary"],
        "sexualities": {
            "male": ["straight", "gay", "bisexual"],
            "female": ["straight", "lesbian", "bisexual"],
            "non-binary": ["straight", "gay", "lesbian", "bisexual"],
        },
    }


@app.post("/api/session")
def new_session(body: NewGameBody):
    session = GameSession.new_game(
        name=body.name,
        gender=body.gender,
        sexuality=body.sexuality,
        skills=body.skills,
        genres=body.genres,
    )
    return {"status": "ok", "state": session.snapshot()}


@app.get("/api/session/{session_id}")
def get_session(session_id: str):
    session = GameSession.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session.snapshot()


@app.get("/api/session/{session_id}/vault")
def get_vault(session_id: str):
    session = GameSession.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return {"beats": session.vault_summary()}


@app.post("/api/session/{session_id}/action")
def run_action(session_id: str, body: ActionBody):
    session = GameSession.get(session_id)
    if not session:
        raise HTTPException(404, "Session not found")
    return session.run_action(body.action_id, body.responses)


if UI_DIR.is_dir():

    @app.get("/")
    def index():
        return FileResponse(
            UI_DIR / "index.html",
            headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
        )

    @app.get("/app.js")
    def app_js():
        return FileResponse(
            UI_DIR / "app.js",
            media_type="application/javascript",
            headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
        )

    @app.get("/styles.css")
    def styles_css():
        return FileResponse(
            UI_DIR / "styles.css",
            media_type="text/css",
            headers={"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}
        )
