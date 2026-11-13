"""Chapter 8: clean the customer's export, then report."""

from _load import solution

m = solution("ex01")


def main() -> None:
    rows = m.load_rows()
    tickets = m.clean(rows)
    print(f"rows in export   {len(rows)}")
    print(f"unique tickets   {len(tickets)}")
    summary = m.summarize(tickets)
    print("tickets by status:")
    for status, n in summary["by_status"].items():
        print(f"  {status:<10} {n:>3}")
    print("median minutes to resolve, resolved or closed:")
    for priority, minutes in summary["median_minutes"].items():
        print(f"  {priority}  {minutes:>6}")
    t1 = next(t for t in tickets if t.ticket_id == "T-001")
    print(f"masked body      {t1.body}")


if __name__ == "__main__":
    main()
