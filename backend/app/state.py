"""Lazy singleton Dataset: the only global state in the app."""
from __future__ import annotations

from dataclasses import dataclass

from .data.baselines import Baselines
from .data.indices import build_origin_index, build_route_index
from .data.loader import load_benchmarks, load_flights, load_users, qa_report
from .data.models import Flight, User


@dataclass
class Dataset:
    flights: list[Flight]
    users: dict[str, User]
    benchmarks: list[dict]
    by_route: dict[tuple[str, str], list[Flight]]
    from_origin: dict[str, list[Flight]]
    baselines: Baselines
    qa: str


_dataset: Dataset | None = None


def get_dataset() -> Dataset:
    global _dataset
    if _dataset is None:
        flights = load_flights()
        users = load_users()
        benches = load_benchmarks()
        _dataset = Dataset(
            flights=flights,
            users=users,
            benchmarks=benches,
            by_route=build_route_index(flights),
            from_origin=build_origin_index(flights),
            baselines=Baselines(flights),
            qa=qa_report(flights, users, benches),
        )
    return _dataset
