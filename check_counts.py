from retrieval.loader import load_principles
from domain.exercises import load_exercises

p = load_principles()
e = load_exercises()
print(f"Total principles: {len(p)}")
print(f"Total exercises: {len(e)}")
