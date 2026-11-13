"""Find exercises, load your code and run checks against it."""

import importlib.util
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path

EXERCISES = {
    "ex01": (
        "ex01_messy_data",
        "Clean a customer's ticket export",
    ),
    "ex02": ("ex02_grounded_answers", "Grounded answers, cited"),
    "ex03": (
        "ex03_guarded_agent",
        "A tool-calling agent, guarded",
    ),
    "ex04": ("ex04_debug_pipeline", "Debug a broken AI pipeline"),
    "ex05": ("ex05_api_client", "A client for a hostile API"),
    "ex06": ("ex06_eval_harness", "Evaluate, then decide"),
}


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


def exercises_root() -> Path:
    repo = Path(__file__).resolve().parents[2] / "exercises"
    if repo.is_dir():
        return repo
    return Path.cwd() / "exercises"


def exercise_dir(key: str) -> Path:
    if key not in EXERCISES:
        raise KeyError(f"unknown exercise {key!r}")
    return exercises_root() / EXERCISES[key][0]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_checks(key: str, target: str = "starter") -> list:
    """Run an exercise's checks against starter.py or solution.py.

    Each check_* function in checks.py receives your module and
    fails by raising. A check that crashes counts as a failure,
    with the last line of the traceback as the detail.
    """
    folder = exercise_dir(key)
    module = load(folder / f"{target}.py", f"{key}_{target}")
    checks = load(folder / "checks.py", f"{key}_checks")
    names = sorted(
        n for n in dir(checks) if n.startswith("check_")
    )
    results = []
    for name in names:
        try:
            getattr(checks, name)(module)
            results.append(CheckResult(name, True))
        except Exception as exc:
            detail = str(exc) or type(exc).__name__
            if not isinstance(exc, AssertionError):
                tb = traceback.format_exception_only(exc)
                detail = tb[-1].strip()
            results.append(CheckResult(name, False, detail))
    return results
