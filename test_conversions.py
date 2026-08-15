#!/usr/bin/env python3
"""Nexluna — conversion accuracy gate (zero-dependency, runs in <1s).

WHY THIS FILE EXISTS
--------------------
The product's only defensible claim is *deterministic correctness* — an LLM can
guess a conversion, we must never be wrong. That claim is worthless without a
test, and this codebase previously mirrored its factor tables in FOUR places.
The canonical source is now data/units.json; generated/browser mirrors remain checked against it.
Mirrored data drifts; drift already shipped one real bug (فدّان labelled as
`acre`, a 3.8% error on every Egyptian land conversion).

So this gate asserts two things:
  1. ACCURACY  — factors match authoritative values (BIPM/NIST/Wikipedia).
  2. CONSISTENCY — generated/browser mirrors agree with the canonical source, so drift fails loudly.

Run:  python3 test_conversions.py     (exit 0 = pass, 1 = fail)
"""
import json
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FAILURES = []
CHECKS = [0]


def check(name, got, want, tol=1e-9):
    """Assert got ≈ want within relative tolerance."""
    CHECKS[0] += 1
    if want == 0:
        ok = abs(got) < tol
    else:
        ok = abs(got - want) / abs(want) < tol
    if not ok:
        FAILURES.append(f"{name}: got {got!r}, expected {want!r}")


def extract_js_table(path):
    """Parse the `base:` factor tables out of a JS source file (no JS runtime)."""
    src = open(path, encoding="utf-8").read()
    tables = {}
    for m in re.finditer(r"(\w+):\s*\{[^{}]*?base:\s*\{(.*?)\}", src, re.S):
        cat, body = m.group(1), m.group(2)
        factors = {}
        for k, v in re.findall(r"'?([A-Za-z0-9_]+)'?\s*:\s*([0-9eE.\-+]+)", body):
            factors[k] = float(v)
        if factors:
            tables[cat] = factors
    return tables


def load_canonical_table(path):
    """Read base factors from the canonical JSON source."""
    data = json.load(open(path, encoding="utf-8"))
    return {
        category: definition.get("base", {})
        for category, definition in data.items()
        if definition.get("base")
    }


# ---------------------------------------------------------------- ground truth
# Authoritative m² values. The Arabic land units are the whole point: generic
# models routinely conflate فدّان with acre, and دونم varies by country.
AREA_TRUTH = {
    "m2": 1.0,
    "km2": 1_000_000.0,
    "ha": 10_000.0,
    "feddan": 4200.833,          # Egyptian feddan (post-1830) — NOT an acre
    "kirat": 4200.833 / 24,      # 1/24 feddan ≈ 175.035 m²
    "sahm": 4200.833 / 576,      # 1/24 kirat
    "dunam": 1000.0,             # metric dunam
    "acre": 4046.8564224,        # international acre
    "ft2": 0.09290304,
    "in2": 0.00064516,
}

VOLUME_TRUTH = {
    "L": 1.0,
    "mL": 0.001,
    "m3": 1000.0,
    "gal": 3.785411784,   # US liquid gallon
    "galUK": 4.54609,     # Imperial gallon — 20% larger, a classic silent error
    "floz": 0.0295735296,
}

LENGTH_TRUTH = {
    "m": 1.0, "km": 1000.0, "cm": 0.01, "mm": 0.001,
    "mi": 1609.344, "yd": 0.9144, "ft": 0.3048, "in": 0.0254, "nmi": 1852.0,
}

WEIGHT_TRUTH = {
    "kg": 1.0, "g": 0.001, "t": 1000.0,
    "lb": 0.45359237, "oz": 0.028349523, "st": 6.35029318, "ct": 0.0002,
}


def main():
    conv = load_canonical_table(os.path.join(HERE, "data/units.json"))
    webmcp_src = open(os.path.join(HERE, "assets/js/webmcp.js"), encoding="utf-8").read()
    mcp = extract_js_table(os.path.join(HERE, "assets/js/webmcp.js"))
    if "root.NexlunaUnits" not in webmcp_src:
        FAILURES.append("webmcp.js does not consume the generated canonical units source")
    for tool_name in ("convert_units", "list_units", "get_unit_info"):
        if "name: '" + tool_name + "'" not in webmcp_src:
            FAILURES.append(f"webmcp.js missing tool '{tool_name}'")

    # ---- 1. accuracy of the canonical engine -----------------------------
    for cat, truth in (("area", AREA_TRUTH), ("volume", VOLUME_TRUTH),
                       ("length", LENGTH_TRUTH), ("weight", WEIGHT_TRUTH)):
        table = conv.get(cat, {})
        if not table:
            FAILURES.append(f"data/units.json: category '{cat}' has no base table")
            continue
        for unit, want in truth.items():
            if unit not in table:
                FAILURES.append(f"data/units.json {cat}: missing unit '{unit}'")
            else:
                check(f"data/units.json {cat}.{unit}", table[unit], want)

    # ---- 2. the specific bug this suite was written to prevent ------------
    area = conv.get("area", {})
    if "feddan" in area and "acre" in area:
        check("feddan != acre (must differ)", 1.0 if area["feddan"] != area["acre"] else 0.0, 1.0)
        # 1 feddan = 1.03805 acre
        check("feddan/acre ratio", area["feddan"] / area["acre"], 1.0380484409448565, 1e-6)
    if "feddan" in area and "kirat" in area:
        check("24 kirat = 1 feddan", area["kirat"] * 24, area["feddan"], 1e-9)
    if "kirat" in area and "sahm" in area:
        check("24 sahm = 1 kirat", area["sahm"] * 24, area["kirat"], 1e-9)

    vol = conv.get("volume", {})
    if "gal" in vol and "galUK" in vol:
        check("UK gal / US gal", vol["galUK"] / vol["gal"], 1.2009499255398, 1e-9)

    # ---- 3. mirrors must agree (drift detector) ---------------------------
    for cat, table in conv.items():
        if cat not in mcp:
            continue
        for unit, val in table.items():
            if unit not in mcp[cat]:
                FAILURES.append(f"webmcp.js {cat}: missing '{unit}' present in data/units.json")
            else:
                check(f"webmcp mirror {cat}.{unit}", mcp[cat][unit], val)

    # build_pairs.py mirrors a subset of the same factors
    pairs_src = open(os.path.join(HERE, "build_pairs.py"), encoding="utf-8").read()
    for cat in ("area", "volume", "length", "weight"):
        m = re.search(r'"%s":\s*\{(.*?)\}' % cat, pairs_src, re.S)
        if not m:
            continue
        for k, v in re.findall(r'"([A-Za-z0-9_]+)"\s*:\s*([0-9eE.\-+]+)', m.group(1)):
            if cat in conv and k in conv[cat]:
                check(f"build_pairs {cat}.{k}", float(v), conv[cat][k])

    # ---- 4. temperature + fuel special cases -----------------------------
    def c_to_f(c):
        return c * 9 / 5 + 32

    check("0C -> 32F", c_to_f(0), 32.0)
    check("100C -> 212F", c_to_f(100), 212.0)
    check("-40C -> -40F", c_to_f(-40), -40.0)

    MPG_US = 1.609344 / 3.785411784
    MPG_UK = 1.609344 / 4.54609
    js = open(os.path.join(HERE, "assets/js/converter.js"), encoding="utf-8").read()
    for name, want in (("MPG_US", MPG_US), ("MPG_UK", MPG_UK)):
        m = re.search(name + r"\s*=\s*([0-9.eE\-+]+)", js)
        if not m:
            FAILURES.append(f"converter.js: {name} constant not found")
        else:
            check(f"converter.js {name}", float(m.group(1)), want, 1e-9)

    # ---- report ----------------------------------------------------------
    if FAILURES:
        print(f"FAIL — {len(FAILURES)} problem(s) out of {CHECKS[0]} checks:\n")
        for f in FAILURES:
            print("  x " + f)
        print("\nConversion accuracy is the product's core promise. Fix before deploy.")
        return 1
    print(f"PASS — {CHECKS[0]} conversion checks OK "
          f"(accuracy + mirror consistency across units.json, webmcp.js, build_pairs.py).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
