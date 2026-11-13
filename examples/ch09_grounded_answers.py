"""Chapter 9: the naive path versus the guarded one."""

import textwrap

from _load import solution
from fdeprep.retrieval import BM25Index
from fdeprep.sim.context_model import ContextModel, Passage
from fdeprep.sim.meridian import DOCS

m = solution("ex02")

QUESTIONS = [
    "Within how many days must a claim be filed?",
    "Does Meridian offer pet insurance?",
    "How quickly are claims approved?",
]


def naive(question: str):
    """Top three passages straight to the model, no checks."""
    index = BM25Index({d.doc_id: d.text for d in DOCS})
    by_id = {d.doc_id: d for d in DOCS}
    hits = index.search(question, k=3)
    passages = [Passage(i, by_id[i].text) for i, _ in hits]
    return ContextModel().answer(question, passages)


def show(label: str, text: str, cited) -> None:
    line = f"{label} {text} {list(cited)}"
    print(
        textwrap.fill(
            line,
            62,
            initial_indent="  ",
            subsequent_indent="           ",
        )
    )


def main() -> None:
    bot = m.Assistant(DOCS, ContextModel())
    for q in QUESTIONS:
        n, g = naive(q), bot.answer(q)
        print(f"Q: {q}")
        show("naive:  ", n.text, n.cited)
        show("guarded:", g.text, g.citations)
        print()


if __name__ == "__main__":
    main()
