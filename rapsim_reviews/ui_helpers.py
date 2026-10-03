"""
rapsim_reviews.ui_helpers
Terminal UI formatting, meter bars, prompts, and selection menus.
"""
import random


def clamp_int(value: int | float) -> int:
    return max(1, min(100, int(value)))


def clamp_meter(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def clamp_fatigue(value: float) -> float:
    return max(0.0, min(140.0, float(value)))


def clamp_popularity(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def clamp_rating(value: float) -> float:
    return max(1.0, min(10.0, float(value)))


def clamp_signed_rating(value: float) -> float:
    return max(-10.0, min(10.0, float(value)))


def money_fmt(value: float) -> str:
    return f"${value:,.2f}"


def weighted_choice(weight_map: dict) -> str:
    items = [(key, float(value)) for key, value in weight_map.items() if float(value) > 0]
    if not items:
        raise ValueError("weighted_choice requires at least one positive weight")
    labels = [item[0] for item in items]
    weights = [item[1] for item in items]
    return random.choices(labels, weights=weights, k=1)[0]


def weighted_choice_from_pool(pool: list[dict]) -> dict:
    return random.choices(pool, weights=[max(0.0, float(item.get("w", 1))) for item in pool], k=1)[0]


def meter_bar(label: str, value: float, width: int = 22, invert: bool = False) -> str:
    value = clamp_meter(value)
    display_value = 100.0 - value if invert else value
    filled = int(round((display_value / 100.0) * width))
    filled = max(0, min(width, filled))
    empty = width - filled
    return f"{label}: [{'#' * filled}{'-' * empty}]"


def prompt_text(prompt: str, default: str | None = None) -> str | None:
    raw = input(prompt).strip()
    if raw:
        return raw
    return default


def prompt_int(prompt: str, minimum: int | None = None, maximum: int | None = None, default: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            value = int(default)
        else:
            try:
                value = int(raw)
            except ValueError:
                print("Enter a valid number.")
                continue
        if minimum is not None and value < minimum:
            print(f"Enter a number >= {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a number <= {maximum}.")
            continue
        return value


def prompt_float(prompt: str, minimum: float | None = None, maximum: float | None = None, default: float | None = None) -> float:
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            value = float(default)
        else:
            try:
                value = float(raw)
            except ValueError:
                print("Enter a valid number.")
                continue
        if minimum is not None and value < minimum:
            print(f"Enter a number >= {minimum}.")
            continue
        if maximum is not None and value > maximum:
            print(f"Enter a number <= {maximum}.")
            continue
        return float(value)


def choose_from_list(title: str, options: list[str], allow_cancel: bool = False) -> int | None:
    while True:
        print(f"\n{title}")
        for idx, option in enumerate(options, 1):
            print(f"{idx}. {option}")
        if allow_cancel:
            print("0. Cancel")
        choice = prompt_int("Choose: ", 0 if allow_cancel else 1, len(options))
        if allow_cancel and choice == 0:
            return None
        return choice - 1


def choose_item_from_list(title: str, options: list[str], allow_cancel: bool = False) -> str | None:
    idx = choose_from_list(title, options, allow_cancel=allow_cancel)
    if idx is None:
        return None
    return options[idx]


def choose_unique_items(title: str, options: list[str], count: int) -> list[str]:
    chosen = []
    while len(chosen) < count:
        remaining = [opt for opt in options if opt not in chosen]
        idx = choose_from_list(
            f"{title} ({len(chosen) + 1}/{count})",
            remaining,
            allow_cancel=False,
        )
        chosen.append(remaining[idx])
    return chosen


def say(speaker: str, text: str, indent: int = 2) -> None:
    pad = " " * indent
    print(f'{pad}{speaker}: "{text}"')


def print_ratings_chart_header(title: str, subtitle: str) -> None:
    print(f"\n{title}")
    print(subtitle)
    print("-" * max(len(title), len(subtitle), 72))


def _stable_rng_for_label(label: str) -> random.Random:
    h = 0
    for ch in str(label):
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return random.Random(h)

