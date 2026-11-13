"""Chapter 10: run every ticket and show what the agent did."""

from _load import solution
from fdeprep.exercise import exercise_dir, load
from fdeprep.sim.backend import demo_orders
from fdeprep.sim.planner import Planner

m = solution("ex03")
tickets = load(
    exercise_dir("ex03") / "tickets.py", "ex03_tickets"
).TICKETS


def main() -> None:
    backend, planner = demo_orders(), Planner()
    for t in tickets:
        out = m.run_ticket(t, backend, planner)
        print(f"{t['id']:<4} {out.status:<9} steps={out.steps}")
        if out.reason:
            print(f"     reason: {out.reason}")
    print()
    print("side effects:")
    for entry in backend.log:
        if entry[0] != "escalate":
            print(f"  {entry}")


if __name__ == "__main__":
    main()
