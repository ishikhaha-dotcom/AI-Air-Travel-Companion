"""Round-trip pairing, including weekday patterns like
"NYC for a Tuesday meeting, back Thursday" (B04): timezone-correct
arrive-before logic using destination-local time.
"""
from __future__ import annotations

from datetime import datetime, time, timedelta, timezone

from ..data.airports import tzinfo
from ..data.models import Leg, TravelerProfile, TripIntent, TripOption
from ..state import Dataset
from .single import hard_filter_legs, leg_options

MIN_TURNAROUND_H = 4
MAX_PAIRS = 400


def _merge_counts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {k: a.get(k, 0) + b.get(k, 0) for k in set(a) | set(b)}


def round_trip_options(ds: Dataset, intent: TripIntent, profile: TravelerProfile,
                       layover_cap: int | None = None,
                       allow_compose: bool = True,
                       force_compose: bool = False) -> tuple[list[TripOption], dict[str, int]]:
    o, d = intent.origin, intent.destinations[0]
    outs = leg_options(ds, o, d, intent.window_start, intent.window_end,
                       allow_compose, force_compose)
    rets = leg_options(ds, d, o, intent.window_start,
                       intent.window_end + timedelta(days=7), allow_compose, force_compose)
    outs, c1 = hard_filter_legs(outs, profile, layover_cap)
    rets, c2 = hard_filter_legs(rets, profile, layover_cap)
    counts = _merge_counts(c1, c2)

    pat = intent.fixed_pattern
    options: list[TripOption] = []
    dtz = tzinfo(d)
    for out in outs:
        arr_local = out.arr_utc.astimezone(dtz)
        if pat:
            # find the target weekday (e.g. Tuesday) the traveler must be there for
            days_ahead = (pat["out_dow"] - arr_local.weekday()) % 7
            target_day = (arr_local + timedelta(days=days_ahead)).date()
            deadline = datetime.combine(target_day, time(pat.get("arrive_by_hour", 23)),
                                        tzinfo=dtz)
            if not (deadline - timedelta(days=3) <= arr_local <= deadline):
                continue  # must land within 3 days before the meeting, before it starts
        for ret in rets:
            if ret.dep_utc < out.arr_utc + timedelta(hours=MIN_TURNAROUND_H):
                continue
            if pat:
                ret_local = ret.dep_utc.astimezone(dtz)
                # return on the named day (±1 — data is sparse; deviation is narrated)
                want = (target_day + timedelta(days=(pat["ret_dow"] - pat["out_dow"]) % 7))
                if abs((ret_local.date() - want).days) > 1:
                    continue
            elif ret.dep_utc > out.arr_utc + timedelta(days=14):
                continue  # unpatterned round trips: cap stay at 2 weeks
            options.append(TripOption(legs=[out, ret]))
            if len(options) >= MAX_PAIRS:
                return options, counts
    return options, counts


def one_way_options(ds: Dataset, intent: TripIntent, profile: TravelerProfile,
                    layover_cap: int | None = None,
                    allow_compose: bool = True,
                    force_compose: bool = False) -> tuple[list[TripOption], dict[str, int]]:
    legs = leg_options(ds, intent.origin, intent.destinations[0],
                       intent.window_start, intent.window_end, allow_compose, force_compose)
    legs, counts = hard_filter_legs(legs, profile, layover_cap)
    return [TripOption(legs=[l]) for l in legs], counts
