"""Hard-constraint invariants, relaxation transparency, weight mapping."""
from app.nlu.intent_rules import parse_intent
from app.profile.fusion import fuse
from app.ranking.scorer import score_options
from app.ranking.weights import derive_weights
from app.search.relaxation import search_with_relaxation
from app.state import get_dataset

DS = get_dataset()


def _run(uid: str, query: str):
    prof = fuse(DS.users[uid])
    intent = parse_intent(query, prof)
    outcome = search_with_relaxation(DS, intent, prof)
    scored, w, notes = score_options(outcome.options, prof, intent)
    return prof, intent, outcome, scored, w, notes


def test_b01_constraint_invariant():
    """No result may violate seats/layover unless a relaxation step says so."""
    prof, intent, outcome, scored, _, _ = _run(
        "U01", "I need to get from home to Tokyo next month, what do you suggest?")
    assert scored, "B01 must return options"
    cap = prof.value("max_layover_minutes")
    if not outcome.relaxations:
        for o in scored:
            for leg in o.legs:
                assert leg.in_ticket_layover <= cap
                assert leg.seats_min >= prof.party_size
    assert all(o.legs[0].origin == "CPT" for o in scored)


def test_b03_party_size_seats():
    prof, intent, outcome, scored, _, _ = _run(
        "U03", "Cheapest option to Bali, I'm flexible on dates over the summer.")
    assert intent.party_size == 3
    for o in scored:
        assert o.seats_min >= 3, "family of 3 must never be offered <3 seats"


def test_b05_trap_relaxation_is_narrated():
    """LIS→SYD: no direct exists + 90-min cap -> must relax AND say so."""
    prof, intent, outcome, scored, _, _ = _run(
        "U05", "I want to visit Sydney around the holidays — what should I expect?")
    assert scored, "B05 must still produce an option"
    assert outcome.relaxations, "constraint relaxation must be recorded"
    assert any("direct" in f.lower() for f in outcome.route_facts), \
        "the no-direct-service route fact must be surfaced"


def test_weight_mapping_follows_blueprint_table():
    prof1 = fuse(DS.users["U01"])  # price_sensitivity=low, direct=strong
    i1 = parse_intent("to Tokyo next month", prof1)
    w1, _ = derive_weights(prof1, i1)
    # low->0.15 price, strong->0.35 convenience, then renormalized to sum 1
    assert abs(sum(w1.values()) - 1.0) < 1e-6
    assert w1["convenience"] > w1["price"], "U01: convenience must outweigh price"

    prof2 = fuse(DS.users["U02"])  # price_sensitivity=high, direct=none
    i2 = parse_intent("cheapest trip to London", prof2)
    w2, _ = derive_weights(prof2, i2)
    assert w2["price"] > 0.5, "U02 + 'cheapest' emphasis: price must dominate"


def test_scores_and_breakdown_consistent():
    _, _, _, scored, w, _ = _run(
        "U01", "I need to get from home to Tokyo next month, what do you suggest?")
    for o in scored:
        assert abs(sum(o.breakdown.values()) - o.fit_score) < 0.5
        assert 0 <= o.fit_score <= 100
