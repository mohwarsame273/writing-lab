# Feedback Infrastructure Research

## Section 1: FeedbackHub

1. **Prompt Assembly**
   The prompt is assembled dynamically inside `process_files` using `ChatPromptTemplate` from LangChain. It uses a strict layout:
   ```text
   # System Message
   {system_message}

   # Section 1 - The Past Feedback Example
   {past_feedback_example}

   # Section 2 - The Assessment Brief
   {assessment_brief}

   # Section 3 - The Grading Criteria
   {grading_criteria}

   # Section 4 - The Task Description
   {task_description}

   # Section 5 - The Feedback Format
   {feedback_format}

   # Section 6 - The Student Submission Content
   {content}

   Please assess the submission and provide feedback based on the above information.
   ```
   If a persona is selected, additional constraints are appended to the `system_message`, enforcing a resolution rule: "Conflict Resolution Rule: The module persona governs subject context and standards; the learner persona governs delivery. Where they conflict, the module persona wins on substance and the learner persona wins on style."

2. **The Five Personas**
   The personas are stored in `backend/data/personas.json`. Their exact system fragments are:
   - **Conciseness Coach**: "You are a writing coach working with a student on concision. Your priority is helping them fit their argument inside the word count without losing substance.\n\nFor each point you raise:\n- Quote the student's own sentence or phrase exactly as they wrote it.\n- Show a tightened version.\n- Give the approximate word saving.\n- Name the specific problem in plain terms: redundancy, hedging, throat-clearing, nominalisation, unnecessary qualification, restating the question, or padding a definition the reader already has.\n\nPrioritise the passages where the most words can be recovered for the least loss of meaning. Do not tighten anything that is carrying analytical weight; if cutting a passage would cost the argument, say so and leave it alone.\n\nWhere the student has under-developed a section, say plainly that they should spend recovered words there rather than trimming further.\n\nYou still address the assessment criteria in full. Concision is how you deliver the feedback, not a substitute for it. Do not soften or omit a weakness because you are focused on word count.\n\nClose with a short summary: approximate total words recoverable, and the two or three highest-value cuts."
   - **Question-Led Tutor**: "You are a tutor who teaches through questioning. Rather than stating what is wrong, ask the question that leads the student to notice it themselves.\n\nEach question must be answerable from the student's own submission. Do not ask questions that require knowledge they have not been taught, and do not ask rhetorical questions that are really statements in disguise.\n\nAsk one question per issue. Keep each to a single sentence. After the question, add a brief line indicating where in their work to look.\n\nIf an issue is factually wrong rather than underdeveloped, state it directly rather than questioning it. Do not leave an error standing because the questioning format is awkward.\n\nAddress all the assessment criteria. End with the two or three questions most worth sitting with before the next draft."
   - **Criteria Marker**: "You are an assessor writing formally against the grading criteria.\n\nStructure your feedback criterion by criterion. For each one: state what the submission demonstrates, cite the specific evidence from the work, and identify what would be required to reach the next band.\n\nUse the vocabulary of the grading criteria and the assessment brief. Do not use conversational register, encouragement, or hedging. Be precise rather than warm.\n\nWhere evidence for a criterion is absent, say so plainly and state what would satisfy it."
   - **Step by Step**: "You give direct, actionable feedback as a numbered list of changes.\n\nEach item states exactly what to do, where in the submission to do it, and why it matters, in that order. Use the imperative. Keep each item to two or three sentences.\n\nOrder the list by impact, highest first. Avoid jargon; where a technical term is unavoidable, define it in a clause.\n\nDo not open with praise or close with encouragement. The list is the feedback. Cover all the assessment criteria across the items."
   - **Supportive Peer**: "You are a supportive, experienced peer talking a student through their work. Your register is warm and plain-spoken.\n\nWhere a mistake is a common one, say so, because knowing it is common reduces the anxiety around fixing it. Introduce one issue at a time and finish the thought before moving on.\n\nBe honest. Warmth means the tone is kind, not that the assessment is softened. Every weakness you would raise in a formal register you raise here too, in a gentler order and with more context. Never imply the work is stronger than it is, and never leave a significant weakness unmentioned to keep the tone light.\n\nCover all the assessment criteria. Close by naming the single next step you would take if this were your submission."

3. **moderate_feedback Pass**
   `moderate_feedback` performs a secondary LLM review over the initial feedback to ensure factual accuracy, structural compliance, and lack of hallucination. It explicitly commands: "If the Initial Feedback praises or mentions something that is NOT in the Student Submission (a hallucination), YOU MUST DELETE THAT POINT ENTIRELY." 
   *Worth having?* Yes, absolutely. A moderation pass specifically targeting hallucinations (false critique or false praise) adds significant integrity to the system, ensuring students are not graded on imaginary text.

4. **Return Shape**
   `process_files` returns a tuple: `(summaries, full_prompt)`. `summaries` is a list of `(filename, final_feedback)` tuples where `final_feedback` is a flat string of markdown text. There is no structural breakdown (rubric, strengths, improvements) returned as data objects to the UI.

5. **Criteria and Assessment Briefs**
   They are supplied via configuration files (`data/module_data.json` and `data/generic_data.json`). The text blocks are passed into the prompt. The assessment brief is provided as a file path referencing a file in `data/`, which is then read during processing.

6. **Defects**
   The application attempts to read the past feedback file (which may be a `.docx`) as a raw text string:
   ```python
   with open(past_feedback_path, 'r', encoding='utf-8') as f:
       past_feedback_example = f.read()
   ```
   This will corrupt or fail when `past_feedback_path` is a binary format like `.docx`. 
   Another structural flaw is returning feedback purely as formatted markdown strings, which makes the UI highly coupled to the LLM's output format and prevents programmatic rendering or manipulation of distinct feedback items.

## Section 2: ConCraftr

1. **Generation Prompts & Chunked Generation**
   ConCraftr uses a plan-first architecture. It first calls `_generate_section_plan` asking the LLM to output a JSON array of sections (title, heading level, scope, negative boundaries). Then, `_generate_long_form_handbook` iterates through this plan array, generating each section one-by-one by passing the section's scope and title to the LLM. It appends the output directly to a Word document via a `WriterBot` to handle memory and token limits seamlessly.

2. **Structured Output vs. Parsing**
   It does *not* use native API structured output features (like `with_structured_output` or `response_schema`). Instead, it asks the LLM to "Return ONLY the JSON array" and parses the free text using a regular expression: `re.search(r"\[[\s\S]*\]", response)` followed by `json.loads`. It uses `langchain==0.2.17`.

3. **Research Grounding**
   `semantic_scholar_client.py` uses the Semantic Scholar (S2) Graph API. It applies a 12-hour TTL cache bounding up to 200 entries to `data/semantic_scholar_cache`. It strictly bounds memory usage, rate-limits gracefully (based on the presence of an API key), and is fail-closed, reverting to an `EMPTY_STATE_CONTEXT` (explicit instruction to write without citing work) on network failures.

4. **Skills England KSB Retrieval**
   `skills_england_client.py` features a two-tier lookup: 
   - **Tier 1:** An offline JSON index (`data/standards_index.json`) mapped without network calls.
   - **Tier 2:** A fetch-once disk cache (`data/skills_england_cache`) with a 30-day TTL. On a cache miss, it calls the Occupational Maps API, normalises the response, caches it, and returns. This enables injection of KSBs directly into template prompts securely and resiliently.

5. **Validation of Generated Output**
   Output validation is minimal and prompt-driven rather than programmatic. `agent_assess_quality` prompts the LLM to score content 1-10 on completeness, accuracy, structure, clarity, and actionability, returning a JSON response. It does not validate schema shapes programmatically or check grounding strictly against the source texts prior to completion.

6. **Reusable Prompt Construction**
   ConCraftr contains a robust `build_prompt_from_template` function that resolves dynamic placeholders (`{field}`, `[field]`, `<<field>>`, `${field}`) mapped from user inputs. It treats the `knowledge_base` field as a special case, compiling uploaded file texts and user notes into a context block that is injected into both the prompt body and the system message.

## Section 3: What WritingLab could adopt

### 1. Feedback Moderation Pass (FeedbackHub)
- **What it is:** A secondary LLM call designed to review initial feedback and strictly remove hallucinations (e.g. false praise or critiques for things the student didn't write).
- **Benefit to WritingLab:** Increases the integrity of the feedback, preventing the LLM from making things up or hallucinating rules.
- **Requirements:** 1 additional LLM call per submission; pure logic change inside `services/llm_grader.py`. No new dependencies.
- **Risk:** Low risk. Slightly higher latency for the user.
- **Effort:** Hours.

### 2. Personas (FeedbackHub)
- **What it is:** Pre-defined system fragments (e.g. "Supportive Peer", "Conciseness Coach") that alter the delivery style without compromising grading substance.
- **Benefit to WritingLab:** Enhances the gamified/DataCamp-style experience by letting users (or difficulty modes) dictate the pedagogical style of feedback.
- **Requirements:** Add persona strings to `domain` logic and inject them into the LLM system prompt.
- **Risk:** Low risk.
- **Effort:** Hours.

### 3. Knowledge Base Context Assembly & Caching Architecture (ConCraftr)
- **What it is:** The pattern of separating core prompt instructions from injected reference context, coupled with fail-closed disk caching mechanisms for external data.
- **Benefit to WritingLab:** As WritingLab expands into longer tasks (e.g., Literature Review), grounding tasks in cached, verified principles or papers will be necessary.
- **Requirements:** Implementation of a disk cache; pure logic.
- **Risk:** Medium risk, adds architectural complexity.
- **Effort:** Days.

*Ranked by Value/Risk:*
1. Feedback Moderation Pass (High value, low effort, low risk)
2. Personas (High value UX, low effort, low risk)
3. Caching Architecture (Medium value for current drills, higher effort)

## Section 4: What NOT to adopt

- **Unstructured Feedback Returns:** FeedbackHub returns long strings of markdown rather than structured data. WritingLab must retain its `GradeResult` discrete structures (`rubric`, `strengths`, `improvements`) to correctly render interactive UI components.
- **Brittle JSON Parsing:** ConCraftr's use of `re.search(r"\[[\s\S]*\]", response)` is fragile. WritingLab should rely on native SDK structured outputs (`response_schema` in Google GenAI or Pydantic parsers in OpenAI) to guarantee output shape.
- **Exemplar File Reading Bug:** FeedbackHub attempts to read `.docx` files as `utf-8` text. This will crash or corrupt text. 
- **Destructive Formatting Re-writes:** FeedbackHub's moderator forces rigid layout constraints (like "three bolded subheadings"). WritingLab relies on discrete data elements; forcing a layout string in the LLM response breaks the UI's ability to render custom components.

## Section 5: Compatibility constraints

WritingLab strictly pins modern, lightweight dependencies: `reflex[db]==0.9.7`, `sqlmodel 0.0.42`, `pydantic 2.13.5`, `google-genai 2.22.0`, and `openai 3.7.0`.

- FeedbackHub and ConCraftr rely heavily on `langchain` (versions 0.2.x and deprecated `langchain.chat_models`), along with older versions of `openai` (1.75.0) and `google-genai` (0.1.0). 
- **Constraint:** We **must not** adopt any LangChain imports or code from these repositories. Adopting them would force dependency regressions, breaking Pydantic V2 schemas and Reflex integrations.
- **Solution:** Any features adopted (like the Moderation Pass or Personas) are *pure logic* improvements and can be implemented directly using WritingLab's existing native SDK calls inside `services/llm_grader.py` without touching `requirements.txt`.