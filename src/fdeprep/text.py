"""Small text helpers shared by the exercises."""

import re

STOPWORDS = frozenset(
    "a an and are as at be by can do does for from has have how"
    " i if in is it its my of on or our that the their this to"
    " was we what when where which who will with you your".split()
)

_WORD = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens without stopwords."""
    words = _WORD.findall(text.lower())
    return [w for w in words if w not in STOPWORDS]


def sentences(text: str) -> list[str]:
    """Split text into sentences on ., ! and ?."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]
