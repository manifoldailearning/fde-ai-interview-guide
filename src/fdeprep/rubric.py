"""This book's self-assessment rubric for mock interviews.

Score each dimension from 1 to 4 after a mock round:
1 = concern, 2 = mixed, 3 = solid, 4 = strong. The verdict is a
practice signal for you. It is not any employer's hiring bar.
"""

from dataclasses import dataclass
from statistics import mean

DIMENSIONS = {
    "screen": ("story", "motivation", "evidence", "clarity"),
    "case": (
        "framing",
        "discovery",
        "metrics",
        "scope",
        "risk",
        "communication",
    ),
    "build": (
        "progress",
        "correctness",
        "judgment",
        "testing",
        "communication",
    ),
    "debug": (
        "method",
        "severity",
        "fix",
        "prevention",
        "communication",
    ),
    "design": (
        "requirements",
        "architecture",
        "trust",
        "operations",
        "tradeoffs",
        "communication",
    ),
    "behavioral": (
        "ownership",
        "specificity",
        "impact",
        "reflection",
        "customer",
    ),
    "roleplay": (
        "listening",
        "clarity",
        "honesty",
        "recommendation",
        "composure",
    ),
}


@dataclass(frozen=True)
class Verdict:
    label: str
    average: float
    focus: tuple[str, ...]


def score(round_: str, scores: dict[str, int]) -> Verdict:
    """Turn dimension scores into a practice verdict.

    strong:     average >= 3.25 and every dimension >= 3
    on the bar: average >= 2.75 and no dimension at 1
    not yet:    anything else
    focus lists the lowest-scoring dimensions to practice next.
    """
    wanted = DIMENSIONS[round_]
    missing = [d for d in wanted if d not in scores]
    extra = [d for d in scores if d not in wanted]
    if missing or extra:
        raise ValueError(f"missing {missing}, unknown {extra}")
    if any(not 1 <= v <= 4 for v in scores.values()):
        raise ValueError("scores must be 1 to 4")
    avg = round(mean(scores.values()), 2)
    low = min(scores.values())
    if avg >= 3.25 and low >= 3:
        label = "strong"
    elif avg >= 2.75 and low >= 2:
        label = "on the bar"
    else:
        label = "not yet"
    focus = tuple(d for d in wanted if scores[d] == low)
    return Verdict(label, avg, focus if low < 4 else ())
