"""Deterministic intent parser (the LLM-off path; unit-tested on all 6 benchmarks).

City gazetteer scan + trip-shape/emphasis keywords -> TripIntent.
"""
from __future__ import annotations

import re

from ..data.airports import AIRPORTS, CITY_ALIASES, REGIONS
from ..data.models import TravelerProfile, TripIntent
from .dates import resolve_window

# longest aliases first so "mexico city" beats "mexico"
_ALIASES = sorted(CITY_ALIASES.items(), key=lambda kv: -len(kv[0]))


def _find_cities(q: str) -> list[str]:
    found: list[tuple[int, str]] = []
    taken: list[tuple[int, int]] = []
    for alias, iata in _ALIASES:
        for m in re.finditer(rf"\b{re.escape(alias)}\b", q):
            span = (m.start(), m.end())
            if any(s < span[1] and span[0] < e for s, e in taken):
                continue  # inside an already-matched longer alias
            taken.append(span)
            found.append((m.start(), iata))
    found.sort()
    out: list[str] = []
    for _, iata in found:
        if iata not in out:
            out.append(iata)
    return out


def parse_intent(query: str, profile: TravelerProfile) -> TripIntent:
    q = query.lower()
    user = profile.user
    notes: list[str] = []

    # origin: home unless "from <city>" names another dataset city
    origin = user.home_airport
    if re.search(r"from\s+home\b", q):
        notes.append(f"“from home” -> {origin} ({user.home_city}, profile home_airport)")
    else:
        m = re.search(r"from\s+((?:[a-z]+\s?){1,3})", q)
        cities = _find_cities(m.group(1).split(" to ")[0]) if m else []
        if cities and cities[0] != origin:
            origin = cities[0]
            notes.append(f"origin overridden by query -> {origin}")
        else:
            notes.append(f"origin defaulted to home airport {origin} ({user.home_city})")

    destinations = [c for c in _find_cities(q) if c != origin]

    # region for open-ended trips ("multi-city Asia trip")
    region = ""
    for rname in REGIONS:
        if re.search(rf"\b{rname}\b", q):
            region = rname
            break

    # window
    win = resolve_window(query, profile)
    notes.extend(win["notes"])

    # trip type
    multi_words = bool(re.search(r"multi-?city|one journey|trip across|tour", q))
    round_words = bool(re.search(r"\bback\b|\breturn\b|round.?trip", q)) or bool(win["fixed_pattern"])
    if (multi_words or len(destinations) >= 2) and destinations:
        trip_type = "multi_city"
    elif region and (multi_words or not destinations):
        trip_type = "open_ended"
    elif round_words and destinations:
        trip_type = "round_trip"
    elif destinations:
        trip_type = "one_way"
    else:
        trip_type = "open_ended" if region else "one_way"

    # emphasis
    emphasis = ""
    if re.search(r"cheap|budget|lowest|deal", q):
        emphasis = "cheapest"
    elif re.search(r"fastest|quickest|shortest|asap", q):
        emphasis = "fastest"
    elif re.search(r"comfort|luxur|first class|business class|relax", q):
        emphasis = "comfort"

    # purpose
    purpose = user.trip_purpose
    if re.search(r"meeting|work trip|business trip|conference|office", q):
        purpose = "business"
        notes.append("purpose inferred as business (“meeting”)")

    trip_len = win["trip_length_days"]
    if trip_type == "open_ended" and not trip_len:
        trip_len = 14
        notes.append("open-ended trip length defaulted to 14 days")

    return TripIntent(
        origin=origin, destinations=destinations, trip_type=trip_type,
        window_start=win["start"], window_end=win["end"],
        party_size=profile.party_size, purpose=purpose, emphasis=emphasis,
        region=region, fixed_pattern=win["fixed_pattern"],
        trip_length_days=trip_len, notes=notes,
    )
