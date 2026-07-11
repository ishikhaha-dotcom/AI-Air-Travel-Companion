# Demo Video Script (target 4:30)

> Recording setup: app running at http://localhost:8000 (backend serves the built UI).
> 1080p, dark theme. Rehearse once; the pipeline is deterministic so every take is identical.
> Keep the cursor deliberate; pause 1s after each reveal.

| Time | Scene | Say (voiceover) | Show (actions) |
|------|-------|-----------------|----------------|
| 0:00–0:35 | Hook | "Ask six travelers 'find me a flight' and there are six different right answers. This is WayFinder — it reads the traveler, not just the query. Fifty thousand itineraries, fifty travelers with messy booking histories, and six benchmark prompts from the judges. Watch it pass all of them, live, with zero LLM dependency." | App header (travel clock badge, 50,000 flights, LLM: off). Scroll the persona rail. |
| 0:35–1:20 | B01 — personalization basics | "U01, Cape Town executive: business cabin, hates connections, red-eyes kill his mornings. 'Get me to Tokyo next month.' WayFinder resolves 'next month' against the travel clock, filters three options that broke his 2-hour layover cap, and explains the pick by quoting his own history." | Click chip B01. Point at: intent notes ("next month → September 2025"), filtered-out line, top card's why-section quotes ("hate connections", "redeyes kill my mornings"), score-breakdown bars. |
| 1:20–2:05 | B03 — the family trap | "U03 asks for the *cheapest* trip to Bali. But her history says 'traveling with 2 kids' — so WayFinder books for three seats, narrows 'summer' to her school-holiday window, and refuses to sell her the absolute-cheapest fare that doesn't fit her life. It shows the tension instead." | Click B03. Hover the party-of-3 chip (evidence tooltip). Show intent note (window narrowed to August), seats pill on the card, trade-off strip Cheapest vs Recommended. |
| 2:05–2:55 | B05 — the impossible request | "U05 flies First, direct-only, 90-minute layovers max, money no object. Sydney for the holidays. Here's the trap: no direct Lisbon–Sydney flight exists in this data. And no First cabin either. WayFinder doesn't error and doesn't fake it — it relaxes constraints one documented step at a time, and prices the holiday premium from the data itself." | Click B05. Point at the route-reality banner, the amber relaxation steps, Business-via-CDG card ($10k, 110-min layover), seasonal premium insight. |
| 2:55–3:40 | B02 + B06 — route optimization | "Multi-city is a real optimizer: for London-Paris-Rome it tries every visit order and chains real dated flights — and when Mexico City has no European service until December, it says so honestly. For 'a multi-city Asia trip' it runs a beam search over the route graph and proposes three complete loops within budget." | Click B02: show the map with the multi-leg arcs + the honest date note. Click B06: three distinct city-set options, map, total price headline. |
| 3:40–4:10 | Self-grading | "Don't take my word for it. This tab runs the judges' own benchmark file and programmatically checks every expected behavior against the live response. Forty-two out of forty-two — in under half a second each." | Benchmark tab → Run all 6. Let the green checks fill. Zoom the 42/42 counter. |
| 4:10–4:35 | Close | "Deterministic core, optional LLM polish with hallucination guards, twenty-six tests, full docs, and every recommendation explained with receipts — the traveler's own words. WayFinder: personalization you can audit. Thank you." | Flash docs/ARCHITECTURE.md diagram, pytest output, then back to the app hero. |

## Recording checklist
- [ ] `python -m uvicorn app.main:app --port 8000` running; http://localhost:8000 loads
- [ ] Fresh browser profile, 100% zoom, 1920×1080, no bookmarks bar
- [ ] Run each benchmark once before recording (warm, and you know what appears)
- [ ] Mic check; speak 10% slower than feels natural
- [ ] Export MP4 ≤ 5 min; verify audio sync; upload to the OneDrive folder with view-for-everyone
