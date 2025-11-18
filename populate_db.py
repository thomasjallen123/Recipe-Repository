# 1. Import the functions to create app and db object
from app import create_app, db
from app.models import Recipe, Ingredient

# 2. Create an instance of your entire application
app = create_app()

# 3. Manually create the "context bubble"
# This tells the script to load the app's configuration (from config.py)
# and prepare the database connection.
with app.app_context():
    
    #debugging statement to indicate the start of the population process
    print("Populating database...")

    
    def parse_ingredient(ingredient_string):
        """
        Parses an ingredient string into quantity, unit, and name.
        This is a simplified example. A robust solution would use a dedicated
        library (like ingredient-parser) or advanced regular expressions.
        """
        # Example: "2 1/2 cups all-purpose flour, sifted"
        parts = ingredient_string.split()
        
        # Simple logic (will not work for all cases)
        quantity = parts[0]
        unit = parts[1]
        name = " ".join(parts[2:])
        
        # Pretend it returns a clean dictionary
        return {"quantity": quantity, "unit": unit, "name": name}


    #debugging statement to indicate database session start
    print(f"Found{len(scraped_data)} recipes to add.")

    for data in scraped_data:
        # Example: Creating a new recipe from scraped data
        new_recipe = Recipe(
            title=data['title'],
            source_url=data['source_url'],
            source_website=data['source_website'],
            prep_time_minutes=data['prep_time'],
            cook_time_minutes=data['cook_time'],
            total_time_minutes=data['total_time'],
            servings=data['servings'],
            difficulty=data['difficulty'],
            cuisine=data['cuisine_type'],
            image_url=data['image_url'],
            scraped_at=data['scraped_at']
        )
        
        # Create a list of Ingredient objects by parsing each string
        ingredient_object_list = []
        for text_line in scraped_data['ingredients']:
            parsed_ing = parse_ingredient(text_line)
            
            ingredient_object = Ingredient(
                quantity=parsed_ing['quantity'],
                unit=parsed_ing['unit'],
                name=parsed_ing['name']
            )
            ingredient_object_list.append(ingredient_object)

        db.session.add(new_recipe)
   
    try:
        print("Committing changes to the database...")
        db.session.commit()
        print("Database commit successful.")

    except Exception as e:
        print("An error occurred while committing to the database:", e)


print("Database population script finished.")