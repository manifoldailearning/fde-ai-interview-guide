"""Checks for ex01. Each receives your module."""

import re
from datetime import datetime


def _tickets(mod):
    return {t.ticket_id: t for t in mod.clean(mod.load_rows())}


def check_duplicates_keep_the_latest_update(mod):
    t = _tickets(mod)
    assert len(t) == 16, f"{len(t)} tickets after dedup"
    assert t["T-002"].resolution_min == 235
    assert t["T-004"].status == "resolved"


def check_every_date_format_parses(mod):
    t = _tickets(mod)
    want = {
        "T-002": datetime(2026, 3, 2, 10, 5),
        "T-003": datetime(2026, 3, 2, 11, 20),
        "T-004": datetime(2026, 3, 3, 8, 0),
        "T-007": datetime(2026, 3, 4, 19, 5),
        "T-009": datetime(2026, 3, 5, 18, 0),
    }
    for tid, when in want.items():
        assert t[tid].created_at == when, (tid, t[tid].created_at)


def check_fields_are_normalized(mod):
    t = _tickets(mod)
    assert t["T-001"].customer_email == "asha.rao@example.com"
    assert t["T-002"].customer_email == "ben@corvane.example"
    got = {
        k: t[k].priority
        for k in ("T-006", "T-008", "T-010", "T-013")
    }
    assert got == {
        "T-006": "P2",
        "T-008": "P3",
        "T-010": "P1",
        "T-013": "P4",
    }, got
    assert t["T-006"].status == "resolved"


def check_resolution_becomes_minutes(mod):
    t = _tickets(mod)
    got = {
        k: t[k].resolution_min
        for k in ("T-001", "T-005", "T-007", "T-010", "T-015")
    }
    assert got == {
        "T-001": 105,
        "T-005": None,
        "T-007": 55,
        "T-010": 1440,
        "T-015": 240,
    }, got


def check_personal_data_is_masked(mod):
    for ticket in _tickets(mod).values():
        assert "@" not in ticket.body, ticket.ticket_id
        assert not re.search(r"\d{4}[\s-]?\d{4}", ticket.body), (
            ticket.ticket_id
        )


def check_summary_matches_a_hand_count(mod):
    got = mod.summarize(mod.clean(mod.load_rows()))
    assert got == {
        "tickets": 16,
        "by_status": {
            "closed": 4,
            "open": 3,
            "pending": 1,
            "resolved": 8,
        },
        "median_minutes": {
            "P1": 130,
            "P2": 90,
            "P3": 1080,
            "P4": 20,
        },
    }, got
