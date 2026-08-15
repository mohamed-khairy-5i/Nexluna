#!/usr/bin/env python3
"""Week 4 regression checks for PWA, deep links, sharing, and accessibility."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
index = (ROOT / "index.html").read_text(encoding="utf-8")
category = (ROOT / "converters" / "length.html").read_text(encoding="utf-8")
pair = (ROOT / "convert" / "km-to-mi.html").read_text(encoding="utf-8")
main = (ROOT / "assets" / "js" / "main.js").read_text(encoding="utf-8")
converter = (ROOT / "assets" / "js" / "converter.js").read_text(encoding="utf-8")
sw = (ROOT / "sw.js").read_text(encoding="utf-8")
css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
manifest = (ROOT / "manifest.webmanifest").read_text(encoding="utf-8")

assert 'rel="manifest"' in index
assert 'data-pwa-install' in index
assert 'beforeinstallprompt' in main and 'appinstalled' in main
assert "nexluna-v6" in sw
for asset in ("smartsearch.js", "webmcp.js", "units.generated.js", "explain.js", "embed.js", "converter.js", "locale.en.generated.js"):
    assert f"/assets/js/{asset}" in sw
assert "'/en/'" in sw
assert "'/en/converters/index.html'" in sw

for page in (index, category, pair):
    assert "/assets/js/units.generated.js" in page
    assert "/assets/js/webmcp.js" in page
assert "/assets/js/explain.js" in index and "/assets/js/explain.js" in category
assert "/assets/js/converter.js" in index and "/assets/js/converter.js" in category
assert index.index("/assets/js/units.generated.js") < index.index("/assets/js/converter.js")
assert category.index("/assets/js/units.generated.js") < category.index("/assets/js/converter.js")

assert "copyTextFallback" in converter
assert "aria-controls" in converter and "role: 'tabpanel'" in converter
assert "navigator.share" in converter and "copyText(url" in converter
assert '"display": "standalone"' in manifest
assert ".cta-actions" in css and "prefers-reduced-motion" in css

print("PASS — Week 4 PWA, install prompt, deep-link/share, offline assets, and accessibility checks verified.")
