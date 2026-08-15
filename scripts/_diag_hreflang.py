#!/usr/bin/env python3
"""Line-by-line replay of test_hreflang_sitemap.py to locate the false failures."""
import json
import pathlib
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build_pages import PAGES

BASE = "https://nexluna.netlify.app"
cats = sorted(PAGES.keys())
htmls = ["index.html", "en/index.html"] + [f"converters/{c}.html" for c in cats] + [f"en/converters/{c}.html" for c in cats]

for loc in ("index.html", "en/index.html"):
    content = (ROOT / loc).read_text(encoding="utf-8")
    if loc == "index.html":
        needle = f'hreflang="en" href="{BASE}/en/index.html"'
    else:
        needle = f'hreflang="ar" href="{BASE}/index.html"'
    found = needle in content
    print(f"{loc}: expect={needle!r} found={found}")
    if not found:
        sample = re_matches = [m.group(0) for m in __import__("re").finditer(r'hreflang="(en|ar)" href="[^"]*"', content)]
        print("   actual alternates:", sample[:6])

tree = ET.parse(ROOT / "sitemap.xml")
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
locs = [el.text for el in tree.getroot().findall("sm:url/sm:loc", ns)]
missing = []
for loc in locs:
    relative = loc.replace(BASE + "/", "")
    target = ROOT / (relative if relative else "index.html")
    if not target.is_file():
        missing.append(loc)
print("sitemap total:", len(locs), "missing:", missing)
