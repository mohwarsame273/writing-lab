# Writing Lab

A gamified, DataCamp-style writing-practice app. Two tracks (academic and
literary craft), short graded drills, and a free-writing diagnostic mirror, with
XP, streaks and skill mastery. Built with [Reflex](https://reflex.dev)
(pure-Python full-stack) on a framework-independent core.

It runs **fully offline out of the box**: with no API key set, grading uses the
deterministic Writer's Diet analyser plus retrieved writing principles. Add an
LLM key later for the contextual third layer.

## Quick start (Windows)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
reflex run
```

Then open http://localhost:3000. No `reflex init` is needed: `rxconfig.py` is
already present.

macOS / Linux: swap the activate line for `source .venv/bin/activate`.

## Run the tests

```
python -m pytest -q
```

These cover the deterministic core and need neither Reflex nor a browser.

## What is where

- `domain/`, `retrieval/`, `services/` — the framework-independent brain
  (diagnostics, grading, mastery, retrieval). No Reflex imports here.
- `writing_lab/` — the Reflex UI shell (state, components, pages, theme).
- `knowledge/` — editable JSON: writing principles, the exercise bank, rubrics.
  **Drop your own writing-aid documents into `knowledge/principles.json`.**

See `ARCHITECTURE.md` for the full map and the rules that keep the layers clean.

## Finishing the build

This is a verified skeleton with a handful of clearly-marked TODOs (LLM wiring,
debounced feedback, CodeMirror inline underlining, semantic retrieval, durable
persistence, more content). `CURSOR_PROMPT.md` is a ready-to-paste brief for an
AI coding agent to complete them safely. Start there.

## Configuration

Grading looks for one of `ANTHROPIC_API_KEY`, `AZURE_OPENAI_API_KEY` or
`OPENAI_API_KEY`. With none set, the app uses the offline grade. Put keys in a
`.env` file (gitignored); never commit secrets.
