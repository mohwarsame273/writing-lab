from domain.exercises import load_exercises, for_mode
from domain.models import Mode
from collections import Counter

exercises = load_exercises()
lit_exercises = for_mode(exercises, Mode.LITERARY)
counts = Counter(e.kind for e in lit_exercises)
print("Literary exercises by kind:")
for k, c in counts.items():
    print(f"  {k}: {c}")

print("Total literary:", sum(counts.values()))
