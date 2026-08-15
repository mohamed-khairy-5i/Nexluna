# Local Preview Findings

## Date

2026-08-15.

## Preview URL

Temporary sandbox preview: `https://8766-ipiz4dmfm1kgvdc8wau1y-c5cfc5ee.sg1.manus.computer/`.

## Homepage smoke check

The Arabic RTL homepage loaded successfully with the Nexluna title, main navigation, Smart Search, 14 category links, converter controls, install CTA, FAQ, and dark/light theme control. Clicking the Smart Search example `5 كم بالميل` produced the deterministic result `5 كيلومتر (km) = 3.106856 ميل (mi)` and exposed the link to the length converter.

## Embed smoke check

The route `/embed.html?category=length&from=km&to=mi&v=5` loaded successfully. Query parameters populated the category, source unit, target unit, and value. The widget displayed the deterministic result `3.1068559611866697`, and the page showed the independent converter controls and link back to the full Nexluna site.

## Observation

Both the main page and embed route are operational under the temporary local preview. The first preview attempt on port 8765 was unavailable through the public proxy because the prior server was bound to localhost; the second server on port 8766 was bound to `0.0.0.0` and worked.

## Converter page smoke check

The route `/converters/length.html` loaded successfully. The page exposed the Arabic RTL converter, the decimal/binary system selector, favorite control, source and target selectors, swap button, and local input/output fields. The extracted page includes the canonical unit list and SEO content. The visible viewport showed the converter card and its controls without a fatal loading state.

## Explanation smoke check

After entering `5` on the length converter, the page produced `5,000` for `5 km → m` and exposed the button `اشرح الحساب`. Clicking it displayed: `النتيجة حُسبت حتميًا بواسطة NexConvert من كيلومتر (km) إلى متر (m). شرح محلي؛ الرقم صادر حتميًا من NexConvert.` The numeric result remained unchanged, confirming the explanation layer is optional and non-authoritative.

## Expansion UI smoke check

The regenerated homepage now shows a materially different hero: deep measurement-themed canvas, RTL split layout, prominent value proposition, deterministic search entry, visible metrics, trust chips, and a measurement orbit preview showing `5 km → 3.10686 mi`. The extracted DOM retained the live search, all 14 categories, converter mount, install CTA, FAQ, and existing navigation. `python3 build_home.py`, JavaScript syntax checks, `test_conversions.py`, and `test_week6.py` passed after the change.

## Category page expansion smoke check

The regenerated `/converters/length.html` now exposes a category hero with the length icon, a clear `حوّل وحدات الطول بوضوح وثقة` headline, deterministic/clipboard/offline pills, and the live converter directly below it. The existing category route, unit selectors, favorite control, and conversion mount remain present. Core conversion, Week 6, PWA, and SEO gates passed after regeneration.


## Phase: English locale verification (post-expansion build)

- English home `/en/`: `lang="en" dir="ltr"`, full English hero, 14 category cards in English, nav links to `/en/...`, "العربية" switch present.
- English length page `/en/converters/length.html`: English title/meta/H1, formulas and common conversions localized, `data-locale="en"`, locale file `locale.en.generated.js` contains `"Kilometer (km)"`, `"Meter (m)"`, `"from {from} to {to}"`.
- Fixed PWA cache bump `nexluna-v5` → `nexluna-v6` with `/en/`, `/en/index.html`, `/en/converters/index.html` in CORE and `locale.en.generated.js`.
- Added cache-busting `?v=6` to English script tags (build_en.py) to defeat stale SW copies in preview.
- Fixed generator comment source path (was printing `en.json.json`).
- Arabic header nav got `<a href="/en/" lang="en">English</a>`.
- `test_i18n.py` PASS (14 categories, full canonical unit coverage, `/en/` pages LTR).
- Smart Search localized for English via `en.json` smart keys + link path rewrite; tests PASS.
- Remaining preview caveat: My Browser SW may still serve old Arabic cached JS for `/en/` paths until v6 takeover completes.
