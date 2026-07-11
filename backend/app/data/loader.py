"""CSV/JSON loaders with dtype coercion + startup data-QA report.

Run directly for the P0 smoke test:  python -m app.data.loader
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from .. import config
from .models import Flight, User


def _dt(s: str) -> datetime:
    # dataset format: 2026-05-23T16:15:00Z
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)


def _semilist(s: str) -> list[str]:
    s = (s or "").strip()
    if not s or s.lower() == "none":
        return []
    return [x.strip() for x in s.split(";") if x.strip()]


def _bool(s: str) -> bool:
    return s.strip().lower() == "true"


def load_flights(path: Path | None = None) -> list[Flight]:
    path = path or config.DATA_DIR / "flights_data.csv"
    flights: list[Flight] = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            f = Flight(
                flight_id=r["flight_id"],
                airline_code=r["airline_code"],
                airline_name=r["airline_name"],
                alliance=r["alliance"],
                flight_numbers=_semilist(r["flight_numbers"]),
                origin=r["origin"], origin_city=r["origin_city"],
                destination=r["destination"], destination_city=r["destination_city"],
                departure_utc=_dt(r["departure_utc"]),
                arrival_utc=_dt(r["arrival_utc"]),
                duration_minutes=int(float(r["duration_minutes"])),
                stops=int(r["stops"]),
                layover_airports=_semilist(r["layover_airports"]),
                layover_minutes=int(float(r["layover_minutes"] or 0)),
                cabin_class=r["cabin_class"],
                price=float(r["price"]),
                currency=r["currency"],
                seats_available=int(r["seats_available"]),
                aircraft_type=r["aircraft_type"],
                on_time_performance=int(float(r["on_time_performance"])),
                baggage_included=_bool(r["baggage_included"]),
                refundable=_bool(r["refundable"]),
                demand_level=r["demand_level"],
                season=r["season"],
                is_holiday_season=_bool(r["is_holiday_season"]),
            )
            f.finalize()
            flights.append(f)
    return flights


def load_users(path: Path | None = None) -> dict[str, User]:
    path = path or config.DATA_DIR / "user_data.csv"
    users: dict[str, User] = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            u = User(
                user_id=r["user_id"],
                age=int(r["age"]),
                home_airport=r["home_airport"],
                home_city=r["home_city"],
                frequent_flyer=r["frequent_flyer"],
                preferred_airlines=_semilist(r["preferred_airlines"]),
                preferred_cabin=r["preferred_cabin"],
                price_sensitivity=r["price_sensitivity"].strip().lower(),
                direct_preference=r["direct_preference"].strip().lower(),
                max_layover_minutes=int(float(r["max_layover_minutes"])),
                date_flexibility_days=int(float(r["date_flexibility_days"])),
                multi_city_tendency=r["multi_city_tendency"].strip().lower(),
                trip_purpose=r["trip_purpose"].strip().lower(),
                preferred_departure=r["preferred_departure"].strip().lower(),
                baggage_preference=r["baggage_preference"],
                seasonal_pattern=r["seasonal_pattern"],
                raw_history=[s.strip() for s in r["raw_history"].split("|") if s.strip()],
            )
            users[u.user_id] = u
    return users


def load_benchmarks(path: Path | None = None) -> list[dict]:
    path = path or config.DATA_DIR / "benchmark_prompts.json"
    return json.loads(Path(path).read_text(encoding="utf-8"))


def qa_report(flights: list[Flight], users: dict[str, User], benches: list[dict]) -> str:
    routes = {(f.origin, f.destination) for f in flights}
    airports = {f.origin for f in flights} | {f.destination for f in flights}
    deps = sorted(f.departure_utc for f in flights)
    bad_time = sum(1 for f in flights if f.arrival_utc <= f.departure_utc)
    lines = [
        "=== WayFinder data QA ===",
        f"flights: {len(flights):,} | airports: {len(airports)} | directed routes: {len(routes):,}",
        f"departures: {deps[0].date()} .. {deps[-1].date()} | SIM_TODAY: {config.sim_today()}",
        f"stops 0/1/2: {sum(1 for f in flights if f.stops==0):,}/"
        f"{sum(1 for f in flights if f.stops==1):,}/{sum(1 for f in flights if f.stops==2):,}",
        f"arrival<=departure anomalies: {bad_time}",
        f"users: {len(users)} | benchmark prompts: {len(benches)} "
        f"({', '.join(b['prompt_id'] for b in benches)})",
        f"redeye share: {sum(1 for f in flights if f.is_redeye)/len(flights):.1%}"
        f" | holiday rows: {sum(1 for f in flights if f.is_holiday_season):,}",
    ]
    missing_users = [b["user_id"] for b in benches if b["user_id"] not in users]
    lines.append(f"benchmark users missing: {missing_users or 'none'}")
    return "\n".join(lines)


if __name__ == "__main__":
    fl = load_flights()
    us = load_users()
    be = load_benchmarks()
    print(qa_report(fl, us, be))
