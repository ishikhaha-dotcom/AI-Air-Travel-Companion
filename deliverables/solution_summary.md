# Solution Summary — WayFinder, an AI Air Travel Companion

**Problem statement.** AI Air Travel Companion (Toolkit Problem Statement 1): build an
AI-powered assistant that suggests and optimizes flight options from user profiles and
*inferred* travel preferences, supporting multi-city travel, direct-vs-connecting trade-offs,
flexible dates, and seasonal pricing/traffic awareness.

**The user & business problem.** Flight search treats everyone identically: the same ranked
list for a solo backpacker and a family of three with a stroller. Travelers' real constraints
live half in structured profile fields and half in how they actually behave — "took a 7hr
layover in SIN to save $120", "kids melt down at night". Generic results mean abandoned
searches, support tickets, and lost bookings; for a platform like Expedia, personalization
that can *explain itself* is conversion and trust.

**The solution.** WayFinder is a hybrid neuro-symbolic travel strategist:

1. **Preference Fusion Engine** — merges structured columns with signals mined from messy
   free-text history into provenance-tagged preferences. Contradictions (a 66-year-old whose
   history says "broke student") are detected, resolved by behavioral-evidence-wins policy,
   and *shown to the user*, not hidden.
2. **Route intelligence** — a deterministic search core over 50,000 itineraries: date-window
   search on a simulated travel clock, self-composed connections when published fares can't
   serve a request, timezone-correct weekday patterns ("Tuesday meeting, back Thursday"),
   multi-city visit-order optimization (permutation × beam search), and open-ended regional
   discovery ("multi-city Asia trip" → best 3-city loops). When constraints can't be met, a
   **relaxation ladder** loosens them step by step and narrates every adjustment.
3. **Personalized explainable ranking** — scoring weights are *derived from the profile* via a
   documented mapping (price sensitivity → price weight; direct preference → stop penalties;
   business purpose → reliability). Every recommendation ships with a 0–100 fit score, its
   per-feature breakdown, and evidence-cited reasons that quote the traveler's own history.
4. **Trade-off & market intelligence** — every answer surfaces Recommended vs Cheapest vs
   Fastest with $/hour framing, empirical seasonal premiums computed from the dataset's own
   medians ("year-end fares run +65% vs shoulder on this route"), seat-scarcity alerts, and
   "shift your dates, save $X" counterfactuals.
5. **Conversational refinement loop** — after any plan, follow-ups like "make it cheaper",
   "no redeyes", "under $900", or "a week later" are parsed into an intent patch and the
   plan re-runs, with every applied change surfaced as a chip. Impossible follow-ups
   ("under $5") degrade honestly to the closest option — a refine never dead-ends.
6. **AI-assisted, deterministically guarded** — a local LLM (Ollama, auto-detected at
   startup) fills NLU gaps, parses unusual follow-up phrasings, and polishes narratives,
   guarded by deterministic fallbacks and a number-integrity check that rejects any
   hallucinated figure. With the LLM entirely off, the full system — including all
   benchmarks — still passes.

**Evidence it works.** A self-grading harness executes all six provided benchmark prompts and
programmatically verifies every `expected_behavior` from `benchmark_prompts.json`:
**42/42 behaviors pass**, fully deterministic, each response < 0.5 s (38 unit/E2E tests
alongside, including the refinement loop). The prototype is a polished React web app —
persona rail with provenance-tagged evidence chips grouped by constraint strength,
airline-style itinerary cards with animated fit-score rings, offline world-map routing with
animated great-circle arcs, price calendar, conversational refine bar, and a live benchmark
self-grading tab — on a FastAPI backend.

**Expected value & impact.** For travelers: recommendations that respect real constraints
(seats for the whole family, layover caps, school holidays) and explain themselves. For the
platform: higher search-to-book conversion via personalization, fewer support escalations via
expectation-setting (holiday premiums, scarcity), and an auditable ranking system —
explainability that survives regulatory and trust scrutiny, because every decision traces to
evidence rather than a black box.
