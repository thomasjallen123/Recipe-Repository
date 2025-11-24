# 1. Import the functions to create app and db object
import logging
import sys
import os

# Add the project root to the Python path, which is the 'Core' directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# relative import after adjusting sys.path
from backend.app import create_app, db
from backend.app.models import Recipe, Ingredient

#Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# include the scrapper directory - change as needed
try: 
    from backend.scrapper.scrape_recipe import scrape_recipe

    logging.info("Successfully imported scrape_recipe from primary path.")
except ImportError:

    logging.warning("Primary import failed, attempting fallback import for scrape_recipe.")
    # Fallback import if the above fails  
    from backend.scrapper.scrape_recipe import scrape_recipe

#----Configuration---
#URL to scrape
logging.info("Setting recipe URL to scrape.")
RECIPE_URL = "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"

# 2. Create an instance of your entire application / API linking to the app factory
logging.info("Creating application instance.")
app = create_app()

logging.info("Application instance created.")

# 3. Manually create the "context bubble"
# This tells the script to load the app's configuration (from config.py)
# and prepare the database connection.
with app.app_context():
    
    #debugging statement to indicate the start of the population process
    logging.info("Starting database population script...")

    
    def parse_ingredient(ingredient_string):

        logging.info(f"Parsing ingredient string: {ingredient_string}")

        """
        Parses an ingredient string into quantity, unit, and name.
        This is a simplified example. A robust solution would use a dedicated
        library (like ingredient-parser) or advanced regular expressions.
        """
        # Example: "2 1/2 cups all-purpose flour, sifted"
        parts = ingredient_string.split()

        if not parts:
            logging.warning("Ingredient string is empty or malformed.")
            return None
        
        quantity = ""
        unit = ""
        name = []


        #Simple check for qunatity (numeric or fraction)

        if parts[0].replace('/', '').replace('.', '').isdigit():
            quantity = parts.pop(0)
            
            #handle cases like "1 1/2"
            if parts and parts[0].replace('/', '').replace('.', '').isdigit() and len(parts) > 1 and parts[1].replace('/', '').replace('.', '').isdigit():
                quantity += " " + parts.pop(0)


        #simple check for a unit
        if parts and len(parts) > 1:  # simplistic check for unit length
        
            common_units = ['cup', 'cups', 'tbsp', 'tsp', 'tablespoon', 'teaspoon', 'oz', 'lb', 'g', 'kg', 'ml', 'l', 'pinch', 'clove', 'cloves']
            if parts[0].lower() in common_units:
                unit = parts.pop(0)

        # The rest is the ingredient name
        name = ' '.join(parts)

        # Pretend it returns a clean dictionary
        return {"quantity": quantity, "unit": unit, "name": name}

    # 4. Scrape data using the scrape_recipe function
    logging.info(f"Scraping recipe from URL: {RECIPE_URL}")
    scraped_data = scrape_recipe(RECIPE_URL)


    #Check if the recipe already exists to avoid duplicates
    existing_recipe = Recipe.query.filter_by(source_url=RECIPE_URL).first()
    if existing_recipe:
        logging.info(f"Recipe already exists in the database: {existing_recipe.title}")
    else:
       

        try: 
            scraped_data = scrape_recipe(RECIPE_URL)
            logging.info(f"Scraped data for recipe: {scraped_data['title']}")

            if not scraped_data:
                logging.error("No data scraped from the provided URL.")
                raise ValueError("Scraped data is empty.")
            else:
                logging.info("Scraped data successfully retrieved: {scraped_data}.get('title')")

                #create recipe object

                new_recipe = Recipe(
                    title=scraped_data['title'],
                    source_url=scraped_data['source_url'],
                    source_website=scraped_data['source_website'],
                    prep_time_minutes=scraped_data['prep_time'],
                    cook_time_minutes=scraped_data['cook_time'],
                    total_time_minutes=scraped_data['total_time'],
                    servings=scraped_data['servings'],
                    difficulty=scraped_data['difficulty'],
                    cuisine=scraped_data['cuisine_type'],
                    image_url=scraped_data['image_url'],
                    scraped_at=scraped_data['scraped_at']
                )

            #ingredient parsing and creation
            Ingredient_list = []
            
            if 'ingredients' in scraped_data:
                for text_line in scraped_data['ingredients']:
                    parsed_ing = parse_ingredient(text_line)

                    if parsed_ing:
                        
                        Ingredient_Obj = Ingredient(
                            name=parsed_ing['name'],
                            quantity=parsed_ing['quantity'],
                            unit=parsed_ing['unit'],
                            recipe=new_recipe  # Associate with the new recipe
                        )
                        # reason for appending to a list is to handle multiple ingredients
                        Ingredient_list.append(Ingredient_Obj)


                        # Add ingredient to the recipe's ingredients relationship
                        new_recipe.ingredients.append(Ingredient_Obj)

                        logging.info(f"Added ingredient: {parsed_ing['name']}")
                    else:
                        logging.warning(f"Failed to parse ingredient: {parsed_ing}")
        
        except Exception as e:
            logging.error(f"Error during scraping or recipe creation: {e}")
            db.session.rollback()
            raise e
        finally:
            db.session.add(new_recipe)

logging.info("Database population script completed.")