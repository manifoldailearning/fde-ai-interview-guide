# ex03 — A tool-calling agent, guarded (live build, 60 minutes)

**Customer:** Brightwater Retail, a fictional online store.
**Ask:** "Let the AI handle order tickets end to end: status,
refunds, cancellations."

You get three things:

- `fdeprep.sim.planner.Planner`: the model. `next_action(ticket,
  history)` returns raw text, usually a JSON tool call or a final
  answer. Read its docstring for the history format.
- `fdeprep.sim.backend.demo_orders()`: the order system with
  `lookup_order`, `issue_refund`, `cancel_order` and `escalate`.
  It does what it is told. It checks nothing.
- `tickets.py`: ten real-looking tickets.

Implement `run_ticket(ticket, backend, planner) -> Outcome` in
`starter.py`.

## Policy the customer signed off

1. At most 6 model calls per ticket. Out of budget: escalate.
2. Unparseable model output: tell the model in the history and
   ask again (it costs a step).
3. Only the four tools above. Anything else: escalate.
4. Act only on an order you looked up and that belongs to the
   ticket's customer.
5. Refunds: at most 200, and never more than the order's unpaid
   balance (total minus already refunded). Above that: escalate
   for human approval.
6. Every escalation goes to the human queue through
   `backend.escalate(reason)`, and the customer gets a holding
   reply that promises nothing.

## Check your work

    fdeprep check ex03

## Talk track (what the interviewer listens for)

- Where each rule is enforced (in code, outside the model) and
  why the prompt is not a control.
- What you log for the customer's audit team.
- Which ticket types you would keep away from automation in
  week one, and how you would earn the right to automate more.
