"""Progress persistence.

For the single-user MVP this keeps XP, streak, completed exercises and mastery
snapshots in a small dataclass that the UI state mirrors, plus optional JSON
save/load so a demo survives a restart. Multi-user persistence (SQLModel /
Reflex's rx.Model, SQLite -> Postgres) is a clearly-marked upgrade.

Keeping persistence here, not in the Reflex state class, is deliberate: the UI
shell stays disposable and this logic stays testable without a browser.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional

import reflex as rx

from domain.models import MasterySnapshot

class AttemptRecord(rx.Model, table=True):
    user_id: str
    exercise_id: str
    passed: bool
    quality: float
    hint_level: int
    timestamp_iso: str

def get_user_attempts(user_id: str) -> list[AttemptRecord]:
    try:
        with rx.session() as session:
            return session.query(AttemptRecord).filter(AttemptRecord.user_id == user_id).all()
    except Exception as e:
        print(f"Warning: DB read failed (get_user_attempts): {e}")
        return []

def record_attempt(
    user_id: str,
    exercise_id: str,
    passed: bool,
    quality: float,
    hint_level: int,
    timestamp_iso: str
) -> None:
    try:
        with rx.session() as session:
            log = AttemptRecord(
                user_id=user_id,
                exercise_id=exercise_id,
                passed=passed,
                quality=quality,
                hint_level=hint_level,
                timestamp_iso=timestamp_iso
            )
            session.add(log)
            session.commit()
    except Exception as e:
        print(f"Warning: DB write failed (record_attempt): {e}")
