"""Checks for ex02. Each receives your module."""

from fdeprep.sim.context_model import ContextModel
from fdeprep.sim.meridian import DOCS, GOLDEN, INJECTED_PAYLOAD

CHECKED = {f"q{i:02d}" for i in range(1, 14)} | {"q31"}
ITEMS = [g for g in GOLDEN if g.qid in CHECKED]


def _assistant(mod):
    return mod.Assistant(DOCS, ContextModel())


def check_answers_with_the_right_citation(mod):
    bot = _assistant(mod)
    for item in ITEMS:
        if item.doc_id is None:
            continue
        got = bot.answer(item.question)
        assert not got.abstained, f"{item.qid} abstained"
        assert got.citations == (item.doc_id,), (
            f"{item.qid} cited {got.citations}"
        )
        assert item.must_contain in got.text, (
            f"{item.qid} answer misses {item.must_contain!r}"
        )


def check_abstains_when_handbook_is_silent(mod):
    bot = _assistant(mod)
    for item in ITEMS:
        if item.slice != "unanswerable":
            continue
        got = bot.answer(item.question)
        assert got.abstained, f"{item.qid} answered: {got.text}"
        assert got.citations == (), f"{item.qid} cites on abstain"


def check_never_repeats_planted_instructions(mod):
    bot = _assistant(mod)
    for item in ITEMS:
        if item.slice != "adversarial":
            continue
        got = bot.answer(item.question)
        assert INJECTED_PAYLOAD not in got.text, (
            f"{item.qid} repeated the vendor instruction"
        )
        assert "vendor-note" not in got.citations


def check_citations_are_real_documents(mod):
    bot = _assistant(mod)
    known = {d.doc_id for d in DOCS}
    for item in ITEMS:
        got = bot.answer(item.question)
        assert set(got.citations) <= known, item.qid
