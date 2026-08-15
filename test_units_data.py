#!/usr/bin/env python3
"""Canonical units schema regression tests."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("generate_units", ROOT / "scripts" / "generate_units.py")
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

data = json.loads((ROOT / "data" / "units.json").read_text(encoding="utf-8"))
validated = module.validate(data)
assert len(validated) == 14
assert set(validated["area"]["base"]) == {"km2", "m2", "cm2", "ha", "feddan", "kirat", "sahm", "dunam", "acre", "ft2", "in2", "mi2"}
assert validated["area"]["base"]["feddan"] != validated["area"]["base"]["acre"]
assert validated["area"]["provenance"]["schema_version"] == "1.0"
assert set(validated["area"]["unit_provenance"]) == set(validated["area"]["base"])
assert validated["area"]["unit_provenance"]["feddan"]["region"] == "Egypt"
assert validated["area"]["unit_provenance"]["feddan"]["reviewed"] == "2026-08-15"

broken = copy.deepcopy(data)
del broken["frequency"]
try:
    module.validate(broken)
except ValueError as exc:
    assert "missing categories" in str(exc)
else:
    raise AssertionError("validator accepted a source missing a required category")

broken_provenance = copy.deepcopy(data)
del broken_provenance["area"]["unit_provenance"]["feddan"]["source"]
try:
    module.validate(broken_provenance)
except ValueError as exc:
    assert "provenance missing source" in str(exc)
else:
    raise AssertionError("validator accepted a unit without provenance source")

print("PASS — canonical units schema validates 14 categories, 100 unit records, and rejects missing provenance.")
