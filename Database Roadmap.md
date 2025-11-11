🧠 Part 1: Understanding the Codebase Structure
Based on the GitHub repo and my role, the project is organized into three major layers:
Layer	Tech Stack	Purpose
Frontend	Vue.js (JavaScript)	User interface: search, login, recipe display
Backend	Flask (Python)	API layer: handles requests, connects frontend to database
Scraper	Python (BeautifulSoup or similar)	Extracts recipe data from AllRecipes and Food Network
Database	SQLite (SQL)	Stores recipes, ingredients, users, collections
I will be working primarily with the backend and database, but understanding how data flows from scraper → backend → frontend will help me collaborate smoothly.

📚 Part 2: Languages to Review (Quick Primer)
here’s how the other languages compare:
🔹 Python (for backend and scraper)
	• Syntax is simpler than Java (no semicolons, no curly braces)
	• Flask is a lightweight web framework — similar to Spring Boot but less verbose
	• I will use Python to: 
		○ Define models (like Recipe, Ingredient)
		○ Write API endpoints
		○ Validate and insert scraped data
🔹 JavaScript (for frontend)
	• Vue.js uses components and reactive data binding
	• Understanding how it calls API endpoints (via axios or fetch) is helpful

🏗️ Part 3: Starting Your Database Blueprint
Here’s how to begin the database design:
✅ Step 1: Identify Entities
From the project goals, I will likely need:
	• Recipe
	• Ingredient
	• Instruction
	• User
	• Collection (user-saved recipes)
✅ Step 2: Define Relationships
	• One recipe → many ingredients
	• One recipe → many instructions
	• One user → many collections
	• One collection → many recipes
✅ Step 3: Draft an ERD (Entity-Relationship Diagram)
Here’s a simple sketch:
User ───< Collection >─── Recipe ───< Ingredient
                             │
                             └───< Instruction

✅ Step 4: Normalize Your Tables
	• Avoid duplication (e.g., don’t store full ingredient text in multiple places)
	• Use foreign keys to link tables
✅ Step 5: Create Schema in SQLite
Start with SQL like:
CREATE TABLE Recipe (
  id INTEGER PRIMARY KEY,
  title TEXT,
  cuisine TEXT,
  prep_time INTEGER,
  cook_time INTEGER,
  servings INTEGER
);
Then build out Ingredient, Instruction, User, and Collection.
