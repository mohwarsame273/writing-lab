"""Deterministic text diagnostics — a working Writer's Diet style analyser.

This module is intentionally dependency-free (standard library only) so it is
fast, transparent, reproducible and cheap. It runs on the debounced server
tick and again at submission. It never calls an LLM.

The five Writer's Diet measures (after Helen Sword):
    verbs           strong finite verbs are good; we report their share
    nominalisations "zombie nouns": abstract nouns hiding a verb/adjective
    prepositions    stacked prepositional phrases bloat prose
    ad_words        adjectives + adverbs (especially -ly adverbs)
    waste_words     it / this / that / there used vaguely

The verdict bands mirror the Writer's Diet test's playful register but the
thresholds here are first-pass estimates. Tune them against your own corpus.

NOTE FOR THE COMPLETING AGENT: the pattern lists below are deliberate,
transparent heuristics, not a full NLP parser. If you upgrade to spaCy for POS
tagging, keep this function's *signature and return type* identical and add the
parser behind a feature flag so the zero-dependency path still works.
"""
from __future__ import annotations

import re
from collections import Counter

from domain.models import Diagnostic, DietScore

# --- lexicons ---------------------------------------------------------------

_NOMINALISATION_SUFFIXES = ("tion", "sion", "ment", "ance", "ence", "ity", "ness", "ancy", "ency")
# words that end in these suffixes but are not zombie nouns
_NOMINALISATION_STOP = {
    "mention", "function", "question", "attention", "condition", "position",
    "information", "nation", "station", "section", "portion", "region",
    "tension", "notion", "motion", "session", "mission", "passion",
}

_PREPOSITIONS = {
    "aboard", "about", "above", "across", "after", "against", "along", "amid",
    "among", "around", "as", "at", "before", "behind", "below", "beneath",
    "beside", "besides", "between", "beyond", "by", "concerning", "despite",
    "down", "during", "except", "for", "from", "in", "inside", "into", "like",
    "near", "of", "off", "on", "onto", "out", "outside", "over", "past",
    "regarding", "since", "through", "throughout", "to", "toward", "towards",
    "under", "underneath", "until", "unto", "up", "upon", "with", "within",
    "without",
}

_WASTE_WORDS = {"it", "this", "that", "there"}

# be-verbs and common weak/auxiliary verbs; a rough proxy for "weak verb" load
_BE_VERBS = {"is", "are", "was", "were", "be", "been", "being", "am"}

# a compact list of common strong verb inflections is impractical; instead we
# approximate "verb-ish" tokens via morphology + a be-verb check. This is a
# heuristic, flagged as such, and is the first thing to replace with real POS.
_VERB_HINT_SUFFIXES = ("ed", "ing", "es", "s")

_PASSIVE_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being|am)\b\s+(?:\w+ly\s+)?(\w+ed|\w+en|done|made|given|taken|seen|known|shown|written|built)\b",
    re.IGNORECASE,
)

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
_SENT_RE = re.compile(r"[^.!?]+[.!?]*")


# --- helpers ----------------------------------------------------------------

def _iter_words(text: str):
    for m in _WORD_RE.finditer(text):
        yield m.group(0), m.start(), m.end()


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT_RE.findall(text) if s.strip()]


def _is_nominalisation(word: str) -> bool:
    w = word.lower()
    if w in _NOMINALISATION_STOP or len(w) < 6:
        return False
    return w.endswith(_NOMINALISATION_SUFFIXES)


# --- public API -------------------------------------------------------------

def analyse(text: str) -> list[Diagnostic]:
    """Return span-level findings suitable for inline underlining.

    Each Diagnostic carries character offsets so the editor can decorate the
    exact range. Messages are phrased as prompts to think, not verdicts, and
    the UI layer decides whether academic/literary mode softens them further.
    """
    findings: list[Diagnostic] = []
    if not text.strip():
        return findings

    # nominalisations / zombie nouns
    for word, start, end in _iter_words(text):
        if _is_nominalisation(word):
            findings.append(
                Diagnostic(
                    type="nominalisation",
                    start=start,
                    end=end,
                    text=word,
                    severity="medium",
                    message=f"Possible zombie noun. Is there a stronger verb hiding inside '{word}'?",
                    rule_id="ACA-NOM-001",
                )
            )

    # passive constructions
    for m in _PASSIVE_RE.finditer(text):
        findings.append(
            Diagnostic(
                type="passive",
                start=m.start(),
                end=m.end(),
                text=m.group(0),
                severity="low",
                message="Passive construction. Consider naming the actor, unless the effect is deliberate.",
                rule_id="ACA-PAS-001",
            )
        )

    # stacked prepositions: 3+ prepositions inside one sentence window
    # (reported at sentence granularity)
    offset = 0
    for sent in _sentences(text):
        idx = text.find(sent, offset)
        offset = idx + len(sent) if idx >= 0 else offset
        prep_hits = [w for w, _, _ in _iter_words(sent) if w.lower() in _PREPOSITIONS]
        if len(prep_hits) >= 4 and idx >= 0:
            findings.append(
                Diagnostic(
                    type="preposition_stack",
                    start=idx,
                    end=idx + len(sent),
                    text=sent[:60] + ("..." if len(sent) > 60 else ""),
                    severity="medium",
                    message=f"{len(prep_hits)} prepositions in one sentence. Try tightening the chain of 'of/in/to' phrases.",
                    rule_id="ACA-PRE-001",
                )
            )

    # -ly adverb pile-ups
    for word, start, end in _iter_words(text):
        if word.lower().endswith("ly") and len(word) > 4:
            findings.append(
                Diagnostic(
                    type="adverb",
                    start=start,
                    end=end,
                    text=word,
                    severity="low",
                    message=f"Adverb '{word}'. Does the verb already carry this, or would a sharper verb do more?",
                    rule_id="ACA-ADV-001",
                )
            )

    return findings


def diet_score(text: str) -> DietScore:
    """Compute the aggregate Writer's Diet profile for a passage."""
    words = [w.lower() for w, _, _ in _iter_words(text)]
    total = len(words) or 1
    sentences = _sentences(text)
    sent_count = len(sentences) or 1

    nominalisations = sum(1 for w in words if _is_nominalisation(w))
    prepositions = sum(1 for w in words if w in _PREPOSITIONS)
    ad_words = sum(1 for w in words if w.endswith("ly") and len(w) > 4)
    waste = sum(1 for w in words if w in _WASTE_WORDS)
    # verb proxy: be-verbs plus morphological verb hints, minus obvious nouns.
    verbish = sum(
        1
        for w in words
        if w in _BE_VERBS or (w.endswith(_VERB_HINT_SUFFIXES) and not _is_nominalisation(w))
    )

    def ratio(n: int) -> float:
        return round(n / total, 4)

    mean_len = round(total / sent_count, 2)

    # crude composite: heavier nominalisation/prep/waste share => flabbier.
    flab = (
        ratio(nominalisations) * 3.0
        + ratio(prepositions) * 1.5
        + ratio(waste) * 2.0
        + ratio(ad_words) * 1.0
    )
    if flab < 0.10:
        verdict = "lean"
    elif flab < 0.16:
        verdict = "fit-and-trim"
    elif flab < 0.24:
        verdict = "needs-toning"
    elif flab < 0.34:
        verdict = "flabby"
    else:
        verdict = "heart-attack"

    return DietScore(
        verbs=ratio(verbish),
        nominalisations=ratio(nominalisations),
        prepositions=ratio(prepositions),
        ad_words=ratio(ad_words),
        waste_words=ratio(waste),
        word_count=total,
        sentence_count=sent_count,
        mean_sentence_len=mean_len,
        verdict=verdict,
    )


def repeated_openings(text: str) -> Counter:
    """Sentences that begin with the same word, a common habit worth surfacing
    in the free-writing profile."""
    openings: Counter = Counter()
    for sent in _sentences(text):
        first = _WORD_RE.match(sent)
        if first:
            openings[first.group(0).lower()] += 1
    return Counter({w: c for w, c in openings.items() if c > 1})
