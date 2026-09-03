import json

# Load existing data
with open('knowledge/principles.json', 'r', encoding='utf-8') as f:
    principles = json.load(f)

with open('knowledge/exercises.json', 'r', encoding='utf-8') as f:
    exercises = json.load(f)

with open('new_items.json', 'r', encoding='utf-8') as f:
    new_items = json.load(f)

# Append new records
principles.extend(new_items['principles'])
exercises.extend(new_items['exercises'])

# Reconcile references
# Ensure every rule_id referenced in exercises exists in principles
missing_rule_ids = {
    "ACA-NOM-001": {
        "rule_id": "ACA-NOM-001",
        "title": "Restore verbs hidden inside abstract nouns",
        "track": "academic",
        "skills": ["nominalisation", "sentence-economy", "verb-strength"],
        "principle": "Nominalisations turn actions into abstract nouns and often conceal who did what. Recovering the buried verb usually shortens the sentence and names the actor.",
        "weak_examples": ["The implementation of the policy was undertaken by the department."],
        "strong_examples": ["The department implemented the policy."],
        "exceptions": ["Keep the noun when the concept itself is the subject of study."],
        "source": {"document": "Style Guide", "section": "Nominalisations"}
    },
    "ACA-PRE-001": {
        "rule_id": "ACA-PRE-001",
        "title": "Break stacked prepositional phrases",
        "track": "academic",
        "skills": ["prepositions", "sentence-economy"],
        "principle": "Long chains of of/in/to/for phrases force the reader to hold too much in suspension. Recast one or two phrases as a verb or a possessive.",
        "weak_examples": ["The reduction in the level of engagement of students with the content of the module."],
        "strong_examples": ["Students engaged less with the module content."],
        "exceptions": ["Some prepositional chains are unavoidable in precise legal or technical description."],
        "source": {"document": "Style Guide", "section": "Prepositions"}
    },
    "ACA-PAS-001": {
        "rule_id": "ACA-PAS-001",
        "title": "Prefer the active voice unless the actor is genuinely irrelevant",
        "track": "academic",
        "skills": ["passive-voice", "clarity"],
        "principle": "The passive is not an error, but habitual passivity hides agency and adds words. Name the actor when the actor matters.",
        "weak_examples": ["Mistakes were made in the analysis."],
        "strong_examples": ["We made mistakes in the analysis."],
        "exceptions": ["Use the passive when the actor is unknown, obvious, or deliberately de-emphasised."],
        "source": {"document": "Style Guide", "section": "Voice"}
    },
    "ACA-TRN-001": {
        "rule_id": "ACA-TRN-001",
        "title": "Use transitions to signal the logical move, not to decorate",
        "track": "academic",
        "skills": ["transitions", "cohesion"],
        "principle": "A transition should name the relationship between ideas: contrast, cause, concession, addition, sequence. The wrong connective misleads the reader about your argument.",
        "weak_examples": ["The results were strong. However, we were pleased."],
        "strong_examples": ["The results were strong. Accordingly, we extended the trial."],
        "exceptions": [],
        "source": {"document": "Style Guide", "section": "Cohesion"}
    },
    "LIT-IMG-001": {
        "rule_id": "LIT-IMG-001",
        "title": "Prefer the concrete and specific over the abstract",
        "track": "literary",
        "skills": ["concrete-description", "imagery"],
        "principle": "Abstractions tell; concrete, sensory detail shows. Replace a general noun with the particular thing the reader can see, hear or touch.",
        "weak_examples": ["The room conveyed a sense of neglect."],
        "strong_examples": ["Dust furred the piano keys; one lampshade hung at an angle."],
        "exceptions": ["Abstraction can be deliberate for distance or irony."],
        "source": {"document": "Craft Notes", "section": "Concrete detail"}
    },
    "LIT-RHY-001": {
        "rule_id": "LIT-RHY-001",
        "title": "Vary sentence length for rhythm",
        "track": "literary",
        "skills": ["rhythm", "sentence-variation"],
        "principle": "A run of same-length sentences flattens the music of prose. A short sentence after several long ones lands like a beat. Read aloud to hear it.",
        "weak_examples": ["He walked to the door. He opened the door. He looked outside. He saw the rain."],
        "strong_examples": ["He walked to the door and opened it, and for a moment he only looked at the grey street. Then the rain came."],
        "exceptions": ["Deliberate monotony can enact tedium or dread."],
        "source": {"document": "Craft Notes", "section": "Rhythm"}
    },
    "LIT-CLI-001": {
        "rule_id": "LIT-CLI-001",
        "title": "Refresh or cut the cliche",
        "track": "literary",
        "skills": ["freshness", "imagery"],
        "principle": "A cliche is an image the reader no longer sees. Replace it with something exact to your scene, or cut it.",
        "weak_examples": ["Her heart was in her throat as time stood still."],
        "strong_examples": ["She counted her own pulse in the silence and lost the number."],
        "exceptions": ["A character may speak in cliche to reveal character."],
        "source": {"document": "Craft Notes", "section": "Cliche"}
    },
    "BOTH-ADV-001": {
        "rule_id": "BOTH-ADV-001",
        "title": "Let the verb do the work before reaching for an adverb",
        "track": "both",
        "skills": ["ad-words", "verb-strength"],
        "principle": "An -ly adverb propping up a weak verb is usually a sign a sharper verb exists. 'Ran quickly' is 'sprinted'; 'said angrily' is often just 'snapped'.",
        "weak_examples": ["She walked quietly and closed the door softly."],
        "strong_examples": ["She crept out and eased the door shut."],
        "exceptions": ["Keep the adverb when it genuinely changes the meaning of the verb."],
        "source": {"document": "Style Guide", "section": "Modifiers"}
    },
    "ACA-JAR-001": {
        "rule_id": "ACA-JAR-001",
        "title": "Avoid unnecessary jargon",
        "track": "academic",
        "skills": ["clarity", "sentence-economy"],
        "principle": "Jargon is useful when communicating with specialists, but excessive jargon obscures meaning. Use plain language when possible.",
        "weak_examples": ["We leveraged synergistic paradigms to optimize outcomes."],
        "strong_examples": ["We combined our approaches to improve results."],
        "exceptions": ["Use jargon when it is the accepted term of art in your field and your audience expects it."],
        "source": {"document": "Style Guide", "section": "Clarity"}
    },
    "LIT-SHO-001": {
        "rule_id": "LIT-SHO-001",
        "title": "Show, don't tell",
        "track": "literary",
        "skills": ["imagery", "concrete-description"],
        "principle": "Instead of telling the reader how a character feels or what a setting is like, show it through actions, sensory details, and dialogue.",
        "weak_examples": ["She was angry."],
        "strong_examples": ["She slammed the door and kicked the chair."],
        "exceptions": ["Telling is useful for summarizing time or transitioning between scenes."],
        "source": {"document": "Craft Notes", "section": "Showing vs Telling"}
    },
    "ACA-ADV-001": {
        "rule_id": "ACA-ADV-001",
        "title": "Avoid piling up adverbs",
        "track": "academic",
        "skills": ["ad-words", "sentence-economy"],
        "principle": "Too many adverbs can make prose sound cluttered. If a strong verb works better, use it.",
        "weak_examples": ["The data strongly and clearly showed that the hypothesis was totally correct."],
        "strong_examples": ["The data confirmed the hypothesis."],
        "exceptions": ["When an adverb is necessary for precision."],
        "source": {"document": "Style Guide", "section": "Modifiers"}
    }
}

existing_principle_ids = {p['rule_id'] for p in principles}
readded = []

# Add required rules if missing
for rid, rule in missing_rule_ids.items():
    if rid not in existing_principle_ids:
        principles.append(rule)
        readded.append(rid)
        existing_principle_ids.add(rid)

# Check all exercise rule_ids
for ex in exercises:
    for rid in ex.get('rule_ids', []):
        if rid not in existing_principle_ids:
            print(f"Warning: Exercise {ex['exercise_id']} references missing rule_id {rid}")

# Ensure every skill tag used in an exercise is covered by at least one principle
exercise_skills = {ex['skill'] for ex in exercises}
principle_skills = set()
for p in principles:
    principle_skills.update(p.get('skills', []))

missing_skills = exercise_skills - principle_skills
if missing_skills:
    print(f"Warning: These skills are used in exercises but missing from principles: {missing_skills}")

# Save updated files
with open('knowledge/principles.json', 'w', encoding='utf-8') as f:
    json.dump(principles, f, indent=2, ensure_ascii=False)

with open('knowledge/exercises.json', 'w', encoding='utf-8') as f:
    json.dump(exercises, f, indent=2, ensure_ascii=False)

print(f"Added {len(new_items['principles'])} principles and {len(new_items['exercises'])} exercises.")
print(f"Re-added rule_ids: {readded}")
