"""Raw-history extraction + fusion (provenance, contradictions, party size)."""
from app.profile.fusion import (effective_price_sensitivity, fuse)
from app.state import get_dataset

DS = get_dataset()


def test_u01_signals():
    p = fuse(DS.users["U01"])
    assert p.value("avoid_redeye") is True
    assert p.value("direct_preference") == "strong"
    assert p.value("preferred_cabin") == "Business"
    assert p.value("seat_wish") is not None  # aisle/front acknowledged


def test_u02_conditional_redeye_and_budget():
    p = fuse(DS.users["U02"])
    assert p.value("redeye_ok_if_cheaper") is True
    assert p.value("budget_priority") == "high"
    assert p.value("layover_tolerance_minutes") == 420  # "7hr layover to save $120"
    assert p.value("airline_loyalty") == "none"


def test_u03_party_and_baggage():
    p = fuse(DS.users["U03"])
    assert p.party_size == 3  # "traveling w/ 2 kids"
    assert p.value("checked_bags") == 2
    assert p.value("stroller") is True
    assert p.value("dates_school_breaks_only") is True
    assert p.value("avoid_night_departure") is True


def test_u05_money_no_object():
    p = fuse(DS.users["U05"])
    assert p.value("budget_priority") == "none"
    assert effective_price_sensitivity(p) == "none"
    assert p.value("preferred_cabin") == "First"


def test_u06_contradiction_flagged():
    p = fuse(DS.users["U06"])
    assert p.value("budget_priority") == "high"
    assert any("broke student" in c for c in p.contradictions), \
        "age-66 vs broke-student persona contradiction must be flagged"


def test_every_preference_has_provenance():
    for uid in ("U01", "U02", "U03", "U04", "U05", "U06"):
        for pref in fuse(DS.users[uid]).preferences:
            assert pref.source in ("structured", "raw_history", "query", "derived")
            assert pref.evidence
