"""Reference solution: grounded answers with citations."""

import re
from dataclasses import dataclass

from fdeprep.retrieval import BM25Index
from fdeprep.sim.context_model import ABSTAIN, Passage
from fdeprep.text import tokenize

TRUSTED_SOURCES = {"handbook"}
MIN_SCORE = 2.0
MIN_COVERAGE = 0.5
TOP_K = 3
_INSTRUCTION = re.compile(
    r"ignore (all )?previous instructions|disregard .*rules",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Answer:
    text: str
    citations: tuple[str, ...]
    abstained: bool


def _abstain() -> Answer:
    return Answer(ABSTAIN, (), True)


class Assistant:
    def __init__(self, docs, model) -> None:
        self.model = model
        self.docs = {
            d.doc_id: d
            for d in docs
            if d.source in TRUSTED_SOURCES
            and not _INSTRUCTION.search(d.text)
        }
        self.index = BM25Index(
            {
                i: f"{d.title}. {d.text}"
                for i, d in self.docs.items()
            }
        )

    def answer(self, question: str) -> Answer:
        hits = self.index.search(question, k=TOP_K)
        if not hits or hits[0][1] < MIN_SCORE:
            return _abstain()
        if (
            _coverage(question, self.docs[hits[0][0]])
            < MIN_COVERAGE
        ):
            return _abstain()
        passages = [
            Passage(i, self.docs[i].text) for i, _ in hits
        ]
        reply = self.model.answer(question, passages)
        shown = {p.doc_id for p in passages}
        if not reply.cited or not set(reply.cited) <= shown:
            return _abstain()
        return Answer(reply.text, reply.cited, False)


def _coverage(question: str, doc) -> float:
    wanted = set(tokenize(question))
    have = set(tokenize(f"{doc.title} {doc.text}"))
    return len(wanted & have) / max(len(wanted), 1)
