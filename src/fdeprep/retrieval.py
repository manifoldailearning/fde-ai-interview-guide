"""BM25 keyword retrieval in a few lines, no dependencies."""

import math
from collections import Counter

from fdeprep.text import tokenize


class BM25Index:
    def __init__(
        self, docs: dict[str, str], k1=1.5, b=0.75
    ) -> None:
        self.k1, self.b = k1, b
        self.ids = list(docs)
        self.tf = [Counter(tokenize(docs[i])) for i in self.ids]
        self.len = [sum(c.values()) for c in self.tf]
        self.avg = sum(self.len) / max(len(self.len), 1)
        df = Counter(t for c in self.tf for t in c)
        n = len(self.ids)
        self.idf = {
            t: math.log(1 + (n - f + 0.5) / (f + 0.5))
            for t, f in df.items()
        }

    def search(
        self, query: str, k: int = 3
    ) -> list[tuple[str, float]]:
        terms = tokenize(query)
        scored = []
        for i, tf in enumerate(self.tf):
            score = 0.0
            norm = self.k1 * (
                1 - self.b + self.b * self.len[i] / self.avg
            )
            for t in terms:
                f = tf.get(t, 0)
                if f:
                    idf = self.idf[t]
                    score += idf * f * (self.k1 + 1) / (f + norm)
            if score > 0:
                scored.append((self.ids[i], round(score, 3)))
        scored.sort(key=lambda p: (-p[1], p[0]))
        return scored[:k]
