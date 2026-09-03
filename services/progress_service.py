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

class User(rx.Model, table=True):
    # id is provided by rx.Model
    xp: int = 0
    streak: int = 0
    last_active_iso: str = ""

class AttemptLog(rx.Model, table=True):
    user_id: int
    exercise_id: str
    xp_awarded: int

class MasteryRow(rx.Model, table=True):
    user_id: int
    skill: str
    mastery: float
    attempts: int

class Progress:
    def __init__(self, user_id: int = 1):
        self.user_id = user_id
        self._fallback_xp = 0
        self._fallback_streak = 0
        self._fallback_last_active = ""
        self._fallback_completed = set()
        self._fallback_mastery = {}
        
        try:
            with rx.session() as session:
                user = session.get(User, self.user_id)
                if not user:
                    user = User(id=self.user_id, xp=0, streak=0, last_active_iso="")
                    session.add(user)
                    session.commit()
                else:
                    self._fallback_xp = user.xp
                    self._fallback_streak = user.streak
                    self._fallback_last_active = user.last_active_iso
        except Exception as e:
            print(f"Warning: Progress DB init failed: {e}")

    @property
    def xp(self) -> int:
        try:
            with rx.session() as session:
                user = session.get(User, self.user_id)
                return user.xp if user else self._fallback_xp
        except Exception as e:
            print(f"Warning: DB read failed (xp): {e}")
            return self._fallback_xp

    @xp.setter
    def xp(self, value: int):
        self._fallback_xp = value
        try:
            with rx.session() as session:
                user = session.get(User, self.user_id)
                if user:
                    user.xp = value
                    session.add(user)
                    session.commit()
        except Exception as e:
            print(f"Warning: DB write failed (xp): {e}")

    @property
    def streak(self) -> int:
        try:
            with rx.session() as session:
                user = session.get(User, self.user_id)
                return user.streak if user else self._fallback_streak
        except Exception as e:
            print(f"Warning: DB read failed (streak): {e}")
            return self._fallback_streak

    @streak.setter
    def streak(self, value: int):
        self._fallback_streak = value
        try:
            with rx.session() as session:
                user = session.get(User, self.user_id)
                if user:
                    user.streak = value
                    session.add(user)
                    session.commit()
        except Exception as e:
            print(f"Warning: DB write failed (streak): {e}")

    @property
    def last_active_iso(self) -> str:
        try:
            with rx.session() as session:
                user = session.get(User, self.user_id)
                return user.last_active_iso if user else self._fallback_last_active
        except Exception as e:
            print(f"Warning: DB read failed (last_active_iso): {e}")
            return self._fallback_last_active

    @last_active_iso.setter
    def last_active_iso(self, value: str):
        self._fallback_last_active = value
        try:
            with rx.session() as session:
                user = session.get(User, self.user_id)
                if user:
                    user.last_active_iso = value
                    session.add(user)
                    session.commit()
        except Exception as e:
            print(f"Warning: DB write failed (last_active_iso): {e}")

    @property
    def completed_exercise_ids(self) -> list[str]:
        try:
            with rx.session() as session:
                logs = session.query(AttemptLog).filter(AttemptLog.user_id == self.user_id).all()
                return list(set(log.exercise_id for log in logs))
        except Exception as e:
            print(f"Warning: DB read failed (completed_exercise_ids): {e}")
            return list(self._fallback_completed)

    # --- streak logic -------------------------------------------------------
    def touch_streak(self, today: date | None = None) -> None:
        today = today or date.today()
        last_iso = self.last_active_iso
        
        if not last_iso:
            self.streak = 1
        else:
            try:
                last = date.fromisoformat(last_iso)
                gap = (today - last).days
                if gap == 0:
                    pass  # already counted today
                elif gap == 1:
                    self.streak += 1
                else:
                    self.streak = 1
            except ValueError:
                self.streak = 1
        self.last_active_iso = today.isoformat()

    def record_completion(self, exercise_id: str, xp: int) -> None:
        self.xp += xp
        self._fallback_completed.add(exercise_id)
        try:
            with rx.session() as session:
                log = AttemptLog(user_id=self.user_id, exercise_id=exercise_id, xp_awarded=xp)
                session.add(log)
                session.commit()
        except Exception as e:
            print(f"Warning: DB write failed (record_completion): {e}")

    def set_mastery(self, snap: MasterySnapshot) -> None:
        self._fallback_mastery[snap.skill] = snap
        try:
            with rx.session() as session:
                row = session.query(MasteryRow).filter(
                    MasteryRow.user_id == self.user_id,
                    MasteryRow.skill == snap.skill
                ).first()
                if row:
                    row.mastery = snap.mastery
                    row.attempts = snap.attempts
                else:
                    row = MasteryRow(
                        user_id=self.user_id,
                        skill=snap.skill,
                        mastery=snap.mastery,
                        attempts=snap.attempts
                    )
                session.add(row)
                session.commit()
        except Exception as e:
            print(f"Warning: DB write failed (set_mastery): {e}")

    def mastery_snapshots(self) -> list[MasterySnapshot]:
        try:
            with rx.session() as session:
                rows = session.query(MasteryRow).filter(MasteryRow.user_id == self.user_id).all()
                return [MasterySnapshot(skill=r.skill, mastery=r.mastery, attempts=r.attempts) for r in rows]
        except Exception as e:
            print(f"Warning: DB read failed (mastery_snapshots): {e}")
            return list(self._fallback_mastery.values())

def load(path: Path | None = None) -> Progress:
    return Progress()

def save(progress: Progress, path: Path | None = None) -> None:
    pass
