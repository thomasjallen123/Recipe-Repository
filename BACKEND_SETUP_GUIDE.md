# Backend Setup Guide

## Quick Start (30 minutes)

### 1. Prerequisites
- Python 3.9+
- pip (Python package manager)
- Virtual environment tool (venv)

### 2. Installation Steps

```bash
# Clone repository
git clone <your-repo-url>
cd recipe-repository

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env

# Initialize database
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized successfully')"

# Run development server
python app.py
```

The API will be available at: `http://localhost:5000`

### 3. Test Installation

```bash
# Test API is running
curl http://localhost:5000/

# Should return:
# {
#   "message": "Welcome to the Recipe Repository API!",
#   "version": "1.0",
#   "endpoints": {...}
# }
```

## File Structure

```
backend/
├── __init__.py           # App initialization, blueprints, CORS
├── app.py                # Application entry point
├── config.py             # Configuration settings
├── models.py             # Database models (User, Recipe, Ingredient, Instruction)
├── auth.py               # Authentication routes (login, register, logout)
├── recipes.py            # Recipe routes (search, filter, retrieve)
├── user_collections.py   # Collections routes (save, unsave recipes)
├── validators.py         # Input validation functions
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
└── app.db                # SQLite database (auto-created)
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///app.db
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info
- `GET /api/auth/verify-token` - Verify session

### Recipes
- `GET /api/recipes` - Get paginated recipes (with filters)
- `GET /api/recipes/<id>` - Get recipe details
- `GET /api/recipes/search` - Search recipes by title
- `GET /api/recipes/by-cuisine/<cuisine>` - Filter by cuisine
- `GET /api/recipes/quick` - Get recipes under 30 minutes

### Collections
- `GET /api/collections` - Get user's saved recipes
- `POST /api/collections/save/<id>` - Save recipe
- `POST /api/collections/unsave/<id>` - Remove recipe
- `GET /api/collections/is-saved/<id>` - Check if saved
- `POST /api/collections/add-multiple` - Save multiple recipes
- `POST /api/collections/clear` - Clear all saved recipes

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique, 3-80 characters
- `email` - Unique, valid email format
- `password` - Hashed with bcrypt
- `created_at` - Timestamp

### Recipes Table
- `id` - Primary key
- `title` - Recipe name
- `source_url` - Link to original recipe
- `source_website` - "AllRecipes" or "Food Network"
- `prep_time_minutes` - Prep time
- `cook_time_minutes` - Cook time
- `total_time_minutes` - Total time
- `servings` - Number of servings
- `difficulty` - "Easy", "Medium", or "Hard"
- `cuisine` - Cuisine type
- `image_url` - Recipe image
- `created_at` - When added to database
- `scraped_at` - When scraped

### Ingredients Table
- `id` - Primary key
- `recipe_id` - Foreign key to recipes
- `name` - Ingredient name
- `quantity` - Amount (e.g., "1", "1.5")
- `unit` - Unit (e.g., "cup", "tsp", "g")

### Instructions Table
- `id` - Primary key
- `recipe_id` - Foreign key to recipes
- `step_number` - Step order
- `step_text` - Instruction text

### User-Recipe Collections Table
- `user_id` - Foreign key to users
- `recipe_id` - Foreign key to recipes
- `added_at` - When recipe was saved

## Development Tips

### Run Tests
```bash
pytest tests/ --cov=app --cov-report=html
```

### Database Reset (Development Only)
```bash
# Delete the database file
rm app.db

# Reinitialize
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database reset')"
```

### Access Database Shell
```bash
python
>>> from app import create_app, db
>>> from app.models import User, Recipe
>>> app = create_app()
>>> app.app_context().push()
>>> Recipe.query.count()
```

## CORS Configuration

Frontend is allowed from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (React default)
- `http://localhost:8080` (Common development port)

Update `__init__.py` CORS configuration to add more origins as needed.

## Important Notes

1. **Security**: Change `SECRET_KEY` in production
2. **Database**: SQLite is fine for MVP; use PostgreSQL for production
3. **Password Hashing**: Uses werkzeug with bcrypt
4. **Sessions**: Session-based authentication, not JWT
5. **CORS**: Must be enabled for frontend integration

## Troubleshooting

**"ModuleNotFoundError: No module named 'app'"**
- Make sure you're in the correct directory
- Activate virtual environment: `source venv/bin/activate`

**"ImportError: cannot import name 'defaultdict'"**
- This was the original collections.py conflict - already fixed in corrected files

**"Database locked" error**
- Close any other database connections
- Check if another Flask instance is running

**CORS errors from frontend**
- Verify frontend URL is in CORS_ORIGINS list
- Check that `CORS(app)` is called in `__init__.py`

## Next Steps

1. Set up frontend (Vue.js)
2. Set up web scraper
3. Run integration tests
4. Deploy to Heroku

See project documentation for full details.
