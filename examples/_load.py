"""Load an exercise's reference solution for the examples."""

from fdeprep.exercise import exercise_dir, load


def solution(key: str):
    path = exercise_dir(key) / "solution.py"
    return load(path, f"{key}_solution")
