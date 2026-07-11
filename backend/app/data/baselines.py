"""Precomputed seasonal price baselines.

Powers empirical statements like "year-end fares on this route run +65% vs
shoulder season" and the flexible-date price calendar context.
"""
from __future__ import annotations

from collections import defaultdict
from statistics import median

from .models import Flight


class Baselines:
    def __init__(self, flights: list[Flight]):
        by_ods: dict[tuple[str, str, str], list[float]] = defaultdict(list)          # (o,d,season)
        by_odcs: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)    # (o,d,cabin,season)
        by_odm: dict[tuple[str, str, str], list[float]] = defaultdict(list)          # (o,d,YYYY-MM)
        for f in flights:
            by_ods[(f.origin, f.destination, f.season)].append(f.price)
            by_odcs[(f.origin, f.destination, f.cabin_class, f.season)].append(f.price)
            by_odm[(f.origin, f.destination, f.departure_utc.strftime("%Y-%m"))].append(f.price)
        self.route_season = {k: median(v) for k, v in by_ods.items()}
        self.route_cabin_season = {k: median(v) for k, v in by_odcs.items()}
        self.route_month = {k: median(v) for k, v in by_odm.items()}

    def seasonal_premium(self, origin: str, dest: str, cabin: str, season: str) -> float | None:
        """Premium (e.g. +0.65) of `season` vs shoulder on this route+cabin; None if unknown."""
        if season == "shoulder":
            return 0.0
        base = (self.route_cabin_season.get((origin, dest, cabin, "shoulder"))
                or self.route_season.get((origin, dest, "shoulder")))
        cur = (self.route_cabin_season.get((origin, dest, cabin, season))
               or self.route_season.get((origin, dest, season)))
        if not base or not cur:
            return None
        return (cur - base) / base
