"""Seasonal pricing + seat-scarcity awareness (judged expected_behavior).
All statements are empirical — computed from the dataset's own baselines."""
from __future__ import annotations

from ..data.models import TravelerProfile, TripIntent, TripOption
from ..state import Dataset

_SEASON_LABEL = {
    "year_end_holidays": "year-end holiday season",
    "thanksgiving_peak": "Thanksgiving peak",
    "summer_peak": "summer peak season",
    "spring_break": "spring-break season",
    "winter_low": "winter low season",
    "shoulder": "shoulder season",
}


def build_insights(ds: Dataset, options: list[TripOption], profile: TravelerProfile,
                   intent: TripIntent) -> list[str]:
    if not options:
        return []
    rec = options[0]
    out: list[str] = []
    flights = [f for l in rec.legs for f in l.flights]

    # --- seasonal pricing context (route+cabin medians vs shoulder) ---
    seen_routes: set[tuple] = set()
    for f in flights:
        key = (f.origin, f.destination, f.season)
        if key in seen_routes or f.season == "shoulder":
            continue
        seen_routes.add(key)
        prem = ds.baselines.seasonal_premium(f.origin, f.destination, f.cabin_class, f.season)
        label = _SEASON_LABEL.get(f.season, f.season)
        if prem is not None and abs(prem) >= 0.08:
            direction = "premium" if prem > 0 else "discount"
            out.append(f"{f.origin}→{f.destination} departs in {label}: fares run "
                       f"{abs(prem):.0%} {direction} vs shoulder season on this route "
                       f"(dataset medians).")
        elif f.is_holiday_season:
            out.append(f"{f.origin}→{f.destination} falls in {label} — expect elevated "
                       f"demand and limited availability.")

    # --- seat scarcity ---
    scarce = [f for f in flights if f.seats_available <= 3]
    if scarce:
        worst = min(scarce, key=lambda f: f.seats_available)
        out.append(f"Scarcity alert: only {worst.seats_available} seat(s) left on "
                   f"{worst.airline_code} {'/'.join(worst.flight_numbers)} "
                   f"({worst.origin}→{worst.destination}, demand: {worst.demand_level})"
                   + (f" — your party needs {intent.party_size}." if intent.party_size > 1 else "."))
    hot = [f for f in flights if f.demand_level in ("high", "peak") and f not in scarce]
    if hot and not scarce:
        out.append(f"Demand on {hot[0].origin}→{hot[0].destination} is "
                   f"{hot[0].demand_level} for these dates — booking early is wise.")

    # --- preferred cabin availability within the actual candidate window ---
    cabin = profile.value("preferred_cabin")
    if cabin and cabin != "Economy":
        offered = {f.cabin_class for o in options for l in o.legs for f in l.flights}
        if cabin not in offered:
            out.append(f"Heads-up: no {cabin} cabin is offered on this route for these "
                       f"dates (available: {', '.join(sorted(offered))}) — showing the "
                       f"closest cabins instead.")

    # --- user's own seasonal rules ---
    if profile.value("avoid_holiday_season") and any(f.is_holiday_season for f in flights):
        out.append("Note: this itinerary falls in a holiday period you usually avoid — "
                   "flagging since options were limited.")
    return out
