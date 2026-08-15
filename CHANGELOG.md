# Changelog

## [1.1.0] — 2026-08-15

Nexluna v1.1.0 يحوّل المنتج من إصدار تقني حتمي إلى منتج ظاهر ومتعدد اللغات ومنظم المحتوى، مع الحفاظ على الحساب الحتمي ومصدر الوحدات الوحيد وعدم دمج Calcuzakat.

### Added

- إعادة تصميم مرئي: Hero جديد مع بطاقة قياس وبطولة صفحات الفئات، مع تنسيق متجاوب يدعم RTL/LTR.
- بنية i18n عبر `data/locales.json` و`data/i18n/en.json` و`scripts/generate_locale_js.py`، وواجهة إنجليزية كاملة تحت `/en/` عبر `build_en.py`.
- توطين محرك المحوّل والشرح والبحث الذكي وerror boundary بحيث تتبدل النصوص فقط ويبقى الحساب واحدًا.
- سجل محتوى canonical جديد `data/content.json` يجمع المقالات التعليمية ويربط كل مقال بمحوّله، مع مقاليّ قياس المساحة (الفدّان والأكر) واستهلاك الوقود.
- روابط hreflang المتبادلة بين العربية والإنجليزية في 31 صفحة، و`sitemap.xml` بمقدار 209 عناوين عبر `scripts/build_sitemap.py`.
- بوابة اختبار جديدة `test_i18n.py` للتحقق من تغطية الإنجليزية و`test_hreflang_sitemap.py` لروابط اللغات وسلامة sitemap.
- توثيق العقود في `docs/CONTRACTS.md`.

### Changed

- رفع Service Worker إلى cache `nexluna-v6` مع cache-busting لأصول النسخة الإنجليزية.
- تحديث GitHub CI ليشمل مولد الإنجليزية والسitemap وبوابات i18n وhreflang.

### Verification

- جميع بوابات الجودة ناجحة: التحويلات (42)، Smart Search (16)، WebMCP وeval (14/14 بأقصى خطأ 5.38e-11)، i18n، الوحدات (14/100)، PWA، SEO (14/163)، أسبوع 6، أسبوع 8، hreflang/sitemap (31 صفحة و209 رابط).
- فحص بصري محلي: الصفحة الرئيسية وصفحات الفئات العربية والإنجليزية وزر «اشرح الحساب» وواجهة embed تعمل فعليًا.

## [1.0.0] — 2026-08-15

Nexluna v1.0.0 يثبت طبقة قياس عربية حتمية وقابلة للاستدعاء من وكلاء الذكاء الاصطناعي، مع إبقاء Calcuzakat مشروعًا منفصلًا خارج نطاق هذا الإصدار.

### Added

- مصدر canonical واحد للوحدات في `data/units.json` مع provenance للفئات والوحدات، وتوليد `assets/js/units.generated.js`.
- عقد WebMCP v1 للأدوات `convert_units` و`list_units` و`get_unit_info` و`explain_conversion`.
- طبقة تفسير اختيارية لا تغيّر الناتج الرقمي ولا تجعل الشبكة شرطًا للحساب.
- واجهة embed مستقلة مع تعبئة query string وإرسال نتيجة `postMessage`.
- دعم PWA والتثبيت والمشاركة والنسخ الاحتياطي المحلي للنتيجة.
- صفحات SEO مولدة لخمسة عشر فهرسًا/مسارًا و162 صفحة زوج تحويل، مع JSON-LD مناسب.
- WebMCP eval يغطي الفئات الأربع عشرة، واختبارات تكامل أسبوع 6، وبوابة GitHub Actions.
- سياسة CSP ورؤوس أمنية، وerror boundary عميل يعرض fallback محليًا دون كشف تفاصيل الخطأ أو إرسالها للخارج.

### Changed

- توحيد ترتيب تحميل JavaScript: `units.generated.js` ثم `explain.js` ثم `webmcp.js` ثم `converter.js` عند الحاجة.
- رفع Service Worker إلى cache `nexluna-v5` وإضافة أصول الشرح والـembed.
- تثبيت نظامي البيانات العشري والثنائي في المحوّل مع إبقاء الحساب حتميًا.

### Verification

- بوابة التحويل: 42 فحصًا ناجحًا.
- Smart Search: 16 حالة regression ناجحة عبر 14 فئة.
- WebMCP contract: ناجح.
- canonical data: 14 فئة و100 سجل وحدة مع provenance صالح.
- SEO: 14 صفحة فئة و163 صفحة زوج/فهرس مع عقود JSON-LD.
- Week 6 integration: ناجح.
- WebMCP eval: 14/14، بمعدل نجاح 100%، وأقصى خطأ نسبي مسجل `5.379660867220314e-11`.
- Week 8 hardening: نجح محليًا عبر `test_week8.py`، مع فحص CSP وerror boundary وملفات الإصدار.

### Scope and limitations

هذا الإصدار مجهز محليًا على فرع `main` ولم يُنشر خارجيًا. لا يحتوي على تكامل أو دمج مع Calcuzakat. تفسير اللغة اختياري، بينما التحويل العددي الأساسي يعمل محليًا من المصدر canonical ولا يعتمد على نموذج أو اتصال شبكي.
