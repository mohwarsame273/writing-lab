"""Exercise bank loading and sequencing.

Exercises live in knowledge/exercises.json so non-engineers can author them.
Selection is mode-aware: academic and literary draw from different banks. The
sequencer prefers skills that are due for spaced practice, then fills with
unseen exercises for the current mode.
"""
from __future__ import annotations

import json
from pathlib import Path

from domain.models import Exercise, Mode

_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


def _coerce_mode(value: str) -> Mode | str:
    if value == "both":
        return "both"
    return Mode(value)


def load_exercises(path: Path | None = None) -> list[Exercise]:
    path = path or (_KNOWLEDGE_DIR / "exercises.json")
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: list[Exercise] = []
    for r in raw:
        out.append(
            Exercise(
                exercise_id=r["exercise_id"],
                kind=r["kind"],
                mode=_coerce_mode(r.get("mode", "both")),
                skill=r["skill"],
                prompt=r["prompt"],
                seed_text=r.get("seed_text", ""),
                target=r.get("target", ""),
                options=r.get("options", []),
                answer_index=r.get("answer_index"),
                hints=r.get("hints", []),
                rule_ids=r.get("rule_ids", []),
                max_xp=r.get("max_xp", 100),
                difficulty=r.get("difficulty", 1),
            )
        )
    return out


def for_mode(exercises: list[Exercise], mode: Mode) -> list[Exercise]:
    return [e for e in exercises if e.mode == mode or e.mode == "both"]


def next_exercise(
    exercises: list[Exercise],
    mode: Mode,
    completed_ids: set[str],
    due_skills: list[str] | None = None,
) -> Exercise | None:
    """Pick the next exercise: prioritise due skills, then unseen, then anything.
    Deliberately deterministic so the completing agent can reason about flow;
    add spacing/interleaving policy on top later."""
    pool = for_mode(exercises, mode)
    if not pool:
        return None

    due_skills = due_skills or []
    unseen = [e for e in pool if e.exercise_id not in completed_ids]

    for skill in due_skills:
        for e in unseen:
            if e.skill == skill:
                return e

    if unseen:
        by_kind = {}
        for e in unseen:
            by_kind.setdefault(e.kind, []).append(e)
            
        for k in by_kind:
            by_kind[k].sort(key=lambda e: e.difficulty)
            
        kinds_order = [
            "sentence_completion", "diagnostic_selection", "transitions",
            "rewrite", "constrained_composition", "paragraph_revision", "free_write"
        ]
        available_kinds = [k for k in kinds_order if k in by_kind]
        if not available_kinds:
            available_kinds = list(by_kind.keys())
            
        if available_kinds:
            idx = len(completed_ids) % len(available_kinds)
            target_kind = available_kinds[idx]
            return by_kind[target_kind][0]
            
        unseen.sort(key=lambda e: e.difficulty)
        return unseen[0]

    # everything seen: cycle back to the easiest for review
    pool.sort(key=lambda e: e.difficulty)
    return pool[0]
