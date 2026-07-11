"""Preference fusion: structured + raw_history -> one canonical TravelerProfile.

Precedence (blueprint §2): query-time statement > raw_history > structured
column. Conflicts are NOT silently dropped — they're recorded in
profile.contradictions and the losing preference keeps a note, so the UI and
narrative can show "we noticed X but went with Y because Z".
"""
from __future__ import annotations

from ..data.models import Preference, TravelerProfile, User
from .extract_rules import extract_rules
from .extract_structured import extract_structured

_PRECEDENCE = {"query": 3, "raw_history": 2, "derived": 2, "structured": 1}


def fuse(user: User, extra: list[Preference] | None = None) -> TravelerProfile:
    structured = extract_structured(user)
    raw = extract_rules(user)
    all_prefs = structured + raw + (extra or [])

    by_key: dict[str, list[Preference]] = {}
    for p in all_prefs:
        by_key.setdefault(p.key, []).append(p)

    fused: list[Preference] = []
    contradictions: list[str] = []
    for key, group in by_key.items():
        group.sort(key=lambda p: (_PRECEDENCE.get(p.source, 0), p.confidence), reverse=True)
        winner = group[0]
        values = {repr(p.value) for p in group}
        if len(values) > 1:
            losers = [p for p in group[1:] if repr(p.value) != repr(winner.value)]
            if losers:
                lo = losers[0]
                contradictions.append(
                    f"{key}: {lo.source} says {lo.value!r} ({lo.evidence}) but "
                    f"{winner.source} says {winner.value!r} ({winner.evidence}) — using {winner.value!r}")
                winner.note = (winner.note + " | " if winner.note else "") + \
                    f"overrides {lo.source} value {lo.value!r}"
        # agreement across sources = higher confidence (both cited in narrative)
        if len(group) > 1 and len(values) == 1 and winner.confidence < 1.0:
            winner.confidence = min(1.0, winner.confidence + 0.1)
            winner.note = (winner.note + " | " if winner.note else "") + \
                "confirmed by multiple sources"
        fused.append(winner)

    profile = TravelerProfile(user=user, preferences=fused,
                              party_size=int(next((p.value for p in fused if p.key == "party_size"), 1)),
                              contradictions=contradictions)

    # persona-level contradiction (different keys, same story): the U06 trap
    budget = profile.value("budget_priority")
    if budget == "high" and user.age >= 60:
        for p in fused:
            if p.key == "budget_priority":
                profile.contradictions.append(
                    f"persona: age {user.age} (structured) vs {p.evidence} (raw history) — "
                    f"behavioral signal wins for weighting; flagged for review")
                break

    # raw-history budget attitude overrides structured price_sensitivity when they disagree
    if budget == "high" and user.price_sensitivity in ("none", "low"):
        profile.contradictions.append(
            f"price: structured price_sensitivity={user.price_sensitivity} vs raw budget_priority=high "
            f"— treating as high per behavioral evidence")
    return profile


def effective_price_sensitivity(profile: TravelerProfile) -> str:
    """budget_priority from raw history refines structured price_sensitivity."""
    budget = profile.value("budget_priority")
    if budget == "high":
        return "high"
    if budget == "none":
        return "none"
    return profile.value("price_sensitivity", profile.user.price_sensitivity)


def effective_direct_preference(profile: TravelerProfile) -> str:
    return profile.value("direct_preference", profile.user.direct_preference)


def needs_checked_bags(profile: TravelerProfile) -> int:
    bags = profile.value("checked_bags")
    if bags is not None:
        return int(bags)
    bag = profile.value("baggage", {})
    return int(bag.get("checked_bags", 0)) if isinstance(bag, dict) else 0


def profile_highlights(profile: TravelerProfile, limit: int = 8) -> list[dict]:
    """Top preferences for API/UI chips, mixed sources first."""
    ranked = sorted(profile.preferences,
                    key=lambda p: ({"hard": 0, "strong": 1, "soft": 2}[p.strength], -p.confidence))
    out = []
    for p in ranked[:limit]:
        out.append({"key": p.key, "value": p.value, "strength": p.strength,
                    "source": p.source, "evidence": p.evidence, "note": p.note})
    return out
