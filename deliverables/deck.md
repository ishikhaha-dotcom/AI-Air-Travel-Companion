---
marp: true
theme: default
paginate: true
html: true
footer: 'WayFinder — AI Air Travel Companion'
size: 16:9
style: |
  :root {
    --ebony: #0F1725;
    --ebony-2: #141D30;
    --ebony-3: #1B2540;
    --royal: #4248ED;
    --royal-soft: rgba(66,72,237,0.14);
    --royal-border: rgba(66,72,237,0.32);
    --canary: #FEBF4F;
    --canary-soft: rgba(254,191,79,0.14);
    --canary-border: rgba(254,191,79,0.38);
    --ink: #F5F7FC;
    --ink-2: #B9C0DE;
    --muted: #7B84AC;
    --border: rgba(255,255,255,0.08);
  }
  section {
    background: var(--ebony);
    color: var(--ink);
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    font-size: 21px;
    padding: 44px 60px 34px;
    line-height: 1.5;
  }
  section::after { color: var(--muted); font-size: 13px; }
  footer { color: var(--muted); font-size: 12px; letter-spacing: 0.04em; }
  h1, h2, h3 { color: var(--ink); letter-spacing: -0.02em; margin: 0 0 6px; }
  h2 { font-size: 28px; color: var(--royal); font-weight: 800; }
  strong { color: var(--ink); font-weight: 700; }
  em { color: var(--ink-2); font-style: italic; }
  code { background: var(--ebony-3); color: var(--canary); padding: 1px 7px; border-radius: 6px; font-size: 0.85em; }
  a { color: var(--royal); }

  /* ---- shared atoms ---- */
  .kicker {
    display: inline-block; font-size: 12.5px; font-weight: 700; letter-spacing: 0.09em;
    color: var(--canary); background: var(--canary-soft); border: 1px solid var(--canary-border);
    border-radius: 999px; padding: 5px 14px; margin-bottom: 16px;
  }
  .tag {
    display: inline-block; font-size: 12px; font-weight: 700; letter-spacing: 0.06em;
    color: var(--canary); background: var(--canary-soft); border: 1px solid var(--canary-border);
    border-radius: 8px; padding: 4px 10px; margin: 2px 4px 2px 0;
  }
  .tag-blue {
    display: inline-block; font-size: 12px; font-weight: 700; letter-spacing: 0.06em;
    color: var(--royal); background: var(--royal-soft); border: 1px solid var(--royal-border);
    border-radius: 8px; padding: 4px 10px; margin: 2px 4px 2px 0;
  }

  /* ---- PAGE 1: hero ---- */
  .hero-grid { display: grid; grid-template-columns: 1.08fr 0.92fr; gap: 40px; align-items: center; margin-top: 4px; }
  .mega { font-size: 64px; font-weight: 800; letter-spacing: -0.03em; line-height: 1; margin: 0 0 12px;
    background: linear-gradient(135deg, #ffffff 30%, #AEB4F5 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
  .hero-lead { font-size: 22px; font-weight: 700; color: var(--royal); margin: 0 0 12px; line-height: 1.35; }
  .hero-sub { font-size: 16.5px; color: var(--ink-2); line-height: 1.6; margin: 0 0 20px; }
  .byline { border-top: 1px solid var(--border); padding-top: 14px; margin-bottom: 18px; }
  .byline-name { font-size: 17px; font-weight: 700; color: var(--ink); }
  .byline-meta { font-size: 13.5px; color: var(--muted); }
  .stat-row { display: flex; gap: 26px; }
  .stat-num { display: block; font-size: 24px; font-weight: 800; color: var(--ink); }
  .stat-num.yellow { color: var(--canary); }
  .stat-label { display: block; font-size: 11.5px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }
  .mockup-frame { position: relative; border-radius: 18px; padding: 10px; background: var(--ebony-2);
    border: 1px solid var(--royal-border); box-shadow: 0 0 0 1px rgba(66,72,237,0.08), 0 30px 70px -20px rgba(66,72,237,0.45); }
  .mockup-frame img { width: 100%; border-radius: 12px; display: block; }
  .mockup-pill { position: absolute; top: 22px; left: 22px; font-size: 11px; font-weight: 700; letter-spacing: 0.05em;
    color: var(--canary); background: rgba(15,23,37,0.85); border: 1px solid var(--canary-border); border-radius: 999px;
    padding: 5px 12px; backdrop-filter: blur(4px); }
  .mockup-caption { font-size: 12.5px; color: var(--muted); text-align: center; margin-top: 10px; }

  /* ---- PAGE 2: split pane ---- */
  .split-pane { display: grid; grid-template-columns: 1fr 1px 1fr; gap: 30px; margin-top: 10px; }
  .pane-divider { background: linear-gradient(var(--ebony), var(--royal-border), var(--ebony)); }
  .pane-kicker { font-size: 12px; font-weight: 800; letter-spacing: 0.1em; margin-bottom: 8px; }
  .pane-left .pane-kicker { color: var(--ink-2); }
  .pane-right .pane-kicker { color: var(--canary); }
  .pane-title { font-size: 17.5px; font-weight: 700; margin-bottom: 16px; line-height: 1.4; }
  .point { border-left: 2px solid var(--border); padding-left: 14px; margin-bottom: 14px; }
  .pane-right .point { border-left-color: var(--royal-border); }
  .point-title { font-size: 15px; font-weight: 700; color: var(--ink); margin-bottom: 2px; }
  .point-body { font-size: 13.5px; color: var(--ink-2); line-height: 1.5; }
  .bridge-tag { margin-top: 20px; text-align: center; font-size: 14px; font-weight: 700; color: var(--canary);
    background: var(--canary-soft); border: 1px solid var(--canary-border); border-radius: 10px; padding: 10px 16px; }

  /* ---- PAGE 3: 3-card pillars ---- */
  .card-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 10px; }
  .pillar-card { background: var(--ebony-2); border: 1px solid var(--border); border-radius: 16px; padding: 20px 18px;
    display: flex; flex-direction: column; gap: 8px; }
  .pillar-num { font-size: 13px; font-weight: 800; color: var(--royal); letter-spacing: 0.05em; }
  .pillar-title { font-size: 16.5px; font-weight: 700; color: var(--ink); line-height: 1.3; min-height: 44px; }
  .pillar-body { font-size: 13px; color: var(--ink-2); line-height: 1.55; flex: 1; }
  .flow-strip { margin-top: 16px; text-align: center; font-size: 13.5px; color: var(--ink-2); font-weight: 600;
    letter-spacing: 0.02em; border-top: 1px solid var(--border); padding-top: 14px; }
  .flow-strip .seg { color: var(--royal); }

  /* ---- PAGE 4: data-flow blocks ---- */
  .flow-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 8px; }
  .flow-block { background: var(--ebony-2); border: 1px solid var(--border); border-radius: 14px; padding: 16px 18px; position: relative; }
  .flow-block.accent { border-color: var(--canary-border); background: linear-gradient(160deg, var(--canary-soft), var(--ebony-2) 55%); }
  .flow-label { font-size: 11.5px; font-weight: 800; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 4px; }
  .flow-title { font-size: 16px; font-weight: 700; color: var(--ink); margin-bottom: 6px; }
  .flow-body { font-size: 12.8px; color: var(--ink-2); line-height: 1.5; }
  .tag-row { margin-top: 16px; text-align: center; }

  /* ---- PAGE 5: proof hero ---- */
  .proof-hero { text-align: center; margin: 6px 0 22px; }
  .proof-num { font-size: 108px; font-weight: 800; line-height: 1; color: var(--canary);
    text-shadow: 0 0 60px rgba(254,191,79,0.35); }
  .proof-den { font-size: 52px; color: var(--ink-2); font-weight: 700; }
  .proof-label { font-size: 17px; font-weight: 700; color: var(--ink); margin-top: 6px; }
  .stat-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }
  .stat-block { background: var(--ebony-2); border: 1px solid var(--border); border-radius: 14px; padding: 16px; text-align: center; }
  .stat-block-num { font-size: 26px; font-weight: 800; color: var(--royal); }
  .stat-block-label { font-size: 11.5px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; margin-top: 4px; }
  .proof-note { font-size: 14.5px; color: var(--ink-2); line-height: 1.6; text-align: center; max-width: 900px; margin: 0 auto; }

  /* ---- PAGE 6: 2x2 impact grid ---- */
  .metric-grid-2x2 { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 16px; margin-top: 10px; height: 480px; }
  .metric-card { background: var(--ebony-2); border: 1px solid var(--border); border-radius: 16px; padding: 20px 22px;
    display: flex; flex-direction: column; justify-content: center; gap: 8px; }
  .metric-title { font-size: 18px; font-weight: 700; color: var(--ink); }
  .metric-body { font-size: 13.5px; color: var(--ink-2); line-height: 1.55; }

  /* ---- PAGE 7: roadmap ---- */
  .roadmap-grid { display: grid; grid-template-columns: 0.85fr 1.3fr; gap: 34px; margin-top: 8px; }
  .col-kicker { font-size: 12px; font-weight: 800; letter-spacing: 0.1em; color: var(--muted); margin-bottom: 14px; }
  .check-item { display: flex; gap: 10px; margin-bottom: 14px; }
  .check-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--muted); margin-top: 6px; flex-shrink: 0; }
  .check-text { font-size: 13.5px; color: var(--ink-2); line-height: 1.5; }
  .check-text b { color: var(--ink); }
  .timeline-col { border-left: 2px solid var(--border); padding-left: 26px; }
  .timeline-row { position: relative; margin-bottom: 22px; }
  .timeline-row:last-child { margin-bottom: 0; }
  .timeline-dot { position: absolute; left: -32px; top: 3px; width: 13px; height: 13px; border-radius: 50%;
    background: var(--ebony); border: 2px solid var(--royal); }
  .timeline-dot.now { background: var(--canary); border-color: var(--canary); }
  .timeline-stage { font-size: 12px; font-weight: 800; letter-spacing: 0.08em; color: var(--royal); margin-bottom: 3px; }
  .timeline-row:first-child .timeline-stage { color: var(--canary); }
  .timeline-text { font-size: 14px; color: var(--ink-2); line-height: 1.55; }
  .timeline-text b { color: var(--ink); }
  .closing-tag { margin-top: 18px; text-align: center; font-size: 14.5px; font-weight: 700; color: var(--royal);
    border-top: 1px solid var(--border); padding-top: 16px; }
---

<!-- PAGE 1 — Title & Product Vision -->

<div class="hero-grid">
<div>

<span class="kicker">AI AIR TRAVEL COMPANION · EXPEDIA HACKATHON</span>

<div class="mega">WayFinder</div>

<div class="hero-lead">The neuro-symbolic travel strategist that reads the traveler — not just the query.</div>

<div class="hero-sub">Every recommendation WayFinder makes is the product of two fused signals: what a traveler <em>declares</em> in their profile, and what they <em>reveal</em> across years of messy, unstructured booking history — resolved into hard constraints, personalized scoring weights, and a route computed live across 50,000 real itineraries, with every decision traced back to its evidence.</div>

<div class="byline">
<div class="byline-name">Ishika Sattawan</div>
<div class="byline-meta">IIT Roorkee · Solo Submission</div>
</div>

<div class="stat-row">
<div><span class="stat-num">50,000</span><span class="stat-label">Itineraries Indexed</span></div>
<div><span class="stat-num">50</span><span class="stat-label">Traveler Profiles</span></div>
<div><span class="stat-num yellow">42/42</span><span class="stat-label">Behaviors Verified</span></div>
</div>

</div>
<div>

<div class="mockup-frame">
<span class="mockup-pill">● LIVE ROUTE ENGINE</span>
<img src="assets/ui-b02-map.png" />
</div>
<div class="mockup-caption">In-product routing surface — true great-circle arcs, animated per journey, computed on request</div>

</div>
</div>

---

<!-- PAGE 2 — The Core Problem Matrix -->

## The Core Problem Matrix

<div class="split-pane">
<div class="pane-left">

<div class="pane-kicker">USER FRICTION</div>
<div class="pane-title">Generic search treats every traveler as the same traveler.</div>

<div class="point">
<div class="point-title">One-size search</div>
<div class="point-body">Static filters can't parse <em>"redeyes kill my mornings"</em> or <em>"broke student, absolute cheapest only"</em> — the exact signals travelers actually leave behind.</div>
</div>

<div class="point">
<div class="point-title">Silent contradictions</div>
<div class="point-body">A profile says age 66, Business preferred; the traveler's own history says <em>"broke student."</em> Today's engines never reconcile it — they just pick one, silently.</div>
</div>

<div class="point">
<div class="point-title">Dead-end constraints</div>
<div class="point-body">Direct-only, 90-minute layover cap, First cabin — on a route where none of the three exist. Most engines return zero results and stop there.</div>
</div>

</div>
<div class="pane-divider"></div>
<div class="pane-right">

<div class="pane-kicker">BUSINESS IMPACT</div>
<div class="pane-title">Every ignored signal is a booking Expedia doesn't make.</div>

<div class="point">
<div class="point-title">Cart abandonment</div>
<div class="point-body">Irrelevant top results erode trust in the first five seconds of a session — before a traveler ever reaches checkout.</div>
</div>

<div class="point">
<div class="point-title">Rising support cost</div>
<div class="point-body">Every unexplained fare spike or layover surprise becomes a support ticket instead of a completed booking.</div>
</div>

<div class="point">
<div class="point-title">Conversion ceiling</div>
<div class="point-body">Generic ranking caps search-to-book conversion no matter how good the underlying inventory actually is.</div>
</div>

</div>
</div>

<div class="bridge-tag">THE GAP → WayFinder closes it with a fused, explainable, deterministic core.</div>

---

<!-- PAGE 3 — Engine Architecture -->

## The Engine Architecture — Three Pillars Under the Hood

<div class="card-grid-3">

<div class="pillar-card">
<div class="pillar-num">01</div>
<div class="pillar-title">Preference Fusion Engine</div>
<div class="pillar-body">Mines free-text booking history with a curated ~40-pattern signal lexicon, safely — every inferred preference carries a confidence score and a verbatim evidence quote. Conflicts between declared fields and behavioral history are surfaced to the traveler, never silently overwritten.</div>
<span class="tag">PROVENANCE-TAGGED</span>
</div>

<div class="pillar-card">
<div class="pillar-num">02</div>
<div class="pillar-title">Deterministic Route Core</div>
<div class="pillar-body">Permutation × beam search routing over 50,000 itineraries: visit-order optimization for fixed multi-city trips, regional beam search for open-ended discovery, and on-the-fly self-composed connections when no published fare can serve a request.</div>
<span class="tag-blue">50,000-ITINERARY GRAPH</span>
</div>

<div class="pillar-card">
<div class="pillar-num">03</div>
<div class="pillar-title">Transparent Relaxation Ladder</div>
<div class="pillar-body">When hard constraints yield zero options, six documented steps loosen them one at a time — widen dates, compose connections, drop rigid patterns, ease layover caps — each one narrated to the traveler. Never a silent dead end.</div>
<span class="tag">ZERO DEAD ENDS</span>
</div>

</div>

<div class="flow-strip"><span class="seg">Preference Fusion</span> → <span class="seg">Deterministic Route Core</span> → <span class="seg">Relaxation Ladder</span> → Ranked, Explained Recommendation</div>

---

<!-- PAGE 4 — High-Performance Engineering Stack -->

## High-Performance Engineering Stack

<div class="flow-grid">

<div class="flow-block">
<div class="flow-label">01 · FRONTEND</div>
<div class="flow-title">React 19 + TypeScript</div>
<div class="flow-body">Vite-built SPA with hand-rolled SVG data visualization — an offline great-circle route map and price-calendar chart with zero external charting runtime, zero tile-server or API-key dependency.</div>
</div>

<div class="flow-block">
<div class="flow-label">02 · API LAYER</div>
<div class="flow-title">FastAPI · Pydantic Contracts</div>
<div class="flow-body">A stateless orchestration layer over the reasoning core — typed request/response schemas shared identically by the UI and the CLI self-grading harness, so there is exactly one code path to trust.</div>
</div>

<div class="flow-block">
<div class="flow-label">03 · REASONING CORE</div>
<div class="flow-title">Zero-Dependency In-Memory Route Graph</div>
<div class="flow-body">50,000 itineraries indexed as O(1) route/origin lookups in pure Python — deliberately no pandas, no database, no cold-start. A conscious engineering call for a dataset this size: fewer dependencies, zero non-determinism, sub-500ms on every benchmark.</div>
</div>

<div class="flow-block accent">
<div class="flow-label">04 · AI EDGE (OPTIONAL)</div>
<div class="flow-title">Local Ollama LLM, Hallucination-Gated</div>
<div class="flow-body">Assists NLU parsing and prose polish only — every output passes a strict Number-Integrity Check that diffs each numeral against the deterministic trace and rejects the response outright if a figure doesn't match.</div>
</div>

</div>

<div class="tag-row">
<span class="tag">SUB-500MS RESPONSE</span>
<span class="tag">ZERO HALLUCINATION TOLERANCE</span>
<span class="tag-blue">LLM: FULLY OPTIONAL</span>
</div>

---

<!-- PAGE 5 — Empirical Proof & Validation Matrix -->

## Empirical Proof & Validation Matrix

<div class="proof-hero">
<div class="proof-num">42<span class="proof-den">/42</span></div>
<div class="proof-label">Judge-defined expected behaviors verified — automatically, deterministically, live in the app.</div>
</div>

<div class="stat-grid-4">
<div class="stat-block"><div class="stat-block-num">6/6</div><div class="stat-block-label">Benchmarks Passed</div></div>
<div class="stat-block"><div class="stat-block-num">38/38</div><div class="stat-block-label">Tests Green</div></div>
<div class="stat-block"><div class="stat-block-num">&lt;500ms</div><div class="stat-block-label">Median Response</div></div>
<div class="stat-block"><div class="stat-block-num">2/2</div><div class="stat-block-label">LLM Modes Verified</div></div>
</div>

<div class="proof-note">Beyond static grading, WayFinder supports a <b style="color:var(--ink)">live conversational refinement loop</b> — "make it cheaper," "no redeyes," "under $900" — patched into the original parsed intent and re-ranked without losing any prior constraint, then independently regression-tested alongside the core benchmark suite.</div>

---

<!-- PAGE 6 — Expected Value & Commercial Impact -->

## Expected Value & Commercial Impact Matrix

<div class="metric-grid-2x2">

<div class="metric-card">
<span class="tag-blue">CONVERSION</span>
<div class="metric-title">Cart Conversion Uplift</div>
<div class="metric-body">Evidence-backed, personalized top picks reduce first-result bounce — travelers see <em>why</em> a fare fits them before they scroll past it.</div>
</div>

<div class="metric-card">
<span class="tag">SUPPORT</span>
<div class="metric-title">Support Ticket Deflection</div>
<div class="metric-body">Transparent layover, pricing, and seasonal-premium explanations pre-empt "why is this so expensive" tickets before they're ever filed.</div>
</div>

<div class="metric-card">
<span class="tag-blue">TRUST</span>
<div class="metric-title">Regulatory & Customer Trust</div>
<div class="metric-body">Every ranking decision traces to a cited, auditable reason — a defensible answer when algorithmic recommendations face compliance or customer-trust review.</div>
</div>

<div class="metric-card">
<span class="tag">RETENTION</span>
<div class="metric-title">Retention Signal</div>
<div class="metric-body">Travelers whose real constraints — family seats, layover pain, budget mode — are visibly respected return to the platform that "gets it."</div>
</div>

</div>

---

<!-- PAGE 7 — Engineering Boundaries & Future Roadmap -->

## Engineering Boundaries & Future Roadmap

<div class="roadmap-grid">
<div>

<div class="col-kicker">CURRENT BOUNDARIES</div>

<div class="check-item"><div class="check-dot"></div><div class="check-text"><b>Synthetic dataset</b> — sparse route/month coverage; one airport per city by design</div></div>
<div class="check-item"><div class="check-dot"></div><div class="check-text"><b>No live booking or fare-class inventory</b> — prices are point-in-time snapshots, not live GDS quotes</div></div>
<div class="check-item"><div class="check-dot"></div><div class="check-text"><b>No seat-map data</b> — seat wishes ("aisle, front of cabin") are acknowledged in the narrative, not optimized against</div></div>

</div>
<div class="timeline-col">

<div class="col-kicker">ROADMAP</div>

<div class="timeline-row">
<div class="timeline-dot now"></div>
<div class="timeline-stage">NOW — SHIPPED</div>
<div class="timeline-text">Deterministic core + optional LLM assist, conversational refinement loop, live self-grading harness — <b>42/42</b> behaviors, reproducible on one command.</div>
</div>

<div class="timeline-row">
<div class="timeline-dot"></div>
<div class="timeline-stage">NEXT</div>
<div class="timeline-text">Live <b>NDC/GDS API</b> connections replacing the synthetic dataset; a <b>Learning-to-Rank</b> model trained on real traveler accept/reject signals, layered on top of today's rule-derived weights.</div>
</div>

<div class="timeline-row">
<div class="timeline-dot"></div>
<div class="timeline-stage">LATER</div>
<div class="timeline-text">Cross-product <b>"travel clock" bundling</b> — hotels, cars, and experiences synchronized to the same trip window — plus CO₂-aware scoring as a first-class ranking factor.</div>
</div>

</div>
</div>

<div class="closing-tag">Built to be extended, not thrown away.</div>
