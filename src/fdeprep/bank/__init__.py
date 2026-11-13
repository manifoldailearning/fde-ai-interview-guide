"""The question bank: 100 interview questions by round."""

import json
import random
from dataclasses import dataclass
from pathlib import Path

ROUNDS = (
    "screen",
    "case",
    "build",
    "debug",
    "design",
    "behavioral",
    "roleplay",
)


@dataclass(frozen=True)
class Question:
    id: str
    round: str
    prompt: str
    signals: tuple[str, ...]
    follow_up: str


def load() -> list[Question]:
    path = Path(__file__).with_name("questions.json")
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        Question(
            q["id"],
            q["round"],
            q["prompt"],
            tuple(q["signals"]),
            q["follow_up"],
        )
        for q in raw
    ]


def drill(
    round_: str | None = None, n: int = 3, seed: int | None = None
) -> list[Question]:
    """Pick n questions, from one round or from all of them."""
    pool = [q for q in load() if round_ in (None, q.round)]
    if not pool:
        raise ValueError(f"no questions for round {round_!r}")
    rng = random.Random(seed)
    return rng.sample(pool, min(n, len(pool)))


def find(qid: str) -> Question:
    for q in load():
        if q.id == qid.upper():
            return q
    raise KeyError(f"no question {qid!r}")
