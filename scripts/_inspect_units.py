import json
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'data' / 'units.json'
data = json.loads(p.read_text(encoding='utf-8'))
for cat, obj in data.items():
    if not isinstance(obj, dict) or 'units' not in obj:
        continue
    print(cat + ': ' + ', '.join(code for code, _ in obj['units']))
