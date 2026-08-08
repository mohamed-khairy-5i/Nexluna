#!/usr/bin/env python3
"""Nexluna — i18n foundation loader + validator (ROADMAP G0.1).

Loads data/locales.json (the single source of truth for the global expansion)
and validates its integrity. This is the first CI quality gate for the global
plan — it embodies the multi-role review baked into the roadmap so that a bad
locale entry can never ship:

  Role 2 (i18n)        : every language has a native name + valid direction.
  Role 3 (measurement) : measurement/gallon values are from the allowed set and
                         mutually consistent (a 'us' gallon only with us/imperial).
  Role 10 (data)       : ISO-code shape, unique langs, EXACTLY ONE root language,
                         number separators are distinct, wave is a non-negative int.

Run:  python3 build_i18n.py   (exits non-zero on any violation)
Import:  from build_i18n import load_locales, LOCALES, ROOT_LANG
"""
import os
import re
import sys
import json

HERE = os.path.dirname(__file__)
DATA_PATH = os.path.join(HERE, "data", "locales.json")

DIRS = {"rtl", "ltr"}
MEASURE = {"metric", "us", "imperial"}
GALLON = {"us", "imperial", "none"}
ISO639 = re.compile(r"^[a-z]{2,3}$")
ISO3166 = re.compile(r"^[A-Z]{2}$")
ISO4217 = re.compile(r"^[A-Z]{3}$")


def load_locales(path=DATA_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(doc):
    errors = []
    langs = doc.get("languages", [])
    if not langs:
        errors.append("no languages defined")
        return errors

    seen = set()
    roots = []
    for i, e in enumerate(langs):
        tag = e.get("lang", "<missing>")
        where = "languages[%d] (%s)" % (i, tag)

        # Role 10 — ISO shape + uniqueness
        if not ISO639.match(e.get("lang", "")):
            errors.append("%s: invalid ISO 639 lang code" % where)
        if tag in seen:
            errors.append("%s: duplicate lang code" % where)
        seen.add(tag)

        # Role 2 — native name + direction
        if not e.get("name_native"):
            errors.append("%s: missing name_native" % where)
        if not e.get("name_en"):
            errors.append("%s: missing name_en" % where)
        if e.get("dir") not in DIRS:
            errors.append("%s: dir must be one of %s" % (where, DIRS))

        # root tracking
        if e.get("root") is True:
            roots.append(tag)

        # wave
        w = e.get("wave")
        if not isinstance(w, int) or w < 0:
            errors.append("%s: wave must be a non-negative int" % where)

        # Role 10 — number format
        num = e.get("number", {})
        dec, grp = num.get("decimal"), num.get("group")
        if not dec or not grp:
            errors.append("%s: number.decimal and number.group are required" % where)
        elif dec == grp:
            errors.append("%s: decimal and group separators must differ" % where)
        if not num.get("intl_locale"):
            errors.append("%s: number.intl_locale (BCP-47) required" % where)

        # Role 3 — measurement consistency
        m, g = e.get("measurement"), e.get("gallon")
        if m not in MEASURE:
            errors.append("%s: measurement must be one of %s" % (where, MEASURE))
        if g not in GALLON:
            errors.append("%s: gallon must be one of %s" % (where, GALLON))
        if g == "us" and m == "metric":
            errors.append("%s: gallon 'us' inconsistent with measurement 'metric'" % where)

        # currency
        if not ISO4217.match(e.get("currency", "")):
            errors.append("%s: invalid ISO 4217 currency" % where)

    # Role 4 / G0.4 — exactly one root language (served at /)
    if len(roots) != 1:
        errors.append("exactly one language must have root=true, found: %s" % (roots or "none"))

    # country_language map integrity (Role 4)
    cl = {k: v for k, v in doc.get("country_language", {}).items() if not k.startswith("$")}
    for code, lang in cl.items():
        if not ISO3166.match(code):
            errors.append("country_language: invalid ISO 3166 code '%s'" % code)
        if lang not in seen:
            errors.append("country_language: '%s' maps to unknown language '%s'" % (code, lang))

    return errors


_doc = load_locales()
LOCALES = _doc["languages"]
ROOT_LANG = next((e["lang"] for e in LOCALES if e.get("root")), None)


def main():
    doc = load_locales()
    errs = validate(doc)
    langs = doc["languages"]
    if errs:
        print("i18n validation FAILED (%d issue(s)):" % len(errs), file=sys.stderr)
        for e in errs:
            print("  - " + e, file=sys.stderr)
        sys.exit(1)
    waves = {}
    for e in langs:
        waves.setdefault(e["wave"], []).append(e["lang"])
    print("i18n OK — %d languages, root=%s" % (len(langs), ROOT_LANG))
    for w in sorted(waves):
        tag = "live" if w == 0 else "wave %d" % w
        print("  %s: %s" % (tag, ", ".join(waves[w])))


if __name__ == "__main__":
    main()
