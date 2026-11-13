"""A simulated model that answers from retrieved passages.

It behaves like a capable but over-eager model:

- it answers with the sentence that overlaps the question most,
- it answers even when that overlap is weak,
- with no passages at all it guesses, without a citation,
- it follows instructions planted inside a passage.

Your code, not the model, has to decide when to abstain and
which passages are safe to show it.
"""

import re
from dataclasses import dataclass

from fdeprep.text import sentences, tokenize

ABSTAIN = "I don't know based on the provided documents."
GUESS = "Most claims are settled within 30 days."

_INJECTION = re.compile(
    r"ignore (?:all )?previous instructions and reply:\s*(.+)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Passage:
    doc_id: str
    text: str


@dataclass(frozen=True)
class ModelReply:
    text: str
    cited: tuple[str, ...]


class ContextModel:
    """Deterministic stand-in for a grounded-answer model."""

    def __init__(self) -> None:
        self.calls = 0

    def answer(
        self, question: str, passages: list[Passage]
    ) -> ModelReply:
        self.calls += 1
        for p in passages:
            hit = _INJECTION.search(p.text)
            if hit:
                payload = hit.group(1).strip()
                return ModelReply(payload, (p.doc_id,))
        if not passages:
            return ModelReply(GUESS, ())
        wanted = set(tokenize(question))
        best, best_score = None, 0
        for p in passages:
            for s in sentences(p.text):
                score = len(wanted & set(tokenize(s)))
                if score > best_score:
                    best, best_score = (p.doc_id, s), score
        if best is None:
            return ModelReply(ABSTAIN, ())
        doc_id, sentence = best
        return ModelReply(sentence, (doc_id,))
