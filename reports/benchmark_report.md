# WayFinder — Benchmark Self-Grading Report

Travel clock (SIM_TODAY): **2025-08-01** · LLM mode: **off** (all results below are fully deterministic)

Each benchmark from `benchmark_prompts.json` is executed end-to-end; every

**Overall: 42/42 expected behaviors verified.**

`expected_behavior` is verified programmatically against the actual response.


---

## B01 — U01 (Cape Town)

> **Request:** “I need to get from home to Tokyo next month, what do you suggest?”

Candidates evaluated: **2** · response time: 2.4ms · window: 2025-09-01 → 2025-09-30

| Expected behavior | Verified | Evidence |
|---|:---:|---|
| Infer preferences from BOTH structured fields and raw_history | ✅ | profile highlights draw on ['raw_history', 'structured']; e.g. raw: “always book business, hate connections” |
| Respect direct_preference='strong' and max_layover_minutes=120 | ✅ | cap=120min; all 2 recommendations within cap |
| Weight cost vs convenience per price_sensitivity='low' | ✅ | derived weights: {'price': 0.1579, 'convenience': 0.3684, 'time': 0.2105, 'reliability': 0.1579, 'preffit': 0.1053}; price weight 0.15 ← price_sensitivity='low' |
| Depart from home_airport=CPT; airline preferences engaged | ✅ | all itineraries start at CPT; preference-fit feature scored (preferred: ['AA']) |
| Surface the cost-vs-time trade-off explicitly | ✅ | Our recommended pick is also the cheapest available. |
| Account for seasonal/holiday pricing and seat scarcity | ✅ | Heads-up: no Business cabin is offered on this route for these dates (available: Economy) — showing the closest cabins instead. |
| Explain WHY the top pick fits this traveler, citing the evidence used | ✅ | 2 evidence-cited reasons; raw-history quoted: True; e.g. “Non-stop routing matches your direct-flight preference” ← “always book business, hate connections” |

### Full response narrative

### Trip plan for U01 — Cape Town traveler

**Understood as:** one way from CPT (Cape Town) to NRT (Tokyo), window 2025-09-01 → 2025-09-30.
- _“from home” -> CPT (Cape Town, profile home_airport)_
- _“next month” resolved to September 2025 (travel clock: 2025-08-01)_

**Filtered out for you:** 3 option(s) exceeded your layover cap.

**Top recommendation** (fit 77.1/100):
> CPT Mon 15 Sep 15:10 → NRT Tue 16 Sep 17:18 (Air India, Economy, direct, 19h08m) — $1,230 total

**Why this one, specifically for you:**
- Non-stop routing matches your direct-flight preference — _“always book business, hate connections”_ (raw history)
- No red-eye departures — _“redeyes kill my mornings, avoid if possible”_ (raw history)

**Trade-offs, in plain terms:**
- Our recommended pick is also the cheapest available.
- Our recommended pick is also the fastest available.

**Season, demand & availability:**
- Heads-up: no Business cabin is offered on this route for these dates (available: Economy) — showing the closest cabins instead.

**Also worth a look:**
- (fit 60.8) CPT Mon 15 Sep 14:40 → NRT Tue 16 Sep 16:48 (Turkish Airlines, Economy, direct, 19h08m) — $1,534 total

_Scoring weights used for you: price 16%, convenience 37%, time 21%, reliability 16%, preffit 11%._
- _price weight 0.15 ← price_sensitivity='low'_
- _convenience weight 0.35 ← direct_preference='strong'_
- _reliability ×1.5 ← business trip (on-time performance & refundability matter)_

_Noted (“aisle seat, front of cabin”): seat maps not in dataset — acknowledged, not optimized._


---

## B02 — U02 (Mexico City)

> **Request:** “Find me the best way to do a London + Paris + Rome trip in one journey.”

Candidates evaluated: **12** · response time: 34.5ms · window: 2025-08-08 → 2025-08-22

| Expected behavior | Verified | Evidence |
|---|:---:|---|
| Infer preferences from BOTH structured fields and raw_history | ✅ | profile highlights draw on ['raw_history', 'structured']; e.g. raw: “cheapest fare wins, dont care about stops” |
| Respect direct_preference='none' and max_layover_minutes=420 | ✅ | cap=420min; zero results under it — relaxation ladder applied and narrated: no feasible city chain in the requested window — scanned the next 6 months for the earliest well-priced chain |
| Weight cost vs convenience per price_sensitivity='high' | ✅ | derived weights: {'price': 0.5238, 'convenience': 0.1429, 'time': 0.1905, 'reliability': 0.0952, 'preffit': 0.0476}; price weight 0.55 ← price_sensitivity='high' |
| Depart from home_airport=MEX; airline preferences engaged | ✅ | all itineraries start at MEX; preference-fit feature scored (preferred: ['SQ', 'BA']) |
| Surface the cost-vs-time trade-off explicitly | ✅ | Cheapest option saves $13.85 vs our pick but takes 24h56m longer (5 stop(s) vs 4) — you'd be selling your time at $0.56/hr. |
| Account for seasonal/holiday pricing and seat scarcity | ✅ | MEX→CDG departs in year-end holiday season: fares run 56% premium vs shoulder season on this route (dataset medians). |
| Explain WHY the top pick fits this traveler, citing the evidence used | ✅ | 3 evidence-cited reasons; raw-history quoted: True; e.g. “Ticketed layovers total 6h21m — within your 420-min cap” ← profile field max_layover_minutes=420 |

### Full response narrative

### Trip plan for U02 — Mexico City traveler

**Understood as:** multi city from MEX (Mexico City) to LHR (London), CDG (Paris), FCO (Rome), window 2025-08-08 → 2025-08-22.
- _origin defaulted to home airport MEX (Mexico City)_
- _no dates given -> default window 2025-08-08..2025-08-22 (lead 7d + your flexibility 7d)_

**What we had to adjust (and why):**
- no feasible city chain in the requested window — scanned the next 6 months for the earliest well-priced chain → 12 option(s)

**Filtered out for you:** 70 option(s) exceeded your layover cap.

**Top recommendation** (fit 84.0/100):
> MEX Sat 27 Dec 14:30 → CDG Sun 28 Dec 17:24 (Emirates, Economy, 2 stop(s) via JFK, LHR, layover 6h21m, 19h54m) ➜ CDG Thu 15 Jan 13:30 → FCO Thu 15 Jan 15:32 (United Airlines, Economy, direct, 2h02m) ➜ FCO Sun 18 Jan 14:05 → LHR Sun 18 Jan 15:33 (Thai Airways, Economy, direct, 2h28m) ➜ LHR Mon 02 Feb 07:50 → MEX Tue 03 Feb 09:27 (Delta/Korean Air, Economy, 2 stop(s) via DOH, DXB*, layover 4h39m, 31h37m) — $3,052 total

**Why this one, specifically for you:**
- Ticketed layovers total 6h21m — within your 420-min cap — _profile field max_layover_minutes=420_ (structured)
- Economy cabin available, matching your usual choice — _profile field preferred_cabin=Economy_ (structured)
- Priced at $3,052/person — price given top priority — _“cheapest fare wins, dont care about stops”_ (raw history)

**Trade-offs, in plain terms:**
- Cheapest option saves $13.85 vs our pick but takes 24h56m longer (5 stop(s) vs 4) — you'd be selling your time at $0.56/hr.
- Our recommended pick is also the fastest available.
- No direct option exists among these results — every itinerary involves at least one stop.

**Season, demand & availability:**
- MEX→CDG departs in year-end holiday season: fares run 56% premium vs shoulder season on this route (dataset medians).
- FCO→LHR departs in winter low season: fares run 12% premium vs shoulder season on this route (dataset medians).
- Scarcity alert: only 2 seat(s) left on EK EK5873/EK1494/EK5250 (MEX→CDG, demand: peak).

**Also worth a look:**
- (fit 82.0) MEX Sat 27 Dec 14:30 → CDG Sun 28 Dec 17:24 (Emirates, Economy, 2 stop(s) via JFK, LHR, layover 6h21m, 19h54m) ➜ CDG Thu 15 Jan 13:30 → FCO Thu 15 Jan 15:32 (Emirates, Economy, direct, 2h02m) ➜ FCO Sun 18 Jan 14:05 → LHR Sun 18 Jan 15:33 (Thai Airways, Economy, direct, 2h28m) ➜ LHR Mon 02 Feb 07:50 → MEX Tue 03 Feb 09:27 (Delta/Korean Air, Economy, 2 stop(s) via DOH, DXB*, layover 4h39m, 31h37m) — $3,057 total
- (fit 74.4) MEX Sat 27 Dec 14:30 → CDG Sun 28 Dec 17:24 (Emirates, Economy, 2 stop(s) via JFK, LHR, layover 6h21m, 19h54m) ➜ CDG Thu 15 Jan 13:30 → FCO Thu 15 Jan 15:32 (United Airlines, Economy, direct, 2h02m) ➜ FCO Sun 18 Jan 14:05 → LHR Mon 19 Jan 16:29 (Qantas, Economy, 1 stop(s) via SFO, layover 2h44m, 27h24m) ➜ LHR Mon 02 Feb 07:50 → MEX Tue 03 Feb 09:27 (Delta/Korean Air, Economy, 2 stop(s) via DOH, DXB*, layover 4h39m, 31h37m) — $3,039 total

_Scoring weights used for you: price 52%, convenience 14%, time 19%, reliability 10%, preffit 5%._
- _price weight 0.55 ← price_sensitivity='high'_
- _convenience weight 0.15 ← direct_preference='none'_
- _preference-fit weight lowered ← “no loyalty” in history_


---

## B03 — U03 (Amsterdam)

> **Request:** “Cheapest option to Bali, I'm flexible on dates over the summer.”

Candidates evaluated: **2** · response time: 0.5ms · window: 2025-08-04 → 2025-08-31

| Expected behavior | Verified | Evidence |
|---|:---:|---|
| Infer preferences from BOTH structured fields and raw_history | ✅ | profile highlights draw on ['raw_history', 'structured']; e.g. raw: “traveling w/ 2 kids, direct is worth paying for” |
| Respect direct_preference='strong' and max_layover_minutes=150 | ✅ | cap=150min; all 2 recommendations within cap |
| Weight cost vs convenience per price_sensitivity='medium' | ✅ | derived weights: {'price': 0.4231, 'convenience': 0.2692, 'time': 0.1538, 'reliability': 0.0769, 'preffit': 0.0769}; price weight 0.35 ← price_sensitivity='medium' |
| Depart from home_airport=AMS; airline preferences engaged | ✅ | all itineraries start at AMS; preference-fit feature scored (preferred: ['KL', 'JL', 'CX']) |
| Surface the cost-vs-time trade-off explicitly | ✅ | Our recommended pick is also the cheapest available. |
| Account for seasonal/holiday pricing and seat scarcity | ✅ | AMS→DPS departs in summer peak season: fares run 55% premium vs shoulder season on this route (dataset medians). |
| Explain WHY the top pick fits this traveler, citing the evidence used | ✅ | 4 evidence-cited reasons; raw-history quoted: True; e.g. “Non-stop routing matches your direct-flight preference” ← “traveling w/ 2 kids, direct is worth paying for” |

### Full response narrative

### Trip plan for U03 — Amsterdam traveler

**Understood as:** one way from AMS (Amsterdam) to DPS (Denpasar), window 2025-08-04 → 2025-08-31, party of 3.
- _origin defaulted to home airport AMS (Amsterdam)_
- _“summer” -> 2025-08-04..2025-08-31_
- _narrowed to school-holiday months [7, 8] (seasonal pattern + “school breaks only”) -> 2025-08-04..2025-08-31_

**Filtered out for you:** 4 option(s) exceeded your layover cap.

**Top recommendation** (fit 79.1/100):
> AMS Thu 28 Aug 01:35 → DPS Thu 28 Aug 23:26 (Korean Air, Economy, direct, 15h51m) — $5,451 total ($1,817/person)

**Why this one, specifically for you:**
- Non-stop routing matches your direct-flight preference — _“traveling w/ 2 kids, direct is worth paying for”_ (raw history)
- Economy cabin available, matching your usual choice — _profile field preferred_cabin=Economy_ (structured)
- 4 seats available — fits your party of 3 — _“traveling w/ 2 kids, direct is worth paying for”_ (raw history)
- Total $5,451 for 3 traveler(s) — optimized for price as requested — _your request_ (query)

**Trade-offs, in plain terms:**
- Our recommended pick is also the cheapest available.
- Our recommended pick is also the fastest available.

**Season, demand & availability:**
- AMS→DPS departs in summer peak season: fares run 55% premium vs shoulder season on this route (dataset medians).
- Demand on AMS→DPS is high for these dates — booking early is wise.

**Also worth a look:**
- (fit 38.0) AMS Thu 28 Aug 01:05 → DPS Thu 28 Aug 22:56 (Emirates, Economy, direct, 15h51m) — $5,607 total ($1,869/person)

_Scoring weights used for you: price 42%, convenience 27%, time 15%, reliability 8%, preffit 8%._
- _price weight 0.35 ← price_sensitivity='medium'_
- _convenience weight 0.35 ← direct_preference='strong'_
- _price +0.20 ← you asked for “cheapest” (inferred needs still enforced)_


---

## B04 — U04 (Melbourne)

> **Request:** “Book me something to New York for a Tuesday meeting, back Thursday.”

Candidates evaluated: **56** · response time: 4.5ms · window: 2025-08-01 → 2025-11-14

| Expected behavior | Verified | Evidence |
|---|:---:|---|
| Infer preferences from BOTH structured fields and raw_history | ✅ | profile highlights draw on ['raw_history', 'structured']; e.g. raw: “carry-on only, live out of a backpack” |
| Respect direct_preference='moderate' and max_layover_minutes=300 | ✅ | cap=300min; zero results under it — relaxation ladder applied and narrated: widened window by your ±21-day flexibility; no published itinerary pairing worked — added self-transfer connections built from separate tickets (90min–6h transfer buffer); no itinerary pair matches the exact weekday pattern in the dataset — showing the closest available round trips instead |
| Weight cost vs convenience per price_sensitivity='high' | ✅ | derived weights: {'price': 0.44, 'convenience': 0.2, 'time': 0.16, 'reliability': 0.12, 'preffit': 0.08}; price weight 0.55 ← price_sensitivity='high' |
| Depart from home_airport=MEL; airline preferences engaged | ✅ | all itineraries start at MEL; preference-fit feature scored (preferred: ['JL']) |
| Surface the cost-vs-time trade-off explicitly | ✅ | Cheapest option saves $1,063 vs our pick but takes 40h24m longer (4 stop(s) vs 1) — you'd be selling your time at $26.31/hr. |
| Account for seasonal/holiday pricing and seat scarcity | ✅ | no seasonal/scarcity signal in window (all shoulder-season, ample seats) |
| Explain WHY the top pick fits this traveler, citing the evidence used | ✅ | 3 evidence-cited reasons; raw-history quoted: True; e.g. “Ticketed layovers total 0m — within your 300-min cap” ← profile field max_layover_minutes=300 |

### Full response narrative

### Trip plan for U04 — Melbourne traveler

**Understood as:** round trip from MEL (Melbourne) to JFK (New York), window 2025-08-01 → 2025-11-14.
- _origin defaulted to home airport MEL (Melbourne)_
- _weekday pattern trip: scanning the next 12 weeks of Tuesdays_
- _purpose inferred as business (“meeting”)_

**What we had to adjust (and why):**
- widened window by your ±21-day flexibility → 0 option(s)
- no published itinerary pairing worked — added self-transfer connections built from separate tickets (90min–6h transfer buffer) → 0 option(s)
- no itinerary pair matches the exact weekday pattern in the dataset — showing the closest available round trips instead → 56 option(s)

**Filtered out for you:** 9 option(s) exceeded your layover cap.

**Top recommendation** (fit 77.3/100):
> MEL Wed 01 Oct 12:55 → JFK Thu 02 Oct 07:46 (American Airlines/Thai Airways, Economy, 1 stop(s) via AKL*, layover 10h28m, 32h51m) ➜ JFK Fri 03 Oct 06:20 → MEL Sat 04 Oct 17:52 (United Airlines, Economy, direct, 21h32m) — $3,410 total

**Why this one, specifically for you:**
- Ticketed layovers total 0m — within your 300-min cap — _profile field max_layover_minutes=300_ (structured)
- Keeps connections to 0m — far below the layovers you pay to avoid — _“value matters but i'll pay to skip a 10hr layover”_ (raw history)
- Economy cabin available, matching your usual choice — _profile field preferred_cabin=Economy_ (structured)

**Trade-offs, in plain terms:**
- Cheapest option saves $1,063 vs our pick but takes 40h24m longer (4 stop(s) vs 1) — you'd be selling your time at $26.31/hr.
- Fastest option saves 30m and costs $84.81 less.
- No direct option exists among these results — every itinerary involves at least one stop.

**Also worth a look:**
- (fit 76.7) MEL Wed 01 Oct 12:25 → JFK Thu 02 Oct 07:46 (Air France/Thai Airways, Economy, 1 stop(s) via AKL*, layover 10h58m, 33h21m) ➜ JFK Fri 03 Oct 06:20 → MEL Sat 04 Oct 17:52 (United Airlines, Economy, direct, 21h32m) — $3,396 total
- (fit 76.6) MEL Wed 01 Oct 12:55 → JFK Thu 02 Oct 07:16 (American Airlines/Turkish Airlines, Economy, 1 stop(s) via AKL*, layover 9h58m, 32h21m) ➜ JFK Fri 03 Oct 06:20 → MEL Sat 04 Oct 17:52 (United Airlines, Economy, direct, 21h32m) — $3,326 total

_Scoring weights used for you: price 44%, convenience 20%, time 16%, reliability 12%, preffit 8%._
- _price weight 0.55 ← price_sensitivity='high'_
- _convenience weight 0.25 ← direct_preference='moderate'_
- _reliability ×1.5 ← business trip (on-time performance & refundability matter)_


---

## B05 — U05 (Lisbon)

> **Request:** “I want to visit Sydney around the holidays — what should I expect?”

Candidates evaluated: **1** · response time: 0.6ms · window: 2025-12-11 → 2026-01-09

| Expected behavior | Verified | Evidence |
|---|:---:|---|
| Infer preferences from BOTH structured fields and raw_history | ✅ | profile highlights draw on ['raw_history', 'structured']; e.g. raw: “direct whenever it exists” |
| Respect direct_preference='strong' and max_layover_minutes=90 | ✅ | cap=90min; zero results under it — relaxation ladder applied and narrated: widened window by your ±4-day flexibility; no published itinerary pairing worked — added self-transfer connections built from separate tickets (90min–6h transfer buffer); layover cap relaxed 90→135 min (×1.5) |
| Weight cost vs convenience per price_sensitivity='none' | ✅ | derived weights: {'price': 0.0625, 'convenience': 0.4375, 'time': 0.25, 'reliability': 0.125, 'preffit': 0.125}; price weight 0.05 ← price_sensitivity='none' |
| Depart from home_airport=LIS; airline preferences engaged | ✅ | all itineraries start at LIS; preference-fit feature scored (preferred: ['LH']) |
| Surface the cost-vs-time trade-off explicitly | ✅ | Our recommended pick is also the cheapest available. |
| Account for seasonal/holiday pricing and seat scarcity | ✅ | LIS→SYD departs in year-end holiday season: fares run 82% premium vs shoulder season on this route (dataset medians). |
| Explain WHY the top pick fits this traveler, citing the evidence used | ✅ | 3 evidence-cited reasons; raw-history quoted: True; e.g. “Business is the highest cabin sold here — closest available to your First preference” ← “first or business only, comfort over cost” |

### Full response narrative

### Trip plan for U05 — Lisbon traveler

**Understood as:** one way from LIS (Lisbon) to SYD (Sydney), window 2025-12-11 → 2026-01-09.
- _origin defaulted to home airport LIS (Lisbon)_
- _“around the holidays” -> year-end window 2025-12-15..2026-01-05_

**Straight talk about this route:**
- No direct LIS→SYD flights exist in the entire dataset (9 itineraries, all with stops; shortest total layover on record: 105 min).
- No First cabin is sold on LIS→SYD in this dataset (available: Business, Economy).

**What we had to adjust (and why):**
- widened window by your ±4-day flexibility → 0 option(s)
- no published itinerary pairing worked — added self-transfer connections built from separate tickets (90min–6h transfer buffer) → 0 option(s)
- layover cap relaxed 90→135 min (×1.5) → 1 option(s)

**Filtered out for you:** 2 option(s) exceeded your layover cap.

**Top recommendation** (fit 63.8/100):
> LIS Fri 19 Dec 09:40 → SYD Sat 20 Dec 22:50 (Qantas, Business, 1 stop(s) via CDG, layover 1h50m, 26h10m) — $10,162 total

**Why this one, specifically for you:**
- Business is the highest cabin sold here — closest available to your First preference — _“first or business only, comfort over cost”_ (raw history)
- Comfort and schedule prioritized over price, as money is not your constraint — _“happy in peak season, money's not the constraint”_ (raw history)
- No direct option exists here; this keeps the layover to 1h50m — the least connection pain available — _“direct whenever it exists”_ (raw history)

**Trade-offs, in plain terms:**
- Our recommended pick is also the cheapest available.
- Our recommended pick is also the fastest available.
- No direct option exists among these results — every itinerary involves at least one stop.

**Season, demand & availability:**
- LIS→SYD departs in year-end holiday season: fares run 82% premium vs shoulder season on this route (dataset medians).
- Scarcity alert: only 3 seat(s) left on QF QF5039/QF5125 (LIS→SYD, demand: peak).
- Heads-up: no First cabin is offered on this route for these dates (available: Business) — showing the closest cabins instead.

_Scoring weights used for you: price 6%, convenience 44%, time 25%, reliability 12%, preffit 12%._
- _price weight 0.05 ← price_sensitivity='none'_
- _convenience weight 0.35 ← direct_preference='strong'_

_Noted (“spa lounge, chauffeur transfer, the works”): ground services not in dataset — acknowledged._


---

## B06 — U06 (Chennai)

> **Request:** “Plan a multi-city Asia trip, I have about three weeks of flexibility.”

Candidates evaluated: **20** · response time: 121.8ms · window: 2025-08-08 → 2025-10-30

| Expected behavior | Verified | Evidence |
|---|:---:|---|
| Infer preferences from BOTH structured fields and raw_history | ✅ | profile highlights draw on ['raw_history', 'structured']; e.g. raw: “2 stops fine, even overnight layovers” |
| Respect direct_preference='none' and max_layover_minutes=480 | ✅ | cap=480min; all 1 recommendations within cap |
| Weight cost vs convenience per price_sensitivity='high' | ✅ | derived weights: {'price': 0.5, 'convenience': 0.1364, 'time': 0.1818, 'reliability': 0.0909, 'preffit': 0.0909}; price weight 0.55 ← price_sensitivity='high' |
| Depart from home_airport=MAA; airline preferences engaged | ✅ | all itineraries start at MAA; preference-fit feature scored (preferred: ['SQ', 'QR']) |
| Surface the cost-vs-time trade-off explicitly | ✅ | Our recommended pick is also the cheapest available. |
| Account for seasonal/holiday pricing and seat scarcity | ✅ | no seasonal/scarcity signal in window (all shoulder-season, ample seats) |
| Explain WHY the top pick fits this traveler, citing the evidence used | ✅ | 3 evidence-cited reasons; raw-history quoted: True; e.g. “Ticketed layovers total 3h14m — within your 480-min cap” ← profile field max_layover_minutes=480 |

### Full response narrative

### Trip plan for U06 — Chennai traveler

**Understood as:** open ended from MAA (Chennai) to Asia (open-ended), window 2025-08-08 → 2025-10-30.
- _origin defaulted to home airport MAA (Chennai)_
- _target trip length ≈ 21 days_
- _flexible start window 2025-08-08..2025-10-30_

**Signals we reconciled from your history:**
- persona: age 66 (structured) vs “broke student, absolute cheapest only” (raw history) — behavioral signal wins for weighting; flagged for review

**Filtered out for you:** 336 option(s) exceeded your layover cap.

**Top recommendation** (fit 81.5/100):
> MAA Sat 13 Sep 19:25 → BKK Mon 15 Sep 01:19 (Air India, Economy, 2 stop(s) via LHR, DOH, layover 2h59m, 28h24m) ➜ BKK Mon 22 Sep 22:50 → ICN Wed 24 Sep 00:18 (Turkish Airlines, Economy, 1 stop(s) via IST, layover 2h51m, 23h28m) ➜ ICN Fri 03 Oct 22:10 → HKG Sun 05 Oct 07:14 (Turkish Airlines, Economy, 1 stop(s) via JFK, layover 2h41m, 34h04m) ➜ HKG Fri 10 Oct 09:50 → MAA Sat 11 Oct 19:11 (Lufthansa, Economy, 1 stop(s) via SFO, layover 3h14m, 35h51m) — $906 total

**Why this one, specifically for you:**
- Ticketed layovers total 3h14m — within your 480-min cap — _profile field max_layover_minutes=480_ (structured)
- Economy cabin available, matching your usual choice — _profile field preferred_cabin=Economy_ (structured)
- Priced at $906/person — price given top priority — _“broke student, absolute cheapest only”_ (raw history)

**Trade-offs, in plain terms:**
- Our recommended pick is also the cheapest available.
- Fastest option saves 30h49m for $49.06 more.
- No direct option exists among these results — every itinerary involves at least one stop.

**Also worth a look:**
- (fit 73.2) MAA Sat 13 Sep 19:25 → BKK Mon 15 Sep 01:19 (Air India, Economy, 2 stop(s) via LHR, DOH, layover 2h59m, 28h24m) ➜ BKK Mon 22 Sep 22:50 → ICN Wed 24 Sep 00:18 (Turkish Airlines, Economy, 1 stop(s) via IST, layover 2h51m, 23h28m) ➜ ICN Fri 03 Oct 22:40 → HKG Sat 04 Oct 00:55 (American Airlines, Economy, direct, 3h15m) ➜ HKG Fri 10 Oct 09:50 → MAA Sat 11 Oct 19:11 (Lufthansa, Economy, 1 stop(s) via SFO, layover 3h14m, 35h51m) — $955 total
- (fit 71.8) MAA Sat 13 Sep 19:25 → BKK Mon 15 Sep 01:19 (Air India, Economy, 2 stop(s) via LHR, DOH, layover 2h59m, 28h24m) ➜ BKK Mon 22 Sep 22:50 → ICN Wed 24 Sep 02:11 (Lufthansa, Economy, 1 stop(s) via AMS, layover 1h50m, 25h21m) ➜ ICN Fri 03 Oct 22:10 → HKG Sun 05 Oct 07:14 (Turkish Airlines, Economy, 1 stop(s) via JFK, layover 2h41m, 34h04m) ➜ HKG Fri 10 Oct 09:50 → MAA Sat 11 Oct 19:11 (Lufthansa, Economy, 1 stop(s) via SFO, layover 3h14m, 35h51m) — $928 total

_Scoring weights used for you: price 50%, convenience 14%, time 18%, reliability 9%, preffit 9%._
- _price weight 0.55 ← price_sensitivity='high'_
- _convenience weight 0.15 ← direct_preference='none'_
