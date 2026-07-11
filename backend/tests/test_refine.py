"""Conversational refinement: follow-up parsing + end-to-end re-planning."""
from app.nlu.refine_rules import parse_refinement
from app.service import recommend, refine

B01_QUERY = "I need to get from home to Tokyo next month, what do you suggest?"


# ---- parser units ----

def test_parse_cheaper():
    p = parse_refinement("make it cheaper")
    assert p.emphasis == "cheapest"
    assert p.applied


def test_parse_budget_cap():
    p = parse_refinement("keep it under $900 please")
    assert p.budget_cap_pp == 900
    assert any("budget cap" in a for a in p.applied)


def test_parse_budget_cap_with_commas():
    p = parse_refinement("no more than $1,500")
    assert p.budget_cap_pp == 1500


def test_parse_no_redeyes():
    p = parse_refinement("no redeyes")
    assert p.avoid_redeye
    p2 = parse_refinement("avoid red-eyes")
    assert p2.avoid_redeye


def test_parse_direct_only():
    p = parse_refinement("direct only")
    assert p.direct_only
    assert parse_refinement("no connections").direct_only


def test_parse_cabin():
    assert parse_refinement("switch to business class").cabin == "Business"
    assert parse_refinement("premium economy is fine").cabin == "Premium Economy"
    # bare "first" must NOT match a cabin ("the first option")
    assert parse_refinement("make the first one cheaper").cabin == ""


def test_parse_shift_days():
    assert parse_refinement("a week later").shift_days == 7
    assert parse_refinement("3 days earlier").shift_days == -3


def test_parse_layover_cap():
    p = parse_refinement("layovers under 4h")
    assert p.max_layover_minutes == 240


# ---- end-to-end ----

def test_refine_cheaper_reorders_to_cheapest():
    base = recommend("U01", B01_QUERY)
    refined = refine("U01", B01_QUERY, "make it cheaper")
    assert refined["refinement"]["applied"]
    base_price = base["recommendations"][0]["total_price_pp"]
    ref_price = refined["recommendations"][0]["total_price_pp"]
    cheapest = refined["anchors"]["cheapest"]["total_price_pp"]
    assert ref_price <= base_price
    assert ref_price == cheapest  # optimizing for price → pick IS the cheapest


def test_refine_budget_cap_filters():
    refined = refine("U01", B01_QUERY, "under $1,300")
    assert all(o["total_price_pp"] <= 1300 for o in refined["recommendations"])


def test_refine_impossible_cap_never_dead_ends():
    refined = refine("U01", B01_QUERY, "under $5")
    assert refined["recommendations"], "refine must never return zero options"
    assert any("no itinerary qualifies" in a for a in refined["refinement"]["applied"])


def test_refine_direct_only():
    refined = refine("U02", "Find me the best way to do a London + Paris + Rome trip in one journey.",
                     "no redeyes")
    assert refined["recommendations"]
    assert refined["refinement"]["followup"] == "no redeyes"
