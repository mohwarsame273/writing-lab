"""Load the JSON writing-rule knowledge base into memory.

At this scale (dozens to a few thousand rule chunks) you do NOT need Pinecone,
Weaviate or any hosted vector DB. A list of dicts plus, optionally, a NumPy
matrix of precomputed embeddings is fast enough and far simpler.

Drop your own writing-aid documents into knowledge/ as principles.json records
shaped like domain.models.Principle. Regenerate embeddings.npy offline when you
add the semantic layer (see retrieval/search.py).
"""
from __future__ import annotations

import json
from pathlib import Path

from domain.models import Mode, Principle

_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def load_principles(path: Path | None = None) -> list[Principle]:
    path = path or (_KNOWLEDGE_DIR / "principles.json")
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: list[Principle] = []
    for r in raw:
        track = r.get("track", "both")
        out.append(
            Principle(
                rule_id=r["rule_id"],
                title=r["title"],
                track=("both" if track == "both" else Mode(track)),
                skills=r.get("skills", []),
                principle=r["principle"],
                weak_examples=r.get("weak_examples", []),
                strong_examples=r.get("strong_examples", []),
                exceptions=r.get("exceptions", []),
                source=r.get("source", {}),
            )
        )
    return out
