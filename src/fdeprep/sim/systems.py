"""Two versions of Meridian's answer service, for evaluation.

`baseline()` is the cautious build: trusted sources only, three
passages, and two abstention gates. `candidate()` is the change
a stakeholder asked for after a demo where the assistant said
"I don't know" too often: one passage (cheaper) and no coverage
gate (answers more questions). Which one should ship is what an
evaluation has to decide.
"""

from dataclasses import dataclass

from fdeprep.retrieval import BM25Index
from fdeprep.sim.context_model import (
    ABSTAIN,
    ContextModel,
    Passage,
)
from fdeprep.sim.meridian import DOCS
from fdeprep.text import tokenize


@dataclass(frozen=True)
class Reply:
    text: str
    cited: tuple[str, ...]
    abstained: bool


@dataclass(frozen=True)
class Config:
    name: str
    top_k: int
    min_score: float
    min_coverage: float


class AnswerService:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.model = ContextModel()
        self.passages_sent = 0
        self.docs = {
            d.doc_id: d for d in DOCS if d.source == "handbook"
        }
        self.index = BM25Index(
            {
                i: f"{d.title}. {d.text}"
                for i, d in self.docs.items()
            }
        )

    def answer(self, question: str) -> Reply:
        cfg = self.config
        hits = self.index.search(question, k=cfg.top_k)
        if not hits or hits[0][1] < cfg.min_score:
            return Reply(ABSTAIN, (), True)
        top = self.docs[hits[0][0]]
        if _coverage(question, top) < cfg.min_coverage:
            return Reply(ABSTAIN, (), True)
        passages = [
            Passage(i, self.docs[i].text) for i, _ in hits
        ]
        self.passages_sent += len(passages)
        out = self.model.answer(question, passages)
        abstained = not out.cited
        return Reply(out.text, out.cited, abstained)


def _coverage(question: str, doc) -> float:
    wanted = set(tokenize(question))
    have = set(tokenize(f"{doc.title} {doc.text}"))
    return len(wanted & have) / max(len(wanted), 1)


def baseline() -> AnswerService:
    return AnswerService(Config("v1-baseline", 3, 2.0, 0.5))


def candidate() -> AnswerService:
    return AnswerService(Config("v2-candidate", 1, 0.0, 0.0))
