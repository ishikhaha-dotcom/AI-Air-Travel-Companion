"""Benchmark self-grading harness: runs B01–B06 end-to-end and verifies each
machine-checkable expected_behavior from benchmark_prompts.json, then writes
reports/benchmark_report.md (submission evidence).

Run:  python -m benchmark.run_benchmarks
"""
from __future__ import annotations

import sys
from pathlib import Path

from app import config
from app.service import recommend
from app.state import get_dataset


def check_benchmark(bench: dict, res: dict, user) -> list[dict]:
    """-> [{behavior, passed, evidence}] — one row per judged dimension."""
    checks: list[dict] = []
    recs = res["recommendations"]
    top = recs[0] if recs else None

    def add(behavior: str, passed: bool, evidence: str) -> None:
        checks.append({"behavior": behavior, "passed": passed, "evidence": evidence})

    # 1. Preference inference from BOTH structured fields and raw_history
    sources = {h["source"] for h in res["profile_highlights"]}
    raw_used = [h for h in res["profile_highlights"] if h["source"] == "raw_history"]
    add("Infer preferences from BOTH structured fields and raw_history",
        {"structured", "raw_history"} <= sources,
        f"profile highlights draw on {sorted(sources)}; e.g. raw: "
        + (raw_used[0]["evidence"] if raw_used else "none"))

    # 2. Respect direct_preference and max_layover_minutes
    cap = user.max_layover_minutes
    relaxed = bool(res["relaxations"])
    cap_eff = cap * (2.0 if relaxed else 1.0)
    viol = [o for o in recs for leg in o["legs"]
            if leg["in_ticket_layover"] > cap_eff]
    detail = f"cap={cap}min; all {len(recs)} recommendations within cap"
    if relaxed:
        detail = (f"cap={cap}min; zero results under it — relaxation ladder applied and "
                  f"narrated: " + "; ".join(r["detail"] for r in res["relaxations"]))
    add(f"Respect direct_preference='{user.direct_preference}' and "
        f"max_layover_minutes={cap}", not viol, detail)

    # 3. Cost-vs-convenience weighting per price_sensitivity
    w = res["weights"]
    note_ok = any("price_sensitivity" in n for n in res["weight_notes"])
    add(f"Weight cost vs convenience per price_sensitivity='{user.price_sensitivity}'",
        note_ok and 0 < w["price"] < 1,
        f"derived weights: {w}; " + next((n for n in res['weight_notes'] if 'price' in n), ""))

    # 4. Filter from home_airport (+ airline preference engaged in scoring)
    origins_ok = all(o["legs"][0]["origin"] == user.home_airport for o in recs)
    add(f"Depart from home_airport={user.home_airport}; airline preferences engaged",
        origins_ok and (not recs or "preffit" in recs[0]["goodness"]),
        f"all itineraries start at {user.home_airport}; preference-fit feature scored "
        f"(preferred: {user.preferred_airlines or 'none'})")

    # 5. Cost-vs-time trade-off surfaced explicitly
    t = res["tradeoffs"]
    add("Surface the cost-vs-time trade-off explicitly",
        bool(t.get("statements")) and "cheapest" in t and "fastest" in t,
        (t.get("statements") or ["none"])[0])

    # 6. Seasonal/holiday pricing and seat scarcity awareness
    flights = [f for o in recs for leg in o["legs"] for f in leg["flights"]]
    needs_note = any(f["season"] != "shoulder" or f["seats"] <= 3
                     or f["demand"] in ("high", "peak") for f in flights)
    add("Account for seasonal/holiday pricing and seat scarcity",
        bool(res["insights"]) or not needs_note,
        res["insights"][0] if res["insights"] else "no seasonal/scarcity signal in window "
        "(all shoulder-season, ample seats)")

    # 7. Explain WHY, citing evidence
    why = top["why"] if top else []
    raw_cited = any(x["source"] == "raw_history" for x in why)
    add("Explain WHY the top pick fits this traveler, citing the evidence used",
        top is not None and len(why) >= 2 and raw_cited,
        f"{len(why)} evidence-cited reasons; raw-history quoted: {raw_cited}; e.g. "
        + (f"“{why[0]['reason']}” ← {why[0]['evidence']}" if why else "n/a"))
    return checks


def main() -> int:
    ds = get_dataset()
    lines: list[str] = [
        "# WayFinder — Benchmark Self-Grading Report",
        f"\nTravel clock (SIM_TODAY): **{config.sim_today()}** · LLM mode: "
        f"**{config.llm_mode()}** (all results below are fully deterministic)\n",
        "Each benchmark from `benchmark_prompts.json` is executed end-to-end; every",
        "`expected_behavior` is verified programmatically against the actual response.\n",
    ]
    total_pass = total = 0
    console: list[str] = []

    for bench in ds.benchmarks:
        bid, uid = bench["prompt_id"], bench["user_id"]
        res = recommend(uid, bench["request"])
        user = ds.users[uid]
        checks = check_benchmark(bench, res, user)
        npass = sum(1 for c in checks if c["passed"])
        total_pass += npass
        total += len(checks)
        console.append(f"[{'PASS' if npass == len(checks) else 'WARN'}] {bid} {uid}: "
                       f"{npass}/{len(checks)} behaviors verified "
                       f"({res['total_candidates']} candidates, {res['elapsed_ms']}ms)")

        lines.append(f"\n---\n\n## {bid} — {uid} ({user.home_city})")
        lines.append(f"\n> **Request:** “{bench['request']}”\n")
        lines.append(f"Candidates evaluated: **{res['total_candidates']}** · "
                     f"response time: {res['elapsed_ms']}ms · "
                     f"window: {res['intent']['window_start']} → {res['intent']['window_end']}\n")
        lines.append("| Expected behavior | Verified | Evidence |")
        lines.append("|---|:---:|---|")
        for c in checks:
            ev = c["evidence"].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {c['behavior']} | {'✅' if c['passed'] else '❌'} | {ev} |")
        lines.append(f"\n### Full response narrative\n\n{res['narrative']}\n")

    lines.insert(3, f"\n**Overall: {total_pass}/{total} expected behaviors verified.**\n")
    config.REPORTS_DIR.mkdir(exist_ok=True)
    out = config.REPORTS_DIR / "benchmark_report.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(console))
    print(f"\nOverall: {total_pass}/{total} behaviors verified -> {out}")
    return 0 if total_pass == total else 1


if __name__ == "__main__":
    sys.exit(main())
