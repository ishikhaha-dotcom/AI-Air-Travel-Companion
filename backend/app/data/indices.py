"""In-memory route indices. 50k rows -> dict lookups keep queries <100ms, no DB."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from .models import Flight


def build_route_index(flights: list[Flight]) -> dict[tuple[str, str], list[Flight]]:
    idx: dict[tuple[str, str], list[Flight]] = defaultdict(list)
    for f in flights:
        idx[(f.origin, f.destination)].append(f)
    for lst in idx.values():
        lst.sort(key=lambda f: f.departure_utc)
    return dict(idx)


def build_origin_index(flights: list[Flight]) -> dict[str, list[Flight]]:
    idx: dict[str, list[Flight]] = defaultdict(list)
    for f in flights:
        idx[f.origin].append(f)
    for lst in idx.values():
        lst.sort(key=lambda f: f.departure_utc)
    return dict(idx)


def in_window(rows: list[Flight], start: datetime, end: datetime) -> list[Flight]:
    """Rows departing within [start, end]. Route lists are <=140 items; linear scan is fine."""
    return [f for f in rows if start <= f.departure_utc <= end]
