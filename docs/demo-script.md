# Writing Lab Demo Script

## Setup
Ensure the app is running (`reflex run`).
Open http://localhost:3000 in your browser.

## The Journey
1. **Dashboard Overview:** Start at the dashboard. Explain that the app tracks XP (momentum) and Skill Evidence (learning). Point out the new honest evidence states ("Not yet sampled", "Practised with support", etc.) instead of fabricated percentages.
2. **Open an Activity:** Click "Start practising". Show the left rail where you can pick a topic. The layout will gracefully handle long text without horizontal scrollbars.
3. **Write and Request Feedback:** Turn off Casual mode using the toggle in the top bar so that XP will be awarded and tracked. Paste a long unbroken string to prove the layout doesn't break. Then write a real answer to the prompt.
4. **Use Contextual Suggestions:** Show the new "Writing Moves" panel. Explain that it prompts the learner to think about what the paragraph needs next (e.g. "Establish the background the reader needs to understand this.") rather than writing the content for them.
5. **Revise:** Submit for grading. Review the feedback, click "Try again", and improve the answer. Both the original text and the feedback will remain visible.
6. **See Evidence State Update:** Once graded, return to the dashboard. Show that the evidence state for the skill has updated from "Not yet sampled" to "Practised with support" or "Demonstrated in independent practice" based on the attempt.
7. **Refresh the Page:** Refresh the browser. Explain that thanks to the new minimal persistence layer (SQLite/Postgres), the evidence states and completed exercises survive the refresh.

## What is Not Yet Built (Honest Gaps)
- **Interview My Thinking:** The multi-step Q&A thinking assistant is not yet implemented.
- **Activity Contract Engine & New Authored Content:** The current content is hardcoded/static. We are not yet loading from a fully authored contract engine.
- **Full Production Persistence & Authentication:** Minimal persistence is in place to survive a refresh, but it uses a hardcoded demo user. Real authentication and multi-user persistence are missing.
- **Next.js Frontend:** The frontend is still in Reflex. The Stage 4 comparison slice and decision is pending.
- **LLM-Generated Suggestions:** The move-card templates are currently a static list, not dynamically generated via an LLM.

## Required Environment Variables for Deployment
- `DB_URL` (e.g. `postgresql://user:pass@host/db` or `sqlite:///reflex.db` fallback)
- One of the following LLM provider keys:
  - `GOOGLE_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`
  - `AZURE_OPENAI_API_KEY` (along with `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_OPENAI_DEPLOYMENT_NAME`)