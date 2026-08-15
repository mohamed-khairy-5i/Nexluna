#!/usr/bin/env python3
"""Week 6 integration gate: explanation, embed contract, generation, and data systems."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def script_order(html, scripts):
    positions = [html.find(f'src="/assets/js/{name}"') for name in scripts]
    require(all(position >= 0 for position in positions), f"missing script in generated page: {scripts}")
    require(positions == sorted(positions), f"script order is invalid: {scripts}")


def main():
    # Generated pages must expose the deterministic explanation stack in order.
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    category = (ROOT / "converters" / "length.html").read_text(encoding="utf-8")
    pair = (ROOT / "convert" / "km-to-m.html").read_text(encoding="utf-8")
    script_order(home, ["units.generated.js", "explain.js", "webmcp.js", "converter.js"])
    script_order(category, ["units.generated.js", "explain.js", "webmcp.js", "converter.js"])
    script_order(pair, ["units.generated.js", "explain.js", "webmcp.js"])

    embed = (ROOT / "embed.html").read_text(encoding="utf-8")
    for element_id in ("embed-category", "embed-from", "embed-to", "embed-value", "embed-result", "embed-form"):
        require(f'id="{element_id}"' in embed, f"embed element missing: {element_id}")
    require("/assets/js/units.generated.js" in embed, "embed must load canonical units")
    require("/assets/js/webmcp.js" in embed, "embed must load WebMCP")
    require("/assets/js/embed.js" in embed, "embed must load embed controller")

    converter = (ROOT / "assets" / "js" / "converter.js").read_text(encoding="utf-8")
    require("explainBtn" in converter and "NexExplain.explain" in converter, "converter explanation control is not wired")
    require("nx-data-system" in converter and "KiB" in converter and "KB" in converter, "data system toggle is not wired")
    require("ic('spark')" in converter, "explanation button icon is missing")

    explain = (ROOT / "assets" / "js" / "explain.js").read_text(encoding="utf-8")
    require("deterministic-fallback" in explain and "optional-model-verified" in explain, "explanation fallback contract is incomplete")
    require("network_required: false" in explain, "explanation must declare no network requirement for baseline")

    sw = (ROOT / "sw.js").read_text(encoding="utf-8")
    for asset in ("/assets/js/explain.js", "/assets/js/embed.js", "/embed.html"):
        require(asset in sw, f"service worker missing Week 6 asset: {asset}")

    subprocess.run(["node", str(ROOT / "test_week6.js")], cwd=ROOT, check=True)
    print("PASS: Week 6 integration gate")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
