"""
rapsim_reviews.date_system
Centralized date and calendar system for RapSim.
Simulates a weekly calendar starting Monday, Jan 1, Year 1 (anchored to 2024-01-01).
"""
import datetime
import random
from typing import Any

BASE_DATE = datetime.date(2024, 1, 1)


def ordinal_suffix(day: int) -> str:
    """Return day number with ordinal suffix (e.g. 1st, 2nd, 3rd, 4th, 16th)."""
    if 11 <= (day % 100) <= 13:
        return f"{day}th"
    last_digit = day % 10
    if last_digit == 1:
        return f"{day}st"
    elif last_digit == 2:
        return f"{day}nd"
    elif last_digit == 3:
        return f"{day}rd"
    else:
        return f"{day}th"


def _resolve_world_week(world_week: int | None = None, year: int | None = None, week: int | None = None) -> int:
    """Resolve world week index (1-based continuous week count) from either world_week or year/week pair."""
    if world_week is not None and world_week > 0:
        return int(world_week)
    if year is not None and week is not None:
        y = max(1, int(year))
        w = max(1, int(week))
        return ((y - 1) * 52) + w
    return 1


def get_week_dates(world_week: int | None = None, year: int | None = None, week: int | None = None) -> tuple[datetime.date, datetime.date]:
    """Return (start_date, end_date) representing Monday to Sunday of the specified week."""
    w_idx = _resolve_world_week(world_week, year, week)
    start_date = BASE_DATE + datetime.timedelta(days=(w_idx - 1) * 7)
    end_date = start_date + datetime.timedelta(days=6)
    return start_date, end_date


def format_week_range(world_week: int | None = None, year: int | None = None, week: int | None = None, capitalize: bool = False) -> str:
    """
    Format the week range according to calendar rules:
    - Same month: 'jan 1-7, year 1'
    - Different months: 'jan 29-feb 4, year 1'
    - Different years: 'dec 30 - jan 5, year 2'
    """
    start_date, end_date = get_week_dates(world_week, year, week)
    y = end_date.year - BASE_DATE.year + 1

    s_m = start_date.strftime("%b")
    e_m = end_date.strftime("%b")
    if not capitalize:
        s_m = s_m.lower()
        e_m = e_m.lower()

    s_d = start_date.day
    e_d = end_date.day
    year_str = f"Year {y}" if capitalize else f"year {y}"

    if start_date.year != end_date.year:
        return f"{s_m} {s_d} - {e_m} {e_d}, {year_str}"
    elif start_date.month != end_date.month:
        return f"{s_m} {s_d}-{e_m} {e_d}, {year_str}"
    else:
        return f"{s_m} {s_d}-{e_d}, {year_str}"


def format_release_date(release_or_week: Any, day_offset: int | None = None, capitalize: bool = False) -> str:
    """
    Format song/album release date as '(month) (date)st/th, (year)'
    e.g. 'jan 16th, year 1'.
    
    Accepts:
    - An integer week number (defaults to day_offset=4, Friday)
    - A release object (WeeklyRelease, PendingRelease, EcosystemSongRuntime, SongEntry, AlbumEntry, etc.)
    """
    if release_or_week is None:
        return "-"

    # Check if string date already cached/assigned
    if hasattr(release_or_week, "release_date") and getattr(release_or_week, "release_date", None):
        return str(release_or_week.release_date)

    # Extract week number
    w_idx = 1
    if isinstance(release_or_week, (int, float)):
        w_idx = int(release_or_week)
    elif hasattr(release_or_week, "release_week_index") and release_or_week.release_week_index is not None:
        w_idx = int(release_or_week.release_week_index)
    elif hasattr(release_or_week, "release_week") and release_or_week.release_week is not None:
        w_idx = int(release_or_week.release_week)
    elif hasattr(release_or_week, "week_number") and release_or_week.week_number is not None:
        w_idx = int(release_or_week.week_number)
    elif hasattr(release_or_week, "week_released") and release_or_week.week_released is not None:
        w_idx = int(release_or_week.week_released)
    elif hasattr(release_or_week, "week_release") and release_or_week.week_release is not None:
        w_idx = int(release_or_week.week_release)

    if w_idx <= 0:
        w_idx = 1

    # Extract or resolve day offset (0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun)
    resolved_offset = 4  # Default to Friday
    if day_offset is not None:
        resolved_offset = max(0, min(6, int(day_offset)))
    elif hasattr(release_or_week, "day_offset") and getattr(release_or_week, "day_offset", None) is not None:
        resolved_offset = max(0, min(6, int(release_or_week.day_offset)))
    elif hasattr(release_or_week, "release_id"):
        # Stable fallback hash: ~13 out of 15 Friday
        rng = random.Random(f"reldate:{release_or_week.release_id}:{w_idx}")
        if rng.random() < (13.0 / 15.0):
            resolved_offset = 4
        else:
            resolved_offset = rng.choice([0, 1, 2, 3, 5, 6])

    start_date = BASE_DATE + datetime.timedelta(days=(w_idx - 1) * 7)
    rel_date = start_date + datetime.timedelta(days=resolved_offset)
    y = rel_date.year - BASE_DATE.year + 1

    m = rel_date.strftime("%b")
    month_str = m if capitalize else m.lower()
    day_str = ordinal_suffix(rel_date.day)
    year_str = f"Year {y}" if capitalize else f"year {y}"

    return f"{month_str} {day_str}, {year_str}"


def assign_release_days(releases: list[Any], week_number: int) -> None:
    """
    Distribute a batch of releases dropping in week_number so that
    13 out of 15 (or n - round(n * 2 / 15)) drop on Friday (day_offset=4),
    and the remaining 2 out of 15 drop on another random day of that week.
    Sets 'day_offset' and 'release_date' attributes on each release object.
    """
    if not releases:
        return

    n = len(releases)
    rng = random.Random(f"assign_release_days:{week_number}")
    num_other = round(n * 2.0 / 15.0)
    other_indices = set(rng.sample(range(n), num_other)) if num_other > 0 else set()
    other_days = [0, 1, 2, 3, 5, 6]

    for i, r in enumerate(releases):
        if i in other_indices:
            offset = rng.choice(other_days)
        else:
            offset = 4  # Friday

        try:
            r.day_offset = offset
            r.release_date = format_release_date(r, day_offset=offset)
        except (AttributeError, TypeError):
            if isinstance(r, dict):
                r["day_offset"] = offset
                r["release_date"] = format_release_date(week_number, day_offset=offset)
