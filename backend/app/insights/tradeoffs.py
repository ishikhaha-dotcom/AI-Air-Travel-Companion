"""Recommended vs Cheapest vs Fastest triad with human-framed deltas
('direct saves 6h10m for +$142 ≈ $23/hr') — a judged expected_behavior."""
from __future__ import annotations

from ..data.models import TripIntent, TripOption, fmt_duration, fmt_money


def build_tradeoffs(options: list[TripOption], intent: TripIntent) -> dict:
    """options must already be fit-score sorted (options[0] = recommended)."""
    if not options:
        return {}
    rec = options[0]
    cheapest = min(options, key=lambda o: o.total_price_pp)
    fastest = min(options, key=lambda o: o.total_duration_minutes)
    party = max(1, intent.party_size)

    def brief(o: TripOption, label: str) -> dict:
        return {"label": label, "key": o.key(), "fit_score": o.fit_score,
                "price_pp": round(o.total_price_pp, 2),
                "price_party": round(o.total_price_pp * party, 2),
                "duration_minutes": o.total_duration_minutes,
                "duration": fmt_duration(o.total_duration_minutes),
                "stops": o.total_stops}

    out = {"recommended": brief(rec, "Recommended"),
           "cheapest": brief(cheapest, "Cheapest"),
           "fastest": brief(fastest, "Fastest"),
           "statements": []}

    if cheapest.key() != rec.key():
        dp = (rec.total_price_pp - cheapest.total_price_pp) * party
        dt = cheapest.total_duration_minutes - rec.total_duration_minutes
        s = (f"Cheapest option saves {fmt_money(abs(dp))} vs our pick")
        if dt > 0:
            s += (f" but takes {fmt_duration(dt)} longer "
                  f"({cheapest.total_stops} stop(s) vs {rec.total_stops})")
            if dt >= 60 and dp > 0:
                s += f" — you'd be selling your time at {fmt_money(dp / (dt / 60))}/hr"
        out["statements"].append(s + ".")
    else:
        out["statements"].append("Our recommended pick is also the cheapest available.")

    if fastest.key() != rec.key():
        dt = rec.total_duration_minutes - fastest.total_duration_minutes
        dp = (fastest.total_price_pp - rec.total_price_pp) * party
        if dt > 0:
            s = f"Fastest option saves {fmt_duration(dt)}"
            s += (f" for {fmt_money(dp)} more" if dp > 0
                  else f" and costs {fmt_money(abs(dp))} less" if dp < 0 else "")
            out["statements"].append(s + ".")
    else:
        out["statements"].append("Our recommended pick is also the fastest available.")

    directs = [o for o in options if o.total_stops == 0]
    stopped = [o for o in options if o.total_stops > 0]
    if directs and stopped:
        cd = min(directs, key=lambda o: o.total_price_pp)
        cs = min(stopped, key=lambda o: o.total_price_pp)
        dp = (cd.total_price_pp - cs.total_price_pp) * party
        dt = cs.total_duration_minutes - cd.total_duration_minutes
        if dp > 0 and dt > 0:
            out["statements"].append(
                f"Direct vs connecting: flying non-stop costs {fmt_money(dp)} more but "
                f"saves {fmt_duration(dt)} ({fmt_money(dp / max(dt / 60, 0.1))}/hr).")
    elif not directs:
        out["statements"].append("No direct option exists among these results — "
                                 "every itinerary involves at least one stop.")
    return out
