# Paste this into Cursor as your first message

You are completing an existing, working Reflex (Python) application called
**Writing Lab**. A senior engineer has already built and verified the skeleton:
the domain layer runs, the tests pass, and all three pages compile. Your job is
to **finish the marked TODOs without breaking what exists**. Read this whole
brief before touching any file.

---

## 0. Before you write any code: install the Reflex skills

This project targets **Reflex 0.9.7**, which is pre-1.0 and changes between
minor releases. Do not rely on your training memory for Reflex APIs. Install the
official Reflex agent skills and use them:

```
npx skills add reflex-dev/agent-skills
```

Confirm these three skills are available before proceeding: `reflex-docs`,
`setup-python-env`, `reflex-process-management`. For any Reflex API question
(components, state, events, styling, routing, database), consult **reflex-docs**
rather than guessing. If an API you remember does not match the docs, the docs win.

Then set up the environment per **setup-python-env** on Windows:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Keep `reflex==0.9.7` pinned. Do not upgrade or downgrade Reflex.

---

## 1. Hard rules (read twice)

These are non-negotiable. Violating them is the main way this task goes wrong.

1. **Additive only. Never delete or rewrite working code.** If something already
   works, leave it. Add alongside it. Do not "tidy", "refactor for consistency",
   or "simplify" files that are not part of a TODO you were asked to do.
2. **Never touch `domain/`, `retrieval/` or `services/` logic** except where a
   `TODO (completing agent)` comment explicitly invites it. These modules are the
   verified core. In particular, **do not add a Reflex import anywhere under
   `domain/`, `retrieval/` or `services/`**. That separation is the whole point.
3. **Preserve public signatures.** Keep function and event names, parameters and
   return types exactly as they are (for example `editor()`,
   `LabState.update_answer(value)`, `retrieve(...)`, `grade(...)`). Other code
   depends on them.
4. **Keep the state as one class.** `writing_lab/state/lab_state.py` is one
   `rx.State` subclass on purpose. Do not split it into substates.
5. **No Python truthiness on Vars.** Never use `if`, `and`, `or`, `not` or
   `bool()` on a Reflex Var. Use `rx.cond(...)` and bitwise `& | ~`. When reading
   from `list[dict]` / `dict` state vars in components, cast before arithmetic:
   `item["score"].to(int)`, `LabState.fw_diet[key].to(float)`.
6. **Verify before you claim done.** After each task run `reflex run` and load the
   affected page. Fix compile errors before moving on. Run `python -m pytest -q`.
7. **Do not commit.** Leave changes unstaged. The owner reviews and commits
   himself. Do not run `git commit` or `git push`.
8. Use **British English** in all copy and comments. Do not use em-dashes.

If a change would require breaking one of these rules, stop and explain the
trade-off instead of doing it.

---

## 2. Orient yourself first

Read, in this order, before editing: `ARCHITECTURE.md`, then
`writing_lab/state/lab_state.py`, then `domain/grading.py` and
`domain/diagnostics.py`. Confirm the app runs (`reflex run`, open `/`,
`/practice`, `/free-write`) so you have a working baseline to protect.

---

## 3. Tasks, in priority order

Do these one at a time. After each, run the app and the tests, then pause.

### Task A. Wire the LLM grading layer (`services/llm_grader.py`)
The third grading layer is stubbed and currently returns `None`, so the app runs
fully offline on the deterministic grade. Implement the real call inside
`grade()` where the `TODO (completing agent)` block is.
- Use the provider the owner already has. Two supported paths are documented in
  the file; pick one and delete the other's comment block only.
- For Azure OpenAI reasoning models, remember: send `max_completion_tokens` and
  `temperature=1`; do not send `max_tokens` or other temperatures.
- Keep the strict JSON-only contract and the existing `_parse()` guard. If the
  call fails or returns malformed JSON, return `None` so the deterministic grade
  still stands. **Do not** change the shape of the returned dict; `domain.grading`
  already consumes it.
- Read the API key from an environment variable. Never hard-code secrets. Add a
  `.env.example` documenting the variable names. `.env` is already gitignored.

### Task B. Debounce live feedback (`writing_lab/components/editor.py` + state)
`LabState.update_answer` runs the analyser on every keystroke. Add a ~600ms
debounce so the live findings update after the learner pauses, not on every
letter. Prefer a Reflex-native approach (check **reflex-docs** for debounced
events / `rx.debounce_input` or an equivalent). Keep the `editor()` signature and
the `on_change -> LabState.update_answer` wiring intact.

### Task C. Inline underlining with CodeMirror 6 (`writing_lab/components/editor.py`)
Replace the plain `rx.text_area` with a wrapped CodeMirror 6 editor
(`rx.NoSSRComponent`) that underlines the diagnostic spans in place. The analyser
already returns character offsets: `domain.diagnostics.analyse()` gives each
finding a `start`, `end` and `severity`. Feed those ranges to CodeMirror
decorations. Keep the live findings list as a fallback. Do not remove the
existing text-area code until the CodeMirror version compiles and renders.

### Task D. Semantic retrieval (`retrieval/search.py`)
Implement `semantic_search` (currently falls back to keyword). Plan is in the
docstring: load `knowledge/embeddings.npy` (row order matches
`load_principles()`), embed the query with the same model used offline, cosine,
take top-k. Then make `retrieve()` blend keyword and semantic scores (hybrid).
Keep the keyword path working as the zero-dependency fallback.

### Task E. Durable, multi-user progress (`services/progress_service.py` + state)
Right now XP, streak and mastery are session-scoped in `LabState`. Define
`rx.Model` tables (User, AttemptLog, MasteryRow) and a repository in
`progress_service.py` with the **same method names** as the current `Progress`
dataclass, then have `LabState` read and write through it. Run
`reflex db init` / `reflex db makemigrations` / `reflex db migrate` per
**reflex-docs**. SQLite is fine for now.

### Task F. Grow the content (`knowledge/*.json`)
The banks are seeded, not complete. Add more `principles.json` records (this is
where the owner's writing-aid documents go) and more `exercises.json` items
across all exercise kinds and both modes. Follow the existing JSON shapes exactly
and reference principles by `rule_ids`. This is pure data; it needs no code
changes.

---

## 4. Definition of done for each task

- `reflex run` compiles and the affected page renders with no console errors.
- `python -m pytest -q` still passes (add tests where sensible).
- No working code was deleted or rewritten outside the task's scope.
- No Reflex import leaked into `domain/`, `retrieval/` or `services/`.
- Changes are unstaged and summarised for the owner to review.

## 5. If you get stuck

Prefer the smallest change that satisfies the task. If a task seems to need a
rule broken, or a Reflex API you are unsure of, stop and ask, citing the
relevant **reflex-docs** section. Do not guess and overwrite working files.
