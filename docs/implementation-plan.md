# Writing Lab Implementation Plan

## Branch
`phase-0-audit`

## Phase 0: Inspect Before Changing

### Baseline Commands Run
- `git status` -> `On branch main`, untracked files present. Created and switched to new branch `phase-0-audit`.
- `pytest tests\` -> 5 passed in 0.25s. The deterministic tests in `tests\test_diagnostics.py` run and pass.

### Answers to 4.1
1. **Is there any persistence at all today?**
   The `services/progress_service.py` file includes `User`, `AttemptLog`, and `MasteryRow` as `rx.Model` (SQLModel) classes. However, in `writing_lab/state/lab_state.py`, progress (XP, streak, completed_ids, mastery) is explicitly marked as "SESSION-SCOPED plain state" and the `_award` method says it "Never touches a database, so it can never crash the app". The persistence code exists but is bypassed by the UI state. There are no existing reliable learner records to migrate.
2. **Is there migration tooling?**
   Yes, `alembic` is present (`alembic.ini`, `alembic/` folder, and pinned to 1.19.1 in `requirements.txt`).
3. **What is the exact pinned Reflex version, and what does it constrain?**
   Reflex is pinned to `reflex[db]==0.9.7`. It constrains `sqlmodel<0.1,>=0.0.24`, `alembic<2.0,>=1.15.2`.
4. **Is there a test suite? Does it currently pass?**
   Yes, `tests/test_diagnostics.py` tests the pure Python core. It passes (5 passed in 0.25s).
5. **Where does AI configuration live, and are credentials currently server-side?**
   AI configuration lives in `services/llm_grader.py` which reads `GOOGLE_API_KEY`, `ANTHROPIC_API_KEY`, `AZURE_OPENAI_API_KEY`, or `OPENAI_API_KEY` from environment variables (expected in `.env`). The credentials are server-side only.

### Discrepancies with Specification
- The specification assumes state is entirely session-scoped. In reality, `progress_service.py` does attempt to use `rx.session()` to write to the DB, but `lab_state.py` does not use it.
- There are no tests for anything other than `test_diagnostics.py`. The "five integrity behaviours" mentioned in Phase 1 do not have existing tests.

### Proposed Plan for Phase 1
1. Add explicit ID, timestamp, and ownership fields to the existing models and create the missing models (ActivityDefinition, Attempt, Artefact, DocumentSnapshot, Feedback, InterviewSession, InterviewTurn, IdeaNode, OutlineNode, Suggestion, Decision, EvidenceEvent, RewardLedger, CapabilityEvidence).
2. Establish a clear schema for retention and data protection.
3. Write failing tests for the five integrity behaviours.
4. Refactor `lab_state.py` to actually use the new database models, removing the session-scoped arrays and dictionaries.
5. Create an Alembic migration for the new schema.
