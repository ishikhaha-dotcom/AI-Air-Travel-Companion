"""Conversational refinement: parse a follow-up ("make it cheaper", "no
redeyes", "under $900") into a structured patch applied on top of the
previously parsed intent + fused profile, then the pipeline re-runs.

Rules-first (deterministic, covers the demo lexicon); when the rules find
nothing and the LLM layer is live, an LLM fallback extracts the same fields
(guarded — any failure returns the empty patch)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class RefinePatch:
    emphasis: str = ""                    # cheapest | fastest | comfort
    budget_cap_pp: float | None = None    # USD per person
    avoid_redeye: bool = False
    direct_only: bool = False
    cabin: str = ""                       # Economy | Premium Economy | Business | First
    max_layover_minutes: int | None = None
    shift_days: int = 0                   # +later / -earlier
    dep_daypart: str = ""                 # morning | afternoon | evening
    applied: list[str] = field(default_factory=list)

    @property
    def empty(self) -> bool:
        return not self.applied


_CABINS = [
    (r"\bpremium economy\b", "Premium Economy"),
    (r"\bfirst class\b", "First"),
    (r"\bbusiness(?: class)?\b", "Business"),
    (r"\beconomy(?: class)?\b", "Economy"),
]


def parse_refinement(text: str) -> RefinePatch:
    t = " " + text.lower().strip() + " "
    p = RefinePatch()

    m = re.search(r"(?:under|below|less than|max(?:imum)?(?: of)?|no more than|budget(?: of)?)\s*\$?\s*([\d][\d,]*)", t)
    if m:
        p.budget_cap_pp = float(m.group(1).replace(",", ""))
        p.applied.append(f"budget cap ${p.budget_cap_pp:,.0f} per person")

    if re.search(r"cheap(er|est)?|save money|less expensive|cut (the )?cost|lower price", t):
        p.emphasis = "cheapest"
        p.applied.append("optimizing for price")
    elif re.search(r"fast(er|est)?|quick(er|est)?|shorter trip|less time|sooner arrival", t):
        p.emphasis = "fastest"
        p.applied.append("optimizing for total time")
    elif re.search(r"comfort|comfortable|nicer|premium feel", t):
        p.emphasis = "comfort"
        p.applied.append("optimizing for comfort")

    if re.search(r"no red-?eyes?|avoid red-?eyes?|no overnight (flight|departure)s?|no late night", t):
        p.avoid_redeye = True
        p.applied.append("red-eyes excluded")

    if re.search(r"direct only|non-?stop only|only direct|no connect(ions?|ing)|no stops|no layovers?|without stops", t):
        p.direct_only = True
        p.applied.append("direct flights only")

    m = re.search(r"layovers? (?:under|below|max|less than|shorter than)\s*(\d+)\s*h", t)
    if m:
        p.max_layover_minutes = int(m.group(1)) * 60
        p.applied.append(f"layovers capped at {m.group(1)}h")

    for pattern, cabin in _CABINS:
        if re.search(pattern, t):
            # "premium economy" is checked before plain "economy"
            p.cabin = cabin
            p.applied.append(f"cabin → {cabin}")
            break

    m = re.search(r"(?:(\d+)\s*days?|a week|one week)\s*(later|earlier)", t)
    if m:
        days = int(m.group(1)) if m.group(1) else 7
        p.shift_days = days if m.group(2) == "later" else -days
        p.applied.append(f"dates shifted {abs(p.shift_days)} days {m.group(2)}")

    m = re.search(r"(morning|afternoon|evening) (departure|flight)s?", t)
    if m:
        p.dep_daypart = m.group(1)
        p.applied.append(f"prefer {m.group(1)} departures")

    if p.empty:
        _llm_fallback(text, p)
    return p


def _llm_fallback(text: str, p: RefinePatch) -> None:
    """Fill the patch via the guarded LLM layer for phrasings the rules miss."""
    from ..llm.adapter import chat_json, llm_available
    if not llm_available():
        return
    out = chat_json(
        "You translate a traveler's follow-up request into a JSON patch. Keys "
        "(all optional): emphasis ('cheapest'|'fastest'|'comfort'), "
        "budget_cap_pp (number, USD), avoid_redeye (bool), direct_only (bool), "
        "cabin ('Economy'|'Premium Economy'|'Business'|'First'), "
        "max_layover_minutes (number), shift_days (int, + = later), "
        "dep_daypart ('morning'|'afternoon'|'evening'). Output only certain keys.",
        text,
    )
    if not out:
        return
    try:
        if out.get("emphasis") in ("cheapest", "fastest", "comfort"):
            p.emphasis = out["emphasis"]
            p.applied.append(f"optimizing for {out['emphasis']} (AI-parsed)")
        if isinstance(out.get("budget_cap_pp"), (int, float)) and out["budget_cap_pp"] > 0:
            p.budget_cap_pp = float(out["budget_cap_pp"])
            p.applied.append(f"budget cap ${p.budget_cap_pp:,.0f} per person (AI-parsed)")
        if out.get("avoid_redeye") is True:
            p.avoid_redeye = True
            p.applied.append("red-eyes excluded (AI-parsed)")
        if out.get("direct_only") is True:
            p.direct_only = True
            p.applied.append("direct flights only (AI-parsed)")
        if out.get("cabin") in ("Economy", "Premium Economy", "Business", "First"):
            p.cabin = out["cabin"]
            p.applied.append(f"cabin → {out['cabin']} (AI-parsed)")
        if isinstance(out.get("max_layover_minutes"), (int, float)) and out["max_layover_minutes"] > 0:
            p.max_layover_minutes = int(out["max_layover_minutes"])
            p.applied.append(f"layovers capped at {p.max_layover_minutes // 60}h (AI-parsed)")
        if isinstance(out.get("shift_days"), int) and out["shift_days"] != 0:
            p.shift_days = out["shift_days"]
            d = "later" if p.shift_days > 0 else "earlier"
            p.applied.append(f"dates shifted {abs(p.shift_days)} days {d} (AI-parsed)")
        if out.get("dep_daypart") in ("morning", "afternoon", "evening"):
            p.dep_daypart = out["dep_daypart"]
            p.applied.append(f"prefer {out['dep_daypart']} departures (AI-parsed)")
    except Exception:
        pass
