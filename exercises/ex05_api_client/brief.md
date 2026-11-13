# ex05 — A client for a hostile API (45 minutes)

**Customer:** Corvane Freight again. Your pilot must read every
open ticket from their ticketing system and write a note back on
the ones it handles.

`fdeprep.sim.ticket_api.FakeTicketAPI` behaves like the real
thing. Read its docstring: short-lived tokens, a rate limit with
`Retry-After`, cursor pagination with a page-size cap, transient
503s, and an `Idempotency-Key` header on note writes. Time runs
on a `VirtualClock`; always wait with `clock.sleep`.

Implement `TicketClient.fetch_all()` and
`TicketClient.add_note(ticket_id, text)` in `starter.py`.

## Requirements

1. `fetch_all` returns every ticket exactly once.
2. Respect the page-size cap and the `Retry-After` header.
3. Refresh the token when it expires; never ask the customer to
   restart a job because a token aged out.
4. Retry 502, 503 and 504 with backoff. Never retry 400 or 404.
5. A note is written exactly once, even if the server stored it
   and then timed out.

## Check your work

    fdeprep check ex05

## Talk track (what the interviewer listens for)

- Why the note write is the dangerous call, and what an
  idempotency key buys you.
- What you would agree with the customer's API owners before the
  pilot (rate limits, a service account, a test tenant).
- How you would know in production that the client is retrying
  more than it should.
