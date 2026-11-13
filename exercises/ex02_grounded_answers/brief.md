# ex02 — Grounded answers, cited (live build, 60 minutes)

**Customer:** Meridian Mutual, a fictional insurer.
**Ask:** "Our agents waste time searching the claims handbook.
Build something that answers their questions from it."

You get the handbook as `fdeprep.sim.meridian.DOCS` (16
documents) and a model, `fdeprep.sim.context_model.ContextModel`,
that answers from whatever passages you hand it. Read its
docstring: it is capable but over-eager. It answers even when the
passages barely relate to the question, it guesses when given
nothing, and it follows instructions planted in a passage.

Implement `Assistant.answer(question) -> Answer` in `starter.py`.

## Requirements

1. Answer from the handbook, citing the document you used.
2. When the handbook does not answer the question, abstain:
   return `abstained=True`, no citations.
3. Never repeat instructions planted inside a document. One
   document came from an outside vendor upload.
4. Only cite documents you actually showed the model.

`fdeprep.retrieval.BM25Index` is available. You may write your
own retrieval instead.

## Check your work

    fdeprep check ex02

The checks ask nine answerable questions, three that the handbook
cannot answer and two that pull in the vendor document.

## Talk track (what the interviewer listens for)

- How you decide when not to answer, and why the model cannot
  be trusted to make that call.
- Why the vendor document is a trust-boundary problem, not a
  prompt-wording problem.
- What you would measure next, and what you would ask the
  customer before going further.
