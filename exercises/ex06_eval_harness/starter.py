"""ex06 starter: implement grade, evaluate, decide (brief.md)."""

from dataclasses import dataclass, field


@dataclass
class Report:
    name: str
    n: int
    accuracy: float  # correct / n, rounded to 3 places
    answer_rate: float  # answered / n, rounded to 3 places
    unsupported: int  # unanswerable items that got an answer
    injected: int  # replies repeating the planted instruction
    passages_per_question: float  # rounded to 2 places
    by_slice: dict[str, float]  # accuracy per slice
    failures: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Decision:
    ship: bool
    reasons: list[str]


def grade(item, reply) -> bool:
    raise NotImplementedError


def evaluate(service, golden) -> Report:
    raise NotImplementedError


def decide(base: Report, cand: Report) -> Decision:
    raise NotImplementedError
