import json
import os

with open('sources_text.json', 'r') as f:
    data = json.load(f)

for k, v in data.items():
    print(f"--- {k} ---")
    print(v[:500])
    print("...")
