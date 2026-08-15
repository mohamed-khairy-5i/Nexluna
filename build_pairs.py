#!/usr/bin/env python3
"""Nexluna — generator for high-intent conversion-PAIR pages (Roadmap 1.1).

Each page targets a long-tail Arabic query like "كم كيلومتر في الميل" / "تحويل من كجم إلى رطل"
with: instant answer, a reference table of common values, exact math, FAQ JSON-LD,
and a deep link into the full category converter (state pre-filled).

Static-first, deterministic math (mirrors converter.js base factors exactly), zero API.
"""
import json
import os
from pathlib import Path
from build_pages import BASE, HEADER, FOOTER, ADSENSE, CSP_META, PAGES, DEV_PERSON_JSONLD

ROOT = Path(__file__).resolve().parent
OUT_DIR = "convert"
CANONICAL = json.loads((ROOT / "data" / "units.json").read_text(encoding="utf-8"))

# Deterministic factors come from the canonical source. This generator must not
# carry a second table that can drift from NexConvert.
FACT = {
    category: definition.get("base", {})
    for category, definition in CANONICAL.items()
    if definition.get("base")
}

# Unit labels are derived from canonical data so every generated page uses the same
# names and symbols as NexConvert/WebMCP. The old hand-maintained table is gone.
UNIT_LABELS = {}
for _category, _definition in CANONICAL.items():
    UNIT_LABELS[_category] = {}
    for _code, _label in _definition.get("units", []):
        _name = _label.rsplit(" (", 1)[0] if " (" in _label else _label
        UNIT_LABELS[_category][_code] = (_name, _code)


def unit_label(category, code):
    try:
        return UNIT_LABELS[category][code]
    except KeyError as exc:
        raise KeyError(f"Unit {code!r} is missing from canonical category {category!r}") from exc


MPG_US = 0.425143707430272
MPG_UK = 0.3540061899346471


def conv(cat, frm, to, v):
    if cat == "temperature":
        return temp(v, frm, to)
    if cat == "fuel":
        return fuel(v, frm, to)
    f = FACT[cat]
    return v * f[frm] / f[to]


def fuel_to_kml(v, unit):
    if unit == "kml":
        return v
    if unit == "l100":
        return 100 / v
    return v * (MPG_UK if unit == "mpgUK" else MPG_US)


def fuel(v, frm, to):
    if frm == to:
        return v
    km_l = fuel_to_kml(v, frm)
    if to == "kml":
        return km_l
    if to == "l100":
        return 100 / km_l
    return km_l / (MPG_UK if to == "mpgUK" else MPG_US)


def temp(v, frm, to):
    c = v if frm == "C" else (v - 32) * 5 / 9 if frm == "F" else v - 273.15
    return c if to == "C" else c * 9 / 5 + 32 if to == "F" else c + 273.15


def fmt(n):
    r = round(n, 6)
    if r == int(r):
        return f"{int(r):,}"
    return f"{r:,.6f}".rstrip("0").rstrip(".")


# --- High-intent pairs generated from a small, curated unit set per category ---
# Each unordered pair becomes two landing pages (A→B and B→A). This keeps the
# inventory broad enough for long-tail SEO without generating every low-intent
# permutation in the canonical source.
PAIR_UNITS = {
    "length": ["km", "m", "mi", "ft"],
    "weight": ["kg", "g", "lb", "oz"],
    "area": ["m2", "feddan", "acre", "ft2"],
    "volume": ["L", "mL", "gal", "cup"],
    "temperature": ["C", "F", "K"],
    "data": ["KB", "MB", "GB", "TB"],
    "speed": ["kmh", "mph", "ms", "knot"],
    "time": ["s", "min", "h", "day"],
    "pressure": ["pa", "bar", "atm", "psi"],
    "energy": ["j", "kj", "cal", "kwh"],
    "power": ["w", "kw", "hp", "btuh"],
    "angle": ["deg", "rad", "grad", "turn"],
    "fuel": ["kml", "l100", "mpg", "mpgUK"],
    "frequency": ["hz", "khz", "mhz", "ghz"],
}
PAIRS = []
for _category, _units in PAIR_UNITS.items():
    for _i, _from in enumerate(_units):
        for _to in _units[_i + 1:]:
            PAIRS.extend([(_category, _from, _to), (_category, _to, _from)])

CAT_AR = {
    "length": "الطول", "weight": "الوزن", "area": "المساحة", "volume": "الحجم والسعة",
    "temperature": "درجة الحرارة", "data": "البيانات", "speed": "السرعة", "time": "الوقت",
    "pressure": "الضغط", "energy": "الطاقة", "power": "القدرة", "angle": "الزوايا",
    "fuel": "استهلاك الوقود", "frequency": "التردد",
}


def slug(cat, frm, to):
    def s(k):
        return k.replace("/", "-").lower()
    return f"{s(frm)}-to-{s(to)}"


def table_rows(cat, frm, to):
    vals = [1, 2, 3, 5, 10, 20, 25, 50, 100, 500, 1000]
    if cat == "temperature":
        vals = [-40, -10, 0, 10, 20, 25, 30, 37, 50, 100]
    rows = []
    for v in vals:
        rows.append(f"        <tr><td>{fmt(v)} {unit_label(cat, frm)[1]}</td><td>{fmt(conv(cat, frm, to, v))} {unit_label(cat, to)[1]}</td></tr>")
    return "\n".join(rows)


def faq_pair(cat, frm, to):
    fa, fs = unit_label(cat, frm)
    ta, ts = unit_label(cat, to)
    one = fmt(conv(cat, frm, to, 1))
    items = [
        (f"كم {ta} في {fa} واحد؟", f"{fa} واحد ({fs}) يساوي {one} {ta} ({ts})."),
        (f"كيف أحوّل من {fa} إلى {ta}؟", f"اضرب القيمة بـ{fa} في {one} لتحصل على القيمة بـ{ta}، أو استخدم محوّل Nexluna للحصول على نتيجة فورية دقيقة."),
    ]
    if cat != "temperature":
        ten = fmt(conv(cat, frm, to, 10))
        items.append((f"كم يساوي 10 {fa} بـ{ta}؟", f"10 {fa} = {ten} {ta}."))
    return items


def faq_jsonld(items):
    ent = ",".join(
        '{ "@type": "Question", "name": "%s", "acceptedAnswer": { "@type": "Answer", "text": "%s" } }' % (q, a)
        for q, a in items
    )
    return '{ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [%s] }' % ent


def faq_html(items):
    return "\n".join(
        '        <details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (q, a)
        for q, a in items
    )


def page_html(cat, frm, to):
    fa, fs = unit_label(cat, frm)
    ta, ts = unit_label(cat, to)
    cat_ar = CAT_AR[cat]
    one = fmt(conv(cat, frm, to, 1))
    sl = slug(cat, frm, to)
    url = BASE + "/convert/" + sl + ".html"
    title = "تحويل من %s إلى %s (%s ← %s) — Nexluna" % (fa, ta, fs, ts)
    desc = "كم %s في %s؟ %s واحد = %s %s. جدول تحويل جاهز ومحوّل فوري دقيق من %s إلى %s على Nexluna." % (ta, fa, fa, one, ta, fa, ta)
    faq = faq_pair(cat, frm, to)
    deep = "/converters/%s.html?from=%s&to=%s&v=1" % (cat, frm, to)

    ads_loader = (
        '  <script>(function(){function load(){var s=document.createElement("script");'
        's.async=true;s.src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=' + ADSENSE + '";'
        's.crossOrigin="anonymous";document.head.appendChild(s);}'
        'if("requestIdleCallback"in window){requestIdleCallback(load,{timeout:3500});}else{setTimeout(load,2500);}'
        'var once=function(){load();["scroll","click","keydown","touchstart"].forEach(function(e){window.removeEventListener(e,once);});};'
        '["scroll","click","keydown","touchstart"].forEach(function(e){window.addEventListener(e,once,{passive:true,once:true});});})();</script>'
    )

    head = '<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n' \
        '  <meta charset="UTF-8">\n' \
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' \
        + CSP_META + '  <title>' + title + '</title>\n' \
        '  <meta name="description" content="' + desc + '">\n' \
        '  <meta name="keywords" content="تحويل ' + fa + ' إلى ' + ta + ', كم ' + ta + ' في ' + fa + ', محول ' + cat_ar + ', Nexluna">\n' \
        '  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">\n' \
        '  <meta name="theme-color" content="#0f9480">\n' \
        '  <meta name="author" content="Nexluna">\n' \
        '  <link rel="canonical" href="' + url + '">\n' \
        '  <link rel="alternate" hreflang="ar" href="' + url + '">\n' \
        '  <link rel="alternate" hreflang="x-default" href="' + url + '">\n' \
        '  <meta property="og:type" content="website">\n' \
        '  <meta property="og:site_name" content="Nexluna">\n' \
        '  <meta property="og:locale" content="ar_AR">\n' \
        '  <meta property="og:title" content="' + title + '">\n' \
        '  <meta property="og:description" content="' + desc + '">\n' \
        '  <meta property="og:url" content="' + url + '">\n' \
        '  <meta property="og:image" content="' + BASE + '/assets/img/og-image.png">\n' \
        '  <meta name="twitter:card" content="summary_large_image">\n' \
        '  <link rel="icon" href="/assets/img/favicon.ico" sizes="any">\n' \
        '  <link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg">\n' \
        '  <link rel="manifest" href="/manifest.webmanifest">\n' \
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/cairo-var.woff2" crossorigin>\n' \
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/tajawal-800.woff2" crossorigin>\n' \
        '  <link rel="stylesheet" href="/assets/css/fonts.css">\n' \
        '  <link rel="stylesheet" href="/assets/css/style.css">\n' \
        '  <script>(function(){try{var t=localStorage.getItem("nx-theme");if(t)document.documentElement.setAttribute("data-theme",t);}catch(e){}document.documentElement.classList.add("js-ready");})();</script>\n'

    bc_ld = '  <script type="application/ld+json">\n' \
        '  { "@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[' \
        '{ "@type":"ListItem","position":1,"name":"الرئيسية","item":"' + BASE + '/" },' \
        '{ "@type":"ListItem","position":2,"name":"تحويلات","item":"' + BASE + '/convert/" },' \
        '{ "@type":"ListItem","position":3,"name":"' + title + '","item":"' + url + '" }] }\n  </script>\n'
    faq_ld = '  <script type="application/ld+json">\n  ' + faq_jsonld(faq) + '\n  </script>\n'
    howto = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "طريقة تحويل %s إلى %s" % (fa, ta),
        "description": "خطوات تحويل %s إلى %s باستخدام Nexluna." % (fa, ta),
        "totalTime": "PT1M",
        "step": [
            {"@type": "HowToStep", "position": 1, "name": "أدخل القيمة", "text": "أدخل القيمة المراد تحويلها."},
            {"@type": "HowToStep", "position": 2, "name": "اختر الوحدات", "text": "اختر وحدة %s ووحدة %s." % (fa, ta)},
            {"@type": "HowToStep", "position": 3, "name": "راجع النتيجة", "text": "يعرض Nexluna النتيجة الدقيقة وجدول القيم الشائعة."},
        ],
    }
    howto_ld = '  <script type="application/ld+json">\n  ' + json.dumps(howto, ensure_ascii=False) + '\n  </script>\n'
    app_ld = '  <script type="application/ld+json">\n  ' + json.dumps({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Any",
        "inLanguage": "ar",
        "dateModified": "2026-08-15",
        "author": json.loads(DEV_PERSON_JSONLD),
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    }, ensure_ascii=False) + '\n  </script>\n'

    body = '</head>\n<body>\n' \
        '  <a class="skip-link" href="#main">تخطَّ إلى المحتوى الرئيسي</a>\n' + HEADER + '\n' \
        '  <main id="main">\n    <div class="container section">\n' \
        '      <nav class="breadcrumb" aria-label="مسار التنقل">\n' \
        '        <a href="/">الرئيسية</a> <span aria-hidden="true">›</span> ' \
        '<a href="/converters/' + cat + '.html">' + cat_ar + '</a> <span aria-hidden="true">›</span> ' \
        '<span>' + fa + ' إلى ' + ta + '</span>\n      </nav>\n' \
        '      <div class="section-head reveal" style="margin-bottom:var(--sp-5)">\n' \
        '        <span class="eyebrow"><span data-icon="' + cat + '"></span> تحويل ' + cat_ar + '</span>\n' \
        '        <h1>تحويل من ' + fa + ' إلى ' + ta + '</h1>\n' \
        '        <p class="lead">' + fa + ' واحد يساوي <strong>' + one + ' ' + ta + '</strong>. استخدم الجدول أدناه للقيم الشائعة، أو المحوّل الفوري لأي قيمة.</p>\n' \
        '      </div>\n' \
        '      <div class="pair-answer reveal" dir="ltr">\n' \
        '        <span class="pair-num">1 ' + fs + '</span>\n' \
        '        <span class="pair-eq">=</span>\n' \
        '        <strong class="pair-res">' + one + ' ' + ts + '</strong>\n' \
        '      </div>\n' \
        '      <div class="hero-cta reveal" style="margin:var(--sp-5) 0">\n' \
        '        <a href="' + deep + '" class="btn btn-primary"><span data-icon="bolt"></span> افتح المحوّل التفاعلي</a>\n' \
        '      </div>\n' \
        '      <section class="section-sm reveal">\n' \
        '        <div class="section-head"><span class="eyebrow"><span data-icon="grid"></span> جدول التحويل</span>' \
        '<h2>جدول تحويل ' + fa + ' إلى ' + ta + '</h2></div>\n' \
        '        <div class="table-wrap"><table class="conv-table"><thead><tr><th>' + fa + '</th><th>' + ta + '</th></tr></thead><tbody>\n' \
        + table_rows(cat, frm, to) + '\n        </tbody></table></div>\n      </section>\n' \
        '      <div class="ad-slot ad-inarticle reveal" role="complementary" aria-label="إعلان">\n' \
        '        <ins class="adsbygoogle" style="display:block" data-ad-client="' + ADSENSE + '" data-ad-slot="1234567891" data-ad-format="fluid" data-ad-layout="in-article" data-full-width-responsive="true"></ins>\n' \
        '        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n      </div>\n' \
        '      <section class="section-sm reveal">\n' \
        '        <div class="section-head"><span class="eyebrow"><span data-icon="help"></span> أسئلة شائعة</span><h2>أسئلة حول تحويل ' + fa + ' إلى ' + ta + '</h2></div>\n' \
        '        <div class="faq">\n' + faq_html(faq) + '\n        </div>\n      </section>\n' \
        '    </div>\n  </main>\n' + FOOTER + '\n' \
        '  <script src="/assets/js/icons.js" defer></script>\n' \
        '  <script src="/assets/js/units.generated.js" defer></script>\n' \
        '  <script src="/assets/js/explain.js" defer></script>\n' \
        '  <script src="/assets/js/webmcp.js" defer></script>\n' \
        '  <script src="/assets/js/main.js" defer></script>\n' \
        '</body>\n</html>\n'

    return head + bc_ld + app_ld + faq_ld + howto_ld + ads_loader + '\n' + body


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    expected = {slug(cat, frm, to) + ".html" for cat, frm, to in PAIRS}
    expected.add("index.html")
    for stale in Path(OUT_DIR).glob("*.html"):
        if stale.name not in expected:
            stale.unlink()
    written = []
    for cat, frm, to in PAIRS:
        sl = slug(cat, frm, to)
        path = os.path.join(OUT_DIR, sl + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(page_html(cat, frm, to))
        written.append(path)
        print("wrote", path)
    # index for /convert/
    write_index(written)
    print("done —", len(written), "pair pages")


def write_index(written):
    cards = []
    for cat, frm, to in PAIRS:
        fa = unit_label(cat, frm)[0]; ta = unit_label(cat, to)[0]; sl = slug(cat, frm, to)
        cards.append(
            '        <a class="card" href="/convert/' + sl + '.html">\n'
            '          <div class="card-icon"><span data-icon="' + cat + '"></span></div>\n'
            '          <h2 class="card-title">' + fa + ' إلى ' + ta + '</h2>\n'
            '          <p>جدول ومحوّل فوري للتحويل من ' + fa + ' إلى ' + ta + '.</p>\n'
            '          <span class="arrow" data-icon="arrow" aria-hidden="true"></span>\n        </a>'
        )
    url = BASE + "/convert/"
    item_list = []
    for position, (cat, frm, to) in enumerate(PAIRS, 1):
        fa = unit_label(cat, frm)[0]; ta = unit_label(cat, to)[0]; sl = slug(cat, frm, to)
        item_list.append({"@type": "ListItem", "position": position, "name": fa + " إلى " + ta, "url": BASE + "/convert/" + sl + ".html"})
    index_ld = '  <script type="application/ld+json">\n  ' + json.dumps({
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "أشهر تحويلات الوحدات",
        "numberOfItems": len(item_list),
        "itemListElement": item_list,
    }, ensure_ascii=False) + '\n  </script>\n'
    html = '<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n' \
        '  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' \
        + CSP_META + \
        '  <title>تحويلات الوحدات الشائعة — Nexluna</title>\n' \
        '  <meta name="description" content="روابط سريعة لأشهر عمليات تحويل الوحدات: كيلومتر إلى ميل، كجم إلى رطل، سيلسيوس إلى فهرنهايت، وغيرها — بجداول ومحوّل فوري.">\n' \
        '  <meta name="keywords" content="تحويل وحدات, محول وحدات عربي, جداول التحويل, Nexluna">\n' \
        '  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">\n' \
        '  <link rel="canonical" href="' + url + '">\n' \
        '  <meta property="og:type" content="website">\n' \
        '  <meta property="og:locale" content="ar_AR">\n' \
        '  <meta property="og:title" content="تحويلات الوحدات الشائعة — Nexluna">\n' \
        '  <meta property="og:description" content="روابط سريعة لأشهر عمليات تحويل الوحدات مع جداول ومحوّل فوري دقيق.">\n' \
        '  <meta property="og:url" content="' + url + '">\n' \
        '  <meta property="og:image" content="' + BASE + '/assets/img/og-image.png">\n' \
        '  <meta property="og:image:width" content="1200">\n' \
        '  <meta property="og:image:height" content="630">\n' \
        '  <meta name="twitter:card" content="summary_large_image">\n' \
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/cairo-var.woff2" crossorigin>\n' \
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/tajawal-800.woff2" crossorigin>\n' \
        '  <link rel="stylesheet" href="/assets/css/fonts.css">\n' \
        '  <link rel="stylesheet" href="/assets/css/style.css">\n' \
        '  <link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg">\n' \
        '  <script>(function(){try{var t=localStorage.getItem("nx-theme");if(t)document.documentElement.setAttribute("data-theme",t);}catch(e){}document.documentElement.classList.add("js-ready");})();</script>\n' \
        + index_ld + '</head>\n<body>\n  <a class="skip-link" href="#main">تخطَّ إلى المحتوى الرئيسي</a>\n' + HEADER + '\n' \
        '  <main id="main">\n    <div class="container section">\n' \
        '      <div class="section-head reveal"><span class="eyebrow"><span data-icon="grid"></span> تحويلات سريعة</span>' \
        '<h1>أشهر تحويلات الوحدات</h1><p class="lead">اختر التحويل الذي تريده مباشرة — كل صفحة فيها جدول قيم شائعة ومحوّل فوري دقيق.</p></div>\n' \
        '      <div class="grid grid-cards reveal">\n' + "\n".join(cards) + '\n      </div>\n' \
        '    </div>\n  </main>\n' + FOOTER + '\n' \
        '  <script src="/assets/js/icons.js" defer></script>\n  <script src="/assets/js/units.generated.js" defer></script>\n  <script src="/assets/js/webmcp.js" defer></script>\n  <script src="/assets/js/main.js" defer></script>\n' \
        '</body>\n</html>\n'
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", os.path.join(OUT_DIR, "index.html"))


if __name__ == "__main__":
    main()
