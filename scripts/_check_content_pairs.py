"""Verify article unit_pairs exist in canonical units.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
content = json.loads((ROOT / "data" / "content.json").read_text(encoding="utf-8"))
data = json.loads((ROOT / "data" / "units.json").read_text(encoding="utf-8"))

bad = []
for a in content["articles"]:
    cat = a["category"]
    if cat not in data:
        bad.append(f"missing category {cat} in {a['slug']}")
        continue
    unit_ids = set(u[0] for u in data[cat].get("units", []))
    for frm, to in a.get("unit_pairs", []):
        for sym in (frm, to):
            if sym and sym not in unit_ids:
                bad.append(f"slug={a['slug']} symbol '{sym}' not found in {cat} (units: {sorted(unit_ids)})")
                break

print("problems:", bad or "none")
