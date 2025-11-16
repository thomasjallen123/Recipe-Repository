from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

## Create an engine that stores data in the local directory's
## sqlalchemy_example.db file.
##Alternate description, this is the location of the library
engine = create_engine('sqlite:///recipes.db', echo=True)

## Configure a base class for future objects
## think of this as a printer that creates library cards that can perform certain actions (create, read, update, delete)
Session = sessionmaker(bind=engine)

## Alternate description, this card carries out the actions(create, read, update, delete)
session_action = Session()

## Alternate description, this is the shelving system that holds all the books
Base = declarative_base()

## Define the Recipe classes that maps to the recipes table

## 1. define the Recipe class for mapping to the recipes table
class Recipe(Base):
    ## Define the table name
    __tablename__ = 'recipes'

    id = Column(Integer, Sequence('recipe_id_seq'), primary_key=True)
    title = Column(String(250), nullable=False)
    url = Column(String(500), nullable=False)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=True)
    yield_amount = Column(Integer, nullable=True) # 'yield' is a keyword in Python
    author = Column(String(250), nullable=True)
    category = Column(String(250), nullable=True)
    
    # Establish bidirectional relationships to the child tables
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    instructions = relationship("Instruction", back_populates="recipe", cascade="all, delete-orphan")
    nutrients = relationship("Nutrient", uselist=False, back_populates="recipe", cascade="all, delete-orphan")

    def __repr__(self):
        ##debugging statement to show the recipe details
        return f"<Recipe(title='{self.title}', url='{self.url}')>"
    
## 2. define the Ingredient class for mapping to the ingredients table
class Ingredient(Base):
    ## Define the table name
    __tablename__ = 'ingredients'

    id = Column(Integer, Sequence('ingredient_id_seq'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient_Mx = Column(String(1000), nullable=False)
    
    # Establish relationship with Recipe
    # linking back to Recipe class to ensure bidirectional entry updates
    recipe = relationship("Recipe", back_populates="ingredients")
    
    def __repr__(self):
            # Creates a preview of the text, e.g., "Flour (2 cups)..."
            mx_preview = (self.ingredient_Mx[:40] + '...') if len(self.ingredient_Mx) > 40 else self.ingredient_Mx
            
            ##debugging statement to show the ingredient details
            return f"<Ingredient(id={self.id}, recipe_id={self.recipe_id}, ingredient_Mx='{mx_preview}')>"
    
## 3. define the Instruction class for mapping to the instructions table
class Instruction(Base):
    ## Define the table name
    __tablename__ = 'instructions'

    id = Column(Integer, Sequence('instruction_id_seq'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    step_number = Column(Integer, nullable=False)
    step_text = Column(String(2000), nullable=False)
    
    # Establish relationship with Recipe
    # linking back to Recipe class to ensure bidirectional entry updates
    recipe = relationship("Recipe", back_populates="instructions")
    
    def __repr__(self):
            # Creates a preview of the text, e.g., "Mix all ingredients..."
            step_preview = (self.step_text[:40] + '...') if len(self.step_text) > 40 else self.step_text
            
            ##debugging statement to show the instruction details
            return f"<Instruction(id={self.id}, recipe_id={self.recipe_id}, step_text='{step_preview}')>"

##4. define the Nutrient class for mapping to the nutrients table
class Nutrient(Base):
    ## Define the table name
    __tablename__ = 'nutrients'

    id = Column(Integer, Sequence('nutrient_id_seq'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    calories = Column(Integer, nullable=False)
    fat_content = Column(String(10), nullable=False)
    saturated_fat = Column(String(10), nullable=False)
    carbohydrates = Column(String(10), nullable=False)
    fiber_content = Column(String(10), nullable=False)
    sugar_content = Column(String(10), nullable=False)
    protein_content = Column(String(10), nullable=False)

    
    # Establish relationship with Recipe
    # linking back to Recipe class to ensure bidirectional entry updates
    recipe = relationship("Recipe", back_populates="nutrients")
    
    def __repr__(self):
        ##debugging statement to show the nutrient details
        
        return (
        f"<Nutrient(id={self.id}, recipe_id={self.recipe_id}, calories={self.calories}, "
        f"fat_content='{self.fat_content}', saturated_fat='{self.saturated_fat}', "
        f"carbohydrates='{self.carbohydrates}', fiber_content='{self.fiber_content}', "
        f"sugar_content='{self.sugar_content}', protein_content='{self.protein_content}')>"
        )
    
##4. define the User class for mapping to the users table
class User(Base):
    ## Define the table name
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    
    def __repr__(self):
        ##debugging statement to show the user details
        return f"<User(username='{self.username}')>"

## Internal Test Case
if __name__ == "__main__":
    # This block will only run when the script is executed directly
    # (e.g., python app.py)

    # 1. Create all tables
    print("--- Creating database and tables ---")
    Base.metadata.create_all(engine)
    print("--- Tables created successfully ---")

    # 2. Create instances of our models
    new_recipe = Recipe(
        title="Classic Pancakes",
        url="http://example.com/pancakes",
        prep_time=10,
        cook_time=15,
        total_time=25,
        yield_amount=8,
        author="Gemini",
        category="Breakfast",
        ingredients=[
            Ingredient(ingredient_Mx="1 1/2 cups all-purpose flour"),
            Ingredient(ingredient_Mx="3 1/2 teaspoons baking powder"),
            Ingredient(ingredient_Mx="1 cup milk"),
            Ingredient(ingredient_Mx="1 large egg")
        ],
        instructions=[
            Instruction(step_number=1, step_text="In a large bowl, sift together the flour, baking powder, salt, and sugar."),
            Instruction(step_number=2, step_text="Make a well in the center and pour in the milk, egg, and melted butter; mix until smooth."),
        ],
        nutrients=Nutrient(
            calories=220, fat_content="9g", saturated_fat="5g",
            carbohydrates="28g", fiber_content="1g", sugar_content="7g", protein_content="6g"
        )
    )

    # 3. Add the new recipe to the session and commit
    print("\n--- Adding new recipe to the database ---")
    session_action.add(new_recipe)
    session_action.commit()
    print(f"--- Recipe '{new_recipe.title}' added successfully ---")

    # 4. Query and verify the data
    print("\n--- Verifying data from database ---")
    retrieved_recipe = session_action.query(Recipe).filter_by(title="Classic Pancakes").first()
    print(f"Retrieved Recipe: {retrieved_recipe}")
    for ingredient in retrieved_recipe.ingredients:
        print(f"  - {ingredient}")
    print(f"Nutrients: {retrieved_recipe.nutrients}")

    # Close the session
    session_action.close()