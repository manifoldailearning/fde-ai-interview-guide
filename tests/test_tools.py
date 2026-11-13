import pytest

from fdeprep import bank, rubric
from fdeprep.cli import main
from fdeprep.estimate import Workload, estimate


def test_bank_has_100_questions_in_known_rounds():
    qs = bank.load()
    assert len(qs) == 100
    assert {q.round for q in qs} == set(bank.ROUNDS)
    assert all(len(q.signals) == 3 for q in qs)


def test_drill_is_reproducible_with_a_seed():
    a = [q.id for q in bank.drill("case", 3, seed=1)]
    b = [q.id for q in bank.drill("case", 3, seed=1)]
    assert a == b and len(set(a)) == 3


def test_rubric_verdicts():
    dims = rubric.DIMENSIONS["debug"]
    assert rubric.score(
        "debug", dict.fromkeys(dims, 4)
    ).label == ("strong")
    mixed = dict.fromkeys(dims, 3) | {"method": 2}
    assert rubric.score("debug", mixed).label == "on the bar"
    weak = dict.fromkeys(dims, 3) | {"severity": 1}
    v = rubric.score("debug", weak)
    assert v.label == "not yet" and v.focus == ("severity",)


def test_rubric_rejects_unknown_dimensions():
    with pytest.raises(ValueError):
        rubric.score("case", {"framing": 3})


def test_estimate_arithmetic():
    w = Workload(400, 20, 3000, 400, 1.0, 4.0)
    out = estimate(w)
    assert out["requests_per_day"] == 8000
    assert out["cost_per_day"] == 36.8
    assert out["cost_per_month"] == 809.6


def test_cli_check_exit_codes(capsys):
    assert main(["check", "ex01", "--solution"]) == 0
    assert main(["check", "ex01"]) == 1
    assert main(["rounds"]) == 0
