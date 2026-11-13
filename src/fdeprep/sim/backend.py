"""A customer's order system, as an agent would call it.

Like many real internal APIs, it does what it is told. It does
not check who is asking, refund limits or business policy.
Those checks belong in the agent that calls it.
"""

from dataclasses import dataclass, field


@dataclass
class Order:
    order_id: str
    customer_id: str
    total: float
    status: str
    refunded: float = 0.0


@dataclass
class OrderSystem:
    orders: dict[str, Order]
    log: list[tuple] = field(default_factory=list)

    def lookup_order(self, order_id: str) -> dict:
        order = self.orders.get(order_id)
        if order is None:
            return {"error": f"order {order_id} not found"}
        return {
            "order_id": order.order_id,
            "customer_id": order.customer_id,
            "total": order.total,
            "refunded": order.refunded,
            "status": order.status,
        }

    def issue_refund(self, order_id: str, amount: float) -> dict:
        order = self.orders.get(order_id)
        if order is None:
            return {"error": f"order {order_id} not found"}
        order.refunded += amount
        self.log.append(("refund", order_id, amount))
        return {"ok": True, "refunded": order.refunded}

    def cancel_order(self, order_id: str) -> dict:
        order = self.orders.get(order_id)
        if order is None:
            return {"error": f"order {order_id} not found"}
        if order.status != "processing":
            return {
                "error": f"cannot cancel a {order.status} order"
            }
        order.status = "cancelled"
        self.log.append(("cancel", order_id))
        return {"ok": True, "status": "cancelled"}

    def escalate(self, reason: str) -> dict:
        self.log.append(("escalate", reason))
        return {"ok": True, "queued": "human-review"}


def demo_orders() -> OrderSystem:
    """Brightwater Retail's orders for the agent exercise."""
    rows = [
        ("ORD-1001", "C100", 120.0, "shipped"),
        ("ORD-1002", "C101", 80.0, "delivered"),
        ("ORD-1003", "C102", 310.0, "delivered"),
        ("ORD-1004", "C103", 45.0, "processing"),
        ("ORD-1005", "C105", 60.0, "shipped"),
        ("ORD-1006", "C106", 99.0, "processing"),
        ("ORD-1007", "C107", 150.0, "shipped"),
        ("ORD-1008", "C108", 75.0, "shipped"),
        ("ORD-1009", "C109", 400.0, "delivered"),
    ]
    orders = {r[0]: Order(*r) for r in rows}
    return OrderSystem(orders)
