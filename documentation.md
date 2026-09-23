# Writing Lab - Application Documentation

## 1. Overview & Vision
The **Writing Lab** is a web-based, gamified writing practice application built with Python and the [Reflex](https://reflex.dev/) framework. It aims to help writers drill and memorize specific writing skills (e.g., transitions, nominalizations, concrete descriptions) through a DataCamp-style two-pane layout. It provides users with live feedback, diagnostic analyses (like the "Writer's Diet" profile), and AI-generated grading and exercises.

## 2. Architecture & Design Principles

The application is structured to decouple the UI from the underlying business logic. 
* **State Management (`writing_lab/state/lab_state.py`)**: Uses a single, centralized state (`LabState`). This acts as a thin bridge to the domain layer.
* **Domain Layer (`domain/`)**: Pure Python dataclasses and functions. This layer holds the core intelligence—grading logic, mastery tracking, diagnostics, and domain models. **Crucially, functions here are pure** (no database access, no Reflex UI imports) to ensure testability without a browser.
* **Services Layer (`services/`)**: Orchestrates external integrations, primarily calling LLMs (like Google's Gemini API) for grading, generating exercises, and managing persistence (`services/progress_service.py` with `AttemptRecord`).
* **UI/Components Layer (`writing_lab/`)**: Contains the Reflex pages and visual components. 

## 3. Gamification Patterns

The app introduces several gamification loops to keep users engaged and encourage retention.

* **Experience Points (XP) & Momentum**: Users earn XP based on the quality of their submission, attempt number, and how many hints they revealed. 
* **Streaks**: Encourages consecutive practice to build momentum.
* **Evidence States (Mastery)**: Replaces fabricated percentages with honest, descriptive states mapping to skill progression (e.g., "Not yet sampled", "Practised with support", "Demonstrated in independent practice").
* **Casual Mode**: Allows the user to turn off the gamification layer display. XP and progression are still tracked in the background, but the UI is simplified for a friendly start.
* **Diet Diagnostics & Verdicts**: Offers a gamified "Writer's Diet" profile score (e.g., "lean", "fit-and-trim", "flabby").

## 4. Directory & File Structure

Here is a breakdown of the key files and their responsibilities:

### **Domain Layer (`/domain`)**
- `models.py`: Defines the pure Python dataclasses (`Exercise`, `Principle`, `Diagnostic`, `DietScore`, `GradeResult`, `MasterySnapshot`).
- `exercises.py`: Logic for loading and cycling through static exercise banks. Returns `None` when banks are exhausted to trigger "All Completed" UI.
- `grading.py`: The deterministic grading pipeline.
- `mastery.py`: Calculates mastery progression and derives human-readable Evidence States.
- `scoring.py`: Pure functions computing XP based on quality, hints used, and attempts (`evaluate_award`, `evaluate_free_write`).
- `diagnostics.py`: Deterministic text analysis (counting verbs, prepositions, "waste words").

### **Services Layer (`/services`)**
- `llm_grader.py`: Handles calling the LLM API to judge a user's writing based on principles.
- `progress_service.py`: Minimal, append-only SQLite/Postgres persistence using `AttemptRecord`. Tracks every pass/fail attempt without mutating past records.
- `exercise_gen.py`: Generates custom, dynamic exercises via the LLM.

### **State Layer (`/writing_lab/state`)**
- `lab_state.py`: The "single source of truth". Handles all UI state, events, and handles `on_load` rehydration from `progress_service.py`.

### **UI Components & Pages (`/writing_lab`)**
- `writing_lab.py`: The app entry point.
- `layout.py`: Shared page shell.
- `pages/practice.py`: The core practice view. Handles the DataCamp-style left rail and right pane. Includes a responsive `min-width: 0` CSS Grid setup to prevent layout blowouts.
- `pages/dashboard.py`: Renders user progress and mastery metrics.
- `components/editor.py`: The main writing surface using CodeMirror.
- `components/feedback_panel.py`: Displays grading rubrics, strengths, and AI coaching notes.
- `components/suggestions.py`: Displays static Rhetorical Move cards for contextual writing suggestions.
- `components/mastery.py`: Renders the evidence states.

## 5. Recent Upgrades & Audits

- **Phase 0 Audit**: Architectural rules established in `/docs/`.
- **Integrity Fixes**: Complex UI state decoupled into pure functions; persistence crash vulnerability resolved with an append-only `AttemptRecord` table.
- **Responsive Layout**: Horizontal expansion bugs fixed via CSS Grid track constraints (`min_width="0"` and `overflow_wrap="anywhere"`).
- **Rhetorical Moves**: Replaced empty suggestions with contextual "move cards" pointing out what a paragraph needs next.
