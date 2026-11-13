# ex04 — Debug a broken AI pipeline (45 minutes)

**Customer:** Tessaly Health, a fictional group of clinics. Two
clinics, North and South, share one deployment of a help-center
answer pipeline.

**Report from the customer, verbatim:** "Since last week some
answers are cut off, some questions get nothing back, and a South
receptionist got the North clinic's refill times. We need this
fixed today and we need to know it cannot happen again."

`starter.py` is the code as it runs today. There are four bugs.
Fix them without rewriting the module.

## How to work

1. Run `fdeprep check ex04` and read every failure first.
2. Reproduce each one in the smallest way you can.
3. Fix one bug at a time and re-run the checks.
4. Say which bug is a data-leak incident, and what you would tell
   the customer about it.

## Talk track (what the interviewer listens for)

- A method, not guessing: reproduce, isolate, fix, verify.
- Severity: one of these bugs is a privacy incident between
  tenants. Treat it differently from the others.
- Prevention: which test or control would have caught each bug
  before release.
