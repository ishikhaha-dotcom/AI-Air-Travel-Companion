"""Flexible-date intelligence: price-vs-date series + 'shift dates, save $X'."""
from __future__ import annotations

from ..data.models import TripOption


def price_by_date(options: list[TripOption]) -> list[dict]:
    """Best (cheapest) option per departure date -> series for the calendar view."""
    by_date: dict[str, dict] = {}
    for o in options:
        d = o.dep_utc.date().isoformat()
        cur = by_date.get(d)
        if cur is None or o.total_price_pp < cur["price"]:
            by_date[d] = {"date": d, "price": round(o.total_price_pp, 2),
                          "fit_score": o.fit_score, "stops": o.total_stops}
    return sorted(by_date.values(), key=lambda x: x["date"])


def date_shift_insight(series: list[dict], recommended: TripOption) -> str | None:
    if len(series) < 2:
        return None
    rec_date = recommended.dep_utc.date().isoformat()
    cheapest = min(series, key=lambda x: x["price"])
    rec_row = next((r for r in series if r["date"] == rec_date), None)
    if rec_row is None or cheapest["date"] == rec_date:
        return None
    saving = rec_row["price"] - cheapest["price"]
    if saving < 25:
        return None
    return (f"Flexible? Departing {cheapest['date']} instead of {rec_date} would save "
            f"${saving:,.0f} per person (cheapest option that date: "
            f"${cheapest['price']:,.0f}, {cheapest['stops']} stop(s)).")
