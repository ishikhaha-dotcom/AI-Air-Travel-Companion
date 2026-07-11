# ◆ WayFinder — AI Air Travel Companion

**Expedia Hackathon · Problem Statement 1 · Solo submission**

WayFinder is a personal air-travel strategist that *reads the traveler, not just the query*.
It fuses each traveler's structured profile with their messy free-text booking history into
constraints and scoring weights, searches 50,000 itineraries like a route planner (multi-city
chains, self-composed connections, flexible dates), and explains every recommendation with
receipts — quoting the traveler's own history back as evidence.

**Proof up front:** `reports/benchmark_report.md` — all 6 judge benchmarks (B01–B06) pass
**42/42 expected behaviors**, verified programmatically, fully deterministic (no LLM needed),
every response under 0.5 s.

## Quick start

Prereqs: Python 3.12+ (tested on 3.14) and Node 18+ (tested on 24).

```powershell
# 1. backend
cd backend
pip install -r requirements.txt
python -m app.data.loader            # data QA smoke test
python -m pytest tests -q            # 26 tests
python -m benchmark.run_benchmarks   # regenerates reports/benchmark_report.md (42/42)

# 2. frontend (one-time build; FastAPI serves it)
cd ../frontend
npm install
npm run build

# 3. run — open http://localhost:8000
cd ../backend
python -m uvicorn app.main:app --port 8000
```

Dev mode (hot reload): `uvicorn app.main:app --reload --port 8000` + `npm run dev` (Vite on
:5173 proxies `/api`).

## What to try in the UI

1. Click any **benchmark chip** (B01–B06) — it selects the right traveler and runs the judges'
   exact prompt.
2. Hover the **preference chips** — every inferred preference shows its evidence (a profile
   column or a verbatim quote from the traveler's raw history).
3. Try **U06** — WayFinder flags the contradiction between structured age 66 and "broke
   student" in the history, and explains which signal it trusted.
4. Run **B05** (Sydney at the holidays) — there is *no* direct LIS→SYD flight and no First
   cabin on the route; watch the relaxation ladder narrate exactly what it adjusted and why.
5. Open the **Benchmark self-grading tab** — it runs all six benchmarks live and checks every
   `expected_behavior` from `benchmark_prompts.json` against the actual response.

## How it works (60-second tour)

```
query + user_id
   │
   ├─ NLU: travel-clock date resolution ("next month" → Sep 2025), city gazetteer,
   │        trip shape (one-way / round-trip / multi-city / open-ended discovery)
   ├─ Preference Fusion: structured columns + regex-lexicon mining of raw_history
   │        → provenance-tagged preferences, contradiction detection, party size
   ├─ Search: route-index window lookup · self-composed connections (incl. overnight
   │        self-transfers) · round-trip weekday patterns (timezone-correct) ·
   │        multi-city permutation chains · open-ended beam search over a region ·
   │        transparent relaxation ladder when constraints yield zero results
   ├─ Ranking: weights DERIVED from the profile (documented mapping), five feature
   │        goodness scores, 0–100 fit score with full breakdown
   ├─ Insights: Recommended/Cheapest/Fastest trade-off deltas ($/hr framing),
   │        empirical seasonal premiums, seat-scarcity alerts, date-shift savings
   └─ Narrative: deterministic, evidence-cited explanation (LLM optionally polishes
            it — with a number-integrity check that rejects hallucinated figures)
```

Full design: [`docs/BLUEPRINT.md`](docs/BLUEPRINT.md) ·
architecture: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) ·
implementation log for continuation by any engineer/AI: [`PROGRESS.md`](PROGRESS.md).

## The travel clock (important)

The dataset spans **2025-01-01 → 2026-07-01** and is entirely historical, so WayFinder runs on
a simulated clock, `TRAVEL_SIM_TODAY` (default **2025-08-01** — validated so every benchmark
has a demonstrable window). All relative dates ("next month", "the holidays") resolve against
it. The UI shows the clock in the header.

## Optional LLM mode

`LLM_MODE=off` (default): 100% deterministic — all benchmarks pass with zero AI-service
dependencies. `LLM_MODE=assist`: an OpenAI-compatible endpoint (local **Ollama** by default:
`LLM_BASE_URL=http://localhost:11434/v1`, `LLM_MODEL=llama3.1:8b`) fills NLU gaps for unusual
phrasings and polishes narrative prose. Every LLM call falls back to the rules path on any
error, and polished text is rejected if it contains any number not present in the
deterministic narrative.

## Assumptions, limitations, future work

- **Assumptions** are documented in [`docs/ASSUMPTIONS.md`](docs/ASSUMPTIONS.md) (travel clock,
  per-person USD prices, total-layover semantics, self-transfer rules, one airport per city).
- **Limitations:** synthetic dataset (sparse route/month coverage — handled via composition and
  relaxation, but real GDS data would be denser); no live booking; no seat maps (seat wishes
  acknowledged verbally); prices are point-in-time snapshots without fare classes.
- **Future work:** real NDC/GDS feeds; learning-to-rank from booking outcomes; hotel/car
  bundling; RAG over reviews for destination advice; per-user weight learning from
  accept/reject feedback; CO₂-aware scoring.

## Repository map

```
data/                  the 3 provided hackathon files (originals also kept at repo root)
backend/app/           pipeline: data / profile / nlu / search / ranking / insights / explain / llm / api
backend/benchmark/     self-grading harness → reports/benchmark_report.md
backend/tests/         26 pytest tests (NLU, fusion, constraints, all 6 benchmarks E2E)
frontend/              React + TS + Tailwind UI (offline SVG world map, hand-rolled charts)
docs/                  BLUEPRINT.md · ARCHITECTURE.md · ASSUMPTIONS.md
deliverables/          solution summary · deck outline · demo video script
reports/               benchmark_report.md (generated)
PROGRESS.md            implementation worklog / AI-agent handoff document
```
