#!/usr/bin/env python3
"""Week 8 hardening and release gate for generated Nexluna pages."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CSP_MARKERS = ("default-src 'self'", "object-src 'none'", "base-uri 'self'")


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    generators = [
        ROOT / "build_pages.py",
        ROOT / "build_home.py",
        ROOT / "build_pairs.py",
        ROOT / "build_content.py",
        ROOT / "build_blog.py",
    ]
    for generator in generators:
        source = generator.read_text(encoding="utf-8")
        require("CSP_META" in source or "Content-Security-Policy" in source, f"CSP is not wired in {generator.name}")

    outputs = [
        ROOT / "index.html",
        ROOT / "converters" / "length.html",
        ROOT / "convert" / "km-to-m.html",
        ROOT / "convert" / "index.html",
        ROOT / "about.html",
        ROOT / "privacy.html",
        ROOT / "contact.html",
        ROOT / "404.html",
        ROOT / "offline.html",
    ]
    blog_pages = sorted((ROOT / "blog").glob("*.html")) if (ROOT / "blog").exists() else []
    outputs.extend(blog_pages[:1])
    for output in outputs:
        require(output.exists(), f"missing generated hardening target: {output.relative_to(ROOT)}")
        html = output.read_text(encoding="utf-8")
        require("Content-Security-Policy" in html, f"CSP missing from {output.relative_to(ROOT)}")
        require(all(marker in html for marker in CSP_MARKERS), f"CSP baseline incomplete in {output.relative_to(ROOT)}")

    main = (ROOT / "assets" / "js" / "main.js").read_text(encoding="utf-8")
    require("unhandledrejection" in main and "data-error-boundary" in main, "error boundary hooks are missing")
    require("NexlunaErrorBoundary" in main, "error boundary API is missing")
    css = (ROOT / "assets" / "css" / "style.css").read_text(encoding="utf-8")
    require(".client-error-banner" in css, "error boundary banner style is missing")

    embed = (ROOT / "embed.html").read_text(encoding="utf-8")
    require("frame-ancestors *" in embed, "embed must remain frameable")
    headers = (ROOT / "_headers").read_text(encoding="utf-8")
    require("Content-Security-Policy:" in headers and "X-Content-Type-Options: nosniff" in headers, "deployment security headers are incomplete")
    require("/embed.html" in headers and "frame-ancestors *" in headers, "embed header override is missing")

    subprocess.run(["node", "--check", "assets/js/main.js"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "-m", "py_compile", "build_pages.py", "build_home.py", "build_pairs.py", "build_content.py", "build_blog.py"], cwd=ROOT, check=True)
    print(f"PASS — Week 8 hardening gate ({len(outputs)} generated pages checked)")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, subprocess.CalledProcessError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
