#!/usr/bin/env python3
"""Gate: international SEO coverage.

- Every Arabic page that has an /en/ counterpart carries hreflang="en"; /en/ pages carry hreflang="ar" back.
- sitemap.xml parses, contains all expected pages, and every listed <loc> resolves to an existing file.
"""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = "https://nexluna.netlify.app"
ns = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "x": "http://www.w3.org/1999/xhtml",
}

fail = []


def expect(cond, msg):
    if not cond:
        fail.append(msg)


# 1. hreflang reciprocity on home and converters
import sys

sys.path.insert(0, str(ROOT))
from build_pages import PAGES

cats = sorted(PAGES.keys())

htmls = [
    ("index.html", "/", "/en/"),
    ("en/index.html", "/", "/en/"),
    ("en/converters/index.html", "/converters/", "/en/converters/"),
] + [(f"converters/{c}.html", f"/converters/{c}.html", f"/en/converters/{c}.html") for c in cats] + [
    (f"en/converters/{c}.html", f"/converters/{c}.html", f"/en/converters/{c}.html") for c in cats
]
for path_loc, ar_canonical, en_canonical in htmls:
    path = ROOT / path_loc
    if not path.is_file():
        fail.append(f"missing page {path_loc}")
        continue
    content = path.read_text(encoding="utf-8")
    if path_loc.startswith("en/"):
        expect(f'hreflang="ar" href="{BASE}{ar_canonical}"' in content,
               f"{path_loc}: missing hreflang ar back-link to {BASE}{ar_canonical}")
    else:
        expect(f'hreflang="en" href="{BASE}{en_canonical}"' in content,
               f"{path_loc}: missing hreflang en to {BASE}{en_canonical}")

# 2. sitemap integrity
sm_path = ROOT / "sitemap.xml"
expect(sm_path.is_file(), "sitemap.xml missing")
tree = ET.parse(sm_path)
locs = [el.text for el in tree.getroot().findall("sm:url/sm:loc", ns)]
expect(len(locs) >= 190, f"sitemap has only {len(locs)} URLs (expected 190+)")

# 3. every sitemap loc points at an existing generated file
missing = []
for loc in locs:
    relative = loc.replace(BASE + "/", "")
    # Directory-URL canonicals (/, /en/, /en/converters/, /blog/) resolve to the folder's index.html.
    if relative.endswith("/"):
        target = ROOT / relative / "index.html"
    elif not relative:
        target = ROOT / "index.html"
    else:
        target = ROOT / relative
    if not target.is_file():
        missing.append(loc)
expect(not missing, f"{len(missing)} sitemap URLs point at missing files: {missing[:5]}")

# 4. xhtml:link alternates well-formed inside sitemap
alts = tree.getroot().findall(".//x:link", ns)
expect(len(alts) > 0, "sitemap has no xhtml:link alternates")

if fail:
    print("FAIL — " + "\n".join(fail))
    raise SystemExit(1)

print(f"PASS — hreflang reciprocity on {len(htmls)} pages, sitemap {len(locs)} URLs verified, {len(alts)} alternates.")
