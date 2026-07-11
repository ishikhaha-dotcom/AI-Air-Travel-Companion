"""Per-candidate feature 'goodness' values in [0,1] (1 = best), normalized
within the candidate set. Kept separate from weights so the UI can show raw
feature bars alongside weighted contributions."""
from __future__ import annotations

from ..data.airports import alliance_of
from ..data.models import TravelerProfile, TripIntent, TripOption
from ..profile.fusion import needs_checked_bags
from .weights import stop_penalty_scale

CABIN_TIER = {"Economy": 0, "Premium Economy": 1, "Business": 2, "First": 3}


def _norm(values: list[float]) -> list[float]:
    lo, hi = min(values), max(values)
    if hi - lo < 1e-9:
        return [0.5] * len(values)
    return [(v - lo) / (hi - lo) for v in values]


def compute_features(options: list[TripOption], profile: TravelerProfile,
                     intent: TripIntent) -> None:
    """Sets opt.goodness for every option in place."""
    if not options:
        return
    party = max(1, intent.party_size)
    prices = _norm([o.total_price_pp * party for o in options])
    times = _norm([float(o.total_duration_minutes) for o in options])

    sscale = stop_penalty_scale(profile)
    avoid_redeye = bool(profile.value("avoid_redeye"))
    redeye_if_cheap = bool(profile.value("redeye_ok_if_cheaper"))
    kids = intent.party_size > 1 and profile.value("party_size") is not None
    daypart = profile.value("preferred_departure")
    cap = int(profile.value("max_layover_minutes", 600) or 600)
    preferred_airlines = list(profile.value("preferred_airlines") or [])
    liked = profile.value("airline_liked")
    if liked and liked not in preferred_airlines:
        preferred_airlines.append(liked)
    pref_alliances = {alliance_of(a) for a in preferred_airlines} - {"none"}
    cabin = profile.value("preferred_cabin", "Economy")
    bags_needed = needs_checked_bags(profile)
    purpose = intent.purpose or profile.value("purpose", "")
    loyalty_off = profile.value("airline_loyalty") == "none"

    cheapest_price = min(o.total_price_pp for o in options)

    for i, opt in enumerate(options):
        flights = [f for l in opt.legs for f in l.flights]

        # --- convenience: start perfect, subtract documented penalties ---
        conv = 1.0
        conv -= min(0.66, 0.22 * sscale * opt.total_stops)
        has_redeye = any(f.is_redeye for f in flights)
        if has_redeye:
            if avoid_redeye:
                conv -= 0.25 * (2.0 if kids or profile.value("avoid_night_departure") else 1.0)
            elif redeye_if_cheap:
                conv -= 0.0 if abs(opt.total_price_pp - cheapest_price) < 1 else 0.10
            else:
                conv -= 0.08
        if daypart and opt.legs[0].flights[0].dep_daypart != daypart:
            conv -= 0.12
        if profile.value("avoid_night_departure") and \
                opt.legs[0].flights[0].dep_daypart == "night":
            conv -= 0.15
        if opt.any_self_transfer:
            conv -= 0.18
            longest_transfer = max(l.transfer_minutes for l in opt.legs if l.self_transfer)
            if longest_transfer > 8 * 60:
                conv -= 0.10  # overnight/long stopover on separate tickets
        conv -= min(0.10, 0.10 * (opt.max_leg_layover / max(cap, 1)))

        # --- reliability: on-time performance + seat-scarcity risk ---
        otp = sum(f.on_time_performance for f in flights) / len(flights) / 100.0
        seat_comfort = min(1.0, opt.seats_min / max(3.0, party + 1.0))
        reliability = 0.7 * otp + 0.3 * seat_comfort

        # --- preference fit: airline / cabin / baggage / refundability ---
        parts: list[float] = []
        if preferred_airlines and not loyalty_off:
            codes = {f.airline_code for f in flights}
            if codes & set(preferred_airlines):
                parts.append(1.0)
            elif pref_alliances & {f.alliance for f in flights}:
                parts.append(0.6)
            else:
                parts.append(0.35)
        want_tier = CABIN_TIER.get(cabin, 0)
        tiers = [CABIN_TIER.get(f.cabin_class, 0) for f in flights]
        dist = min(abs(t - want_tier) for t in tiers)
        parts.append({0: 1.0, 1: 0.55}.get(dist, 0.25))
        if bags_needed > 0:
            parts.append(1.0 if all(f.baggage_included for f in flights) else 0.3)
        if purpose == "business":
            parts.append(1.0 if all(f.refundable for f in flights) else 0.5)
        preffit = sum(parts) / len(parts) if parts else 0.5

        opt.goodness = {
            "price": round(1.0 - prices[i], 4),
            "time": round(1.0 - times[i], 4),
            "convenience": round(max(0.0, min(1.0, conv)), 4),
            "reliability": round(max(0.0, min(1.0, reliability)), 4),
            "preffit": round(max(0.0, min(1.0, preffit)), 4),
        }
