# Recipe-Repository
Capstone MVP: Recipe scraper + app

# 🍳 Recipe Repository – Scraper Module

**Capstone:** CMSC 495 — Recipe Repository MVP  
**Role:** Data Engineer (Web Scraper)

This module scrapes recipes from **AllRecipes** and **Food Network**, 
normalizes data to a shared schema, writes JSON/Markdown “recipe cards,” 
and (optionally) loads them into a local SQLite DB for backend testing.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install

# AllRecipes
python scrape_recipe.py "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"

# Food Network (auto-fallback to Playwright on 403)
python scrape_foodnetwork.py "https://www.foodnetwork.com/recipes/food-network-kitchen/spicy-chicken-tortilla-chip-casserole-3676584"

#Batch
python run_batch.py --domain allrecipes \
  --infile scraper/seed_allrecipes.txt \
  --outdir output/allrecipes \
  --sleep 2 --limit 5

python run_batch.py --domain foodnetwork \
  --infile scraper/seed_foodnetwork.txt \
  --outdir output/foodnetwork \
  --sleep 2 --limit 5

#Outputs
output/<domain>/*.json
output/<domain>/*.md

#Logs & Failures
logs/scraper.log
output/<domain>/failures.csv


#Notes

Keep --sleep ≥ 1.5–2s to be polite.

Limited to a small set of URLs for the MVP demo.
