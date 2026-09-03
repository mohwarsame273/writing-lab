import docx
import os
import json

def read_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

files = os.listdir("knowledge/sources")
data = {}
for f in files:
    if f.endswith('.docx'):
        data[f] = read_docx(os.path.join("knowledge/sources", f))

with open('sources_text.json', 'w') as f:
    json.dump(data, f, indent=2)
