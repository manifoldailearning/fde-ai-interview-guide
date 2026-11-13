import json

from fdeprep.sim.backend import demo_orders
from fdeprep.sim.clock import VirtualClock
from fdeprep.sim.context_model import (
    ABSTAIN,
    GUESS,
    ContextModel,
    Passage,
)
from fdeprep.sim.meridian import DOCS, GOLDEN
from fdeprep.sim.planner import Planner
from fdeprep.sim.ticket_api import (
    CLIENT_ID,
    CLIENT_SECRET,
    FakeTicketAPI,
)


def test_context_model_guesses_without_passages():
    reply = ContextModel().answer("How long?", [])
    assert reply.text == GUESS and reply.cited == ()


def test_context_model_abstains_on_zero_overlap():
    p = Passage("x", "Bananas are yellow.")
    assert (
        ContextModel().answer("Tax rates?", [p]).text == ABSTAIN
    )


def test_context_model_obeys_planted_instructions():
    vendor = next(d for d in DOCS if d.source == "vendor-upload")
    p = Passage(vendor.doc_id, vendor.text)
    reply = ContextModel().answer("anything", [p])
    assert "24 hours" in reply.text


def test_golden_set_shape():
    assert len(GOLDEN) == 31
    ids = {d.doc_id for d in DOCS}
    for g in GOLDEN:
        assert g.doc_id is None or g.doc_id in ids


def test_planner_returns_broken_json_once_for_glitch():
    p = Planner()
    raw = p.next_action("#glitch ORD-1005", [])
    try:
        json.loads(raw)
        raise AssertionError("expected invalid JSON")
    except json.JSONDecodeError:
        pass
    retry = [{"tool": None, "args": {}, "result": {}}]
    assert json.loads(p.next_action("#glitch ORD-1005", retry))


def test_backend_does_not_enforce_policy():
    b = demo_orders()
    assert b.issue_refund("ORD-1001", 9999)["ok"]


def test_api_rate_limits_and_expires_tokens():
    clock = VirtualClock()
    api = FakeTicketAPI(clock)
    tok = api.request(
        "POST",
        "/oauth/token",
        body={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).body["access_token"]
    h = {"Authorization": f"Bearer {tok}"}
    codes = [
        api.request("GET", "/tickets", h, {"limit": 5}).status
        for _ in range(6)
    ]
    assert codes[-1] == 429
    clock.sleep(20)
    assert api.request("GET", "/tickets", h).status == 401


def test_virtual_clock_rejects_negative_sleep():
    try:
        VirtualClock().sleep(-1)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
