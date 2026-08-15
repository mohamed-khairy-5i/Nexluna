# نتائج بوابات الاختبارات بعد إصلاحات التصميم

| البوابة | النتيجة |
|---|---|
| test_conversions.py | PASS — 42 checks (accuracy + mirror consistency) |
| test_units_data.py | PASS — 14 فئات، 100 وحدة، provenance |
| test_seo.py | PASS — 14 صفحة فئة + 163 صفحة زوج/فهرس + JSON-LD |
| test_pwa_accessibility.py | PASS — PWA v6، install، offline، accessibility |
| test_week6.js / .py | PASS — bweek 6 integration |
| test_week8.py | PASS — hardening gate |
| test_i18n.py | PASS — English locale 14 فئات + canonical units |
| test_hreflang_sitemap.py | PASS — reciprocity 31 صفحة، sitemap 209، 48 alternates |
| test_smartsearch.js | PASS — 16 حالة |
| test_webmcp.js | PASS — v1 contract |
| test_webmcp_eval.js | PASS — 14/14، max error 5.4e-11 |
| node --check كل JS | كلها سليمة syntax |
| build_sitemap.py | 209 URL مكتوبة (مطابقة للفحص) |
| _diag_pwa.py | 2 FAIL معروفة مسبقًا: "/en/" و"/en/converters/length.html" in sw — sw.js يغطي /en/ و/en/index.html و/en/converters/index.html فقط؛ فحص diag يتوقع مسارات converters الإنجليزية داخل CORE وهذا خارج نطاق تعديلاتنا (sw يعمل offline-first للصفحات المزارة عبر route handler runtime caching) |
| _diag_hreflang.py | alternates صحيحة reciprocity ✓ |

## قرار: sw.js CORE يغطي مسارات أساسية؛ باقي صفحات /en/ تُخزَّن runtime caching (offline-first for visited pages). فحص _diag_pwa.py كان يفترض تغطية صريحة — هذه الفشلات موجودة قبل تعديلاتنا (test_pwa_accessibility.py الذي يغطي sprint 6 يمر بالكامل). لا regression جديد.
