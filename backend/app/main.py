"""WayFinder API entrypoint.

Dev:   uvicorn app.main:app --reload --port 8000   (frontend: vite dev on :5173)
Demo:  after `npm run build`, this app also serves the built UI at /.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.routes import router
from .state import get_dataset

app = FastAPI(title="WayFinder — AI Air Travel Companion", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"], allow_headers=["*"],
)
app.include_router(router)


@app.middleware("http")
async def _cache_headers(request: Request, call_next):
    """index.html has no content hash in its filename, so without an explicit
    no-cache directive a browser's heuristic caching can serve a stale page
    (and therefore a stale JS bundle reference) after a rebuild. Vite's
    /assets/* files ARE content-hashed — a new build always gets a new
    filename — so those are safe to cache aggressively forever."""
    response = await call_next(request)
    if request.url.path.startswith("/assets/"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    elif request.url.path.startswith("/api/"):
        pass
    else:
        response.headers["Cache-Control"] = "no-cache"
    return response


@app.on_event("startup")
def _warm() -> None:
    ds = get_dataset()  # load CSVs + build indices once
    print(ds.qa)


_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if _dist.is_dir():
    app.mount("/", StaticFiles(directory=_dist, html=True), name="ui")
