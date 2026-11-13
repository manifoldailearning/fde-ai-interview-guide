"""Chapter 17: one practice loop: drill, answer, score, focus."""

import textwrap

from fdeprep import bank, rubric


def main() -> None:
    for q in bank.drill("design", n=2, seed=17):
        print(textwrap.fill(f"[{q.id}] {q.prompt}", 62))
    print()
    scores = {
        "requirements": 3,
        "architecture": 3,
        "trust": 2,
        "operations": 2,
        "tradeoffs": 3,
        "communication": 4,
    }
    v = rubric.score("design", scores)
    print(f"verdict {v.label}, average {v.average}")
    print(f"practice next: {', '.join(v.focus)}")


if __name__ == "__main__":
    main()
