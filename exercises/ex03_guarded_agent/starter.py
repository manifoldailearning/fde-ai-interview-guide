"""ex03 starter: implement run_ticket (see brief.md)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Outcome:
    status: str  # "resolved" or "escalated"
    reply: str  # what the customer will read
    steps: int  # model calls used
    reason: str = ""


def run_ticket(ticket: dict, backend, planner) -> Outcome:
    raise NotImplementedError("build the agent loop")
