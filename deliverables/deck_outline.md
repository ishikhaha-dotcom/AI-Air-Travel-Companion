# Presentation Deck Outline — 7 pages, Expedia dark brand system

> Source of truth is `deck.md` (Marp) → exported to `deck.pdf` / `deck.pptx`. This file is a
> quick-reference summary of that deck's structure and intent — edit `deck.md` first, then
> resync this outline if the structure changes.

**Brand system:** Deep Ebony `#0F1725` background · Brilliant Royal Blue `#4248ED` headers/
accents · Exquisite Canary Yellow `#FEBF4F` for status/AI/metric tags. Custom HTML/CSS grid
layouts per slide (Marp `html: true`), not a generic template.

## Page 1 — Title & Product Vision
Asymmetric grid: left column carries the name, hook, byline (Ishika Sattawan · IIT Roorkee),
and headline stats (50,000 itineraries · 50 travelers · 42/42 behaviors); right column is a
framed screenshot of the live in-product route map (`assets/ui-b02-map.png`) with a floating
"● LIVE ROUTE ENGINE" tag — the "premium UI mockup" is the actual product, not a fake mockup.

## Page 2 — The Core Problem Matrix
Two-column split pane: **User Friction** (one-size search can't parse messy history, silent
profile-vs-history contradictions, dead-end hard constraints) vs. **Business Impact** (cart
abandonment, rising support cost, a conversion ceiling generic ranking imposes). Closes on a
single bridge tag naming WayFinder as the fix.

## Page 3 — The Engine Architecture
3-card modular grid, one card per pillar: **Preference Fusion Engine** (provenance-tagged
history mining), **Deterministic Route Core** (permutation × beam search over 50,000
itineraries), **Transparent Relaxation Ladder** (six documented steps, never a silent dead
end). A flow strip underneath shows the pipeline order.

## Page 4 — High-Performance Engineering Stack
2×2 data-flow block grid: React 19 + TypeScript frontend → FastAPI/Pydantic API layer → the
**zero-dependency in-memory route graph** (deliberately no pandas/DB — see PROGRESS.md D1;
sub-500ms on every benchmark) → the optional local-Ollama AI edge, gated by a number-integrity
check that rejects any hallucinated figure.

## Page 5 — Empirical Proof & Validation Matrix
Massive `42/42` hero number (behaviors verified) with a 4-tile stat row underneath: 6/6
benchmarks passed, 38/38 tests green, <500ms median response, 2/2 LLM modes verified. Closing
note covers the live conversational refinement loop as a second, independently-tested proof
point.

## Page 6 — Expected Value & Commercial Impact Matrix
Clean 2×2 metric grid: Cart Conversion Uplift, Support Ticket Deflection, Regulatory &
Customer Trust, Retention Signal — each framed as a concrete business KPI for a platform like
Expedia, grounded in features actually shipped (evidence-cited picks, transparent pricing/
layover explanations, auditable ranking).

## Page 7 — Engineering Boundaries & Future Roadmap
Vertical asymmetric layout: a narrow honest checklist of current limitations (synthetic
dataset, no live booking/fare-class inventory, no seat-map data) beside a wider Now/Next/Later
timeline (shipped deterministic core + refinement loop → live NDC/GDS feeds + Learning-to-Rank
→ cross-product travel-clock bundling + CO₂-aware scoring).

## Regenerating after any edit
```powershell
cd deliverables
npx @marp-team/marp-cli deck.md --pdf --allow-local-files --html -o deck.pdf
npx @marp-team/marp-cli deck.md --pptx --allow-local-files --html -o deck.pptx
```
Screenshots referenced by the deck live in `deliverables/assets/` — refresh them from the live
app (`http://localhost:8000`) if the UI changes before re-exporting.

## Demo video
Not a deck page — recorded separately per `demo_video_script.md` (3–5 min, timed click-path)
and submitted alongside the deck per the toolkit's deliverables list.
