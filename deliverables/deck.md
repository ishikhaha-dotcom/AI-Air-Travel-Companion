---
marp: true
theme: default
paginate: true
html: true
footer: 'WayFinder · Expedia Group Campus Hackathon 2026'
size: 16:9
style: |
  :root {
    --paper: #ffffff;
    --page: #eef3fb;
    --navy: #10152E;
    --navy-2: #1C2A4A;
    --ink: #26324a;
    --ink-2: #55617a;
    --muted: #8894ab;
    --blue: #1668E3;
    --blue-2: #0f52bf;
    --blue-soft: #e7f0fe;
    --blue-border: rgba(22,104,227,0.28);
    --yellow: #FDB92C;
    --yellow-soft: #fff3d6;
    --yellow-border: rgba(253,185,44,0.55);
    --border: rgba(16,21,46,0.10);
    --shadow: 0 10px 34px -14px rgba(16,21,46,0.28);
  }
  section {
    background:
      radial-gradient(680px 380px at 6% -8%, rgba(253,185,44,0.18), transparent 60%),
      radial-gradient(720px 440px at 100% -4%, rgba(22,104,227,0.12), transparent 55%),
      var(--page);
    color: var(--ink);
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    font-size: 21px;
    padding: 42px 58px 34px;
    line-height: 1.5;
  }
  section::after { color: var(--muted); font-size: 13px; font-weight: 600; }
  footer { color: var(--muted); font-size: 12px; letter-spacing: 0.03em; }
  h1, h2, h3 { color: var(--navy); letter-spacing: -0.02em; margin: 0 0 6px; }
  h2 { font-size: 30px; font-weight: 800; }
  strong { color: var(--navy); font-weight: 700; }
  em { color: var(--ink-2); font-style: italic; }
  a { color: var(--blue); }

  /* ---- brand mark + section tags ---- */
  .brand { display: inline-flex; align-items: center; gap: 10px; margin-bottom: 18px; }
  .brand-word { font-size: 18px; font-weight: 800; color: var(--navy); letter-spacing: -0.02em; }
  .brand-sub { font-size: 12.5px; font-weight: 600; color: var(--ink-2); border-left: 1px solid var(--border); padding-left: 10px; margin-left: 2px; }
  .tag-num {
    display: inline-flex; align-items: center; gap: 8px; margin-bottom: 14px;
    font-size: 12.5px; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase;
    color: var(--blue); background: var(--blue-soft); border: 1px solid var(--blue-border);
    border-radius: 999px; padding: 6px 14px;
  }
  .tag-num .n {
    display: inline-flex; align-items: center; justify-content: center;
    width: 20px; height: 20px; border-radius: 6px; background: var(--yellow); color: var(--navy);
    font-size: 12px; font-weight: 800;
  }
  .pill {
    display: inline-block; font-size: 12px; font-weight: 700; letter-spacing: 0.04em;
    color: var(--navy); background: var(--yellow-soft); border: 1px solid var(--yellow-border);
    border-radius: 8px; padding: 4px 10px; margin: 2px 4px 2px 0;
  }
  .pill-blue {
    display: inline-block; font-size: 12px; font-weight: 700; letter-spacing: 0.04em;
    color: var(--blue); background: var(--blue-soft); border: 1px solid var(--blue-border);
    border-radius: 8px; padding: 4px 10px; margin: 2px 4px 2px 0;
  }
  .card {
    background: var(--paper); border: 1px solid var(--border);
    border-radius: 16px; box-shadow: var(--shadow); padding: 20px 22px;
  }

  /* ---- PAGE 1 cover ---- */
  .cover-grid { display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 42px; align-items: center; margin-top: 2px; }
  .display { font-size: 66px; font-weight: 800; letter-spacing: -0.03em; line-height: 1; color: var(--navy); margin: 0 0 14px; }
  .display .fin { color: var(--blue); }
  .lead { font-size: 22px; font-weight: 700; color: var(--navy-2); line-height: 1.35; margin: 0 0 12px; }
  .sub { font-size: 16px; color: var(--ink-2); line-height: 1.6; margin: 0 0 20px; }
  .byline { border-top: 1px solid var(--border); padding-top: 14px; margin-bottom: 18px; }
  .byline b { font-size: 17px; color: var(--navy); }
  .byline span { display: block; font-size: 13px; color: var(--muted); margin-top: 2px; }
  .stat-row { display: flex; gap: 26px; }
  .stat b { display: block; font-size: 25px; font-weight: 800; color: var(--navy); }
  .stat.blue b { color: var(--blue); }
  .stat span { display: block; font-size: 11.5px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }
  .browser { border-radius: 14px; overflow: hidden; border: 1px solid var(--border); box-shadow: 0 24px 60px -20px rgba(16,21,46,0.4); background: #0f1725; }
  .browser-bar { display: flex; align-items: center; gap: 6px; padding: 9px 12px; background: #e9edf5; }
  .browser-bar i { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
  .browser-url { flex: 1; margin-left: 8px; font-size: 11px; color: #6b7488; background: #fff; border-radius: 6px; padding: 3px 10px; text-align: center; font-style: normal; }
  .browser img { width: 100%; display: block; }
  .cap { font-size: 12px; color: var(--muted); text-align: center; margin-top: 10px; }

  /* ---- PAGE 2 problem ---- */
  .prob-hero { font-size: 20px; color: var(--navy-2); font-weight: 600; line-height: 1.5; max-width: 900px; margin: 2px 0 18px; }
  .prob-hero b { color: var(--navy); }
  .prob-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
  .prob-card { background: var(--paper); border: 1px solid var(--border); border-left: 4px solid var(--yellow); border-radius: 14px; box-shadow: var(--shadow); padding: 18px; }
  .prob-card.blue { border-left-color: var(--blue); }
  .prob-card h4 { font-size: 15.5px; font-weight: 700; color: var(--navy); margin: 0 0 6px; }
  .prob-card p { font-size: 13.5px; color: var(--ink-2); line-height: 1.55; margin: 0; }
  .kicker-line { margin-top: 18px; font-size: 15px; font-weight: 700; color: var(--navy); text-align: center; background: var(--yellow-soft); border: 1px solid var(--yellow-border); border-radius: 12px; padding: 12px 16px; }

  /* ---- PAGE 3 solution ---- */
  .pillar-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 6px 0 14px; }
  .pillar { background: var(--paper); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 18px; display: flex; flex-direction: column; gap: 8px; }
  .pillar .num { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 9px; background: var(--blue); color: #fff; font-weight: 800; font-size: 15px; }
  .pillar h4 { font-size: 16px; font-weight: 700; color: var(--navy); margin: 0; min-height: 40px; }
  .pillar p { font-size: 13px; color: var(--ink-2); line-height: 1.55; margin: 0; flex: 1; }
  .sol-foot { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }

  /* ---- PAGE 4 architecture ---- */
  .flow { display: flex; flex-direction: column; gap: 9px; margin-top: 6px; }
  .flow-row { display: flex; align-items: stretch; gap: 10px; }
  .flow-step { flex: 1; background: var(--paper); border: 1px solid var(--border); border-radius: 12px; box-shadow: var(--shadow); padding: 12px 15px; }
  .flow-step .s { font-size: 11px; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase; color: var(--blue); }
  .flow-step .t { font-size: 14.5px; font-weight: 700; color: var(--navy); margin: 2px 0; }
  .flow-step .d { font-size: 12px; color: var(--ink-2); line-height: 1.45; }
  .flow-step.accent { border-color: var(--yellow-border); background: var(--yellow-soft); }
  .flow-step.accent .s { color: #b6810c; }
  .why-note { margin-top: 12px; font-size: 13.5px; color: var(--navy-2); background: var(--blue-soft); border: 1px solid var(--blue-border); border-radius: 12px; padding: 12px 16px; line-height: 1.5; }
  .why-note b { color: var(--blue); }

  /* ---- PAGE 5 datasets ---- */
  .data-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 6px 0 14px; }
  .data-card { background: var(--paper); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 18px; }
  .data-card .fname { font-size: 13.5px; font-weight: 800; color: var(--blue); font-family: ui-monospace, monospace; }
  .data-card .big { font-size: 30px; font-weight: 800; color: var(--navy); margin: 6px 0 2px; }
  .data-card .lbl { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em; }
  .data-card p { font-size: 12.5px; color: var(--ink-2); line-height: 1.5; margin: 8px 0 0; }
  .data-note { font-size: 13.5px; color: var(--navy-2); background: var(--yellow-soft); border: 1px solid var(--yellow-border); border-radius: 12px; padding: 12px 16px; line-height: 1.5; }
  .data-note b { color: var(--navy); }

  /* ---- PAGE 6 demo ---- */
  .demo-grid { display: grid; grid-template-columns: 1.4fr 1fr; gap: 30px; align-items: center; margin-top: 6px; }
  .demo-list { list-style: none; padding: 0; margin: 8px 0 0; }
  .demo-list li { font-size: 14.5px; color: var(--ink); line-height: 1.5; padding: 7px 0 7px 26px; position: relative; border-bottom: 1px solid var(--border); }
  .demo-list li:before { content: '▸'; position: absolute; left: 4px; color: var(--blue); font-weight: 800; }
  .demo-list li b { color: var(--navy); }
  .qr-box { background: var(--paper); border: 2px dashed var(--blue-border); border-radius: 16px; box-shadow: var(--shadow); padding: 26px; text-align: center; }
  .qr-box .q { width: 130px; height: 130px; margin: 0 auto 14px; border-radius: 12px; background: repeating-conic-gradient(var(--navy) 0% 25%, #fff 0% 50%) 50% / 22px 22px; opacity: 0.15; }
  .qr-box .lbl { font-size: 13px; font-weight: 700; color: var(--navy); }
  .qr-box .url { font-size: 12px; color: var(--blue); margin-top: 4px; word-break: break-all; }

  /* ---- PAGE 7 impact ---- */
  .impact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 6px 0 12px; }
  .metric { background: var(--paper); border: 1px solid var(--border); border-radius: 16px; box-shadow: var(--shadow); padding: 16px 18px; }
  .metric h4 { font-size: 15.5px; font-weight: 700; color: var(--navy); margin: 6px 0 4px; }
  .metric p { font-size: 12.8px; color: var(--ink-2); line-height: 1.5; margin: 0; }
  .close-line { text-align: center; font-size: 17px; font-weight: 800; color: var(--navy); margin-top: 4px; }
  .close-line span { color: var(--blue); }
---

<!-- PAGE 1 : COVER -->

<div class="brand">
<svg width="30" height="30" viewBox="0 0 34 34" aria-hidden="true"><rect x="1" y="1" width="32" height="32" rx="8" fill="#FDB92C"/><path d="M11.5 21.5 L21.5 11.5 M21.5 11.5 L21.5 17.5 M21.5 11.5 L15.5 11.5" stroke="#10152E" stroke-width="2.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
<span class="brand-word">Expedia</span>
<span class="brand-sub">Campus Hackathon 2026 · Problem Statement 1</span>
</div>

<div class="cover-grid">
<div>

<div class="display">Way<span class="fin">Finder</span></div>

<div class="lead">The AI travel companion that reads the traveler, not just the query.</div>

<div class="sub">A traveler tells you how they fly in two places. Half sits in their profile. The other half is buried in messy history like <em>"redeyes kill my mornings."</em> WayFinder reads both, fuses them into one traveler model, searches 50,000 real itineraries, and shows a receipt for every decision it makes.</div>

<div class="byline">
<b>Ishika Sattawan</b>
<span>Build the Future of Travel · Innovation Round</span>
</div>

<div class="stat-row">
<div class="stat"><b>50,000</b><span>Itineraries</span></div>
<div class="stat"><b>50</b><span>Travelers</span></div>
<div class="stat blue"><b>42/42</b><span>Behaviors Verified</span></div>
</div>

</div>
<div>

<div class="browser">
<div class="browser-bar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i><i style="background:#28c840"></i><span class="browser-url">localhost:8000 · WayFinder</span></div>
<img src="assets/ui-b02-map.png" />
</div>
<div class="cap">The live product: multi-city routing rendered on a real great-circle map</div>

</div>
</div>

---

<!-- PAGE 2 : PROBLEM STATEMENT -->

<div class="tag-num"><span class="n">I</span> Problem Statement</div>

## Six travelers, one query, one lazy answer

<div class="prob-hero">Ask six different people to <b>"find me a flight"</b> and today's search hands all six the same list. A backpacker chasing the cheapest red-eye and a family of three with a stroller get treated as if they are the same person. They are not.</div>

<div class="prob-grid">
<div class="prob-card">
<h4>Filters cannot read a human</h4>
<p>"Redeyes kill my mornings" means nothing to a dropdown. The preferences that actually decide a booking never fit in a checkbox.</p>
</div>
<div class="prob-card">
<h4>The real signal is hiding</h4>
<p>Two kids. A 90 minute layover limit. School holidays only. It is all sitting in messy booking history, and nobody bothers to read it.</p>
</div>
<div class="prob-card blue">
<h4>So travelers bounce</h4>
<p>Every irrelevant top result is a booking the platform never makes, and often a support ticket it will. Generic ranking caps conversion no matter how good the inventory is.</p>
</div>
</div>

<div class="kicker-line">The gap: personalization that understands messy humans, and can prove how it did it.</div>

---

<!-- PAGE 3 : SOLUTION OVERVIEW -->

<div class="tag-num"><span class="n">II</span> Solution Overview</div>

## WayFinder reads the traveler, not just the query

<div class="pillar-grid">
<div class="pillar">
<span class="num">1</span>
<h4>Preference Fusion, with receipts</h4>
<p>Mines the messy free-text history with a curated signal lexicon and fuses it with the structured profile. Every inferred preference carries a confidence score and a verbatim quote, so you can see exactly where it came from. Contradictions get flagged, never silently overwritten.</p>
</div>
<div class="pillar">
<span class="num">2</span>
<h4>A route engine that never dead-ends</h4>
<p>Searches 50,000 itineraries with visit-order optimization for multi-city trips and composes its own connections when no published fare exists. When constraints cannot be met, a Relaxation Ladder loosens them one documented step at a time.</p>
</div>
<div class="pillar">
<span class="num">3</span>
<h4>A conversation, not a one-shot</h4>
<p>Say "make it cheaper" or "no redeyes" and it patches the original request and re-ranks, without forgetting anything you already asked for. Personalized fit scores from 0 to 100, every result explained in plain language.</p>
</div>
</div>

<div class="sol-foot">
<span class="pill-blue">Deterministic core</span>
<span class="pill-blue">Optional guarded LLM</span>
<span class="pill">Evidence on every pick</span>
<span class="pill">Trade-offs made explicit</span>
<span class="pill">Seasonal &amp; scarcity aware</span>
</div>

---

<!-- PAGE 4 : ARCHITECTURE / WORKFLOW -->

<div class="tag-num"><span class="n">III</span> Architecture &amp; Workflow</div>

## From a vague sentence to an explained itinerary

<div class="flow">
<div class="flow-row">
<div class="flow-step"><div class="s">Input</div><div class="t">Query + Traveler</div><div class="d">"Get me to Tokyo next month" for a specific profile</div></div>
<div class="flow-step"><div class="s">Step 1 · NLU</div><div class="t">Understand the ask</div><div class="d">Resolves dates against a simulated travel clock, detects trip shape</div></div>
<div class="flow-step"><div class="s">Step 2 · Fusion</div><div class="t">Build the traveler</div><div class="d">Profile plus mined history, every signal provenance-tagged</div></div>
</div>
<div class="flow-row">
<div class="flow-step"><div class="s">Step 3 · Search</div><div class="t">Find real routes</div><div class="d">Beam and permutation search, self-composed connections, relaxation ladder</div></div>
<div class="flow-step"><div class="s">Step 4 · Score</div><div class="t">Rank for this person</div><div class="d">Profile-derived weights produce a 0 to 100 fit score with a breakdown</div></div>
<div class="flow-step accent"><div class="s">Step 5 · Explain</div><div class="t">Show the receipts</div><div class="d">Trade-offs, seasonal and scarcity insights, evidence-cited narrative</div></div>
</div>
</div>

<div class="why-note"><b>Why it is built this way:</b> the core is a deterministic Python engine, so results are reproducible and the demo cannot break on stage. The LLM is optional and guarded, so every number it produces is checked against the deterministic engine and rejected if it does not match. With the AI switched fully off, the whole system still passes every test.</div>

---

<!-- PAGE 5 : DATASETS / INPUTS -->

<div class="tag-num"><span class="n">IV</span> Datasets &amp; Inputs Used</div>

## Built entirely on the provided hackathon data

<div class="data-grid">
<div class="data-card">
<div class="fname">flights_data.csv</div>
<div class="big">50,000</div>
<div class="lbl">Priced Itineraries</div>
<p>35 airports, 1,172 routes, 0 to 2 stops each. Carries price, seats left, on-time rate, season, and demand level per flight.</p>
</div>
<div class="data-card">
<div class="fname">user_data.csv</div>
<div class="big">50</div>
<div class="lbl">Traveler Profiles</div>
<p>16 structured columns plus a raw_history free-text field full of the messy, contradictory, real-world signal the engine mines.</p>
</div>
<div class="data-card">
<div class="fname">benchmark_prompts.json</div>
<div class="big">6</div>
<div class="lbl">Judge Prompts</div>
<p>B01 to B06, each with a list of expected behaviors. The app grades itself against these live.</p>
</div>
</div>

<div class="data-note"><b>One honest design note:</b> the flight data is historical, so WayFinder runs on a simulated travel clock set to August 2025. That is how a vague "next month" turns into a real, bookable window instead of a broken date. No external APIs, fully offline, exactly as the toolkit intended.</div>

---

<!-- PAGE 6 : DEMO VIDEO -->

<div class="tag-num"><span class="n">V</span> Demo Video</div>

## See it think, live (3 to 5 minutes)

<div class="demo-grid">
<div>
<ul class="demo-list">
<li><b>Personalization with receipts</b> · hover any preference to see the quote it came from</li>
<li><b>Conversational refinement</b> · "make it cheaper", "under $900", it never forgets or fakes</li>
<li><b>The family trap</b> · books 3 seats from "traveling with 2 kids", narrows to school holidays</li>
<li><b>The impossible request</b> · no direct Lisbon to Sydney exists, watch the Relaxation Ladder</li>
<li><b>Multi-city map</b> · every visit order tried, self-composed connections drawn as dashed arcs</li>
<li><b>Self-grading</b> · runs the judges' own prompts and verifies 42 of 42 behaviors on screen</li>
</ul>
</div>
<div>
<div class="qr-box">
<div class="q"></div>
<div class="lbl">Watch the 3 to 5 min demo</div>
<div class="url">[ paste OneDrive / YouTube link here ]</div>
</div>
</div>
</div>

---

<!-- PAGE 7 : IMPACT & CLOSE -->

<div class="tag-num"><span class="n">✦</span> Why It Wins</div>

## Proven, differentiated, and ready to grow

<div class="impact-grid">
<div class="metric">
<span class="pill-blue">Proof</span>
<h4>42 of 42 behaviors verified</h4>
<p>The app grades itself against the judges' own benchmark file, deterministically, reproducible with one command. Not screenshots, actual checks.</p>
</div>
<div class="metric">
<span class="pill">Differentiation</span>
<h4>Personalization you can audit</h4>
<p>Every recommendation traces to a cited reason. Receipts on preferences, honesty when a request is impossible, a conversation that remembers.</p>
</div>
<div class="metric">
<span class="pill-blue">Impact for Expedia</span>
<h4>Conversion, trust, deflection</h4>
<p>Relevant first results lift search-to-book. Transparent pricing and layover explanations pre-empt support tickets. Auditable ranking survives review.</p>
</div>
<div class="metric">
<span class="pill">Roadmap</span>
<h4>Built to extend, not throw away</h4>
<p>Live NDC and GDS feeds, learning-to-rank from real booking outcomes, and cross-product bundling for hotels and cars on the same trip clock.</p>
</div>
</div>

<div class="close-line">Personalization you can actually <span>audit</span>. Thank you.</div>
