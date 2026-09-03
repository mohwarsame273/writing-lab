"""The grader: three layers, assembled into one GradeResult.

    Layer 1  deterministic diagnostics  (domain.diagnostics)  -- always runs
    Layer 2  retrieved writing principles (retrieval.search)   -- always runs
    Layer 3  contextual LLM judgement     (services.llm_grader) -- optional

The golden rule: the LLM is never the whole marking system. It judges only
what counting words cannot (meaning preservation, force, whether a
nominalisation is *useful* rather than merely present). If no LLM is
configured, Layers 1 and 2 still yield a genuine, explainable grade.

Academic and literary modes apply different rubrics and soften different
findings. See `_rubric_for` and `_soften`.
"""
from __future__ import annotations

from domain.diagnostics import analyse, diet_score
from domain.models import (
    Diagnostic,
    Exercise,
    GradeResult,
    Mode,
    RubricScore,
)
from domain.scoring import xp_for_attempt


def _rubric_for(mode: Mode) -> list[tuple[str, int]]:
    """(label, out_of) per band. Academic and literary weight differently."""
    if mode == Mode.ACADEMIC:
        return [
            ("Task fulfilment", 20),
            ("Clarity", 20),
            ("Sentence control", 20),
            ("Meaning preservation", 20),
            ("Concision", 20),
        ]
    return [
        ("Task fulfilment", 20),
        ("Voice", 20),
        ("Rhythm and variation", 20),
        ("Concrete imagery", 20),
        ("Restraint", 20),
    ]


def _soften(diags: list[Diagnostic], mode: Mode) -> list[Diagnostic]:
    """Literary mode tolerates fragments, passives and repetition when they are
    deliberate. We do not delete findings; we downgrade tone so the app teaches
    judgement rather than mechanical elimination."""
    if mode == Mode.ACADEMIC:
        return diags
    out = []
    for d in diags:
        if d.type in {"passive", "adverb"}:
            d.severity = "low"
            d.message = d.message.replace("Consider", "In academic prose you might")
        out.append(d)
    return out


def _deterministic_quality(diags: list[Diagnostic], word_count: int) -> float:
    """A transparent 0..1 quality proxy from finding density. Used when no LLM
    is present, and as a floor when one is. Fewer high-severity findings per
    100 words => higher quality."""
    if word_count == 0:
        return 0.0
    weight = {"low": 0.5, "medium": 1.0, "high": 2.0}
    # normalise per 100 words, but floor the denominator so a short, clean
    # sentence is not punished as if findings were densely packed.
    per_hundred = max(word_count, 40) / 100.0
    load = sum(weight[d.severity] for d in diags) / per_hundred
    # load of 0 -> ~0.95 ; load of ~6 -> ~0.35
    return max(0.2, min(0.98, 0.95 - load / 8.0))


def grade(
    *,
    submission: str,
    exercise: Exercise,
    mode: Mode,
    hint_level: int,
    attempt_number: int,
    retrieved_principles: list | None = None,
    llm_result: dict | None = None,
) -> GradeResult:
    """Assemble a GradeResult. `llm_result`, if provided, is the constrained
    JSON returned by services.llm_grader.grade(); when None, the deterministic
    path is authoritative."""
    diags = _soften(analyse(submission), mode)
    diet = diet_score(submission)
    rubric_spec = _rubric_for(mode)

    if llm_result:
        used_llm = True
        rubric = [
            RubricScore(label=lbl, score=int(llm_result.get("rubric", {}).get(lbl, 0)), out_of=out)
            for lbl, out in rubric_spec
        ]
        total = sum(r.score for r in rubric)
        out_of = sum(r.out_of for r in rubric)
        strengths = list(llm_result.get("strengths", []))
        improvements = list(llm_result.get("improvements", []))
        quality = total / out_of if out_of else 0.0
        model_revision = llm_result.get("model_revision", "")
        coaching_note = llm_result.get("coaching_note", "")
    else:
        used_llm = False
        quality = _deterministic_quality(diags, diet.word_count)
        out_of = sum(o for _, o in rubric_spec)
        # spread the single quality proxy across bands as an honest placeholder
        rubric = [RubricScore(label=lbl, score=int(round(quality * out)), out_of=out) for lbl, out in rubric_spec]
        total = sum(r.score for r in rubric)
        strengths = _auto_strengths(diet, mode)
        improvements = _auto_improvements(diags)
        model_revision = ""
        coaching_note = ""

    xp = xp_for_attempt(
        max_xp=exercise.max_xp,
        quality=quality,
        hint_level=hint_level,
        attempt_number=attempt_number,
    )

    return GradeResult(
        total=total,
        out_of=out_of,
        rubric=rubric,
        strengths=strengths,
        improvements=improvements,
        diagnostics=diags,
        diet=diet,
        xp_awarded=xp,
        used_llm=used_llm,
        passed=quality >= 0.7,
        model_revision=model_revision,
        coaching_note=coaching_note,
    )


def _auto_strengths(diet, mode: Mode) -> list[str]:
    out = []
    if diet.verdict in {"lean", "fit-and-trim"}:
        out.append("Lean prose: low zombie-noun and preposition load.")
    if diet.mean_sentence_len and diet.mean_sentence_len < 22:
        out.append("Controlled sentence length.")
    if not out:
        out.append("Submission received. Tighten the flagged spans to lift the score.")
    return out


def _auto_improvements(diags: list[Diagnostic]) -> list[dict]:
    out = []
    seen = set()
    for d in diags:
        if d.type in seen:
            continue
        seen.add(d.type)
        out.append({"issue": d.message, "suggestion": f"Review the highlighted '{d.text}'."})
        if len(out) >= 4:
            break
    return out
