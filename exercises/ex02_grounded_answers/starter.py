"""ex02 starter: implement Assistant.answer (see brief.md)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Answer:
    text: str
    citations: tuple[str, ...]
    abstained: bool


class Assistant:
    def __init__(self, docs, model) -> None:
        self.docs = docs
        self.model = model

    def answer(self, question: str) -> Answer:
        raise NotImplementedError("build the answer path")
