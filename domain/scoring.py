"""XP and hint economics. Pure functions, easy to unit test and tune.

Design rules (after DataCamp):
- Hints are part of the exercise, not a punishment. Each hint lowers the *cap*
  on XP for that attempt but never blocks completion.
- Mistakes never subtract previously earned XP. They affect this attempt's
  score and the mastery estimate only.
- Revising after feedback is rewarded, to encourage iteration.
"""
from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class AwardOutcome:
    xp_delta: int
    completed_id: str | None
    mastery_quality: float | None

def evaluate_award(
    exercise_id: str,
    passed: bool,
    quality: float,
    xp_from_rubric: int,
    already_completed: frozenset[str],
) -> AwardOutcome:
    xp_delta = xp_from_rubric
    
    completed_id = None
    if passed and exercise_id and exercise_id not in already_completed:
        completed_id = exercise_id
        
    mastery_quality = quality
    
    return AwardOutcome(
        xp_delta=xp_delta,
        completed_id=completed_id,
        mastery_quality=mastery_quality
    )

@dataclass(frozen=True)
class FreeWriteOutcome:
    xp_delta: int

def evaluate_free_write(
    word_count: int,
    text_changed: bool
) -> FreeWriteOutcome:
    if word_count < 20 or not text_changed:
        return FreeWriteOutcome(xp_delta=0)
    return FreeWriteOutcome(xp_delta=20)

# fraction of max XP remaining after each successive hint level
# level 0 = no hint, 1 = concept, 2 = location, 3 = transformation, 4 = model reveal
_HINT_MULTIPLIERS = [1.0, 0.85, 0.7, 0.5, 0.25]

_FIRST_TRY_BONUS = 20
_REVISION_BONUS = 15


def xp_for_attempt(
    max_xp: int,
    quality: float,          # 0..1, how well the submission met the target
    hint_level: int,
    attempt_number: int,
    improved_on_previous: bool = False,
) -> int:
    """Return XP for a single graded attempt."""
    mult = _HINT_MULTIPLIERS[min(hint_level, len(_HINT_MULTIPLIERS) - 1)]
    base = max_xp * mult * max(0.0, min(1.0, quality))
    bonus = 0
    if attempt_number == 1 and hint_level == 0 and quality >= 0.8:
        bonus += _FIRST_TRY_BONUS
    if improved_on_previous:
        bonus += _REVISION_BONUS
    return int(round(base + bonus))


def hint_cap_label(hint_level: int) -> str:
    pct = int(_HINT_MULTIPLIERS[min(hint_level, len(_HINT_MULTIPLIERS) - 1)] * 100)
    return f"XP cap: {pct}%"
