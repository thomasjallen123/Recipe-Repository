# backend/seed_from_scraper.py
import json
from datetime import datetime
from pathlib import Path
import os

from app import create_app, db
from app.models import Recipe, Ingredient, Instruction

app = create_app()

# FIXED: Render clones to /app/backend → output folder is at /app/output
SCRAPER_OUTPUT_DIR = Path("/opt/render/project/src/output")
SCRAPER_OUTPUT_DIR.mkdir(exist_ok=True)

def get_scraped_json_files():
    if not SCRAPER_OUTPUT_DIR.exists():
        print(f"Directory not found: {SCRAPER_OUTPUT_DIR} — creating it")
        SCRAPER_OUTPUT_DIR.mkdir(exist_ok=True)
        return []
    return list(SCRAPER_OUTPUT_DIR.glob("*.json"))

def load_recipe_from_json(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract real difficulty
        raw_diff = (
            data.get("difficulty") or
            data.get("level") or
            data.get("cook_time_complexity") or
            data.get("recipeDifficulty") or
            data.get("difficulty_level") or
            data.get("difficultyLevel")
        )
        difficulty = None
        if raw_diff and isinstance(raw_diff, str):
            diff_lower = raw_diff.lower()
            if any(x in diff_lower for x in ["easy", "simple", "beginner"]):
                difficulty = "Easy"
            elif any(x in diff_lower for x in ["hard", "advanced", "difficult", "expert"]):
                difficulty = "Hard"
            else:
                difficulty = "Medium"

        return {
            "title": data.get("title", "Unknown Title"),
            "source_url": data.get("url") or data.get("source_url"),
            "source_website": data.get("source", Path(json_path).stem.split("_")[0]),
            "image_url": data.get("image"),
            "prep_time_minutes": data.get("prep_time"),
            "cook_time_minutes": data.get("cook_time"),
            "total_time_minutes": data.get("total_time"),
            "servings": data.get("servings") or data.get("yield"),
            "difficulty": difficulty,
            "cuisine": data.get("cuisine"),
            "ingredients": data.get("ingredients", []),
            "instructions": data.get("instructions", []),
            "scraped_at": datetime.utcnow(),  # ← FIXED: works everywhere
        }
    except Exception as e:
        print(f"Failed to load {json_path}: {e}")
        return None

def recipe_exists(url):
    if not url:
        return True
    return db.session.query(Recipe.query.filter_by(source_url=url).exists()).scalar()

def seed_all_recipes():
    json_files = get_scraped_json_files()
    print(f"Found {len(json_files)} scraped recipe files in {SCRAPER_OUTPUT_DIR}")

    added = skipped = 0

    with app.app_context():
        for json_path in json_files:
            recipe_data = load_recipe_from_json(json_path)
            if not recipe_data or not recipe_data.get("title") or not recipe_data.get("source_url"):
                skipped += 1
                continue

            if recipe_exists(recipe_data["source_url"]):
                skipped += 1
                continue

            try:
                recipe = Recipe(
                    title=recipe_data["title"],
                    source_url=recipe_data["source_url"],
                    source_website=recipe_data["source_website"],
                    image_url=recipe_data["image_url"],
                    prep_time_minutes=recipe_data["prep_time_minutes"],
                    cook_time_minutes=recipe_data["cook_time_minutes"],
                    total_time_minutes=recipe_data["total_time_minutes"],
                    servings=recipe_data["servings"],
                    difficulty=recipe_data["difficulty"],
                    cuisine=recipe_data["cuisine"],
                    created_at=datetime.utcnow(),  # ← FIXED
                    scraped_at=recipe_data["scraped_at"],
                )
                db.session.add(recipe)
                db.session.flush()

                # Ingredients
                for ing in recipe_data["ingredients"]:
                    name = quantity = unit = None
                    if isinstance(ing, dict):
                        name = ing.get("name") or ing.get("ingredient")
                        quantity = ing.get("quantity") or ing.get("amount")
                        unit = ing.get("unit")
                    elif isinstance(ing, (list, tuple)) and len(ing) >= 1:
                        name = ing[0]
                        quantity = ing[1] if len(ing) > 1 else None
                        unit = ing[2] if len(ing) > 2 else None
                    if name:
                        db.session.add(Ingredient(
                            recipe_id=recipe.id,
                            name=str(name).strip(),
                            quantity=str(quantity).strip() if quantity else None,
                            unit=str(unit).strip() if unit else None,
                        ))

                # Instructions
                instructions = recipe_data["instructions"]
                if isinstance(instructions, str):
                    instructions = [line.strip() for line in instructions.split('\n') if line.strip()]
                for i, text in enumerate(instructions, 1):
                    if isinstance(text, dict):
                        text = text.get("text") or text.get("step") or ""
                    if text:
                        db.session.add(Instruction(
                            recipe_id=recipe.id,
                            step_number=i,
                            step_text=str(text).strip()
                        ))

                db.session.commit()
                added += 1
                print(f"Added: {recipe.title}")

            except Exception as e:
                db.session.rollback()
                print(f"Failed: {recipe_data.get('title', 'Unknown')}: {e}")
                skipped += 1

    print(f"\nSeeding complete! Added: {added} | Skipped: {skipped}")

if __name__ == "__main__":
    print("Starting perfect import...")
    seed_all_recipes()