"""Chapter 11: the checks before and after the fixes."""

from fdeprep.exercise import run_checks


def main() -> None:
    for target in ("starter", "solution"):
        results = run_checks("ex04", target)
        passed = sum(r.ok for r in results)
        print(f"{target}: {passed}/{len(results)} checks pass")
        for r in results:
            if not r.ok:
                print(f"  FAIL {r.name.removeprefix('check_')}")


if __name__ == "__main__":
    main()
