#!/usr/bin/env python3
import argparse, csv, logging, time
from pathlib import Path

# Import scrapers regardless of whether files are in the same folder or in scraper/
try:
    from scrape_recipe import scrape_recipe
    from scrape_foodnetwork import scrape_one as scrape_foodnetwork
    from card_utils import write_outputs
except ImportError:
    from scraper.scrape_recipe import scrape_recipe
    from scraper.scrape_foodnetwork import scrape_one as scrape_foodnetwork
    from scraper.card_utils import write_outputs

def iter_urls(path: Path):
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        yield line

def run(domain: str, infile: Path, outdir: Path, sleep: float, limit: int | None):
    outdir.mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename="logs/scraper.log", level=logging.INFO)

    failures_path = outdir / "failures.csv"
    fcsv = failures_path.open("w", newline="", encoding="utf-8")
    writer = csv.writer(fcsv)
    writer.writerow(["url", "error"])

    ok = fail = 0
    for i, url in enumerate(iter_urls(infile), start=1):
        if limit and i > limit:
            break
        try:
            if domain.lower() == "foodnetwork":
                card = scrape_foodnetwork(url, outdir, sleep=0)  # FN function writes files itself
            else:
                # AllRecipes (generic) path:
                card = scrape_recipe(url)                        # returns dict
                write_outputs(card, outdir)                      # write JSON + MD

            ok += 1
            print(f"[{ok}] ✔ {card['title']}")
        except Exception as e:
            fail += 1
            writer.writerow([url, str(e)])
            logging.exception(f"[{domain}] Failed: {url}")
            print(f"[{i}] ✗ {url} — {e}")
        time.sleep(sleep)  # polite delay

    fcsv.close()
    print(f"\nDone. OK={ok} FAIL={fail} • Failures file: {failures_path if fail else 'none'}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Batch scrape recipes")
    ap.add_argument("--domain", choices=["allrecipes", "foodnetwork"], required=True)
    ap.add_argument("--infile", required=True, help="Text file with one URL per line")
    ap.add_argument("--outdir", required=True, help="Output directory")
    ap.add_argument("--sleep", type=float, default=1.5, help="Delay between URLs (sec)")
    ap.add_argument("--limit", type=int, default=0, help="Stop after N URLs (0 = all)")
    args = ap.parse_args()

    run(
        domain=args.domain,
        infile=Path(args.infile),
        outdir=Path(args.outdir),
        sleep=args.sleep,
        limit=args.limit if args.limit > 0 else None,
    )
