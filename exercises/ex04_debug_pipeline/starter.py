"""ex04: the help-center answer pipeline as it runs today.

Two clinics share this deployment. Since last week's release,
staff report answers that are missing, wrong, or that mention the
other clinic. Find and fix the bugs (see brief.md).
"""

from fdeprep.text import tokenize

CHUNK_WORDS = 12
OVERLAP = 4


def chunk(doc_id: str, text: str) -> list[dict]:
    words = text.split()
    step = CHUNK_WORDS - OVERLAP
    return [
        {
            "doc_id": doc_id,
            "start": start,
            "text": " ".join(words[start : start + CHUNK_WORDS]),
        }
        for start in range(0, len(words) - CHUNK_WORDS, step)
    ]


class Pipeline:
    def __init__(self, docs: list[dict]) -> None:
        self.chunks = []
        for d in docs:
            for c in chunk(d["doc_id"], d["text"]):
                c["tenant"] = d["tenant"]
                c["tokens"] = set(c["text"].lower().split())
                self.chunks.append(c)
        self.cache: dict = {}

    def search(self, tenant: str, query: str, k: int = 2):
        wanted = set(tokenize(query))
        scored = [
            (len(wanted & c["tokens"]), c) for c in self.chunks
        ]
        scored = [s for s in scored if s[0] > 0]
        scored.sort(key=lambda s: (-s[0], s[1]["doc_id"]))
        return [c for _, c in scored[:k]]

    def answer(self, tenant: str, question: str) -> dict:
        key = question.strip().lower()
        if key in self.cache:
            return self.cache[key]
        hits = self.search(tenant, question)
        result = {
            "answer": hits[0]["text"] if hits else None,
            "sources": [c["doc_id"] for c in hits],
        }
        self.cache[key] = result
        return result
