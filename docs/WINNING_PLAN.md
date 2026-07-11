# WINNING_PLAN.md — WayFinder upgrade plan

> **STATUS (2026-07-11, implementation session): Phases 1, 2.1, 2.2 and most of 3–4 are DONE.**
> UI fully overhauled (design system, lucide icons, Inter, itinerary cards + fit rings,
> animated map, collapsed tri-summary, benchmark trophy strip). LLM auto-detect + guarded
> status chip shipped. `/api/refine` conversational loop shipped with 12 new tests
> (38 total pass; 42/42 benchmarks in both LLM modes). Deck written & exported
> (deliverables/deck.pdf/.pptx), video script rewritten as a timed click-path,
> solution summary + README refreshed, submission checklist added.
> **Remaining (user actions): record the 3–5 min demo video, optional `ollama pull
> llama3.1:8b` for the AI-assisted demo, fresh-clone dry run, OneDrive packaging + email.**
> Phase 2.3 (embeddings) intentionally skipped — optional per plan.

> Written 2026-07-11 after an end-to-end audit against the Hackathon Participant Toolkit
> (judging criteria + mandatory deliverables). This file is the single source of truth for
> the next working session. Work through phases in order; each phase lists concrete tasks
> with file paths.

## Verdict from the audit (context)

**What already wins points** (verified live on 2026-07-11):
- 26/26 pytest, 42/42 benchmark behaviors, all 6 judge prompts < 0.5 s — reproducible.
- Coverage of every challenge dimension: preference inference from messy history (with
  provenance + contradiction detection), multi-city permutation/beam search, direct-vs-
  connecting trade-offs, flexible dates, seasonal/holiday pricing, relaxation ladder.
- Docs complete: README, ASSUMPTIONS, ARCHITECTURE, BLUEPRINT, benchmark report.
- The "strong solutions may demonstrate" list in the toolkit is matched bullet-for-bullet.

**What loses points today:**
1. **AI optics.** Header literally says "LLM: off (deterministic)". Judged on
   "AI/data/reasoning approach" at an AI hackathon, a regex NLU with the LLM switched off
   reads as "not AI". The deterministic core is a *strength* but the story must be
   inverted: AI-first, deterministically guarded.
2. **Mandatory deliverables missing.** Only *outlines* exist (`deliverables/deck_outline.md`,
   `demo_video_script.md`). The actual deck (PDF/PPT) and the recorded 3–5 min demo video
   do not exist. These are hard submission requirements — without them the rest is moot.
3. **UI quality.** Functional but reads as an internal debug tool: flat grey-on-black, emoji
   as icons (💬 🗂 📈 in ProfilePanel/ResultsView), dense 12–14 px text with no hierarchy,
   nearly-invisible world map, redundant triple summary cards when all three picks are the
   same flight, large empty area inside result cards, no loading/skeleton states, no
   transitions, generic system font, "Preffit" label leaking a backend key. Judges score
   "demo video quality" and "overall quality of presentation" — the video is a screen
   recording of this UI, so UI quality gates the video score.
4. **One-shot interaction.** No follow-up refinement ("cheaper", "avoid redeyes", "add
   Rome") — the single most demo-impressive, lowest-cost AI feature we could add, since
   parsed intent is already a structured object we can patch and re-run.

---

## Phase 1 — UI overhaul (highest effort, gates everything downstream)

Goal: from "debug dashboard" to "modern travel product". Keep the committed dark theme but
add depth, hierarchy, and a real icon system. All offline/local (no CDN) — bundle assets.

### 1.1 Design system (`frontend/src/index.css` + new `frontend/src/theme.ts`)
- Typography: bundle **Inter** (or Geist) woff2 locally in `frontend/src/assets/fonts/`;
  scale: 12/13 captions → 14/15 body → 17 section titles → 22–28 prices/scores
  (tabular-nums for all numerics).
- Color: keep near-black page but introduce **elevation layers** (page #0b0c0e →
  surface #14161a → raised #1c1f24 → overlay #24282e), one **accent gradient**
  (sky-400→indigo-500) reserved for primary actions + the Recommended card, and semantic
  greens/ambers only for status. Kill the all-grey monotony.
- Spacing: 8-pt grid; card radius 12; consistent 1px borders at 8% white.
- Install **lucide-react** and replace every emoji icon:
  `ProfilePanel.tsx:10` (💬 🗂 ✳ → MessageSquareQuote / Table2 / Sparkles),
  `ResultsView.tsx:77` (📈 → TrendingUp), plus any chip/section glyphs.

### 1.2 Component redesign (in priority order for demo impact)
1. **ResultCard.tsx — airline-style itinerary card.** Horizontal flight timeline
   (dep time/code ── duration bar with stop dots ── arr time/code), airline + cabin +
   seats-left as sub-row, price large-right with **fit-score ring** (SVG donut, 0–100).
   Fix the empty middle space. Rename `Pref-fit` → "Preference fit" via a display-name
   map (also fixes the "Preffit" weights panel label in ResultsView).
2. **Tri-summary strip (ResultsView).** When Recommended = Cheapest = Fastest, collapse
   to ONE card with three stacked badges ("Best fit · also cheapest · also fastest") —
   currently it shows three identical $1,230 cards side-by-side. When they differ, render
   as a segmented comparison with delta chips ("+$14 · −25 h").
3. **RouteMap.tsx.** Brighter landmass (#2a2e35 on #0b0c0e), animated dash-draw route
   arcs, plane glyph at arc midpoint, airport dots with labels that don't collide,
   dashed styling + legend for self-transfer legs. Consider a subtle graticule.
4. **PersonaRail.tsx.** Initial-avatar circles colored by trip purpose, benchmark badge
   as a proper pill, two-line rows with better truncation, active state with accent left
   bar (exists but strengthen), search box with icon.
5. **ProfilePanel.tsx.** Group chips: Hard constraints / Strong / Soft with section
   micro-headers instead of the legend sentence; evidence popover styled as a quote card
   with source tag; contradiction banner (U06) as an amber callout with both sides shown.
6. **TripConsole.tsx.** Bigger input, accent "Plan it" button with loading spinner state,
   benchmark chips untruncated on wide screens (grid, 2 rows of 3).
7. **Loading & motion.** Skeleton cards while planning; 150–200 ms fade/slide on results
   mount; count-up on fit score. CSS-only is fine (avoid heavy deps).
8. **Header.** Product wordmark with the ◆ mark in accent gradient; travel-clock chip
   with clock icon; **LLM status chip redesigned** (see Phase 2) — never the word "off".
9. **Trade-offs strip (TradeoffStrip.tsx).** Replace odd glyphs with lucide icons; each
   trade-off as icon + one bold number sentence.
10. **BenchmarkTab.tsx.** Green check rows with per-behavior expansion; add a compact
    "42/42 · avg 28 ms" header stat strip. This tab is a killer feature — make it look
    triumphant, not like a test log.

### 1.3 Regenerate all screenshots after redesign (used by deck + README).

## Phase 2 — Flip the AI story (medium effort, biggest judging delta)

Goal: demo runs **AI-visible**, degrades gracefully, and the guardrails become the
differentiator ("the agent that can't hallucinate a price").

### 2.1 LLM assist on by default for the demo
- `backend/app/config.py`: default `LLM_MODE=assist` when an Ollama probe succeeds at
  startup (GET /api/tags with ~300 ms timeout), else fall back to `off`. Keep env override.
- Recommended local model: `llama3.1:8b` (already the default) — document
  `ollama pull llama3.1:8b` in README quick start as an optional step.
- Header chip states: "AI: llama3.1 (guarded)" / "AI: deterministic fallback" — with a
  tooltip explaining the number-integrity check. Never render "LLM: off".
- Surface *where* AI acted per query: the "Understood" panel gets per-note source tags
  ("AI parse" vs "rules"), and the narrative gets a "polished by AI · numbers verified"
  badge when polish succeeded.

### 2.2 Conversational refinement (the demo wow — do not skip)
- New endpoint `POST /api/refine` in `backend/app/api/routes.py`: body = session's prior
  parsed intent + follow-up text. Rules lexicon for the common patterns
  (cheaper/budget cap $X, no redeyes, direct only, add/remove city, shift ±N days,
  cabin up/down, morning/evening) with `app/nlu/intent_llm.py`-style LLM fallback for
  unusual phrasing → returns an **intent patch**; service re-runs search on the patched
  intent.
- UI: after results, a compact follow-up input ("Refine: e.g. 'under $900', 'no
  redeyes'…") + suggestion chips. Show a **diff strip** of what changed
  ("budget cap → $900 · redeyes excluded") and re-rendered results.
- Tests: patch-parser unit tests + one E2E (B01 then "make it cheaper" ⇒ cheapest-first
  reordering) so the feature is provably solid.

### 2.3 Semantic evidence matching (optional — only if time after 2.2)
- Tiny embedding index over raw-history phrases (Ollama `/api/embeddings` or
  sentence-transformers, in-memory cosine — FAISS unnecessary at 50 users but mention
  "FAISS-ready" in the deck since the toolkit suggests it).
- Use to catch paraphrases the regex lexicon misses; tag those chips "semantic match".
  Deterministic lexicon remains the primary path; embeddings add recall only.

### 2.4 Language for the deck (no code): frame search as **time-expanded graph + beam
search + constraint relaxation** — it already is; say so in those words (toolkit suggests
"graph-based or route optimization logic").

## Phase 3 — Mandatory deliverables (blocking submission)

1. **Deck (8 slides).** Build from `deliverables/deck_outline.md` as a **Marp** markdown
   deck (`deliverables/deck.md` → export PDF + PPTX) using post-redesign screenshots.
   Keep the outline's narrative: six-right-answers hook → data traps → architecture →
   fusion receipts → relaxation ladder → 42/42 self-grading → impact/roadmap → video.
2. **Demo video (3–5 min).** Tighten `deliverables/demo_video_script.md` into a timed
   click-path (0:00–0:30 hook with U01 vs U05 same query, 0:30–1:30 B01 + evidence chips,
   1:30–2:30 B05 relaxation ladder, 2:30–3:15 refinement follow-up "make it cheaper",
   3:15–4:00 benchmark tab 42/42, 4:00–4:30 architecture + close). User records via
   QuickTime/OBS at 1512×950; rehearse once against the checklist.
3. **Solution summary**: refresh `deliverables/solution_summary.md` to mention the
   refinement loop + AI-guarded mode (post-Phase-2 truth).
4. **Submission packaging**: OneDrive folder (deck PDF+PPTX, video MP4, summary PDF,
   repo zip or link, benchmark report) — set "Everyone can view", test in incognito,
   email link to careers@expediagroup.com before deadline.

## Phase 4 — Final QA
- `python -m pytest tests -q` (all pass) and `python -m benchmark.run_benchmarks`
  (42/42) **with LLM on and with it off** — the guarantee is the story; prove it.
- Fresh-clone dry run of README quick start on a clean machine/venv.
- Cross-check every toolkit deliverable bullet against the OneDrive folder contents.

## Execution order & rough effort
| Phase | What | Est. effort |
|---|---|---|
| 1 | UI overhaul | 1 solid session (bulk of work) |
| 2.1–2.2 | AI-on default + refinement loop | half session |
| 2.3 | Embeddings (optional) | only if time remains |
| 3 | Deck + video + packaging | half session + user recording time |
| 4 | QA sweep | 1 hour |

## Non-goals (explicitly rejected)
- No framework swap, no redesign of the search/ranking core (it's the strength — don't
  touch working 42/42 logic except additive endpoints).
- No external APIs/datasets (toolkit says optional; adds risk, zero judging upside here).
- No light theme (committed dark theme is fine; polish it instead).
