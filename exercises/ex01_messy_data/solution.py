"""Reference solution: clean a customer's ticket export."""

import csv
import re
import statistics
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

EXPORT = Path(__file__).with_name("tickets_export.csv")

PRIORITY = {
    "p1": "P1",
    "1": "P1",
    "urgent": "P1",
    "critical": "P1",
    "p2": "P2",
    "2": "P2",
    "high": "P2",
    "p3": "P3",
    "3": "P3",
    "medium": "P3",
    "normal": "P3",
    "": "P3",
    "p4": "P4",
    "4": "P4",
    "low": "P4",
}
STATUS = {
    "open": "open",
    "pending": "pending",
    "resolved": "resolved",
    "solved": "resolved",
    "closed": "closed",
}
FORMATS = (
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M:%SZ",
    "%d/%m/%Y %H:%M",
    "%b %d, %Y %I:%M %p",
)
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(\.[\w-]+)+")
_PHONE = re.compile(r"\+?\d[\d\s-]{8,}\d")
_DURATION = re.compile(r"^(?:(\d+)h)?\s*(?:(\d+)m)?$")


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    created_at: datetime
    customer_email: str
    priority: str
    status: str
    resolution_min: int | None
    body: str


def load_rows(path: Path = EXPORT) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_time(value: str) -> datetime:
    value = value.strip()
    if value.isdigit():
        return datetime.fromtimestamp(int(value), UTC).replace(
            tzinfo=None
        )
    for fmt in FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"unrecognized timestamp {value!r}")


def parse_minutes(value: str) -> int | None:
    value = value.strip().lower()
    if value in ("", "n/a"):
        return None
    if value.isdigit():
        return int(value)
    m = _DURATION.match(value)
    if not m or not any(m.groups()):
        raise ValueError(f"unrecognized duration {value!r}")
    hours, minutes = (int(g or 0) for g in m.groups())
    return hours * 60 + minutes


def mask(text: str) -> str:
    text = _EMAIL.sub("[email]", text)
    return _PHONE.sub("[phone]", text)


def clean(rows: list[dict]) -> list[Ticket]:
    latest: dict[str, tuple[datetime, dict]] = {}
    for row in rows:
        updated = parse_time(row["updated_at"])
        tid = row["ticket_id"].strip()
        if tid not in latest or updated > latest[tid][0]:
            latest[tid] = (updated, row)
    tickets = []
    for tid, (_, row) in sorted(latest.items()):
        tickets.append(
            Ticket(
                ticket_id=tid,
                created_at=parse_time(row["created_at"]),
                customer_email=row["customer_email"]
                .strip()
                .lower(),
                priority=PRIORITY[
                    row["priority"].strip().lower()
                ],
                status=STATUS[row["status"].strip().lower()],
                resolution_min=parse_minutes(row["resolution"]),
                body=mask(row["body"]),
            )
        )
    return tickets


def summarize(tickets: list[Ticket]) -> dict:
    by_status: dict[str, int] = {}
    durations: dict[str, list[int]] = {}
    for t in tickets:
        by_status[t.status] = by_status.get(t.status, 0) + 1
        done = t.status in ("resolved", "closed")
        if done and t.resolution_min is not None:
            durations.setdefault(t.priority, []).append(
                t.resolution_min
            )
    return {
        "tickets": len(tickets),
        "by_status": dict(sorted(by_status.items())),
        "median_minutes": {
            p: statistics.median(v)
            for p, v in sorted(durations.items())
        },
    }
