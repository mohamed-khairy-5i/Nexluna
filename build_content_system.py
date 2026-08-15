#!/usr/bin/env python3
"""Generate educational content pages from data/content.json.

Produces cross-linked converter↔article sections appended under each category
converter page (ar + en) and a glossary/faq section. Article bodies remain in
build_blog.py; this module only consumes the canonical registry so that slugs,
dates, categories and pairs stay consistent across blog, converters, and sitemaps.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = json.loads((ROOT / "data" / "content.json").read_text(encoding="utf-8"))
DATA = json.loads((ROOT / "data" / "units.json").read_text(encoding="utf-8"))

AR_LABELS = {c: DATA[c].get("label", c) for c in DATA}
EN_LABELS = json.loads((ROOT / "data" / "i18n" / "en.json").read_text(encoding="utf-8"))["categories"]


def article_links(lang):
    """Map slug → article page url for the given locale."""
    if lang == "en":
        return {a["slug"]: f"/en/blog/{a['slug']}.html" for a in CONTENT["articles"]}
    return {a["slug"]: f"/blog/{a['slug']}.html" for a in CONTENT["articles"]}


def converter_links(lang, cat):
    """Related article links for a category (ar | en)."""
    links = []
    for a in CONTENT["articles"]:
        if a["category"] == cat:
            href = f"/en/blog/{a['slug']}.html" if lang == "en" else f"/blog/{a['slug']}.html"
            title = a[f"title_{lang}"] if f"title_{lang}" in a else a["title_ar"]
            links.append((href, title))
    return links


def glossary_items(lang):
    """FAQ-topics index rows: topic slug, question, and the canonical source article when known."""
    map_q = {
        "feddan-vs-acre": ("ما الفرق بين الفدّان والأكر؟", "What is the difference between the feddan and the acre?"),
        "gb-vs-gib": ("ما الفرق بين GB وGiB؟", "What is the difference between GB and GiB?"),
        "celsius-fahrenheit": ("كيف أحوّل بين السيلسيوس والفهرنهايت؟", "How do I convert between Celsius and Fahrenheit?"),
        "us-vs-imperial-gallon": ("ما الفرق بين الغالون الأمريكي والبريطاني؟", "US vs UK gallon: what's the difference?"),
        "kb-vs-kib": ("هل الكيلوبايت 1000 أم 1024 بايت؟", "Is a kilobyte 1000 or 1024 bytes?"),
    }
    out = []
    for topic in CONTENT["faq_topics"]:
        q_ar, q_en = map_q[topic]
        q = q_en if lang == "en" else q_ar
        out.append((topic, q))
    return out


def registry():
    return CONTENT


if __name__ == "__main__":
    print("content.json articles:", len(CONTENT["articles"]))
    for a in CONTENT["articles"]:
        print(" -", a["slug"], a["category"], a["date"])
    print("faq topics:", len(CONTENT["faq_topics"]))
