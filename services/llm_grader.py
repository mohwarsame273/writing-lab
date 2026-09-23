"""Contextual LLM grading — the optional third layer.

This wrapper is deliberately thin and side-effect-isolated. If no API key is
configured it returns None, and domain.grading falls back to the deterministic
grade. That means the app runs end to end offline, which keeps the skeleton
demoable and keeps your dev loop cheap.

Contract: grade() returns constrained JSON (a dict), never free prose:

    {
      "rubric": {"Task fulfilment": 18, "Clarity": 17, ...},  # keys match domain.grading._rubric_for
      "strengths": ["Restored a strong finite verb"],
      "improvements": [{"issue": "...", "suggestion": "..."}]
    }

NOTE FOR THE COMPLETING AGENT: wire this to the same provider Mo already uses.
Two supported paths, pick one and delete the other:
  - Anthropic API (anthropic package), model per product-self-knowledge.
  - Azure OpenAI (BPP tenancy): reasoning model needs `max_completion_tokens`
    and `temperature=1` (do NOT send `max_tokens`/other temperatures).
Keep the JSON-only system prompt strict: no preamble, no markdown fences.
"""
from __future__ import annotations

import json
import os
from typing import Optional

from domain.models import Exercise, Mode

_SYSTEM = (
    "You are a precise writing assessor. Judge only what deterministic tools "
    "cannot: whether meaning is preserved, whether the revision has more force "
    "and clarity, and whether any nominalisation or fragment is a deliberate, "
    "useful choice rather than a lapse. Respond with a single JSON object only, "
    "no preamble and no markdown. Keys: rubric (object of band->int), strengths "
    "(array of strings), improvements (array of {issue, suggestion}), "
    "model_revision (string, a one or two sentence exemplar rewrite of the learner's submission), "
    "coaching_note (string, one sentence naming the single most useful next move)."
)


def _build_prompt(submission: str, exercise: Exercise, mode: Mode, principles: list) -> str:
    principle_block = "\n".join(f"- {p.title}: {p.principle}" for p in (principles or []))
    return (
        f"MODE: {mode.value}\n"
        f"EXERCISE: {exercise.prompt}\n"
        f"TARGET: {exercise.target}\n"
        f"RELEVANT PRINCIPLES:\n{principle_block}\n\n"
        f"LEARNER SUBMISSION:\n{submission}\n\n"
        "Return the JSON object now."
    )


def is_configured() -> bool:
    return bool(
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("ANTHROPIC_API_KEY")
        or os.getenv("AZURE_OPENAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )


def grade(
    submission: str,
    exercise: Exercise,
    mode: Mode,
    principles: list | None = None,
) -> tuple[Optional[dict], Optional[str]]:
    """Return constrained JSON, or None if no provider is configured or the call
    fails (the caller then uses the deterministic grade)."""
    if not is_configured():
        return None, None

    prompt = _build_prompt(submission, exercise, mode, principles or [])

    if os.getenv("GOOGLE_API_KEY"):
        from google import genai
        from google.genai import types
        
        try:
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=_SYSTEM,
                    temperature=0.3,
                    max_output_tokens=65535,
                    response_mime_type="application/json"
                )
            )
            raw = response.text
            if raw is not None:
                return _parse(raw), None
        except Exception as e:
            print(f"Gemini LLM grade failed: {e}")
            return None, "Could not reach the AI service, using offline mode"
            
    elif os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"):
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "")
        )
        
        try:
            msg = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4"),
                max_completion_tokens=800,
                temperature=1.0,
                messages=[
                    {"role": "system", "content": _SYSTEM},
                    {"role": "user", "content": prompt}
                ],
            )
            raw = msg.choices[0].message.content
            if raw is not None:
                return _parse(raw), None
        except Exception as e:
            print(f"LLM grade failed: {e}")
            return None, "Could not reach the AI service, using offline mode"
            
    return None, None


def _parse(raw: str) -> Optional[dict]:
    """Strip accidental fences and parse. Return None on malformed output so the
    deterministic grade wins rather than crashing the submission."""
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        data = json.loads(cleaned)
        if isinstance(data, dict) and "rubric" in data:
            return data
    except json.JSONDecodeError:
        pass
    return None

def free_write_note(text: str) -> tuple[str, Optional[str]]:
    """Generate a short coaching note for a free-writing session."""
    if not is_configured() or not os.getenv("GOOGLE_API_KEY"):
        return "", None
        
    from google import genai
    from google.genai import types
    
    prompt = (
        "Read this free-writing submission. Write a short qualitative coaching note "
        "(two or three sentences) commenting on the writer's voice, rhythm, and identifying "
        "their single strongest line.\n\n"
        f"TEXT:\n{text}"
    )
    
    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                max_output_tokens=65535
            )
        )
        return response.text.strip() if response.text else "", None
    except Exception as e:
        print(f"Free write note failed: {e}")
        return "", "Could not reach the AI service, using offline mode"
