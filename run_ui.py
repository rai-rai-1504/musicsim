"""Launch the Rapsim web UI (FastAPI + static frontend)."""

import sys

import uvicorn


def configure_console():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    configure_console()
    uvicorn.run(
        "rapsim_api.server:app",
        host="127.0.0.1",
        port=8765,
        reload=False,
    )
