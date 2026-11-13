"""Checks for ex05. Each receives your module."""

from fdeprep.sim.clock import VirtualClock
from fdeprep.sim.ticket_api import (
    CLIENT_ID,
    CLIENT_SECRET,
    FakeTicketAPI,
)


def _setup(mod):
    clock = VirtualClock()
    api = FakeTicketAPI(clock)
    client = mod.TicketClient(
        api, clock, CLIENT_ID, CLIENT_SECRET
    )
    return clock, api, client


def check_fetches_every_ticket_exactly_once(mod):
    _, api, client = _setup(mod)
    tickets = client.fetch_all()
    ids = [t["id"] for t in tickets]
    assert len(ids) == len(set(ids)), "duplicate tickets"
    assert len(ids) == len(api.tickets), f"got {len(ids)}"


def check_respects_page_size_limit(mod):
    _, api, client = _setup(mod)
    client.fetch_all()
    assert api.status_counts.get(400, 0) == 0, (
        "asked for too much"
    )


def check_backs_off_when_rate_limited(mod):
    clock, api, client = _setup(mod)
    client.fetch_all()
    limited = api.status_counts.get(429, 0)
    assert limited <= 3, f"hit the rate limit {limited} times"
    assert clock.slept > 0, "never waited"


def check_recovers_from_token_expiry(mod):
    clock, api, client = _setup(mod)
    client.fetch_all()
    clock.sleep(60)
    note = client.add_note("T0001", "Customer called back.")
    assert note["ticket_id"] == "T0001"


def check_note_is_written_once_despite_timeout(mod):
    _, api, client = _setup(mod)
    client.add_note("T0002", "Escalated to carrier.")
    written = [n for n in api.notes if n["ticket_id"] == "T0002"]
    assert len(written) == 1, f"{len(written)} copies written"


def check_does_not_retry_a_missing_ticket(mod):
    _, api, client = _setup(mod)
    client.fetch_all()
    before = api.requests
    try:
        client.add_note("T9999", "hello")
    except Exception:
        pass
    else:
        raise AssertionError("a 404 must raise")
    assert api.requests - before <= 2, "retried a 404"
