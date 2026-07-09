#!/usr/bin/env python3
"""Nexluna — generator for high-intent conversion-PAIR pages (Roadmap 1.1).

Each page targets a long-tail Arabic query like "كم كيلومتر في الميل" / "تحويل من كجم إلى رطل"
with: instant answer, a reference table of common values, exact math, FAQ JSON-LD,
and a deep link into the full category converter (state pre-filled).

Static-first, deterministic math (mirrors converter.js base factors exactly), zero API.
"""
import os
from build_pages import HEADER, FOOTER, ADSENSE, BASE

OUT_DIR = "convert"

# --- Deterministic factor mirror of converter.js DATA (base-unit multipliers) ---
FACT = {
    "length": {"km": 1000, "m": 1, "cm": 0.01, "mm": 0.001, "mi": 1609.344,
               "yd": 0.9144, "ft": 0.3048, "in": 0.0254, "nmi": 1852},
    "weight": {"t": 1000, "kg": 1, "g": 0.001, "mg": 0.000001, "lb": 0.45359237,
               "oz": 0.028349523, "st": 6.35029318, "ct": 0.0002},
    "data": {"bit": 0.125, "B": 1, "KB": 1000, "MB": 1000000, "GB": 1000000000,
             "TB": 1000000000000, "KiB": 1024, "MiB": 1048576, "GiB": 1073741824},
    "speed": {"kmh": 1, "ms": 3.6, "mph": 1.609344, "knot": 1.852, "fts": 1.09728},
    "volume": {"m3": 1000, "L": 1, "mL": 0.001, "gal": 3.785411784, "qt": 0.946352946,
               "pt": 0.473176473, "cup": 0.2365882365, "floz": 0.0295735296},
    "area": {"km2": 1000000, "m2": 1, "cm2": 0.0001, "ha": 10000, "acre": 4046.8564224,
             "ft2": 0.09290304, "in2": 0.00064516, "mi2": 2589988.11},
    "time": {"ms": 0.001, "s": 1, "min": 60, "h": 3600, "day": 86400, "week": 604800},
}

# Arabic + short labels for units used in pairs
UL = {
    "km": ("كيلومتر", "km"), "m": ("متر", "m"), "cm": ("سنتيمتر", "cm"), "mm": ("مليمتر", "mm"),
    "mi": ("ميل", "mi"), "yd": ("ياردة", "yd"), "ft": ("قدم", "ft"), "in": ("إنش", "in"),
    "kg": ("كيلوغرام", "kg"), "g": ("غرام", "g"), "lb": ("رطل", "lb"), "oz": ("أونصة", "oz"), "t": ("طن", "t"),
    "C": ("سيلسيوس", "°C"), "F": ("فهرنهايت", "°F"), "K": ("كلفن", "K"),
    "KB": ("كيلوبايت", "KB"), "MB": ("ميغابايت", "MB"), "GB": ("غيغابايت", "GB"), "TB": ("تيرابايت", "TB"),
    "kmh": ("كم/ساعة", "km/h"), "mph": ("ميل/ساعة", "mph"), "ms": ("متر/ثانية", "m/s"),
    "L": ("لتر", "L"), "mL": ("مليلتر", "mL"), "gal": ("جالون", "gal"), "cup": ("كوب", "cup"),
}


def conv(cat, frm, to, v):
    if cat == "temperature":
        return temp(v, frm, to)
    f = FACT[cat]
    return v * f[frm] / f[to]


def temp(v, frm, to):
    c = v if frm == "C" else (v - 32) * 5 / 9 if frm == "F" else v - 273.15
    return c if to == "C" else c * 9 / 5 + 32 if to == "F" else c + 273.15


def fmt(n):
    r = round(n, 6)
    if r == int(r):
        return f"{int(r):,}"
    return f"{r:,.6f}".rstrip("0").rstrip(".")


# --- The high-intent pairs to generate (category, from, to) ---
# Chosen for real Arabic search demand around unit conversions.
PAIRS = [
    ("length", "km", "mi"), ("length", "mi", "km"),
    ("length", "cm", "in"), ("length", "in", "cm"),
    ("length", "ft", "m"),  ("length", "m", "ft"),
    ("length", "km", "m"),  ("length", "m", "km"),
    ("weight", "kg", "lb"), ("weight", "lb", "kg"),
    ("weight", "g", "oz"),  ("weight", "oz", "g"),
    ("weight", "t", "kg"),
    ("temperature", "C", "F"), ("temperature", "F", "C"),
    ("temperature", "C", "K"),
    ("data", "GB", "MB"), ("data", "MB", "KB"), ("data", "TB", "GB"),
    ("speed", "kmh", "mph"), ("speed", "mph", "kmh"), ("speed", "ms", "kmh"),
    ("volume", "L", "gal"), ("volume", "gal", "L"), ("volume", "cup", "mL"),
]

CAT_AR = {"length": "الطول", "weight": "الوزن", "temperature": "درجة الحرارة",
          "data": "البيانات", "speed": "السرعة", "volume": "الحجم"}


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
        rows.append(f"        <tr><td>{fmt(v)} {UL[frm][1]}</td><td>{fmt(conv(cat, frm, to, v))} {UL[to][1]}</td></tr>")
    return "\n".join(rows)


def faq_pair(cat, frm, to):
    fa, fs = UL[frm]
    ta, ts = UL[to]
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
    fa, fs = UL[frm]
    ta, ts = UL[to]
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
        '  <title>' + title + '</title>\n' \
        '  <meta name="description" content="' + desc + '">\n' \
        '  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">\n' \
        '  <meta name="theme-color" content="#0f9488">\n' \
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
        '      <div class="ad-slot ad-inarticle reveal" aria-hidden="true">\n' \
        '        <ins class="adsbygoogle" style="display:block" data-ad-client="' + ADSENSE + '" data-ad-slot="1234567891" data-ad-format="fluid" data-ad-layout="in-article" data-full-width-responsive="true"></ins>\n' \
        '        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>\n      </div>\n' \
        '      <section class="section-sm reveal">\n' \
        '        <div class="section-head"><span class="eyebrow"><span data-icon="help"></span> أسئلة شائعة</span><h2>أسئلة حول تحويل ' + fa + ' إلى ' + ta + '</h2></div>\n' \
        '        <div class="faq">\n' + faq_html(faq) + '\n        </div>\n      </section>\n' \
        '    </div>\n  </main>\n' + FOOTER + '\n' \
        '  <script src="/assets/js/icons.js" defer></script>\n' \
        '  <script src="/assets/js/main.js" defer></script>\n' \
        '</body>\n</html>\n'

    return head + bc_ld + faq_ld + ads_loader + '\n' + body


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
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
        fa = UL[frm][0]; ta = UL[to][0]; sl = slug(cat, frm, to)
        cards.append(
            '        <a class="card" href="/convert/' + sl + '.html">\n'
            '          <div class="card-icon"><span data-icon="' + cat + '"></span></div>\n'
            '          <h3>' + fa + ' إلى ' + ta + '</h3>\n'
            '          <p>جدول ومحوّل فوري للتحويل من ' + fa + ' إلى ' + ta + '.</p>\n'
            '          <span class="arrow" data-icon="arrow" aria-hidden="true"></span>\n        </a>'
        )
    url = BASE + "/convert/"
    html = '<!DOCTYPE html>\n<html lang="ar" dir="rtl">\n<head>\n' \
        '  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n' \
        '  <title>تحويلات الوحدات الشائعة — Nexluna</title>\n' \
        '  <meta name="description" content="روابط سريعة لأشهر عمليات تحويل الوحدات: كيلومتر إلى ميل، كجم إلى رطل، سيلسيوس إلى فهرنهايت، وغيرها — بجداول ومحوّل فوري.">\n' \
        '  <link rel="canonical" href="' + url + '">\n' \
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/cairo-var.woff2" crossorigin>\n' \
        '  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/tajawal-800.woff2" crossorigin>\n' \
        '  <link rel="stylesheet" href="/assets/css/fonts.css">\n' \
        '  <link rel="stylesheet" href="/assets/css/style.css">\n' \
        '  <link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg">\n' \
        '  <script>(function(){try{var t=localStorage.getItem("nx-theme");if(t)document.documentElement.setAttribute("data-theme",t);}catch(e){}document.documentElement.classList.add("js-ready");})();</script>\n' \
        '</head>\n<body>\n  <a class="skip-link" href="#main">تخطَّ إلى المحتوى الرئيسي</a>\n' + HEADER + '\n' \
        '  <main id="main">\n    <div class="container section">\n' \
        '      <div class="section-head reveal"><span class="eyebrow"><span data-icon="grid"></span> تحويلات سريعة</span>' \
        '<h1>أشهر تحويلات الوحدات</h1><p class="lead">اختر التحويل الذي تريده مباشرة — كل صفحة فيها جدول قيم شائعة ومحوّل فوري دقيق.</p></div>\n' \
        '      <div class="cards-grid reveal">\n' + "\n".join(cards) + '\n      </div>\n' \
        '    </div>\n  </main>\n' + FOOTER + '\n' \
        '  <script src="/assets/js/icons.js" defer></script>\n  <script src="/assets/js/main.js" defer></script>\n' \
        '</body>\n</html>\n'
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", os.path.join(OUT_DIR, "index.html"))


if __name__ == "__main__":
    main()
