"""Main entrypoint for the unified artist career simulator."""

import sys

from rapsim_reviews.career_mode import main


def configure_console():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


if __name__ == "__main__":
    configure_console()
    main()
