# Writing Lab - Application Documentation

## 1. Overview & Vision
The **Writing Lab** is a web-based, gamified writing practice application built with Python and the [Reflex](https://reflex.dev/) framework. It aims to help writers drill and memorize specific writing skills (e.g., transitions, nominalizations, concrete descriptions) through a DataCamp-style two-pane layout. It provides users with live feedback, diagnostic analyses (like the "Writer's Diet" profile), and AI-generated grading and exercises.

## 2. Architecture & Design Principles

The application is structured to decouple the UI from the underlying business logic. 
* **State Management (`writing_lab/state/lab_state.py`)**: Uses a single, centralized state (`LabState`). This acts as a thin bridge to the domain layer. Progress and state variables are currently session-scoped to avoid database-related crashes, keeping the app lightweight and fast.
* **Domain Layer (`domain/`)**: Pure Python dataclasses and functions. This layer holds the core intelligence—grading logic, mastery tracking, diagnostics, and domain models. It is completely independent of the Reflex UI framework.
* **Services Layer (`services/`)**: Orchestrates external integrations, primarily calling LLMs (like Google's Gemini API) for grading and generating fresh exercises (`services/llm_grader.py`, `services/exercise_gen.py`). These fall back gracefully offline if the AI is unreachable.
* **UI/Components Layer (`writing_lab/`)**: Contains the Reflex pages and visual components. 

## 3. Gamification Patterns

The app introduces several gamification loops to keep users engaged and encourage retention, managed via `LabState` and `domain/mastery.py`.

* **Experience Points (XP) & Momentum**: Users earn XP based on the quality of their submission, attempt number, and how many hints they revealed. This provides immediate, tangible rewards.
* **Streaks**: Encourages consecutive practice to build momentum.
* **Mastery System (`MasterySnapshot`)**: Tracks learning separately from XP. It tracks attempts and mastery percentage (0.0 to 1.0) on a per-skill basis (e.g., "nominalisation", "rhythm"). This sets the stage for a spaced-repetition system.
* **Casual Mode toggle**: Allows the user to turn off the gamification layer (XP, mastery, progress tracking). By default, casual mode is ON, giving beginners a friendly start without overwhelming them with metrics.
* **Diet Diagnostics & Verdicts**: Offers a gamified "Writer's Diet" profile score (e.g., "lean", "fit-and-trim", "flabby"), transforming passive feedback into a score they can try to optimize live in the editor.

## 4. Directory & File Structure

Here is a breakdown of the key files and their responsibilities:

### **Domain Layer (`/domain`)**
- `models.py`: Defines the pure Python dataclasses (`Exercise`, `Principle`, `Diagnostic`, `DietScore`, `GradeResult`, `MasterySnapshot`).
- `exercises.py`: Logic for loading and cycling through static exercise banks.
- `grading.py`: The deterministic grading pipeline that combines text analysis, retrieved rules, and LLM verdicts into a final `GradeResult`.
- `mastery.py`: Calculates mastery progression.
- `scoring.py`: Logic for computing XP based on quality, hints used, and attempts.
- `diagnostics.py`: Deterministic text analysis (counting verbs, prepositions, "waste words") to generate the Writer's Diet profile.

### **Services Layer (`/services`)**
- `llm_grader.py`: Handles calling the Gemini API to judge a user's writing based on principles.
- `exercise_gen.py`: Generates custom, dynamic exercises via the Gemini API when the user exhausts static banks or requests a fresh drill.
- `progress_service.py`: Contains auxiliary progress-tracking utilities.

### **State Layer (`/writing_lab/state`)**
- `lab_state.py`: The "single source of truth". Handles all UI state, events (toggling modes, generating drills, grading), and connects the UI events to the `domain/` and `services/` layers.

### **UI Components & Pages (`/writing_lab`)**
- `writing_lab.py`: The app entry point, where pages are registered.
- `layout.py`: Shared page shell, ensuring uniform max-widths, top bars, and theming.
- `pages/practice.py`: The core practice view. Renders the DataCamp-style left rail (topic picker, progress) and right pane (prompt, editor, feedback).
- `pages/free_write.py`: A separate mode for open-ended writing with live analysis.
- `pages/dashboard.py`: Renders user progress, mastery metrics, and statistics.
- `components/editor.py`: The main writing surface, wiring a CodeMirror editor to `LabState` for live text analysis and diagnostic underlines.
- `components/feedback_panel.py`: Displays grading rubrics, strengths, and AI coaching notes after submission.
- `components/hint_panel.py`: Progressive hint exposure UI.
- `components/top_bar.py`: Navigation and global controls (e.g., Casual mode toggle).

---

## 5. UI Layout Bug: "Generated Practice Routine Width Expansion"

### **The Issue**
When a user clicks "Generate a fresh drill" and the AI creates a new practice routine, the new text causes the page width to horizontally stretch and elongate. This ruins the bounded, proportionate visual look of the app. The text expands infinitely sideways rather than breaking to a new line, widening the overall page container.

### **Potential Causes**
This is a classic issue with **CSS Grid and Flexbox layouts** interacting with long, unbroken strings or unconstrained containers.

1. **Grid Container `min-width: auto` Default**: 
   In `pages/practice.py`, the layout is defined using a CSS Grid: `rx.grid(..., columns=rx.breakpoints(initial="1", md="340px 1fr"))`. 
   By default, a CSS grid track (like `1fr`) has a minimum width of `auto`. This means it will never shrink smaller than the minimum intrinsic width of its content. If the generated text doesn't explicitly wrap, the text dictates the width of the `1fr` column, blowing out the grid and the `1160px` max-width container.
2. **Missing Text Wrap Rules**: 
   The generated `ex_prompt` or `ex_seed` text might contain long URLs, code-like structures, or simply lack spaces (or the browser misinterprets it). Without rules like `word-break: break-word;` or `white-space: pre-wrap;`, the text forces the `rx.text()` container to expand horizontally.
3. **Flex/Box Children Unconstrained**:
   Inside `_right_pane()`, components like `_prompt_card()` are set to `width="100%"`. If their parent (`_right_pane` which sits in the `1fr` grid slot) isn't forced to shrink by the grid, `100%` becomes as wide as the longest line of generated text.

### **Potential Fixes**

To keep the generated text strictly bounded within the designed page width, you can implement the following CSS-level fixes via Reflex props (Reminder: do not change code yet, these are recommendations):

1. **Constrain the Grid Track (The most robust fix):**
   Apply `min_width="0"` to the `_right_pane` component or the components inside the `1fr` track. Setting `min_width="0"` overrides the default `min-width: auto` behavior of CSS grid items, allowing the `1fr` column to shrink below the content's intrinsic size, forcing the text inside to wrap.
2. **Force Text to Wrap:**
   On the text elements displaying AI-generated content (e.g., inside `_prompt_card` in `pages/practice.py`):
   * Add `overflow_wrap="break-word"` or `word_break="break-word"` to the `rx.text()` components.
   * Add `white_space="normal"` or `white_space="pre-wrap"` if pre-formatted text is causing issues.
3. **Clip Overflow on the Card:**
   Add `overflow="hidden"` to the `_prompt_card` Box. While this might hide some text if it still doesn't wrap, combining it with text-wrapping props guarantees the card never exceeds the grid boundary. 

Applying `min_width="0"` to the container in the `1fr` column and `overflow_wrap="break-word"` to the generated text blocks should immediately lock the page width.
