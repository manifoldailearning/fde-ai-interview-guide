"""A customer's ticketing API with the habits of real ones.

- OAuth-style tokens that expire after TOKEN_TTL seconds (401).
- A rate limit of RATE_LIMIT requests per RATE_WINDOW seconds,
  answered with 429 and a Retry-After header.
- Cursor pagination with a maximum page size (400 above it).
- A transient 503 on every 7th authenticated request.
- Note creation that honors an Idempotency-Key header. The very
  first note write is stored and then answered with a 503, the
  way a gateway timeout looks to a client.

Time comes from a VirtualClock, so nothing really sleeps.
"""

import math
from dataclasses import dataclass, field

from fdeprep.sim.clock import VirtualClock

CLIENT_ID = "fde-demo"
CLIENT_SECRET = "s3cret"
TOKEN_TTL = 15.0
RATE_LIMIT = 5
RATE_WINDOW = 10.0
PAGE_MAX = 20


@dataclass
class Response:
    status: int
    body: dict
    headers: dict = field(default_factory=dict)


class FakeTicketAPI:
    def __init__(self, clock: VirtualClock, n: int = 137) -> None:
        self.clock = clock
        self.tickets = [_ticket(i) for i in range(1, n + 1)]
        self.notes: list[dict] = []
        self.requests = 0
        self.status_counts: dict[int, int] = {}
        self._tokens: dict[str, float] = {}
        self._recent: list[float] = []
        self._authed = 0
        self._idem: dict[str, Response] = {}
        self._first_note = True

    def request(
        self,
        method: str,
        path: str,
        headers: dict | None = None,
        params: dict | None = None,
        body: dict | None = None,
    ) -> Response:
        self.requests += 1
        resp = self._route(
            method, path, headers or {}, params or {}, body or {}
        )
        code = resp.status
        self.status_counts[code] = (
            self.status_counts.get(code, 0) + 1
        )
        return resp

    def _route(self, method, path, headers, params, body):
        if method == "POST" and path == "/oauth/token":
            return self._issue_token(body)
        if not self._valid_token(headers):
            return Response(401, {"error": "invalid_token"})
        limited = self._rate_limited()
        if limited:
            return limited
        self._authed += 1
        if self._authed % 7 == 0:
            return Response(503, {"error": "unavailable"})
        if method == "GET" and path == "/tickets":
            return self._list(params)
        parts = path.strip("/").split("/")
        if method == "POST" and len(parts) == 3:
            if parts[0] == "tickets" and parts[2] == "notes":
                return self._add_note(parts[1], headers, body)
        return Response(404, {"error": "not_found"})

    def _issue_token(self, body):
        ok = (
            body.get("client_id") == CLIENT_ID
            and body.get("client_secret") == CLIENT_SECRET
        )
        if not ok:
            return Response(400, {"error": "invalid_client"})
        token = f"tok-{len(self._tokens) + 1}"
        self._tokens[token] = self.clock.time() + TOKEN_TTL
        body = {"access_token": token, "expires_in": TOKEN_TTL}
        return Response(200, body)

    def _valid_token(self, headers):
        auth = headers.get("Authorization", "")
        token = auth.removeprefix("Bearer ")
        expiry = self._tokens.get(token)
        return expiry is not None and self.clock.time() < expiry

    def _rate_limited(self):
        now = self.clock.time()
        cutoff = now - RATE_WINDOW
        self._recent = [t for t in self._recent if t > cutoff]
        if len(self._recent) >= RATE_LIMIT:
            wait = self._recent[0] + RATE_WINDOW - now
            headers = {"Retry-After": str(math.ceil(wait))}
            return Response(
                429, {"error": "rate_limited"}, headers
            )
        self._recent.append(now)
        return None

    def _list(self, params):
        limit = int(params.get("limit", 10))
        if limit > PAGE_MAX:
            return Response(400, {"error": "limit too large"})
        cursor = params.get("cursor") or "c0"
        start = int(cursor.removeprefix("c"))
        page = self.tickets[start : start + limit]
        end = start + len(page)
        more = end < len(self.tickets)
        nxt = f"c{end}" if more else None
        return Response(200, {"data": page, "next_cursor": nxt})

    def _add_note(self, ticket_id, headers, body):
        if not any(t["id"] == ticket_id for t in self.tickets):
            return Response(404, {"error": "no such ticket"})
        key = headers.get("Idempotency-Key")
        if key and key in self._idem:
            return self._idem[key]
        note = {
            "id": f"N{len(self.notes) + 1}",
            "ticket_id": ticket_id,
            "text": body.get("text", ""),
        }
        self.notes.append(note)
        resp = Response(201, note)
        if key:
            self._idem[key] = resp
        if self._first_note:
            self._first_note = False
            return Response(503, {"error": "gateway timeout"})
        return resp


def _ticket(i: int) -> dict:
    priority = ("P1", "P2", "P3", "P3", "P4")[i % 5]
    return {
        "id": f"T{i:04d}",
        "subject": f"Shipment exception {i}",
        "priority": priority,
    }
