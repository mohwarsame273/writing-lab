# Knowledge base

This folder is the app's in-memory RAG corpus. No vector database is required
at this scale.

- `principles.json` — writing rules (shape: `domain.models.Principle`). **Drop
  your several dozen writing-aid documents here**, one JSON record per rule.
- `exercises.json` — the exercise bank (shape: `domain.models.Exercise`).
- `rubrics.json` — grading bands per mode.
- `embeddings.npy` — *(optional, add later)* precomputed embedding matrix whose
  row order matches `principles.json`, for the semantic retrieval path in
  `retrieval/search.py`.

## Adding your own documents

1. Convert each writing principle into a `principles.json` record. Keep
   `track` as `academic`, `literary`, or `both`, and tag `skills` so retrieval
   and mastery can find it.
2. Author exercises that reference those rules via `rule_ids`.
3. (Later) regenerate `embeddings.npy` offline and switch `retrieve()` to the
   hybrid path.
