"""Acceptance checks for the first complete English locale."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
units = json.loads((ROOT / "data" / "units.json").read_text(encoding="utf-8"))
en = json.loads((ROOT / "data" / "i18n" / "en.json").read_text(encoding="utf-8"))

assert en["lang"] == "en"
assert en["dir"] == "ltr"
assert en["root"] == "/en/"
assert set(en["categories"]) == set(units)
assert set(en["units"]) == set(units)
for category, data in units.items():
    canonical_codes = {item[0] for item in data.get("units", [])}
    localized_codes = set(en["units"][category])
    assert localized_codes == canonical_codes, f"unit coverage mismatch: {category}"
    meta = en["categories"][category]
    for key in ("label", "title", "description", "intro", "formulas", "common"):
        assert meta.get(key), f"missing {category}.{key}"

locale_js = (ROOT / "assets/js/locale.en.generated.js").read_text(encoding="utf-8")
assert "window.NexlunaLocale" in locale_js
assert "from {from} to {to}" in locale_js

for category in units:
    page = ROOT / "en" / "converters" / f"{category}.html"
    assert page.exists(), f"missing English page: {page}"
    html = page.read_text(encoding="utf-8")
    assert '<html lang="en" dir="ltr">' in html
    assert "/assets/js/locale.en.generated.js" in html
    assert f'data-only="{category}"' in html
    assert f"/en/converters/{category}.html" in html

home = (ROOT / "en" / "index.html").read_text(encoding="utf-8")
assert '<html lang="en" dir="ltr">' in home
assert "/assets/js/smartsearch.js" in home
assert 'href="/en/"' in home

converter = (ROOT / "assets/js/converter.js").read_text(encoding="utf-8")
assert "window.NexlunaLocale" in converter
assert "NexConvert" in converter
assert "var DATA = window.NexlunaUnits" in converter
assert not re.search(r"var\s+(?:DATA|BASE)\s*=\s*\{", converter)

print("i18n checks passed: English locale covers 14 categories and all canonical units")
