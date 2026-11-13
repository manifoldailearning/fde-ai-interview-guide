"""fdeprep: drills, exercises and sizing from the command line."""

import argparse
import sys
import textwrap

from fdeprep import bank, rubric
from fdeprep.estimate import Workload, estimate
from fdeprep.exercise import EXERCISES, exercise_dir, run_checks

WRAP = 64


def _wrap(text: str, indent: str = "") -> str:
    return textwrap.fill(
        text,
        WRAP,
        initial_indent=indent,
        subsequent_indent=indent,
    )


def cmd_rounds(args) -> int:
    questions = bank.load()
    for r in bank.ROUNDS:
        n = sum(q.round == r for q in questions)
        print(f"{r:<11} {n:>3} questions")
    return 0


def cmd_drill(args) -> int:
    for q in bank.drill(args.round, args.n, args.seed):
        print(f"[{q.id}] ({q.round})")
        print(_wrap(q.prompt, "  "))
        if args.reveal:
            print("  Strong answers show:")
            for s in q.signals:
                print(_wrap(f"- {s}", "    "))
            print(_wrap(f"Follow-up: {q.follow_up}", "  "))
        print()
    return 0


def cmd_exercises(args) -> int:
    for key, (_, title) in EXERCISES.items():
        print(f"{key}  {title}")
    return 0


def cmd_brief(args) -> int:
    path = exercise_dir(args.exercise) / "brief.md"
    print(path.read_text(encoding="utf-8"))
    return 0


def cmd_check(args) -> int:
    target = "solution" if args.solution else "starter"
    results = run_checks(args.exercise, target)
    for r in results:
        mark = "PASS" if r.ok else "FAIL"
        print(f"{mark}  {r.name.removeprefix('check_')}")
        if not r.ok:
            print(_wrap(r.detail, "      "))
    passed = sum(r.ok for r in results)
    print(f"\n{passed}/{len(results)} checks passed ({target})")
    return 0 if passed == len(results) else 1


def cmd_estimate(args) -> int:
    w = Workload(
        users=args.users,
        requests_per_user=args.per_user,
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        price_in=args.price_in,
        price_out=args.price_out,
        working_days=args.days,
        active_hours=args.hours,
        peak_factor=args.peak,
    )
    for key, value in estimate(w).items():
        print(f"{key:<22} {value:>14,}")
    return 0


def cmd_score(args) -> int:
    scores = {}
    for pair in args.scores:
        name, _, value = pair.partition("=")
        scores[name] = int(value)
    v = rubric.score(args.round, scores)
    print(f"verdict: {v.label}  (average {v.average})")
    if v.focus:
        print(f"practice next: {', '.join(v.focus)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fdeprep")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("rounds", help="question counts by round")

    d = sub.add_parser("drill", help="random practice questions")
    d.add_argument("--round", choices=bank.ROUNDS)
    d.add_argument("--n", type=int, default=3)
    d.add_argument("--seed", type=int)
    d.add_argument("--reveal", action="store_true")

    sub.add_parser("exercises", help="list hands-on exercises")
    b = sub.add_parser("brief", help="print an exercise brief")
    b.add_argument("exercise", choices=EXERCISES)
    c = sub.add_parser("check", help="run an exercise's checks")
    c.add_argument("exercise", choices=EXERCISES)
    c.add_argument("--solution", action="store_true")

    e = sub.add_parser("estimate", help="size cost and load")
    e.add_argument("--users", type=int, required=True)
    e.add_argument("--per-user", type=float, required=True)
    e.add_argument("--input-tokens", type=int, required=True)
    e.add_argument("--output-tokens", type=int, required=True)
    e.add_argument("--price-in", type=float, required=True)
    e.add_argument("--price-out", type=float, required=True)
    e.add_argument("--days", type=int, default=22)
    e.add_argument("--hours", type=float, default=8.0)
    e.add_argument("--peak", type=float, default=3.0)

    s = sub.add_parser("score", help="score a mock round")
    s.add_argument("round", choices=list(rubric.DIMENSIONS))
    s.add_argument("scores", nargs="+", metavar="DIM=1..4")
    return p


COMMANDS = {
    "rounds": cmd_rounds,
    "drill": cmd_drill,
    "exercises": cmd_exercises,
    "brief": cmd_brief,
    "check": cmd_check,
    "estimate": cmd_estimate,
    "score": cmd_score,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return COMMANDS[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
