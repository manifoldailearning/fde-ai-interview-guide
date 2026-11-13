# Corvane Freight: "an AI agent for dispatch"

## Prompt (read aloud)

Corvane Freight's chief operating officer wants an AI agent for
dispatch. They've seen a demo and they want to move fast. Where
do you start?

## Facts to reveal only when asked

- **Why now?** Late-delivery complaints are up; two large shippers
  raised them at quarterly reviews. The COO thinks dispatch reacts
  too slowly.
- **What do complaints say?** Many are about finding out late: the
  shipper hears about a delay from its own customer.
- **Team and volume.** 24 planners, about 1,800 loads a day.
- **Exceptions.** Their estimate: about 12 percent of loads have an
  exception (late pickup, breakdown, missing customs documents).
  Planners estimate 15 to 25 minutes per exception.
- **Where the time goes.** Unknown. Planners say gathering
  information and updating people are the worst part.
- **Data.** The transport management system has load records and
  status events, behind a rate-limited vendor API. Carrier emails
  go to a shared inbox. Calls are not recorded. Planners keep
  free-text notes per exception.
- **Constraints.** Some shippers' contracts restrict sharing their
  data with third parties; legal must review external model use.
- **People.** The head of dispatch must agree. Planners have been
  through a failed software rollout and are skeptical.

## Change of facts (minute 25)

"Legal says no data can leave Corvane's network."

## Watch for

- Separates on-time delivery from timely notification.
- Asks how the 15 to 25 minutes splits between gathering,
  deciding and updating.
- Sizes out loud: about 216 exceptions a day, 54 to 90 planner
  hours, labeled as their estimate.
- Proposes a baseline before the pilot.
- Wedge keeps planners in control (drafts and summaries), starts
  with email exceptions, excludes automatic rerouting.
- After the change: in-network hosting, model evaluation on past
  exceptions, wedge unchanged.

## Common weak moves

- Designs an autonomous rerouting agent in the first five minutes.
- Never asks about planners or the previous rollout.
- Claims on-time delivery will improve by a specific percentage.
