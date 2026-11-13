"""Chapter 13: evaluate both builds, then decide."""

from _load import solution
from fdeprep.sim.meridian import GOLDEN
from fdeprep.sim.systems import baseline, candidate

m = solution("ex06")


def show(r) -> None:
    print(f"{r.name}")
    print(f"  accuracy      {r.accuracy:.3f}")
    print(f"  answer rate   {r.answer_rate:.3f}")
    print(f"  unsupported   {r.unsupported}")
    print(f"  passages/q    {r.passages_per_question}")
    for name, acc in r.by_slice.items():
        print(f"  {name:<13} {acc:.3f}")
    print(f"  failures      {' '.join(r.failures)}")


def main() -> None:
    base = m.evaluate(baseline(), GOLDEN)
    cand = m.evaluate(candidate(), GOLDEN)
    show(base)
    show(cand)
    decision = m.decide(base, cand)
    print(f"ship candidate: {decision.ship}")
    for reason in decision.reasons:
        print(f"  - {reason}")


if __name__ == "__main__":
    main()
