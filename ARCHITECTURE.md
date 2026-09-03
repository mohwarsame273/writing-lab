# Writing Lab: architecture

A gamified, DataCamp-style writing-practice app. Two tracks (academic and
literary), short graded drills, a free-writing diagnostic mirror, XP, streaks
and skill mastery.

## The one rule that governs everything

**The product's intelligence is framework-independent. The UI is disposable.**

```
  domain/  retrieval/  services/          writing_lab/
  -----------------------------           ------------------
  pure Python, no Reflex import   <----   Reflex UI shell only
  (diagnostics, grading, mastery)         (state, components, pages, theme)
```

If Reflex ever disappoints, only `writing_lab/` is rewritten. Never let domain
logic leak upward into the Reflex state class, and never let a Reflex import
leak down into `domain/`, `retrieval/` or `services/`.

## File tree

```
writing-lab/
├── rxconfig.py                  # Reflex config (app_name="writing_lab", Tailwind V4)
├── requirements.txt             # reflex==0.9.7 (pinned on purpose)
├── README.md                    # setup + run
├── ARCHITECTURE.md              # this file
├── CURSOR_PROMPT.md             # paste into Cursor to brief the completing agent
│
├── knowledge/                   # in-memory RAG corpus (author-editable JSON)
│   ├── principles.json          #   writing rules (drop your documents here)
│   ├── exercises.json           #   the exercise bank
│   ├── rubrics.json             #   grading bands per mode
│   └── README.md
│
├── domain/                      # FRAMEWORK-INDEPENDENT CORE  (no reflex import)
│   ├── models.py                #   dataclasses: Mode, Exercise, Diagnostic, GradeResult, ...
│   ├── diagnostics.py           #   WORKING Writer's Diet analyser (stdlib only)
│   ├── grading.py               #   three-layer grader (deterministic + retrieval + optional LLM)
│   ├── scoring.py               #   XP + hint economics
│   ├── mastery.py               #   mastery EMA + spaced repetition
│   └── exercises.py             #   load + sequence exercises
│
├── retrieval/                   # in-memory hybrid retrieval  (no reflex import)
│   ├── loader.py                #   load principles.json
│   └── search.py                #   WORKING keyword search; semantic_search is a stub
│
├── services/                    # side-effectful adapters  (no reflex import)
│   ├── llm_grader.py            #   optional LLM layer; returns None when unconfigured
│   └── progress_service.py     #   durable progress (JSON now; rx.Model later)
│
├── writing_lab/                 # REFLEX UI SHELL (disposable)
│   ├── writing_lab.py           #   app entry: theme, pages, on_load
│   ├── theme.py                 #   all colours, fonts, style tokens
│   ├── layout.py                #   page shell (top bar + container)
│   ├── state/
│   │   └── lab_state.py         #   ONE state class; thin bridge to domain/
│   ├── components/
│   │   ├── common.py            #   pill, stat_card, section_heading, severity_dot
│   │   ├── top_bar.py           #   header: mode toggle, streak, XP, avatar
│   │   ├── mode_toggle.py       #   academic <-> literary
│   │   ├── editor.py            #   text area + live diagnostics (CodeMirror = TODO)
│   │   ├── hint_panel.py        #   progressive hints
│   │   ├── diagnostics.py       #   findings list (shared)
│   │   ├── feedback_panel.py    #   score, rubric, strengths, diet profile
│   │   └── mastery.py           #   mastery bars
│   └── pages/
│       ├── dashboard.py         #   "/"          hero, stats, mastery
│       ├── practice.py          #   "/practice"  two-pane exercise screen
│       └── free_write.py        #   "/free-write" free session + profile
│
└── tests/
    └── test_diagnostics.py      #   pure-Python tests for the core
```

## Data flow of one graded attempt

```
learner types  ->  LabState.update_answer  ->  domain.diagnostics.analyse   (live preview)
submit         ->  LabState.submit         ->  retrieval.retrieve           (relevant principles)
                                           ->  services.llm_grader.grade    (optional; None offline)
                                           ->  domain.grading.grade         (assembles GradeResult)
                                           ->  domain.scoring / mastery      (XP + mastery update)
                   feedback_panel renders the GradeResult
```

## Design language

Tokens live only in `writing_lab/theme.py`. Purple (#6E368A) primary with an
energetic accent set (amber XP, orange streak, teal success). The component
vocabulary is drawn from the supplied UI design library: Badge, Card, Progress,
Accordion, Alert/Callout, Avatar, Tabs, Tooltip. Keep new UI consistent with
these tokens; do not introduce ad-hoc colours.

## State: why it is one class

`writing_lab/state/lab_state.py` is deliberately a single `rx.State` subclass.
Reflex cross-state access (`get_state`) is a frequent source of subtle bugs. Do
NOT split it up unless you have a concrete need, and if you do, keep the public
event names identical.

## Verified environment facts (Reflex 0.9.7)

- Config: `rx.Config(app_name=..., plugins=[SitemapPlugin(), TailwindV4Plugin()])`.
- App: `rx.App(theme=rx.theme(...), style=..., stylesheets=[...])`; pages via `app.add_page(fn, route=, title=, on_load=)`.
- In component code, values from `list[dict]` / `dict` state vars are typeless
  Vars: **cast before arithmetic**, e.g. `item["score"].to(int)`,
  `LabState.fw_diet[key].to(float)`. This is already done throughout; keep doing it.
- Never use Python `if`, `and`, `or`, `not`, `bool()` on a Var. Use `rx.cond`
  and `&  |  ~`.
