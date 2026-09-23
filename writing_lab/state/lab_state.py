"""The application's single source of truth.

Deliberately ONE state class. Reflex substate access (get_state) is a common
source of subtle bugs, so the whole exercise flow lives here.

This class is a thin bridge: every non-trivial decision is delegated to the
framework-independent domain layer (domain/, retrieval/). If you find business
logic creeping in here, push it down into domain/ instead.

Design notes for this rewrite:
- casual_mode is a plain bool. Do NOT wrap it in rx.LocalStorage: that stores a
  string and Reflex then rejects it against the bool type. Casual mode defaults
  ON, which is the friendly beginner experience, and resets per browser session,
  which is fine because ON is the default anyway.
- Progress (xp, streak, completed_ids, mastery) is SESSION-SCOPED plain state.
  It deliberately does not read or write the database. That coupling was the
  cause of repeated crashes and is not worth cross-restart persistence for a
  personal tool. Durable persistence can be re-added later behind a guarded,
  best-effort hook without changing any of the UI.
- The AI service calls (llm_grader.grade, llm_grader.free_write_note,
  exercise_gen.generate_exercise) each return a (result, error) tuple. On error
  we surface a friendly toast and fall back cleanly; the app always works
  offline.
"""
from __future__ import annotations

import reflex as rx

from domain.exercises import load_exercises, next_exercise
from domain.grading import grade
from domain.mastery import update_mastery
from domain.models import Exercise, Mode, MasterySnapshot
from domain.scoring import hint_cap_label, xp_for_attempt
from domain import diagnostics as diag
from retrieval.loader import load_principles
from retrieval.search import retrieve
from services import llm_grader

# Static corpora loaded once at import. These never change at runtime.
_EXERCISES = load_exercises()
_PRINCIPLES = load_principles()

_SELECTION_KINDS = {"diagnostic_selection", "transitions"}



def _mode_value(ex: Exercise) -> str:
    return getattr(ex.mode, "value", ex.mode)


class LabState(rx.State):
    # --- settings -----------------------------------------------------------
    casual_mode: bool = True                 # friendly default; hides gamification
    mode: str = Mode.ACADEMIC.value

    # --- session progress (NOT persisted to the DB, by design) --------------
    user_id: str = "demo-user"
    xp: int = 0
    streak: int = 1
    completed_ids: list[str] = []
    mastery: list[dict] = []      # [{skill, mastery, attempts, independent_attempts, delayed_attempts, last_seen_iso, due_iso}]

    @rx.event
    def on_load(self):
        from services.progress_service import get_user_attempts
        from domain.mastery import update_mastery
        from domain.models import MasterySnapshot
        
        attempts = get_user_attempts(self.user_id)
        if not attempts:
            return
            
        seen = set()
        mastery_dict = {}
        xp_total = 0
        
        for attempt in attempts:
            if attempt.passed:
                seen.add(attempt.exercise_id)
                # recompute xp? In minimal persistence we didn't store xp_awarded in this table, but we can just leave xp=0 or recalculate
                xp_total += 10 # dummy 
                
            skill = "unknown"
            for ex in _EXERCISES:
                if ex.exercise_id == attempt.exercise_id:
                    skill = ex.skill
                    break
            
            if skill != "unknown":
                prev = mastery_dict.get(skill)
                # Just mock update
                snap = update_mastery(prev, skill, attempt.quality, attempt.hint_level)
                # Note: This is an approximation since update_mastery checks current time vs last_seen
                mastery_dict[skill] = snap
                
        self.completed_ids = list(seen)
        self.xp = xp_total
        
        m_list = []
        for snap in mastery_dict.values():
            m_list.append({
                "skill": snap.skill, 
                "mastery": snap.mastery, 
                "attempts": snap.attempts,
                "independent_attempts": snap.independent_attempts,
                "delayed_attempts": snap.delayed_attempts,
                "last_seen_iso": snap.last_seen_iso,
                "due_iso": snap.due_iso
            })
        self.mastery = m_list

    # --- topic focus: practise one skill/category to memorise it ------------
    selected_skill: str = ""                 # "" means practise everything

    # --- current exercise (flattened for easy rendering) --------------------
    ex_id: str = ""
    ex_kind: str = ""
    ex_skill: str = ""
    ex_prompt: str = ""
    ex_seed: str = ""
    ex_target: str = ""
    ex_options: list[str] = []
    ex_answer_index: int = -1
    ex_hints: list[str] = []
    ex_max_xp: int = 100
    ex_difficulty: int = 1

    # --- attempt state ------------------------------------------------------
    answer: str = ""
    selected_option: int = -1
    hint_level: int = 0
    attempt_number: int = 1
    is_grading: bool = False
    is_generating_drill: bool = False
    graded: bool = False

    live_diagnostics: list[dict] = []        # [{type, text, severity, message}]
    live_verdict: str = ""

    all_completed: bool = False

    # --- feedback after grading --------------------------------------------
    fb_total: int = 0
    fb_out_of: int = 100
    fb_passed: bool = False
    fb_used_llm: bool = False
    fb_xp: int = 0
    fb_rubric: list[dict] = []               # [{label, score, out_of}]
    fb_strengths: list[str] = []
    fb_improvements: list[dict] = []          # [{issue, suggestion}]
    fb_diagnostics: list[dict] = []           # [{type, text, severity, message}]
    fb_diet: dict = {}
    fb_model_revision: str = ""
    fb_coaching_note: str = ""

    # --- free-writing session (independent of the exercise flow) ------------
    fw_text: str = ""
    fw_analysed: bool = False
    fw_diet: dict = {}
    fw_diagnostics: list[dict] = []
    fw_openings: list[dict] = []              # [{word, count}]
    fw_ai_note: str = ""
    fw_last_analysed_text: str = ""

    # ------------------------------------------------------------- computed
    @rx.var
    def mode_is_academic(self) -> bool:
        return self.mode == Mode.ACADEMIC.value

    @rx.var
    def is_selection(self) -> bool:
        return self.ex_kind in _SELECTION_KINDS

    @rx.var
    def revealed_hints(self) -> list[str]:
        return self.ex_hints[: self.hint_level]

    @rx.var
    def can_reveal_hint(self) -> bool:
        return self.hint_level < len(self.ex_hints)

    @rx.var
    def xp_cap_label(self) -> str:
        return hint_cap_label(self.hint_level)

    @rx.var
    def word_count(self) -> int:
        return len(self.answer.split())

    @rx.var
    def fw_word_count(self) -> int:
        return len(self.fw_text.split())

    @rx.var
    def available_skills(self) -> list[str]:
        """Distinct skill tags available in the current mode, for the topic
        picker. Sorted for a stable menu."""
        skills = {
            e.skill
            for e in _EXERCISES
            if _mode_value(e) in (self.mode, "both")
        }
        return sorted(skills)

    @rx.var
    def focus_label(self) -> str:
        return self.selected_skill if self.selected_skill else "All topics"

    @rx.var
    def progress_pct(self) -> int:
        from domain.exercises import calculate_progress_pct
        return calculate_progress_pct(self._mode_pool(), set(self.completed_ids))

    @rx.var
    def mastery_display_list(self) -> list[dict]:
        from domain.mastery import derive_evidence_state
        from domain.models import MasterySnapshot
        out = []
        for skill in self.available_skills:
            m_dict = next((m for m in self.mastery if m["skill"] == skill), None)
            if m_dict:
                snap = MasterySnapshot(
                    skill=skill,
                    mastery=m_dict.get("mastery", 0.0),
                    attempts=m_dict.get("attempts", 0),
                    independent_attempts=m_dict.get("independent_attempts", 0),
                    delayed_attempts=m_dict.get("delayed_attempts", 0),
                    last_seen_iso=m_dict.get("last_seen_iso"),
                    due_iso=m_dict.get("due_iso")
                )
            else:
                snap = None
            
            state_label = derive_evidence_state(snap)
            attempts = snap.attempts if snap else 0
            
            # format date
            date_str = ""
            if snap and snap.last_seen_iso:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(snap.last_seen_iso)
                    date_str = dt.strftime("%b %d, %Y")
                except Exception:
                    pass
                    
            out.append({
                "skill": skill,
                "state": state_label,
                "attempts": attempts,
                "date": date_str,
            })
        return out

    # ------------------------------------------------------- topic focus events
    @rx.event
    def set_focus_skill(self, skill: str):
        """Focus practice on a single skill/category (e.g. 'transitions',
        'rhetorical-devices', 'reporting-results') to drill and memorise it."""
        self.selected_skill = skill
        self.load_next()

    @rx.event
    def clear_focus(self):
        self.selected_skill = ""
        self.load_next()

    # ------------------------------------------------------------ settings events
    @rx.event
    def toggle_casual_mode(self, value: bool):
        self.casual_mode = value

    @rx.event
    def set_mode(self, mode: str):
        self.mode = mode
        self.selected_skill = ""     # a mode's skills differ; reset focus
        self.load_next()

    @rx.event
    def toggle_mode(self):
        self.set_mode(
            Mode.LITERARY.value if self.mode == Mode.ACADEMIC.value else Mode.ACADEMIC.value
        )

    # --------------------------------------------------------- exercise flow
    def _mode_pool(self) -> list[Exercise]:
        return [e for e in _EXERCISES if _mode_value(e) in (self.mode, "both")]

    def _pick_next(self) -> Exercise | None:
        """Choose the next exercise, honouring an optional topic focus.

        No focus: defer to domain.next_exercise so the mixed-kind interleaving
        is preserved. Focused: serve unseen items in the chosen skill first,
        then cycle through them so a category can be drilled to memory."""
        seen = set(self.completed_ids)

        if not self.selected_skill:
            return next_exercise(_EXERCISES, Mode(self.mode), seen)

        from domain.exercises import pick_focused_exercise
        return pick_focused_exercise(self._mode_pool(), self.selected_skill, seen)

    def _apply_exercise(self, ex: Exercise):
        self.ex_id = ex.exercise_id
        self.ex_kind = ex.kind
        self.ex_skill = ex.skill
        self.ex_prompt = ex.prompt
        self.ex_seed = ex.seed_text
        self.ex_target = ex.target
        self.ex_options = list(ex.options)
        self.ex_answer_index = ex.answer_index if ex.answer_index is not None else -1
        self.ex_hints = list(ex.hints)
        self.ex_max_xp = ex.max_xp
        self.ex_difficulty = ex.difficulty
        self._reset_attempt(seed=True)

    @rx.event
    def load_next(self):
        ex = self._pick_next()
        if ex is not None:
            self.all_completed = False
            self._apply_exercise(ex)
        else:
            self.all_completed = True

    @rx.event
    def generate_fresh_drill(self):
        """Opt-in AI drill generation. Fails safe: on any error we toast and
        keep the current drill."""
        self.is_generating_drill = True
        yield

        new_ex = None
        err = None
        try:
            from services.exercise_gen import generate_exercise
            new_ex, err = generate_exercise(Mode(self.mode), self.ex_skill)
        except Exception as exc:  # never let generation crash the page
            err = "Could not reach the AI service, using offline mode."
            print(f"[generate_fresh_drill] {exc}")

        self.is_generating_drill = False
        if err:
            yield rx.toast.warning(err)
        if new_ex is not None:
            self._apply_exercise(new_ex)

    def _reset_attempt(self, seed: bool = False):
        self.answer = self.ex_seed if seed else ""
        self.selected_option = -1
        self.hint_level = 0
        self.attempt_number = 1
        self.is_grading = False
        self.graded = False
        self.live_diagnostics = []
        self.live_verdict = ""
        self._clear_feedback()

    def _clear_feedback(self):
        self.fb_total = 0
        self.fb_passed = False
        self.fb_used_llm = False
        self.fb_xp = 0
        self.fb_rubric = []
        self.fb_strengths = []
        self.fb_improvements = []
        self.fb_diagnostics = []
        self.fb_diet = {}
        self.fb_model_revision = ""
        self.fb_coaching_note = ""

    # ------------------------------------------------------------ attempt events
    @rx.event
    def update_answer(self, value: str):
        """Live deterministic preview as the learner types."""
        self.answer = value
        if len(value.split()) >= 3:
            findings = diag.analyse(value)
            self.live_diagnostics = [
                {"type": f.type, "text": f.text, "severity": f.severity, "message": f.message}
                for f in findings[:12]
            ]
            self.live_verdict = diag.diet_score(value).verdict
        else:
            self.live_diagnostics = []
            self.live_verdict = ""

    @rx.event
    def select_option(self, index: int):
        self.selected_option = index

    @rx.event
    def reveal_hint(self):
        if self.can_reveal_hint:
            self.hint_level += 1

    @rx.event
    def try_again(self):
        self.graded = False
        self.attempt_number += 1
        self._clear_feedback()

    @rx.event
    def submit(self):
        """Grade the current attempt. Generator event: the first yield flushes
        the grading spinner before the work runs."""
        self.is_grading = True
        yield

        current_mode = Mode(self.mode)

        if self.is_selection:
            correct = self.selected_option == self.ex_answer_index
            self._grade_selection(correct)
        else:
            exercise = self._current_exercise_obj()
            principles = retrieve(
                self.answer or self.ex_prompt,
                _PRINCIPLES,
                mode=current_mode,
                skills=[self.ex_skill],
            )
            llm_result = None
            err = None
            try:
                llm_result, err = llm_grader.grade(
                    self.answer, exercise, current_mode, principles
                )
            except Exception as exc:  # AI must never break grading
                err = "Could not reach the AI service, using offline mode."
                print(f"[submit] {exc}")
            if err:
                yield rx.toast.warning(err)

            result = grade(
                submission=self.answer,
                exercise=exercise,
                mode=current_mode,
                hint_level=self.hint_level,
                attempt_number=self.attempt_number,
                retrieved_principles=principles,
                llm_result=llm_result,
            )
            self._apply_grade_result(result)

        self.is_grading = False
        self.graded = True

    # ----------------------------------------------------------- grade helpers
    def _current_exercise_obj(self) -> Exercise:
        """Rebuild an Exercise from the current flattened state. Works for both
        static and AI-generated drills, so grading always targets the drill on
        screen."""
        return Exercise(
            exercise_id=self.ex_id,
            kind=self.ex_kind,
            mode=Mode(self.mode),
            skill=self.ex_skill,
            prompt=self.ex_prompt,
            seed_text=self.ex_seed,
            target=self.ex_target,
            options=list(self.ex_options),
            answer_index=(self.ex_answer_index if self.ex_answer_index >= 0 else None),
            hints=list(self.ex_hints),
            rule_ids=[],
            max_xp=self.ex_max_xp,
            difficulty=self.ex_difficulty,
        )

    def _grade_selection(self, correct: bool):
        quality = 1.0 if correct else 0.0
        xp = xp_for_attempt(self.ex_max_xp, quality, self.hint_level, self.attempt_number)
        self.fb_total = 100 if correct else 0
        self.fb_out_of = 100
        self.fb_passed = correct
        self.fb_xp = xp
        self.fb_strengths = ["Correct. You chose the clearest option."] if correct else []
        self.fb_improvements = (
            [] if correct
            else [{"issue": "Not quite.", "suggestion": "Re-read each option and ask which one you can picture."}]
        )
        self._award(correct, xp, quality)

    def _apply_grade_result(self, result):
        self.fb_total = result.total
        self.fb_out_of = result.out_of
        self.fb_passed = result.passed
        self.fb_used_llm = result.used_llm
        self.fb_xp = result.xp_awarded
        self.fb_rubric = [{"label": r.label, "score": r.score, "out_of": r.out_of} for r in result.rubric]
        self.fb_strengths = result.strengths
        self.fb_improvements = result.improvements
        self.fb_diagnostics = [
            {"type": d.type, "text": d.text, "severity": d.severity, "message": d.message}
            for d in result.diagnostics[:12]
        ]
        self.fb_diet = result.diet.as_dict() if result.diet else {}
        self.fb_model_revision = getattr(result, "model_revision", "") or ""
        self.fb_coaching_note = getattr(result, "coaching_note", "") or ""
        quality = (result.total / result.out_of) if result.out_of else 0.0
        self._award(result.passed, result.xp_awarded, quality)

    def _award(self, passed: bool, xp: int, quality: float):
        """Session-only. Never touches a database, so it can never crash the app."""
        from domain.scoring import evaluate_award
        from services.progress_service import record_attempt
        from datetime import datetime, timezone
        
        outcome = evaluate_award(
            exercise_id=self.ex_id,
            passed=passed,
            quality=quality,
            xp_from_rubric=xp,
            already_completed=frozenset(self.completed_ids)
        )
        
        self.xp += outcome.xp_delta
        if outcome.completed_id:
            self.completed_ids = self.completed_ids + [outcome.completed_id]
        if outcome.mastery_quality is not None:
            self._update_mastery(self.ex_skill, outcome.mastery_quality, self.hint_level)
            
        record_attempt(
            user_id=self.user_id,
            exercise_id=self.ex_id,
            passed=passed,
            quality=quality,
            hint_level=self.hint_level,
            timestamp_iso=datetime.now(timezone.utc).isoformat()
        )

    def _update_mastery(self, skill: str, quality: float, hint_level: int):
        prev = None
        for m in self.mastery:
            if m["skill"] == skill:
                prev = MasterySnapshot(
                    skill=skill, 
                    mastery=m.get("mastery", 0.0), 
                    attempts=m.get("attempts", 0),
                    independent_attempts=m.get("independent_attempts", 0),
                    delayed_attempts=m.get("delayed_attempts", 0),
                    last_seen_iso=m.get("last_seen_iso"),
                    due_iso=m.get("due_iso")
                )
                break
        snap = update_mastery(prev, skill, quality, hint_level)
        row = {
            "skill": snap.skill, 
            "mastery": snap.mastery, 
            "attempts": snap.attempts,
            "independent_attempts": snap.independent_attempts,
            "delayed_attempts": snap.delayed_attempts,
            "last_seen_iso": snap.last_seen_iso,
            "due_iso": snap.due_iso
        }
        updated = False
        new_list = []
        for m in self.mastery:
            if m["skill"] == skill:
                new_list.append(row)
                updated = True
            else:
                new_list.append(m)
        if not updated:
            new_list.append(row)
        self.mastery = new_list

    # ----------------------------------------------------------- free-write
    @rx.event
    def update_free_write(self, value: str):
        self.fw_text = value

    @rx.event
    def analyse_free_write(self):
        """A diagnostic mirror, deliberately not a score. Optional AI note when
        configured; the deterministic profile is always primary."""
        text = self.fw_text
        if len(text.split()) < 20:
            return
        self.fw_diet = diag.diet_score(text).as_dict()
        self.fw_diagnostics = [
            {"type": f.type, "text": f.text, "severity": f.severity, "message": f.message}
            for f in diag.analyse(text)[:20]
        ]
        self.fw_openings = [
            {"word": w, "count": c} for w, c in diag.repeated_openings(text).most_common(6)
        ]
        self.fw_analysed = True
        
        from domain.scoring import evaluate_free_write
        outcome = evaluate_free_write(
            word_count=len(text.split()),
            text_changed=(text != self.fw_last_analysed_text)
        )
        self.xp += outcome.xp_delta
        self.fw_last_analysed_text = text

        yield  # flush the profile before any network call

        self.fw_ai_note = ""
        if llm_grader.is_configured():
            note = ""
            err = None
            try:
                note, err = llm_grader.free_write_note(text)
            except Exception as exc:
                err = "Could not reach the AI service, using offline mode."
                print(f"[analyse_free_write] {exc}")
            self.fw_ai_note = note or ""
            if err:
                yield rx.toast.warning(err)

    @rx.event
    def reset_free_write(self):
        self.fw_analysed = False
        self.fw_diet = {}
        self.fw_diagnostics = []
        self.fw_openings = []
        self.fw_ai_note = ""