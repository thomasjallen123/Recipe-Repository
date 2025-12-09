# backend/fix_cuisines_forever.py — RUN THIS ONCE AND YOU'RE DONE
from app import create_app, db
from app.models import Recipe
from tqdm import tqdm

app = create_app()

with app.app_context():
    recipes = Recipe.query.all()
    print(f"Fixing cuisine capitalization on {len(recipes)} recipes...")

    updated = 0
    for r in tqdm(recipes):
        if not r.cuisine:
            continue

        # THIS IS THE ONLY LINE THAT MATTERS
        new_cuisine = r.cuisine.strip().title()  # "italian" → "Italian", "MEXICAN" → "Mexican", "thai food" → "Thai Food"

        if new_cuisine != r.cuisine:
            r.cuisine = new_cuisine
            updated += 1

    db.session.commit()
    print(f"\nDone! Fixed {updated} cuisines.")
    print("All cuisines are now perfectly Title Case.")
    print("Refresh your app — every card will look perfect.")