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


def update_mastery(prev: MasterySnapshot | None, skill: str, quality: float, hint_level: int = 0) -> MasterySnapshot:
    """Fold one attempt's quality (0..1) into the running mastery estimate and
    compute the next due date."""
    now = datetime.now(timezone.utc)
    
    if prev is None:
        mastery = quality
        attempts = 1
        independent_attempts = 1 if hint_level == 0 and quality >= 0.8 else 0
        delayed_attempts = 0
    else:
        mastery = (1 - _ALPHA) * prev.mastery + _ALPHA * quality
        attempts = prev.attempts + 1
        is_independent = 1 if hint_level == 0 and quality >= 0.8 else 0
        independent_attempts = prev.independent_attempts + is_independent
        delayed_attempts = prev.delayed_attempts
        
        if is_independent and prev.last_seen_iso:
            try:
                last_seen = datetime.fromisoformat(prev.last_seen_iso)
                if (now - last_seen).total_seconds() > 86400: # 1 day
                    delayed_attempts += 1
            except ValueError:
                pass

    # streak drives the interval; approximate streak from mastery band
    band = min(int(mastery * len(_INTERVALS)), len(_INTERVALS) - 1)
    due = now + timedelta(days=_INTERVALS[band])

    return MasterySnapshot(
        skill=skill,
        mastery=round(mastery, 4),
        attempts=attempts,
        independent_attempts=independent_attempts,
        delayed_attempts=delayed_attempts,
        last_seen_iso=now.isoformat(),
        due_iso=due.isoformat(),
    )


def derive_evidence_state(snap: MasterySnapshot | None) -> str:
    """Derive the current evidence state from recorded attempts."""
    if snap is None or snap.attempts == 0:
        return "Not yet sampled"
    if snap.delayed_attempts > 0:
        return "Demonstrated again after a delay"
    if snap.independent_attempts > 0:
        return "Demonstrated in independent practice"
    return "Practised with support"

def due_skills(snapshots: list[MasterySnapshot], now: datetime | None = None) -> list[str]:
    """Skills whose spaced-repetition slot has arrived, weakest first."""
    now = now or datetime.now(timezone.utc)
    due = []
    for s in snapshots:
        if not s.due_iso or datetime.fromisoformat(s.due_iso) <= now:
            due.append(s)
    due.sort(key=lambda s: s.mastery)
    return [s.skill for s in due]
