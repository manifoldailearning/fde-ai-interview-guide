"""Checks for ex06. Each receives your module."""

from fdeprep.sim.meridian import GOLDEN, INJECTED_PAYLOAD
from fdeprep.sim.systems import Reply, baseline, candidate

BY_ID = {g.qid: g for g in GOLDEN}


def check_grade_follows_the_rules(mod):
    q01, q11, q10 = BY_ID["q01"], BY_ID["q11"], BY_ID["q10"]
    good = Reply(
        "Filed within 60 days.", ("claims-filing",), False
    )
    wrong_doc = Reply(
        "Filed within 60 days.", ("appeals",), False
    )
    abstain = Reply("I don't know.", (), True)
    hijacked = Reply(f"Claims {INJECTED_PAYLOAD}.", ("x",), False)
    assert mod.grade(q01, good) is True
    assert mod.grade(q01, wrong_doc) is False
    assert mod.grade(q01, abstain) is False
    assert mod.grade(q11, abstain) is True
    assert mod.grade(q11, good) is False
    assert mod.grade(q10, hijacked) is False


def check_baseline_report(mod):
    r = mod.evaluate(baseline(), GOLDEN)
    assert r.n == 31
    assert r.accuracy == 0.871, r.accuracy
    assert r.answer_rate == 0.806, r.answer_rate
    assert (r.unsupported, r.injected) == (2, 0)
    assert r.by_slice["claims"] == 0.778, r.by_slice
    assert r.failures == ["q22", "q24", "q27", "q30"], r.failures


def check_candidate_report(mod):
    r = mod.evaluate(candidate(), GOLDEN)
    assert r.accuracy == 0.742, r.accuracy
    assert r.answer_rate == 0.968, r.answer_rate
    assert r.unsupported == 6, r.unsupported
    assert r.passages_per_question == 0.97
    assert r.by_slice["unanswerable"] == 0.143, r.by_slice


def check_decision_holds_the_candidate(mod):
    base = mod.evaluate(baseline(), GOLDEN)
    cand = mod.evaluate(candidate(), GOLDEN)
    d = mod.decide(base, cand)
    assert d.ship is False
    text = " ".join(d.reasons)
    assert "unsupported" in text and "accuracy" in text, d.reasons


def check_decision_ships_an_equal_build(mod):
    base = mod.evaluate(baseline(), GOLDEN)
    again = mod.evaluate(baseline(), GOLDEN)
    assert mod.decide(base, again).ship is True
