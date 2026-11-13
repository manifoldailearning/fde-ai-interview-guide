"""Checks for ex04. Each receives your module."""

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "ex04_docs", Path(__file__).with_name("clinic_docs.py")
)
_docs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_docs)
DOCS = _docs.DOCS


def check_chunks_cover_every_word(mod):
    for d in DOCS:
        pieces = mod.chunk(d["doc_id"], d["text"])
        assert pieces, f"{d['doc_id']} produced no chunks"
        seen = set()
        for p in pieces:
            n = len(p["text"].split())
            seen.update(range(p["start"], p["start"] + n))
        words = len(d["text"].split())
        missing = set(range(words)) - seen
        assert not missing, f"{d['doc_id']} loses words {missing}"


def check_short_documents_are_searchable(mod):
    pipe = mod.Pipeline(DOCS)
    hits = pipe.search("north", "Where is parking?")
    got = [h["doc_id"] for h in hits]
    assert got == ["north-parking"], f"got {got}"


def check_punctuation_does_not_hide_matches(mod):
    pipe = mod.Pipeline(DOCS)
    hits = pipe.search("south", "hours")
    got = {h["doc_id"] for h in hits}
    assert got == {"south-refills"}, got


def check_tenants_never_see_each_other(mod):
    pipe = mod.Pipeline(DOCS)
    for tenant in ("north", "south"):
        hits = pipe.search(tenant, "How long do refills take?")
        assert hits, f"no hits for {tenant}"
        for h in hits:
            assert h["doc_id"].startswith(tenant), (
                f"{tenant} saw {h['doc_id']}"
            )


def check_cache_is_scoped_per_tenant(mod):
    pipe = mod.Pipeline(DOCS)
    q = "How long do prescription refills take?"
    north = pipe.answer("north", q)
    south = pipe.answer("south", q)
    assert north["sources"][0] == "north-refills", north
    assert south["sources"][0] == "south-refills", south
