import json

with open('knowledge/exercises.json', 'r', encoding='utf-8') as f:
    exercises = json.load(f)

with open('literary_drills_extra.json', 'r', encoding='utf-8') as f:
    extra = json.load(f)

existing_ex_ids = {e['exercise_id'] for e in exercises}
added = 0
for e in extra:
    if e['exercise_id'] not in existing_ex_ids:
        exercises.append(e)
        existing_ex_ids.add(e['exercise_id'])
        added += 1

with open('knowledge/exercises.json', 'w', encoding='utf-8') as f:
    json.dump(exercises, f, indent=2, ensure_ascii=False)

print(f"Added {added} extra literary drills.")
