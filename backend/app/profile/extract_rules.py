"""Deterministic raw_history parser — the 'messy data' intelligence.

Each pipe-separated snippet is matched against a curated signal lexicon.
Every hit becomes a Preference whose evidence is the VERBATIM snippet, so the
UI/narrative can quote the user back to themselves ("you said: ...").
This is the LLM-off path; extract_llm.py (optional) merges on top, never replaces.
"""
from __future__ import annotations

import re

from ..data.models import Preference, User

# Airline codes that appear colloquially in histories ("prefer JL", "booked SQ")
_AIRLINE_CODES = {"AA", "AF", "AI", "BA", "CX", "DL", "EK", "JL", "KE", "KL",
                  "LH", "NH", "QF", "QR", "SQ", "TG", "TK", "UA"}


def _mk(i: int, key: str, value, strength: str, snippet: str, conf: float, note: str = "") -> Preference:
    return Preference(id=f"r{i:02d}_{key}", key=key, value=value, strength=strength,
                      source="raw_history", evidence=f"“{snippet}”",
                      confidence=conf, note=note)


def extract_rules(user: User) -> list[Preference]:
    prefs: list[Preference] = []
    for i, raw in enumerate(user.raw_history):
        s = raw.lower()

        # --- red-eye attitude (conditional tolerance beats blanket flags) ---
        if re.search(r"ok with redeye if|redeye if it'?s cheaper", s):
            prefs.append(_mk(i, "redeye_ok_if_cheaper", True, "soft", raw, 0.9,
                             "conditional: tolerates redeyes only when they save money"))
        elif re.search(r"redeyes? (kill|ruin)|avoid.*redeye|no redeyes?|hate redeyes?", s) or \
                ("redeye" in s and re.search(r"avoid", s)):
            prefs.append(_mk(i, "avoid_redeye", True, "strong", raw, 0.9))

        # --- direct vs stops ---
        if re.search(r"hate connections?|direct.{0,20}worth paying|direct whenever", s):
            prefs.append(_mk(i, "direct_preference", "strong", "strong", raw, 0.9))
        if re.search(r"don'?t care about stops|dont care about stops|stops? fine|2 stops fine", s):
            prefs.append(_mk(i, "direct_preference", "none", "strong", raw, 0.9))
        if re.search(r"overnight layovers?", s):
            prefs.append(_mk(i, "layover_tolerance_high", True, "soft", raw, 0.8))
        m = re.search(r"(\d+)\s*hr layover.{0,25}save", s)
        if m:
            prefs.append(_mk(i, "layover_tolerance_minutes", int(m.group(1)) * 60, "soft", raw, 0.8,
                             "has traded long layovers for savings before"))
        m = re.search(r"pay to skip a (\d+)\s*hr layover", s)
        if m:
            prefs.append(_mk(i, "layover_pain_minutes", int(m.group(1)) * 60, "soft", raw, 0.8,
                             "will pay to avoid layovers this long"))

        # --- budget attitude ---
        if re.search(r"cheapest (fare|wins|only)|absolute cheapest|whatever'?s cheapest|broke student", s):
            prefs.append(_mk(i, "budget_priority", "high", "strong", raw, 0.9))
        if re.search(r"money'?s not the constraint|comfort over cost|cost( is|'s)? (no|not an?) (issue|object)", s):
            prefs.append(_mk(i, "budget_priority", "none", "strong", raw, 0.9))
        if re.search(r"value matters", s):
            prefs.append(_mk(i, "budget_priority", "balanced", "soft", raw, 0.7))

        # --- cabin ---
        if re.search(r"always book business", s):
            prefs.append(_mk(i, "preferred_cabin", "Business", "strong", raw, 0.95))
        if re.search(r"first or business only", s):
            prefs.append(_mk(i, "preferred_cabin", "First", "strong", raw, 0.95,
                             "Business acceptable as fallback"))

        # --- loyalty / airlines ---
        if re.search(r"no loyalty", s):
            prefs.append(_mk(i, "airline_loyalty", "none", "strong", raw, 0.9))
        m = re.search(r"prefer ([A-Z]{2})\b", raw)
        if m and m.group(1) in _AIRLINE_CODES:
            prefs.append(_mk(i, "airline_liked", m.group(1), "soft", raw, 0.8))

        # --- party & baggage ---
        m = re.search(r"w(?:/|ith) (\d+) kids", s)
        if m:
            prefs.append(_mk(i, "party_size", 1 + int(m.group(1)), "hard", raw, 0.95,
                             f"traveling with {m.group(1)} children"))
        m = re.search(r"(?:need )?(\d+) checked bags?", s)
        if m:
            prefs.append(_mk(i, "checked_bags", int(m.group(1)), "strong", raw, 0.9))
        if "stroller" in s:
            prefs.append(_mk(i, "stroller", True, "strong", raw, 0.9))
        if re.search(r"carry-?on only|no bags beyond a backpack|live out of a backpack", s):
            prefs.append(_mk(i, "carryon_only", True, "strong", raw, 0.9))

        # --- timing ---
        if re.search(r"morning departures?|redeyes? kill my mornings", s):
            prefs.append(_mk(i, "preferred_departure", "morning", "strong", raw, 0.85))
        if re.search(r"kids melt down at night", s):
            prefs.append(_mk(i, "avoid_night_departure", True, "strong", raw, 0.9))

        # --- dates / seasonality ---
        if re.search(r"school (breaks?|holidays?) only", s):
            prefs.append(_mk(i, "dates_school_breaks_only", True, "strong", raw, 0.9))
        if re.search(r"huge date flexibility|whole summer free|flexible", s) and "school" not in s:
            prefs.append(_mk(i, "dates_very_flexible", True, "soft", raw, 0.8))
        if re.search(r"happy in peak season", s):
            prefs.append(_mk(i, "peak_season_ok", True, "soft", raw, 0.8))

        # --- trip shape ---
        if re.search(r"multi-?city (all the time|euro trip|trip planned)|multi-?city all the time", s):
            prefs.append(_mk(i, "multi_city_tendency", "high", "soft", raw, 0.8))

        # --- unbookable courtesy wishes (no seat-map in dataset; acknowledged verbally) ---
        if re.search(r"aisle seat|front of cabin|window seat", s):
            prefs.append(_mk(i, "seat_wish", raw, "soft", raw, 0.7,
                             "seat maps not in dataset — acknowledged, not optimized"))
        if re.search(r"spa lounge|chauffeur|the works", s):
            prefs.append(_mk(i, "premium_services_wish", raw, "soft", raw, 0.7,
                             "ground services not in dataset — acknowledged"))
    return prefs
