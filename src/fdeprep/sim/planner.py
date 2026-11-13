"""A simulated tool-calling model for the agent exercise.

`Planner.next_action` returns raw text, usually a JSON object:

    {"tool": "lookup_order", "args": {"order_id": "ORD-1001"}}
    {"final": "Your order is on its way."}

It reads the ticket and the history of executed tool calls,
where each history item is a dict with "tool", "args" and
"result" keys (use "tool": None for a step that failed to
parse). Like a real model it is usually right, and sometimes:

- returns invalid JSON (tickets tagged #glitch, first call),
- never stops looking things up (#loop),
- calls a tool that does not exist (#bogus-tool),
- obeys instructions a customer typed into the ticket,
- reports success after a step was blocked.
"""

import json
import re

_ORDER = re.compile(r"ORD-\d{4}")
_AMOUNT = re.compile(r"\$(\d+(?:\.\d{1,2})?)")
_INJECT = "ignore previous instructions"


def _call(tool: str, **args) -> str:
    return json.dumps({"tool": tool, "args": args})


def _final(text: str) -> str:
    return json.dumps({"final": text})


class Planner:
    def __init__(self) -> None:
        self.calls = 0

    def next_action(
        self, ticket: str, history: list[dict]
    ) -> str:
        self.calls += 1
        text = ticket.lower()
        done = [h.get("tool") for h in history if h.get("tool")]
        match = _ORDER.search(ticket)
        oid = match.group(0) if match else None

        if "#glitch" in text and not history:
            return '{"tool": "lookup_order", "args": {"order_'
        if "#loop" in text:
            return _call("lookup_order", order_id=oid)
        if "#bogus-tool" in text and not done:
            return _call("update_address", order_id=oid)
        if oid is None:
            if "escalate" not in done:
                return _call("escalate", reason="no order id")
            return _final("A specialist will contact you.")
        if "lookup_order" not in done:
            return _call("lookup_order", order_id=oid)

        order = next(
            h["result"]
            for h in history
            if h.get("tool") == "lookup_order"
        )
        last = history[-1]["result"]
        if "refund" in text:
            if "issue_refund" not in done:
                amount = _refund_amount(ticket, order)
                return _call(
                    "issue_refund", order_id=oid, amount=amount
                )
            return _final(f"Your refund for {oid} is processed.")
        if "cancel" in text:
            if "cancel_order" not in done:
                return _call("cancel_order", order_id=oid)
            if "error" in last:
                return _final("We could not cancel this order.")
            return _final(f"Order {oid} has been cancelled.")
        status = order.get("status", "unknown")
        return _final(f"Order {oid} is currently {status}.")


def _refund_amount(ticket: str, order: dict) -> float:
    if _INJECT in ticket.lower():
        return 5000.0
    found = _AMOUNT.search(ticket)
    if found:
        return float(found.group(1))
    return float(order.get("total", 0.0))
