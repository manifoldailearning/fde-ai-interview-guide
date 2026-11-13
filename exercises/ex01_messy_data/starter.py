"""ex01 starter: implement clean and summarize (see brief.md)."""

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

EXPORT = Path(__file__).with_name("tickets_export.csv")


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    created_at: datetime  # naive, UTC
    customer_email: str
    priority: str  # P1..P4
    status: str  # open, pending, resolved, closed
    resolution_min: int | None
    body: str  # emails and phone numbers masked


def load_rows(path: Path = EXPORT) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def clean(rows: list[dict]) -> list[Ticket]:
    raise NotImplementedError


def summarize(tickets: list[Ticket]) -> dict:
    raise NotImplementedError
