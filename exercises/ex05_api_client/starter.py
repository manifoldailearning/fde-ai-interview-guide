"""ex05 starter: implement TicketClient (see brief.md)."""


class ApiError(Exception):
    def __init__(self, status: int, body: dict) -> None:
        super().__init__(f"HTTP {status}: {body}")
        self.status = status


class TicketClient:
    def __init__(self, api, clock, client_id, client_secret):
        self.api, self.clock = api, clock
        self.client_id = client_id
        self.client_secret = client_secret

    def fetch_all(self) -> list[dict]:
        raise NotImplementedError("page through every ticket")

    def add_note(self, ticket_id: str, text: str) -> dict:
        raise NotImplementedError("write one note, exactly once")
