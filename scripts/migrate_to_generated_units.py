#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONVERTER = ROOT / "assets" / "js" / "converter.js"


def migrate_converter() -> None:
    path = CONVERTER
    text = path.read_text(encoding="utf-8")
    start = "  /* ---------- Data (base-unit factor tables) ---------- */\n  var DATA = {"
    end = "  };\n\n  var STORE ="
    if start not in text:
        raise SystemExit("converter data start marker not found")
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    replacement = (
        "  /* ---------- Data (generated canonical source) ---------- */\n"
        "  var DATA = window.NexlunaUnits || {};\n"
        "  if (!Object.keys(DATA).length) throw new Error('Nexluna units data not loaded');\n\n"
        "  var STORE ="
    )
    path.write_text(text[:start_index] + replacement + text[end_index + len("  };\n\n  var STORE ="):], encoding="utf-8")


def add_generated_script() -> None:
    for path in ROOT.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        marker = '  <script src="/assets/js/converter.js" defer></script>'
        generated = '  <script src="/assets/js/units.generated.js" defer></script>'
        if marker in text and generated not in text:
            text = text.replace(marker, generated + "\n" + marker, 1)
            path.write_text(text, encoding="utf-8")


def update_service_worker() -> None:
    path = ROOT / "sw.js"
    text = path.read_text(encoding="utf-8")
    marker = "  '/assets/js/converter.js',"
    generated = "  '/assets/js/units.generated.js',"
    if generated not in text:
        if marker not in text:
            raise SystemExit("service worker converter marker not found")
        text = text.replace(marker, generated + "\n" + marker, 1)
        text = text.replace("const CACHE = 'nexluna-v2';", "const CACHE = 'nexluna-v3';", 1)
        path.write_text(text, encoding="utf-8")


def update_node_test() -> None:
    path = ROOT / "test_smartsearch.js"
    text = path.read_text(encoding="utf-8")
    marker = "load('assets/js/converter.js');"
    generated = "load('assets/js/units.generated.js');"
    if generated not in text:
        if marker not in text:
            raise SystemExit("Smart Search test converter marker not found")
        text = text.replace(marker, generated + "\n" + marker, 1)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    migrate_converter()
    add_generated_script()
    update_service_worker()
    update_node_test()
    print("Migrated converter, HTML pages, Service Worker, and Smart Search test")
