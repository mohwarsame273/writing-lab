import json
import os

with open('knowledge/principles.json', 'r', encoding='utf-8') as f:
    principles = json.load(f)
    
with open('knowledge/exercises.json', 'r', encoding='utf-8') as f:
    exercises = json.load(f)

with open('literary_bank.json', 'r', encoding='utf-8') as f:
    lit_principles = json.load(f)

with open('literary_exercises.json', 'r', encoding='utf-8') as f:
    lit_exercises = json.load(f)

# Append principles
existing_principle_ids = {p['rule_id'] for p in principles}
added_p = 0
for p in lit_principles:
    if p['rule_id'] not in existing_principle_ids:
        principles.append(p)
        existing_principle_ids.add(p['rule_id'])
        added_p += 1

# Append exercises
existing_ex_ids = {e['exercise_id'] for e in exercises}
added_e = 0
for e in lit_exercises:
    if e['exercise_id'] not in existing_ex_ids:
        exercises.append(e)
        existing_ex_ids.add(e['exercise_id'])
        added_e += 1

# Re-check references
missing_rules = set()
for e in exercises:
    for rid in e.get('rule_ids', []):
        if rid not in existing_principle_ids:
            missing_rules.add(rid)

if missing_rules:
    print(f"Warning: these rules are referenced but missing: {missing_rules}")

with open('knowledge/principles.json', 'w', encoding='utf-8') as f:
    json.dump(principles, f, indent=2, ensure_ascii=False)

with open('knowledge/exercises.json', 'w', encoding='utf-8') as f:
    json.dump(exercises, f, indent=2, ensure_ascii=False)

print(f"Added {added_p} literary principles and {added_e} literary exercises.")
