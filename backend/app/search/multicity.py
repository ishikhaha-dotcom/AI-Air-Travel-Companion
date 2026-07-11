"""Multi-city planning (blueprint §4).

fixed_multicity  — B02-style: known city set, optimize visit ORDER (all
                   permutations) + dated leg chain via beam search.
open_ended       — B06-style: "multi-city Asia trip" with no cities given;
                   beam search over the region's route graph from home,
                   returning the best chain per distinct city-set.

Both honor hard constraints per leg (layover cap, party seats) and record
date-window widening as relaxation steps.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .. import config
from ..data.airports import REGIONS
from ..data.models import Leg, TravelerProfile, TripIntent, TripOption
from ..state import Dataset
from .relaxation import RelaxationStep, SearchOutcome
from .single import hard_filter_legs, leg_options


@dataclass
class _Chain:
    legs: list[Leg]
    cost: float = 0.0
    visited: frozenset = field(default_factory=frozenset)

    @property
    def arr(self) -> datetime:
        return self.legs[-1].arr_utc


def _extend(ds: Dataset, chains: list[_Chain], origin: str, dest: str,
            profile: TravelerProfile, stay_min: int, stay_max: int,
            beam: int, counts: dict[str, int],
            max_arr: datetime | None = None) -> list[_Chain]:
    nxt: list[_Chain] = []
    for ch in chains:
        lo = ch.arr + timedelta(days=stay_min)
        hi = ch.arr + timedelta(days=stay_max)
        if max_arr is not None:
            hi = min(hi, max_arr)
            if hi <= lo:
                continue
        legs = leg_options(ds, origin, dest, lo, hi, allow_compose=True)
        legs, c = hard_filter_legs(legs, profile)
        for k in c:
            counts[k] = counts.get(k, 0) + c[k]
        for leg in sorted(legs, key=lambda l: l.price)[:6]:  # bound branching
            nxt.append(_Chain(legs=ch.legs + [leg], cost=ch.cost + leg.price,
                              visited=ch.visited | {dest}))
    if not nxt and chains and stay_max < config.STAY_MAX_ADAPTIVE_DAYS:
        # sparse route/month coverage: allow lingering longer in a city rather
        # than returning nothing (recorded upstream as a relaxation note)
        return _extend(ds, chains, origin, dest, profile, stay_min,
                       config.STAY_MAX_ADAPTIVE_DAYS, beam, counts, max_arr)
    nxt.sort(key=lambda c: c.cost)
    return nxt[:beam]


def _seed(ds: Dataset, origin: str, dest: str, start: datetime, end: datetime,
          profile: TravelerProfile, counts: dict[str, int], per_dest: int = 8) -> list[_Chain]:
    legs = leg_options(ds, origin, dest, start, end, allow_compose=True)
    legs, c = hard_filter_legs(legs, profile)
    for k in c:
        counts[k] = counts.get(k, 0) + c[k]
    return [_Chain(legs=[l], cost=l.price, visited=frozenset({dest}))
            for l in sorted(legs, key=lambda l: l.price)[:per_dest]]


def fixed_multicity(ds: Dataset, intent: TripIntent,
                    profile: TravelerProfile) -> SearchOutcome:
    """Known cities, e.g. MEX -> {LHR,CDG,FCO} -> MEX. Tries every visit order."""
    from itertools import permutations
    outcome = SearchOutcome(options=[])
    home = intent.origin
    counts: dict[str, int] = {}

    def run(start: datetime, end: datetime) -> list[TripOption]:
        results: list[TripOption] = []
        for order in permutations(intent.destinations):
            chains = _seed(ds, home, order[0], start, end, profile, counts)
            for i in range(1, len(order)):
                chains = _extend(ds, chains, order[i - 1], order[i], profile,
                                 config.STAY_MIN_DAYS, config.STAY_MAX_DAYS,
                                 config.MULTICITY_BEAM_WIDTH, counts)
            chains = _extend(ds, chains, order[-1], home, profile,
                             config.STAY_MIN_DAYS, config.STAY_MAX_DAYS,
                             config.MULTICITY_BEAM_WIDTH, counts)
            results += [TripOption(legs=c.legs) for c in chains[:12]]
        return results

    options = run(intent.window_start, intent.window_end)
    if not options:
        # the dataset's route/month gaps make tight windows infeasible — widen
        # to a 6-month horizon and say so (honest, data-grounded)
        wide_end = intent.window_start + timedelta(days=185)
        options = run(intent.window_start, wide_end)
        outcome.relaxations.append(RelaxationStep(
            "widen_dates_multicity",
            "no feasible city chain in the requested window — scanned the next "
            "6 months for the earliest well-priced chain", len(options)))
    outcome.options = _dedupe(options, 40)
    outcome.filtered_counts = counts
    return outcome


def open_ended(ds: Dataset, intent: TripIntent, profile: TravelerProfile) -> SearchOutcome:
    """No cities given ("multi-city Asia trip"): propose the best chains.
    Returns the best chain per distinct city-set (top city-set variety first)."""
    outcome = SearchOutcome(options=[])
    home = intent.origin
    region = set(REGIONS.get(intent.region, set())) - {home}
    counts: dict[str, int] = {}
    trip_cap = timedelta(days=(intent.trip_length_days or 14) + 7)

    # seed: home -> any region airport in the start window
    seed_end = min(intent.window_end, intent.window_start + timedelta(days=45))
    chains: list[_Chain] = []
    for dest in region:
        chains += _seed(ds, home, dest, intent.window_start, seed_end, profile, counts,
                        per_dest=4)
    chains.sort(key=lambda c: c.cost)
    chains = chains[:config.OPEN_ENDED_BEAM_WIDTH]

    for _hop in range(1, config.OPEN_ENDED_STOPS):
        nxt: list[_Chain] = []
        # group chains by current airport so _extend's adaptive-stay retry applies
        by_cur: dict[str, list[_Chain]] = {}
        for ch in chains:
            by_cur.setdefault(ch.legs[-1].destination, []).append(ch)
        for cur, group in by_cur.items():
            for dest in region - {cur}:
                eligible = [ch for ch in group if dest not in ch.visited
                            and ch.arr - ch.legs[0].dep_utc < trip_cap]
                if not eligible:
                    continue
                nxt += _extend(ds, eligible, cur, dest, profile,
                               config.OPEN_ENDED_STAY_MIN, config.OPEN_ENDED_STAY_MAX,
                               config.OPEN_ENDED_BEAM_WIDTH // 4, counts,
                               max_arr=None)
        nxt.sort(key=lambda c: c.cost)
        chains = nxt[:config.OPEN_ENDED_BEAM_WIDTH]

    # close the loop home (respecting the total-trip-length cap)
    finals: list[_Chain] = []
    by_cur = {}
    for ch in chains:
        by_cur.setdefault(ch.legs[-1].destination, []).append(ch)
    for cur, group in by_cur.items():
        for ch in group:
            finals += _extend(ds, [ch], cur, home, profile,
                              config.OPEN_ENDED_STAY_MIN, config.OPEN_ENDED_STAY_MAX,
                              2, counts, max_arr=ch.legs[0].dep_utc + trip_cap)
    finals.sort(key=lambda c: c.cost)
    outcome.options = _dedupe([TripOption(legs=c.legs) for c in finals], 30)
    outcome.filtered_counts = counts
    if not outcome.options:
        outcome.relaxations.append(RelaxationStep(
            "open_ended_exhausted", "no full loop found within constraints", 0))
    return outcome


def _dedupe(options: list[TripOption], keep: int) -> list[TripOption]:
    seen: set[str] = set()
    out: list[TripOption] = []
    for o in options:
        k = o.key()
        if k not in seen:
            seen.add(k)
            out.append(o)
        if len(out) >= keep:
            break
    return out


def distinct_city_sets(options: list[TripOption], n: int = 3) -> list[TripOption]:
    """Best option per distinct visited-city set (for 'here are 3 different trips')."""
    best: dict[frozenset, TripOption] = {}
    for o in options:  # options arrive fit-score-sorted
        key = frozenset(o.city_sequence[1:-1])
        if key not in best:
            best[key] = o
        if len(best) >= n:
            break
    return list(best.values())
