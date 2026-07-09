#!/usr/bin/env python3
"""Generate sitemap.xml from the known page set."""
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


def build():
    body = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pr, cf in urls:
        body.append("  <url>")
        body.append("    <loc>%s%s</loc>" % (BASE, loc))
        body.append("    <lastmod>%s</lastmod>" % TODAY)
        body.append("    <changefreq>%s</changefreq>" % cf)
        body.append("    <priority>%s</priority>" % pr)
        body.append("  </url>")
    body.append("</urlset>\n")
    with open(os.path.join(os.path.dirname(__file__), "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(body))
    print("wrote sitemap.xml (%d urls)" % len(urls))


if __name__ == "__main__":
    build()
