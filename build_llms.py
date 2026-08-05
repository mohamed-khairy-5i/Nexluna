#!/usr/bin/env python3
"""Generate AI-agent discovery artifacts:
  - llms.txt            (llmstxt.org convention — a curated map of the site for LLMs)
  - .well-known/api-catalog  (RFC 9727 linkset — points agents to the site's tools)
All content is derived from the single source of truth in build_pages / build_pairs
so it can never drift out of sync with the actual pages.
"""
import os
import json
from build_pages import BASE, ORDER, PAGES, DEV
from build_pairs import PAIRS, slug

HERE = os.path.dirname(__file__)


def build_llms():
    lines = []
    lines.append("# Nexluna")
    lines.append("")
    lines.append("> محوّل وحدات عربي مجاني، سريع ودقيق — 14 فئة تحويل (طول، وزن، حرارة، "
                 "بيانات، سرعة، وقت، ضغط، طاقة، قدرة، زوايا، وقود، تردد، مساحة، حجم). "
                 "A free, fast, accurate Arabic-first unit converter covering 14 categories.")
    lines.append("")
    lines.append("Nexluna is a static, privacy-friendly website. All conversions run "
                 "client-side in the browser — there is no tracking of user input. "
                 "Content is in Arabic (RTL).")
    lines.append("")

    # Converters
    lines.append("## المحوّلات (Converters)")
    lines.append("")
    for c in ORDER:
        name = PAGES[c].get("name", c)
        desc = PAGES[c].get("desc", name).split(".")[0].strip()
        lines.append("- [%s](%s/converters/%s.html): %s" % (name, BASE, c, desc))
    lines.append("")

    # Popular conversion pairs
    lines.append("## تحويلات شائعة (Popular conversions)")
    lines.append("")
    for cat, frm, to in PAIRS:
        s = slug(cat, frm, to)
        lines.append("- [%s → %s](%s/convert/%s.html)" % (frm, to, BASE, s))
    lines.append("")

    # Key pages
    lines.append("## صفحات مهمة (Key pages)")
    lines.append("")
    lines.append("- [كل المحوّلات](%s/convert/): فهرس صفحات التحويل" % BASE)
    lines.append("- [المدوّنة](%s/blog/): أدلّة ومقالات عن وحدات القياس" % BASE)
    lines.append("- [من نحن](%s/about.html)" % BASE)
    lines.append("- [اتصل بنا](%s/contact.html)" % BASE)
    lines.append("- [سياسة الخصوصية](%s/privacy.html)" % BASE)
    lines.append("")

    lines.append("## Metadata")
    lines.append("")
    lines.append("- Language: Arabic (ar), RTL")
    lines.append("- License: content © Nexluna; open-source under MIT")
    lines.append("- Developer: %s (%s) — %s" % (DEV["name_en"], DEV["role_en"], DEV["portfolio"]))
    lines.append("- Sitemap: %s/sitemap.xml" % BASE)
    lines.append("")

    out = "\n".join(lines)
    with open(os.path.join(HERE, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote llms.txt (%d bytes)" % len(out.encode("utf-8")))


def build_api_catalog():
    """RFC 9727 API catalog. Nexluna has no REST API, but we advertise the
    machine-readable resources agents can actually use (sitemap, llms.txt)."""
    linkset = {
        "linkset": [
            {
                "anchor": BASE + "/",
                "service-doc": [{"href": BASE + "/llms.txt", "type": "text/plain"}],
                "describedby": [{"href": BASE + "/sitemap.xml", "type": "application/xml"}],
            }
        ]
    }
    wk = os.path.join(HERE, ".well-known")
    os.makedirs(wk, exist_ok=True)
    path = os.path.join(wk, "api-catalog")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(linkset, f, ensure_ascii=False, indent=2)
    print("wrote .well-known/api-catalog")


if __name__ == "__main__":
    build_llms()
    build_api_catalog()
