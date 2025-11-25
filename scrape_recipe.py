from recipe_scrapers import scrape_me
import json
from pathlib import Path

def scrape_recipe(url: str):
    scraper = scrape_me(url)
    data = {
        "title": scraper.title(),
        "host": scraper.host(),
        "image": scraper.image(),
        "ingredients": scraper.ingredients(),
        "instructions": scraper.instructions(),
        "yields": scraper.yields(),
        "total_time": scraper.total_time(),
    }
    return data

if __name__ == "__main__":
    url = input("Enter a recipe URL: ").strip()
    recipe = scrape_recipe(url)

    # Create output directory
    Path("output").mkdir(exist_ok=True)

    # Save to JSON
    safe_title = recipe["title"].replace(" ", "_").replace("/", "_")
    out_file = Path("output") / f"{safe_title}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(recipe, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Recipe saved to: {out_file}")
    print(f"📘 Title: {recipe['title']}")
    print(f"📜 Ingredients: {len(recipe['ingredients'])} items")
