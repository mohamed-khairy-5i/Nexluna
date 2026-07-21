#!/usr/bin/env python3
"""Generate Nexluna content pages (about, contact, privacy, 404, blog)."""
import os
from build_pages import HEADER, FOOTER, BASE

def page(path, title, desc, body, canonical=None, noindex=False, extra_head=""):
    canon = canonical or (BASE + "/" + path)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    canon_tag = "" if noindex else f'  <link rel="canonical" href="{canon}">\n'
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#4f46e5">
  <meta name="author" content="Nexluna">
{canon_tag}  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Nexluna">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{BASE}/assets/img/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:image" content="{BASE}/assets/img/og-image.png">

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
{extra_head}</head>
<body>
  <a class="skip-link" href="#main">تخطَّ إلى المحتوى الرئيسي</a>
{HEADER}
  <main id="main">
{body}
  </main>
{FOOTER}
  <script src="/assets/js/icons.js" defer></script>
  <script src="/assets/js/main.js" defer></script>
</body>
</html>
'''

def write(path, html):
    full = os.path.join(os.path.dirname(__file__), path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

# ---------- About ----------
about_body = '''    <div class="container section">
      <nav class="breadcrumb" aria-label="مسار التنقل"><a href="/">الرئيسية</a> <span aria-hidden="true">›</span> <span>عن الموقع</span></nav>
      <div class="prose">
        <h1>عن Nexluna</h1>
        <p>Nexluna منصّة ويب عربية مجانية وفخمة لتحويل وحدات القياس المختلفة بدقة وسرعة. أُنشئت لتوفير تجربة أنيقة وسريعة تعمل على جميع الأجهزة، مع دعم كامل للغة العربية والاتجاه من اليمين إلى اليسار.</p>
        <h2>رسالتنا</h2>
        <p>نؤمن بأن أدوات القياس اليومية تستحق واجهة عربية عصرية تحترم المستخدم — سريعة، دقيقة، خالية من التشويش، وتحمي خصوصيتك بالكامل.</p>
        <h2>ما الذي يميّزنا؟</h2>
        <ul>
          <li><strong>دقة عالية:</strong> نعتمد معاملات التحويل الرسمية الدولية بدقة تصل إلى 6 خانات عشرية.</li>
          <li><strong>سرعة فورية:</strong> النتائج تظهر أثناء الكتابة دون إعادة تحميل الصفحة.</li>
          <li><strong>سجل ومفضّلة:</strong> يحفظ المحوّل آخر تحويلاتك وفئاتك المفضّلة تلقائيًا على جهازك.</li>
          <li><strong>يعمل دون اتصال:</strong> تطبيق ويب تقدّمي (PWA) قابل للتثبيت ويعمل بلا إنترنت.</li>
          <li><strong>خصوصية تامّة:</strong> كل الحسابات تتم داخل متصفحك — لا نجمع بياناتك.</li>
          <li><strong>مجاني للجميع:</strong> بلا تسجيل وبلا رسوم.</li>
        </ul>
        <h2>الفئات المدعومة</h2>
        <p>ندعم 14 فئة قياس وأكثر من 100 وحدة: الطول، الوزن، المساحة، الحجم والسعة، درجة الحرارة، البيانات الرقمية، السرعة، الوقت، الضغط، الطاقة، القدرة، الزوايا، استهلاك الوقود، والتردد — ونضيف المزيد باستمرار.</p>
        <p><a class="btn btn-primary" href="/"><span data-icon="bolt"></span> ابدأ التحويل الآن</a></p>
      </div>
    </div>'''
write("about.html", page("about.html", "عن الموقع | Nexluna محول الوحدات",
    "تعرّف على Nexluna، الأداة العربية المجانية لتحويل وحدات القياس بدقة وسرعة على جميع الأجهزة.", about_body))

# ---------- Contact ----------
contact_body = '''    <div class="container section">
      <nav class="breadcrumb" aria-label="مسار التنقل"><a href="/">الرئيسية</a> <span aria-hidden="true">›</span> <span>اتصل بنا</span></nav>
      <div class="prose">
        <h1>اتصل بنا</h1>
        <p>يسعدنا تواصلك معنا لأي اقتراح أو ملاحظة أو استفسار. املأ النموذج التالي وسنعود إليك في أقرب وقت.</p>
        <form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/contact-success.html" style="display:grid;gap:var(--sp-4);max-width:560px">
          <input type="hidden" name="form-name" value="contact">
          <p style="display:none"><label>لا تملأ هذا الحقل: <input name="bot-field"></label></p>
          <div class="field"><label for="c-name">الاسم</label><input id="c-name" name="name" type="text" required autocomplete="name" maxlength="80"></div>
          <div class="field"><label for="c-email">البريد الإلكتروني</label><input id="c-email" name="email" type="email" required autocomplete="email" maxlength="120"></div>
          <div class="field"><label for="c-msg">الرسالة</label><textarea id="c-msg" name="message" rows="5" required maxlength="2000" style="padding:var(--sp-3) var(--sp-4);border:1px solid var(--border);border-radius:var(--radius-sm);font-family:var(--font);font-size:var(--step-0);background:var(--surface);color:var(--text)"></textarea></div>
          <button class="btn btn-primary" type="submit">إرسال الرسالة</button>
        </form>
      </div>
    </div>'''
write("contact.html", page("contact.html", "اتصل بنا | Nexluna",
    "تواصل مع فريق Nexluna لأي اقتراح أو ملاحظة أو استفسار حول أدوات تحويل الوحدات.", contact_body))

# ---------- Contact success ----------
success_body = '''    <div class="container section text-center">
      <div class="prose" style="text-align:center">
        <h1>تم إرسال رسالتك ✅</h1>
        <p>شكرًا لتواصلك مع Nexluna. سنعود إليك في أقرب وقت ممكن.</p>
        <p><a class="btn btn-primary" href="/">العودة إلى الصفحة الرئيسية</a></p>
      </div>
    </div>'''
write("contact-success.html", page("contact-success.html", "تم الإرسال | Nexluna",
    "تم استلام رسالتك بنجاح، وسيتواصل معك فريق Nexluna في أقرب وقت ممكن. شكرًا لتواصلك معنا.", success_body, noindex=True))

# ---------- Privacy ----------
privacy_body = '''    <div class="container section">
      <nav class="breadcrumb" aria-label="مسار التنقل"><a href="/">الرئيسية</a> <span aria-hidden="true">›</span> <span>سياسة الخصوصية</span></nav>
      <div class="prose">
        <h1>سياسة الخصوصية</h1>
        <p>آخر تحديث: 2025. تحترم Nexluna خصوصيتك. توضّح هذه السياسة كيفية تعاملنا مع البيانات عند استخدامك للموقع.</p>
        <h2>البيانات التي نجمعها</h2>
        <p>عمليات التحويل تُجرى بالكامل داخل متصفحك ولا تُرسل قيمك إلى خوادمنا. قد نجمع بيانات إحصائية مجهّلة الهوية لتحسين الخدمة.</p>
        <h2>الإعلانات وملفات تعريف الارتباط</h2>
        <p>نستخدم إعلانات Google AdSense التي قد تستعمل ملفات تعريف الارتباط (Cookies) لعرض إعلانات مناسبة. يمكنك إدارة تفضيلات الإعلانات من
        <a href="https://www.google.com/settings/ads" rel="nofollow noopener" target="_blank">إعدادات إعلانات Google</a>.
        كما يستخدم بائعو الطرف الثالث — بما فيهم Google — ملفات الارتباط لعرض الإعلانات بناءً على زياراتك السابقة.</p>
        <h2>التحليلات</h2>
        <p>قد نستخدم أدوات تحليل لفهم كيفية استخدام الموقع بشكل تجميعي دون تحديد هويتك الشخصية.</p>
        <h2>حقوقك</h2>
        <p>يمكنك تعطيل ملفات تعريف الارتباط من إعدادات متصفحك في أي وقت. لأي استفسار حول الخصوصية، يُرجى <a href="/contact.html">التواصل معنا</a>.</p>
      </div>
    </div>'''
write("privacy.html", page("privacy.html", "سياسة الخصوصية | Nexluna",
    "سياسة خصوصية Nexluna: كيف نتعامل مع بياناتك وملفات تعريف الارتباط والإعلانات.", privacy_body))

# ---------- 404 ----------
nf_body = '''    <div class="container section text-center">
      <div class="prose" style="text-align:center">
        <h1 style="font-size:var(--step-3)">404</h1>
        <p>عذرًا، الصفحة التي تبحث عنها غير موجودة أو تم نقلها.</p>
        <p><a class="btn btn-primary" href="/">العودة إلى الرئيسية</a></p>
        <p class="mt-6"><a href="/converters/length.html">الطول</a> · <a href="/converters/weight.html">الوزن</a> · <a href="/converters/temperature.html">الحرارة</a> · <a href="/converters/data.html">البيانات</a> · <a href="/blog/">المدونة</a></p>
      </div>
    </div>'''
write("404.html", page("404.html", "الصفحة غير موجودة | Nexluna",
    "عذرًا، الصفحة التي تبحث عنها غير موجودة أو تم نقلها. عد إلى الرئيسية أو استكشف محوّلات Nexluna للوحدات.", nf_body, noindex=True))

# ---------- Offline (PWA fallback) ----------
offline_body = '''    <div class="container section text-center">
      <div class="prose" style="text-align:center">
        <div style="display:inline-grid;place-items:center;width:88px;height:88px;border-radius:24px;background:var(--primary-50);color:var(--primary);margin-bottom:var(--sp-4)"><span data-icon="offline" style="display:grid;place-items:center"></span></div>
        <h1>أنت غير متصل بالإنترنت</h1>
        <p>يبدو أنك فقدت الاتصال. يمكنك تصفّح الصفحات التي زرتها سابقًا، أو المحاولة مرة أخرى عند عودة الاتصال.</p>
        <p><a class="btn btn-primary" href="/"><span data-icon="history"></span> إعادة المحاولة</a></p>
      </div>
    </div>'''
write("offline.html", page("offline.html", "غير متصل | Nexluna",
    "يبدو أنك فقدت الاتصال بالإنترنت. يمكنك تصفّح الصفحات التي زرتها سابقًا في Nexluna أو إعادة المحاولة لاحقًا.", offline_body, noindex=True))

if __name__ == "__main__":
    print("done")
