#!/usr/bin/env python3
"""Generate Markdown-for-Agents (.md) versions of the site's key pages.

Cloudflare "Agent-Ready" Markdown Negotiation: when an agent requests a page
with `Accept: text/markdown`, Netlify redirects (200 rewrite) to the matching
`.md` file which is served with `Content-Type: text/markdown` (see netlify.toml).

All content derives from the single source of truth (build_pages / build_pairs /
converter tables) so the markdown can never drift out of sync with the HTML.
"""
import os
from build_pages import BASE, PAGES, ORDER, DEV

HERE = os.path.dirname(__file__)
MD_DIR = os.path.join(HERE, "md")

# Base-unit factor tables + labels (mirror of assets/js/converter.js DATA).
UNITS = {
    "length": [("km", "كيلومتر"), ("m", "متر"), ("cm", "سنتيمتر"), ("mm", "مليمتر"),
               ("mi", "ميل"), ("yd", "ياردة"), ("ft", "قدم"), ("in", "إنش"), ("nmi", "ميل بحري")],
    "weight": [("t", "طن"), ("kg", "كيلوغرام"), ("g", "غرام"), ("mg", "مليغرام"),
               ("lb", "رطل"), ("oz", "أونصة"), ("st", "ستون"), ("ct", "قيراط")],
    "area": [("km2", "كم مربع"), ("m2", "متر مربع"), ("cm2", "سم مربع"), ("ha", "هكتار"),
             ("acre", "فدان"), ("ft2", "قدم مربع"), ("in2", "إنش مربع"), ("mi2", "ميل مربع")],
    "volume": [("m3", "متر مكعب"), ("L", "لتر"), ("mL", "مليلتر"), ("gal", "جالون"),
               ("qt", "كوارت"), ("pt", "باينت"), ("cup", "كوب"), ("floz", "أونصة سائلة"),
               ("tbsp", "ملعقة كبيرة"), ("tsp", "ملعقة صغيرة")],
    "temperature": [("C", "سيلسيوس"), ("F", "فهرنهايت"), ("K", "كلفن")],
    "data": [("bit", "بت"), ("B", "بايت"), ("KB", "كيلوبايت"), ("MB", "ميغابايت"),
             ("GB", "غيغابايت"), ("TB", "تيرابايت"), ("KiB", "كيبي بايت"),
             ("MiB", "ميبي بايت"), ("GiB", "غيبي بايت")],
    "speed": [("kmh", "كم/ساعة"), ("ms", "متر/ثانية"), ("mph", "ميل/ساعة"),
              ("knot", "عقدة"), ("fts", "قدم/ثانية")],
    "time": [("ms", "مليثانية"), ("s", "ثانية"), ("min", "دقيقة"), ("h", "ساعة"),
             ("day", "يوم"), ("week", "أسبوع"), ("month", "شهر"), ("year", "سنة")],
    "pressure": [("pa", "باسكال"), ("kpa", "كيلوباسكال"), ("bar", "بار"), ("atm", "جو"),
                 ("psi", "psi"), ("mmhg", "مم زئبق"), ("torr", "تور")],
    "energy": [("j", "جول"), ("kj", "كيلوجول"), ("cal", "سعرة"), ("kcal", "كيلوسعرة"),
               ("wh", "واط·ساعة"), ("kwh", "كيلوواط·ساعة"), ("btu", "BTU"), ("ev", "إلكترون فولت")],
    "power": [("w", "واط"), ("kw", "كيلوواط"), ("mw", "ميغاواط"), ("hp", "حصان"), ("btuh", "BTU/ساعة")],
    "angle": [("deg", "درجة"), ("rad", "راديان"), ("grad", "غراد"),
              ("arcmin", "دقيقة قوسية"), ("arcsec", "ثانية قوسية"), ("turn", "دورة")],
    "fuel": [("kml", "كم/لتر"), ("l100", "لتر/100كم"), ("mpg", "ميل/جالون")],
    "frequency": [("hz", "هيرتز"), ("khz", "كيلوهيرتز"), ("mhz", "ميغاهيرتز"),
                  ("ghz", "غيغاهيرتز"), ("rpm", "دورة/دقيقة")],
}


def converter_md(cat):
    p = PAGES[cat]
    L = []
    L.append("# %s" % p["title"])
    L.append("")
    L.append("> %s" % p["desc"])
    L.append("")
    L.append(p["intro"])
    L.append("")
    L.append("**الرابط:** %s/converters/%s.html" % (BASE, cat))
    L.append("")
    units = UNITS.get(cat, [])
    if units:
        L.append("## الوحدات المدعومة")
        L.append("")
        L.append("| الرمز (code) | الوحدة |")
        L.append("| --- | --- |")
        for code, label in units:
            L.append("| `%s` | %s |" % (code, label))
        L.append("")
    faq = p.get("faq", [])
    if faq:
        L.append("## أسئلة شائعة")
        L.append("")
        for q, a in faq:
            L.append("### %s" % q)
            L.append("")
            L.append(a)
            L.append("")
    L.append("## للوكلاء (For AI agents)")
    L.append("")
    L.append("- التحويل متاح برمجياً عبر أداة WebMCP باسم `convert_units` "
             "(الفئة: `%s`). Use the WebMCP tool `convert_units` with category `%s`." % (cat, cat))
    L.append("- الحساب حتمي ويجري بالكامل داخل المتصفح (بدون خادم).")
    L.append("")
    return "\n".join(L)


def index_md():
    L = []
    L.append("# Nexluna — محوّل الوحدات العربي")
    L.append("")
    L.append("> محوّل وحدات عربي مجاني، سريع ودقيق — 14 فئة تحويل. "
             "A free, fast, accurate Arabic-first unit converter (14 categories).")
    L.append("")
    L.append("Nexluna موقع ثابت يعمل بالكامل داخل المتصفح — لا خوادم ولا تتبّع لمدخلات المستخدم.")
    L.append("")
    L.append("## المحوّلات")
    L.append("")
    for c in ORDER:
        name = PAGES[c].get("name", c)
        desc = PAGES[c].get("desc", name).split(".")[0].strip()
        L.append("- [%s](%s/md/converters/%s.md): %s" % (name, BASE, c, desc))
    L.append("")
    L.append("## موارد للوكلاء")
    L.append("")
    L.append("- llms.txt: %s/llms.txt" % BASE)
    L.append("- API catalog: %s/.well-known/api-catalog" % BASE)
    L.append("- Agent Skills: %s/.well-known/agent-skills/index.json" % BASE)
    L.append("- WebMCP: أداة `convert_units` مُسجّلة في كل صفحة عبر navigator.modelContext.")
    L.append("- Sitemap: %s/sitemap.xml" % BASE)
    L.append("")
    L.append("## Metadata")
    L.append("")
    L.append("- Language: Arabic (ar), RTL")
    L.append("- License: MIT (code)")
    L.append("- Developer: %s (%s) — %s" % (DEV["name_en"], DEV["role_en"], DEV["portfolio"]))
    L.append("")
    return "\n".join(L)


def main():
    os.makedirs(os.path.join(MD_DIR, "converters"), exist_ok=True)
    n = 0
    with open(os.path.join(MD_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_md())
    n += 1
    for cat in ORDER:
        with open(os.path.join(MD_DIR, "converters", cat + ".md"), "w", encoding="utf-8") as f:
            f.write(converter_md(cat))
        n += 1
    print("wrote %d markdown files under md/" % n)


if __name__ == "__main__":
    main()
