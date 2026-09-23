from __future__ import annotations

import json
import os
from typing import Optional

from domain.models import Exercise, Mode, ExerciseKind

_GEN_SYSTEM = (
    "You are an expert writing tutor creating a single practice exercise. "
    "Output exactly one JSON object matching the Exercise dataclass shape, "
    "with no markdown formatting or extra text. "
    "Required keys: exercise_id, kind, mode, skill, prompt, seed_text, target, "
    "options (array of strings, for selection kinds), answer_index (int, for selection kinds), "
    "hints (array of strings), rule_ids (array of strings), max_xp (int), difficulty (int)."
)

def generate_exercise(mode: Mode, skill: str) -> tuple[Optional[Exercise], Optional[str]]:
    from services.llm_grader import is_configured
    if not is_configured() or not os.getenv("GOOGLE_API_KEY"):
        return None, None
        
    from google import genai
    from google.genai import types
    
    prompt = (
        f"Generate a new exercise for mode: {mode.value}, focusing on the skill: '{skill}'.\n"
        f"Make it engaging and unique. Choose an appropriate ExerciseKind.\n"
        f"Ensure 'options' has choices and 'answer_index' is set if the kind is a selection type.\n"
    )
    
    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=_GEN_SYSTEM,
                temperature=0.7,
                max_output_tokens=65535,
                response_mime_type="application/json"
            )
        )
        raw = response.text
        if raw is None:
            return None, "Empty response from AI service"
            
        cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(cleaned)
        
        # Validate
        if "exercise_id" not in data or "kind" not in data or "mode" not in data:
            return None, "Invalid exercise shape returned"
            
        if data["kind"] in {"diagnostic_selection", "transitions"}:
            if not data.get("options") or data.get("answer_index") is None:
                return None, "Invalid selection options"
                
        if data["mode"] != mode.value and data["mode"] != "both":
            return None, "Incorrect mode returned"
            
        ex = Exercise(
            exercise_id=data.get("exercise_id", "gen-1"),
            kind=data.get("kind", "rewrite"),
            mode=data.get("mode", mode.value),
            skill=data.get("skill", skill),
            prompt=data.get("prompt", ""),
            seed_text=data.get("seed_text", ""),
            target=data.get("target", ""),
            options=data.get("options", []),
            answer_index=data.get("answer_index", None),
            hints=data.get("hints", []),
            rule_ids=data.get("rule_ids", []),
            max_xp=int(data.get("max_xp", 100)),
            difficulty=int(data.get("difficulty", 2))
        )
        return ex, None
        
    except Exception as e:
        print(f"Exercise generation failed: {e}")
        return None, "Could not reach the AI service, using offline mode"
