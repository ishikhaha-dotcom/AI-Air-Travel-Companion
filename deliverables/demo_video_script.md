# 🎬 WayFinder — Demo Video Script (Definitive Cut)

**Target duration: 4:55 (hard cap 5:00)**
**Presenter: Ishika Sattawan**
**Event: Expedia Group Campus Hackathon 2026 — "Build the Future of Travel" · Innovation Round**

> This script is written to score against the **exact** judging criteria: problem understanding
> & relevance, AI/data/reasoning approach, solution design & architecture, innovation &
> differentiation, prototype/demo evidence, pitch clarity & storytelling, demo-video quality,
> and overall presentation. Every scene below is tagged with the criteria it targets, and the
> narration deliberately says both **what** the product does and **why it was built that way** —
> because the brief asks judges to assess "both the strength of the idea and the quality of its
> execution."

---

## 🎥 Recording Setup (read fully before recording)

**Technical**
- Backend running: `cd backend && python -m uvicorn app.main:app --port 8000`
- Open `http://localhost:8000` — **hard-refresh once** (Ctrl+Shift+R) so you get the latest build
- 1920×1080, browser at 100% zoom, fresh profile, no bookmarks bar, no extensions visible
- OBS (or similar): **mic ON, system audio OFF**; record the browser window only
- **Warm-up pass**: run all 6 benchmarks once before recording — data caches, and you'll know
  exactly what appears on each click (the engine is deterministic, so every take is identical)
- Windows Focus Assist → Alarms Only; quit Slack/Teams/Discord so nothing pops up

**Delivery**
- Speak **10–15% slower** than feels natural. Pause **1 second** after each click before talking.
- Move the cursor slowly and deliberately to whatever you're describing.
- Use this as a guide, not a teleprompter — sound like you're showing a friend something you're proud of.
- Searches take ~1–6 s. **Narrate over the wait** ("…and watch what it does here"). Never sit in silence.

**Don't**: apologize · say "basically / so yeah / um" · read code line-by-line · rush. Dead air beats stumbling.

---

## 🗺️ Scene Map (at a glance)

| # | Scene | Time | Primary criteria |
|---|-------|------|------------------|
| 1 | The Hook | 0:00–0:20 | Problem understanding · Storytelling |
| 2 | What it is & the core insight | 0:20–0:48 | Problem relevance · Innovation |
| 3 | How it's built (the "why") | 0:48–1:25 | AI/data/reasoning · Architecture |
| 4 | B01 — Personalization with receipts | 1:25–2:15 | Innovation · Demo evidence |
| 5 | Conversational refinement | 2:15–2:50 | Innovation · Differentiation |
| 6 | B03 — The family trap | 2:50–3:20 | Data/reasoning depth |
| 7 | B05 — The impossible request | 3:20–3:58 | Problem understanding · Architecture |
| 8 | B02 — Multi-city + the map | 3:58–4:22 | Demo quality · Prototype evidence |
| 9 | Self-grading: 42/42 | 4:22–4:45 | Prototype evidence · Pitch clarity |
| 10 | The Close | 4:45–4:55 | Storytelling · Overall presentation |

---

## 📝 THE SCRIPT

---

### SCENE 1 — The Hook · 0:00–0:20
**Criteria: Problem understanding & relevance · Storytelling**

> **[Screen: App loaded on the "Plan a trip" tab. Header shows the travel-clock chip, "50,000 flights · 1,172 routes", and the "AI: deterministic engine" chip. The 50-traveler sidebar is open on the left.]**

**SAY:**
> "When six different travelers all type the same three words — *find me a flight* — should they all get the same results?
>
> Of course not. But that's exactly what flight search does today. It answers the query and ignores the person.
>
> This is **WayFinder**. It reads the *traveler*, not just the query."

**DO:** Let the UI breathe for a beat. Slowly sweep the cursor across the header chips as you name the problem.

---

### SCENE 2 — What it is & the core insight · 0:20–0:48
**Criteria: Problem relevance · Innovation & differentiation**

**SAY:**
> "Here's the insight the whole project is built on: a traveler tells you how they fly in two places. Half is in their **structured profile** — cabin, budget sensitivity, home airport. But the *other* half is buried in messy, unstructured history — throwaway lines like *'redeyes kill my mornings'* or *'traveling with two kids.'*
>
> Most systems only read the columns. WayFinder reads **both**, fuses them into one traveler model, and — crucially — it can *prove* where every inference came from."

**DO:** Gesture to the left sidebar (the travelers) on "structured profile," and to the planner on the right on "reads both."

---

### SCENE 3 — How it's built, and *why* · 0:48–1:25
**Criteria: AI/data/reasoning approach · Solution design & architecture**

> **[Screen: Stay on the app. Point at the header chips as you reference them — the travel clock, then the "AI: deterministic engine" chip.]**

**SAY:**
> "Quickly, under the hood — because *how* it's built is the point.
>
> It's a **neuro-symbolic** system. The core is a **deterministic reasoning engine** in pure Python: a preference-fusion layer, a route search over fifty thousand real itineraries, and a personalized scoring model. On top, there's an **optional** local LLM that helps parse unusual phrasing and polish explanations.
>
> And that LLM is **guarded** — every number it produces is checked against the deterministic engine, and if anything doesn't match, it's rejected and we fall back instantly. I made that choice deliberately: with the AI completely off, the entire system still passes every test. *The demo can't die on stage, and a judge can reproduce every result.*
>
> One more design decision you'll see everywhere — this dataset is historical, so the app runs on a **simulated travel clock**, set to August 2025. That's how *'next month'* becomes a real, bookable window instead of a broken date."

**DO:** On "deterministic engine," point at the `AI: deterministic engine` chip. On "travel clock," point at the date chip. Keep this moving — it's the *why*, delivered in 35 seconds, not a lecture.

---

### SCENE 4 — B01: Personalization with receipts · 1:25–2:15
**Criteria: Innovation & differentiation · Prototype/demo evidence**

> **[Screen: In the sidebar, the B-badges mark the six judge travelers. Click the **B01** benchmark chip in the planner — it auto-selects traveler U01 and runs his exact prompt.]**

**SAY:**
> "Let's watch it work on the judges' own benchmark prompts. This is U01 — a Cape Town executive. He flies Business, hates connections, and his history literally says *'redeyes kill my mornings.'* His prompt: *'I need to get from home to Tokyo next month.'*"

> **[Results load. Point at the "Understood" intent line and its notes.]**

> "*'Next month'* is vague — but see here, WayFinder resolved it against the travel clock to **September 2025**, and it shows you that reasoning in plain language.
>
> Now the traveler dossier on the left. Instead of dumping raw database fields, it shows clean, human tags — this isn't `seasonal_months colon bracket three four five`, it's readable. Let me open the mined persona."

> **[Click the "🔍 View Mined Travel Persona Insights" accordion in the left dossier to expand it. Hover over a chip such as the direct-flight or no-redeye preference.]**

> "Every preference is grouped — hard constraints, strong, soft — and here's the part that matters: **hover any chip and you see its receipt.** It's quoting his own booking history back to him, with the source. Nothing here is a black box.
>
> And the recommendation itself — the **fit-score ring** scores how well this flight matches *this specific traveler*, zero to a hundred, and the *'why this one'* box lists the evidence-cited reasons. That's the differentiator: personalization you can **audit**."

**DO:** Expand the accordion slowly. Hover 1–2 chips so the tooltips are readable. Point at the fit ring, then the "why this one" box.

---

### SCENE 5 — Conversational refinement · 2:15–2:50
**Criteria: Innovation & differentiation**

> **[Screen: Still on B01 results. The refine bar sits above the cards with suggestion chips.]**

**SAY:**
> "And it's a **conversation**, not a one-shot search. Watch — *'make it cheaper.'*"

> **[Click the "make it cheaper" suggestion chip. Results update.]**

> "The original request stays intact — WayFinder *patches* the intent and re-ranks, and it chips the applied change right here so you always know what it did.
>
> Now something harder — *'under 900 dollars.'*"

> **[Type `under $900` in the refine bar, press Enter.]**

> "When a cap genuinely can't be met, it doesn't dump you to a blank screen. It tells you honestly that nothing qualifies, and shows the closest it found. It never dead-ends, it never silently forgets what you already asked for, and it never invents an answer."

**DO:** Click the chip deliberately; point at the applied-change chip. After the budget cap, point at the honest fallback message.

---

### SCENE 6 — B03: The family trap · 2:50–3:20
**Criteria: AI/data/reasoning depth**

> **[Screen: Click the **B03** chip — auto-selects U03.]**

**SAY:**
> "A subtle one. U03 asks for the *cheapest* flight to Bali over the summer. Sounds trivial. But her history says *'traveling with two kids.'*
>
> So WayFinder books for **three seats**, not one — watch, it filters out anything that can't seat the whole family — and it narrows *'summer'* to the school-holiday window, because that's what actually constrains a parent."

> **[Expand the persona accordion; hover the party-of-3 tag to show its evidence.]**

> "And here's the reasoning judges should notice: *cheapest* and *right* aren't the same for her. The absolute-cheapest double-connection red-eye is wrong for a family. So the **trade-off tiles** put both on the table — cheapest versus best-fit — with the exact dollar-and-hour difference, and let her decide with full information."

**DO:** Hover the party-of-3 evidence tooltip. Point at the Recommended / Cheapest / Fastest trade-off tiles and their deltas.

---

### SCENE 7 — B05: The impossible request · 3:20–3:58
**Criteria: Problem understanding · Architecture (the standout feature)**

> **[Screen: Click the **B05** chip — auto-selects U05.]**

**SAY:**
> "Now the hardest test — and my favorite. U05 wants **First class, direct only, ninety-minute layover cap, money no object**, to Sydney for the holidays.
>
> The trap: there is **no** direct Lisbon-to-Sydney flight anywhere in this dataset. And **no** First-class cabin on that route at all. A normal engine returns zero results and stops.
>
> WayFinder runs what I call the **Relaxation Ladder**."

> **[Point at the orange "Route reality" banner, then walk the cursor down each amber "Adjusted" step.]**

> "First it's honest — *'no direct Lisbon–Sydney exists.'* Then it relaxes the constraints **one documented step at a time** — and every single adjustment is recorded in these amber chips, so you can see precisely what it traded away and why. It lands on the best Business option via Paris, and it even prices the holiday-season premium from the data itself.
>
> That's the philosophy of the whole product: when the world can't give you what you asked for, **explain, don't fake.**"

**DO:** Point at the "Route reality" banner first, then each amber relaxation step slowly, then the seasonal-premium insight.

---

### SCENE 8 — B02: Multi-city + the map · 3:58–4:22
**Criteria: Demo-video quality · Prototype evidence**

> **[Screen: Click the **B02** chip — auto-selects U02. Let the route map animate.]**

**SAY:**
> "Multi-city is where the engine shows off. U02 wants **London, Paris, and Rome in one journey.** WayFinder tries every visit order, chains real dated flights, and where no published fare connects two cities, it **composes its own connection.**
>
> See these **dashed arcs** on the map? Those are self-transfer connections the system built on its own — and the whole map is a real great-circle route render, running fully offline, no tile servers, no API keys.
>
> And this — a **seat-scarcity alert**. Only a couple of seats left on a leg. That's intelligence that actually changes whether you book now."

**DO:** Let the great-circle arcs draw (it's beautiful — don't rush it). Point at a dashed self-transfer arc, then the scarcity alert.

---

### SCENE 9 — Self-grading: 42/42 · 4:22–4:45
**Criteria: Prototype/demo evidence · Pitch clarity**

> **[Screen: Click the "Benchmark self-grading" tab at the top.]**

**SAY:**
> "And here's the part I'm proudest of — you don't have to take my word for any of this.
>
> This tab runs the **judges' own benchmark file** — all six prompts — and checks every expected behavior against the live response, **programmatically.** Not screenshots. Not me clicking around. Watch."

> **[Click "Run all 6". Let the trophy stat strip fill to 42/42.]**

> "**Forty-two out of forty-two expected behaviors — verified.** Milliseconds each. Fully deterministic — one command on your own machine reproduces this exactly."

> **[Expand one check row to reveal the per-behavior detail.]**

**DO:** Let the 42/42 counter land — hold on it. Expand one row to show a real verified behavior + evidence.

---

### SCENE 10 — The Close · 4:45–4:55
**Criteria: Storytelling · Overall presentation**

> **[Screen: Stay on the 42/42 benchmark screen.]**

**SAY:**
> "So that's WayFinder — a preference engine that shows its receipts, a route search that never dead-ends, a conversation that refines without forgetting, and a system that grades itself against the rubric.
>
> Personalization you can actually **audit**. Thank you."

> **[Hold on 42/42 for 2-3 seconds. Cut to an end card: "WayFinder · Ishika Sattawan".]**

---

## ✅ Pre-Recording Checklist

- [ ] `uvicorn app.main:app --port 8000` running; `http://localhost:8000` loads; **hard-refresh once**
- [ ] Ran all 6 benchmarks once (data warm; you know each screen)
- [ ] 1920×1080, 100% zoom, clean browser, notifications silenced, chat apps quit
- [ ] Mic test recorded & played back — clear, no clipping
- [ ] 30-second practice take — check audio level + text legibility at final resolution
- [ ] Sidebar **open** at the start (Scene 1 shows the 50 travelers)
- [ ] "Plan a trip" tab active at the start; you'll switch to "Benchmark" only in Scene 9
- [ ] Export **MP4, ≤ 5:00**, verify audio sync, filename `WayFinder_demo.mp4`

---

## 📊 Criteria Coverage Map (for the judges)

| Judging criterion | Scenes that carry it |
|---|---|
| **Problem understanding & relevance** | 1 (the hook), 2 (the two-halves insight), 7 (the impossible request) |
| **AI / data / reasoning approach** | 3 (neuro-symbolic core + guarded LLM), 4 (evidence-cited inference), 6 (party-size + season reasoning) |
| **Solution design & architecture** | 3 (deterministic core, travel clock, fallback), 7 (relaxation ladder), 8 (self-composed routing) |
| **Innovation & differentiation** | 4 (auditable receipts), 5 (conversational refinement), 7 (relaxation ladder) |
| **Prototype / demo evidence** | 4–8 (live product throughout), 9 (42/42 self-grading harness) |
| **Pitch clarity & storytelling** | 1 (hook), 3 (why, in 35s), 10 (memorable close), one clear idea per scene |
| **Demo-video quality** | Setup section; deliberate pacing; the animated map in Scene 8 |
| **Overall presentation** | Polished dark UI end-to-end; strong open + close; no dead air |

---

## 🎯 Six Lines to Nail (say these exactly)

1. **"It reads the traveler, not just the query."** — Scene 1, your tagline
2. **"With the AI completely off, the entire system still passes every test."** — Scene 3, engineering maturity
3. **"Every preference has a receipt."** — Scene 4, the differentiator
4. **"It never dead-ends, it never silently forgets, and it never invents an answer."** — Scene 5, trust
5. **"When the world can't give you what you asked for — explain, don't fake."** — Scene 7, the philosophy
6. **"Personalization you can actually audit."** — Scene 10, the sign-off

---

## 🎤 Bonus — Finale Live Round prep (if shortlisted)

The video wins the Innovation Round; the Finale is live. If you advance, lead with the **42/42
self-grading harness first** (proof up front for a live audience), then take an **unscripted
prompt from the judges** for any traveler — the deterministic engine makes live improv safe.
Keep Scene 3's "why" (neuro-symbolic, guarded LLM, reproducible) as your one-paragraph answer to
"walk us through your architecture." Have `docs/ARCHITECTURE.md` and `PROGRESS.md` open in a tab
as backup for any deep technical question.
