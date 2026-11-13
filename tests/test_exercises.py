import pytest

from fdeprep.exercise import EXERCISES, run_checks


@pytest.mark.parametrize("key", sorted(EXERCISES))
def test_reference_solution_passes_every_check(key):
    results = run_checks(key, "solution")
    failed = [(r.name, r.detail) for r in results if not r.ok]
    assert results and not failed


@pytest.mark.parametrize("key", sorted(EXERCISES))
def test_starter_does_not_pass_yet(key):
    results = run_checks(key, "starter")
    assert any(not r.ok for r in results)


def test_debug_starter_fails_every_check():
    results = run_checks("ex04", "starter")
    assert not any(r.ok for r in results)
