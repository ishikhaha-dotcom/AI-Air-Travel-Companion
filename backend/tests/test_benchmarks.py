"""End-to-end: every benchmark prompt must verify all expected behaviors
(the same checks the self-grading harness runs)."""
import pytest

from app.service import recommend
from app.state import get_dataset
from benchmark.run_benchmarks import check_benchmark

DS = get_dataset()


@pytest.mark.parametrize("bench", DS.benchmarks, ids=[b["prompt_id"] for b in DS.benchmarks])
def test_benchmark_all_behaviors(bench):
    res = recommend(bench["user_id"], bench["request"])
    checks = check_benchmark(bench, res, DS.users[bench["user_id"]])
    failed = [c for c in checks if not c["passed"]]
    assert not failed, f"{bench['prompt_id']}: {[c['behavior'] for c in failed]}"
    assert res["recommendations"], f"{bench['prompt_id']} returned no recommendations"
    assert res["narrative"], "narrative must never be empty"
