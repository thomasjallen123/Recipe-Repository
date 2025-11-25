# Database Roadmap

This document describes the database design and how data flows through the
project (scraper → backend → frontend). It also includes a starter schema
for SQLite and a recommended set of entities and relationships to support
recipes, ingredients, instructions, users, and collections.

## Part 1 — Codebase structure (high level)

The project is organized into three major layers:

- Frontend
  - Tech: Vue.js (JavaScript)
  - Purpose: User interface — search, login, recipe display
- Backend
  - Tech: Flask (Python)
  - Purpose: API layer — handles requests and connects frontend to DB
- Scraper
  - Tech: Python (BeautifulSoup or similar)
  - Purpose: Extract recipe data from sites like AllRecipes and Food Network
- Database
  - Tech: SQLite
  - Purpose: Stores recipes, ingredients, users, and collections

Understanding the full flow (scraper → backend → frontend) helps collaboration.

## Part 2 — Languages to review (quick primer)

- Python (backend and scraper)
  - Syntax is simpler than Java — no semicolons, no braces.
  - Flask is lightweight: use it to define models, API endpoints, and to
    validate/insert scraped data.
- JavaScript (frontend)
  - Vue.js uses components and reactive data binding.
  - Learn how the UI calls API endpoints (axios or fetch) to coordinate
    behavior with the backend.

## Part 3 — Starting your database blueprint

Follow these steps to design the database.

### Step 1 — Identify entities

Likely entities:

- Recipe
- Ingredient
- Instruction (or Step)
- User
- Collection (user-saved recipes)
- (Optional) Tag or Cuisine
- (Optional) RecipeIngredient join table to store quantities

### Step 2 — Define relationships

- One Recipe → many Ingredients (via a join table to store quantities)
- One Recipe → many Instructions (ordered steps)
- One User → many Collections
- One Collection → many Recipes

### Step 3 — Simple ERD sketch

An ASCII ERD sketch:

```
User ───< Collection >─── Recipe ───< RecipeIngredient >─── Ingredient
                       │
                       └───< Instruction
```

Notes:
- Collection is a join between User and Recipe (a user’s saved list).
- RecipeIngredient is a join to store quantity/unit for each ingredient.
- Instruction stores ordered steps for a recipe.

### Step 4 — Normalization guidance

- Avoid duplicating ingredient text across recipes. Use a normalized
  Ingredient table and a join table for per-recipe quantities.
- Use foreign keys to enforce relationships and maintain referential
  integrity.
- Keep step text and ordering in a separate Instructions table.

### Step 5 — Starter SQLite schema

This is a minimal starting schema. 

```sql
-- Recipes
CREATE TABLE Recipe (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  cuisine TEXT,
  prep_time INTEGER,   -- minutes
  cook_time INTEGER,   -- minutes
  servings INTEGER,
  source_url TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Ingredients master list
CREATE TABLE Ingredient (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

-- Join table: recipe ingredients with quantity and unit
CREATE TABLE RecipeIngredient (
  id INTEGER PRIMARY KEY,
  recipe_id INTEGER NOT NULL,
  ingredient_id INTEGER NOT NULL,
  quantity TEXT,       -- keep as text to handle "1 1/2", "to taste", etc.
  unit TEXT,
  FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE,
  FOREIGN KEY (ingredient_id) REFERENCES Ingredient(id) ON DELETE CASCADE
);

-- Ordered instructions / steps
CREATE TABLE Instruction (
  id INTEGER PRIMARY KEY,
  recipe_id INTEGER NOT NULL,
  step_number INTEGER NOT NULL,
  text TEXT NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE
);

-- Users
CREATE TABLE User (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  email TEXT UNIQUE,
  password_hash TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Collections (a user's saved recipes)
CREATE TABLE Collection (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Join table between Collection and Recipe
CREATE TABLE CollectionRecipe (
  id INTEGER PRIMARY KEY,
  collection_id INTEGER NOT NULL,
  recipe_id INTEGER NOT NULL,
  added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (collection_id) REFERENCES Collection(id) ON DELETE CASCADE,
  FOREIGN KEY (recipe_id) REFERENCES Recipe(id) ON DELETE CASCADE
);
```

## Additional recommendations

- Scraper → Backend
  - Validate scraped data before inserting (title, ingredient list, steps).
  - Normalize ingredient names (lowercase, strip punctuation).
  - Use transactions when inserting a recipe and its related rows.
- Backend API
  - Provide endpoints for listing, searching, and retrieving a recipe
    with ingredients and instructions.
  - Paginate result sets and index searchable columns (title, cuisine).
- Migrations / schema management
  - Even with SQLite, use a simple migrations tool (Flask-Migrate / Alembic)
    to track schema changes.
- Tests
  - Add tests for parsing, insertion, and retrieval to guard against
    scraper or schema changes.
