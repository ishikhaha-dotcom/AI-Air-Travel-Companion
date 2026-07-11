"""Optional LLM layer — OpenAI-compatible chat endpoint (Ollama by default).

Design contract (blueprint §"LLM-optional by design"): every call site MUST
degrade gracefully — any exception, timeout, or LLM_MODE=off returns None and
the deterministic path is used. The demo can never die because of an LLM.
"""
from __future__ import annotations

import json

import httpx

from .. import config


def llm_available() -> bool:
    return config.llm_mode() == "assist"


def chat(system: str, user: str, json_mode: bool = False) -> str | None:
    """One chat completion; None on ANY failure (caller falls back to rules)."""
    if not llm_available():
        return None
    try:
        body = {
            "model": config.LLM_MODEL,
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": 0.2,
            "stream": False,
        }
        if json_mode:
            body["response_format"] = {"type": "json_object"}
        r = httpx.post(
            f"{config.LLM_BASE_URL.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {config.LLM_API_KEY}"},
            json=body, timeout=config.LLM_TIMEOUT_S,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception:
        return None


def chat_json(system: str, user: str) -> dict | None:
    raw = chat(system, user, json_mode=True)
    if raw is None:
        return None
    try:
        raw = raw.strip()
        if raw.startswith("```"):
            raw = raw.strip("`").removeprefix("json").strip()
        return json.loads(raw)
    except Exception:
        return None
