"""Date resolution + intent parsing against the fixed travel clock (2025-08-01)."""
from app.nlu.dates import resolve_window
from app.nlu.intent_rules import parse_intent
from app.profile.fusion import fuse
from app.state import get_dataset

DS = get_dataset()


def _prof(uid):
    return fuse(DS.users[uid])


def test_next_month_resolves_to_september():
    w = resolve_window("to Tokyo next month", _prof("U01"))
    assert w["start"].date().isoformat() == "2025-09-01"
    assert w["end"].date().isoformat() == "2025-09-30"


def test_summer_narrowed_by_school_holidays_for_u03():
    w = resolve_window("flexible on dates over the summer", _prof("U03"))
    # U03: school holidays jul-aug only; Jun-Jul already past the clock -> August
    assert w["start"].date().month == 8 and w["end"].date().month == 8
    assert any("school" in n for n in w["notes"])


def test_holidays_window():
    w = resolve_window("around the holidays", _prof("U05"))
    assert w["start"].date().isoformat() == "2025-12-15"
    assert w["end"].date().isoformat() == "2026-01-05"


def test_weekday_pattern_tuesday_thursday():
    w = resolve_window("for a Tuesday meeting, back Thursday", _prof("U04"))
    assert w["fixed_pattern"] == {"out_dow": 1, "ret_dow": 3, "arrive_by_hour": 9}


def test_three_weeks_trip_length():
    w = resolve_window("about three weeks of flexibility", _prof("U06"))
    assert w["trip_length_days"] == 21


def test_intent_b01_home_to_tokyo():
    i = parse_intent("I need to get from home to Tokyo next month", _prof("U01"))
    assert i.origin == "CPT" and i.destinations == ["NRT"] and i.trip_type == "one_way"


def test_intent_b02_multicity():
    i = parse_intent("Find me the best way to do a London + Paris + Rome trip in one journey.",
                     _prof("U02"))
    assert i.origin == "MEX" and set(i.destinations) == {"LHR", "CDG", "FCO"}
    assert i.trip_type == "multi_city"


def test_intent_b04_roundtrip_business():
    i = parse_intent("Book me something to New York for a Tuesday meeting, back Thursday.",
                     _prof("U04"))
    assert i.trip_type == "round_trip" and i.destinations == ["JFK"]
    assert i.purpose == "business"


def test_intent_b06_open_ended_asia():
    i = parse_intent("Plan a multi-city Asia trip, I have about three weeks of flexibility.",
                     _prof("U06"))
    assert i.trip_type == "open_ended" and i.region == "asia"
    assert i.trip_length_days == 21
