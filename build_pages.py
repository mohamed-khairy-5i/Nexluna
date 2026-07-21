#!/usr/bin/env python3
"""Static page generator for Nexluna converter pages.
Generates /converters/*.html for all 14 categories with the premium design.
Also exposes shared HEADER/FOOTER/BASE for build_content.py and build_blog.py."""
import os

BASE = "https://nexluna.netlify.app"
ADSENSE = "ca-pub-9822291009441043"

# ---- Shared navigation used across every page (modern data-icon icons) ----
HEADER = '''  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="/" aria-label="Nexluna — الصفحة الرئيسية">
        <img class="brand-logo" src="/assets/img/logo.svg" width="36" height="36" alt="">
        <span>Nexluna</span>
      </a>
      <nav class="nav-links" aria-label="التنقل الرئيسي">
        <a href="/">الرئيسية</a>
        <a href="/converters/length.html">الطول</a>
        <a href="/converters/weight.html">الوزن</a>
        <a href="/converters/temperature.html">الحرارة</a>
        <a href="/converters/data.html">البيانات</a>
        <a href="/blog/">المدونة</a>
        <a href="/about.html">عن الموقع</a>
      </nav>
      <div class="nav-actions">
        <button class="icon-btn" data-theme-toggle type="button" aria-label="تبديل الوضع الليلي"><span data-icon="moon"></span></button>
        <button class="icon-btn nav-toggle" type="button" aria-label="فتح القائمة" aria-expanded="false"><span data-icon="menu"></span></button>
      </div>
    </div>
  </header>'''

FOOTER = '''  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a class="brand" href="/" style="margin-bottom:var(--sp-3)">
            <img class="brand-logo" src="/assets/img/logo.svg" width="36" height="36" alt="">
            <span>Nexluna</span>
          </a>
          <p style="color:var(--text-muted);font-size:var(--step--1);max-width:38ch">منصّة عربية فخمة لتحويل وحدات القياس بدقّة وسرعة — تعمل على كل الأجهزة وبدون إنترنت.</p>
          <div class="footer-badges" style="display:flex;gap:var(--sp-2);margin-top:var(--sp-3);flex-wrap:wrap">
            <span class="chip"><span data-icon="offline"></span> يعمل دون إنترنت</span>
            <span class="chip"><span data-icon="shield"></span> بدون تتبّع</span>
          </div>
        </div>
        <div>
          <h2 class="footer-heading">المحولات</h2>
          <a href="/converters/length.html">الطول</a>
          <a href="/converters/weight.html">الوزن</a>
          <a href="/converters/area.html">المساحة</a>
          <a href="/converters/temperature.html">درجة الحرارة</a>
          <a href="/converters/volume.html">الحجم والسعة</a>
          <a href="/converters/data.html">البيانات الرقمية</a>
        </div>
        <div>
          <h2 class="footer-heading">المزيد</h2>
          <a href="/converters/speed.html">السرعة</a>
          <a href="/converters/time.html">الوقت</a>
          <a href="/converters/pressure.html">الضغط</a>
          <a href="/converters/energy.html">الطاقة</a>
          <a href="/converters/power.html">القدرة</a>
          <a href="/converters/fuel.html">استهلاك الوقود</a>
        </div>
        <div>
          <h2 class="footer-heading">روابط</h2>
          <a href="/convert/">تحويلات سريعة</a>
          <a href="/blog/">المدونة</a>
          <a href="/about.html">عن الموقع</a>
          <a href="/privacy.html">سياسة الخصوصية</a>
          <a href="/contact.html">اتصل بنا</a>
        </div>
      </div>
      <div class="footer-bottom">© <span data-year>2025</span> Nexluna — جميع الحقوق محفوظة. صُنع بإتقان للمستخدم العربي.</div>
    </div>
  </footer>'''

# ---- All 14 converter categories with SEO copy + FAQ ----
PAGES = {
    "length": {"name": "الطول", "icon": "length",
        "title": "محول وحدات الطول | متر، كيلومتر، ميل، قدم — Nexluna",
        "desc": "حوّل وحدات الطول والمسافة بدقة: متر، كيلومتر، سنتيمتر، مليمتر، ميل، ياردة، قدم، وإنش. أداة مجانية وسريعة من Nexluna.",
        "intro": "استخدم محوّل الطول لتحويل المسافات بين النظامين المتري والإمبراطوري بدقة فورية. أدخل القيمة واختر الوحدتين لتظهر النتيجة مباشرة.",
        "faq": [("كم سنتيمتر في المتر؟", "المتر الواحد يساوي 100 سنتيمتر و1000 مليمتر."),
                ("كم متر في الميل؟", "الميل الواحد يساوي 1609.344 متر أي نحو 1.60934 كيلومتر."),
                ("كيف أحوّل من قدم إلى متر؟", "اضرب عدد الأقدام في 0.3048 لتحصل على القيمة بالمتر.")]},
    "weight": {"name": "الوزن", "icon": "weight",
        "title": "محول وحدات الوزن | كيلوغرام، غرام، رطل، أونصة — Nexluna",
        "desc": "حوّل وحدات الوزن والكتلة بدقة: طن، كيلوغرام، غرام، مليغرام، رطل، وأونصة. أداة مجانية وسريعة من Nexluna.",
        "intro": "حوّل بين وحدات الوزن المترية والإمبراطورية بسهولة. مثالي للطبخ والشحن والتمارين والاستخدامات اليومية.",
        "faq": [("كم غرام في الكيلوغرام؟", "الكيلوغرام الواحد يساوي 1000 غرام."),
                ("كم رطل في الكيلوغرام؟", "الكيلوغرام الواحد يساوي تقريبًا 2.20462 رطل."),
                ("كم أونصة في الرطل؟", "الرطل الواحد يساوي 16 أونصة.")]},
    "area": {"name": "المساحة", "icon": "area",
        "title": "محول وحدات المساحة | متر مربع، هكتار، فدان — Nexluna",
        "desc": "حوّل وحدات المساحة بدقة: متر مربع، كيلومتر مربع، هكتار، فدان، قدم مربع، وإنش مربع. أداة مجانية من Nexluna.",
        "intro": "احسب مساحات الأراضي والعقارات بسهولة بالتحويل بين المتر المربع والهكتار والفدان والوحدات الإمبراطورية.",
        "faq": [("كم متر مربع في الهكتار؟", "الهكتار الواحد يساوي 10,000 متر مربع."),
                ("كم فدان في الهكتار؟", "الهكتار الواحد يساوي نحو 2.47105 فدان.")]},
    "volume": {"name": "الحجم والسعة", "icon": "volume",
        "title": "محول الحجم والسعة | لتر، متر مكعب، جالون، كوب — Nexluna",
        "desc": "حوّل وحدات الحجم والسعة بدقة: متر مكعب، لتر، مليلتر، جالون، كوارت، كوب، وأونصة سائلة. أداة مجانية من Nexluna.",
        "intro": "مثالي للطبخ والوصفات: حوّل بين اللتر والمليلتر والكوب والجالون والوحدات المكعبة بدقة فورية.",
        "faq": [("كم مليلتر في اللتر؟", "اللتر الواحد يساوي 1000 مليلتر."),
                ("كم لتر في الجالون الأمريكي؟", "الجالون الأمريكي يساوي نحو 3.78541 لتر.")]},
    "temperature": {"name": "درجة الحرارة", "icon": "temperature",
        "title": "محول درجة الحرارة | سيلسيوس، فهرنهايت، كلفن — Nexluna",
        "desc": "حوّل درجات الحرارة بدقة بين سيلسيوس (°C)، فهرنهايت (°F)، وكلفن (K). أداة مجانية وسريعة من Nexluna.",
        "intro": "حوّل درجات الحرارة فورًا بين سيلسيوس وفهرنهايت وكلفن، مع عرض الصيغ الحسابية للتحويل.",
        "faq": [("كيف أحوّل من سيلسيوس إلى فهرنهايت؟", "استخدم الصيغة: °F = (°C × 9/5) + 32."),
                ("ما درجة تجمّد الماء؟", "تجمّد الماء يحدث عند 0°C أي 32°F أو 273.15K.")]},
    "data": {"name": "البيانات الرقمية", "icon": "data",
        "title": "محول وحدات البيانات | بايت، ميغابايت، غيغابايت — Nexluna",
        "desc": "حوّل وحدات تخزين البيانات بدقة: بت، بايت، كيلوبايت، ميغابايت، غيغابايت، تيرابايت، والوحدات الثنائية (KiB, MiB, GiB). أداة مجانية من Nexluna.",
        "intro": "حوّل بين وحدات تخزين البيانات العشرية (KB, MB, GB) والثنائية (KiB, MiB, GiB) بدقة، مفيد للمطوّرين ومحبّي التقنية.",
        "faq": [("كم بايت في الكيلوبايت؟", "الكيلوبايت العشري = 1000 بايت، أما الكيبي بايت (KiB) = 1024 بايت."),
                ("ما الفرق بين GB و GiB؟", "الغيغابايت (GB) = مليار بايت، بينما الغيبي بايت (GiB) = 1,073,741,824 بايت.")]},
    "speed": {"name": "السرعة", "icon": "speed",
        "title": "محول وحدات السرعة | كم/ساعة، م/ث، ميل/ساعة، عقدة — Nexluna",
        "desc": "حوّل وحدات السرعة بدقة: كيلومتر/ساعة، متر/ثانية، ميل/ساعة، عقدة، وقدم/ثانية. أداة مجانية وسريعة من Nexluna.",
        "intro": "حوّل بين وحدات السرعة المختلفة فورًا — مفيد للسفر والرياضة والملاحة البحرية والجوية.",
        "faq": [("كم م/ث تساوي كم/ساعة؟", "1 متر/ثانية = 3.6 كيلومتر/ساعة."),
                ("كم كم/ساعة تساوي العقدة؟", "العقدة الواحدة = 1.852 كيلومتر/ساعة.")]},
    "time": {"name": "الوقت", "icon": "time",
        "title": "محول وحدات الوقت | ثانية، دقيقة، ساعة، يوم، سنة — Nexluna",
        "desc": "حوّل وحدات الوقت بدقة: مليثانية، ثانية، دقيقة، ساعة، يوم، أسبوع، شهر، وسنة. أداة مجانية من Nexluna.",
        "intro": "حوّل بين وحدات الوقت المختلفة بسهولة — من المليثانية حتى السنة.",
        "faq": [("كم ثانية في الساعة؟", "الساعة الواحدة = 3600 ثانية."),
                ("كم يوم في السنة؟", "السنة الشمسية ≈ 365.25 يوم.")]},
    "pressure": {"name": "الضغط", "icon": "pressure",
        "title": "محول وحدات الضغط | باسكال، بار، ضغط جوي، psi — Nexluna",
        "desc": "حوّل وحدات الضغط بدقة: باسكال، كيلوباسكال، بار، ضغط جوي (atm)، psi، وملم زئبق. أداة مجانية من Nexluna.",
        "intro": "حوّل بين وحدات الضغط المستخدمة في الهندسة والطقس والإطارات بدقة فورية.",
        "faq": [("كم باسكال في البار؟", "البار الواحد = 100,000 باسكال."),
                ("كم psi في الضغط الجوي؟", "الضغط الجوي (1 atm) ≈ 14.6959 psi.")]},
    "energy": {"name": "الطاقة", "icon": "energy",
        "title": "محول وحدات الطاقة | جول، سعرة، كيلوواط·ساعة، BTU — Nexluna",
        "desc": "حوّل وحدات الطاقة بدقة: جول، كيلوجول، سعرة، كيلوسعرة، واط·ساعة، كيلوواط·ساعة، وBTU. أداة مجانية من Nexluna.",
        "intro": "حوّل بين وحدات الطاقة المختلفة — مفيد للتغذية والفيزياء وفواتير الكهرباء.",
        "faq": [("كم جول في الكيلوسعرة؟", "الكيلوسعرة الواحدة = 4184 جول."),
                ("كم كيلوسعرة في الكيلوواط·ساعة؟", "1 كيلوواط·ساعة ≈ 860.42 كيلوسعرة.")]},
    "power": {"name": "القدرة", "icon": "power",
        "title": "محول وحدات القدرة | واط، كيلوواط، حصان، BTU/ساعة — Nexluna",
        "desc": "حوّل وحدات القدرة بدقة: واط، كيلوواط، ميغاواط، حصان، وBTU/ساعة. أداة مجانية وسريعة من Nexluna.",
        "intro": "حوّل بين وحدات القدرة المختلفة — مفيد للمحركات والأجهزة الكهربائية والتكييف.",
        "faq": [("كم واط في الحصان؟", "الحصان الواحد ≈ 745.7 واط."),
                ("كم حصان في الكيلوواط؟", "1 كيلوواط ≈ 1.34102 حصان.")]},
    "angle": {"name": "الزوايا", "icon": "angle",
        "title": "محول وحدات الزوايا | درجة، راديان، غراد — Nexluna",
        "desc": "حوّل وحدات الزوايا بدقة: درجة، راديان، غراد، دقيقة قوسية، وثانية قوسية. أداة مجانية من Nexluna.",
        "intro": "حوّل بين وحدات قياس الزوايا — مفيد للرياضيات والهندسة والفلك.",
        "faq": [("كم درجة في الراديان؟", "1 راديان ≈ 57.2958 درجة."),
                ("كم درجة في الدورة الكاملة؟", "الدورة الكاملة = 360 درجة = 2π راديان.")]},
    "fuel": {"name": "استهلاك الوقود", "icon": "fuel",
        "title": "محول استهلاك الوقود | كم/لتر، لتر/100كم، ميل/جالون — Nexluna",
        "desc": "حوّل معدلات استهلاك الوقود بدقة بين كم/لتر، لتر/100كم، وميل/جالون (mpg). أداة مجانية من Nexluna.",
        "intro": "قارن كفاءة استهلاك السيارات بالتحويل بين كم/لتر ولتر/100كم وميل/جالون.",
        "faq": [("كيف أحوّل من كم/لتر إلى لتر/100كم؟", "اقسم 100 على قيمة كم/لتر."),
                ("كم كم/لتر يساوي 30 mpg؟", "30 ميل/جالون ≈ 12.75 كيلومتر/لتر.")]},
    "frequency": {"name": "التردد", "icon": "frequency",
        "title": "محول وحدات التردد | هيرتز، كيلوهيرتز، ميغاهيرتز — Nexluna",
        "desc": "حوّل وحدات التردد بدقة: هيرتز، كيلوهيرتز، ميغاهيرتز، غيغاهيرتز، ودورة/دقيقة (rpm). أداة مجانية من Nexluna.",
        "intro": "حوّل بين وحدات التردد المختلفة — مفيد للإلكترونيات والصوتيات والاتصالات.",
        "faq": [("كم هيرتز في الكيلوهيرتز؟", "الكيلوهيرتز الواحد = 1000 هيرتز."),
                ("كم هيرتز يساوي 60 rpm؟", "60 دورة/دقيقة = 1 هيرتز.")]},
}

ORDER = list(PAGES.keys())


def faq_jsonld(items):
    ent = ",".join(
        '{ "@type": "Question", "name": "%s", "acceptedAnswer": { "@type": "Answer", "text": "%s" } }' % (q, a)
        for q, a in items
    )
    return '{ "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [%s] }' % ent


def faq_html(items):
    out = []
    for q, a in items:
        out.append('        <details class="faq-item"><summary>%s</summary><p>%s</p></details>' % (q, a))
    return "\n".join(out)


def related_cards(cur):
    """3 related converter cards (skip current)."""
    others = [c for c in ORDER if c != cur][:3]
    # prefer a sensible neighbour set
    cards = []
    for c in others:
        p = PAGES[c]
        cards.append(
            '        <a class="card" href="/converters/%s.html">\n'
            '          <div class="card-icon"><span data-icon="%s"></span></div>\n'
            '          <h3>%s</h3>\n'
            '          <p>تحويل فوري ودقيق لوحدات %s.</p>\n'
            '          <span class="arrow" data-icon="arrow" aria-hidden="true"></span>\n'
            '        </a>' % (c, p["icon"], p["name"], p["name"])
        )
    return "\n".join(cards)


TEMPLATE = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="theme-color" content="#4f46e5">
  <meta name="author" content="Nexluna">
  <link rel="canonical" href="{base}/converters/{cat}.html">
  <link rel="alternate" hreflang="ar" href="{base}/converters/{cat}.html">
  <link rel="alternate" hreflang="x-default" href="{base}/converters/{cat}.html">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Nexluna">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{base}/converters/{cat}.html">
  <meta property="og:image" content="{base}/assets/img/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{base}/assets/img/og-image.png">

  <link rel="icon" href="/assets/img/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.webmanifest">

  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/cairo-var.woff2" crossorigin>
  <link rel="preload" as="font" type="font/woff2" href="/assets/fonts/tajawal-800.woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/fonts.css">

  <link rel="stylesheet" href="/assets/css/style.css">
  <script>(function(){{try{{var t=localStorage.getItem('nx-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}document.documentElement.classList.add('js-ready');}})();</script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "الرئيسية", "item": "{base}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "المحولات", "item": "{base}/#converters" }},
      {{ "@type": "ListItem", "position": 3, "name": "{name}", "item": "{base}/converters/{cat}.html" }}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "محول وحدات {name} — Nexluna",
    "url": "{base}/converters/{cat}.html",
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Any",
    "inLanguage": "ar",
    "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }}
  }}
  </script>
  <script type="application/ld+json">
  {faq_ld}
  </script>

{ads_loader}
</head>
<body>
  <a class="skip-link" href="#main">تخطَّ إلى المحتوى الرئيسي</a>
{header}
  <main id="main">
    <div class="container section">
      <nav class="breadcrumb" aria-label="مسار التنقل">
        <a href="/">الرئيسية</a> <span aria-hidden="true">›</span> <a href="/#converters">المحولات</a> <span aria-hidden="true">›</span> <span>{name}</span>
      </nav>
      <div class="section-head reveal" style="margin-bottom:var(--sp-6)">
        <span class="eyebrow"><span data-icon="{icon}"></span> محوّل {name}</span>
        <h1>محول وحدات {name}</h1>
        <p class="lead">{intro}</p>
      </div>

      <div class="converter reveal" id="converter-app" data-only="{cat}"><div class="conv-skeleton" aria-hidden="true"><div class="sk sk-tabs"></div><div class="sk-row"><div class="sk sk-field"></div><div class="sk sk-swap"></div><div class="sk sk-field"></div></div><div class="sk sk-result"></div></div></div>

      <div class="ad-slot ad-inarticle reveal" aria-hidden="true">
        <ins class="adsbygoogle" style="display:block" data-ad-client="{adsense}" data-ad-slot="1234567891" data-ad-format="fluid" data-ad-layout="in-article" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <section class="section-sm reveal">
        <div class="section-head">
          <span class="eyebrow"><span data-icon="grid"></span> محولات ذات صلة</span>
          <h2>جرّب محولات أخرى</h2>
        </div>
        <div class="grid grid-3">
{related}
        </div>
      </section>

      <section class="section-sm reveal">
        <div class="prose">
          <h2>الأسئلة الشائعة عن تحويل {name}</h2>
{faq_html}
        </div>
      </section>

      <div class="ad-slot ad-leaderboard reveal" aria-hidden="true">
        <ins class="adsbygoogle" style="display:block" data-ad-client="{adsense}" data-ad-slot="1234567892" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>
    </div>
  </main>
{footer}
  <script src="/assets/js/icons.js" defer></script>
  <script src="/assets/js/converter.js" defer></script>
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
'''


ADS_LOADER = (
    '  <script>/* Defer AdSense until idle — keeps LCP/TBT low (perf pillar) */\n'
    '  (function(){function load(){if(window.__ads)return;window.__ads=1;'
    "var s=document.createElement('script');s.async=true;s.crossOrigin='anonymous';"
    "s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + ADSENSE + "';"
    'document.head.appendChild(s);}\n'
    "  if('requestIdleCallback'in window){requestIdleCallback(load,{timeout:3500});}"
    "else{window.addEventListener('load',function(){setTimeout(load,1200);});}\n"
    "  ['scroll','pointerdown','keydown'].forEach(function(e){window.addEventListener(e,load,{once:true,passive:true});});})();</script>"
)


def main():
    outdir = os.path.join(os.path.dirname(__file__), "converters")
    os.makedirs(outdir, exist_ok=True)
    for cat, p in PAGES.items():
        html = TEMPLATE.format(
            base=BASE, cat=cat, name=p["name"], title=p["title"], desc=p["desc"],
            intro=p["intro"], icon=p["icon"], header=HEADER, footer=FOOTER, adsense=ADSENSE,
            faq_ld=faq_jsonld(p["faq"]), faq_html=faq_html(p["faq"]),
            related=related_cards(cat), ads_loader=ADS_LOADER,
        )
        with open(os.path.join(outdir, cat + ".html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote converters/%s.html" % cat)


if __name__ == "__main__":
    main()
