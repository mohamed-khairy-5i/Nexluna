"""Diagnose failing assertion in test_pwa_accessibility line by line."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = (ROOT / "index.html").read_text(encoding="utf-8")
category = (ROOT / "converters" / "length.html").read_text(encoding="utf-8")
pair = (ROOT / "convert" / "km-to-mi.html").read_text(encoding="utf-8")
main = (ROOT / "assets" / "js" / "main.js").read_text(encoding="utf-8")
converter = (ROOT / "assets" / "js" / "converter.js").read_text(encoding="utf-8")
sw = (ROOT / "sw.js").read_text(encoding="utf-8")
css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
manifest = (ROOT / "manifest.webmanifest").read_text(encoding="utf-8")

checks = [
    ('rel="manifest" in index', 'rel="manifest"' in index),
    ("data-pwa-install in index", "data-pwa-install" in index),
    ("beforeinstallprompt/appinstalled in main", "beforeinstallprompt" in main and "appinstalled" in main),
    ("nexluna-v6 in sw", "nexluna-v6" in sw),
]
for asset in ("smartsearch.js", "webmcp.js", "units.generated.js", "explain.js", "embed.js", "converter.js", "locale.en.generated.js"):
    checks.append((f"/assets/js/{asset} in sw", f"/assets/js/{asset}" in sw))
for route in ("/en/", "/en/converters/length.html"):
    checks.append((f'"{route}" in sw', f'"{route}"' in sw))
for page in (index, category, pair):
    checks.append(("/assets/js/units.generated.js in page", "/assets/js/units.generated.js" in page))
    checks.append(("/assets/js/webmcp.js in page", "/assets/js/webmcp.js" in page))
checks.append(("explain.js in index+category", "/assets/js/explain.js" in index and "/assets/js/explain.js" in category))
checks.append(("converter.js in index+category", "/assets/js/converter.js" in index and "/assets/js/converter.js" in category))
checks.append(("units before converter in index", index.index("/assets/js/units.generated.js") < index.index("/assets/js/converter.js")))
checks.append(("units before converter in category", category.index("/assets/js/units.generated.js") < category.index("/assets/js/converter.js")))
checks.append(("copyTextFallback in converter", "copyTextFallback" in converter))
checks.append(("aria-controls/role tabpanel in converter", "aria-controls" in converter and "role: 'tabpanel'" in converter))
checks.append(("navigator.share + copyText(url in converter", "navigator.share" in converter and "copyText(url" in converter))
checks.append(('"display": "standalone" in manifest', '"display": "standalone"' in manifest))
checks.append((".cta-actions + prefers-reduced-motion in css", ".cta-actions" in css and "prefers-reduced-motion" in css))

for name, ok in checks:
    if not ok:
        print("FAIL:", name)
