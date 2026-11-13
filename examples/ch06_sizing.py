"""Chapter 6: size a use case out loud, then find the lever.

Prices here are placeholders (per million tokens), not real
quotes. In an interview, say your assumptions and do the
arithmetic where the interviewer can follow it.
"""

from fdeprep.estimate import Workload, estimate

BASE = Workload(
    users=400,
    requests_per_user=20,
    input_tokens=3000,
    output_tokens=400,
    price_in=1.0,
    price_out=4.0,
)


def show(label: str, w: Workload) -> None:
    out = estimate(w)
    print(
        f"{label:<26} {out['cost_per_month']:>9,.2f}/month"
        f"  peak {out['peak_rps']:.2f} rps"
    )


def main() -> None:
    for key, value in estimate(BASE).items():
        print(f"{key:<22} {value:>14,}")
    print()
    show("baseline", BASE)
    show("context cut to 1,500", _with(input_tokens=1500))
    show("answers cut to 200", _with(output_tokens=200))
    show("usage doubles", _with(requests_per_user=40))


def _with(**changes) -> Workload:
    return Workload(**(BASE.__dict__ | changes))


if __name__ == "__main__":
    main()
