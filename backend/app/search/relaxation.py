"""Transparent constraint-relaxation ladder (blueprint §4).

When a search returns zero options we relax stepwise and RECORD each step —
the B05 trap (LIS→SYD: no direct exists, user's 90-min layover cap can't be
met) must end in a narrated relaxation, never an error or silence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta

from .. import config
from ..data.models import TravelerProfile, TripIntent, TripOption
from ..state import Dataset
from . import roundtrip


@dataclass
class RelaxationStep:
    name: str
    detail: str
    result_count: int


@dataclass
class SearchOutcome:
    options: list[TripOption]
    filtered_counts: dict[str, int] = field(default_factory=dict)
    relaxations: list[RelaxationStep] = field(default_factory=list)
    route_facts: list[str] = field(default_factory=list)  # e.g. "no direct service exists"


def _route_facts(ds: Dataset, intent: TripIntent, profile: TravelerProfile) -> list[str]:
    """Whole-dataset facts about the requested route(s) — independent of dates.
    Powers honest expectation-setting ('no direct LIS→SYD exists at all')."""
    facts: list[str] = []
    pairs = [(intent.origin, d) for d in intent.destinations]
    for o, d in pairs:
        rows = ds.by_route.get((o, d), [])
        if not rows:
            facts.append(f"No {o}→{d} itineraries exist anywhere in the dataset — "
                         f"self-transfer connections required.")
            continue
        directs = [f for f in rows if f.stops == 0]
        if not directs and profile.value("direct_preference") in ("strong", "moderate"):
            best_lay = min(f.layover_minutes for f in rows if f.stops > 0)
            facts.append(f"No direct {o}→{d} flights exist in the entire dataset "
                         f"({len(rows)} itineraries, all with stops; shortest total "
                         f"layover on record: {best_lay} min).")
        cabin = profile.value("preferred_cabin")
        if cabin and cabin not in {f.cabin_class for f in rows}:
            cabins = sorted({f.cabin_class for f in rows})
            facts.append(f"No {cabin} cabin is sold on {o}→{d} in this dataset "
                         f"(available: {', '.join(cabins)}).")
    return facts


def search_with_relaxation(ds: Dataset, intent: TripIntent,
                           profile: TravelerProfile) -> SearchOutcome:
    """One-way / round-trip search with the documented relaxation ladder.
    (Multi-city has its own beam logic in multicity.py.)"""
    fn = roundtrip.round_trip_options if intent.trip_type == "round_trip" \
        else roundtrip.one_way_options
    outcome = SearchOutcome(options=[], route_facts=_route_facts(ds, intent, profile))
    cap = int(profile.value("max_layover_minutes", 10 ** 6))
    flex = int(profile.value("date_flexibility_days", 0) or 0)

    options, counts = fn(ds, intent, profile)
    outcome.filtered_counts = counts
    if options:
        outcome.options = options
        return outcome

    # ① widen dates by the user's own flexibility
    if flex > 0:
        intent.window_start -= timedelta(days=flex)
        intent.window_end += timedelta(days=flex)
        if intent.window_start.date() < config.sim_today():
            from datetime import datetime, time, timezone
            intent.window_start = datetime.combine(config.sim_today(), time.min, tzinfo=timezone.utc)
        options, counts = fn(ds, intent, profile)
        outcome.filtered_counts = counts
        outcome.relaxations.append(RelaxationStep(
            "widen_dates_flex", f"widened window by your ±{flex}-day flexibility",
            len(options)))
        if options:
            outcome.options = options
            return outcome

    # ①b build self-transfer connections (published fares kept the weekday
    # pattern unreachable — B04's MEL↔JFK never pairs on matching dates)
    options, counts = fn(ds, intent, profile, force_compose=True)
    outcome.filtered_counts = counts
    outcome.relaxations.append(RelaxationStep(
        "compose_self_transfer",
        "no published itinerary pairing worked — added self-transfer connections "
        "built from separate tickets (90min–6h transfer buffer)", len(options)))
    if options:
        outcome.options = options
        return outcome

    # ①c weekday-pattern trips: if no pairing matches the exact weekday pattern
    # even with composed connections, drop the pattern and say so
    if intent.fixed_pattern:
        saved_pattern = dict(intent.fixed_pattern)
        intent.fixed_pattern = {}
        options, counts = fn(ds, intent, profile, force_compose=True)
        outcome.filtered_counts = counts
        outcome.relaxations.append(RelaxationStep(
            "drop_weekday_pattern",
            "no itinerary pair matches the exact weekday pattern in the dataset — "
            "showing the closest available round trips instead", len(options)))
        if options:
            outcome.options = options
            return outcome
        intent.fixed_pattern = saved_pattern

    # ② then ③ relax the layover cap in documented increments
    for factor in config.LAYOVER_RELAX_FACTORS:
        relaxed_cap = int(cap * factor)
        options, counts = fn(ds, intent, profile, layover_cap=relaxed_cap)
        outcome.filtered_counts = counts
        outcome.relaxations.append(RelaxationStep(
            "relax_layover_cap",
            f"layover cap relaxed {cap}→{relaxed_cap} min (×{factor})", len(options)))
        if options:
            outcome.options = options
            return outcome

    # ④ widen dates aggressively (+30d both sides), keep relaxed cap
    intent.window_start -= timedelta(days=config.DATE_WIDEN_EXTRA_DAYS)
    intent.window_end += timedelta(days=config.DATE_WIDEN_EXTRA_DAYS)
    from datetime import datetime, time, timezone
    if intent.window_start.date() < config.sim_today():
        intent.window_start = datetime.combine(config.sim_today(), time.min, tzinfo=timezone.utc)
    relaxed_cap = int(cap * config.LAYOVER_RELAX_FACTORS[-1])
    options, counts = fn(ds, intent, profile, layover_cap=relaxed_cap)
    outcome.filtered_counts = counts
    outcome.relaxations.append(RelaxationStep(
        "widen_dates_extra", f"window widened by ±{config.DATE_WIDEN_EXTRA_DAYS} days",
        len(options)))
    if options:
        outcome.options = options
        return outcome

    # ⑤ nearest-month scan: find when this route is actually served
    o = intent.origin
    for d in intent.destinations[:1]:
        rows = [f for f in ds.by_route.get((o, d), [])
                if f.departure_utc.date() >= config.sim_today()]
        if rows:
            first = rows[0].departure_utc
            month_start = first.replace(day=1, hour=0, minute=0, second=0)
            nxt = (month_start + timedelta(days=32)).replace(day=1)
            intent.window_start, intent.window_end = month_start, nxt
            options, counts = fn(ds, intent, profile, layover_cap=relaxed_cap)
            outcome.filtered_counts = counts
            outcome.relaxations.append(RelaxationStep(
                "nearest_service_month",
                f"moved to the nearest month with {o}→{d} service "
                f"({first.strftime('%B %Y')})", len(options)))
    outcome.options = options
    return outcome
