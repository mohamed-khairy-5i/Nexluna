# حالة مهمة مراجعة التصميم (Design Review)

## طلب المستخدم
أخطاء في التصميم — رجعها بشكل منطقي وليس جزءًا جزءًا (كل الإصلاحات دفعة واحدة)، مع تطبيق أفضل ممارسات الأزرار ومقاساتها المناسبة.

## البيئة
- المعاينة المحلية: http://127.0.0.1:8766 (أعد تشغيله بـ `cd /home/ubuntu/Nexluna && nohup python3 -m http.server 8766 --bind 0.0.0.0 >/dev/null 2>&1 &`)
- المشروع: /home/ubuntu/Nexluna على main، الإصدار 1.1.0
- نسخة احتياطية: assets/css/style.css.bak.v110

## نتائج الفحص البرمجي (مكتمل)

### تباين (scripts/_audit_contrast.py — يُشغّل بالفحص)
- ✗ FAIL أبيض على --accent (#14b8a6): 2.49:1
- ✗ FAIL أبيض على تدرج أفتح لون #2dd4bf: 1.86:1
- Δ حدي أبيض على --primary (#0f9488): 3.74:1 (كبير ≥18px/700)
- ✓ الباقي جميعه ≥4.5:1

### أزرار (scripts/_audit_buttons.py)
- 12 كلاساً بلا focus: .btn, .btn-primary, .btn-outline, .btn-sm, .cta-actions .btn, .pill-btn, .tab-btn, .swap-btn, .cat-card, .feature, .hero .btn-primary, .cta-band .btn-outline
- <44px: .result .copy-result (38px), .result .copy-result svg (18px), chip svg (15px), أيقونات svg داخل أزرار (16-24px — مقبول داخل حاوية 44px)
- 4 كلاسات بلا hover: .btn svg, .cta-actions .btn, .btn, .btn-sm
- 99 حالة px ثابت (بعضها في media queries = مقبول)

### كشف مهم: صفحة /en/ كلها بلا أنماط!
كلاسات build_en.py غير معرّفة إطلاقًا في style.css: hero-redesign, hero-actions, hero-pills, hero-lead, hero-measure-card, measure-orbit, measure-label, measure-mini, category-card, cat-icon, category-grid, feature-grid, related-card, related-grid, content-panel, section-lead, section-muted, btn-ghost, converter-shell, footer-badges, pair-num
(build_en.py يبني: header/footer/shell/home/converter/index — header EN يستخدم أيقونات menu/moon من icons.js، converter EN يستخدم assets/js/converter.js مع data-locale="en")

## قائمة إصلاحات style.css المعتمدة (دُفعت واحدة)
1. تدرج --grad-brand: استبدال #2dd4bf بـ #17a899 (أغمق قليلًا — يرفع تباين النص الأبيض من 1.86 إلى ≥4.5) + --grad-brand-soft تبقى (عناصر زخرفية)
2. token جديد --btn-grad-safe مع تدرج آمن أو تغطية عبر تعديل مباشر على القيم
3. embed-shell button: خلفية --accent → --accent-600 (أبيض نص على accent = FAIL)
4. .btn, .btn-primary, .btn-outline, .btn-sm, .btn-ghost: إضافة :focus-visible مع ring، و:active scale(0.98)، و:disabled opacity .5
5. pill-btn, tab-btn, swap-btn, .copy-result, .clear, .ss-chip: focus-visible + active
6. .result .copy-result: رفع من 38×38 إلى 44×44
7. chip التفاعلي: min-height 44px على (max-width:768px)
8. footer-dev-links a: 30×30 → 44×44
9. طبقة أنماط /en/ كاملة (انظر أعلاه)
10. focus على inputs يحافظ على :focus الحالي (box-shadow ring موجود) لكن .field input:focus {outline:none} — نضيف focus-visible explicit
11. hero .btn-primary (أبيض خلفية، نص nx-ink-deep) — سليم تباينًا، يبقى كما هو

## DESIGN_SPEC.md كُتب في /home/ubuntu/Nexluna/DESIGN_SPEC.md

## البوابات الواجب إعادة تشغيلها بعد التوليد
test_conversions.py, test_smartsearch.js, test_webmcp.js, test_webmcp_eval.js, test_i18n.py, test_units_data.py, test_pwa_accessibility.py, test_seo.py, test_week6.py, test_week8.py, test_hreflang_sitemap.py + node --check لكل سكربت JS
(في v1.1.0 نجحت كلها: conversions 42, smartsearch 16, webmcp 14/14, i18n, pwa v6, seo 14/163, week6, week8, hreflang/sitemap 31 صفحة 209 رابط)

## سكربتات التوليد
- build_home.py → index.html (عربي)
- build_pages.py → HEADER/FOOTER + صفحات الفئات converters/*.html + about/privacy/contact
- build_en.py → /en/index, /en/converters/*, /en/converters/index
- build_pairs.py → convert/*.html + convert/index
- embed.html مستقل (يدوي)
- بعد التعديلات: python3 build_home.py && python3 build_pages.py && python3 build_en.py && python3 build_pairs.py

## المرحلة الحالية
المرحلة 3: ✅ أُكملت إصلاحات style.css دفعة واحدة:
- تدرج --grad-brand أصبح #0c8578→#0e8e80→#0e9484 (أبيض نص عليه: 3.76:1 ≈ 3:1 large، نص كبير ≥18px/700 مقبول؛ لا يمكن تجاوز 4.5 إلا بتغميق قاتل للهوية — وثّق في DESIGN_SPEC)
- embed-shell button الآن --accent-600
- focus states: 22 كلاس تفاعلي الآن لديه focus-visible موحد
- copy-result 38→44px، pill/tab 44px، footer icons 30→44px، data-system-select 44px
- طبقة /en/ كاملة أُضيفت (hero-actions, hero-pills, category-grid, feature-grid, related, content-panel, measure-card...)
- embed.html حُدّث (focus states + min-height 3rem)
- ملاحظة: .btn svg يبقى "بلا hover/focus" في الفحص لكن موثق كعنصر داخلي داخل حاوية 48px — مقبول
- تباين --accent نفسه (2.49) بقي مُعلّمًا FAIL قصديًا كحارس: يُمنع استخدام نص أبيض على --accent (يستخدم للأيقونات/الحدود فقط)

## المتبقي
1. فحص بصري عبر المعرض بعد التوليد
2. توليد الصفحات: build_home.py, build_pages.py, build_en.py, build_pairs.py
3. تشغيل البوابات (انظر قائمة البوابات أعلاه)
4. تسليم مع جدول قبل/بعد
