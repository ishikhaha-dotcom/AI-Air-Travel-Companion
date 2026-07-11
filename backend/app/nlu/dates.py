"""Relative-date resolution against the simulated travel clock (config.sim_today()).

Returns UTC window datetimes plus notes explaining every inference — the notes
feed the narrative ("'over the summer' + your school-holiday pattern -> Aug 4–31").
"""
from __future__ import annotations

import calendar
import re
from datetime import date, datetime, time, timedelta, timezone

from .. import config
from ..data.models import TravelerProfile

_MONTH_NAMES = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}
_DOW = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4,
        "saturday": 5, "sunday": 6}


def _utc(d: date, end: bool = False) -> datetime:
    return datetime.combine(d, time.max if end else time.min, tzinfo=timezone.utc)


def _month_window(year: int, month: int) -> tuple[date, date]:
    last = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last)


def resolve_window(query: str, profile: TravelerProfile) -> dict:
    """-> {start, end (UTC datetimes), fixed_pattern, trip_length_days, notes[]}"""
    q = query.lower()
    today = config.sim_today()
    flex = int(profile.value("date_flexibility_days", 0) or 0)
    notes: list[str] = []
    fixed_pattern: dict = {}
    trip_length_days = 0
    start: date | None = None
    end: date | None = None

    # --- "next month" ---
    if "next month" in q:
        y, m = (today.year, today.month + 1) if today.month < 12 else (today.year + 1, 1)
        start, end = _month_window(y, m)
        notes.append(f"“next month” resolved to {calendar.month_name[m]} {y} "
                     f"(travel clock: {today.isoformat()})")

    # --- "summer" (northern-hemisphere Jun–Aug), intersected with user's fixed months ---
    elif re.search(r"\bsummer\b", q):
        season_months = [6, 7, 8]
        year = today.year if today <= date(today.year, 8, 24) else today.year + 1
        start = max(date(year, 6, 1), today + timedelta(days=3))
        end = date(year, 8, 31)
        notes.append(f"“summer” -> {start.isoformat()}..{end.isoformat()}")
        user_months = profile.value("seasonal_months") or []
        if profile.value("dates_school_breaks_only") and user_months:
            allowed = [m for m in season_months if m in user_months]
            if allowed:
                s2, e2 = _month_window(year, min(allowed))[0], _month_window(year, max(allowed))[1]
                start, end = max(start, s2), min(end, e2)
                notes.append(f"narrowed to school-holiday months {allowed} "
                             f"(seasonal pattern + “school breaks only”) -> "
                             f"{start.isoformat()}..{end.isoformat()}")

    # --- "holidays" = year-end window ---
    elif re.search(r"holiday", q):
        year = today.year if today <= date(today.year, 12, 20) else today.year + 1
        start, end = date(year, 12, 15), date(year + 1, 1, 5)
        notes.append(f"“around the holidays” -> year-end window {start.isoformat()}..{end.isoformat()}")

    # --- explicit month name (preposition-anchored so "may/march" as verbs don't trigger) ---
    else:
        for name, m in _MONTH_NAMES.items():
            if re.search(rf"\b(in|for|during|around)\s+(early\s+|mid\s+|late\s+)?{name}\b", q):
                year = today.year if m >= today.month else today.year + 1
                start, end = _month_window(year, m)
                notes.append(f"“{name}” -> {calendar.month_name[m]} {year}")
                break

    # --- weekday pattern: "a Tuesday meeting, back Thursday" ---
    out_dow = ret_dow = None
    for name, dow in _DOW.items():
        if re.search(rf"\b{name}\b", q):
            if out_dow is None:
                out_dow = dow
            elif dow != out_dow and ret_dow is None:
                ret_dow = dow
    if out_dow is not None and (re.search(r"\bback\b|\breturn\b", q) or ret_dow is not None):
        fixed_pattern = {"out_dow": out_dow, "ret_dow": ret_dow if ret_dow is not None else out_dow + 2}
        if re.search(r"meeting|work|business|office", q):
            fixed_pattern["arrive_by_hour"] = 9
        if start is None:
            start, end = today + timedelta(days=2), today + timedelta(days=84)
            notes.append("weekday pattern trip: scanning the next 12 weeks of "
                         f"{calendar.day_name[fixed_pattern['out_dow']]}s")

    # --- trip length: "about three weeks" ---
    m = re.search(r"(\w+|\d+)\s+weeks?", q)
    if m:
        w = {"one": 1, "two": 2, "three": 3, "four": 4}.get(m.group(1), None)
        w = w or (int(m.group(1)) if m.group(1).isdigit() else None)
        if w:
            trip_length_days = w * 7
            notes.append(f"target trip length ≈ {trip_length_days} days")
            if start is None:
                start = today + timedelta(days=config.DEFAULT_LEAD_DAYS)
                end = today + timedelta(days=max(90, trip_length_days + 45))
                notes.append(f"flexible start window {start.isoformat()}..{end.isoformat()}")

    # --- fallback default window ---
    if start is None:
        start = today + timedelta(days=config.DEFAULT_LEAD_DAYS)
        end = start + timedelta(days=max(flex, config.DEFAULT_WINDOW_DAYS))
        notes.append(f"no dates given -> default window {start.isoformat()}..{end.isoformat()} "
                     f"(lead {config.DEFAULT_LEAD_DAYS}d + your flexibility {flex}d)")
    elif flex and not fixed_pattern:
        end = end + timedelta(days=0)  # flexibility padding applied during relaxation, not here
    if start < today:
        start = today
    return {"start": _utc(start), "end": _utc(end, end=True),
            "fixed_pattern": fixed_pattern, "trip_length_days": trip_length_days, "notes": notes}
