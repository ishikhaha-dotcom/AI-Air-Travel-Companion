"""WayFinder API entrypoint.

Dev:   uvicorn app.main:app --reload --port 8000   (frontend: vite dev on :5173)
Demo:  after `npm run build`, this app also serves the built UI at /.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.routes import router
from .state import get_dataset

app = FastAPI(title="WayFinder — AI Air Travel Companion", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"], allow_headers=["*"],
)
app.include_router(router)


@app.on_event("startup")
def _warm() -> None:
    ds = get_dataset()  # load CSVs + build indices once
    print(ds.qa)


_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if _dist.is_dir():
    app.mount("/", StaticFiles(directory=_dist, html=True), name="ui")
