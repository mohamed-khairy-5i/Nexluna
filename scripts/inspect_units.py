import json
from pathlib import Path

source = json.loads((Path(__file__).resolve().parents[1] / 'data' / 'units.json').read_text(encoding='utf-8'))
for category, definition in source.items():
    print(category, ':', ', '.join(code for code, _ in definition.get('units', [])))
