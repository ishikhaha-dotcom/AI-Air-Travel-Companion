# PROGRESS.md — Implementation Worklog & Agent Handoff Document

> **Purpose:** Any AI agent or engineer must be able to read this file and continue the work
> without re-planning. Read [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md) first (the approved master
> design), then this file for current state. **Update this file after every meaningful step.**

## How to run (current state)

```powershell
# Backend deps (Python 3.14, verified working)
cd backend
pip install -r requirements.txt

# Data QA smoke test (P0 exit criterion)
python -m app.data.loader

# Unit tests
python -m pytest tests/ -q

# Benchmark harness (P2 exit criterion) — writes reports/benchmark_report.md
python -m benchmark.run_benchmarks

# API server
uvicorn app.main:app --reload --port 8000

# Frontend (once P3 lands)
cd ../frontend && npm install && npm run dev   # Vite on :5173, proxies /api → :8000
```

Config via env vars: `TRAVEL_SIM_TODAY` (default `2025-08-01`), `LLM_MODE` (`off`|`assist`, default `off`),
`LLM_BASE_URL`/`LLM_MODEL`/`LLM_API_KEY` (OpenAI-compatible; e.g., Ollama `http://localhost:11434/v1`).

## Phase status

| Phase | Scope | Status | Exit criterion |
|-------|-------|--------|----------------|
| P0 | Scaffold, data copy, docs, data layer (airports/models/loader/indices/baselines) | ✅ done | `python -m app.data.loader` QA: 50,000 flights / 35 airports / 1,172 routes / 0 anomalies |
| P1 | Profile fusion, NLU, search (single/round-trip/composition/relaxation), ranking | ✅ done | pytest green (26 tests) |
| P2 | Multi-city, flexdates, insights, narrative, benchmark harness | ✅ done | **`reports/benchmark_report.md`: 42/42 behaviors verified, all six benchmarks PASS, ≤460ms each, LLM off** |
| P3 | FastAPI + React UI | ✅ done | UI built (112KB gz) & served by FastAPI at :8000; /api/* endpoints verified E2E incl. live benchmark runs |
| P4 | Optional LLM adapter | ✅ done | `LLM_MODE=assist` with no LLM server degrades gracefully (verified); number-integrity check on polish; intent gap-fill validated against dataset airports |
| P5 | Deliverables (README, assumptions, deck outline, demo script, solution summary) | ✅ done | README.md, docs/ASSUMPTIONS.md, docs/ARCHITECTURE.md, deliverables/* all written; run.ps1 one-command launcher |

## Done so far (chronological)

- **2026-07-10** Analyzed all 4 kit files; validated benchmark route coverage, seasonal price signal,
  route/month sparsity; chose `SIM_TODAY=2025-08-01` (validated: every benchmark B01–B06 has a
  demonstrable window under it). Full findings in `docs/BLUEPRINT.md` §"Load-bearing data findings".
- **2026-07-10** Blueprint approved by owner; saved to `docs/BLUEPRINT.md`.
- **2026-07-10** Scaffolded repo tree (see blueprint §"Repository layout"); copied the 3 dataset files
  to `data/` (originals left untouched at repo root); `backend/requirements.txt` installed OK on
  Python 3.14 (fastapi, uvicorn, pydantic, tzdata, httpx, pytest).
- **2026-07-11** P0+P1+P2 complete. Full pipeline works: fusion (provenance + contradictions) →
  NLU (travel-clock dates, intents) → search (window/composition/round-trip/relaxation ladder,
  multi-city permutation chains, open-ended beam) → personalized scoring → trade-offs/seasonal/
  scarcity insights → deterministic narrative. **Benchmark harness: 42/42 expected behaviors
  verified across B01–B06** (`python -m benchmark.run_benchmarks`); pytest 26/26 green.
  Key debugging findings recorded as decisions D5–D8 below.
- **2026-07-11** P3+P4+P5 complete — **project fully built.** FastAPI serves API + built React
  UI at :8000 (persona rail w/ evidence chips, trip console w/ benchmark chips, trade-off
  strip, offline d3-geo world map, hand-rolled SVG price calendar, score-breakdown cards,
  live benchmark self-grading tab). LLM layer added (adapter/intent gap-fill/polish w/
  number-integrity check) — verified graceful fallback with no LLM server. All deliverable
  docs written (README, ASSUMPTIONS, ARCHITECTURE, solution summary, deck outline, timed demo
  script, run.ps1). Final verify: pytest 26/26 · harness 42/42 · live HTTP checks 200.

## Decisions log (deviations/refinements vs blueprint — keep appending)

| # | Decision | Why |
|---|----------|-----|
| D1 | Stdlib-first backend (csv/dataclasses/zoneinfo/statistics), **no pandas** | 50k rows is trivial in-memory; removes Python 3.14 wheel risk; faster startup; deterministic |
| D2 | Added `app/data/models.py` (dataclasses) and `app/service.py` (pipeline orchestrator) beyond blueprint file list | Cleaner separation; service is shared by API routes and benchmark CLI |
| D3 | Cabin + airline preferences are **soft (scored)**, never hard filters; absence on a route is detected and narrated | Prevents empty results; B05 "no First on route" becomes an insight, not a dead end |
| D4 | `tzdata` pip package required | Windows has no system IANA tz database; `zoneinfo` needs it |
| D5 | Self-transfer buffer extended to 26h (overnight stopovers) and **layover cap applies to in-ticket layovers only** (`Leg.in_ticket_layover`), not to separate-ticket stopovers | The dataset is time-sparse: MEL↔JFK published fares NEVER pair into a Tue–Thu round trip; overnight self-transfer (narrated + convenience-penalized) is the only honest way to serve B04 |
| D6 | Multi-city stay windows are adaptive: 2–5 days preferred, auto-extends to 21 days when a leg finds zero service (`_extend` recursion in multicity.py) | Route/month gaps kill rigid chains (B02's CDG→FCO only flies Jan/Feb 2026) |
| D7 | Relaxation ladder order: widen-by-flex → force self-transfer composition (pattern kept) → drop weekday pattern → layover ×1.5/×2 → widen +30d → nearest-service-month | Preserves the user's strongest stated constraint (meeting day) longest |
| D8 | `_why` has evidence fallbacks (closest-cabin, budget-priority, layover-pain, carry-on/self-transfer synergy) | Relaxed picks (B05: no First, no direct) still need ≥2 evidence-cited reasons incl. raw history |

## Conventions

- Python: dataclasses + type hints; module-level pure functions; no global mutable state except the
  singleton `Dataset` loaded once in `app/state.py` (lazy).
- All money = USD floats rounded to 2dp at display time; all times ISO-8601; internal datetimes are tz-aware UTC, converted to airport-local only for display/daypart logic.
- Every scoring/filter decision must be traceable: functions return (result, trace_entries) or append to a `Trace` object — the narrative generator consumes ONLY the trace (no re-derivation).
- Tests live in `backend/tests/`, run with `python -m pytest` from `backend/`.
- Frontend talks ONLY to `/api/*` JSON endpoints (Vite dev proxy → :8000).

## Next steps (remaining work is submission logistics + optional polish)

**All build phases P0–P5 are COMPLETE.** Verified state: pytest 26/26 · benchmark harness
42/42 · UI built and served at http://localhost:8000 (start via `.\run.ps1` or
`python -m uvicorn app.main:app --port 8000` from `backend/`).

Remaining for the participant (human tasks):
1. Record the demo video following `deliverables/demo_video_script.md` (app must be running).
2. Build the slide deck from `deliverables/deck_outline.md` (take screenshots from the live UI).
3. Assemble the OneDrive folder: deck, video, `deliverables/solution_summary.md`, code (this
   repo), `README.md`, `reports/benchmark_report.md`; set permissions to "Everyone can view";
   email the link to careers@expediagroup.com.

Optional polish if time remains (in value order):
- Install Ollama + `llama3.1:8b` and demo `LLM_MODE=assist` (narrative polish) as a bonus beat.
- Add a small "compare two travelers side-by-side" view (strong demo moment, ~2h).
- Extract-LLM path (`app/profile/extract_llm.py`) mirroring extract_rules output schema.

## Known risks / gotchas for the next agent

- The dataset is entirely in the past vs real today → NEVER use `datetime.now()` in logic; always
  `config.sim_today()`.
- 2-stop rows have ONE `layover_minutes` value (total). Composed self-transfer legs add our buffer
  to layover totals.
- Route/month coverage is sparse (see blueprint findings #4) — searches must widen windows or compose
  connections rather than return empty.
- `seats_available` ∈ 1..9 — party-size filtering (U03 = 3 people) is a judged behavior; don't drop it.
- Benchmark B05 (LIS→SYD) MUST end in a narrated relaxation, not an error and not silence.
