"""Optional narrative polish with a number-integrity contract.

The LLM may rephrase for warmth/fluency but every number in its output must
already exist in the deterministic narrative — otherwise the polish is REJECTED
and the original returned. Hallucinated prices can never reach the user.
"""
from __future__ import annotations

import re

from ..llm.adapter import chat

_SYSTEM = (
    "You are a travel concierge editor. Rewrite the following recommendation "
    "narrative to be warmer and more fluent. STRICT RULES: keep ALL numbers, "
    "prices, times, airport codes and quoted history snippets EXACTLY as given; "
    "do not add any new numbers or facts; keep the markdown structure (###, "
    "bullets, bold); keep it the same length or shorter."
)

_NUM = re.compile(r"\d[\d,.:]*")


def _numbers(text: str) -> set[str]:
    return {m.rstrip(".,:").replace(",", "") for m in _NUM.findall(text)}


def polish(narrative: str) -> tuple[str, bool]:
    """-> (text, was_polished). Falls back to the deterministic narrative."""
    out = chat(_SYSTEM, narrative)
    if not out:
        return narrative, False
    if not _numbers(out) <= _numbers(narrative):
        return narrative, False  # invented a number -> reject
    return out, True
