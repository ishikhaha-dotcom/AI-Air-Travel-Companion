# Presentation Deck Outline — 7 pages, Expedia light brand

> Source of truth is `deck.md` (Marp) exported to `deck.pdf` / `deck.pptx`. This file is a
> quick-reference summary. Edit `deck.md` first, then resync this outline if the structure changes.

**Brand system:** the Expedia consumer look. Light background with soft yellow and blue glows,
white cards, navy text (`#10152E`), Expedia action blue (`#1668E3`) for accents and section
tags, Expedia yellow (`#FDB92C`) for highlights and the brand mark. Custom HTML/CSS layouts per
slide (Marp `html: true`), not a generic template. No em dashes anywhere in the copy.

**Flow:** problem first, then the solution, then how it works, then the data, then the demo,
then why it wins. The five required deliverable sections are all present and labelled.

## Page 1 — Cover
Expedia brand mark (recreated yellow-tile logo) + "Campus Hackathon 2026". "WayFinder" wordmark,
tagline, the two-halves insight, byline **Ishika Sattawan** (name only), headline stats
(50,000 / 50 / 42-of-42). Right side: the live product framed in a browser window.

## Page 2 — I. Problem Statement
"Six travelers, one query, one lazy answer." Three problem cards (filters cannot read a human /
the real signal is hiding / so travelers bounce) and a one-line gap statement.

## Page 3 — II. Solution Overview
"WayFinder reads the traveler, not just the query." Three pillar cards: Preference Fusion with
receipts, a route engine that never dead-ends, a conversation not a one-shot. Capability pills
underneath.

## Page 4 — III. Architecture & Workflow
Six-step flow (Query+Traveler → NLU → Fusion → Search → Score → Explain) as a 2-row block grid,
plus a "why it is built this way" note covering the deterministic core and the guarded optional
LLM.

## Page 5 — IV. Datasets & Inputs Used
Three data cards: `flights_data.csv` (50,000 itineraries, 35 airports, 1,172 routes),
`user_data.csv` (50 profiles with the messy raw_history field), `benchmark_prompts.json`
(6 judge prompts). Plus the honest simulated-travel-clock note.

## Page 6 — V. Demo Video
"See it think, live (3 to 5 minutes)." Six things the video shows, next to a placeholder QR /
link box. **Action: paste the real OneDrive or YouTube link into `deck.md` before submitting.**

## Page 7 — Why It Wins (close)
2x2 grid: Proof (42/42), Differentiation (auditable), Impact for Expedia (conversion / trust /
deflection), Roadmap. Closes on "Personalization you can actually audit."

## Regenerating after any edit
```powershell
cd deliverables
npx @marp-team/marp-cli deck.md --pdf --allow-local-files --html -o deck.pdf
npx @marp-team/marp-cli deck.md --pptx --allow-local-files --html -o deck.pptx
```
Screenshots referenced by the deck live in `deliverables/assets/`. Refresh them from the live
app (`http://localhost:8000`) if the UI changes before re-exporting.

## Demo video
Recorded separately per `demo_video_script.md` (3 to 5 min, timed click-path) and submitted
alongside the deck per the toolkit's deliverables list.
