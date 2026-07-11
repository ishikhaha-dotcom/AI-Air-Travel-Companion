"""Optional LLM assist for intent parsing — fills gaps the rules parser missed
(unusual city phrasings, implicit trip shapes). Rules output always wins where
it found something; the LLM only supplies MISSING fields, and every value is
validated against the dataset's airports before use.
"""
from __future__ import annotations

from ..data.airports import AIRPORTS, REGIONS
from ..data.models import TripIntent
from ..llm.adapter import chat_json

_SYSTEM = (
    "Extract flight-search intent from the user's request. Reply as JSON with "
    'keys: "destinations" (array of IATA codes from this list only: '
    + ", ".join(sorted(AIRPORTS)) +
    '), "region" (one of: ' + ", ".join(REGIONS) + ' or ""), '
    '"emphasis" ("cheapest"|"fastest"|"comfort"|""). Unknown -> empty.'
)


def enrich_intent(query: str, intent: TripIntent) -> TripIntent:
    """Only called when LLM_MODE=assist; never raises; never overrides rules."""
    if intent.destinations or intent.region:
        return intent  # rules already got it
    data = chat_json(_SYSTEM, query)
    if not data:
        return intent
    dests = [d for d in (data.get("destinations") or [])
             if isinstance(d, str) and d in AIRPORTS and d != intent.origin]
    if dests:
        intent.destinations = dests[:4]
        intent.trip_type = "multi_city" if len(dests) > 1 else "one_way"
        intent.notes.append(f"destinations resolved by LLM assist: {dests}")
    region = str(data.get("region") or "").lower()
    if not dests and region in REGIONS:
        intent.region = region
        intent.trip_type = "open_ended"
        intent.notes.append(f"region resolved by LLM assist: {region}")
    if not intent.emphasis and data.get("emphasis") in ("cheapest", "fastest", "comfort"):
        intent.emphasis = data["emphasis"]
    return intent
