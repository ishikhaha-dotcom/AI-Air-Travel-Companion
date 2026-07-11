"""Deterministic narrative generator (the LLM-off path).

Consumes ONLY pipeline artifacts (trace-first principle from PROGRESS.md
conventions): fused preferences, filter counts, relaxation steps, route facts,
trade-offs, insights. Never re-derives — so every number it states is auditable.
"""
from __future__ import annotations

from ..data.airports import AIRPORTS
from ..data.models import (TravelerProfile, TripIntent, TripOption,
                           fmt_duration, fmt_money)
from ..search.relaxation import SearchOutcome


def describe_option(opt: TripOption, party: int) -> str:
    parts = []
    for leg in opt.legs:
        f0, fl = leg.flights[0], leg.flights[-1]
        seg = (f"{leg.origin} {f0.dep_local.strftime('%a %d %b %H:%M')} → "
               f"{leg.destination} {fl.arr_local.strftime('%a %d %b %H:%M')} "
               f"({'/'.join(sorted({f.airline_name for f in leg.flights}))}, "
               f"{'/'.join(leg.cabins)}, "
               f"{'direct' if leg.stops == 0 else str(leg.stops) + ' stop(s)'}")
        if leg.stops > 0:
            vias = [a for f in leg.flights for a in f.layover_airports]
            if leg.self_transfer:
                vias.append(leg.transfer_airport + "*")
            seg += f" via {', '.join(dict.fromkeys(vias))}, layover {fmt_duration(leg.layover_total)}"
        seg += f", {fmt_duration(leg.duration_minutes)})"
        parts.append(seg)
    price = fmt_money(opt.total_price_pp * party)
    per = f" ({fmt_money(opt.total_price_pp)}/person)" if party > 1 else ""
    return " ➜ ".join(parts) + f" — {price} total{per}"


def build_narrative(profile: TravelerProfile, intent: TripIntent,
                    outcome: SearchOutcome, options: list[TripOption],
                    weights: dict[str, float], weight_notes: list[str],
                    tradeoffs: dict, insights: list[str],
                    flex_insight: str | None = None) -> str:
    u = profile.user
    party = max(1, intent.party_size)
    md: list[str] = []

    dests = ", ".join(f"{d} ({AIRPORTS[d].city})" for d in intent.destinations) \
        if intent.destinations else f"{intent.region.title()} (open-ended)"
    md.append(f"### Trip plan for {u.user_id} — {u.home_city} traveler\n")
    md.append(f"**Understood as:** {intent.trip_type.replace('_', ' ')} from "
              f"{intent.origin} ({AIRPORTS[intent.origin].city}) to {dests}, "
              f"window {intent.window_start.date()} → {intent.window_end.date()}"
              + (f", party of {party}" if party > 1 else "") + ".")
    for n in intent.notes:
        md.append(f"- _{n}_")

    if profile.contradictions:
        md.append("\n**Signals we reconciled from your history:**")
        for c in profile.contradictions:
            md.append(f"- {c}")

    if outcome.route_facts:
        md.append("\n**Straight talk about this route:**")
        for fact in outcome.route_facts:
            md.append(f"- {fact}")

    if outcome.relaxations:
        md.append("\n**What we had to adjust (and why):**")
        for r in outcome.relaxations:
            md.append(f"- {r.detail} → {r.result_count} option(s)")

    filtered = {k: v for k, v in outcome.filtered_counts.items() if v}
    if filtered:
        labels = {"layover_cap": "exceeded your layover cap",
                  "seats": f"had fewer than {party} seats available"}
        md.append("\n**Filtered out for you:** " + "; ".join(
            f"{v} option(s) {labels.get(k, k)}" for k, v in filtered.items()) + ".")

    if not options:
        md.append("\n**No viable itineraries found** even after relaxation — "
                  "the dataset simply has no service matching this request. "
                  "Consider different dates or a nearby departure city.")
        return "\n".join(md)

    rec = options[0]
    md.append(f"\n**Top recommendation** (fit {rec.fit_score}/100):")
    md.append(f"> {describe_option(rec, party)}")
    if rec.why:
        md.append("\n**Why this one, specifically for you:**")
        for w in rec.why:
            md.append(f"- {w['reason']} — _{w['evidence']}_ ({w['source'].replace('_', ' ')})")

    if tradeoffs.get("statements"):
        md.append("\n**Trade-offs, in plain terms:**")
        for s in tradeoffs["statements"]:
            md.append(f"- {s}")

    if insights:
        md.append("\n**Season, demand & availability:**")
        for s in insights:
            md.append(f"- {s}")
    if flex_insight:
        md.append(f"- {flex_insight}")

    runners = options[1:3]
    if runners:
        md.append("\n**Also worth a look:**")
        for o in runners:
            md.append(f"- (fit {o.fit_score}) {describe_option(o, party)}")

    md.append(f"\n_Scoring weights used for you: " +
              ", ".join(f"{k} {v:.0%}" for k, v in weights.items()) + "._")
    for n in weight_notes:
        md.append(f"- _{n}_")

    courtesy = [p for p in profile.preferences
                if p.key in ("seat_wish", "premium_services_wish")]
    for p in courtesy:
        md.append(f"\n_Noted ({p.evidence}): {p.note}._")
    return "\n".join(md)
