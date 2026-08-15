# Task state: expansion build (post v1.0)

Phase 3 (i18n EN) DONE. Phase 4 (content system) DONE. Phase 5 (intl SEO + API contracts) IN PROGRESS.

Local server: `python3 -m http.server 8766 --bind 0.0.0.0` (session default). Public preview: https://8766-ipiz4dmfm1kgvdc8wau1y-c5cfc5ee.sg1.manus.computer/

## Key facts
- data/content.json: canonical content registry (9 articles: length, cooking, temperature, data-storage, weight, speed, natural-language-search, area, fuel) with slug, category, title_ar/en, excerpt_ar/en, unit_pairs (verified vs canonical units.json).
- build_blog.py: imports build_content_system; appends "مقالات ودلائل ذات صلة" per article; NEW full Arabic articles area-measurement-guide + fuel-economy-units with bodies+faq. All 9 pages, zero warnings.
- build_en.py: generates /en/ home + converters + /en/converters/index.html (no blog), shares HEADER/FOOTER/BASE/CSP from build_pages.py; scripts use ?v=6.
- build_pages.py: HEADER has English nav link; PAGES dict 14 cats w/ title/desc/intro/faq; faq_jsonld() helper; CSP_META; BASE=https://nexluna.netlify.app.
- All regenerators run clean. Gates pass: i18n, SEO (14 cats + 163 pair/index, JSON-LD), smartsearch 16, webmcp, conversions 42, units_data 14/100, week6, week8 (10 pages). test_pwa_accessibility fixed (v5→v6 cache, added locale.en.generated.js + /en/ SW checks).
- sw.js cache = nexluna-v6; VERSION file = v1.0.0; expansion target = v1.1.0.
- Rules: deterministic math never duplicated; single source data/units.json; no Calcuzakat merge; no external publishing; CI .github/workflows/ci.yml covers build + test_week8.

## Phase 5 DONE
- hreflang: build_home.py (ar home → en + x-default → /en/), build_pages.py (ar converters → hreflang="en" → /en/converters/{cat}), build_en.py shell() takes ar_path kwarg (en pages → hreflang="ar" back to / counterpart).
- scripts/build_sitemap.py: sitemap.xml 209 URLs (163 pairs, 9 articles, ar+en+static), valid XML, xhtml hreflang for home/converters (48 links).
- docs/CONTRACTS.md created: NexMCP v1 tools, embed postMessage, i18n structure, strict rules.

## Phase 6 progress (almost done)
- Full gate run ALL PASS (conversions 42, smartsearch 16, webmcp, webmcp_eval 14/14 max err 5.38e-11, i18n, units_data 14/100, pwa, seo 14/163, week6, week8, js syntax OK).
- test_hreflang_sitemap.py created (fixed: ar_path kwarg in build_en.py calls, directory-URL sitemap locs): PASS — 31 pages reciprocity, 209 sitemap URLs, 48 alternates.
- CI updated: added build_en.py + build_sitemap.py + test_i18n + test_hreflang_sitemap.
- VERSION bumped to 1.1.0.
- TODO: add [1.1.0] section to CHANGELOG.md (redesign hero + category hero, i18n EN via data/i18n/en.json + build_en.py, content registry data/content.json + 9 articles incl 2 new (area-measurement-guide, fuel-economy-units), hreflang + sitemap.xml, docs/CONTRACTS.md, CI updates), write NEXLUNA_EXPANSION_REPORT.md, final visual check on preview, deliver.

## Phase 6 TODO
- Full gate run (test_conversions, test_smartsearch, test_webmcp, test_webmcp_eval, test_i18n, test_units_data, test_pwa_accessibility, test_seo, test_week6, test_week8 + new sitemap/hreflang test).
- Bump VERSION + CHANGELOG → 1.1.0; write NEXLUNA_EXPANSION_REPORT.md; deliver with LOCAL_PREVIEW_FINDINGS.md.

User: Mohamed (Fayoum, Egypt). Replies in Egyptian Arabic.
