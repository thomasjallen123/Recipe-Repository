#!/usr/bin/env python3
import argparse, logging, time
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from recipe_scrapers import scrape_html
from card_utils import normalize, write_outputs

# ---- HTTP client with realistic headers + retries ----
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}

def _requests_session():
    s = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.6,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    s.mount("https://", HTTPAdapter(max_retries=retries))
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.headers.update(HEADERS)
    return s

def fetch_html_requests(url: str) -> tuple[str, str, int]:
    """Return (html, final_url, status_code) using requests."""
    s = _requests_session()
    r = s.get(url, timeout=20, allow_redirects=True)
    return r.text, str(r.url), r.status_code

def fetch_html_playwright(url: str) -> tuple[str, str]:
    """Use Playwright when requests gets blocked (403)."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            user_agent=HEADERS["User-Agent"],
            locale="en-US",
        )
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=30000)
        html = page.content()
        final_url = page.url
        ctx.close(); browser.close()
    return html, final_url

def scrape_one(url: str, outdir: Path, sleep: float = 1.5):
    if "foodnetwork.com" not in urlparse(url).netloc:
        raise ValueError("This prototype only accepts foodnetwork.com URLs")

    # 1) Try requests first
    html, final_url, status = fetch_html_requests(url)

    # 2) If blocked, fallback to Playwright
    if status in (401, 403, 406):
        logging.info(f"Requests blocked ({status}) → using Playwright: {url}")
        html, final_url = fetch_html_playwright(url)

    # Parse with recipe_scrapers
    scraper = scrape_html(html=html, org_url=final_url)
    card = normalize(scraper)

    if not card.get("ingredients") or not card.get("steps"):
        raise RuntimeError("Parsed recipe has no ingredients or steps")

    write_outputs(card, outdir)
    time.sleep(sleep)
    return card

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Food Network scraper with 403 fallback")
    ap.add_argument("url")
    ap.add_argument("--outdir", default="output/foodnetwork")
    ap.add_argument("--sleep", type=float, default=1.5)
    args = ap.parse_args()

    Path(args.outdir).mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename="logs/scraper.log", level=logging.INFO)

    try:
        card = scrape_one(args.url, Path(args.outdir), args.sleep)
        print(f"✅ Saved → {args.outdir}\n📘 {card['title']}")
        print(f"📜 Ingredients: {len(card['ingredients'])} • 🧭 Steps: {len(card['steps'])}")
    except Exception as e:
        logging.exception(f"Failed on URL: {args.url}")
        print(f"❌ Error: {e}")
        raise SystemExit(1)
