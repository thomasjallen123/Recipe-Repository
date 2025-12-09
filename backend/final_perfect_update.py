from app import create_app, db
from app.models import Recipe
from tqdm import tqdm

app = create_app()

with app.app_context():
    recipes = Recipe.query.all()
    print(f"Final polish on {len(recipes)} recipes...\n")

    for r in tqdm(recipes, desc="Polishing"):
        updated = False

        # Only set cuisine if missing
        if not r.cuisine:
            text = (r.title + " " + (r.source_url or "")).lower()
            cuisine_map = {
                "Italian": ["italian", "pasta", "pizza", "risotto", "bolognese", "carbonara", "parmigiana", "lasagna"],
                "Mexican": ["mexican", "taco", "enchilada", "burrito", "fajita", "mole"],
                "Indian": ["indian", "curry", "tikka", "masala", "biryani", "naan"],
                "Chinese": ["chinese", "stir fry", "fried rice", "dumpling", "lo mein"],
                "Japanese": ["japanese", "sushi", "teriyaki", "ramen", "tempura"],
                "Thai": ["thai", "pad thai", "tom yum", "green curry"],
                "Korean": ["korean", "bibimbap", "kimchi", "bulgogi"],
            }
            for name, keywords in cuisine_map.items():
                if any(kw in text for kw in keywords):
                    r.cuisine = name
                    updated = True
                    break
            if not r.cuisine:
                r.cuisine = "American"
                updated = True

        # Only set time if missing
        if not r.total_time_minutes or r.total_time_minutes <= 0:
            r.total_time_minutes = 45
            r.prep_time_minutes = 10
            r.cook_time_minutes = 35
            updated = True

        # ONLY set difficulty if scraper didn't provide one
        if not r.difficulty or r.difficulty in ["N/A", None]:
            time = r.total_time_minutes or 0
            if time <= 25:
                r.difficulty = "Easy"
            elif time >= 120:
                r.difficulty = "Hard"
            else:
                r.difficulty = "Medium"
            updated = True

        if updated:
            db.session.commit()

    print("\nPERFECTION ACHIEVED")
    