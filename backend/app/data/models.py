"""Core domain dataclasses shared across the pipeline.

Flight  = one CSV row (a complete priced itinerary with 0-2 built-in stops).
Leg     = one traveler movement A->B: a single Flight, or two Flights composed
          into a self-transfer connection (search/single.py).
TripOption = the unit we score and recommend: 1 leg (one-way), 2 legs (round
          trip), or N legs (multi-city).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from .airports import tzinfo


@dataclass(slots=True)
class Flight:
    flight_id: str
    airline_code: str
    airline_name: str
    alliance: str
    flight_numbers: list[str]
    origin: str
    origin_city: str
    destination: str
    destination_city: str
    departure_utc: datetime
    arrival_utc: datetime
    duration_minutes: int
    stops: int
    layover_airports: list[str]
    layover_minutes: int  # TOTAL across stops (assumption #3 in blueprint)
    cabin_class: str
    price: float
    currency: str
    seats_available: int
    aircraft_type: str
    on_time_performance: int
    baggage_included: bool
    refundable: bool
    demand_level: str
    season: str
    is_holiday_season: bool
    # derived at load time
    dep_local: datetime = field(default=None)  # type: ignore[assignment]
    arr_local: datetime = field(default=None)  # type: ignore[assignment]
    dep_daypart: str = ""
    is_redeye: bool = False

    def finalize(self) -> None:
        self.dep_local = self.departure_utc.astimezone(tzinfo(self.origin))
        self.arr_local = self.arrival_utc.astimezone(tzinfo(self.destination))
        h = self.dep_local.hour
        self.dep_daypart = ("morning" if 5 <= h <= 11 else
                            "afternoon" if 12 <= h <= 16 else
                            "evening" if 17 <= h <= 21 else "night")
        self.is_redeye = h >= 22 or h <= 5


@dataclass(slots=True)
class User:
    user_id: str
    age: int
    home_airport: str
    home_city: str
    frequent_flyer: str
    preferred_airlines: list[str]
    preferred_cabin: str
    price_sensitivity: str      # none|low|medium|high
    direct_preference: str      # none|moderate|strong
    max_layover_minutes: int
    date_flexibility_days: int
    multi_city_tendency: str
    trip_purpose: str           # business|leisure|mixed
    preferred_departure: str    # morning|afternoon|evening|any
    baggage_preference: str
    seasonal_pattern: str
    raw_history: list[str]      # pipe-split snippets, stripped


@dataclass(slots=True)
class Preference:
    """One fused preference with full provenance (the audit trail)."""
    id: str                      # e.g. "pref_layover_cap"
    key: str                     # machine key, e.g. "max_layover_minutes"
    value: Any
    strength: str                # hard | strong | soft
    source: str                  # structured | raw_history | query | derived
    evidence: str                # column name or verbatim quoted snippet
    confidence: float = 1.0
    note: str = ""


@dataclass(slots=True)
class TravelerProfile:
    user: User
    preferences: list[Preference]
    party_size: int = 1
    contradictions: list[str] = field(default_factory=list)

    def get(self, key: str) -> Optional[Preference]:
        for p in self.preferences:  # fusion guarantees one winner per key
            if p.key == key:
                return p
        return None

    def value(self, key: str, default: Any = None) -> Any:
        p = self.get(key)
        return p.value if p is not None else default


@dataclass(slots=True)
class TripIntent:
    origin: str
    destinations: list[str]          # IATA codes; empty for open_ended
    trip_type: str                   # one_way | round_trip | multi_city | open_ended
    window_start: datetime           # UTC, inclusive
    window_end: datetime             # UTC, inclusive
    party_size: int = 1
    purpose: str = ""                # business | leisure | mixed | ""
    emphasis: str = ""               # cheapest | fastest | comfort | ""
    region: str = ""                 # for open_ended, e.g. "asia"
    fixed_pattern: dict[str, Any] = field(default_factory=dict)
    # e.g. {"out_dow": 1, "ret_dow": 3, "arrive_by_hour": 9} for "Tue meeting, back Thu"
    trip_length_days: int = 0        # open_ended target trip length
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Leg:
    origin: str
    destination: str
    flights: list[Flight]            # 1 row, or 2 rows for self-transfer
    self_transfer: bool = False
    transfer_airport: str = ""
    transfer_minutes: int = 0

    @property
    def dep_utc(self) -> datetime:
        return self.flights[0].departure_utc

    @property
    def arr_utc(self) -> datetime:
        return self.flights[-1].arrival_utc

    @property
    def price(self) -> float:
        return sum(f.price for f in self.flights)

    @property
    def duration_minutes(self) -> int:
        return int((self.arr_utc - self.dep_utc).total_seconds() // 60)

    @property
    def stops(self) -> int:
        return sum(f.stops for f in self.flights) + (1 if self.self_transfer else 0)

    @property
    def layover_total(self) -> int:
        return sum(f.layover_minutes for f in self.flights) + self.transfer_minutes

    @property
    def in_ticket_layover(self) -> int:
        """Layover minutes inside published tickets only — the user's
        max_layover cap applies to this, not to self-transfer stopovers."""
        return sum(f.layover_minutes for f in self.flights)

    @property
    def seats_min(self) -> int:
        return min(f.seats_available for f in self.flights)

    @property
    def airlines(self) -> list[str]:
        return sorted({f.airline_code for f in self.flights})

    @property
    def cabins(self) -> list[str]:
        return sorted({f.cabin_class for f in self.flights})


@dataclass(slots=True)
class TripOption:
    legs: list[Leg]
    # scoring artifacts (set by ranking/scorer.py)
    fit_score: float = 0.0
    breakdown: dict[str, float] = field(default_factory=dict)   # feature -> weighted pts
    goodness: dict[str, float] = field(default_factory=dict)    # feature -> raw 0..1
    badges: list[str] = field(default_factory=list)
    why: list[dict[str, str]] = field(default_factory=list)     # evidence-cited reasons

    @property
    def total_price_pp(self) -> float:
        return sum(l.price for l in self.legs)

    @property
    def total_duration_minutes(self) -> int:
        return sum(l.duration_minutes for l in self.legs)

    @property
    def total_stops(self) -> int:
        return sum(l.stops for l in self.legs)

    @property
    def max_leg_layover(self) -> int:
        return max((l.layover_total for l in self.legs), default=0)

    @property
    def seats_min(self) -> int:
        return min(l.seats_min for l in self.legs)

    @property
    def dep_utc(self) -> datetime:
        return self.legs[0].dep_utc

    @property
    def arr_utc(self) -> datetime:
        return self.legs[-1].arr_utc

    @property
    def any_self_transfer(self) -> bool:
        return any(l.self_transfer for l in self.legs)

    @property
    def city_sequence(self) -> list[str]:
        seq = [self.legs[0].origin]
        seq += [l.destination for l in self.legs]
        return seq

    def key(self) -> str:
        return "|".join(f.flight_id for l in self.legs for f in l.flights)


def fmt_duration(minutes: int) -> str:
    h, m = divmod(int(minutes), 60)
    return f"{h}h{m:02d}m" if h else f"{m}m"


def fmt_money(x: float) -> str:
    return f"${x:,.0f}" if x >= 100 else f"${x:,.2f}"
