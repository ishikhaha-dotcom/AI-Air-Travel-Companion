"""Pipeline orchestrator: NLU → fusion → search → scoring → analytics → narrative.

recommend() is the single entry point used by both the FastAPI routes and the
benchmark harness, returning one JSON-able dict with the full reasoning trace.
"""
from __future__ import annotations

import time as _time

from . import config
from .data.airports import AIRPORTS
from .data.models import TravelerProfile, TripIntent, TripOption
from .explain.narrative import build_narrative, describe_option
from .insights.seasonal import build_insights
from .insights.tradeoffs import build_tradeoffs
from .nlu.intent_rules import parse_intent
from .profile.fusion import fuse, profile_highlights
from .ranking.scorer import score_options
from .search import flexdates
from .search.multicity import distinct_city_sets, fixed_multicity, open_ended
from .search.relaxation import SearchOutcome, search_with_relaxation
from .state import get_dataset


def _flight_json(f) -> dict:
    return {
        "flight_id": f.flight_id, "airline": f.airline_code,
        "airline_name": f.airline_name, "numbers": f.flight_numbers,
        "origin": f.origin, "destination": f.destination,
        "dep_utc": f.departure_utc.isoformat(), "arr_utc": f.arrival_utc.isoformat(),
        "dep_local": f.dep_local.strftime("%Y-%m-%d %H:%M"),
        "arr_local": f.arr_local.strftime("%Y-%m-%d %H:%M"),
        "daypart": f.dep_daypart, "redeye": f.is_redeye,
        "duration_minutes": f.duration_minutes, "stops": f.stops,
        "layover_airports": f.layover_airports, "layover_minutes": f.layover_minutes,
        "cabin": f.cabin_class, "price": f.price, "seats": f.seats_available,
        "otp": f.on_time_performance, "baggage_included": f.baggage_included,
        "refundable": f.refundable, "demand": f.demand_level, "season": f.season,
        "holiday": f.is_holiday_season, "aircraft": f.aircraft_type,
    }


def _leg_json(l) -> dict:
    return {
        "origin": l.origin, "destination": l.destination,
        "origin_city": AIRPORTS[l.origin].city,
        "destination_city": AIRPORTS[l.destination].city,
        "flights": [_flight_json(f) for f in l.flights],
        "self_transfer": l.self_transfer, "transfer_airport": l.transfer_airport,
        "transfer_minutes": l.transfer_minutes, "price": round(l.price, 2),
        "duration_minutes": l.duration_minutes, "stops": l.stops,
        "layover_total": l.layover_total, "in_ticket_layover": l.in_ticket_layover,
        "seats_min": l.seats_min,
    }


def _option_json(o: TripOption, party: int) -> dict:
    return {
        "key": o.key(), "fit_score": o.fit_score, "breakdown": o.breakdown,
        "goodness": o.goodness, "badges": o.badges, "why": o.why,
        "legs": [_leg_json(l) for l in o.legs],
        "total_price_pp": round(o.total_price_pp, 2),
        "total_price_party": round(o.total_price_pp * party, 2),
        "total_duration_minutes": o.total_duration_minutes,
        "total_stops": o.total_stops, "seats_min": o.seats_min,
        "self_transfer": o.any_self_transfer,
        "cities": o.city_sequence, "summary": describe_option(o, party),
        "dep_date": o.dep_utc.date().isoformat(),
    }


def _intent_json(i: TripIntent) -> dict:
    return {
        "origin": i.origin, "destinations": i.destinations, "trip_type": i.trip_type,
        "window_start": i.window_start.date().isoformat(),
        "window_end": i.window_end.date().isoformat(),
        "party_size": i.party_size, "purpose": i.purpose, "emphasis": i.emphasis,
        "region": i.region, "fixed_pattern": i.fixed_pattern,
        "trip_length_days": i.trip_length_days, "notes": i.notes,
    }


def recommend(user_id: str, query: str, top_n: int | None = None) -> dict:
    t0 = _time.perf_counter()
    ds = get_dataset()
    top_n = top_n or config.TOP_N_RESULTS
    user = ds.users[user_id]
    profile: TravelerProfile = fuse(user)
    intent = parse_intent(query, profile)
    if config.llm_mode() == "assist":
        from .nlu.intent_llm import enrich_intent
        intent = enrich_intent(query, intent)  # fills gaps only; never overrides rules

    if intent.trip_type == "multi_city":
        outcome: SearchOutcome = fixed_multicity(ds, intent, profile)
    elif intent.trip_type == "open_ended":
        outcome = open_ended(ds, intent, profile)
    else:
        outcome = search_with_relaxation(ds, intent, profile)

    scored, weights, weight_notes = score_options(outcome.options, profile, intent)

    if intent.trip_type == "open_ended":
        top = distinct_city_sets(scored, n=max(3, top_n))
    else:
        top = scored[:top_n]

    tradeoffs = build_tradeoffs(scored, intent)
    insights = build_insights(ds, scored, profile, intent)

    series, flex_insight = [], None
    if intent.trip_type in ("one_way", "round_trip") and scored:
        series = flexdates.price_by_date(scored)
        flex_insight = flexdates.date_shift_insight(series, scored[0])

    narrative = build_narrative(profile, intent, outcome, scored, weights,
                                weight_notes, tradeoffs, insights, flex_insight)
    llm_polished = False
    if config.llm_mode() == "assist":
        from .explain.llm_polish import polish
        narrative, llm_polished = polish(narrative)  # number-integrity checked
    party = max(1, intent.party_size)
    return {
        "user_id": user_id,
        "query": query,
        "sim_today": config.sim_today().isoformat(),
        "intent": _intent_json(intent),
        "profile_highlights": profile_highlights(profile, limit=10),
        "contradictions": profile.contradictions,
        "weights": weights, "weight_notes": weight_notes,
        "recommendations": [_option_json(o, party) for o in top],
        "anchors": {
            "cheapest": _option_json(min(scored, key=lambda o: o.total_price_pp), party)
            if scored else None,
            "fastest": _option_json(min(scored, key=lambda o: o.total_duration_minutes), party)
            if scored else None,
        },
        "tradeoffs": tradeoffs,
        "insights": insights,
        "price_by_date": series,
        "flex_insight": flex_insight,
        "relaxations": [{"name": r.name, "detail": r.detail, "count": r.result_count}
                        for r in outcome.relaxations],
        "route_facts": outcome.route_facts,
        "filtered_counts": outcome.filtered_counts,
        "narrative": narrative,
        "llm_polished": llm_polished,
        "elapsed_ms": round((_time.perf_counter() - t0) * 1000, 1),
        "total_candidates": len(scored),
    }
