"""rapsim_reviews.sales_system
Physical edition manufacturing, digital sales tracking, side hustles,
and label management contract negotiations.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
import random
from typing import TYPE_CHECKING

from rapsim_reviews.ui_helpers import (
    choose_from_list,
    choose_item_from_list,
    meter_bar,
    money_fmt,
    prompt_float,
    prompt_int,
    prompt_text,
    clamp_meter,
    clamp_popularity,
)
from rapsim_reviews.career_models import (
    Artist,
    SongEntry,
    AlbumEntry,
    PhysicalEdition,
    SalesSnapshot,
    JobContract,
    ManagementContract,
    PHYSICAL_UNIT_COSTS,
    PHYSICAL_BULK_DISCOUNTS,
    PHYSICAL_LIMITED_COST_MULT,
    PHYSICAL_LIMITED_DEMAND_MULT,
    PHYSICAL_BASE_PRICES,
    RIAA_CERTIFICATIONS,
    NEGOTIATION_WALK_AWAY_BUFFER,
    _player_week_index,
    _ecosystem_seed_by_name,
    _ecosystem_artist_popularity,
    _ecosystem_release_quality,
)

if TYPE_CHECKING:
    from rapsim_reviews.artist_ecosystem_sim import EcosystemWorld

SIDE_HUSTLES = [
    {"name": "Burger Bunker", "pay": 35.0, "fatigue": 18.0},
    {"name": "Needle & Noise Records", "pay": 75.0, "fatigue": 24.0},
    {"name": "RushRoute Delivery", "pay": 130.0, "fatigue": 31.0},
    {"name": "Moonline Warehouse", "pay": 220.0, "fatigue": 38.0},
]


MANAGEMENT_COMPANIES = [
    {"name": "Amplify Collective", "yearly_cost": 12000.0, "pop_gain": (8.0, 13.0), "base_cut": 10.0, "strictness": 0.85},
    {"name": "The Narrative Arc", "yearly_cost": 35000.0, "pop_gain": (13.0, 18.0), "base_cut": 12.0, "strictness": 1.0},
    {"name": "Momentum Media", "yearly_cost": 90000.0, "pop_gain": (22.0, 30.0), "base_cut": 15.0, "strictness": 1.15},
    {"name": "Catalyst Comms", "yearly_cost": 220000.0, "pop_gain": (34.0, 42.0), "base_cut": 18.0, "strictness": 1.3},
    {"name": "Verve Public Relations", "yearly_cost": 550000.0, "pop_gain": (46.0, 56.0), "base_cut": 22.0, "strictness": 1.45},
]


def _first_week_sales_value(last_week_sales: int, first_week_sales: int) -> int:
    return int(first_week_sales or last_week_sales or 0)


def _riaa_certification_label(total_sales: int) -> str:
    for threshold, label in RIAA_CERTIFICATIONS:
        if int(total_sales) >= int(threshold):
            return label
    return "-"


def _effective_sale_price(list_price: float, discount_pct: float) -> float:
    return max(0.5, float(list_price) * (1.0 - max(0.0, min(0.9, float(discount_pct)))))


def _physical_bulk_discount(copies: int) -> float:
    for threshold, discount in PHYSICAL_BULK_DISCOUNTS:
        if int(copies) >= int(threshold):
            return float(discount)
    return 0.0


def _physical_unit_cost(format_name: str, copies: int, limited_edition: bool = False) -> float:
    base_cost = float(PHYSICAL_UNIT_COSTS[format_name])
    if limited_edition:
        base_cost *= float(PHYSICAL_LIMITED_COST_MULT)
    return round(base_cost * (1.0 - _physical_bulk_discount(copies)), 2)


def _physical_edition_label(edition: PhysicalEdition) -> str:
    prefix = "limited " if bool(getattr(edition, "limited_edition", False)) else ""
    return f"{prefix}{edition.format_name}"


def _physical_financials(editions: list[PhysicalEdition]) -> tuple[float, float, float, float]:
    spent = 0.0
    revenue = 0.0
    for edition in editions:
        edition_spent = float(getattr(edition, "total_manufacturing_cost", 0.0) or 0.0)
        if edition_spent <= 0:
            edition_spent = float(getattr(edition, "unit_cost", 0.0) or 0.0) * int(getattr(edition, "copies_created", 0) or 0)
        spent += edition_spent
        revenue += float(getattr(edition, "total_revenue", 0.0) or 0.0)
    profit = revenue - spent
    margin = (profit / revenue * 100.0) if revenue > 0 else 0.0
    return float(spent), float(revenue), float(profit), float(margin)


def _release_kind_label(release_type: str) -> str:
    release_type = str(release_type or "single")
    if release_type in {"album", "deluxe", "mixtape"}:
        return release_type
    return "single"


def _physical_fair_price(release_type: str, format_name: str, quality: float, popularity: float) -> float:
    base = PHYSICAL_BASE_PRICES.get((_release_kind_label(release_type), format_name), 9.99)
    quality_factor = 0.82 + (max(1.0, min(10.0, float(quality))) / 10.0) * 0.38
    popularity_factor = 0.88 + (max(0.0, min(100.0, float(popularity))) / 100.0) * 0.32
    return round(base * quality_factor * popularity_factor, 2)


def _physical_pricing_multiplier(price_ratio: float, effective_price: float, format_name: str) -> float:
    price_ratio = max(0.01, float(price_ratio))
    effective_price = max(0.5, float(effective_price))
    if price_ratio <= 1.0:
        return 1.0 + ((1.0 - price_ratio) * 0.35)

    # Above fair price, demand falls exponentially. Absolute luxury pricing gets
    # another hard penalty so absurd prices do not keep selling through volume.
    ratio_mult = math.exp(-1.8 * ((price_ratio - 1.0) ** 1.65))
    barrier = 60.0 if format_name == "disc" else 160.0
    if effective_price <= barrier:
        absolute_mult = 1.0
    else:
        absolute_mult = math.exp(-((effective_price - barrier) / barrier) ** 1.35)
    return max(0.0, min(1.35, ratio_mult * absolute_mult))


def _physical_units_from_streams(
    *,
    weekly_streams: int,
    popularity: float,
    quality: float,
    release_type: str,
    format_name: str,
    effective_price: float,
    limited_edition: bool = False,
) -> int:
    if int(weekly_streams) <= 0 or float(popularity) <= 50.0:
        return 0
    base = float(weekly_streams) / 5000.0
    quality_mult = 0.70 + (max(1.0, min(10.0, float(quality))) / 10.0) * 0.55
    popularity_mult = 0.65 + (max(0.0, min(100.0, float(popularity))) / 100.0) * 0.75
    fair_price = _physical_fair_price(release_type, format_name, quality, popularity)
    if limited_edition:
        fair_price = round(fair_price * 1.35, 2)
    price_ratio = float(effective_price) / max(0.5, fair_price)
    pricing_mult = _physical_pricing_multiplier(price_ratio, effective_price, format_name)
    limited_mult = float(PHYSICAL_LIMITED_DEMAND_MULT) if limited_edition else 1.0
    units = base * quality_mult * popularity_mult * pricing_mult * limited_mult * random.uniform(0.75, 1.25)
    whole = int(units)
    frac = units - whole
    if random.random() < frac:
        whole += 1
    return max(0, whole)


def _apply_physical_sales(
    editions: list[PhysicalEdition],
    *,
    weekly_streams: int,
    popularity: float,
    quality: float,
    release_type: str,
) -> tuple[int, float]:
    total_units = 0
    total_revenue = 0.0
    for edition in editions:
        edition.last_week_units_sold = 0
        if edition.copies_remaining <= 0:
            continue
        effective_price = edition.effective_price()
        demand_units = _physical_units_from_streams(
            weekly_streams=int(weekly_streams),
            popularity=float(popularity),
            quality=float(quality),
            release_type=release_type,
            format_name=edition.format_name,
            effective_price=effective_price,
            limited_edition=bool(getattr(edition, "limited_edition", False)),
        )
        sold = min(int(edition.copies_remaining), int(demand_units))
        if sold <= 0:
            continue
        edition.copies_remaining -= sold
        edition.last_week_units_sold = sold
        edition.total_units_sold += sold
        revenue = sold * effective_price
        edition.total_revenue += revenue
        total_units += sold
        total_revenue += revenue
    return int(total_units), float(total_revenue)


def _player_song_sales_snapshot(entry: SongEntry) -> SalesSnapshot:
    return SalesSnapshot(
        total_digital=int(entry.total_digital_sales),
        last_week_digital=int(entry.last_week_digital_sales),
        total_physical=int(entry.total_physical_sales),
        last_week_physical=int(entry.last_week_physical_sales),
        first_week_sales=int(entry.first_week_sales),
    )


def _player_album_sales_snapshot(artist, album_entry: AlbumEntry) -> SalesSnapshot:
    tracks = [
        linked_entry
        for song in album_entry.album.songs
        for linked_entry in [next((e for e in artist.singles if e.song is song and e.released), None)]
        if linked_entry is not None
    ]
    total_digital = sum(int(track.total_digital_sales) for track in tracks)
    last_week_digital = sum(int(track.last_week_digital_sales) for track in tracks)
    total_physical = sum(int(edition.total_units_sold) for edition in album_entry.physical_editions)
    last_week_physical = sum(int(edition.last_week_units_sold) for edition in album_entry.physical_editions)
    if album_entry.first_week_sales <= 0 and (last_week_digital + last_week_physical) > 0:
        album_entry.first_week_sales = int(last_week_digital + last_week_physical)
    album_entry.total_digital_sales = int(total_digital)
    album_entry.last_week_digital_sales = int(last_week_digital)
    album_entry.total_physical_sales = int(total_physical)
    album_entry.last_week_physical_sales = int(last_week_physical)
    return SalesSnapshot(
        total_digital=int(total_digital),
        last_week_digital=int(last_week_digital),
        total_physical=int(total_physical),
        last_week_physical=int(last_week_physical),
        first_week_sales=int(album_entry.first_week_sales),
    )


def _ensure_sales_state(world: EcosystemWorld | None):
    if world is None:
        return
    if getattr(world, "song_sales_state", None) is None:
        world.song_sales_state = {}
    if getattr(world, "release_sales_state", None) is None:
        world.release_sales_state = {}
    if getattr(world, "physical_inventory_by_release", None) is None:
        world.physical_inventory_by_release = {}


def _world_song_sales(world: EcosystemWorld, song_id: str) -> SalesSnapshot:
    _ensure_sales_state(world)
    if song_id not in world.song_sales_state:
        world.song_sales_state[song_id] = SalesSnapshot()
    return world.song_sales_state[song_id]


def _world_release_sales(world: EcosystemWorld, release_id: str) -> SalesSnapshot:
    _ensure_sales_state(world)
    if release_id not in world.release_sales_state:
        world.release_sales_state[release_id] = SalesSnapshot()
    return world.release_sales_state[release_id]


def _world_release_editions(world: EcosystemWorld, release_id: str) -> list[PhysicalEdition]:
    _ensure_sales_state(world)
    if release_id not in world.physical_inventory_by_release:
        world.physical_inventory_by_release[release_id] = []
    return world.physical_inventory_by_release[release_id]


def _ensure_ecosystem_physical_inventory(world: EcosystemWorld, release, popularity: float):
    if float(popularity) <= 50.0:
        return
    editions = _world_release_editions(world, str(getattr(release, "release_id", "")))
    if editions:
        return
    release_type = _release_kind_label(str(getattr(release, "release_type", "single")))
    quality = _ecosystem_release_quality(release)
    base_copies = 60 if release_type == "single" else 140
    pop_bonus = int(max(0.0, float(popularity) - 50.0) * (3 if release_type == "single" else 5))
    total_copies = max(20, base_copies + pop_bonus)
    disc_share = 0.75 if release_type == "single" else 0.55
    disc_copies = int(total_copies * disc_share)
    vinyl_copies = max(0, total_copies - disc_copies)
    for format_name, copies in (("disc", disc_copies), ("vinyl", vinyl_copies)):
        if copies <= 0:
            continue
        editions.append(
            PhysicalEdition(
                format_name=format_name,
                unit_cost=float(PHYSICAL_UNIT_COSTS[format_name]),
                list_price=_physical_fair_price(release_type, format_name, quality, popularity),
                discount_pct=0.0,
                copies_created=int(copies),
                copies_remaining=int(copies),
            )
        )


def _step_ecosystem_sales(world: EcosystemWorld):
    _ensure_sales_state(world)
    popularity_by_name = getattr(world, "artist_popularity", {}) or {}
    for runtime_song in world.song_runtime.values():
        song_state = _world_song_sales(world, str(getattr(runtime_song, "song_id", "")))
        digital_units = int(getattr(runtime_song, "last_week_streams", 0) or 0) // 1000
        song_state.last_week_digital = int(digital_units)
        song_state.total_digital += int(digital_units)
        song_state.last_week_physical = 0
        if song_state.first_week_sales <= 0 and digital_units > 0 and int(getattr(runtime_song, "weeks_since_release", 0)) <= 1:
            song_state.first_week_sales = int(digital_units)

    for releases in world.release_history.values():
        for release in releases:
            release_id = str(getattr(release, "release_id", ""))
            if not release_id:
                continue
            weeks_since_release = int(getattr(world, "week_number", 0)) - int(getattr(release, "week_number", 0))
            tracks = list(getattr(release, "tracks", None) or ())
            if weeks_since_release > 30:
                weekly_streams = sum(int(getattr(world.song_runtime.get(str(getattr(track, "song_id", "")), None), "last_week_streams", 0) or 0) for track in tracks)
                editions = _world_release_editions(world, release_id)
                is_sold_out = (not editions) or all(int(getattr(edition, "copies_remaining", 0)) <= 0 for edition in editions)
                if weekly_streams == 0 and is_sold_out:
                    release_state = _world_release_sales(world, release_id)
                    release_state.last_week_digital = 0
                    release_state.last_week_physical = 0
                    release_state.total_digital = sum(int(_world_song_sales(world, str(getattr(t, "song_id", ""))).total_digital) for t in tracks)
                    release_state.total_physical = sum(int(getattr(edition, "total_units_sold", 0)) for edition in editions)
                    continue

            release_state = _world_release_sales(world, release_id)
            release_state.last_week_digital = 0
            release_state.total_digital = 0
            for track in tracks:
                track_state = _world_song_sales(world, str(getattr(track, "song_id", "")))
                release_state.last_week_digital += int(track_state.last_week_digital)
                release_state.total_digital += int(track_state.total_digital)
            popularity = float(popularity_by_name.get(str(getattr(release, "artist_name", "")), 0.0))
            _ensure_ecosystem_physical_inventory(world, release, popularity)
            physical_units, _ = _apply_physical_sales(
                _world_release_editions(world, release_id),
                weekly_streams=sum(int(getattr(world.song_runtime.get(str(getattr(track, "song_id", "")), None), "last_week_streams", 0) or 0) for track in tracks),
                popularity=popularity,
                quality=_ecosystem_release_quality(release),
                release_type=str(getattr(release, "release_type", "single")),
            )
            release_state.last_week_physical = int(physical_units)
            release_state.total_physical = sum(int(edition.total_units_sold) for edition in _world_release_editions(world, release_id))
            if release_state.first_week_sales <= 0 and int(getattr(release, "week_number", 0)) == int(getattr(world, "week_number", 0)):
                release_state.first_week_sales = int(release_state.last_week_sales)


def _player_release_sales_candidates(player_artist: Artist) -> list[dict]:
    rows: list[dict] = []
    for entry in player_artist.singles:
        if not entry.released:
            continue
        if str(getattr(entry, "source_label", "")).startswith("Album:"):
            continue
        snapshot = _player_song_sales_snapshot(entry)
        rows.append(
            {
                "artist": player_artist.name,
                "title": entry.song.name,
                "release_type": "single",
                "release_week": int(entry.release_week_index or 0),
                "first_week_sales": int(snapshot.first_week_sales),
                "last_week_sales": int(snapshot.last_week_sales),
                "total_sales": int(snapshot.total_sales),
            }
        )
    for album_entry in player_artist.albums:
        if not album_entry.released:
            continue
        snapshot = _player_album_sales_snapshot(player_artist, album_entry)
        rows.append(
            {
                "artist": player_artist.name,
                "title": album_entry.album.name,
                "release_type": "deluxe" if album_entry.deluxe_of else "album",
                "release_week": int(album_entry.release_week_index or 0),
                "first_week_sales": int(snapshot.first_week_sales),
                "last_week_sales": int(snapshot.last_week_sales),
                "total_sales": int(snapshot.total_sales),
            }
        )
    return rows


def _ecosystem_release_sales_candidates(world: EcosystemWorld | None) -> list[dict]:
    if world is None:
        return []
    _ensure_sales_state(world)
    rows: list[dict] = []
    for artist_name, releases in world.release_history.items():
        for release in releases:
            state = _world_release_sales(world, str(getattr(release, "release_id", "")))
            rows.append(
                {
                    "artist": artist_name,
                    "title": str(getattr(release, "title", "")),
                    "release_type": str(getattr(release, "release_type", "single")),
                    "release_week": int(getattr(release, "week_number", 0)),
                    "first_week_sales": int(state.first_week_sales),
                    "last_week_sales": int(state.last_week_sales),
                    "total_sales": int(state.total_sales),
                }
            )
    return rows


def _physical_stock_summary(editions: list[PhysicalEdition]) -> str:
    if not editions:
        return "no physical stock"
    parts = []
    for edition in editions:
        total_cost = float(getattr(edition, "total_manufacturing_cost", 0.0) or 0.0)
        cost_label = f" | mfg {money_fmt(total_cost)}" if total_cost > 0 else ""
        parts.append(
            f"{_physical_edition_label(edition)}: {edition.copies_remaining}/{edition.copies_created} left @ "
            f"{money_fmt(edition.effective_price())}{cost_label}"
        )
    return " | ".join(parts)


def _manage_physical_editions(
    artist: Artist,
    *,
    title: str,
    release_type: str,
    quality: float,
    popularity: float,
    editions: list[PhysicalEdition],
) -> None:
    while True:
        options = [
            f"Restock discs ({_physical_stock_summary([e for e in editions if e.format_name == 'disc' and not getattr(e, 'limited_edition', False)])})",
            f"Restock vinyls ({_physical_stock_summary([e for e in editions if e.format_name == 'vinyl' and not getattr(e, 'limited_edition', False)])})",
            f"Restock limited discs ({_physical_stock_summary([e for e in editions if e.format_name == 'disc' and getattr(e, 'limited_edition', False)])})",
            f"Restock limited vinyls ({_physical_stock_summary([e for e in editions if e.format_name == 'vinyl' and getattr(e, 'limited_edition', False)])})",
            "Back",
        ]
        choice = choose_from_list(f"Physical copies | {title}", options, allow_cancel=False)
        if choice is None or choice == 4:
            return
        format_name = "disc" if choice in {0, 2} else "vinyl"
        limited_edition = choice in {2, 3}
        existing = next(
            (
                edition
                for edition in editions
                if edition.format_name == format_name
                and bool(getattr(edition, "limited_edition", False)) == bool(limited_edition)
            ),
            None,
        )
        fair_price = _physical_fair_price(release_type, format_name, quality, popularity)
        if limited_edition:
            fair_price = round(fair_price * 1.35, 2)
        default_price = existing.list_price if existing is not None else fair_price
        default_discount = int(round((existing.discount_pct if existing is not None else 0.0) * 100))
        base_unit_cost = float(PHYSICAL_UNIT_COSTS[format_name]) * (
            float(PHYSICAL_LIMITED_COST_MULT) if limited_edition else 1.0
        )
        edition_label = f"limited {format_name}" if limited_edition else format_name
        print(
            f"\nManufacturing {edition_label}: base {money_fmt(base_unit_cost)} each. "
            f"Bulk discounts: 1,000+ 5% | 5,000+ 10% | 25,000+ 15% | 100,000+ 20%."
        )
        copies = prompt_int(
            f"How many {edition_label} copies to manufacture? ",
            0,
            200_000,
            100 if release_type == "single" else 250,
        )
        unit_cost = _physical_unit_cost(format_name, copies, limited_edition)
        bulk_discount = _physical_bulk_discount(copies)
        manufacturing_cost = float(copies) * unit_cost
        print(
            f"Manufacturing cost: {copies:,} x {money_fmt(unit_cost)}"
            f"{f' ({int(bulk_discount * 100)}% bulk discount)' if bulk_discount else ''} = "
            f"{money_fmt(manufacturing_cost)}"
        )
        price = prompt_float(
            f"Sale price per {edition_label} copy ({money_fmt(fair_price)} fair price): ",
            0.5,
            500.0,
            default_price,
        )
        discount_pct = prompt_int("Discount %: ", 0, 80, default_discount) / 100.0
        if copies > 0 and artist.money < manufacturing_cost:
            print(f"You need {money_fmt(manufacturing_cost)} to manufacture that run.")
            input("Press Enter...")
            continue
        if copies > 0:
            artist.money -= manufacturing_cost
        if existing is None:
            editions.append(
                PhysicalEdition(
                    format_name=format_name,
                    unit_cost=unit_cost,
                    list_price=float(price),
                    discount_pct=float(discount_pct),
                    limited_edition=bool(limited_edition),
                    copies_created=int(copies),
                    copies_remaining=int(copies),
                    total_manufacturing_cost=float(manufacturing_cost),
                )
            )
        else:
            existing.list_price = float(price)
            existing.discount_pct = float(discount_pct)
            existing.unit_cost = float(unit_cost)
            existing.copies_created += int(copies)
            existing.copies_remaining += int(copies)
            existing.total_manufacturing_cost = float(getattr(existing, "total_manufacturing_cost", 0.0) or 0.0) + float(manufacturing_cost)
        print(
            f"{title}: {edition_label} stock updated. "
            f"Manufacturing cost {money_fmt(manufacturing_cost)} | "
            f"sale price {money_fmt(_effective_sale_price(price, discount_pct))} after discount."
        )
        input("Press Enter...")


def manage_physical_copies_menu(artist: Artist):
    options: list[tuple[str, object, str, float]] = []
    labels: list[str] = []
    for entry in artist.singles:
        if not entry.released or str(getattr(entry, "source_label", "")).startswith("Album:"):
            continue
        labels.append(
            f"Single | {entry.song.name} | sales {entry.total_digital_sales + entry.total_physical_sales:,} | {_physical_stock_summary(entry.physical_editions)}"
        )
        options.append(("single", entry, "single", float(entry.song.quality)))
    for album_entry in artist.albums:
        if not album_entry.released:
            continue
        snapshot = _player_album_sales_snapshot(artist, album_entry)
        release_type = "deluxe" if album_entry.deluxe_of else "album"
        avg_quality = (
            sum(float(song.quality) for song in album_entry.album.songs) / max(1, len(album_entry.album.songs))
            if album_entry.album.songs else float(album_entry.average_review or 5.0)
        )
        labels.append(
            f"{release_type.title()} | {album_entry.album.name} | sales {snapshot.total_sales:,} | {_physical_stock_summary(album_entry.physical_editions)}"
        )
        options.append((release_type, album_entry, release_type, float(avg_quality)))
    if not options:
        print("\nYou need a released single or album before you can press physical copies.")
        return
    idx = choose_from_list("Manage physical copies", labels, allow_cancel=True)
    if idx is None:
        return
    kind, item, release_type, quality = options[idx]
    if kind == "single":
        _manage_physical_editions(
            artist,
            title=item.song.name,
            release_type="single",
            quality=quality,
            popularity=float(artist.popularity),
            editions=item.physical_editions,
        )
    else:
        _manage_physical_editions(
            artist,
            title=item.album.name,
            release_type=release_type,
            quality=quality,
            popularity=float(artist.popularity),
            editions=item.physical_editions,
        )


def _print_sales_line(label: str, sales: SalesSnapshot, editions: list[PhysicalEdition] | None = None) -> None:
    print(
        f"{label} | digital {sales.total_digital:,} total / {sales.last_week_digital:,} last week | "
        f"physical {sales.total_physical:,} total / {sales.last_week_physical:,} last week | "
        f"all {sales.total_sales:,} total | fw {sales.first_week_sales:,} | "
        f"{_riaa_certification_label(sales.total_sales)}"
    )
    if editions:
        spent, revenue, profit, margin = _physical_financials(editions)
        print(
            f"  physical money: spent {money_fmt(spent)} | received {money_fmt(revenue)} | "
            f"profit {money_fmt(profit)} | margin {margin:.1f}%"
        )


def view_player_sales_menu(artist: Artist):
    released_singles = [
        entry
        for entry in artist.singles
        if entry.released and not str(getattr(entry, "source_label", "")).startswith("Album:")
    ]
    released_albums = [entry for entry in artist.albums if entry.released]
    if not released_singles and not released_albums:
        print("\nNo released music has sales yet.")
        return

    while True:
        options = ["Singles", "Albums", "Back"]
        choice = choose_from_list("View Sales", options, allow_cancel=False)
        if choice == 0:
            if not released_singles:
                print("\nNo released singles.")
                input("Press Enter...")
                continue
            print("\nSingle Sales")
            for entry in released_singles:
                _print_sales_line(entry.song.name, _player_song_sales_snapshot(entry), entry.physical_editions)
                if entry.physical_editions:
                    print(f"  stock: {_physical_stock_summary(entry.physical_editions)}")
            input("\nPress Enter to go back...")
        elif choice == 1:
            if not released_albums:
                print("\nNo released albums.")
                input("Press Enter...")
                continue
            print("\nAlbum Sales")
            for album_entry in released_albums:
                release_type = "Deluxe" if album_entry.deluxe_of else "Album"
                album_sales = _player_album_sales_snapshot(artist, album_entry)
                _print_sales_line(f"{release_type} | {album_entry.album.name}", album_sales, album_entry.physical_editions)
                if album_entry.physical_editions:
                    print(f"  stock: {_physical_stock_summary(album_entry.physical_editions)}")
                linked_tracks = [
                    linked_entry
                    for song in album_entry.album.songs
                    for linked_entry in [next((e for e in artist.singles if e.song is song and e.released), None)]
                    if linked_entry is not None
                ]
                if linked_tracks:
                    print("  Songs")
                    for track in linked_tracks:
                        track_sales = _player_song_sales_snapshot(track)
                        print(
                            f"  - {track.song.name}: digital {track_sales.total_digital:,} total / "
                            f"{track_sales.last_week_digital:,} last week | physical {track_sales.total_physical:,} total / "
                            f"{track_sales.last_week_physical:,} last week | all {track_sales.total_sales:,}"
                        )
            input("\nPress Enter to go back...")
        else:
            return


def work_side_hustle(artist):
    if artist.side_hustle:
        print(
            f"You are already working at {artist.side_hustle.job_name} for "
            f"{artist.side_hustle.weeks_left} more weeks."
        )
        return
    options = [
        f"{job['name']} | {money_fmt(job['pay'])}/week | fatigue {job['fatigue']:.1f}/week | 12 weeks"
        for job in SIDE_HUSTLES
    ]
    idx = choose_from_list("Choose a side hustle shift", options, allow_cancel=True)
    if idx is None:
        return
    job = SIDE_HUSTLES[idx]
    artist.side_hustle = JobContract(
        job_name=job["name"],
        weekly_pay=job["pay"],
        weekly_fatigue=job["fatigue"],
        weeks_left=12,
    )
    print(
        f"You started a 12-week job at {job['name']}. "
        f"It pays {money_fmt(job['pay'])} each week."
    )


def process_side_hustle_week(artist):
    if not artist.side_hustle:
        return 0.0, 0.0, False
    weekly_pay = artist.side_hustle.weekly_pay
    weekly_fatigue = 0.0
    was_extra_tired = artist.fatigue > weekly_fatigue
    if was_extra_tired:
        extra_fatigue = artist.fatigue - weekly_fatigue
        weekly_pay = max(
            0.0,
            weekly_pay - ((extra_fatigue / 100.0) / 2.0 * artist.side_hustle.weekly_pay),
        )
    artist.money += weekly_pay
    artist.side_hustle.weeks_left -= 1
    if artist.side_hustle.weeks_left <= 0:
        print(f"{artist.side_hustle.job_name} shift contract ended.")
        artist.side_hustle = None
    return weekly_pay, weekly_fatigue, was_extra_tired


def contract_terms():
    return {
        0: {"label": "4 Weeks", "weeks": 4, "billing_every": 1, "payments": 4},
        1: {"label": "6 Months", "weeks": 24, "billing_every": 4, "payments": 6},
        2: {"label": "Yearly", "weeks": 48, "billing_every": 24, "payments": 2},
    }


def build_contract(company, term_info, fee_multiplier=1.0, cut_delta=0.0):
    total_cost = company["yearly_cost"] * (term_info["weeks"] / 48.0) * fee_multiplier
    billing_amount = total_cost / term_info["payments"]
    cut = max(3.0, company["base_cut"] + cut_delta)
    return ManagementContract(
        company_name=company["name"],
        term_label=term_info["label"],
        weeks_left=term_info["weeks"],
        billing_amount=billing_amount,
        billing_every_weeks=term_info["billing_every"],
        weeks_until_payment=term_info["billing_every"],
        weekly_popularity_range=company["pop_gain"],
        current_weekly_popularity=random.uniform(*company["pop_gain"]),
        stream_cut_pct=cut,
    )


def negotiate_contract(company, term_info):
    base_contract = build_contract(company, term_info)
    print(f"\n{company['name']}: Here's our opening ask.")
    print(
        f"{company['name']}: {term_info['label']} deal, "
        f"{money_fmt(base_contract.billing_amount)} every {base_contract.billing_every_weeks} week(s), "
        f"{company['base_cut']:.1f}% stream cut, "
        f"weekly base popularity in the {company['pop_gain'][0]:.1f}% to {company['pop_gain'][1]:.1f}% range."
    )
    if term_info["label"] == "Yearly":
        print(
            f"{company['name']}: For yearly, we take the first 24 weeks upfront and the second half at week 24."
        )

    if prompt_text("Negotiate this deal? (y/n): ", "n").lower() != "y":
        return base_contract, base_contract.billing_amount

    print(f"\nYou: I want to discuss the money and cut.")
    fee_change = prompt_int(
        "Fee change % (negative asks them to lower price, positive offers more): ",
        -40,
        40,
    )
    cut_change = prompt_int(
        "Cut change in points (negative asks them to take less, positive offers more): ",
        -10,
        10,
    )

    fee_multiplier = 1.0 + (fee_change / 100.0)
    pressure_score = (max(0, -fee_change) * 0.9) + (max(0, -cut_change) * 6.0)
    goodwill_score = (max(0, fee_change) * 0.45) + (max(0, cut_change) * 3.0)
    patience = random.uniform(10.0, 22.0) / company["strictness"]

    # A large extra buffer means the company sees the ask as insulting, not just aggressive.
    if pressure_score > patience + NEGOTIATION_WALK_AWAY_BUFFER:
        print(f"{company['name']}: Absolutely not. That is insulting.")
        print(f"{company['name']}: We are not running a charity and we are not desperate.")
        print(f"{company['name']}: Come back when you want a real conversation.")
        return None, 0.0

    if pressure_score > patience:
        counter_fee_multiplier = 1.0 + min(0.18, max(-0.08, fee_change / 220.0))
        counter_cut_delta = max(-2.0, min(3.0, cut_change / 3.0))
        counter = build_contract(company, term_info, counter_fee_multiplier, counter_cut_delta)
        print(f"{company['name']}: No, not on those terms.")
        print(
            f"{company['name']}: Best we can do is {money_fmt(counter.billing_amount)} every "
            f"{counter.billing_every_weeks} week(s) and {counter.stream_cut_pct:.1f}%."
        )
        if choose_from_list(
            "Accept the counter?",
            ["Accept counter", "Walk away"],
            allow_cancel=False,
        ) == 0:
            upfront = counter.billing_amount if counter.term_label == "Yearly" else 0.0
            return counter, upfront
        print("You walk away from the table.")
        return None, 0.0

    final = build_contract(company, term_info, fee_multiplier, cut_change)
    if goodwill_score > 0:
        print(f"{company['name']}: That's generous. We can absolutely do that.")
        print(f"{company['name']}: Easy money for us. Pleasure doing business.")
    else:
        print(f"{company['name']}: Fine. We can make that work.")
        print(f"{company['name']}: Do not expect us to move any further.")
    upfront = final.billing_amount if final.term_label == "Yearly" else 0.0
    return final, upfront


def management_menu(artist):
    if artist.management:
        print(
            f"\nCurrent management: {artist.management.company_name} | "
            f"{artist.management.term_label} | billing {money_fmt(artist.management.billing_amount)} "
            f"every {artist.management.billing_every_weeks} week(s) | "
            f"weekly base popularity {artist.management.current_weekly_popularity:.1f}% | "
            f"stream cut {artist.management.stream_cut_pct:.1f}%"
        )
        if choose_from_list(
            "Management options",
            ["Keep current contract", "Drop current contract"],
            allow_cancel=True,
        ) == 1:
            print(f"You ended the contract with {artist.management.company_name}.")
            artist.management = None
        return

    company_idx = choose_from_list(
        "Choose a management company",
        [
            f"{c['name']} | yearly {money_fmt(c['yearly_cost'])} | "
            f"weekly popularity +{c['pop_gain'][0]:.0f}-{c['pop_gain'][1]:.0f}%"
            for c in MANAGEMENT_COMPANIES
        ],
        allow_cancel=True,
    )
    if company_idx is None:
        return
    company = MANAGEMENT_COMPANIES[company_idx]

    term_choice = choose_from_list("Choose contract term", ["4 weeks", "6 months", "Yearly"], allow_cancel=True)
    if term_choice is None:
        return
    term_info = contract_terms()[term_choice]
    contract, upfront_due = negotiate_contract(company, term_info)
    if contract is None:
        return
    if artist.money < upfront_due:
        print(
            f"You need at least {money_fmt(upfront_due)} available to take this contract."
        )
        return
    artist.money -= upfront_due
    artist.management = contract
    print(
        f"Signed with {contract.company_name}. "
        f"Paid {money_fmt(upfront_due)} upfront | "
        f"base popularity {contract.current_weekly_popularity:.1f}% this week | "
        f"stream cut {contract.stream_cut_pct:.1f}%"
    )


def show_shawtify_streams(artist):
    released = [entry for entry in artist.singles if entry.released]
    if not released:
        print("\nNo released songs are tracking streams yet.")
        return

    print("\nSHAWTIFY STREAMS")
    for idx, entry in enumerate(
        sorted(released, key=lambda e: e.total_streams, reverse=True), 1
    ):
        sales = _player_song_sales_snapshot(entry)
        catchiness = getattr(entry.song, "catchiness", None)
        catchy_label = f" | catchy {catchiness}" if catchiness is not None else ""
        v = getattr(entry.song, "virality", None)
        m = getattr(entry.song, "maturity_weeks", None)
        viral_label = ""
        if v is not None and m is not None and v >= 2.0:
            remaining = max(0, int(m - entry.weeks_since_release))
            viral_label = f" | viral {v} (matures in {remaining}w)"
        review = (
            f" | avg review {entry.average_review}/10"
            if entry.average_review is not None
            else ""
        )
        print(
            f"- {idx}. {entry.song.name} [{entry.source_label}] | "
            f"total {entry.total_streams:,} | this week {entry.last_week_streams:,} | "
            f"sales {sales.total_sales:,} total / {sales.last_week_sales:,} last week / "
            f"{_first_week_sales_value(sales.last_week_sales, sales.first_week_sales):,} first week | "
            f"{_riaa_certification_label(sales.total_sales)}{catchy_label}{viral_label}{review}"
        )

