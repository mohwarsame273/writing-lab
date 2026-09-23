import pytest
from writing_lab.state.lab_state import LabState, _EXERCISES
from domain.models import Exercise, Mode
import reflex as rx
from services.progress_service import AttemptRecord

@pytest.fixture(autouse=True)
def clean_db():
    from rxconfig import config
    db_url = config.db_url
    if not db_url or not db_url.startswith("sqlite:///"):
        pytest.exit(f"Safety abort: Refusing to wipe database. DB_URL must be a local SQLite database, got: {db_url}")
        
    with rx.session() as session:
        session.query(AttemptRecord).delete()
        session.commit()

def test_casual_mode_retains_history():
    state = LabState()
    state.user_id = "test_casual"
    state.casual_mode = True
    state.completed_ids = []
    real_ex = _EXERCISES[0]
    state.ex_id = real_ex.exercise_id
    state.ex_skill = real_ex.skill
    state.mastery = []
    state.hint_level = 0
    
    state._award(True, 10, 1.0)
    
    assert real_ex.exercise_id in state.completed_ids, "Failed: Completion not recorded in memory."
    assert state.xp > 0, "Failed: XP not recorded in memory."
    assert len(state.mastery) > 0, "Failed: Mastery not recorded in memory."
    
    # Simulate restart
    new_state = LabState()
    new_state.user_id = "test_casual"
    
    new_state.on_load()
    
    assert real_ex.exercise_id in new_state.completed_ids, "Failed: Completion did not rehydrate."
    assert new_state.xp > 0, "Failed: XP did not rehydrate."
    assert len(new_state.mastery) > 0, "Failed: Mastery did not rehydrate."

def test_pick_next_exhausts_pool():
    state = LabState()
    state.mode = Mode.ACADEMIC.value
    pool = state._mode_pool()
    
    # Positive twin: Non-exhausted pool
    state.completed_ids = []
    ex = state._pick_next()
    assert ex is not None, "Failed: Did not pick an item when pool was not exhausted."
    
    # Negative twin: Exhausted pool
    state.completed_ids = [e.exercise_id for e in pool]
    ex2 = state._pick_next()
    assert ex2 is None, "Failed: Picked an item when the pool should be exhausted."

def test_progress_pct_ignores_generated_ids():
    state = LabState()
    state.mode = Mode.ACADEMIC.value
    
    pool = state._mode_pool()
    # Add one static completed and two generated
    state.completed_ids = [pool[0].exercise_id, "gen-1", "gen-2"]
    
    pct = state.progress_pct
    expected_pct = int(round(100 * 1 / (len(pool) or 1)))
    assert pct == expected_pct, f"Failed: Progress percentage mixes generated IDs (got {pct}, expected {expected_pct})."

def test_failed_attempt_does_not_mark_completed():
    state = LabState()
    state.user_id = "test_fail"
    state.ex_id = "ex-1"
    state.ex_skill = "skill-1"
    state.ex_max_xp = 100
    state.hint_level = 0
    state.attempt_number = 1
    state.casual_mode = False
    state.completed_ids = []
    state.mastery = []
    
    class FakeResult:
        def __init__(self, passed: bool):
            self.total = 0
            self.out_of = 100
            self.passed = passed
            self.used_llm = False
            self.xp_awarded = 10
            self.rubric = []
            self.strengths = []
            self.improvements = []
            self.diagnostics = []
            self.diet = None
            self.model_revision = ""
            self.coaching_note = ""

    # Negative twin: Failed attempt
    state._apply_grade_result(FakeResult(passed=False))
    assert "ex-1" not in state.completed_ids, "Failed: Failed attempt counted as completed."
    
    # Positive twin: Passed attempt
    state.ex_id = "ex-2"
    state._apply_grade_result(FakeResult(passed=True))
    assert "ex-2" in state.completed_ids, "Failed: Passed attempt did not count as completed."

def test_free_write_awards_xp_only_on_change():
    state = LabState()
    state.casual_mode = False
    state.xp = 0
    state.fw_text = "This is a long enough text with more than twenty words so that it passes the length check. " * 3
    
    list(state.analyse_free_write())
    xp1 = state.xp
    assert xp1 > 0, "Failed: Initial free write did not award XP."
    
    list(state.analyse_free_write())
    xp2 = state.xp
    
    assert xp2 == xp1, "Failed: Free writing awarded repeated XP for unchanged text."
    
    # Third step: change text and assert XP increases
    state.fw_text += " This is an additional sentence to ensure the text has changed."
    list(state.analyse_free_write())
    xp3 = state.xp
    
    assert xp3 > xp2, "Failed: Changed free write did not award additional XP."
