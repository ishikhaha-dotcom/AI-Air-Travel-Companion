# Presentation Deck Outline (7 slides + demo video slide)

> Target: 6–8 slides per toolkit guidance. Visual style: dark theme matching the app;
> one idea per slide; screenshots from the live UI.

## Slide 1 — Same question, six different right answers
- Hook: "I want to go to Sydney for the holidays." For U05 the right answer is a Business
  cabin via Paris at $10k. For U06 it would be two stops and $900. Flight search that ignores
  who's asking is broken.
- Problem statement recap (one line) + the three data files we were given.

## Slide 2 — The data has traps (we found them)
- 50,000 itineraries, 35 airports, 1,172 routes — but service is *sparse by month* (MEL↔JFK
  never pairs for a Tue–Thu round trip).
- Deliberate contradictions in user histories (age 66 vs "broke student").
- LIS→SYD has ZERO direct flights while U05 demands direct-only + 90-min layovers + a First
  cabin that isn't sold on the route.
- Message: we didn't just read the schema — we let the data shape the architecture.

## Slide 3 — Architecture: deterministic core, optional AI edge
- The mermaid diagram from docs/ARCHITECTURE.md.
- Punchline: LLM_MODE=off passes all benchmarks; the LLM only fills gaps and polishes prose
  (with a number-integrity check). The demo cannot die on stage.

## Slide 4 — Preference Fusion with receipts
- Screenshot: U03's chips — party of 3 inferred from "traveling w/ 2 kids", stroller, school
  holidays; U06's contradiction banner.
- Every preference carries provenance (structured field vs quoted history) and feeds either a
  hard filter, a scoring weight, or a narrative citation.

## Slide 5 — Optimization that tells you what it did
- B05 screenshot: route-reality banner (no direct exists), relaxation ladder narration,
  the $10,161 Business-via-CDG pick with year-end premium quantified.
- The relaxation ladder + weight-derivation table (small).

## Slide 6 — Graded by the judges' own rubric
- Screenshot: Benchmark tab, 42/42 green.
- Table: B01–B06 → candidates, ms, behaviors verified. All deterministic, <0.5 s.

## Slide 7 — Impact & what's next
- Traveler: constraints respected, expectations set, explanations quoted from their own words.
- Platform: conversion lift, support deflection, auditable ranking.
- Roadmap: real NDC/GDS feeds, learning-to-rank from bookings, hotel/car bundling, CO₂-aware
  scoring.

## Slide 8 — Demo video (3–5 min, embedded/linked)
- Per toolkit: the recorded demo of the working model (script in demo_video_script.md).
