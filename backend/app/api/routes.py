"""HTTP API. Thin layer over app.service — all logic lives in the pipeline."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import config
from ..profile.fusion import fuse, profile_highlights
from ..service import recommend
from ..state import get_dataset
from benchmark.run_benchmarks import check_benchmark

router = APIRouter(prefix="/api")


class RecommendRequest(BaseModel):
    user_id: str
    query: str
    top_n: int | None = None


@router.get("/meta")
def meta() -> dict:
    ds = get_dataset()
    return {
        "sim_today": config.sim_today().isoformat(),
        "llm_mode": config.llm_mode(),
        "flights": len(ds.flights),
        "users": len(ds.users),
        "routes": len(ds.by_route),
        "benchmarks": len(ds.benchmarks),
        "qa": ds.qa,
    }


@router.get("/users")
def users() -> list[dict]:
    ds = get_dataset()
    out = []
    for u in ds.users.values():
        out.append({
            "user_id": u.user_id, "age": u.age, "home_airport": u.home_airport,
            "home_city": u.home_city, "trip_purpose": u.trip_purpose,
            "price_sensitivity": u.price_sensitivity,
            "direct_preference": u.direct_preference,
            "preferred_cabin": u.preferred_cabin,
            "summary": f"{u.home_city} · {u.trip_purpose} · "
                       f"{u.preferred_cabin} · price sens. {u.price_sensitivity}",
        })
    return out


@router.get("/users/{user_id}/profile")
def user_profile(user_id: str) -> dict:
    ds = get_dataset()
    if user_id not in ds.users:
        raise HTTPException(404, f"unknown user {user_id}")
    u = ds.users[user_id]
    prof = fuse(u)
    return {
        "user_id": user_id, "home_city": u.home_city, "home_airport": u.home_airport,
        "age": u.age, "raw_history": u.raw_history,
        "party_size": prof.party_size,
        "contradictions": prof.contradictions,
        "preferences": [
            {"key": p.key, "value": p.value, "strength": p.strength,
             "source": p.source, "evidence": p.evidence,
             "confidence": p.confidence, "note": p.note}
            for p in sorted(prof.preferences,
                            key=lambda p: {"hard": 0, "strong": 1, "soft": 2}[p.strength])
        ],
        "highlights": profile_highlights(prof, limit=10),
    }


@router.post("/recommend")
def api_recommend(req: RecommendRequest) -> dict:
    ds = get_dataset()
    if req.user_id not in ds.users:
        raise HTTPException(404, f"unknown user {req.user_id}")
    if not req.query.strip():
        raise HTTPException(422, "query must not be empty")
    return recommend(req.user_id, req.query, req.top_n)


@router.get("/benchmarks")
def benchmarks() -> list[dict]:
    return get_dataset().benchmarks


@router.post("/benchmarks/{prompt_id}/run")
def run_benchmark(prompt_id: str) -> dict:
    ds = get_dataset()
    bench = next((b for b in ds.benchmarks if b["prompt_id"] == prompt_id), None)
    if bench is None:
        raise HTTPException(404, f"unknown benchmark {prompt_id}")
    res = recommend(bench["user_id"], bench["request"])
    checks = check_benchmark(bench, res, ds.users[bench["user_id"]])
    return {"benchmark": bench, "checks": checks,
            "passed": sum(1 for c in checks if c["passed"]),
            "total": len(checks), "response": res}
