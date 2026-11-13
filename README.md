# The Forward Deployed AI Engineer Interview: Practice Kit

Companion code for the book **The Forward Deployed AI Engineer
Interview** by Nachiketh Murthy.

Forward deployed interviews test more than coding. You will be
asked to frame a vague customer problem, build something that
works against the clock, debug a system you did not write,
integrate with an API that fights back, prove quality with an
evaluation, and explain all of it to people who do not write
code. This repository lets you practice the hands-on parts for
real, offline, and on your own schedule.

## What's inside

- **Six timed exercises**, each with a customer brief, a starter
  file, automated checks and a reference solution:

  | Key  | Exercise | Round | Time |
  |------|----------|-------|------|
  | ex01 | Clean a customer's ticket export | Coding screen | 40 min |
  | ex02 | Grounded answers with citations | Live build | 60 min |
  | ex03 | A tool-calling agent with guardrails | Live build | 60 min |
  | ex04 | Debug a broken multi-tenant AI pipeline | Debugging | 45 min |
  | ex05 | A client for a rate-limited, flaky API | Integration | 45 min |
  | ex06 | An eval harness and a ship-or-hold decision | Evals | 45 min |

- **A 100-question bank** across seven rounds (screen, case,
  build, debug, design, behavioral, role-play). Each question
  lists what a strong answer shows and a follow-up.
- **A scoring rubric** for mock rounds, and a **sizing tool** for
  back-of-envelope cost and load estimates.
- **Interviewer packs** in `cases/` so a friend can run a case
  round with you.

Everything is simulated: the models, the customer's order system
and the ticketing API are deterministic stand-ins. Nothing calls
a paid service, and every result is reproducible.

## Quick start

```bash
git clone https://github.com/manifoldailearning/fde-ai-interview-guide
cd fde-ai-interview-guide
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"      # Python 3.11+, no runtime dependencies
pytest -q
```

## Practice

```bash
fdeprep exercises                 # list the exercises
fdeprep brief ex02                # read a customer brief
fdeprep check ex02                # check your starter.py
fdeprep check ex02 --solution     # see the reference pass

fdeprep rounds                    # question counts by round
fdeprep drill --round case --n 3  # three random case questions
fdeprep drill --round design --reveal

fdeprep estimate --users 400 --per-user 20 \
  --input-tokens 3000 --output-tokens 400 \
  --price-in 1 --price-out 4      # prices are your inputs

fdeprep score case framing=3 discovery=2 metrics=3 \
  scope=3 risk=2 communication=4
```

Work in each exercise's `starter.py`. Set a timer before you
open the brief. Read the reference solution only after your own
attempt, then compare decisions, not just code.

## Repository map

- `src/fdeprep/sim/` deterministic stand-ins for models and
  customer systems
- `src/fdeprep/bank/` the question bank (`questions.json`)
- `src/fdeprep/rubric.py`, `estimate.py`, `cli.py`
- `exercises/exNN_*/` brief, starter, checks and solution
- `examples/chNN_*.py` the runs shown in the book
- `cases/` interviewer packs for mock case rounds

## Learn more

- *The Forward Deployed AI Engineer*, the companion field guide
  to owning enterprise AI delivery
- Live program: [Agentic AI Enterprise Mastery Bootcamp](https://manifoldailearning.com/services/agenticaibootcamp)
- [manifoldailearning.com](https://manifoldailearning.com)

## License

MIT. See [LICENSE](LICENSE).
