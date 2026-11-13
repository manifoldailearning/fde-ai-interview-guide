"""Checks for ex03. Each receives your module."""

import importlib.util
from pathlib import Path

from fdeprep.sim.backend import demo_orders
from fdeprep.sim.planner import Planner

_spec = importlib.util.spec_from_file_location(
    "ex03_tickets", Path(__file__).with_name("tickets.py")
)
_tickets = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_tickets)
TICKETS, EXPECTED = _tickets.TICKETS, _tickets.EXPECTED


def _run_all(mod):
    backend, planner = demo_orders(), Planner()
    outcomes = {}
    for t in TICKETS:
        before = planner.calls
        out = mod.run_ticket(t, backend, planner)
        outcomes[t["id"]] = (out, planner.calls - before)
    return backend, outcomes


def check_each_ticket_ends_in_the_right_state(mod):
    _, outcomes = _run_all(mod)
    for tid, (out, _) in outcomes.items():
        assert out.status == EXPECTED[tid], (
            f"{tid}: {out.status}, expected {EXPECTED[tid]}"
        )


def check_only_safe_side_effects_happen(mod):
    backend, _ = _run_all(mod)
    money = [
        e for e in backend.log if e[0] in ("refund", "cancel")
    ]
    assert money == [
        ("refund", "ORD-1002", 40.0),
        ("cancel", "ORD-1004"),
    ], f"unexpected side effects: {money}"


def check_step_budget_is_enforced(mod):
    _, outcomes = _run_all(mod)
    for tid, (out, calls) in outcomes.items():
        assert calls <= 6, f"{tid} made {calls} model calls"
        assert out.steps <= 6, tid


def check_every_escalation_reaches_a_human(mod):
    backend, outcomes = _run_all(mod)
    queued = [e for e in backend.log if e[0] == "escalate"]
    escalated = [
        o for o, _ in outcomes.values() if o.status == "escalated"
    ]
    assert len(queued) == len(escalated), (
        f"{len(escalated)} escalated, {len(queued)} queued"
    )


def check_escalated_replies_claim_nothing(mod):
    _, outcomes = _run_all(mod)
    for tid, (out, _) in outcomes.items():
        if out.status != "escalated":
            continue
        text = out.reply.lower()
        for claim in ("processed", "cancelled", "refunded"):
            assert claim not in text, (
                f"{tid} reply claims {claim}"
            )
