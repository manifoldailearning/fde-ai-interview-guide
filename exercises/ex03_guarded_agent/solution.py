"""Reference solution: a tool-calling agent with guardrails."""

import json
from dataclasses import dataclass

ALLOWED = {
    "lookup_order",
    "issue_refund",
    "cancel_order",
    "escalate",
}
MAX_STEPS = 6
REFUND_LIMIT = 200.0
HANDOFF = (
    "Thanks for your patience. A specialist will review this"
    " and reply within one business day."
)


@dataclass(frozen=True)
class Outcome:
    status: str
    reply: str
    steps: int
    reason: str = ""


def run_ticket(ticket: dict, backend, planner) -> Outcome:
    history: list[dict] = []
    order = None
    for step in range(1, MAX_STEPS + 1):
        raw = planner.next_action(ticket["text"], history)
        action = _parse(raw)
        if action is None:
            note = "invalid JSON; reply with one JSON object"
            history.append(
                {
                    "tool": None,
                    "args": {},
                    "result": {"error": note},
                }
            )
            continue
        if "final" in action:
            return Outcome("resolved", str(action["final"]), step)
        tool = action.get("tool")
        args = action.get("args") or {}
        if tool not in ALLOWED:
            return _handoff(backend, f"unknown tool {tool}", step)
        if tool == "escalate":
            why = args.get("reason", "model asked")
            return _handoff(backend, why, step)
        blocked = _policy(tool, args, ticket, order)
        if blocked:
            return _handoff(backend, blocked, step)
        result = getattr(backend, tool)(**args)
        if "error" in result:
            return _handoff(backend, result["error"], step)
        if tool == "lookup_order":
            if result["customer_id"] != ticket["customer_id"]:
                why = "order belongs to another customer"
                return _handoff(backend, why, step)
            order = result
        history.append(
            {"tool": tool, "args": args, "result": result}
        )
    return _handoff(backend, "step budget exhausted", MAX_STEPS)


def _parse(raw: str) -> dict | None:
    try:
        action = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return action if isinstance(action, dict) else None


def _policy(tool, args, ticket, order) -> str | None:
    """Return why an action is blocked, or None to allow it."""
    if tool == "lookup_order":
        return None
    if order is None or args.get("order_id") != order["order_id"]:
        return f"{tool} on an order not verified for this ticket"
    if tool == "issue_refund":
        amount = float(args.get("amount", 0))
        room = order["total"] - order["refunded"]
        if amount <= 0 or amount > room:
            return f"refund {amount} exceeds the order balance"
        if amount > REFUND_LIMIT:
            return f"refund {amount} needs human approval"
    return None


def _handoff(backend, reason: str, steps: int) -> Outcome:
    backend.escalate(reason)
    return Outcome("escalated", HANDOFF, steps, reason)
