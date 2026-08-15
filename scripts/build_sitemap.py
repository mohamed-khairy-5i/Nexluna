#!/usr/bin/env python3
"""Generate sitemap.xml from the same build sources used by the site generators.

Lists: Arabic home/converters/pair pages + blog, English /en/ pages, and static content pages.
hreflang pairs are emitted from the build source of truth (build_pages PAGES + content registry).
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://nexluna.netlify.app"

import sys
sys.path.insert(0, str(ROOT))
from build_pages import PAGES, ORDER  # noqa: E402

# Pair pages exist for every ordered pair of units within each category (convert/{from}-to-{to}.html)
try:
    from build_pairs import PAIR_META  # may not exist
except Exception:
    PAIR_META = None

# Discover actual convert pages on disk to stay truthful to the generated artifact.
convert_dir = ROOT / "convert"
pair_paths = sorted(p.relative_to(ROOT).as_posix() for p in convert_dir.glob("*.html")) if convert_dir.is_dir() else []

content = json.loads((ROOT / "data" / "content.json").read_text(encoding="utf-8"))
blog_paths = [f"blog/{article['slug']}.html" for article in content.get("articles", [])]

static = ["about.html", "privacy.html", "contact.html", "404.html", "offline.html"]


def url(loc, changefreq="weekly", priority="0.8", alt=None):
    out = ["  <url>", f"    <loc>{BASE}/{loc}</loc>"]
    out.append(f"    <changefreq>{changefreq}</changefreq>")
    out.append(f"    <priority>{priority}</priority>")
    if alt:
        out.append(f'    <xhtml:link rel="alternate" hreflang="ar" href="{BASE}/{loc}"/>')
        out.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/{alt}"/>')
        out.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/{alt}"/>')
    out.append("  </url>")
    return "\n".join(out)


entries = []

# Home
entries.append(url("", changefreq="daily", priority="1.0", alt="en/"))

# Arabic converters (hreflang to /en/ counterparts)
for cat in ORDER:
    entries.append(url(f"converters/{cat}.html", alt=f"en/converters/{cat}.html"))

# Arabic pair pages (no /en/ counterpart generated yet -> omit hreflang)
for loc in pair_paths:
    entries.append(url(loc, changefreq="weekly", priority="0.6"))

# Blog
entries.append(url("blog/", alt="en/blog/"))
for loc in blog_paths:
    entries.append(url(loc, changefreq="monthly", priority="0.7"))

# English
entries.append(url("en/", changefreq="daily", priority="0.9"))
entries.append(url("en/converters/", changefreq="weekly", priority="0.7"))
for cat in ORDER:
    entries.append(url(f"en/converters/{cat}.html", changefreq="weekly", priority="0.8"))

# Static
for s in static:
    entries.append(url(s, changefreq="monthly", priority="0.3"))

xml = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(entries)
    + "\n</urlset>\n"
)

(ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
print(f"wrote sitemap.xml with {len(entries)} URLs ({len(pair_paths)} pair pages, {len(blog_paths)} articles)")
