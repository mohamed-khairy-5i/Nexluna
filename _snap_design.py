#!/usr/bin/env python3
"""Capture design-review screenshots for visual verification."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path("/home/ubuntu/Nexluna/.review_shots")
OUT.mkdir(exist_ok=True)
BASE = "http://127.0.0.1:8766"

PAGES = [
    ("/", "home_ar"),
    ("/converters/length.html", "converter_length_ar"),
    ("/en/", "home_en"),
    ("/en/converters/length.html", "converter_length_en"),
]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1360, "height": 900})
        for url, name in PAGES:
            await page.goto(BASE + url, wait_until="networkidle")
            await page.wait_for_timeout(1200)
            await page.screenshot(path=str(OUT / f"{name}_desktop.png"), full_page=False)
            await page.set_viewport_size({"width": 390, "height": 844})
            await page.wait_for_timeout(400)
            await page.screenshot(path=str(OUT / f"{name}_mobile.png"), full_page=False)
            await page.set_viewport_size({"width": 1360, "height": 900})
        await browser.close()
        print("captured:", list(OUT.glob("*.png")))


asyncio.run(main())
