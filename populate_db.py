#Import for local logic 
import logging
import json
import re
from sqlalchemy import inspect #for checking existing records


#relative import - when running as part of the package
from backend.app import create_app, db
from backend.app.models import Recipe, Ingredient, Instruction

#Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fromScrape_json(json_file_path):
    """
    Loads recipe data from a JSON file.
    """
    logging.info(f"Loading recipe data from JSON file: {json_file_path}")

    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        logging.info(f"Successfully loaded recipe data from {json_file_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading JSON file {json_file_path}: {e}")
        return None
 

#----Configuration---
def parse_instructions(instruction_string):
    ''''
    Parses a single instruction string into individual steps.
    
    '''

    logging.info("starting instruction parsing.")

    if not instruction_string:
        logging.warning("Instruction string is empty or malformed.")
        return None

    # Split after lowercase+period
    chunks = re.split(r'(?<=[a-z]\.)', instruction_string)

    # Clean up whitespace
    steps = [chunk.strip() for chunk in chunks if chunk.strip()]

    # Count steps
    num_steps = len(steps)

    return {"steps": steps, "step_number": num_steps}


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

def main(json_file_path):
    """
    Main function to populate the database from a JSON file.
    """  
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

        


        # 4. Scrape data using the scrape_recipe function
        logging.info(f"Preparing data retrieve from json file.")
        scraped_data = fromScrape_json(json_file_path)
        
        if not scraped_data:
            logging.error("Failed to retrieve data from JSON file.")
            return

        # Ensure the database tables are created
        inspector = inspect(db.engine)

        if not inspector.has_table("recipe"):
            logging.info("Creating database tables...")
            db.create_all()
            logging.info("Database tables created.")
        else:
            logging.info("Database tables already exist.")
        
        #Check if the recipe already exists to avoid duplicates
        existing_recipe = Recipe.query.filter_by(title=scraped_data['title']).first()

        if existing_recipe:
            logging.info(f"Recipe already exists in the database: {existing_recipe.title}")
        else:       

            try:

                logging.info(f"Scraped data for recipe: {scraped_data.get('title')}")

                if not scraped_data:
                    logging.error("No data scraped from the provided URL.")
                    raise ValueError("Scraped data is empty.")
                else:
                    logging.info("Scraped data successfully retrieved: {scraped_data}.get('title')")

                    #create recipe object
                    #using get method to avoid key errors
                    new_recipe = Recipe(
                        title=scraped_data['title'],
                        source_url=scraped_data.get('source_url'),
                        source_website=scraped_data.get('host'),
                        prep_time_minutes=scraped_data.get('prep_time'),
                        cook_time_minutes=scraped_data.get('cook_time'),
                        total_time_minutes=scraped_data.get('total_time'),
                        servings=scraped_data.get('servings'),
                        difficulty=scraped_data.get('difficulty'),
                        cuisine=scraped_data.get('cuisine_type'),
                        image_url=scraped_data.get('image'),
                        scraped_at=scraped_data.get('scraped_at')
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

                #instruction parsing and creation   
                # TODO: Add step number handling 
                if 'instructions' in scraped_data:

                    parsed_steps = parse_instructions(scraped_data['instructions'])

                    instruction_obj = Instruction(
                            step_number=parsed_steps['step_number'],
                            step_text=scraped_data['instructions'] #input full text for now
                            #recipe=new_recipe
                        )
                    new_recipe.instructions.append(instruction_obj)
                    logging.info(f"Added all instruction: {parsed_steps['step_number']} steps")

                db.session.add(new_recipe)

                # Commit the session to save changes
                logging.info("Committing changes to the database.")
                db.session.commit()
                logging.info("Database population script completed.")
            
            except Exception as e:
                logging.error(f"Error during scraping or recipe creation: {e}")
                db.session.rollback()
                raise e



if __name__ == '__main__':
    import argparse

    logging.info("Starting script with command-line argument parsing.")

    #Create the argument parser
    parser = argparse.ArgumentParser(description='Populate the database with recipe data from a JSON file.')
    
    # Add argument for JSON file path
    parser.add_argument('--json', type=str, default=r'C:\Users\Michael\Documents\Academic Library\Academic Course work\Active\CMSC 495\output\Spicy_Chicken-Tortilla_Chip_Casserole.json',help='Path to the JSON file containing recipe data.')
    
    #Parse the arguments
    args=parser.parse_args()

    #pass the  JSON file path to the population function
    logging.info(f"Using JSON file path: {args.json}")

    json_file_path = args.json
    
    logging.info("Invoking main function to populate database.")
    main(args.json)
