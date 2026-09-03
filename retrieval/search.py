"""In-memory hybrid retrieval over the principle corpus.

Ships with a working keyword/overlap scorer so the app is useful with zero
extra dependencies. A cosine-similarity path is stubbed behind
`semantic_search`; wire it up once you have embeddings.npy and a small embed
client. Keep both and blend the scores (hybrid retrieval beats either alone).
"""
from __future__ import annotations

import re
import os
import numpy as np
from collections import Counter

from domain.models import Mode, Principle

_TOKEN_RE = re.compile(r"[a-z][a-z'-]+")
_STOP = {
    "the", "a", "an", "of", "to", "in", "is", "are", "and", "or", "for",
    "with", "that", "this", "it", "as", "on", "by", "be", "was", "were",
}

# Load embeddings once at module level if they exist
_EMBEDDINGS = None
_EMBEDDINGS_PATH = os.path.join("knowledge", "embeddings.npy")
if os.path.exists(_EMBEDDINGS_PATH):
    try:
        _EMBEDDINGS = np.load(_EMBEDDINGS_PATH)
    except Exception as e:
        print(f"Failed to load embeddings: {e}")

def _get_embedding(text: str) -> np.ndarray | None:
    from services.llm_grader import is_configured
    if not is_configured():
        return None
        
    if os.getenv("GOOGLE_API_KEY"):
        from google import genai
        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            response = client.models.embed_content(
                model="text-embedding-004",
                contents=text
            )
            return np.array(response.embeddings[0].values)
        except Exception as e:
            print(f"Gemini Embedding failed: {e}")
            return None
            
    elif os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"):
        from openai import AzureOpenAI
        try:
            client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"),
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "")
            )
            response = client.embeddings.create(
                input=text,
                model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
            )
            return np.array(response.data[0].embedding)
        except Exception as e:
            print(f"Azure/OpenAI Embedding failed: {e}")
            return None
            
    return None


def _tokens(text: str) -> Counter:
    return Counter(t for t in _TOKEN_RE.findall(text.lower()) if t not in _STOP)


def _principle_terms(p: Principle) -> Counter:
    blob = " ".join([p.title, p.principle, " ".join(p.skills)])
    return _tokens(blob)


def keyword_search(
    query: str,
    principles: list[Principle],
    mode: Mode | None = None,
    skills: list[str] | None = None,
    k: int = 4,
) -> list[Principle]:
    """Score by token overlap, filtered by track and (optionally) skill tags.
    Deterministic and explainable."""
    q = _tokens(query)
    skills = set(skills or [])

    scored: list[tuple[float, Principle]] = []
    for p in principles:
        if mode is not None and p.track not in (mode, "both"):
            continue
        if skills and not (skills & set(p.skills)):
            continue
        terms = _principle_terms(p)
        overlap = sum(min(q[t], terms[t]) for t in q)
        skill_boost = 2.0 * len(skills & set(p.skills))
        score = overlap + skill_boost
        if score > 0:
            scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:k]]


def semantic_search(query: str, principles: list[Principle], k: int = 4) -> list[Principle]:
    """Cosine similarity over precomputed embeddings."""
    if _EMBEDDINGS is None or len(_EMBEDDINGS) != len(principles):
        return keyword_search(query, principles, k=k)
        
    query_emb = _get_embedding(query)
    if query_emb is None:
        return keyword_search(query, principles, k=k)
        
    # Cosine similarity
    norms = np.linalg.norm(_EMBEDDINGS, axis=1) * np.linalg.norm(query_emb)
    # Avoid division by zero
    norms[norms == 0] = 1e-10
    sims = np.dot(_EMBEDDINGS, query_emb) / norms
    
    scored = [(float(sim), principles[i]) for i, sim in enumerate(sims)]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:k]]

def retrieve(
    query: str,
    principles: list[Principle],
    mode: Mode | None = None,
    skills: list[str] | None = None,
    k: int = 4,
) -> list[Principle]:
    """Hybrid retrieval: blend keyword and semantic scores."""
    if _EMBEDDINGS is None:
        return keyword_search(query, principles, mode=mode, skills=skills, k=k)
        
    query_emb = _get_embedding(query)
    if query_emb is None:
        return keyword_search(query, principles, mode=mode, skills=skills, k=k)
        
    # Get keyword scores for all
    q = _tokens(query)
    skills_set = set(skills or [])
    
    hybrid_scored = []
    
    # Cosine similarity
    norms = np.linalg.norm(_EMBEDDINGS, axis=1) * np.linalg.norm(query_emb)
    norms[norms == 0] = 1e-10
    sims = np.dot(_EMBEDDINGS, query_emb) / norms
    
    for i, p in enumerate(principles):
        if mode is not None and p.track not in (mode, "both"):
            continue
        if skills_set and not (skills_set & set(p.skills)):
            continue
            
        terms = _principle_terms(p)
        overlap = sum(min(q[t], terms[t]) for t in q)
        skill_boost = 2.0 * len(skills_set & set(p.skills))
        keyword_score = overlap + skill_boost
        
        # Normalize keyword score roughly (e.g. max expected is around 10)
        norm_kw = min(keyword_score / 10.0, 1.0)
        
        # Blend (e.g., 60% semantic, 40% keyword)
        semantic_score = sims[i]
        final_score = 0.6 * semantic_score + 0.4 * norm_kw
        
        if final_score > 0.1:
            hybrid_scored.append((final_score, p))
            
    hybrid_scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in hybrid_scored[:k]]
