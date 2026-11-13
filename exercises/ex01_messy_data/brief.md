# ex01 — Clean a customer's ticket export (coding screen, 40 min)

**Customer:** Corvane Freight, a fictional logistics company.
**Ask:** "Here's our ticket export. How fast do we resolve
things, by priority?"

`tickets_export.csv` is what the customer actually sent. It came
from two help-desk tools merged by hand, so:

- dates come in four formats, including Unix epoch seconds;
  slashed dates are day/month/year (the team is in India);
- some tickets appear twice; keep the row with the latest
  `updated_at`;
- priority is written as P1, 1, urgent, critical, high, medium,
  normal, low, or left blank (blank means P3, the customer's
  default);
- status has mixed case and the word "solved";
- resolution is minutes, "1h 45m", "55m", "24h", blank or N/A;
- ticket bodies contain customers' phone numbers and emails.

## Implement in starter.py

1. `clean(rows) -> list[Ticket]`, sorted by ticket id, with
   emails and phone numbers in `body` replaced by `[email]` and
   `[phone]`, and `customer_email` trimmed and lowercased.
2. `summarize(tickets) -> dict` with `tickets` (count),
   `by_status` (counts) and `median_minutes` per priority, over
   resolved or closed tickets that have a resolution time.

Fail loudly on a value you do not recognize. Do not guess.

## Check your work

    fdeprep check ex01

## Talk track (what the interviewer listens for)

- Which assumptions you made, and which you would confirm with
  the customer before reporting a number (the date order, what a
  blank priority means, what "resolution" measures).
- Why the masking happens before anything is logged or shared.
- What the median hides, and what you would show next to it.
