# AI Air Travel Companion — End-to-End Engineering Blueprint
**Expedia Hackathon (Innovation Round) · Solo participant · Working title: "WayFinder"**

> This is the approved master blueprint. Any engineer or AI agent should be able to implement
> the system from this document alone. Implementation state is tracked in [`../PROGRESS.md`](../PROGRESS.md).

## Context

The `project_expedia` folder contains the complete hackathon kit for Problem Statement 1 (*AI Air Travel Companion*): a toolkit .docx (rules, judging criteria, deliverables), `flights_data.csv` (50,000 itineraries), `user_data.csv` (50 traveler profiles), and `benchmark_prompts.json` (6 judged scenarios, B01–B06). The task: build an AI-powered air-travel assistant that suggests and optimizes flight options based on user profiles and inferred travel preferences, supporting multi-city travel, direct-vs-connecting trade-offs, flexible dates, and seasonal pricing/traffic patterns.

**Judging (from the toolkit):** problem understanding, AI/data reasoning, solution design/architecture, innovation, prototype/demo evidence, pitch clarity, demo-video quality. Chatbot UI not required; production-readiness not required; assumptions must be documented.

**Winning strategy:** a **hybrid neuro-symbolic system** — deterministic search/optimization/scoring core (always correct, always demo-safe) with an optional LLM layer for language understanding and explanation polish, plus a **self-grading benchmark harness** that proves each expected_behavior from the judges' own file.

## Load-bearing data findings (verified by analysis)

1. **flights_data.csv** — 50,000 rows, 35 airports, 1,172 directed routes (graph nearly complete). Each row is a full priced itinerary (0/1/2 stops pre-composed; `flight_numbers` semicolon-joined). Columns include price (all USD), `seats_available` (1–9 — scarcity is real), `on_time_performance`, `baggage_included`, `refundable`, `demand_level`, `season`, `is_holiday_season`. Departures span **2025-01-01 → 2026-07-01**.
2. **Seasons are per-flight and hemisphere-aware** (e.g., `summer_peak` rows in Dec–Feb for southern routes). Seasonal price signal is real: LHR→JFK economy direct medians — winter $517 / shoulder $602 / year-end $996 (**+65% holiday premium**) → the system can quantify seasonal premiums empirically.
3. **The dataset is entirely in the past relative to the real today** → a simulated "travel clock" is mandatory. **Validated anchor: `SIM_TODAY = 2025-08-01`** (configurable via `TRAVEL_SIM_TODAY` env). Under it every benchmark has a demonstrable window (see playbook below).
4. **Route/month density is sparse and gappy** (e.g., CPT→NRT has zero flights May–Aug 2025; MEL→JFK and JFK→MEL only co-exist in Oct 2025). → The planner **must compose its own connections** from row-pairs when no single row serves a leg/date; date-window search and transparent relaxation are core features, not extras.
5. **user_data.csv** — 50 users: 16 structured columns (`price_sensitivity`, `direct_preference`, `max_layover_minutes`, `preferred_airlines`, `date_flexibility_days`, `multi_city_tendency`, `seasonal_pattern`, …) **plus `raw_history`**: pipe-separated colloquial notes with typos, conditionals ("ok with redeye **if** it's cheaper"), and **deliberate contradictions** (U06: structured age 66 vs raw "broke student"). Extracting/fusing these is an explicit judged dimension.
6. **2-stop rows** carry two `layover_airports` but a **single `layover_minutes` value** → treat as *total* layover time (documented assumption).
7. **benchmark_prompts.json** — 6 scenarios tied to U01–U06; every one is judged on: inference from structured+raw, respecting `direct_preference`/`max_layover_minutes`, cost-vs-convenience weighting by `price_sensitivity`, home-airport/airline filtering, explicit cost-vs-time trade-off, seasonal pricing + **seat scarcity** awareness, and evidence-cited explanations.
8. **Designed traps found** (differentiators if handled): B05 LIS→SYD has **zero direct flights** ever, while U05 demands direct-only + 90-min max layover + First cabin (route has none) → graceful multi-step relaxation with narration. U03 travels with 2 kids → **party size 3** → `seats_available ≥ 3` and total-price math. B03 says "flexible over the summer" but U03's pattern says school holidays only → window narrows to Jul–Aug.

## Product concept

**WayFinder** — a personal air-travel strategist that *reads the traveler, not just the query*. One-line pitch: "Every traveler tells us how they fly — half in their profile, half in how they grumble. WayFinder fuses both into constraints and weights, searches 50k itineraries like a route planner, and explains every recommendation with receipts."

Signature capabilities (each maps to a judged criterion):
- **Preference Fusion Engine** with **provenance + contradiction detection** — every inferred preference carries its evidence (structured field or quoted raw_history snippet) and a confidence; conflicts are resolved by policy and *surfaced in the UI as evidence chips*.
- **Deterministic route intelligence** — date-window search, self-composed connections, multi-city leg-order optimization (permutation search over ≤5 cities + beam search for open-ended trips), hard-constraint filtering, and a **transparent relaxation ladder** when constraints yield zero results.
- **Personalized multi-objective scoring** — per-user weights derived from the profile via a documented mapping; every result shows its score decomposition (price / time / convenience / reliability / preference-fit bars).
- **Trade-off Analyst** — always presents *Recommended vs Cheapest vs Fastest*, with deltas framed in human terms ("direct saves 6h10m for +$142 ≈ $23/hr"), seasonal counterfactuals ("leaving Dec 22 costs +48% vs Dec 3"), and scarcity warnings ("only 2 seats left, peak demand").
- **Benchmark self-grading harness** — runs B01–B06 end-to-end and emits a per-behavior evidence report; also shown live in a UI tab.
- **LLM-optional by design** — with `LLM_MODE=off` the entire system (all 6 benchmarks) works via the rules NLU + template narratives; with an LLM (local Ollama or any OpenAI-compatible endpoint) it handles free-form queries and polishes prose. Demo can never die on stage.

## Architecture

```
React UI (Vite+TS+Tailwind)  ──HTTP──►  FastAPI backend
 ├ Persona picker (50 users)            ├ /api/users, /api/recommend, /api/benchmark
 ├ Trip console (query + quick chips)   │
 ├ Ranked result cards + score bars     ▼
 ├ Trade-off strip / price calendar   Pipeline: NLU → Profile Fusion → Candidate Gen
 ├ SVG route map (offline, no tiles)     → Scoring → Trade-off Analytics → Narrative
 └ Benchmark tab (live B01–B06)        Data layer: in-memory route index,
                                        seasonal price baselines, airport tz/coord table
                                       LLM adapter (optional): intent parse, history
                                        extraction, prose polish — each with rules fallback
```

Request flow for `/api/recommend`: `{user_id, query, overrides?}` → **TripIntent** (origin=home default, destinations, window resolved against SIM_TODAY, trip type, party size) → **TravelerProfile** (fused prefs with provenance) → candidate itineraries (single-leg, round-trip, or multi-city chains; composed connections when needed) → hard filters → relaxation ladder if empty → scoring → top-N + cheapest/fastest anchors → analytics → narrative → JSON with full reasoning trace.

## Component specifications

### 1. Data layer (`backend/app/data/`)
- `loader.py`: read CSVs with dtype coercion (timestamps → aware datetimes, semicolon lists → lists); derive per-row: `dep_local`/`arr_local` (via embedded 35-airport IATA→timezone dict), `is_redeye` (local dep 22:00–05:59), `dep_daypart` (morning/afternoon/evening/night). Run a **data QA report** at startup (row counts, date span, orphan checks).
- `indices.py`: dict indices `route[(o,d)] → [rows sorted by departure]` and `departures[o] → [rows]` for graph expansion; O(1) route lookups keep every query <100 ms without a database.
- `baselines.py`: precompute median price per (origin, destination, cabin, season) and per (route, month) → powers seasonal premium/discount statements and the price calendar.
- `airports.py`: static 35-entry table {IATA: city, country, lat, lon, tz} (hand-embedded; no external API) + city-alias gazetteer + region sets.

### 2. Preference Fusion Engine (`backend/app/profile/`)
Output: `TravelerProfile` = list of `Preference{key, value, strength(hard|strong|soft), source(structured|raw_history|query), evidence_quote, confidence}`.
- `extract_structured.py`: map the 16 columns → preferences (e.g., `max_layover_minutes` → hard cap; `price_sensitivity` → weight profile; `seasonal_pattern` string → window rules like "school holidays (Jul–Aug, Dec)").
- `extract_rules.py`: deterministic raw_history parser — split on `|`, match against a curated signal lexicon (~40 regex patterns) covering: redeye aversion/tolerance (+conditionals "if cheaper"), bag/stroller/kids counts → **party_size & baggage needs**, cabin words, loyalty ("no loyalty"), layover pain thresholds, budget words ("broke student", "money's not the constraint"), timing ("mornings", "kids melt down at night").
- `extract_llm.py` (optional): same output schema via structured-output prompt; merged with rules output, never replacing it.
- `fusion.py`: precedence = query-time statement > raw_history (recent, specific) > structured column; **contradictions kept and flagged** (e.g., U06 age 66 vs "broke student" → budget signal wins for weighting; contradiction noted in the trace). Every downstream decision references preference IDs → full audit trail.

### 3. Query understanding / NLU (`backend/app/nlu/`)
`TripIntent{origin, destinations[], trip_type(one_way|round|multi_city|open_ended), window(start,end), fixed_dow?(e.g. Tue–Thu), party_size, purpose, emphasis(cheapest|fastest|comfort|null)}`.
- `dates.py`: resolve relative phrases against SIM_TODAY — "next month" → calendar month ahead; "over the summer" → Jun–Aug (intersected with user seasonal_pattern → Jul–Aug for U03); "around the holidays" → Dec 15–Jan 5; "a Tuesday… back Thursday" → scan the next 8 Tuesdays, pick feasible+best; honor `date_flexibility_days` as window padding.
- `intent_rules.py`: keyword/gazetteer parser (city→IATA incl. "Tokyo→NRT", "Bali→DPS", "New York→JFK", "London/Paris/Rome→LHR/CDG/FCO"); handles "multi-city Asia trip" → open_ended with region=Asia airport set.
- `intent_llm.py` (optional): JSON-schema extraction for arbitrary phrasing; falls back to rules on failure/timeout. **All 6 benchmarks must parse correctly with rules alone** (unit-tested).

### 4. Candidate generation (`backend/app/search/`)
- `single.py`: for each leg: candidate rows = route index lookup within window; if thin/empty, **compose connections**: rows (o→X)+(X→d) with transfer buffer 90 min–6 h (same airport), price=sum, stops=sum+1, layover=buffer+inner layovers; cap composition depth at 2 rows/leg. Mark `self_transfer=true` and say so in explanations.
- `roundtrip.py`: outbound×return pairing honoring stay bounds (Tue meeting → arrive before Tue 09:00 *local destination time*, return Thu).
- `multicity.py`: fixed city set (B02): try all leg orders (≤4! = 24), chain dated legs with per-city stay 2–4 days (configurable), objective = personalized score summed over legs; prune dominated partial chains (beam width 50). Open-ended (B06): beam search over region airports from home, 2–4 stops, within flexibility window, optimizing total cost + user weights; return top-3 distinct city-sets.
- `flexdates.py`: when window > trip length, evaluate per-feasible-start-date best option → **price-vs-date series** for the calendar view and "shift dates, save $X" insights.
- `relaxation.py`: on zero candidates, relax stepwise and **record each step**: ① widen dates by flexibility → ② layover cap ×1.5 → ③ allow more stops / self-transfer composition → ④ nearest-month scan. Cabin and airline preferences are soft (scored, not filtered), but their absence on a route is detected and narrated (e.g., "no First cabin exists on this route"). Output includes `relaxations_applied[]` — the UI renders them as amber notices.

### 5. Scoring (`backend/app/ranking/`)
Features per candidate, normalized within the candidate set (each a 0–1 "goodness"): `g_price` (total for party), `g_time` (total duration), `g_convenience` (stops penalty scaled by direct preference, layover total, redeye vs preference, daypart match, self-transfer penalty), `g_reliability` (on_time_performance, seat-scarcity risk), `g_preffit` (airline/alliance match, cabin match, baggage_included vs needs, refundable for business).
Weight derivation table (the innovation: *weights are computed from the profile, not hardcoded*):
- `price_sensitivity` none/low/medium/high → `w_price` 0.05/0.15/0.35/0.55
- `direct_preference` none/moderate/strong → stops-penalty scale 0.2/0.6/1.0 and `w_convenience` 0.15/0.25/0.35
- purpose=business → `w_reliability` ×1.5, refundable bonus; kids → redeye penalty ×2
- base `w_time` 0.20, `w_reliability` 0.10, `w_preffit` 0.10; weights re-normalized to Σ=1. Query emphasis ("cheapest") shifts +0.20 to that weight but **never erases inferred needs** (B03's "cheapest" still respects direct-strong + 3 seats — narrated explicitly).
Hard constraints (filters, not weights): seats_available ≥ party_size; layover total ≤ max_layover_minutes; window bounds. Score = Σ wᵢ·gᵢ → 0–100 "fit score" with stored per-feature contributions.

### 6. Trade-off & insight analytics (`backend/app/insights/`)
For every response: Recommended / Cheapest / Fastest triad with explicit deltas (+$ / −h and $-per-hour framing); seasonal context from `baselines.py` ("Dec year-end median on this route is +65% vs shoulder"); scarcity notes (seats ≤3, demand high/peak); date-shift counterfactual from flexdates series.

### 7. Explanation generator (`backend/app/explain/`)
`narrative.py`: deterministic template narrative assembled from the trace — *why this flight* (top firing preferences with evidence quotes), *what was filtered* ("removed 14 options over your 120-min layover cap"), *trade-offs*, *risks*. `llm_polish.py` (optional): rewrites for fluency with a "do not alter numbers/facts" contract; every number in output must exist in the trace (regex check) or the polish is rejected.

### 8. API (`backend/app/api/`) — FastAPI + pydantic schemas
- `GET /api/users` → id, city, one-line persona summary. `GET /api/users/{id}/profile` → fused preferences with provenance (drives evidence chips).
- `POST /api/recommend` `{user_id, query, sim_today?, llm_mode?}` → `{intent, profile_highlights, recommendations[{itinerary(legs, flights), fit_score, score_breakdown, badges, narrative}], anchors{cheapest, fastest}, tradeoffs, insights, relaxations_applied, trace_id}`.
- `GET /api/benchmarks` / `POST /api/benchmarks/{id}/run` → live benchmark execution + behavior checklist results.
- `GET /api/meta` → SIM_TODAY, dataset stats, llm status (UI header badge).

### 9. Frontend (`frontend/` — Vite + React + TS + Tailwind; Recharts for charts)
Screens: **(1) Persona rail** — 50 users, avatar+summary; selecting shows fused preference chips (hover → evidence quote & source). **(2) Trip console** — free-text box + one-click chips for the 6 benchmark prompts; "travel clock" badge showing SIM_TODAY. **(3) Results** — ranked cards (airline, times in local tz, duration, stops w/ layover detail, price for party, seats-left pill, season/demand badges, fit-score with per-feature mini-bars, expandable "Why this?" narrative + evidence). Trade-off strip pinned above (Recommended/Cheapest/Fastest). Price-vs-date mini calendar when dates flexible. **(4) Route map** — offline SVG world map (d3-geo + bundled world-atlas topojson; great-circle arcs per leg; no tile servers). **(5) Benchmark tab** — run B01–B06 live; each expected_behavior renders ✓ with linked evidence.

## Benchmark playbook (demo script backbone; all validated against the data)

| ID | Scenario | What WayFinder showcases (verified feasible under SIM_TODAY=2025-08-01) |
|----|----------|--------------------------------------------------------------------------|
| B01 | U01 (CPT, business, direct-strong, ≤120m, no redeyes) "home → Tokyo next month" | "Next month" → Sep 2025: 5 CPT→NRT itineraries; picks morning direct Business, cites "hate connections"+"redeyes kill my mornings"; aisle/front noted as unbookable-in-dataset courtesy line; shows what the 120-min cap filtered. |
| B02 | U02 (MEX, cheapest-wins, 7h layovers OK) "London+Paris+Rome one journey" | Multi-city permutation search (6 orders × dated chains, composed connections allowed); price-dominant weights; proposes cheapest feasible departure window (Dec 2025 per data gaps — narrated honestly); cites "took a 7hr layover to save $120". |
| B03 | U03 (AMS, 2 kids, direct-strong ≤150m, school breaks) "cheapest to Bali, flexible over summer" | Window narrows to Aug 2025 (school holidays — inferred, not asked); party=3 → seats≥3 filter + total price; "cheapest" emphasis vs direct-strong tension narrated: cheapest-that-fits vs absolute cheapest delta shown; bags/stroller → baggage_included preferred. |
| B04 | U04 (MEL, high price sens., carry-on, JL) "NYC Tuesday meeting, back Thursday" | Tuesday scan with timezone-correct arrive-before-9am logic; MEL↔JFK rows co-exist only in Oct 2025 → planner finds Oct 7–9 pair and/or composed alternative via hub — sparsity handled transparently; business trip → reliability/refundable weighting up. |
| B05 | U05 (LIS, First, direct-strong, ≤90m, money-no-object) "Sydney around the holidays" | The trap: zero LIS→SYD directs; no First on route. Relaxation ladder narrates: no direct exists → best 1-stop Dec 19 Business via CDG, 110-min layover (20 over cap); year-end premium quantified vs shoulder alternative (May 2026 $5,584); scarcity + expectation-setting tone. |
| B06 | U06 (MAA, ultra-budget, 2 stops fine, ≤480m, 30-day flex) "multi-city Asia trip, ~3 weeks" | Open-ended beam search proposes 3 city-set options (e.g., BKK/SIN/HKG loop) within ~21 days minimizing total cost; contradiction chip (age 66 vs "broke student") shown resolved to budget-first; SQ/QR soft preference; total trip budget headline. |

## Repository layout

```
project_expedia/
  data/                      # the 3 provided files (loader reads this path; originals kept at root)
  backend/
    app/{config.py, main.py, service.py}
    app/data/{airports,models,loader,indices,baselines}.py
    app/profile/{extract_structured,extract_rules,extract_llm,fusion}.py
    app/nlu/{dates,intent_rules,intent_llm}.py
    app/search/{single,roundtrip,multicity,flexdates,relaxation}.py
    app/ranking/{features,weights,scorer}.py
    app/insights/{tradeoffs,seasonal}.py
    app/explain/{narrative,llm_polish}.py
    app/llm/adapter.py
    app/api/{routes,schemas}.py
    benchmark/run_benchmarks.py          # CLI → reports/benchmark_report.md
    tests/                               # pytest
    requirements.txt
  frontend/                              # Vite React TS app
  docs/{BLUEPRINT.md, ASSUMPTIONS.md, ARCHITECTURE.md}
  deliverables/{solution_summary.md, deck_outline.md, demo_video_script.md}
  PROGRESS.md                            # agent-handoff worklog
  README.md
```

Stack rationale: Python 3.14 + Node 24 verified on the dev machine. Stdlib-first backend (csv/datetime/zoneinfo/statistics — 50k rows need no pandas/DB; fewer wheels = fewer risks) with FastAPI+pydantic+uvicorn for the API; LLM via an adapter speaking the OpenAI-compatible protocol → works with local **Ollama** (open-source models, toolkit-suggested) or any hosted endpoint; `LLM_MODE=off|assist` env switch.

## Testing & verification

1. **Unit tests (pytest)**: date resolution table-driven cases; rules extractor against all 50 users' raw_history; hard-constraint invariants (no result ever violates seats/layover/window unless a recorded relaxation says so); weight-derivation mapping; multicity chain feasibility (arrivals precede next departures with stay bounds).
2. **Benchmark harness**: `python -m benchmark.run_benchmarks` executes B01–B06, asserts machine-checkable behaviors (home-airport origin, layover cap or recorded relaxation, party-size seats, trade-off deltas present, ≥2 evidence citations incl. ≥1 raw_history quote, seasonal note when window is peak/holiday), and writes `reports/benchmark_report.md` — doubles as submission evidence.
3. **E2E demo check**: `uvicorn` + `npm run dev`, run all 6 chips in the UI, verify map/calendar/score-bars render, then run once with `LLM_MODE=off` to prove the fallback path.

## Assumptions register (mirrored in docs/ASSUMPTIONS.md, a judged deliverable)

1. SIM_TODAY=2025-08-01 travel clock (dataset is historical; all relative dates resolve against it; configurable).
2. Prices are per-person per-itinerary in USD; party cost = price × party_size; no seat-map data (seat-preference wishes acknowledged verbally only).
3. 2-stop `layover_minutes` = total across both stops; the max_layover cap applies to the total (stricter, traveler-friendly).
4. `seats_available` is booking-class inventory (1–9), treated as a hard availability floor and a scarcity signal.
5. Self-composed connections assume same-airport transfer, 90 min–6 h buffer, separate tickets (flagged as self-transfer risk).
6. City→airport mapping fixed (Tokyo=NRT, NYC=JFK, Bali=DPS, London=LHR, Paris=CDG, Rome=FCO) since the dataset has one airport per city.
7. Synthetic-data oddities (e.g., geographically odd routings) are treated as offered products, not errors.

## Deliverables kit (mandatory per toolkit)

- **Solution summary** (1 page): problem → "profiles + messy history → fused constraints/weights → optimized, explained itineraries"; impact framed as conversion-lift/support-deflection for a travel platform.
- **Deck outline (7 slides)**: 1 Problem & why personalization fails today · 2 Data insights (the traps we found) · 3 Architecture (one diagram) · 4 Preference fusion with provenance (U06 contradiction demo) · 5 Optimization & relaxation (B05 story) · 6 Live benchmark self-grading · 7 Impact, assumptions, roadmap.
- **Demo video script (3–5 min, scene-timed)**: 0:00 hook ("ask 6 travelers the same question…") → 0:40 B01 personalization → 1:30 B03 kids/party-size inference → 2:20 B05 relaxation trap → 3:10 B02/B06 multi-city map → 4:00 benchmark tab all-green → 4:30 architecture flash + close.
- **README**: setup, assumptions, limitations (no live fares/booking, synthetic data, single-airport cities), future work (real GDS/NDC feeds, learning-to-rank from bookings, hotel/car bundling, RAG over review corpora).

## Build phases

- **P0 – Foundation**: repo scaffold, data copy to `data/`, loader+indices+baselines+airports, config with SIM_TODAY; smoke script printing dataset QA.
- **P1 – Brain**: profile extraction/fusion (rules), NLU dates+intents, single-leg & round-trip search with composition, relaxation ladder, scoring with weight derivation.
- **P2 – Benchmarks**: multicity (fixed + open-ended beam), flexdates series, insights, narrative generator, benchmark harness green for B01–B06.
- **P3 – Surface**: FastAPI endpoints, React UI (persona rail → console → results → map → benchmark tab).
- **P4 – Optional LLM layer**: adapter + intent/extraction/polish paths with fallbacks; `LLM_MODE` toggle proof.
- **P5 – Deliverables**: README, ASSUMPTIONS, ARCHITECTURE, solution summary, deck outline, demo script.

Priorities if time compresses: P0–P2 are non-negotiable (they win the technical judging); P3 UI can degrade to the benchmark report + a minimal results view; P4 is a bonus flourish; P5 is mandatory for submission.
