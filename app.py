from sqlachemy import create_engine, Column, Integer, String, ForeignKey, Sequence
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
    Yield = Column(Integer, nullable=True)
    author = Column(String(250), nullable=True)
    category = Column(String(250), nullable=True)
    
    def __repr__(self):
        ##debugging statement to show the recipe details
        return f"<Recipe(title='{self.title}', url='{self.url}')>"
    
## 2. define the Ingredient class for mapping to the ingredients table
class Ingredient(Base):
    ## Define the table name
    __tablename__ = 'ingredients'

    id = Column(Integer, Sequence('ingredient_id_seq'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    IngredientMx = Column(String(1000), nullable=False)
    
    # Establish relationship with Recipe
    # linking back to Recipe class to ensure bidirectional entry updates
    recipe = relationship("Recipe", back_populates="ingredients")
    
    def __repr__(self):
            # Creates a preview of the text, e.g., "Flour (2 cups)..."
            mx_preview = (self.IngredientMx[:40] + '...') if len(self.IngredientMx) > 40 else self.IngredientMx
            
            ##debugging statement to show the ingredient details
            return f"<Ingredient(id={self.id}, recipe_id={self.recipe_id}, IngredientMx='{mx_preview}')>"
    
## 3. define the Instruction class for mapping to the instructions table
class Instruction(Base):
    ## Define the table name
    __tablename__ = 'instructions'

    id = Column(Integer, Sequence('instruction_id_seq'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    Step_number = Column(Integer, nullable=False)
    StepText = Column(String(2000), nullable=False)
    
    # Establish relationship with Recipe
    # linking back to Recipe class to ensure bidirectional entry updates
    recipe = relationship("Recipe", back_populates="instructions")
    
    def __repr__(self):
            # Creates a preview of the text, e.g., "Mix all ingredients..."
            step_preview = (self.StepText[:40] + '...') if len(self.StepText) > 40 else self.StepText
            
            ##debugging statement to show the instruction details
            return f"<Instruction(id={self.id}, recipe_id={self.recipe_id}, StepText='{step_preview}')>"

##4. define the Nutrient class for mapping to the nutrients table
class Nutrient(Base):
    ## Define the table name
    __tablename__ = 'nutrients'

    id = Column(Integer, Sequence('nutrient_id_seq'), primary_key=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    Calories = Column(Integer, nullable=False)
    Fat = Column(String(10), nullable=False)
    Saturated_fat = Column(String(10), nullable=False)
    Carbohydrates = Column(String(10), nullable=False)
    Fiber = Column(String(10), nullable=False)
    Sugars = Column(String(10), nullable=False)
    Protein = Column(String(10), nullable=False)

    
    # Establish relationship with Recipe
    # linking back to Recipe class to ensure bidirectional entry updates
    recipe = relationship("Recipe", back_populates="nutrients")
    
    def __repr__(self):
        ##debugging statement to show the nutrient details
        
        return (
        f"<Nutrient(id={self.id}, recipe_id={self.recipe_id}, "
        f"Calories={self.Calories}, Fat='{self.Fat}', "
        f"Saturated_fat='{self.Saturated_fat}', "
        f"Carbohydrates='{self.Carbohydrates}', Fiber='{self.Fiber}', "
        f"Sugars='{self.Sugars}', Protein='{self.Protein}')>"
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
        return f"<User(username='{self.username}', email='{self.email}')>"