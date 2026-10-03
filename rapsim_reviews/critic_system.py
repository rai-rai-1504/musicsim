"""
rapsim_reviews.critic_system
Critic profiles, reviewer identities, and sentence pool expansion utilities.
"""
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class CriticProfile:
    name: str
    username: str
    gender: str
    sexuality: str
    romance_preference: str


CRITIC_PROFILES = [
    CriticProfile("Marcus Vane", "@marcusvane", "male", "straight", "prefers_female"),
    CriticProfile("Deja Hayes", "@dejahayes", "female", "bisexual", "prefers_both"),
    CriticProfile("Vic Osei", "@vicosei", "male", "gay", "prefers_male"),
    CriticProfile("Ray Coldwell", "@raycoldwell", "male", "straight", "prefers_female"),
    CriticProfile("Earl Mosely", "@earlmosely", "male", "bisexual", "prefers_both"),
    CriticProfile("Zara Nights", "@zaranights", "female", "straight", "prefers_male"),
    CriticProfile("Tobias Lund", "@tobiaslund", "male", "straight", "prefers_female"),
    CriticProfile("Nina Pascal", "@ninapascal", "female", "lesbian", "prefers_female"),
    CriticProfile("Teena Naruka", "@teenaruka", "female", "bisexual", "prefers_both"),
    CriticProfile("Shatam Rai", "@shatamrai", "male", "straight", "prefers_female"),
]

CRITIC_NAMES = [critic.name for critic in CRITIC_PROFILES]
CRITIC_PROFILE_BY_NAME = {critic.name: critic for critic in CRITIC_PROFILES}
CRITIC_USERNAMES = {critic.name: critic.username for critic in CRITIC_PROFILES}


def _critic_username(name: str) -> str:
    clean = str(name).lower().replace(" ", "").replace("-", "").replace(".", "").replace(",", "")
    return CRITIC_USERNAMES.get(name, f"@{clean}")


def _expand_sentence_pool(
    pool: list[str],
    min_extra: int = 10,
    max_extra: int = 14,
    prefixes: list[str] | None = None,
    suffixes: list[str] | None = None,
) -> list[str]:
    expanded = list(pool)
    seen = set(expanded)
    extras_needed = min(max_extra, max(min_extra, len(pool)))
    prefix_pool = prefixes if prefixes is not None else []
    suffix_pool = suffixes if suffixes is not None else [
        "and the timeline noticed.",
        "nobody is pretending otherwise.",
        "there is no soft way to say that.",
        "people are going to talk about it all week.",
        "that is where things are now.",
        "everyone can read between the lines.",
        "it feels bigger than a passing moment.",
        "this is going to echo for a while.",
        "it landed exactly how you think it landed.",
        "and that changed the mood immediately.",
    ]
    for base in pool:
        if len(expanded) >= len(pool) + extras_needed:
            break
        if prefix_pool:
            for prefix in prefix_pool:
                variant = f"{prefix} {base}"
                if variant not in seen:
                    expanded.append(variant)
                    seen.add(variant)
                if len(expanded) >= len(pool) + extras_needed:
                    break
            if len(expanded) >= len(pool) + extras_needed:
                break
        for suffix in suffix_pool:
            trimmed = base[:-1] if base.endswith((".", "!", "?")) else base
            variant = f"{trimmed}. {suffix}"
            if variant not in seen:
                expanded.append(variant)
                seen.add(variant)
            if len(expanded) >= len(pool) + extras_needed:
                break
    return expanded


def _expand_pool_dict(
    pool_dict: dict[str, list[str]],
    min_extra: int = 10,
    max_extra: int = 14,
    prefixes: list[str] | None = None,
    suffixes: list[str] | None = None,
) -> dict[str, list[str]]:
    for key, pool in list(pool_dict.items()):
        pool_dict[key] = _expand_sentence_pool(
            list(pool),
            min_extra=min_extra,
            max_extra=max_extra,
            prefixes=prefixes,
            suffixes=suffixes,
        )
    return pool_dict
