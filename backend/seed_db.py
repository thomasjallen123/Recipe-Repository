from datetime import datetime

from app import create_app
from app import db
from app.models import Recipe, Ingredient, Instruction


def seed():
    """Drop all tables, recreate them, and insert one example recipe."""
    app = create_app()
    with app.app_context():
        #This wipes old data. OK right now since your DB is basically empty.
        db.drop_all()
        db.create_all()

        # --- Example recipe: Simple Pancakes ---
        pancakes = Recipe(
            title="Simple Pancakes",
            source_url="https://example.com/pancakes",
            source_website="Demo",
            prep_time_minutes=10,
            cook_time_minutes=15,
            total_time_minutes=25,
            servings=4,
            difficulty="Easy",
            cuisine="American",
            image_url=None,
            created_at=datetime.utcnow(),
            scraped_at=datetime.utcnow(),
        )
        db.session.add(pancakes)
        db.session.flush()  # so pancakes.id is available

        ingredients = [
            ("Flour", "1", "cup"),
            ("Milk", "1", "cup"),
            ("Egg", "1", None),
            ("Sugar", "2", "tbsp"),
            ("Baking powder", "2", "tsp"),
        ]
        for name, qty, unit in ingredients:
            db.session.add(
                Ingredient(
                    recipe_id=pancakes.id,
                    name=name,
                    quantity=qty,
                    unit=unit,
                )
            )

        steps = [
            "Whisk dry ingredients in a bowl.",
            "Add milk and egg; mix until smooth.",
            "Cook batter on a greased pan until golden on both sides.",
        ]
        for i, text in enumerate(steps, start=1):
            db.session.add(
                Instruction(
                    recipe_id=pancakes.id,
                    step_number=i,
                    step_text=text,
                )
            )

        db.session.commit()
        print("Database seeded with example pancake recipe.")


if __name__ == "__main__":
    seed()
