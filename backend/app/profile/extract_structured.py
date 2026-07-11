"""Structured-column extractor: user_data.csv columns -> provenance-tagged Preferences."""
from __future__ import annotations

import re

from ..data.models import Preference, User

_MONTHS = {m: i + 1 for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}

SHOULDER_MONTHS = [3, 4, 5, 9, 10]
PEAK_MONTHS = [6, 7, 8, 12]


def parse_seasonal_pattern(text: str) -> tuple[list[int], bool, str]:
    """-> (allowed_months (empty = any), avoid_holiday_season, note)"""
    t = text.lower()
    months = sorted({_MONTHS[m] for m in _MONTHS if re.search(rf"\b{m}", t)})
    avoid_holidays = bool(re.search(r"avoid\w*\s+holiday", t))
    if months:
        # ranges like "jul-aug" already captured word-by-word; add in-between months
        expanded = set(months)
        for a, b in re.findall(r"\b(\w{3})\w*\s*-\s*(\w{3})", t):
            if a[:3] in _MONTHS and b[:3] in _MONTHS:
                lo, hi = _MONTHS[a[:3]], _MONTHS[b[:3]]
                if lo <= hi:
                    expanded.update(range(lo, hi + 1))
        return sorted(expanded), avoid_holidays, text
    if "shoulder" in t:
        return SHOULDER_MONTHS, avoid_holidays, text
    if "peak" in t or "summer" in t:
        return ([6, 7, 8] if "summer" in t else PEAK_MONTHS), avoid_holidays, text
    return [], avoid_holidays, text


def parse_baggage(text: str) -> dict:
    t = text.lower()
    out = {"carryon_only": False, "checked_bags": 0, "stroller": False}
    if "carry-on only" in t or "carry on only" in t:
        out["carryon_only"] = True
    m = re.search(r"(\d+)\s*checked", t)
    if m:
        out["checked_bags"] = int(m.group(1))
    if "stroller" in t:
        out["stroller"] = True
    return out


def extract_structured(user: User) -> list[Preference]:
    P = []

    def add(id_, key, value, strength, evidence, note=""):
        P.append(Preference(id=id_, key=key, value=value, strength=strength,
                            source="structured", evidence=f"profile field {evidence}", note=note))

    add("s_home", "home_airport", user.home_airport, "hard", f"home_airport={user.home_airport}")
    add("s_layover", "max_layover_minutes", user.max_layover_minutes, "hard",
        f"max_layover_minutes={user.max_layover_minutes}")
    add("s_direct", "direct_preference", user.direct_preference, "strong",
        f"direct_preference={user.direct_preference}")
    add("s_price", "price_sensitivity", user.price_sensitivity, "strong",
        f"price_sensitivity={user.price_sensitivity}")
    if user.preferred_airlines:
        add("s_airlines", "preferred_airlines", user.preferred_airlines, "soft",
            f"preferred_airlines={';'.join(user.preferred_airlines)}")
    add("s_cabin", "preferred_cabin", user.preferred_cabin, "soft",
        f"preferred_cabin={user.preferred_cabin}")
    if user.preferred_departure and user.preferred_departure != "any":
        add("s_daypart", "preferred_departure", user.preferred_departure, "soft",
            f"preferred_departure={user.preferred_departure}")
    add("s_flex", "date_flexibility_days", user.date_flexibility_days, "soft",
        f"date_flexibility_days={user.date_flexibility_days}")
    add("s_purpose", "purpose", user.trip_purpose, "soft", f"trip_purpose={user.trip_purpose}")
    add("s_mct", "multi_city_tendency", user.multi_city_tendency, "soft",
        f"multi_city_tendency={user.multi_city_tendency}")

    bag = parse_baggage(user.baggage_preference)
    add("s_bags", "baggage", bag, "soft", f"baggage_preference='{user.baggage_preference}'")

    months, avoid_hol, note = parse_seasonal_pattern(user.seasonal_pattern)
    if months:
        add("s_season", "seasonal_months", months, "strong",
            f"seasonal_pattern='{user.seasonal_pattern}'", note="travel window restricted")
    if avoid_hol:
        add("s_avoidhol", "avoid_holiday_season", True, "strong",
            f"seasonal_pattern='{user.seasonal_pattern}'")
    if user.frequent_flyer and user.frequent_flyer.lower() != "none":
        add("s_ff", "frequent_flyer", user.frequent_flyer, "soft",
            f"frequent_flyer={user.frequent_flyer}")
    return P
