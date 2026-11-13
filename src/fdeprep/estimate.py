"""Back-of-envelope sizing for case and design rounds.

Prices are inputs, per million tokens, in whatever currency you
use. Bring the customer's or the provider's current numbers; the
defaults in examples are placeholders, not real prices.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Workload:
    users: int
    requests_per_user: float  # per working day
    input_tokens: int  # per request, prompt plus context
    output_tokens: int  # per request
    price_in: float  # per million input tokens
    price_out: float  # per million output tokens
    working_days: int = 22  # per month
    active_hours: float = 8.0  # per working day
    peak_factor: float = 3.0  # peak rate over the day's average


def estimate(w: Workload) -> dict:
    per_day = w.users * w.requests_per_user
    tokens_in = per_day * w.input_tokens
    tokens_out = per_day * w.output_tokens
    cost_day = (
        tokens_in * w.price_in + tokens_out * w.price_out
    ) / 1_000_000
    avg_rps = per_day / (w.active_hours * 3600)
    return {
        "requests_per_day": round(per_day),
        "input_tokens_per_day": round(tokens_in),
        "output_tokens_per_day": round(tokens_out),
        "cost_per_day": round(cost_day, 2),
        "cost_per_month": round(cost_day * w.working_days, 2),
        "cost_per_request": round(cost_day / per_day, 5),
        "average_rps": round(avg_rps, 3),
        "peak_rps": round(avg_rps * w.peak_factor, 3),
    }
