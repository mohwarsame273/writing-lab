# Phase 0 Verification

### Source-review findings (Section 4.2)

1. **Casual mode suppresses completion history.**
   - **Reproduced**: Yes.
   - **File/Line**: `writing_lab/state/lab_state.py`, line 422 in `_award()`. It returns early if `self.casual_mode` is True, so `self.completed_ids` is not updated.
2. **Repetition may pick completed items indefinitely.**
   - **Reproduced**: Yes.
   - **File/Line**: `writing_lab/state/lab_state.py`, line 220 in `_pick_next()`. If all items are seen, it loops using `pool[len(self.completed_ids) % len(pool)]`.
3. **Bank progress mixes modes and generated IDs.**
   - **Reproduced**: Yes.
   - **File/Line**: `writing_lab/state/lab_state.py`, line 164 in `progress_pct()`. It counts all `self.completed_ids` (which can include AI-generated IDs) but divides by the length of `_EXERCISES` (which only contains static exercises).
4. **Failed attempts count as completed.**
   - **Reproduced**: Yes.
   - **File/Line**: `writing_lab/state/lab_state.py`, line 400 and 420 in `_apply_grade_result`. It calls `_award()` regardless of `result.passed`, which adds the exercise to `completed_ids`.
5. **Free-writing analysis may award repeated XP for unchanged text.**
   - **Reproduced**: Yes.
   - **File/Line**: `writing_lab/state/lab_state.py`, line 472 in `analyse_free_write()`. It adds 20 XP every time the button is clicked, without checking if the text changed.

### Untested Risks

- **Persistence Crash Risk**: While killing dangling Node processes fixes a port clash, it does not confirm the root cause of the original persistence crash is completely gone. The new append-only design using `AttemptRecord` structurally avoids the old failure mode, but the original crash remains an untested risk.

### Reflex Migrations

- `reflex run` auto-applies pending Alembic migrations, so generating a migration and starting the app is enough to execute it. Note that any future migration touching existing tables must be reviewed and backed up before the app is started.

### Test Suite Safety Guard

- The test suite includes a `clean_db` fixture that deletes `AttemptRecord` rows to ensure test isolation. To prevent accidental data loss against production or staging databases, this fixture reads `config.db_url` and will immediately abort the test run if it points to anything other than a local SQLite database (`sqlite:///...`). Do not remove this guard.
