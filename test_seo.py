#!/usr/bin/env python3
"""SEO and structured-data regression checks for generated Nexluna pages."""
from __future__ import annotations

import json
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.jsonld = []
        self.title = ""
        self._in_title = False
        self._jsonld = False
        self._buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href", ""))
        if tag == "title":
            self._in_title = True
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self._jsonld = True
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._jsonld:
            self.jsonld.append("".join(self._buf))
            self._jsonld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._jsonld:
            self._buf.append(data)


def inspect(path: Path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    objects = []
    for raw in parser.jsonld:
        value = json.loads(raw)
        objects.extend(value if isinstance(value, list) else [value])
    return parser, objects


def main():
    category_pages = sorted((ROOT / "converters").glob("*.html"))
    pair_pages = sorted((ROOT / "convert").glob("*.html"))
    assert len(category_pages) == 14, len(category_pages)
    assert len(pair_pages) == 163, len(pair_pages)
    all_canonicals = []

    for path in category_pages + pair_pages:
        parser, objects = inspect(path)
        assert parser.title.strip(), path
        assert len(parser.canonicals) == 1, path
        canonical = parser.canonicals[0]
        assert canonical.startswith("https://nexluna.netlify.app/"), (path, canonical)
        all_canonicals.append(canonical)
        types = {item.get("@type") for item in objects}
        if path.parent.name == "convert" and path.name == "index.html":
            assert "ItemList" in types, path
            continue
        assert "BreadcrumbList" in types, path
        assert "FAQPage" in types, path
        assert "HowTo" in types, path
        if path.parent.name == "converters":
            assert "WebApplication" in types, path
            app = next(item for item in objects if item.get("@type") == "WebApplication")
            assert app.get("dateModified") == "2026-08-15", path
            assert isinstance(app.get("author"), dict), path
        if path.parent.name == "convert" and path.name != "index.html":
            assert "WebApplication" in types, path

    assert len(all_canonicals) == len(set(all_canonicals)), "duplicate canonical URLs"
    print(f"SEO OK: {len(category_pages)} category pages + {len(pair_pages)} pair/index pages")
    print("JSON-LD OK: BreadcrumbList, FAQPage, HowTo, and WebApplication contracts verified")


if __name__ == "__main__":
    main()
