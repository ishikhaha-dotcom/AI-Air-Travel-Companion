"""Single-leg candidate generation: route-index window lookup, plus
self-composed connections when the route is thin/absent for the window
(route/month coverage is sparse — blueprint finding #4).
"""
from __future__ import annotations

from datetime import datetime, timedelta

from .. import config
from ..data.indices import in_window
from ..data.models import Flight, Leg, TravelerProfile
from ..state import Dataset


def leg_options(ds: Dataset, origin: str, dest: str,
                start: datetime, end: datetime,
                allow_compose: bool = True,
                force_compose: bool = False) -> list[Leg]:
    rows = in_window(ds.by_route.get((origin, dest), []), start, end)
    legs = [Leg(origin=origin, destination=dest, flights=[f]) for f in rows]

    if force_compose or (allow_compose and len(legs) < config.COMPOSE_WHEN_FEWER_THAN):
        legs += compose_connections(ds, origin, dest, start, end)
    return legs


def compose_connections(ds: Dataset, origin: str, dest: str,
                        start: datetime, end: datetime,
                        max_results: int = 40) -> list[Leg]:
    """Self-transfer itineraries built from two rows: (o->X) + (X->d),
    same-airport transfer within [90min, 6h] (blueprint assumption #5)."""
    out: list[Leg] = []
    lo = timedelta(minutes=config.SELF_TRANSFER_MIN_BUFFER_MIN)
    hi = timedelta(minutes=config.SELF_TRANSFER_MAX_BUFFER_MIN)
    for f1 in in_window(ds.from_origin.get(origin, []), start, end):
        mid = f1.destination
        if mid == dest or mid == origin:
            continue
        for f2 in in_window(ds.by_route.get((mid, dest), []),
                            f1.arrival_utc + lo, f1.arrival_utc + hi):
            buffer_min = int((f2.departure_utc - f1.arrival_utc).total_seconds() // 60)
            out.append(Leg(origin=origin, destination=dest, flights=[f1, f2],
                           self_transfer=True, transfer_airport=mid,
                           transfer_minutes=buffer_min))
    out.sort(key=lambda l: l.price)
    return out[:max_results]


def hard_filter_legs(legs: list[Leg], profile: TravelerProfile,
                     layover_cap: int | None = None) -> tuple[list[Leg], dict[str, int]]:
    """Hard constraints only (soft prefs are scored, never filtered).
    Returns (kept, filtered_counts) — counts feed the narrative
    ('removed 14 options over your 120-min layover cap')."""
    cap = layover_cap if layover_cap is not None else \
        int(profile.value("max_layover_minutes", 10 ** 6))
    party = profile.party_size
    counts = {"layover_cap": 0, "seats": 0}
    kept: list[Leg] = []
    for l in legs:
        if l.in_ticket_layover > cap:
            counts["layover_cap"] += 1
        elif l.seats_min < party:
            counts["seats"] += 1
        else:
            kept.append(l)
    return kept, counts
