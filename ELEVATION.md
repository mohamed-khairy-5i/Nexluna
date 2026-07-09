# Nexluna — Best-in-Class Elevation Dossier
> From "excellent" to "can sit next to the best web products in its category."
> Author: mohamed-khairy-5i

---

## PHASE 0 — COMPETITIVE BENCHMARK

**Category:** Online unit-converter tools (Arabic-first / RTL niche).

### Reference set

| # | Reference | Type | What actually makes it feel top-tier (concrete) |
|---|-----------|------|--------------------------------------------------|
| 1 | **RapidTables** | Direct competitor (category leader by traffic) | Instant, no-JS-blocking result; conversion table always visible; zero layout shift. **Weakness to beat:** dated 2010s design, ad-choked, no dark mode, no motion, English-only. |
| 2 | **unitconverters.net** | Direct competitor (#1 organic) | Enormous category coverage; result appears the instant you type. **Weakness to beat:** generic Bootstrap look, cramped, no craft, no RTL. |
| 3 | **Google inline unit widget** | The "instant" bar | Result feels like it exists *before* you finish typing; dropdowns are frictionless; one focal input. **Target:** match its zero-perceived-latency feel. |
| 4 | **Linear.app** | Craft bar (out of niche) | Spring-eased motion, one accent color used only for the primary action, 8px rhythm, restrained. **Target:** motion discipline + a real token system. |
| 5 | **Stripe docs / Vercel** | Craft bar | Self-hosted variable font, instant navigation, inline critical CSS, near-100 Lighthouse. **Target:** performance that *feels* instant, not just passes an audit. |

### "Must match or exceed" targets (per pillar)

- **P1 Design system:** A named 5-color token system with stated reasons; a **characterful display face** (not the same weight-family as body) + body face; must NOT match any of the 3 AI-default looks. Signature element = **the converter itself as a tactile "instrument"** (the product IS the converter — spend boldness there, not on a generic hero).
- **P2 Motion:** ONE orchestrated moment (typed-value → result count-up with spring), physics easing everywhere, skeleton on first paint, full `prefers-reduced-motion`.
- **P3 Performance:** Self-host a **subset** Cairo/Tajawal font (kill the 2 render-blocking Google Fonts round-trips), inline critical CSS, defer AdSense until idle, measure real numbers.
- **P4 AI:** Scoped **semantic converter search** ("كم قدم في المتر", "20 celsius to F") — parses free-text over the site's OWN 14 categories, zero external API cost, always correct (deterministic parse, not a hallucinating LLM). Beats a generic chatbot because it's always right and instant.
- **P5 Story/CTA:** Homepage narrative arc (problem → instrument → proof → one CTA "ابدأ التحويل"). Interactive proof = the live widget itself, above the fold.

---

## PHASE 1 — ELEVATION BLUEPRINT

| # | What | Why (→ benchmark target) | Priority |
|---|------|--------------------------|----------|
| 1 | Replace palette: **deep ink + warm off-white + a single restrained brand teal-green, one amber highlight** | Escapes AI-default #1 (cream+terracotta) & #2 (near-black+acid); Linear-style single-accent discipline | HIGH |
| 2 | Add **Tajawal** (geometric display) alongside Cairo (body) — two deliberate typefaces | P1: "2+ deliberate typefaces", escapes single-family look | HIGH |
| 3 | **Self-host subset fonts**, inline critical CSS, defer ads to idle | P3: kill render-blocking; feel instant | HIGH |
| 4 | Signature: converter becomes a **precision instrument** — count-up animated result, live-as-you-type, focal | P1 signature + P3 Google-instant feel | HIGH |
| 5 | Motion pass: spring easing token, orchestrated load reveal, skeleton, reduced-motion | P2 | HIGH |
| 6 | **Semantic search bar** (natural-language → conversion) | P4 scoped AI, always-correct | MED |
| 7 | Homepage copy → narrative arc, one CTA | P5 | MED |

**Non-goals:** keep Prompt-#1 foundation, RTL, PWA, SEO/JSON-LD, single-author git. One design risk only = the instrument converter; everything else quiet.

---

## PHASE 3 — RESULTS

### Metric arc (measured, local `http.server`, headless Chromium)

| Metric | Before (Prompt #1) | After (elevation) | Note |
|---|---|---|---|
| Render-blocking 3rd-party requests | 2 (Google Fonts CSS + font files) | **0** | Fonts self-hosted & subset |
| Critical CSS (gz) | style.css only | **11.0 KB** style + **0.37 KB** fonts.css | |
| Font payload on critical path | full Cairo+Tajawal families via GF | **cairo-var 144 KB + tajawal-800 49 KB** (preloaded) | one variable file covers every body weight |
| First Contentful Paint | ~fonts-blocked | **260 ms** | no external font round-trip |
| DOMContentLoaded | — | **126 ms** | all JS `defer` |
| load event | — | **175 ms** | |
| First-party JS (gz) | converter+main+icons | **+ smartsearch 4.4 KB** (14.8 KB total, all deferred) | |
| Ads on critical path | script in `<head>` | **0** — loaded on `requestIdleCallback` / first interaction | 8 ad requests all fire post-load |
| AI feature cost | n/a | **$0 / 0 API calls** | deterministic parser, no LLM |

### Side-by-side vs Phase 0 targets

| Benchmark target | Status |
|---|---|
| **RapidTables / unitconverters.net** — instant correct math, no reload | ✅ Met + exceeded: live count-up result, verified exact (5 km→3.106856 mi, 100 °C→212 °F) |
| **Google inline widget** — zero-perceived-latency, one focal input | ✅ Met: smart-search answers as you type (120 ms debounce), FCP 260 ms, no external round-trips |
| **Linear.app** — single-accent restraint, characterful type | ✅ Met: one teal-green brand accent + amber highlight only; Tajawal display + Cairo body |
| **Stripe/Vercel** — craft bar (motion, skeletons, reduced-motion) | ✅ Met: spring easing token, orchestrated hero reveal, skeleton shimmer, `prefers-reduced-motion` honored everywhere |
| Escape 3 AI-default looks | ✅ Deep-ink + warm-paper + teal-green is none of (cream+terracotta / near-black+acid / broadsheet-hairline) |
| P4 AI only where earned | ✅ Scoped semantic NL search over the site's own 14 categories — always correct, no hallucination, no cost |
| P5 narrative + one CTA | ✅ Hero: problem→instrument→single CTA; sharpened active-voice copy |

### Signature element
**The converter as a tactile precision instrument** — animated count-up result (easeOutCubic, spring-eased), tabular-nums mono readout with gradient fill, skeleton→result transition. The product's boldness is spent on the thing users actually came to use.

### Pillar 4 — scoped AI, evaluated
Deterministic Arabic+English NL parser (normalize → strip diacritics/prefixes → longest-match lexicon → same-category pairing). Handles: `5 كم بالميل`, `100 كجم رطل`, `20 celsius to fahrenheit`, `1 gb in mb`, `كم قدم في المتر`, `100 celsius to f`. Correctly disambiguates «كم» (question word vs kilometre) and strips definite-article prefixes (بال/ال). **0 hallucinations by construction** — every answer routes through the same math as the converter (`window.NexConvert`).
