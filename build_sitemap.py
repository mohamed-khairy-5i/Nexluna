#!/usr/bin/env python3
"""Generate sitemap.xml from the known page set.

Arabic pages that have an /en/ counterpart carry xhtml:link hreflang
alternates (ar/en/x-default), and the /en/ pages are listed as their own
URLs with reciprocal alternates.
"""
import os
from datetime import date
from build_pages import BASE, ORDER
from build_blog import ARTICLES
from build_pairs import PAIRS, slug

TODAY = date.today().isoformat()

# (loc, priority, changefreq)
urls = [("/", "1.0", "weekly")]
for c in ORDER:
    urls.append(("/converters/%s.html" % c, "0.9", "monthly"))
# Conversion-pair landing pages (Roadmap 1.1)
urls.append(("/convert/", "0.7", "weekly"))
for cat, frm, to in PAIRS:
    urls.append(("/convert/%s.html" % slug(cat, frm, to), "0.8", "monthly"))
urls.append(("/blog/", "0.7", "weekly"))
for a in ARTICLES:
    urls.append(("/blog/%s.html" % a["slug"], "0.6", "monthly"))
for p in ("/about.html", "/contact.html", "/privacy.html"):
    urls.append((p, "0.4", "yearly"))

# English section (hreflang counterparts)
en_urls = [("/en/", "/", "1.0", "weekly")]
for c in ORDER:
    en_urls.append(("/en/converters/%s.html" % c, "/converters/%s.html" % c, "0.9", "monthly"))
en_map = {ar: en for en, ar, _, _ in en_urls}

NS_SM = "http://www.sitemaps.org/schemas/sitemap/0.9"
NS_XH = "http://www.w3.org/1999/xhtml"


def alt_links(ar_loc, en_loc):
    return [
        ('{%s}link' % NS_XH, {"rel": "alternate", "hreflang": "ar", "href": "%s%s" % (BASE, ar_loc)}),
        ('{%s}link' % NS_XH, {"rel": "alternate", "hreflang": "en", "href": "%s%s" % (BASE, en_loc)}),
        ('{%s}link' % NS_XH, {"rel": "alternate", "hreflang": "x-default", "href": "%s%s" % (BASE, ar_loc)}),
    ]


def build():
    import xml.etree.ElementTree as ET
    ET.register_namespace("", NS_SM)
    ET.register_namespace("xhtml", NS_XH)
    root = ET.Element("{%s}urlset" % NS_SM)

    def add(loc, pr, cf, alts=()):
        u = ET.SubElement(root, "{%s}url" % NS_SM)
        ET.SubElement(u, "{%s}loc" % NS_SM).text = "%s%s" % (BASE, loc)
        ET.SubElement(u, "{%s}lastmod" % NS_SM).text = TODAY
        ET.SubElement(u, "{%s}changefreq" % NS_SM).text = cf
        ET.SubElement(u, "{%s}priority" % NS_SM).text = pr
        for tag, attrs in alts:
            ET.SubElement(u, tag, attrs)

    for loc, pr, cf in urls:
        en = en_map.get(loc)
        add(loc, pr, cf, alt_links(loc, en) if en else ())
    for en, ar, pr, cf in en_urls:
        add(en, pr, cf, alt_links(ar, en))

    body = ET.tostring(root, encoding="unicode")
    body = '<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n"
    total = len(urls) + len(en_urls)
    with open(os.path.join(os.path.dirname(__file__), "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(body)
    print("wrote sitemap.xml (%d urls)" % total)


if __name__ == "__main__":
    build()
