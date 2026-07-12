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

Config via env vars: `TRAVEL_SIM_TODAY` (default `2025-08-01`), `LLM_MODE` (`off`|`assist`;
**unset = auto-detect**: probes Ollama at startup and enables assist if found),
`LLM_BASE_URL`/`LLM_MODEL`/`LLM_API_KEY` (OpenAI-compatible; e.g., Ollama `http://localhost:11434/v1`).

Production-style serving (what the demo uses): `npm run build` in `frontend/`, then FastAPI
at :8000 serves the built UI — no Vite needed.

## Phase status

| Phase | Scope | Status | Exit criterion |
|-------|-------|--------|----------------|
| P0 | Scaffold, data copy, docs, data layer (airports/models/loader/indices/baselines) | ✅ done | `python -m app.data.loader` QA: 50,000 flights / 35 airports / 1,172 routes / 0 anomalies |
| P1 | Profile fusion, NLU, search (single/round-trip/composition/relaxation), ranking | ✅ done | pytest green (26 tests) |
| P2 | Multi-city, flexdates, insights, narrative, benchmark harness | ✅ done | **`reports/benchmark_report.md`: 42/42 behaviors verified, all six benchmarks PASS, ≤460ms each, LLM off** |
| P3 | FastAPI + React UI | ✅ done | UI built (112KB gz) & served by FastAPI at :8000; /api/* endpoints verified E2E incl. live benchmark runs |
| P4 | Optional LLM adapter | ✅ done | `LLM_MODE=assist` with no LLM server degrades gracefully (verified); number-integrity check on polish; intent gap-fill validated against dataset airports |
| P5 | Deliverables (README, assumptions, deck outline, demo script, solution summary) | ✅ done | README.md, docs/ASSUMPTIONS.md, docs/ARCHITECTURE.md, deliverables/* all written; run.ps1 one-command launcher |
| P6 | Winning-plan upgrade: UI overhaul, AI-story flip, conversational refinement, final deck | ✅ done | pytest 38/38 (both LLM modes) · 42/42 benchmarks · deck.pdf/.pptx exported · full plan + status in `docs/WINNING_PLAN.md` |
| P7 | UI/results polish pass: true great-circle map, compare table, a11y, bug fixes | ✅ done | frontend-only, zero backend risk; pytest 38/38 + benchmarks 42/42 unchanged; `npm run build` clean |
| P8 | Two-pane workspace overhaul + exact brand palette + string humanizer | ✅ done | frontend-only; humanizer verified against live API data for U02/U03/U06; `npm run build` clean |

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
- **2026-07-11 (session 2)** P6 complete — audited the project against the toolkit's judging
  criteria (`docs/WINNING_PLAN.md` has the full gap analysis + status header), then:
  - **UI overhaul** (the old UI read as a debug tool): design system rewrite in
    `frontend/src/index.css` (Inter via @fontsource, elevation layers, sky→indigo accent
    gradient, motion/skeleton keyframes); all emoji icons replaced with **lucide-react**;
    new `src/labels.ts` (display names — fixes the "Preffit" key leak) and
    `src/components/FitRing.tsx` (animated 0–100 fit donut). Rebuilt components: PersonaRail
    (purpose-colored avatars, legend footer), ProfilePanel (chips grouped hard/strong/soft,
    contradiction callout, quote-styled raw history), TripConsole (benchmark chip grid,
    spinner), ResultCard (airline-style per-leg timeline with stop dots + fit ring),
    ResultsView (icon banners, weight bars w/ proper labels), TradeoffStrip (**collapses the
    three summary tiles into one card with "also the cheapest/fastest" badges when one
    option wins every axis**), RouteMap (graticule, brighter land, glow + dash-draw animated
    arcs), BenchmarkTab (42/42 trophy stat strip), PriceCalendar (header polish), App
    (wordmark header, LLM status chip, loading skeleton, refine wiring).
  - **AI story flip**: `config.llm_mode()` now auto-detects Ollama when `LLM_MODE` is unset
    (`llm_live()` cached probe); `/api/meta` exposes `llm_model`/`llm_live`; header chip
    reads "AI: llama3.1 · guarded" or "AI: deterministic engine" — never "LLM: off".
    Narrative section shows "polished by AI · numbers verified" badge when polish ran.
  - **Conversational refinement** (new judged-demo centerpiece): `POST /api/refine`
    {user_id, query, followup} → `app/nlu/refine_rules.py` parses the follow-up
    (rules lexicon: cheaper/faster/comfort, budget caps "under $900", no-redeyes,
    direct-only, cabin, layover caps, date shifts, dayparts; guarded LLM fallback for odd
    phrasings) into a `RefinePatch`; `service.recommend()` gained patch hooks —
    profile-pref overrides (avoid_redeye/cabin/layover/daypart as hard "refinement"-sourced
    prefs), intent tweaks (emphasis, window shift), and post-search filters that **never
    dead-end** (unsatisfiable filter → kept results + honest note in `applied`). Response
    carries `refinement: {followup, applied}`; UI `RefineBar.tsx` shows suggestion chips +
    applied-diff chips. 12 new tests in `backend/tests/test_refine.py`.
  - **Deliverables built**: `deliverables/deck.md` (Marp, dark theme matching app) exported
    to `deck.pdf` + `deck.pptx` (`npx @marp-team/marp-cli deck.md --pdf --allow-local-files`);
    fresh 2x screenshots in `deliverables/assets/`; `demo_video_script.md` rewritten with a
    refinement beat (4:40 timed table); `solution_summary.md` + `README.md` refreshed;
    `deliverables/SUBMISSION_CHECKLIST.md` added.
  - **Final verify**: pytest **38/38** under `LLM_MODE=off` AND `LLM_MODE=assist` with no
    Ollama running (graceful-fallback proof) · harness **42/42** · `npm run build` clean ·
    every UI surface screenshot-verified in a real browser (incl. live refine round-trip:
    B01 + "make it cheaper" → fit 77→81, applied chip rendered).

- **2026-07-12** P7 complete — asked to "improve the UI and the results as much as possible."
  Audited every component against the live app rather than guessing; found and fixed real gaps,
  frontend-only (zero backend/scoring changes, so the 42/42 invariant was never at risk):
  - **RouteMap.tsx**: the map claimed "great-circle arcs" but actually drew straight chords
    between airports (a plain 2-point `LineString` through `geoPath` has no curvature). Now
    samples 48 points per hop via `geoInterpolate` for a true curved great circle, and computes
    the draw-in animation's dash length from the real projected arc length (was a bounding-box
    guess before). Added a per-leg color legend row for multi-city results (B02/B06) — the
    legend mapping color→leg segment was simply missing.
  - **CompareTable.tsx** (new): an at-a-glance ranked table above the result cards — route,
    price (+delta vs #1), duration (+delta), stops, fit-score bar — for all shown
    recommendations. Click a row to smooth-scroll to its full card. Directly answers "how do
    these N picks compare" without reading every card, which the card-only layout couldn't do.
  - **ResultCard.tsx**: cards ranked #2+ now show a compact "vs #1: +$142 · +2h10m · fit −6"
    line under the price (reuses fields already in the response — no backend change), plus a
    `scroll-mt-4` anchor id so CompareTable rows can jump to them, plus a subtle hover shadow.
  - **PriceCalendar.tsx**: fixed a latent SVG bug — the rounded-top-corner bar path used fixed
    4px control points that fold back on themselves when a bar is shorter than ~8px (a
    near-zero-price outlier date), which can render as a visible spike/glitch. Falls back to a
    plain rect below that height.
  - **ResultsView.tsx**: added an explicit empty-state card (icon + explanation) for the
    zero-recommendation case — previously it just silently fell through to the (open-by-default)
    narrative details with no visual acknowledgment that the search came up empty.
  - **Accessibility**: global `:focus-visible` ring (previously only `.input` had one — buttons,
    chips-as-buttons, and table rows had no visible keyboard focus state), `prefers-reduced-motion`
    guard on all `rise-in`/`skeleton`/`route-arc` animations, `role="status" aria-live="polite"`
    on the loading skeleton and the refine bar (screen readers now announce search/refine
    progress), `aria-label` on the refine input.
  - **Verify**: `npm run build` clean (366KB/121KB gz, +6KB over P6 for CompareTable), backend
    untouched so pytest 38/38 and benchmark harness 42/42 reconfirmed unchanged; manually
    checked live API responses for B01 (single-leg + price-by-date), B02 (4-leg multi-city,
    5 distinct fit scores, unique keys), and B05 (1-result edge case — confirmed CompareTable
    and the multi-leg legend correctly no-op below their 2-item thresholds instead of rendering
    broken/empty UI).
- **2026-07-12 (P8)** Given a Streamlit-flavored brief (`st.columns`, `st.expander`, etc.) for
  a "frontend overhaul" — flagged the framework mismatch (this app is React/TS/FastAPI, no
  Streamlit anywhere) and implemented the same UX intent natively instead of writing dead code:
  - **Exact brand palette**: `index.css` tokens repointed to Deep Ebony `#0F1725` (page/surface
    ramp), Brilliant Royal Blue `#4248ED` (`--accent`, headers/CTAs), Exquisite Canary Yellow
    `#FEBF4F` (`--status-warn` + new `--canary`/`.chip-ai` — reserved for status/AI/metric tags
    only; true error/critical red and success green were deliberately NOT repainted canary, to
    keep "AI is on" visually distinct from "something went wrong").
  - **Two-pane workspace**: `App.tsx` restructured into a real `lg:grid-cols-[1fr_2.5fr]` grid.
    Deleted `PersonaRail.tsx` (the old always-visible 256px 50-row list) and replaced it with
    `TravelerSwitcher.tsx` — a compact trigger + searchable dropdown — composed with
    `ProfilePanel` into the left "dossier" column; `TripConsole` + results moved into the right
    "planner" column, which is now roughly 2.5x wider and no longer starved for space.
  - **Collapsible persona insights**: `ProfilePanel.tsx` now shows only the identity line +
    contradiction banner by default; the full hard/strong/soft chip breakdown + raw history is
    behind one `<details>` accordion titled exactly "🔍 View Mined Travel Persona Insights",
    collapsed by default.
  - **Dynamic benchmark chips**: `TripConsole.tsx` takes a `compact` prop; `App.tsx` sets a
    one-way `hasSearched` flag true the instant `run()` fires. Pre-search: full B01–B06 template
    grid. Post-search (permanently, for the session): a tight single-row horizontally-scrollable
    pill rail, freeing vertical space for results.
  - **String humanizer** (`src/humanize.ts`, new): targeted translator (not a generic JSON
    formatter) for the exact shapes the fusion engine emits — `seasonal_months` arrays → season
    labels, `baggage` objects + standalone `checked_bags`/`stroller` → bag/stroller tags,
    `preferred_airlines` arrays + standalone `airline_liked` strings → IATA-code-to-airline-name
    "Loyalist:" tags, boolean flags → a keyed phrase table, with a never-raw-JSON fallback for
    anything unmapped. Verified by executing it (via `node --experimental-strip-types`) against
    real preference payloads pulled live from `/api/users/{U02,U03,U06}/profile` — caught two
    real gaps this way (`checked_bags` as a bare number and `airline_liked` as a bare string,
    not arrays) that hand-tracing had missed, fixed before shipping.
  - Premium result cards (fit-score ring, route timeline, evidence-cited "why this" box) were
    already built in P6/P7 — confirmed still correct against the directive, left untouched;
    they inherit the new brand tokens automatically via CSS variables.
  - **Verify**: `npm run build` clean; backend untouched, pytest 38/38 reconfirmed.

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
| D9 | Refinement = **patch, not re-prompt**: follow-ups re-parse the ORIGINAL query then apply a `RefinePatch` (pref overrides + intent tweaks + post-filters). Refines don't stack — each applies to the base query | Deterministic, testable, and the search core stays untouched; pref overrides flow through existing filters/scoring/why-citations for free (fuse() builds a fresh profile per request, so in-place override is leak-safe) |
| D10 | Refine post-filters (budget cap / direct-only / no-redeye) never return empty: an unsatisfiable filter is skipped with an honest note appended to `refinement.applied` | A refine must never dead-end on stage; honesty-over-silence matches the relaxation-ladder philosophy |
| D11 | `LLM_MODE` unset = auto-detect (cached 0.5s probe of `{LLM_BASE_URL}/models`); explicit `off`/`assist` still wins. UI copy says "AI: deterministic engine", never "LLM: off" | Judging optics at an AI hackathon: assist mode lights up when Ollama is present, zero config; benchmarks/tests stay deterministic when it isn't |
| D12 | UI: bare cabin word "first" is NOT parsed as First cabin in refinements (requires "first class"); backend keys never render raw (display-name map in `src/labels.ts`) | "make the first one cheaper" must not switch cabins; "Preffit" leaked to the weights panel pre-P6 |

## Conventions

- Python: dataclasses + type hints; module-level pure functions; no global mutable state except the
  singleton `Dataset` loaded once in `app/state.py` (lazy).
- All money = USD floats rounded to 2dp at display time; all times ISO-8601; internal datetimes are tz-aware UTC, converted to airport-local only for display/daypart logic.
- Every scoring/filter decision must be traceable: functions return (result, trace_entries) or append to a `Trace` object — the narrative generator consumes ONLY the trace (no re-derivation).
- Tests live in `backend/tests/`, run with `python -m pytest` from `backend/`.
- Frontend talks ONLY to `/api/*` JSON endpoints (Vite dev proxy → :8000).

## Next steps (remaining work is submission logistics + optional polish)

**All build phases P0–P6 are COMPLETE.** Verified state: pytest 38/38 (both LLM modes) ·
benchmark harness 42/42 · UI redesigned, built and served at http://localhost:8000 (start via
`.\run.ps1` or `python -m uvicorn app.main:app --port 8000` from `backend/`). The deck is
already exported (`deliverables/deck.pdf` / `.pptx`); regenerate after any UI change with
fresh screenshots into `deliverables/assets/` then
`npx @marp-team/marp-cli deck.md --pdf --allow-local-files -o deck.pdf` (and `--pptx`).

Remaining for the participant (human tasks — see `deliverables/SUBMISSION_CHECKLIST.md`):
1. Record the demo video following `deliverables/demo_video_script.md` (timed 4:40 click-path;
   includes the refinement beat). App must be running; hard-refresh first.
2. Optional but recommended: `ollama pull llama3.1:8b` + Ollama running, so the header shows
   "AI: llama3.1 · guarded" on camera (auto-detected; no env var needed).
3. Fresh-clone dry run of the README quick start, then assemble the OneDrive folder
   (deck.pdf/pptx, video, solution summary, repo, benchmark report), set "Everyone can view",
   email the link to careers@expediagroup.com.

Optional polish if time remains (in value order):
- Add a small "compare two travelers side-by-side" view (strong demo moment, ~2h).
- Phase 2.3 of `docs/WINNING_PLAN.md` (embedding-based semantic evidence matching) —
  intentionally skipped as optional.
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
- The Ollama probe result is cached for the process lifetime (`config._llm_probe_cache`) —
  starting/stopping Ollama mid-demo won't flip the header chip until uvicorn restarts.
- FastAPI serves `frontend/dist/` — after any frontend change run `npm run build`, or the
  browser keeps getting the old bundle (Vite dev mode on :5173 is only for development).
- Refines are independent (base query + one follow-up), not cumulative — the demo script
  phrases this as "it never forgets what you asked first"; don't demo two stacked refines
  expecting both to apply.
