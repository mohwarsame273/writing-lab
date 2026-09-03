"""Skill mastery and spaced repetition.

Mastery is an exponential moving average of attempt quality per skill, tracked
separately from XP. When a learner keeps struggling with a pattern, that skill
is rescheduled sooner. This is more educationally useful than a leaderboard.

The scheduling here is a simple, transparent SM-2-lite. Swap in a fuller
algorithm later without changing the public functions.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from domain.models import MasterySnapshot

_ALPHA = 0.35  # weight on the newest attempt in the moving average

# spaced-repetition intervals by consecutive-success streak, in days
_INTERVALS = [0, 1, 3, 7, 16, 35]


def update_mastery(prev: MasterySnapshot | None, skill: str, quality: float) -> MasterySnapshot:
    """Fold one attempt's quality (0..1) into the running mastery estimate and
    compute the next due date."""
    now = datetime.now(timezone.utc)
    if prev is None:
        mastery = quality
        attempts = 1
    else:
        mastery = (1 - _ALPHA) * prev.mastery + _ALPHA * quality
        attempts = prev.attempts + 1

    # streak drives the interval; approximate streak from mastery band
    band = min(int(mastery * len(_INTERVALS)), len(_INTERVALS) - 1)
    due = now + timedelta(days=_INTERVALS[band])

    return MasterySnapshot(
        skill=skill,
        mastery=round(mastery, 4),
        attempts=attempts,
        last_seen_iso=now.isoformat(),
        due_iso=due.isoformat(),
    )


def due_skills(snapshots: list[MasterySnapshot], now: datetime | None = None) -> list[str]:
    """Skills whose spaced-repetition slot has arrived, weakest first."""
    now = now or datetime.now(timezone.utc)
    due = []
    for s in snapshots:
        if not s.due_iso or datetime.fromisoformat(s.due_iso) <= now:
            due.append(s)
    due.sort(key=lambda s: s.mastery)
    return [s.skill for s in due]
