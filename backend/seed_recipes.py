from app import create_app, db
from app.models import Recipe, Ingredient, Instruction

app = create_app()

recipes_to_add = [
    {
        "title": "Classic Spaghetti Bolognese",
        "cuisine": "Italian",
        "prep": 15,
        "cook": 45,
        "difficulty": "Easy",
        "servings": 4,
        "url": "https://www.allrecipes.com/recipe/158140/spaghetti-bolognese/",
        "ingredients": [
            ("Ground Beef", "1", "lb"),
            ("Onion", "1", "medium"),
            ("Garlic", "2", "cloves"),
            ("Tomato Sauce", "24", "oz"),
            ("Olive Oil", "2", "tbsp"),
        ],
        "instructions": [
            "Heat oil, sauté onions & garlic.",
            "Add ground beef and cook until browned.",
            "Add tomato sauce and simmer 30 minutes.",
            "Serve over cooked spaghetti."
        ]
    },
    {
        "title": "Chicken Alfredo Pasta",
        "cuisine": "Italian",
        "prep": 10,
        "cook": 20,
        "difficulty": "Easy",
        "servings": 4,
        "url": "https://www.allrecipes.com/recipe/22831/alfredo-sauce/",
        "ingredients": [
            ("Chicken Breast", "2", "pieces"),
            ("Fettuccine Pasta", "12", "oz"),
            ("Butter", "4", "tbsp"),
            ("Heavy Cream", "1", "cup"),
            ("Parmesan Cheese", "1", "cup"),
        ],
        "instructions": [
            "Cook pasta according to package.",
            "Pan-fry chicken until cooked.",
            "Melt butter, add cream, stir in Parmesan.",
            "Mix pasta & chicken into sauce."
        ]
    },
    {
        "title": "Beef Stir Fry",
        "cuisine": "Chinese",
        "prep": 10,
        "cook": 10,
        "difficulty": "Medium",
        "servings": 3,
        "url": "https://www.allrecipes.com/recipe/228823/quick-beef-stir-fry/",
        "ingredients": [
            ("Beef Strips", "1", "lb"),
            ("Bell Pepper", "1", "large"),
            ("Soy Sauce", "3", "tbsp"),
            ("Ginger", "1", "tbsp"),
            ("Vegetable Oil", "2", "tbsp"),
        ],
        "instructions": [
            "Heat oil in a wok.",
            "Stir fry beef until browned.",
            "Add peppers, soy sauce, and ginger.",
            "Cook for 3–4 minutes."
        ]
    },
    {
        "title": "Butter Chicken",
        "cuisine": "Indian",
        "prep": 20,
        "cook": 30,
        "difficulty": "Medium",
        "servings": 4,
        "url": "https://www.allrecipes.com/recipe/45957/chicken-makhani-indian-butter-chicken/",
        "ingredients": [
            ("Chicken Thighs", "1", "lb"),
            ("Butter", "3", "tbsp"),
            ("Tomato Puree", "1", "cup"),
            ("Cream", "1/2", "cup"),
            ("Garam Masala", "1", "tbsp"),
        ],
        "instructions": [
            "Cook chicken with spices.",
            "Add tomato puree and simmer.",
            "Stir in cream and butter.",
            "Serve with rice."
        ]
    },
    {
        "title": "Teriyaki Salmon",
        "cuisine": "Japanese",
        "prep": 5,
        "cook": 15,
        "difficulty": "Easy",
        "servings": 2,
        "url": "https://www.allrecipes.com/recipe/25678/salmon-teriyaki/",
        "ingredients": [
            ("Salmon Fillets", "2", "pieces"),
            ("Soy Sauce", "1/4", "cup"),
            ("Honey", "2", "tbsp"),
            ("Garlic", "1", "clove"),
        ],
        "instructions": [
            "Mix sauce ingredients.",
            "Bake salmon and brush with sauce.",
            "Broil 2 minutes for glaze."
        ]
    },
    {
        "title": "Beef Tacos",
        "cuisine": "Mexican",
        "prep": 10,
        "cook": 10,
        "difficulty": "Easy",
        "servings": 4,
        "url": "https://www.allrecipes.com/recipe/214658/easy-ground-beef-tacos/",
        "ingredients": [
            ("Ground Beef", "1", "lb"),
            ("Taco Seasoning", "1", "packet"),
            ("Tortillas", "8", "pieces"),
            ("Lettuce", "1", "cup"),
        ],
        "instructions": [
            "Brown beef in skillet.",
            "Add seasoning and water.",
            "Toast tortillas.",
            "Assemble tacos."
        ]
    },
    {
        "title": "Pancit Canton (Filipino Stir-Fry Noodles)",
        "cuisine": "Filipino",
        "prep": 10,
        "cook": 15,
        "difficulty": "Easy",
        "servings": 4,
        "url": "https://www.allrecipes.com/recipe/262570/pancit-canton-filipino-stir-fry-noodles/",
        "ingredients": [
            ("Canton Noodles", "8", "oz"),
            ("Chicken", "1/2", "lb"),
            ("Carrots", "1", "cup"),
            ("Soy Sauce", "3", "tbsp"),
        ],
        "instructions": [
            "Sauté chicken and vegetables.",
            "Add noodles and soy sauce.",
            "Stir fry until cooked."
        ]
    },
    {
        "title": "Shrimp Fried Rice",
        "cuisine": "Chinese",
        "prep": 10,
        "cook": 8,
        "difficulty": "Easy",
        "servings": 3,
        "url": "https://www.allrecipes.com/recipe/79543/fried-rice-restaurant-style/",
        "ingredients": [
            ("Shrimp", "1/2", "lb"),
            ("Rice", "3", "cups"),
            ("Eggs", "2", None),
            ("Soy Sauce", "2", "tbsp"),
        ],
        "instructions": [
            "Scramble eggs.",
            "Add shrimp and rice.",
            "Stir in soy sauce.",
            "Cook 3 minutes."
        ]
    },
    {
        "title": "Greek Salad",
        "cuisine": "Greek",
        "prep": 10,
        "cook": 0,
        "difficulty": "Easy",
        "servings": 2,
        "url": "https://www.allrecipes.com/recipe/14447/greek-salad-i/",
        "ingredients": [
            ("Cucumber", "1", None),
            ("Tomatoes", "2", None),
            ("Feta Cheese", "1/2", "cup"),
            ("Olives", "1/4", "cup"),
        ],
        "instructions": [
            "Chop vegetables.",
            "Mix with feta and olives.",
            "Add dressing."
        ]
    },
    {
        "title": "Chocolate Chip Cookies",
        "cuisine": "American",
        "prep": 15,
        "cook": 12,
        "difficulty": "Easy",
        "servings": 24,
        "url": "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/",
        "ingredients": [
            ("Flour", "2 1/4", "cups"),
            ("Sugar", "1", "cup"),
            ("Chocolate Chips", "2", "cups"),
            ("Eggs", "2", None),
        ],
        "instructions": [
            "Mix dry ingredients.",
            "Add wet ingredients.",
            "Scoop onto tray.",
            "Bake at 350°F for 12 minutes."
        ]
    }
]

with app.app_context():
    for r in recipes_to_add:
        recipe = Recipe(
            title=r["title"],
            cuisine=r["cuisine"],
            prep_time_minutes=r["prep"],
            cook_time_minutes=r["cook"],
            total_time_minutes=r["prep"] + r["cook"],
            difficulty=r["difficulty"],
            servings=r["servings"],
            source_url=r["url"]
        )

        db.session.add(recipe)
        db.session.commit()

        for ing in r["ingredients"]:
            ingredient = Ingredient(
                recipe_id=recipe.id,
                name=ing[0],
                quantity=ing[1],
                unit=ing[2]
            )
            db.session.add(ingredient)

        for i, step in enumerate(r["instructions"], start=1):
            instruction = Instruction(
                recipe_id=recipe.id,
                step_number=i,
                step_text=step
            )
            db.session.add(instruction)

        db.session.commit()

print("Added 10 recipes successfully!")
