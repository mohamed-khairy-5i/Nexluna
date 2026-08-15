#!/usr/bin/env python3
"""Generate Nexluna blog index and articles."""
import os
from build_pages import HEADER, FOOTER, BASE, CSP_META

def article_page(slug, title, desc, date, body_html, faq=None, image=None, alt="", read="5", meta_title=None):
    doc_title = meta_title or f"{title} | مدونة Nexluna"
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
{CSP_META}  <title>{doc_title}</title>
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
        <div class="ad-slot ad-inarticle" role="complementary" aria-label="إعلان">
          <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-9822291009441043" data-ad-slot="1234567893" data-ad-format="fluid" data-ad-layout="in-article" data-full-width-responsive="true"></ins>
          <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>
        <p class="mt-6"><a class="btn btn-primary" href="/"><span data-icon="bolt"></span> جرّب محول Nexluna الآن</a></p>
      </div>
    </article>
  </main>
{FOOTER}
  <script src="/assets/js/icons.js" defer></script>
  <script src="/assets/js/webmcp.js" defer></script>
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
        "meta_title": "تحويل درجات الحرارة: سيلسيوس وفهرنهايت وكلفن",
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
        "meta_title": "وحدات تخزين البيانات: كيلوبايت مقابل كيبي بايت",
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
    {
        "slug": "weight-conversion-guide",
        "title": "دليل تحويل وحدات الوزن: كيلوغرام ورطل وأونصة",
        "desc": "تعلّم التحويل بين الكيلوغرام والغرام والرطل والأونصة بدقة، مع جداول جاهزة وأمثلة عملية للطبخ والشحن والرياضة.",
        "date": "2025-05-08",
        "read": "6",
        "image": "/assets/img/blog/weight.webp",
        "alt": "ميزان يوضح وحدات الوزن المختلفة",
        "excerpt": "كل ما تحتاجه للتحويل بين وحدات الوزن المترية والإمبراطورية بدقة.",
        "body": '''        <p>الوزن من أكثر القياسات حضورًا في حياتنا: من وزن الحقائب في المطار إلى مقادير الوصفات وأوزان التمارين. يستخدم معظم العالم النظام المتري (كيلوغرام وغرام)، بينما تعتمد الولايات المتحدة الرطل والأونصة.</p>
        <h2>أهم معاملات التحويل</h2>
        <table>
          <thead><tr><th>من</th><th>إلى</th><th>اضرب في</th></tr></thead>
          <tbody>
            <tr><td>كيلوغرام</td><td>رطل</td><td>2.204623</td></tr>
            <tr><td>رطل</td><td>كيلوغرام</td><td>0.453592</td></tr>
            <tr><td>غرام</td><td>أونصة</td><td>0.035274</td></tr>
            <tr><td>أونصة</td><td>غرام</td><td>28.349523</td></tr>
          </tbody>
        </table>
        <h2>أمثلة عملية</h2>
        <ul>
          <li>لتحويل 70 كيلوغرامًا إلى أرطال: 70 × 2.204623 = 154.32 رطل.</li>
          <li>لتحويل 16 أونصة إلى غرامات: 16 × 28.349523 = 453.59 غرام (أي رطل واحد).</li>
        </ul>
        <p>احسب أي وزن فورًا عبر <a href="/converters/weight.html">محول الوزن من Nexluna</a>، أو استخدم صفحات التحويل الجاهزة مثل <a href="/convert/kg-to-lb.html">كيلوغرام إلى رطل</a>.</p>''',
        "faq": [("كم رطل في الكيلوغرام؟", "الكيلوغرام الواحد يساوي نحو 2.204623 رطل."), ("كم غرام في الأونصة؟", "الأونصة الواحدة تساوي نحو 28.35 غرام.")],
    },
    {
        "slug": "speed-conversion-guide",
        "title": "تحويل وحدات السرعة: كم/ساعة وميل/ساعة والعقدة",
        "desc": "افهم الفروق بين كيلومتر/ساعة وميل/ساعة ومتر/ثانية والعقدة، مع صيغ تحويل وأمثلة للسفر والرياضة والملاحة.",
        "date": "2025-06-03",
        "read": "5",
        "image": "/assets/img/blog/speed.webp",
        "alt": "عدّاد سرعة يوضح وحدات السرعة",
        "excerpt": "دليل مبسّط للتحويل بين وحدات السرعة الشائعة في السفر والملاحة.",
        "body": '''        <p>تختلف وحدات السرعة حسب السياق: الطرق تستخدم كيلومتر/ساعة أو ميل/ساعة، والفيزياء تستخدم متر/ثانية، بينما تعتمد الملاحة البحرية والجوية العقدة (knot).</p>
        <h2>أهم معاملات التحويل</h2>
        <table>
          <thead><tr><th>من</th><th>إلى</th><th>القاعدة</th></tr></thead>
          <tbody>
            <tr><td>متر/ثانية</td><td>كم/ساعة</td><td>× 3.6</td></tr>
            <tr><td>كم/ساعة</td><td>ميل/ساعة</td><td>× 0.621371</td></tr>
            <tr><td>عقدة</td><td>كم/ساعة</td><td>× 1.852</td></tr>
          </tbody>
        </table>
        <h2>أمثلة عملية</h2>
        <ul>
          <li>سيارة تسير بـ100 كم/ساعة = نحو 62.14 ميل/ساعة.</li>
          <li>سفينة بسرعة 20 عقدة = 37.04 كم/ساعة.</li>
        </ul>
        <p>حوّل أي سرعة فورًا عبر <a href="/converters/speed.html">محول السرعة</a>، أو جرّب <a href="/convert/kmh-to-mph.html">كم/ساعة إلى ميل/ساعة</a>.</p>''',
        "faq": [("كم ميل/ساعة يساوي 100 كم/ساعة؟", "100 كم/ساعة ≈ 62.14 ميل/ساعة."), ("كم كم/ساعة في العقدة؟", "العقدة الواحدة = 1.852 كيلومتر/ساعة.")],
    },
    {
        "slug": "natural-language-conversion-search",
        "title": "كيف تحوّل الوحدات بلغتك الطبيعية على Nexluna",
        "desc": "اكتب سؤالك كما تنطقه — «5 كم بالميل» أو «100 celsius to f» — واحصل على إجابة فورية دقيقة عبر البحث الذكي في Nexluna.",
        "date": "2025-07-01",
        "read": "4",
        "image": "/assets/img/blog/search.webp",
        "alt": "شريط بحث ذكي لتحويل الوحدات",
        "excerpt": "تعرّف على البحث الذكي الذي يفهم أسئلتك بالعربية والإنجليزية ويجيبك فورًا.",
        "body": '''        <p>لم تعد بحاجة لاختيار الفئة والوحدات يدويًا. يفهم البحث الذكي في Nexluna أسئلتك المكتوبة بلغة طبيعية — بالعربية أو الإنجليزية — ويعطيك الرقم فورًا.</p>
        <h2>أمثلة يفهمها فورًا</h2>
        <ul>
          <li><strong>5 كم بالميل</strong> ← 3.106856 ميل</li>
          <li><strong>100 كجم رطل</strong> ← 220.462262 رطل</li>
          <li><strong>كم قدم في المتر</strong> ← يفهم «كم» كسؤال ويعطي 3.28 قدم</li>
          <li><strong>100 celsius to f</strong> ← 212 فهرنهايت</li>
        </ul>
        <h2>كيف يعمل؟</h2>
        <p>يحلّل النظام سؤالك حرفيًا: يوحّد الأرقام العربية واللاتينية، ويزيل التشكيل، ويتعرّف على السوابق مثل «بال» و«ال»، ثم يطابق الوحدات ويحسب النتيجة بنفس دقّة المحوّل الكامل — <strong>بلا أي تخمين أو ذكاء اصطناعي يهلوس</strong>. كل إجابة صحيحة رياضيًا بنسبة 100%.</p>
        <p>جرّبه الآن من <a href="/">الصفحة الرئيسية</a> — فقط اكتب سؤالك واضغط Enter.</p>''',
        "faq": [("هل يفهم البحث العربية والإنجليزية معًا؟", "نعم، يمكنك الخلط بينهما مثل «20 celsius to فهرنهايت»."), ("هل النتائج دقيقة؟", "نعم، تمرّ كل النتائج عبر نفس محرّك الحساب الدقيق في المحوّل، بلا تخمين.")],
    },
    {
        "slug": "area-measurement-guide",
        "title": "دليل قياس المساحات: الفدّان والقيراط والهكتار والأكر",
        "meta_title": "دليل قياس المساحات: الفدّان والأكر والهكتار",
        "desc": "افهم الفرق بين الفدّان المصري والأكر الدولي وقارن بين وحدات المساحات الشائعة في المنطقة بخطوات بسيطة.",
        "date": "2025-08-05",
        "read": "6",
        "image": "/assets/img/blog/area.webp",
        "alt": "خريطة ومساحات أراضي بوحدات مختلفة",
        "excerpt": "الفرق بين الفدّان المصري والأكر الدولي ولماذا يخلط بينهما كثيرون.",
        "body": '''        <p>تُعدّ وحدات قياس المساحات من أكثر ما يسبّب ارتباكًا في التعاملات العقارية والأراضي الزراعية، خاصة في مصر والوطن العربي حيث يُستخدم الفدّان والقيراط والسهم والدونم إلى جانب الأكر والهكتار الدوليين.</p>
        <h2>الفدّان المصري مقابل الأكر الدولي</h2>
        <p>الفدّان وحدة مصرية تقليدية تساوي 4200.833 مترًا مربعًا تقريبًا، بينما الأكر الدولي (Acre) المستخدم في الولايات المتحدة وبريطانيا يساوي 4046.856 مترًا مربعًا. الفرق بينهما نحو 3.8%، وهو فرق كافٍ للتأثير على حسابات الأسعار والمساحات في العقود.</p>
        <h2>أهم الوحدات في المنطقة</h2>
        <table>
          <thead><tr><th>الوحدة</th><th>القيمة بالمتر المربع</th></tr></thead>
          <tbody>
            <tr><td>الفدّان</td><td>4200.833</td></tr>
            <tr><td>القيراط (المصري)</td><td>175.03</td></tr>
            <tr><td>السهم</td><td>7.29</td></tr>
            <tr><td>الدونم</td><td>1000</td></tr>
            <tr><td>الهكتار</td><td>10,000</td></tr>
            <tr><td>الأكر</td><td>4046.856</td></tr>
          </tbody>
        </table>
        <p>حوّل بين أي من هذه الوحدات بدقة عبر <a href="/converters/area.html">محول المساحات من Nexluna</a>.</p>''',
        "faq": [("كم متر مربع في الفدّان؟", "الفدّان الواحد يساوي نحو 4200.833 مترًا مربعًا."), ("ما الفرق بين الفدّان والأكر؟", "الفدّان أكبر من الأكر بنحو 3.8%."), ("كم قيراط في الفدّان؟", "الفدّان الواحد يساوي 24 قيراطًا."), ("ما قيمة السهم؟", "السهم الواحد يساوي نحو 7.29 مترًا مربعًا.")],
    },
    {
        "slug": "fuel-economy-units",
        "title": "وحدات استهلاك الوقود: كم/لتر وmpg الأمريكية والبريطانية",
        "meta_title": "وحدات استهلاك الوقود: كم/لتر وmpg وl/100km",
        "desc": "تعرّف على اتفاقيات قياس كفاءة استهلاك الوقود الثلاث ولماذا يختلف رقم mpg بين أمريكا وبريطانيا.",
        "date": "2025-09-01",
        "read": "5",
        "image": "/assets/img/blog/fuel.webp",
        "alt": "عداد الوقود ورمز استهلاكه في لوحة سيارة",
        "excerpt": "لماذا تختلف أرقام استهلاك الوقود بين أمريكا وبريطانيا والوطن العربي؟",
        "body": '''        <p>تُقاس كفاءة استهلاك الوقود بثلاث اتفاقيات رئيسية حول العالم، وكل منها يعكس طريقة تفكير مختلفة: المسافة لكل لتر في الشرق الأوسط كثيرًا، والمسافة لكل غالون في أمريكا وبريطانيا، وحجم الوقود لكل مسافة (لتر/100 كم) في معظم أوروبا.</p>
        <h2>الغالون الأمريكي مقابل البريطاني</h2>
        <p>الغالون الأمريكي يساوي 3.785 لترًا، بينما الغالون البريطاني (الإمبراطوري) يساوي 4.546 لترًا. لذلك فإن رقم «30 mpg» أمريكيًا يعادل نحو 36 mpg بريطانيًا — نفس الاستهلاك الحقيقي برقمين مختلفين.</p>
        <h2>قواعد التحويل الأساسية</h2>
        <table>
          <thead><tr><th>من</th><th>إلى</th><th>القاعدة</th></tr></thead>
          <tbody>
            <tr><td>كم/لتر</td><td>mpg أمريكي</td><td>× 2.352</td></tr>
            <tr><td>لتر/100 كم</td><td>كم/لتر</td><td>100 ÷ القيمة</td></tr>
            <tr><td>mpg أمريكي</td><td>لتر/100 كم</td><td>235.215 ÷ القيمة</td></tr>
          </tbody>
        </table>
        <p>قارن بين كل هذه الاتفاقيات فورًا عبر <a href="/converters/fuel.html">محول استهلاك الوقود من Nexluna</a>.</p>''',
        "faq": [("ما الفرق بين mpg الأمريكية والبريطانية؟", "الغالون البريطاني أكبر من الأمريكي بنحو 20%، فالرقم البريطاني أعلى لنفس الاستهلاك."), ("كيف أحوّل كم/لتر إلى mpg؟", "اضرب القيمة في 2.352 للحصول على mpg الأمريكية."), ("ما معنى لتر/100 كم؟", "حجم الوقود المستهلك لقطع 100 كيلومتر؛ الرقم الأقل يعني استهلاكًا أفضل.")],
    },
]

import build_content_system

def write(path, html):
    full = os.path.join(os.path.dirname(__file__), path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def body_suffix(cat):
    """Related converter + article links from the canonical content registry."""
    related = build_content_system.converter_links("ar", cat)
    if not related:
        return ""
    items = "".join(f'<li><a href="{href}">{title}</a></li>' for href, title in related)
    return f'''        <h2>مقالات ودلائل ذات صلة</h2>
        <ul>{items}</ul>'''

def build():
    registry_articles = {a["slug"]: a for a in build_content_system.registry()["articles"]}
    for a in ARTICLES:
        reg = registry_articles.get(a["slug"])
        body = a["body"]
        if reg:
            body = (body.rstrip() + "\n" + body_suffix(reg["category"]).lstrip()).strip()
        write(f"blog/{a['slug']}.html", article_page(a["slug"], a["title"], a["desc"], a["date"], body,
              a.get("faq"), image=a.get("image"), alt=a.get("alt", ""), read=a.get("read", "5"),
              meta_title=a.get("meta_title")))
    for slug in registry_articles:
        if slug not in {a["slug"] for a in ARTICLES}:
            print("warning: content.json article without body:", slug)
    # blog index — image cards
    cards = "\n".join(
        f'''          <a class="card blog-card" href="/blog/{a['slug']}.html">
            <img class="blog-thumb" src="{a['image']}" width="600" height="338" alt="{a.get('alt','')}" loading="lazy">
            <div class="blog-card-body">
              <span class="blog-date">{a['date']} · قراءة {a.get('read','5')} دقائق</span>
              <h2 class="card-title">{a['title']}</h2>
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
