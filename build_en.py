"""Generate the first complete English locale under /en/.

The converter math is never duplicated here: pages consume the same generated
NexlunaUnits payload as the Arabic site and only swap presentation/content.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "units.json").read_text(encoding="utf-8"))
EN = json.loads((ROOT / "data" / "i18n" / "en.json").read_text(encoding="utf-8"))
UI = EN["ui"]
CATS = EN["categories"]
ORDER = list(DATA.keys())


def esc(value):
    return html.escape(str(value), quote=True)


def scripts(include_search=False):
    extra = '\n  <script src="/assets/js/smartsearch.js" defer></script>' if include_search else ''
    return f'''  <script src="/assets/js/icons.js?v=6" defer></script>
  <script src="/assets/js/units.generated.js?v=6" defer></script>
  <script src="/assets/js/locale.en.generated.js?v=6" defer></script>
  <script src="/assets/js/explain.js?v=6" defer></script>
  <script src="/assets/js/webmcp.js?v=6" defer></script>
  <script src="/assets/js/converter.js?v=6" defer></script>{extra}
  <script src="/assets/js/main.js?v=6" defer></script>'''


def header():
    return f'''  <header class="site-header">
    <div class="container nav">
      <a class="brand" href="/en/" aria-label="Nexluna — home"><img class="brand-logo" src="/assets/img/logo.svg" width="36" height="36" alt=""><span>Nexluna</span></a>
      <nav class="nav-links" aria-label="Main navigation">
        <a href="/en/">{UI['home']}</a>
        <a href="/en/converters/length.html">{UI['length']}</a>
        <a href="/en/converters/weight.html">{UI['weight']}</a>
        <a href="/en/converters/temperature.html">{UI['temperature']}</a>
        <a href="/en/converters/data.html">{UI['data']}</a>
        <a href="/en/blog/">{UI['blog']}</a>
        <a href="/">{UI['language_switch']}</a>
      </nav>
      <div class="nav-actions"><button class="icon-btn" data-theme-toggle type="button" aria-label="{UI['theme']}"><span data-icon="moon"></span></button><button class="icon-btn nav-toggle" type="button" aria-label="{UI['menu']}" aria-expanded="false"><span data-icon="menu"></span></button></div>
    </div>
  </header>'''


def footer():
    return f'''  <footer class="site-footer"><div class="container"><div class="footer-grid">
      <div><a class="brand" href="/en/" style="margin-bottom:var(--sp-3)"><img class="brand-logo" src="/assets/img/logo.svg" width="36" height="36" alt=""><span>Nexluna</span></a><p style="color:var(--text-muted);font-size:var(--step--1);max-width:38ch">{UI['footer_blurb']}</p><div class="footer-badges" style="display:flex;gap:var(--sp-2);margin-top:var(--sp-3);flex-wrap:wrap"><span class="chip"><span data-icon="offline"></span> {UI['offline']}</span><span class="chip"><span data-icon="shield"></span> {UI['privacy']}</span></div></div>
      <div><h2 class="footer-heading">{UI['footer_categories']}</h2><a href="/en/converters/length.html">{UI['length']}</a><a href="/en/converters/weight.html">{UI['weight']}</a><a href="/en/converters/area.html">{CATS['area']['label']}</a><a href="/en/converters/temperature.html">{UI['temperature']}</a><a href="/en/converters/volume.html">{CATS['volume']['label']}</a><a href="/en/converters/data.html">{UI['data']}</a></div>
      <div><h2 class="footer-heading">{UI['footer_more']}</h2><a href="/en/converters/speed.html">{CATS['speed']['label']}</a><a href="/en/converters/time.html">{CATS['time']['label']}</a><a href="/en/converters/pressure.html">{CATS['pressure']['label']}</a><a href="/en/converters/energy.html">{CATS['energy']['label']}</a><a href="/en/converters/power.html">{CATS['power']['label']}</a><a href="/en/converters/fuel.html">{CATS['fuel']['label']}</a></div>
      <div><h2 class="footer-heading">{UI['footer_links']}</h2><a href="/en/converters/">{UI['quick_conversions']}</a><a href="/en/blog/">{UI['blog']}</a><a href="/en/about.html">{UI['about']}</a><a href="/en/privacy.html">{UI['privacy']}</a><a href="/en/contact.html">{UI['contact']}</a></div>
    </div><div class="footer-bottom">© <span data-year>2026</span> Nexluna — {UI['copyright']}</div></div></footer>'''


def shell(title, description, body, include_search=False, canonical="/en/", ar_path="/"):
    return f'''<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="theme-color" content="#0b1220"><link rel="canonical" href="https://nexluna.netlify.app{canonical}"><link rel="alternate" hreflang="ar" href="https://nexluna.netlify.app{ar_path}"><link rel="alternate" hreflang="en" href="https://nexluna.netlify.app{canonical}"><link rel="alternate" hreflang="x-default" href="https://nexluna.netlify.app/"><link rel="manifest" href="/manifest.webmanifest"><link rel="stylesheet" href="/assets/css/style.css"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'self'; form-action 'self'; script-src 'self' 'unsafe-inline'; connect-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; worker-src 'self'; manifest-src 'self'"><script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"Nexluna","url":"https://nexluna.netlify.app{canonical}","inLanguage":"en","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","description":{json.dumps(description)}}}</script></head><body>{header()}<main id="main-content">{body}</main>{footer()}{scripts(include_search)}</body></html>'''


def home():
    cards = ''.join(f'<a class="category-card" href="/en/converters/{cat}.html"><span class="cat-icon">{DATA[cat].get("icon", "")}</span><strong>{esc(CATS[cat]["label"])}</strong><span>{esc(CATS[cat]["intro"][:100])}...</span></a>' for cat in ORDER)
    body = f'''<section class="hero hero-redesign"><div class="container hero-grid"><div class="hero-copy"><p class="eyebrow">{UI['hero_eyebrow']}</p><h1>{UI['hero_title_1']}<br><span>{UI['hero_title_2']}</span></h1><p class="hero-lead">{UI['hero_lead']}</p><div class="hero-actions"><a class="btn btn-primary" href="#converter">{UI['start']} <span data-icon="arrow"></span></a><a class="btn btn-ghost" href="/en/about.html">{UI['about']}</a></div><div class="hero-pills"><span>{UI['instant']}</span><span>{UI['deterministic']}</span><span>{UI['offline']}</span></div></div><div class="hero-measure-card"><div class="measure-orbit"></div><span class="measure-label">{UI['deterministic']}</span><strong>100+</strong><span>{UI['coverage_a']}</span><div class="measure-mini"><span>km</span><b>→</b><span>mi</span></div></div></div></section>
    <section class="section" id="converter"><div class="container"><div id="smart-search"></div><div id="converter-app" class="converter-shell" data-locale="en"></div></div></section>
    <section class="section section-muted"><div class="container"><p class="eyebrow">{UI['categories_kicker']}</p><h2>{UI['categories_title']}</h2><p class="section-lead">{UI['categories_lead']}</p><div class="category-grid">{cards}</div></div></section>
    <section class="section"><div class="container"><p class="eyebrow">{UI['features_kicker']}</p><h2>{UI['features_title']}</h2><p class="section-lead">{UI['features_lead']}</p><div class="feature-grid"><article><h3>{UI['feature_instant']}</h3><p>{UI['feature_instant_desc']}</p></article><article><h3>{UI['feature_offline']}</h3><p>{UI['feature_offline_desc']}</p></article><article><h3>{UI['feature_copy']}</h3><p>{UI['feature_copy_desc']}</p></article><article><h3>{UI['feature_privacy']}</h3><p>{UI['feature_privacy_desc']}</p></article></div></div></section>'''
    return shell(UI['site_title'], UI['site_description'], body, True, "/en/", ar_path="/")


def converter(cat):
    meta = CATS[cat]
    cards = ''.join(f'<a class="related-card" href="/en/converters/{other}.html">{esc(CATS[other]["label"])} <span data-icon="arrow"></span></a>' for other in ORDER if other != cat and len([x for x in ORDER if x != cat]) > 0)[:800]
    body = f'''<section class="category-hero"><div class="container"><p class="eyebrow">{UI['converter_eyebrow'].format(name=meta['label'])}</p><h1>{UI['converter_headline'].format(name=meta['label'])}</h1><p class="hero-lead">{esc(meta['intro'])}</p><div class="hero-pills">{''.join('<span>'+esc(p)+'</span>' for p in UI['converter_pills'])}</div></div></section><section class="section"><div class="container"><div id="converter-app" class="converter-shell" data-only="{cat}" data-locale="en"></div><div class="content-panel"><h2>{UI['formulas']}</h2><p>{'<br>'.join(esc(x) for x in meta['formulas'])}</p><h2>{UI['common']}</h2><ul>{''.join('<li>'+esc(x)+'</li>' for x in meta['common'])}</ul></div></div></section><section class="section section-muted"><div class="container"><p class="eyebrow">{UI['related']}</p><h2>{UI['related_title']}</h2><div class="related-grid">{cards}</div></div></section>'''
    return shell(meta['title'], meta['description'], body, False, f"/en/converters/{cat}.html", ar_path=f"/converters/{cat}.html")


def index():
    cards = ''.join(f'<a class="category-card" href="/en/converters/{cat}.html"><strong>{esc(CATS[cat]["label"])}</strong><span>{esc(CATS[cat]["description"])}</span></a>' for cat in ORDER)
    body = f'<section class="section"><div class="container"><p class="eyebrow">{UI["categories_kicker"]}</p><h1>{UI["categories_title"]}</h1><p class="section-lead">{UI["categories_lead"]}</p><div class="category-grid">{cards}</div></div></section>'
    return shell(UI['categories_title'] + ' | Nexluna', UI['categories_lead'], body, False, "/en/converters/", ar_path="/converters/")


def main():
    out = ROOT / "en"
    (out / "converters").mkdir(parents=True, exist_ok=True)
    (out / "converters" / "index.html").write_text(index(), encoding="utf-8")
    (out / "index.html").write_text(home(), encoding="utf-8")
    for cat in ORDER:
        (out / "converters" / f"{cat}.html").write_text(converter(cat), encoding="utf-8")
    print(f"generated English home, index, and {len(ORDER)} converter pages")


if __name__ == "__main__":
    main()
