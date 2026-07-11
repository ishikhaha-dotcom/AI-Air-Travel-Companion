# Demo Video Script (target 4:40, hard cap 5:00)

> Recording setup: app running at http://localhost:8000 (backend serves the built UI).
> 1080p, dark theme. Rehearse once; the pipeline is deterministic so every take is identical.
> Keep the cursor deliberate; pause 1s after each reveal. If Ollama is running the header
> reads "AI: llama3.1 · guarded"; if not, "AI: deterministic engine" — both are demo-safe
> (mention whichever is showing).

| Time | Scene | Say (voiceover) | Show (actions) |
|------|-------|-----------------|----------------|
| 0:00–0:30 | Hook | "Ask six travelers 'find me a flight' and there are six different right answers. This is WayFinder — it reads the traveler, not just the query. Fifty thousand itineraries, fifty travelers with messy booking histories, and the six benchmark prompts the judges wrote — scored live, in the app." | App header (travel clock, 50,000 flights chip, AI status chip). Scroll the persona rail briefly. |
| 0:30–1:15 | B01 — personalization with receipts | "U01, Cape Town executive: business cabin, hates connections, red-eyes kill his mornings. 'Get me to Tokyo next month.' WayFinder resolves 'next month' against the travel clock, respects his 2-hour layover cap, and explains the pick by quoting his own history. One summary card — because our best-fit pick is also the cheapest and the fastest, and it says so instead of padding three columns." | Click chip B01. Point at: hard/strong/soft profile groups, hover **direct preference: strong** (evidence tooltip), intent notes ("next month → September 2025"), the collapsed Recommended card with 'also the cheapest · also the fastest' badges, the fit ring + quoted reasons on card #1. |
| 1:15–1:55 | Refinement — the conversation | "And it takes follow-ups. 'Make it cheaper' — the intent is patched, the plan re-runs, and the applied change is chipped right there. 'Under 900 dollars' — when a cap can't be met it says so honestly and shows the closest. It never dead-ends, and it never forgets what you asked first." | Click **make it cheaper** suggestion chip → point at the applied chip + 'optimizing for cheapest' in Understood. Type `under $900`, Enter → point at the honest '(budget cap: no itinerary qualifies…)' chip. |
| 1:55–2:35 | B03 — the family trap | "U03 asks for the *cheapest* trip to Bali. But her history says 'traveling with 2 kids' — so WayFinder books for three seats, narrows 'summer' to her school-holiday window, and shows the tension between absolute-cheapest and what actually fits her life." | Click B03. Hover the party-of-3 chip (evidence tooltip). Intent note (window narrowed), seats on the card, trade-off tiles with delta lines. |
| 2:35–3:20 | B05 — the impossible request | "U05 flies First, direct-only, 90-minute layovers, money no object. Sydney for the holidays. The trap: no direct Lisbon–Sydney flight exists in this data — and no First cabin either. WayFinder doesn't error and doesn't fake it: route reality first, then it relaxes constraints one documented step at a time, and prices the holiday premium from the data itself." | Click B05. Point at the **Route reality** banner, the amber **Adjusted** relaxation steps, the Business-via-CDG card, the year-end premium insight. |
| 3:20–3:55 | B02 — multi-city optimizer | "Multi-city is a real optimizer: for London-Paris-Rome it tries every visit order and chains real dated flights — self-composed connections where no published fare exists, drawn right on the map. And a scarcity alert: two seats left on the Emirates leg." | Click B02. Scroll to the map (animated arcs, dashed self-transfer), one multi-leg itinerary card, the seat-scarcity insight. |
| 3:55–4:25 | Self-grading | "Don't take my word for it. This tab runs the judges' own benchmark file and programmatically checks every expected behavior against the live response. Forty-two out of forty-two, about thirty milliseconds each — deterministic, so it reproduces on your machine with one command." | Benchmark tab → **Run all 6**. Let the trophy stat strip fill (42/42). Expand one check row. |
| 4:25–4:40 | Close | "Preference fusion with receipts, graph search with honesty, a conversational refinement loop, and a benchmark harness that grades itself. WayFinder: personalization you can audit. Thank you." | Stay on the 42/42 screen; end frame. |

## Recording checklist
- [ ] `python -m uvicorn app.main:app --port 8000` running; http://localhost:8000 loads (hard refresh)
- [ ] Fresh browser profile, 100% zoom, 1920×1080, no bookmarks bar
- [ ] Run each benchmark once before recording (warm, and you know what appears)
- [ ] Searches take ~1–6 s — narrate over them, never silence
- [ ] Mic check; speak 10% slower than feels natural
- [ ] Export MP4 ≤ 5 min (`WayFinder_demo.mp4`); verify audio sync; upload to the OneDrive folder with view-for-everyone
