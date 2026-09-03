"""Framework-independent domain models.

Nothing in this package may import Reflex. These types are the contract
between the intelligence of the product (diagnostics, grading, mastery) and
whatever UI shell renders it. If the UI framework is ever swapped, this layer
does not change.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Optional


class Mode(str, Enum):
    """Academic and literary are not a colour swap: they switch the exercise
    bank, the interpretation of diagnostics, and the grading rubric."""

    ACADEMIC = "academic"
    LITERARY = "literary"


Severity = Literal["low", "medium", "high"]

ExerciseKind = Literal[
    "sentence_completion",
    "rewrite",
    "diagnostic_selection",
    "constrained_composition",
    "paragraph_revision",
    "free_write",
    "transitions",  # spaced practice of transition words until memorised
]


@dataclass(frozen=True)
class Principle:
    """A single writing rule drawn from the JSON knowledge base."""

    rule_id: str
    title: str
    track: Mode | Literal["both"]
    skills: list[str]
    principle: str
    weak_examples: list[str] = field(default_factory=list)
    strong_examples: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    source: dict = field(default_factory=dict)


@dataclass
class Diagnostic:
    """One finding produced by the deterministic analyser. `start`/`end` are
    character offsets so the editor can underline the span."""

    type: str
    start: int
    end: int
    text: str
    severity: Severity
    message: str
    rule_id: Optional[str] = None


@dataclass
class DietScore:
    """Writer's Diet style profile. Ratios are share-of-words in [0, 1]."""

    verbs: float
    nominalisations: float
    prepositions: float
    ad_words: float          # adjectives + adverbs
    waste_words: float       # it / this / that / there
    word_count: int
    sentence_count: int
    mean_sentence_len: float
    verdict: str             # "lean" | "fit-and-trim" | "needs-toning" | "flabby" | "heart-attack"

    def as_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class Exercise:
    exercise_id: str
    kind: ExerciseKind
    mode: Mode | Literal["both"]
    skill: str
    prompt: str
    seed_text: str = ""                     # text shown in the editor to start
    target: str = ""                        # the objective, not one exact answer
    options: list[str] = field(default_factory=list)   # for selection kinds
    answer_index: Optional[int] = None      # for selection kinds
    hints: list[str] = field(default_factory=list)     # progressive: concept -> location -> transformation -> model
    rule_ids: list[str] = field(default_factory=list)
    max_xp: int = 100
    difficulty: int = 1                     # 1..5


@dataclass
class RubricScore:
    label: str
    score: int
    out_of: int


@dataclass
class GradeResult:
    """The unified result of grading a submission. Assembled from three layers:
    deterministic diagnostics, retrieved principles, and (optionally) an LLM
    judgement. The app can always produce this even with no LLM available."""

    total: int
    out_of: int
    rubric: list[RubricScore] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    improvements: list[dict] = field(default_factory=list)   # {issue, suggestion}
    diagnostics: list[Diagnostic] = field(default_factory=list)
    diet: Optional[DietScore] = None
    xp_awarded: int = 0
    used_llm: bool = False
    passed: bool = False
    model_revision: str = ""
    coaching_note: str = ""


@dataclass
class MasterySnapshot:
    """Skill mastery is tracked separately from XP. XP measures momentum;
    mastery measures learning."""

    skill: str
    mastery: float   # 0..1
    attempts: int
    last_seen_iso: Optional[str] = None
    due_iso: Optional[str] = None   # next spaced-repetition slot
