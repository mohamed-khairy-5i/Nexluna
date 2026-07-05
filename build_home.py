#!/usr/bin/env python3
"""Generate the premium Nexluna homepage (index.html)."""
import os
from build_pages import HEADER, FOOTER, BASE, ADSENSE, PAGES, ORDER

# Category cards for the converter grid (all 14)
CARD_DESC = {
    "length": "متر، كيلومتر، ميل، قدم، إنش",
    "weight": "كيلوغرام، غرام، رطل، أونصة",
    "area": "متر مربع، هكتار، فدان",
    "volume": "لتر، جالون، كوب، متر مكعب",
    "temperature": "سيلسيوس، فهرنهايت، كلفن",
    "data": "بايت، ميغابايت، غيغابايت",
    "speed": "كم/س، م/ث، ميل/س، عقدة",
    "time": "ثانية، دقيقة، ساعة، سنة",
    "pressure": "باسكال، بار، atm، psi",
    "energy": "جول، سعرة، كيلوواط·ساعة",
    "power": "واط، كيلوواط، حصان",
    "angle": "درجة، راديان، غراد",
    "fuel": "كم/لتر، لتر/100كم، mpg",
    "frequency": "هيرتز، كيلوهيرتز، ميغاهيرتز",
}


def cards():
    out = []
    for i, c in enumerate(ORDER):
        p = PAGES[c]
        out.append(
            '          <a class="card cat-card cat-%s reveal" style="--d:%dms" href="/converters/%s.html">\n'
            '            <div class="card-icon"><span data-icon="%s"></span></div>\n'
            '            <div class="cat-card-text"><h3>%s</h3><p>%s</p></div>\n'
            '            <span class="arrow" data-icon="arrow" aria-hidden="true"></span>\n'
            '          </a>' % (c, (i % 5) * 45, c, p["icon"], p["name"], CARD_DESC[c])
        )
    return "\n".join(out)


FEATURES = [
    ("bolt", "نتائج فورية", "تحويل لحظي أثناء الكتابة دون الضغط على أي زر، بدقة تصل إلى 6 خانات عشرية."),
    ("offline", "يعمل بدون إنترنت", "تطبيق ويب تقدّمي (PWA) قابل للتثبيت ويعمل بالكامل حتى دون اتصال بالشبكة."),
    ("copy", "نسخ وحفظ", "انسخ النتيجة بنقرة واحدة، واحتفظ بسجل آخر تحويلاتك ومفضّلاتك تلقائيًا."),
    ("moon", "وضع ليلي أنيق", "تبديل سلس بين المظهر الفاتح والداكن مع حفظ تفضيلك على جهازك."),
    ("shield", "خصوصية تامّة", "كل الحسابات تتم داخل متصفحك — لا نجمع بياناتك ولا نرسلها لأي خادم."),
    ("globe", "عربي أصيل RTL", "واجهة عربية بالكامل من اليمين لليسار بخط Cairo الأنيق على كل الأجهزة."),
]


def features():
    out = []
    for icon, h, p in FEATURES:
        out.append(
            '          <div class="feature reveal">\n'
            '            <div class="fi"><span data-icon="%s"></span></div>\n'
            '            <div><h3>%s</h3><p>%s</p></div>\n'
            '          </div>' % (icon, h, p)
        )
    return "\n".join(out)


# Competitor comparison rows: (feature, us, rivals...)
COMPARE_ROWS = [
    ("تحويل فوري أثناء الكتابة", True, True, False),
    ("سجل التحويلات والمفضّلة", True, False, False),
    ("نسخ النتيجة بنقرة واحدة", True, True, True),
    ("يعمل دون إنترنت (PWA)", True, False, False),
    ("وضع ليلي كامل", True, True, False),
    ("واجهة عربية RTL أصيلة", True, False, False),
    ("14 فئة + 100+ وحدة", True, False, True),
    ("بدون تتبّع أو تسجيل دخول", True, True, False),
]


def compare():
    rows = []
    for feat, a, b, c in COMPARE_ROWS:
        def cell(v, cls=""):
            mark = '<span data-icon="check" class="yes"></span>' if v else '<span class="no">—</span>'
            return '<td class="%s">%s</td>' % (cls, mark)
        rows.append(
            '          <tr><td>%s</td>%s%s%s</tr>'
            % (feat, cell(a, "us"), cell(b), cell(c))
        )
    return "\n".join(rows)


HTML = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nexluna | محوّل وحدات القياس العربي الأدق والأسرع — مجانًا</title>
  <meta name="description" content="Nexluna منصّة عربية فخمة لتحويل وحدات القياس: الطول، الوزن، الحرارة، الحجم، البيانات، السرعة والمزيد — 14 فئة و100+ وحدة بدقة فورية، تعمل دون إنترنت وبدون تتبّع.">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="theme-color" content="#4f46e5">
  <meta name="author" content="Nexluna">
  <meta name="keywords" content="محول وحدات, تحويل الوحدات, محول الطول, محول الوزن, محول درجة الحرارة, تحويل القياسات, محول عربي">
  <link rel="canonical" href="''' + BASE + '''/">
  <link rel="alternate" hreflang="ar" href="''' + BASE + '''/">
  <link rel="alternate" hreflang="x-default" href="''' + BASE + '''/">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Nexluna">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:title" content="Nexluna | محوّل وحدات القياس العربي الأدق والأسرع">
  <meta property="og:description" content="14 فئة و100+ وحدة بدقة فورية، تعمل دون إنترنت وبدون تتبّع.">
  <meta property="og:url" content="''' + BASE + '''/">
  <meta property="og:image" content="''' + BASE + '''/assets/img/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Nexluna | محوّل وحدات القياس العربي">
  <meta name="twitter:description" content="14 فئة و100+ وحدة بدقة فورية، تعمل دون إنترنت.">
  <meta name="twitter:image" content="''' + BASE + '''/assets/img/og-image.png">

  <link rel="icon" href="/assets/img/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="icon" type="image/svg+xml" href="/assets/img/logo.svg">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.webmanifest">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap"></noscript>

  <link rel="stylesheet" href="/assets/css/style.css">
  <script>(function(){try{var t=localStorage.getItem('nx-theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}document.documentElement.classList.add('js-ready');})();</script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Nexluna",
    "alternateName": "نكسلونا",
    "url": "''' + BASE + '''/",
    "inLanguage": "ar",
    "description": "منصّة عربية لتحويل وحدات القياس بدقة وسرعة.",
    "potentialAction": {
      "@type": "SearchAction",
      "target": "''' + BASE + '''/converters/{search_term_string}.html",
      "query-input": "required name=search_term_string"
    }
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Nexluna",
    "url": "''' + BASE + '''/",
    "logo": "''' + BASE + '''/assets/img/icon-512.png",
    "sameAs": []
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Nexluna — محوّل الوحدات",
    "url": "''' + BASE + '''/",
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Any",
    "inLanguage": "ar",
    "browserRequirements": "Requires JavaScript",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
    "featureList": ["تحويل 14 فئة قياس", "سجل التحويلات", "المفضّلة", "يعمل دون إنترنت", "وضع ليلي", "نسخ النتيجة"]
  }
  </script>

  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=''' + ADSENSE + '''" crossorigin="anonymous"></script>
</head>
<body>
  <a class="skip-link" href="#main">تخطَّ إلى المحتوى الرئيسي</a>
''' + HEADER + '''
  <main id="main">

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <span class="eyebrow"><span class="dot"></span> المحوّل العربي الأدق لعام 2026</span>
        <h1>حوّل أي وحدة قياس<br><span class="grad">بدقّة وسرعة وأناقة</span></h1>
        <p class="lead">منصّة Nexluna تجمع 14 فئة و100+ وحدة في مكان واحد — نتائج فورية، سجل ذكي، ووضع ليلي، تعمل حتى دون إنترنت.</p>
        <div class="hero-cta">
          <a href="#converter" class="btn btn-primary"><span data-icon="bolt"></span> ابدأ التحويل الآن</a>
          <a href="#converters" class="btn btn-outline"><span data-icon="grid"></span> تصفّح المحولات</a>
        </div>
        <div class="hero-stats">
          <div class="hero-stat"><b>14</b><span>فئة قياس</span></div>
          <div class="hero-stat"><b>+100</b><span>وحدة مدعومة</span></div>
          <div class="hero-stat"><b>100%</b><span>مجاني وبلا إعلان مزعج</span></div>
          <div class="hero-stat"><b>0</b><span>تتبّع أو تسجيل</span></div>
        </div>
        <div class="trust-bar">
          <span class="chip"><span data-icon="bolt"></span> نتائج فورية</span>
          <span class="chip"><span data-icon="offline"></span> يعمل دون إنترنت</span>
          <span class="chip"><span data-icon="shield"></span> بدون تتبّع</span>
          <span class="chip"><span data-icon="globe"></span> عربي RTL</span>
        </div>
      </div>
    </section>

    <!-- Live converter -->
    <section class="container section-sm" id="converter">
      <div class="converter reveal" id="converter-app"></div>
    </section>

    <!-- Ad -->
    <div class="container">
      <div class="ad-slot ad-leaderboard reveal" aria-hidden="true">
        <ins class="adsbygoogle" style="display:block" data-ad-client="''' + ADSENSE + '''" data-ad-slot="1234567890" data-ad-format="auto" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
      </div>
    </div>

    <!-- All converters grid -->
    <section class="container section" id="converters">
      <div class="section-head reveal">
        <span class="eyebrow"><span data-icon="grid"></span> كل المحولات</span>
        <h2>14 فئة تحويل في متناول يدك</h2>
        <p>اختر الفئة التي تحتاجها وابدأ التحويل فورًا — كل صفحة مُحسّنة لمحركات البحث ومزوّدة بصيغ التحويل والأسئلة الشائعة.</p>
      </div>
      <div class="grid grid-cards">
''' + cards() + '''
      </div>
    </section>

    <!-- Features -->
    <section class="container section" id="features">
      <div class="section-head reveal">
        <span class="eyebrow"><span data-icon="star"></span> لماذا Nexluna؟</span>
        <h2>مزايا تصنع الفارق</h2>
        <p>صُمّم كل تفصيل ليمنحك تجربة تحويل سريعة وأنيقة وآمنة على أي جهاز.</p>
      </div>
      <div class="grid grid-2">
''' + features() + '''
      </div>
    </section>

    <!-- Comparison table -->
    <section class="container section" id="compare">
      <div class="section-head reveal">
        <span class="eyebrow"><span data-icon="check2"></span> مقارنة عادلة</span>
        <h2>لماذا يتفوّق Nexluna؟</h2>
        <p>قارنّا مزايانا بأشهر أدوات التحويل الأخرى لتختار عن اقتناع.</p>
      </div>
      <div class="compare-wrap reveal">
        <table class="compare">
          <thead>
            <tr>
              <th>الميزة</th>
              <th class="us">Nexluna</th>
              <th>أدوات تقليدية</th>
              <th>محولات أجنبية</th>
            </tr>
          </thead>
          <tbody>
''' + compare() + '''
          </tbody>
        </table>
      </div>
    </section>

    <!-- CTA band -->
    <section class="container section">
      <div class="cta-band reveal">
        <h2>ثبّت Nexluna على جهازك</h2>
        <p>أضف المحوّل إلى شاشتك الرئيسية واستخدمه كأي تطبيق — بسرعة وبدون إنترنت.</p>
        <a href="#converter" class="btn btn-outline"><span data-icon="bolt"></span> جرّبه الآن</a>
      </div>
    </section>

    <!-- FAQ -->
    <section class="container section" id="faq">
      <div class="prose reveal">
        <h2 class="text-center">الأسئلة الشائعة</h2>
        <details class="faq-item"><summary>هل استخدام Nexluna مجاني بالكامل؟</summary><p>نعم، جميع أدوات التحويل مجانية 100% دون تسجيل أو اشتراك.</p></details>
        <details class="faq-item"><summary>هل يعمل الموقع بدون اتصال بالإنترنت؟</summary><p>نعم، Nexluna تطبيق ويب تقدّمي (PWA) يمكن تثبيته والعمل به بالكامل دون إنترنت بعد أول زيارة.</p></details>
        <details class="faq-item"><summary>هل تُحفظ بياناتي أو تُرسل لخادم؟</summary><p>لا. كل الحسابات تتم داخل متصفحك فقط، وسجل التحويلات يُخزّن محليًا على جهازك ولا يُرسل لأي مكان.</p></details>
        <details class="faq-item"><summary>كم فئة ووحدة يدعمها الموقع؟</summary><p>يدعم Nexluna 14 فئة قياس وأكثر من 100 وحدة، من الطول والوزن حتى البيانات الرقمية واستهلاك الوقود.</p></details>
        <details class="faq-item"><summary>ما مدى دقة النتائج؟</summary><p>تُحسب النتائج بمعاملات تحويل قياسية دقيقة وتُعرض حتى 6 خانات عشرية.</p></details>
      </div>
    </section>

  </main>
''' + FOOTER + '''
  <script src="/assets/js/icons.js" defer></script>
  <script src="/assets/js/converter.js" defer></script>
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
'''


def main():
    path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(HTML)
    print("wrote index.html (%d chars)" % len(HTML))


if __name__ == "__main__":
    main()
