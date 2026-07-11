"""Central configuration. All tunables live here; env vars override defaults.

CRITICAL: the dataset spans 2025-01-01..2026-07-01 and is entirely in the past
relative to the real clock. Never use datetime.now() in planning logic — always
sim_today(). See docs/BLUEPRINT.md ("travel clock" assumption #1).
"""
from __future__ import annotations

import os
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.environ.get("TRAVEL_DATA_DIR", REPO_ROOT / "data"))
REPORTS_DIR = REPO_ROOT / "reports"

DEFAULT_SIM_TODAY = "2025-08-01"  # validated in blueprint: every benchmark demoable


def sim_today() -> date:
    return date.fromisoformat(os.environ.get("TRAVEL_SIM_TODAY", DEFAULT_SIM_TODAY))


# ---- LLM (optional layer; system is fully functional with LLM_MODE=off) ----
def llm_mode() -> str:
    return os.environ.get("LLM_MODE", "off").lower()  # off | assist


LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1")  # Ollama default
LLM_MODEL = os.environ.get("LLM_MODEL", "llama3.1:8b")
LLM_API_KEY = os.environ.get("LLM_API_KEY", "ollama")
LLM_TIMEOUT_S = float(os.environ.get("LLM_TIMEOUT_S", "20"))

# ---- Search tunables ----
SELF_TRANSFER_MIN_BUFFER_MIN = 90       # composed connections: min transfer time
SELF_TRANSFER_MAX_BUFFER_MIN = 26 * 60  # ... up to an overnight stopover (narrated;
                                        # the user's layover cap applies to in-ticket
                                        # layovers, not separate-ticket stopovers)
COMPOSE_WHEN_FEWER_THAN = 3             # compose connections if direct rows in window < N
DEFAULT_WINDOW_DAYS = 14                # no date phrase -> [today+7, today+7+max(flex, this)]
DEFAULT_LEAD_DAYS = 7

# Multi-city
STAY_MIN_DAYS = 2
STAY_MAX_DAYS = 5
STAY_MAX_ADAPTIVE_DAYS = 21   # fallback stay ceiling when a leg finds no service
MULTICITY_BEAM_WIDTH = 60
OPEN_ENDED_BEAM_WIDTH = 120
OPEN_ENDED_STOPS = 3                    # cities visited on open-ended trips
OPEN_ENDED_STAY_MIN = 3
OPEN_ENDED_STAY_MAX = 6

# Relaxation ladder multipliers (order matters; see search/relaxation.py)
LAYOVER_RELAX_FACTORS = (1.5, 2.0)
DATE_WIDEN_EXTRA_DAYS = 30
NEAREST_MONTH_SCAN_MONTHS = 10

TOP_N_RESULTS = 5
