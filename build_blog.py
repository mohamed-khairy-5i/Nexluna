#!/usr/bin/env python3
"""Generate Nexluna blog index and articles."""
import os
from build_pages import HEADER, FOOTER, BASE

def article_page(slug, title, desc, date, body_html, faq=None, image=None, alt="", read="5"):
    img = image or "/assets/img/og-image.png"
    img_abs = BASE + img if img.startswith("/") else img
    hero_html = f'        <img class="article-hero" src="{img}" width="1200" height="675" alt="{alt}" fetchpriority="high">' if image else ""
    faq_ld = ""
    if faq:
        ents = ",".join('{ "@type": "Question", "name": "%s", "acceptedAnswer": { "@type": "Answer", "text": "%s" } }' % (q, a) for q, a in faq)
        faq_ld = '\n  <script type="application/ld+json">\n  { "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [%s] }\n  </script>' % ents
    url = f"{BASE}/blog/{slug}.html"
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | مدونة Nexluna</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <meta name="theme-color" content="#4f46e5">
  <meta name="author" content="Nexluna">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Nexluna">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img_abs}">
  <meta property="article:published_time" content="{date}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:image" content="{img_abs}">

  <link rel="icon" href="/assets/img/favicon.ico" sizes="any">
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
    "@type": "Article",
    "headline": "{title}",
    "description": "{desc}",
    "datePublished": "{date}",
    "dateModified": "{date}",
    "image": "{img_abs}",
    "author": {{ "@type": "Organization", "name": "Nexluna" }},
    "publisher": {{ "@type": "Organization", "name": "Nexluna", "logo": {{ "@type": "ImageObject", "url": "{BASE}/assets/img/icon-512.png" }} }},
    "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{url}" }},
    "inLanguage": "ar"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "الرئيسية", "item": "{BASE}/" }},
      {{ "@type": "ListItem", "position": 2, "name": "المدونة", "item": "{BASE}/blog/" }},
      {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "{url}" }}
    ]
  }}
  </script>{faq_ld}

  <script>/* Defer AdSense until the page is idle — keeps LCP/TBT low (perf pillar) */
  (function(){{function load(){{if(window.__ads)return;window.__ads=1;var s=document.createElement('script');s.async=true;s.crossOrigin='anonymous';s.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9822291009441043';document.head.appendChild(s);}}
  if('requestIdleCallback'in window){{requestIdleCallback(load,{{timeout:3500}});}}else{{window.addEventListener('load',function(){{setTimeout(load,1200);}});}}
  ['scroll','pointerdown','keydown'].forEach(function(e){{window.addEventListener(e,load,{{once:true,passive:true}});}});}})();</script>
</head>
<body>
  <a class="skip-link" href="#main">تخطَّ إلى المحتوى الرئيسي</a>
{HEADER}
  <main id="main">
    <article class="container section">
      <nav class="breadcrumb" aria-label="مسار التنقل"><a href="/">الرئيسية</a> <span aria-hidden="true">›</span> <a href="/blog/">المدونة</a> <span aria-hidden="true">›</span> <span>{title}</span></nav>
      <div class="prose">
        <h1>{title}</h1>
        <p class="article-meta" style="color:var(--text-muted);font-size:var(--step--1);display:flex;gap:var(--sp-3);flex-wrap:wrap;align-items:center"><span>نُشر في {date}</span><span aria-hidden="true">·</span><span>قراءة {read} دقائق</span></p>
{hero_html}
{body_html}
        <div class="ad-slot ad-inarticle" aria-hidden="true">
          <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9822291009441043" data-ad-slot="1234567893" data-ad-format="fluid" data-ad-layout="in-article" data-full-width-responsive="true"></ins>
          <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>
        <p class="mt-6"><a class="btn btn-primary" href="/"><span data-icon="bolt"></span> جرّب محول Nexluna الآن</a></p>
      </div>
    </article>
  </main>
{FOOTER}
  <script src="/assets/js/icons.js" defer></script>
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
'''

ARTICLES = [
    {
        "slug": "length-conversion-guide",
        "title": "الدليل الشامل لتحويل وحدات الطول",
        "desc": "تعلّم كيفية التحويل بين المتر والكيلومتر والميل والقدم والإنش بأمثلة عملية وجداول مرجعية سهلة.",
        "date": "2025-01-15",
        "read": "6",
        "image": "/assets/img/blog/length.webp",
        "alt": "أدوات قياس الطول مثل المسطرة وشريط القياس",
        "excerpt": "كل ما تحتاج معرفته للتحويل بين وحدات الطول المترية والإمبراطورية بدقة.",
        "body": '''        <p>تُعدّ وحدات الطول من أكثر وحدات القياس استخدامًا في حياتنا اليومية، من قياس المسافات على الخرائط إلى حساب أبعاد الأثاث. في هذا الدليل نشرح الفروق بين النظام المتري والنظام الإمبراطوري، ونقدّم جداول تحويل جاهزة.</p>
        <h2>النظام المتري مقابل الإمبراطوري</h2>
        <p>يعتمد النظام المتري على المتر كوحدة أساسية، ويتفرّع منه الكيلومتر والسنتيمتر والمليمتر بمضاعفات عشرية بسيطة. أما النظام الإمبراطوري فيستخدم القدم والإنش والميل والياردة، وهو شائع في الولايات المتحدة والمملكة المتحدة.</p>
        <h2>أهم معاملات التحويل</h2>
        <table>
          <thead><tr><th>من</th><th>إلى</th><th>اضرب في</th></tr></thead>
          <tbody>
            <tr><td>متر</td><td>قدم</td><td>3.28084</td></tr>
            <tr><td>كيلومتر</td><td>ميل</td><td>0.621371</td></tr>
            <tr><td>إنش</td><td>سنتيمتر</td><td>2.54</td></tr>
            <tr><td>ميل</td><td>كيلومتر</td><td>1.60934</td></tr>
          </tbody>
        </table>
        <h2>أمثلة عملية</h2>
        <ul>
          <li>لتحويل 5 كيلومترات إلى أميال: 5 × 0.621371 = 3.107 ميل.</li>
          <li>لتحويل 10 أقدام إلى أمتار: 10 × 0.3048 = 3.048 متر.</li>
        </ul>
        <p>يمكنك إجراء كل هذه الحسابات فورًا باستخدام <a href="/converters/length.html">محول الطول من Nexluna</a> دون الحاجة لحفظ المعاملات.</p>''',
        "faq": [("كم قدم في المتر؟", "المتر الواحد يساوي 3.28084 قدم."), ("كم كيلومتر في الميل؟", "الميل الواحد يساوي 1.60934 كيلومتر.")],
    },
    {
        "slug": "cooking-measurement-conversion",
        "title": "تحويل وحدات القياس في الطبخ: دليل المطبخ العملي",
        "desc": "تعلّم كيفية تحويل الأكواب والملاعق والغرامات والمليلترات في وصفاتك بدقة لنتائج مثالية في كل مرة.",
        "date": "2025-02-10",
        "read": "5",
        "image": "/assets/img/blog/cooking.webp",
        "alt": "أدوات المطبخ وأكواب وملاعق القياس",
        "excerpt": "دليل عملي لتحويل مقادير الطبخ بين الأكواب والغرامات والمليلترات.",
        "body": '''        <p>الطبخ علمٌ ودقة، وكثير من الوصفات العالمية تستخدم وحدات مختلفة عمّا اعتدنا عليه. معرفة كيفية تحويل الأكواب إلى غرامات أو المليلترات إلى أونصات يضمن نجاح وصفتك.</p>
        <h2>الوزن مقابل الحجم</h2>
        <p>من المهم التمييز بين وحدات الوزن (غرام، رطل) ووحدات الحجم (مليلتر، كوب). فالكوب الواحد من الدقيق لا يزن مثل الكوب الواحد من السكر، لأن الكثافة تختلف.</p>
        <h2>جدول تحويل سريع للمطبخ</h2>
        <table>
          <thead><tr><th>الوحدة</th><th>المكافئ</th></tr></thead>
          <tbody>
            <tr><td>1 كوب</td><td>≈ 236.6 مليلتر</td></tr>
            <tr><td>1 ملعقة كبيرة</td><td>≈ 15 مليلتر</td></tr>
            <tr><td>1 ملعقة صغيرة</td><td>≈ 5 مليلتر</td></tr>
            <tr><td>1 أونصة سائلة</td><td>≈ 29.57 مليلتر</td></tr>
          </tbody>
        </table>
        <h2>نصائح للطهاة</h2>
        <ul>
          <li>استخدم ميزانًا رقميًا للوصفات التي تتطلب دقة عالية مثل المخبوزات.</li>
          <li>حوّل درجات حرارة الفرن بين الفهرنهايت والسيلسيوس باستخدام <a href="/converters/temperature.html">محول الحرارة</a>.</li>
          <li>للسوائل، استعن بـ<a href="/converters/volume.html">محول الحجم والسعة</a> للحصول على نتائج فورية.</li>
        </ul>''',
        "faq": [("كم مليلتر في الكوب؟", "الكوب الأمريكي يساوي نحو 236.6 مليلتر."), ("كم مليلتر في الملعقة الكبيرة؟", "الملعقة الكبيرة تساوي نحو 15 مليلتر.")],
    },
    {
        "slug": "temperature-conversion-guide",
        "title": "تحويل درجات الحرارة: سيلسيوس وفهرنهايت وكلفن بالتفصيل",
        "desc": "افهم الفرق بين سيلسيوس وفهرنهايت وكلفن، وتعلّم صيغ التحويل بينها مع أمثلة عملية ونقاط مرجعية مهمة.",
        "date": "2025-03-05",
        "read": "6",
        "image": "/assets/img/blog/temperature.webp",
        "alt": "ميزان حرارة يوضح درجات الحرارة بالسيلسيوس والفهرنهايت",
        "excerpt": "شرح مبسّط لصيغ التحويل بين وحدات الحرارة الثلاث مع أمثلة.",
        "body": '''        <p>تُقاس درجة الحرارة بثلاث وحدات رئيسية حول العالم: السيلسيوس (°C) الشائع في معظم الدول، والفهرنهايت (°F) المستخدم في الولايات المتحدة، والكلفن (K) المعتمد في العلوم الفيزيائية. معرفة التحويل بينها مهارة يومية مفيدة.</p>
        <h2>صيغ التحويل الأساسية</h2>
        <table>
          <thead><tr><th>التحويل</th><th>الصيغة</th></tr></thead>
          <tbody>
            <tr><td>سيلسيوس → فهرنهايت</td><td>°F = (°C × 9/5) + 32</td></tr>
            <tr><td>فهرنهايت → سيلسيوس</td><td>°C = (°F − 32) × 5/9</td></tr>
            <tr><td>سيلسيوس → كلفن</td><td>K = °C + 273.15</td></tr>
          </tbody>
        </table>
        <h2>نقاط مرجعية مهمة</h2>
        <ul>
          <li>تجمّد الماء: 0°C = 32°F = 273.15K</li>
          <li>غليان الماء: 100°C = 212°F = 373.15K</li>
          <li>درجة حرارة الجسم الطبيعية: 37°C = 98.6°F</li>
        </ul>
        <h2>مثال عملي</h2>
        <p>لتحويل 25 درجة سيلسيوس إلى فهرنهايت: (25 × 9/5) + 32 = 77°F. جرّب أي قيمة فورًا عبر <a href="/converters/temperature.html">محول درجة الحرارة من Nexluna</a>.</p>''',
        "faq": [("كيف أحوّل من سيلسيوس إلى فهرنهايت؟", "استخدم الصيغة °F = (°C × 9/5) + 32."), ("ما درجة غليان الماء بالفهرنهايت؟", "غليان الماء يحدث عند 212°F أي 100°C.")],
    },
    {
        "slug": "data-storage-units-explained",
        "title": "وحدات تخزين البيانات: الفرق بين الكيلوبايت والكيبي بايت",
        "desc": "دليل تقني مبسّط يشرح وحدات تخزين البيانات العشرية (KB, MB, GB) والثنائية (KiB, MiB, GiB) ولماذا تختلف أحجام أقراصك.",
        "date": "2025-04-12",
        "read": "7",
        "image": "/assets/img/blog/data.webp",
        "alt": "خوادم وأقراص تخزين البيانات الرقمية",
        "excerpt": "لماذا يظهر قرص 1 تيرابايت بسعة أقل؟ الفرق بين النظامين العشري والثنائي.",
        "body": '''        <p>كثيرًا ما نتساءل: لماذا يظهر قرص سعته «1 تيرابايت» بمساحة أقل عند توصيله بالحاسوب؟ الجواب يكمن في الفرق بين نظامي القياس العشري والثنائي لوحدات البيانات.</p>
        <h2>النظام العشري مقابل الثنائي</h2>
        <p>الشركات المصنّعة للأقراص تستخدم النظام العشري (1 كيلوبايت = 1000 بايت)، بينما تحسب أنظمة التشغيل بالنظام الثنائي (1 كيبي بايت = 1024 بايت). هذا الفرق يتراكم كلما كبر الحجم.</p>
        <h2>جدول الوحدات</h2>
        <table>
          <thead><tr><th>الوحدة</th><th>القيمة</th></tr></thead>
          <tbody>
            <tr><td>1 بايت</td><td>8 بت</td></tr>
            <tr><td>1 كيلوبايت (KB)</td><td>1000 بايت</td></tr>
            <tr><td>1 كيبي بايت (KiB)</td><td>1024 بايت</td></tr>
            <tr><td>1 ميغابايت (MB)</td><td>1,000,000 بايت</td></tr>
            <tr><td>1 غيغابايت (GB)</td><td>مليار بايت</td></tr>
          </tbody>
        </table>
        <h2>لماذا يهم هذا للمطوّرين؟</h2>
        <ul>
          <li>عند حساب سرعات النقل، تأكّد من نوع الوحدة (بت أم بايت).</li>
          <li>تُقاس سرعات الإنترنت غالبًا بالميغابت (Mbps) وليس الميغابايت.</li>
        </ul>
        <p>حوّل بين كل هذه الوحدات بدقة عبر <a href="/converters/data.html">محول البيانات الرقمية من Nexluna</a>.</p>''',
        "faq": [("ما الفرق بين GB و GiB؟", "الغيغابايت (GB) = مليار بايت، أما الغيبي بايت (GiB) = 1,073,741,824 بايت."), ("كم بت في البايت؟", "البايت الواحد يساوي 8 بت.")],
    },
]

def write(path, html):
    full = os.path.join(os.path.dirname(__file__), path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

def build():
    for a in ARTICLES:
        write(f"blog/{a['slug']}.html", article_page(a["slug"], a["title"], a["desc"], a["date"], a["body"],
              a.get("faq"), image=a.get("image"), alt=a.get("alt", ""), read=a.get("read", "5")))
    # blog index — image cards
    cards = "\n".join(
        f'''          <a class="card blog-card" href="/blog/{a['slug']}.html">
            <img class="blog-thumb" src="{a['image']}" width="600" height="338" alt="{a.get('alt','')}" loading="lazy">
            <div class="blog-card-body">
              <span class="blog-date">{a['date']} · قراءة {a.get('read','5')} دقائق</span>
              <h3>{a['title']}</h3>
              <p>{a['excerpt']}</p>
              <span class="arrow" data-icon="arrow" aria-hidden="true"></span>
            </div>
          </a>''' for a in ARTICLES)
    idx_body = f'''    <div class="container section">
      <nav class="breadcrumb" aria-label="مسار التنقل"><a href="/">الرئيسية</a> <span aria-hidden="true">›</span> <span>المدونة</span></nav>
      <div class="section-head">
        <span class="eyebrow"><span data-icon="book"></span> المدونة</span>
        <h1>مدونة Nexluna</h1>
        <p>مقالات ودلائل عملية حول وحدات القياس والتحويل بينها بأسلوب مبسّط.</p>
      </div>
      <div class="grid grid-2 blog-grid">
{cards}
      </div>
    </div>'''
    from build_content import page
    write("blog/index.html", page("blog/", "المدونة | Nexluna محول الوحدات",
        "مقالات ودلائل عملية حول تحويل وحدات القياس: الطول، الوزن، الحرارة، الحجم والمزيد.",
        idx_body, canonical=BASE + "/blog/"))

if __name__ == "__main__":
    build()
