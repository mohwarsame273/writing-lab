"""A few real tests for the deterministic core. Run with: python -m pytest -q
(These are pure-Python and do not need Reflex or a browser.)"""
from domain.diagnostics import analyse, diet_score, repeated_openings
from domain.models import Mode
from domain.scoring import xp_for_attempt


def test_flags_nominalisation_and_passive():
    text = "An evaluation of the proposal was undertaken by the committee."
    types = {d.type for d in analyse(text)}
    assert "nominalisation" in types
    assert "passive" in types


def test_clean_active_sentence_is_leaner():
    flabby = diet_score("An evaluation of the situation was undertaken in the context of the review.")
    lean = diet_score("The committee evaluated the situation and revised the plan.")
    assert lean.nominalisations <= flabby.nominalisations
    assert lean.prepositions <= flabby.prepositions


def test_repeated_openings_detects_habit():
    text = "He walked. He opened it. He looked out."
    openings = repeated_openings(text)
    assert openings.get("he", 0) >= 2


def test_hints_lower_xp_cap():
    no_hint = xp_for_attempt(100, quality=1.0, hint_level=0, attempt_number=1)
    two_hints = xp_for_attempt(100, quality=1.0, hint_level=2, attempt_number=1)
    assert two_hints < no_hint


def test_mistakes_never_negative():
    assert xp_for_attempt(100, quality=0.0, hint_level=4, attempt_number=3) >= 0
