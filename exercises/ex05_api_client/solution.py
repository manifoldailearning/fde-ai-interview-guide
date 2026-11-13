"""Reference solution: a client that survives a real API."""

import uuid

PAGE_SIZE = 20
MAX_ATTEMPTS = 6
RETRYABLE = {502, 503, 504}


class ApiError(Exception):
    def __init__(self, status: int, body: dict) -> None:
        super().__init__(f"HTTP {status}: {body}")
        self.status = status


class TicketClient:
    def __init__(self, api, clock, client_id, client_secret):
        self.api, self.clock = api, clock
        self.creds = {
            "client_id": client_id,
            "client_secret": client_secret,
        }
        self.token = None
        self.expires_at = 0.0

    def fetch_all(self) -> list[dict]:
        seen: dict[str, dict] = {}
        cursor = None
        while True:
            params = {"limit": PAGE_SIZE}
            if cursor:
                params["cursor"] = cursor
            page = self._send("GET", "/tickets", params=params)
            for t in page["data"]:
                seen[t["id"]] = t
            cursor = page["next_cursor"]
            if not cursor:
                return list(seen.values())

    def add_note(self, ticket_id: str, text: str) -> dict:
        key = uuid.uuid4().hex
        return self._send(
            "POST",
            f"/tickets/{ticket_id}/notes",
            body={"text": text},
            headers={"Idempotency-Key": key},
        )

    def _login(self) -> None:
        resp = self.api.request(
            "POST", "/oauth/token", body=self.creds
        )
        if resp.status != 200:
            raise ApiError(resp.status, resp.body)
        self.token = resp.body["access_token"]
        ttl = float(resp.body["expires_in"])
        self.expires_at = self.clock.time() + ttl - 1.0

    def _send(
        self, method, path, params=None, body=None, headers=None
    ) -> dict:
        headers = dict(headers or {})
        delay = 0.5
        refreshed = False
        for _ in range(MAX_ATTEMPTS):
            if (
                self.token is None
                or self.clock.time() >= self.expires_at
            ):
                self._login()
            headers["Authorization"] = f"Bearer {self.token}"
            resp = self.api.request(
                method, path, headers, params, body
            )
            if resp.status == 401 and not refreshed:
                self.token, refreshed = None, True
                continue
            if resp.status == 429:
                wait = float(resp.headers.get("Retry-After", 1))
                self.clock.sleep(wait)
                continue
            if resp.status in RETRYABLE:
                self.clock.sleep(delay)
                delay *= 2
                continue
            if resp.status >= 400:
                raise ApiError(resp.status, resp.body)
            return resp.body
        raise ApiError(resp.status, resp.body)
