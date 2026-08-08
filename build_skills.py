#!/usr/bin/env python3
"""Generate the Agent Skills discovery index (Cloudflare Agent Skills Discovery
RFC v0.2.0):  /.well-known/agent-skills/index.json

Each skill entry has: name, type, description, url, and a sha256 digest of the
skill document it points to. We publish one skill — "unit-conversion" — backed
by a SKILL.md file that documents the WebMCP `convert_units` tool.
"""
import os
import json
import hashlib
from build_pages import BASE, ORDER, PAGES, DEV

HERE = os.path.dirname(__file__)
WK = os.path.join(HERE, ".well-known", "agent-skills")


def unit_conversion_skill_md():
    L = []
    L.append("# Skill: unit-conversion")
    L.append("")
    L.append("تحويل قيمة رقمية بين وحدتين قياس ضمن نفس الفئة، بحساب حتمي دقيق يجري "
             "بالكامل داخل المتصفح. Convert a numeric value between two units of the "
             "same measurement category — deterministic, client-side, no server.")
    L.append("")
    L.append("## كيفية الاستخدام (WebMCP)")
    L.append("")
    L.append("الأداة مُسجّلة في كل صفحة عبر `navigator.modelContext.provideContext()`.")
    L.append("")
    L.append("### الأداة: `convert_units`")
    L.append("")
    L.append("المدخلات (inputSchema):")
    L.append("")
    L.append("```json")
    L.append(json.dumps({
        "category": "string (enum)",
        "from": "string (unit code)",
        "to": "string (unit code)",
        "value": "number"
    }, ensure_ascii=False, indent=2))
    L.append("```")
    L.append("")
    L.append("### الأداة: `list_units`")
    L.append("")
    L.append("تُعيد رموز الوحدات المتاحة لفئة (أو كل الفئات). Returns unit codes for a "
             "category (or all categories).")
    L.append("")
    L.append("## الفئات المدعومة (categories)")
    L.append("")
    for c in ORDER:
        name = PAGES[c].get("name", c)
        L.append("- `%s` — %s: %s/converters/%s.html" % (c, name, BASE, c))
    L.append("")
    L.append("## موارد ذات صلة")
    L.append("")
    L.append("- Markdown pages: %s/md/index.md" % BASE)
    L.append("- llms.txt: %s/llms.txt" % BASE)
    L.append("- API catalog: %s/.well-known/api-catalog" % BASE)
    L.append("")
    L.append("Developer: %s (%s) — %s" % (DEV["name_en"], DEV["role_en"], DEV["portfolio"]))
    L.append("")
    return "\n".join(L)


def sha256_hex(text_bytes):
    return hashlib.sha256(text_bytes).hexdigest()


def main():
    os.makedirs(WK, exist_ok=True)

    # 1) Write the skill document and hash it.
    skill_md = unit_conversion_skill_md().encode("utf-8")
    skill_path = os.path.join(WK, "unit-conversion.md")
    with open(skill_path, "wb") as f:
        f.write(skill_md)

    # 2) Build the index referencing the skill doc + its sha256.
    index = {
        "$schema": "https://raw.githubusercontent.com/cloudflare/agent-skills-discovery-rfc/main/schemas/v0.2.0/index.json",
        "version": "0.2.0",
        "name": "Nexluna",
        "description": "محوّل وحدات عربي دقيق — مهارات تحويل الوحدات للوكلاء. "
                       "Arabic-first unit converter — unit-conversion skills for AI agents.",
        "skills": [
            {
                "name": "unit-conversion",
                "type": "webmcp",
                "description": "تحويل قيمة بين وحدتين ضمن 14 فئة (طول، وزن، مساحة، حجم، "
                               "حرارة، بيانات، سرعة، وقت، ضغط، طاقة، قدرة، زوايا، وقود، تردد) "
                               "عبر أداة WebMCP باسم convert_units. Convert values across 14 "
                               "measurement categories via the WebMCP tool convert_units.",
                "url": BASE + "/.well-known/agent-skills/unit-conversion.md",
                "sha256": sha256_hex(skill_md)
            }
        ]
    }
    index_path = os.path.join(WK, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print("wrote .well-known/agent-skills/index.json + unit-conversion.md")


if __name__ == "__main__":
    main()
