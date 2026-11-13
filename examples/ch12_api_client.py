"""Chapter 12: what the client had to survive."""

from _load import solution
from fdeprep.sim.clock import VirtualClock
from fdeprep.sim.ticket_api import (
    CLIENT_ID,
    CLIENT_SECRET,
    FakeTicketAPI,
)

m = solution("ex05")


def main() -> None:
    clock = VirtualClock()
    api = FakeTicketAPI(clock)
    client = m.TicketClient(api, clock, CLIENT_ID, CLIENT_SECRET)
    tickets = client.fetch_all()
    client.add_note("T0002", "Escalated to carrier.")
    waited = clock.slept
    clock.sleep(60)  # the job pauses; the token expires
    client.add_note("T0003", "Customer confirmed delivery.")
    codes = dict(sorted(api.status_counts.items()))
    print(f"tickets fetched    {len(tickets)}")
    print(f"notes stored       {len(api.notes)}")
    print(f"requests sent      {api.requests}")
    print(f"responses          {codes}")
    print(f"client waits (s)   {waited}")


if __name__ == "__main__":
    main()
