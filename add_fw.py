import json

with open('knowledge/principles.json', 'r', encoding='utf-8') as f:
    principles = json.load(f)

free_writing_rule = {
    "rule_id": "BOTH-FREE-001",
    "title": "Write freely to build momentum",
    "track": "both",
    "skills": ["free-writing"],
    "principle": "Free-writing is about sustaining momentum without stopping to edit or correct. It helps generate raw material and identify natural habits.",
    "weak_examples": ["Stopping every sentence to check the spelling."],
    "strong_examples": ["Writing continuously for five minutes, capturing whatever comes to mind."],
    "exceptions": ["Editing is necessary later, but not during the free-writing phase."],
    "source": {"document": "Craft Notes", "section": "Free-writing"}
}

principles.append(free_writing_rule)

with open('knowledge/principles.json', 'w', encoding='utf-8') as f:
    json.dump(principles, f, indent=2, ensure_ascii=False)

print("Added BOTH-FREE-001")
