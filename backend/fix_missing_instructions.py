# backend/fix_missing_instructions.py
from app import create_app, db
from app.models import Recipe, Instruction
from recipe_scrapers import scrape_me
from tqdm import tqdm
import time

app = create_app()

with app.app_context():
    recipes = Recipe.query.all()
    print(f"Fixing instructions for {len(recipes)} recipes...")

    for recipe in tqdm(recipes):
        if not recipe.source_url or "foodnetwork.com" not in recipe.source_url:
            continue

        try:
            scraper = scrape_me(recipe.source_url)
            instructions = scraper.instructions()

            # Delete old (empty) instructions
            Instruction.query.filter_by(recipe_id=recipe.id).delete()

            # Save new ones
            for i, step in enumerate(instructions.split("\n"), 1):
                step = step.strip()
                if step and len(step) > 5:  # ignore junk
                    db.session.add(Instruction(
                        recipe_id=recipe.id,
                        step_number=i,
                        step_text=step
                    ))
            db.session.commit()
            print(f"Fixed: {recipe.title}")
            time.sleep(1)  # be nice to Food Network
        except Exception as e:
            print(f"Failed {recipe.title}: {e}")
            db.session.rollback()

    print("INSTRUCTIONS FIXED FOREVER")