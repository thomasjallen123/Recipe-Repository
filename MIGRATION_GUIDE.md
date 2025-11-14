# Backend Migration Guide - From Old to Corrected Files

## Overview

This guide walks through replacing your old backend files with the corrected versions.

**Time required:** 30 minutes  
**Risk level:** LOW (changes are additive, no breaking changes for frontend)

---

## Step 1: Backup Your Current Files

```bash
# Create backup directory
mkdir backup
cp *.py backup/
cp requirements.txt backup/
```

---

## Step 2: Replace Files

### Files to Delete
```bash
rm collections.py  # CRITICAL - This file name causes import errors
```

### Files to Replace

Replace each of these with the corrected version:

1. `__init__.py` - Add user loader, CORS, error handlers
2. `models.py` - Add complete schema, M2M relationship
3. `auth.py` - Add email field, validation
4. `recipes.py` - Add search, filter, pagination
5. `app.py` - Add error handlers
6. `config.py` - Complete configuration options

### New Files to Add

```bash
# These files don't exist yet - copy them to your project
cp validators.py <your-project>/
cp requirements.txt <your-project>/
cp .env.example <your-project>/
```

### Files That Don't Change

These can stay as-is or use updated versions:
- `__pycache__/` (auto-generated, ignore)
- `app.db` (SQLite database, keep it)

---

## Step 3: Update Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install new dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "Flask|SQLAlchemy|CORS"
```

**New dependencies added:**
- `Flask-CORS` - For frontend integration
- Updated version pinning for stability

---

## Step 4: Migrate Database Schema

Because the models changed, you need to reinitialize the database:

```bash
# Option A: Start fresh (recommended for development)
rm app.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✓ Database initialized')"

# Option B: If you have data you want to keep, use Alembic migrations (advanced)
# This is covered in the "Advanced" section below
```

### What Changed in Database

**Users Table:**
- Added: `email` field (required, unique)
- Added: `created_at` timestamp

**Recipes Table:**
- Added: `source_url`, `source_website`
- Added: `prep_time_minutes` (was `prep_time`)
- Renamed: `cook_time` → `cook_time_minutes`
- Added: `total_time_minutes`
- Added: `servings`, `difficulty`, `image_url`
- Added: `created_at`, `scraped_at`

**New Table:**
- `user_recipe_collection` - M2M junction table for collections

**Ingredients Table:**
- Added: `unit` field (e.g., "cup", "tsp")

**Instructions Table:**
- Renamed: `step` → `step_text`

---

## Step 5: Test the Application

```bash
# Start Flask
python app.py

# In another terminal, test endpoints
curl http://localhost:5000/
# Should see: {"message": "Welcome to the Recipe Repository API!", ...}

# Test health check
curl http://localhost:5000/health
# Should see: {"status": "healthy", "service": "Recipe Repository API"}
```

---

## Step 6: Test Authentication

```bash
# Register a user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Expected response:
# {"message": "User registered successfully", "user": {"id": 1, "username": "testuser", ...}}

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }' \
  -c cookies.txt  # Save session cookies

# Get current user (requires login)
curl http://localhost:5000/api/auth/me \
  -b cookies.txt  # Use session cookies
```

---

## Step 7: Update Frontend Integration

If your frontend is already built, these endpoint changes may affect it:

### Endpoint Changes

**New Endpoints:**
```
GET /api/recipes/search?q=chicken
GET /api/recipes/by-cuisine/Italian
GET /api/recipes/quick
GET /api/collections/is-saved/<id>
POST /api/collections/add-multiple
POST /api/collections/clear
```

**Modified Endpoints:**

Old response:
```json
{"recipes": [...]}
```

New response:
```json
{
  "recipes": [...],
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "per_page": 20
}
```

**Field Names Changed:**

Old Recipe Response:
```json
{
  "id": 1,
  "title": "Pasta",
  "cuisine": "Italian",
  "cook_time": 20
}
```

New Recipe Response:
```json
{
  "id": 1,
  "title": "Pasta",
  "cuisine": "Italian",
  "cook_time_minutes": 20,
  "prep_time_minutes": 10,
  "total_time_minutes": 30,
  "servings": 4,
  "source_url": "https://...",
  "source_website": "AllRecipes",
  "image_url": "https://...",
  "ingredients": [...],
  "instructions": [...]
}
```

**Update Vue.js Code:**

```javascript
// Old (WRONG)
recipe.cook_time

// New (CORRECT)
recipe.cook_time_minutes

// New data available
recipe.prep_time_minutes
recipe.servings
recipe.source_website
recipe.image_url
```

---

## Step 8: Update Database Seeding Script

If you have a script that seeds recipes from your scraper, update field names:

```python
# Old code (WRONG)
recipe = Recipe(
    title="Pasta",
    cook_time=20,
    cuisine="Italian"
)

# New code (CORRECT)
recipe = Recipe(
    title="Pasta",
    cook_time_minutes=20,
    prep_time_minutes=10,
    total_time_minutes=30,
    servings=4,
    cuisine="Italian",
    source_website="AllRecipes",
    source_url="https://www.allrecipes.com/...",
    image_url="https://..."
)
```

---

## Step 9: Commit Changes

```bash
git add -A
git commit -m "fix: correct backend implementation

- Rename collections.py to user_collections.py (fixes import conflict)
- Add user_loader for Flask-Login
- Add email field to User model
- Complete Recipe schema with all fields
- Add M2M relationship for collections
- Add input validation
- Add pagination to search endpoints
- Add CORS configuration
- Add comprehensive error handlers
"
```

---

## Advanced: Database Migrations (Optional)

If you want to keep existing data, use Flask-Migrate:

```bash
# Install Flask-Migrate
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration
flask db migrate -m "Update recipe schema"

# Apply migration
flask db upgrade
```

This creates a `migrations/` folder to track schema changes without dropping data.

---

## Rollback Plan (If Something Goes Wrong)

```bash
# Restore from backup
cp backup/* .

# Restore old database
rm app.db
cp backup/app.db .

# Downgrade dependencies
pip install -r backup/requirements.txt
```

---

## Verification Checklist

After migration, verify:

- [ ] App starts without import errors
- [ ] `python app.py` runs successfully
- [ ] `curl http://localhost:5000/` returns welcome message
- [ ] Registration endpoint works
- [ ] Login endpoint works
- [ ] Recipes endpoint returns data
- [ ] Collections endpoints work
- [ ] Frontend can call API (no CORS errors)
- [ ] Database has all expected tables

```bash
# Quick verification script
python << 'EOF'
from app import create_app, db
from app.models import User, Recipe, Ingredient, Instruction

app = create_app()
app.app_context().push()

print("✓ App imported successfully")
print(f"✓ Users table: {User.query.count()} users")
print(f"✓ Recipes table: {Recipe.query.count()} recipes")
print(f"✓ Ingredients table: {Ingredient.query.count()} ingredients")
print(f"✓ Instructions table: {Instruction.query.count()} instructions")
print("\nAll checks passed!")
EOF
```

---

## Common Issues & Solutions

### Issue: "No such table: recipe"
**Cause:** Database not initialized  
**Solution:** `rm app.db && python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"`

### Issue: "email column does not exist"
**Cause:** Old database schema  
**Solution:** Reinitialize database (delete app.db)

### Issue: "ImportError: cannot import name 'defaultdict'"
**Cause:** collections.py naming conflict  
**Solution:** Delete `collections.py`, use `user_collections.py`

### Issue: CORS errors from frontend
**Cause:** Frontend origin not in allowed list  
**Solution:** Update CORS config in `__init__.py` with frontend URL

### Issue: "User must provide a password"
**Cause:** Old registration code not handling new email field  
**Solution:** Update frontend registration form to include email

---

## Frontend Updates Needed

Update your Vue.js registration form:

```javascript
// Old (INCOMPLETE)
const registerUser = async (username, password) => {
  // ...
}

// New (COMPLETE)
const registerUser = async (username, email, password) => {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username,
      email,      // ADD THIS
      password
    })
  })
  return response.json()
}
```

Update recipe display:

```javascript
// Old
<p>Cook time: {{ recipe.cook_time }} min</p>

// New
<p>Prep time: {{ recipe.prep_time_minutes }} min</p>
<p>Cook time: {{ recipe.cook_time_minutes }} min</p>
<p>Total time: {{ recipe.total_time_minutes }} min</p>
```

---

## Timeline

- **5 min:** Backup files
- **5 min:** Replace files and install dependencies
- **10 min:** Reinitialize database
- **5 min:** Test endpoints
- **5 min:** Update frontend code

**Total: ~30 minutes**

---

## Questions?

Refer to:
- `BACKEND_CODE_REVIEW.md` - Detailed explanation of issues and fixes
- `BACKEND_SETUP_GUIDE.md` - Full setup and API documentation
- Project Design Document - Overall architecture

Good luck with the migration!
