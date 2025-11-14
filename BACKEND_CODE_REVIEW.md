# Recipe Repository - Backend Code Review

**Date:** November 12, 2025  
**Reviewed By:** Code Quality Assessment  
**Status:** Issues Found - Action Required

---

## Critical Issues (Must Fix Before Deployment)

### 1. **Module Naming Conflict - `collections.py` (CRITICAL)**

**Severity:** CRITICAL - Blocks Application Launch

**Problem:**
The file is named `collections.py`, which conflicts with Python's built-in `collections` module. When Flask tries to import, Python's module resolution loads your local `collections.py` instead of the standard library `collections` module, causing a circular import and immediate application failure.

**Error Observed:**
```
ImportError: cannot import name 'defaultdict' from partially initialized module 'collections'
```

**Current Code Structure:**
```
uploads/
├── collections.py  ← PROBLEMATIC NAME
├── auth.py
├── recipes.py
├── models.py
├── __init__.py
└── app.py
```

**Fix:** Rename the file to avoid the naming conflict.

**Recommended Solutions (in order of preference):**

1. **Rename to `user_collections.py`** (BEST - most explicit)
   ```bash
   mv collections.py user_collections.py
   ```
   Then update `__init__.py`:
   ```python
   from .user_collections import collections_bp
   app.register_blueprint(collections_bp, url_prefix='/api/collections')
   ```

2. **Rename to `saved_recipes.py`** (ALTERNATIVE - also clear)
   ```bash
   mv collections.py saved_recipes.py
   ```
   Then update `__init__.py`:
   ```python
   from .saved_recipes import collections_bp
   app.register_blueprint(collections_bp, url_prefix='/api/collections')
   ```

**Impact:** This will immediately allow the application to start without import errors.

---

## Structural Issues (Fix Before Next Sprint)

### 2. **Missing Blueprint Import in `__init__.py`**

**Severity:** HIGH - Application won't start

**Problem:**
The `__init__.py` file imports blueprints but the import statements assume a different module structure than what exists.

**Current Code (Line 11-12):**
```python
from .auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')
```

**Issue:** 
After you rename `collections.py`, this import will still fail because the module name doesn't match.

**Fix:**
```python
from .user_collections import collections_bp  # Updated import
app.register_blueprint(collections_bp, url_prefix='/api/collections')
```

---

## Functional Issues (Fix Before Sprint 2)

### 3. **Missing User Loader Function**

**Severity:** HIGH - Flask-Login won't work correctly

**File:** `__init__.py`  
**Problem:** Flask-Login requires a user loader callback to retrieve users from the database.

**Current Code:** Missing user loader implementation

**Required Addition:**
```python
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

Add this after `login_manager.init_app(app)` in `__init__.py`.

**Why:** Without this, `login_required` decorators will fail, and session management won't work.

---

### 4. **Missing Email Field in User Model**

**Severity:** MEDIUM - Registration will fail

**File:** `models.py`  
**Problem:** The registration endpoint (`auth.py` line 21) expects an email field:
```python
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')  # ← NO EMAIL HANDLING
```

But the `User` model only has `username` and `password`:
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # ← MISSING email field
```

**Fix in `models.py`:**
```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # ADD THIS
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email  # ADD THIS
        }
```

**Fix in `auth.py`:**
```python
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')  # ADD THIS
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():  # ADD THIS CHECK
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)  # ADD email
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'user': new_user.to_dict()}), 201
```

---

### 5. **Password Hash Field Name Mismatch**

**Severity:** HIGH - Login will fail

**File:** `models.py` (line 7) vs `auth.py` (line 17, 34)

**Problem:**
- **Model definition:** `password = db.Column(db.String(200), nullable=False)`
- **Login code:** `check_password_hash(user.password, password)`
- **Issue:** The model stores the raw password field, but Flask-Login expects `password_hash` by convention. More importantly, you're never actually hashing the password on login check.

**Current `auth.py` login (BROKEN):**
```python
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):  # ← This works IF password was hashed on registration
        login_user(user)
        return jsonify({'user': user.to_dict(), 'token': 'session-token'}), 200

    return jsonify({'error': 'Invalid credentials'}), 401
```

**Issue:** The registration code DOES hash the password with `generate_password_hash()`, but the database field is just called `password`. This is technically fine, but inconsistent with conventions.

**Recommendation:** Keep current approach (field is named `password`, it contains the hash). The code will work, but just understand that `user.password` contains the hashed value, not plaintext.

---

### 6. **Missing Recipe-User Many-to-Many Relationship**

**Severity:** HIGH - Collections feature won't work

**File:** `models.py`

**Problem:**
Collections should be a many-to-many relationship (users save recipes, recipes are saved by multiple users). Currently missing the junction table.

**Current Code (INCOMPLETE):**
```python
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    cuisine = db.Column(db.String(50))
    cook_time = db.Column(db.Integer)
    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan')
    instructions = db.relationship('Instruction', backref='recipe', cascade='all, delete-orphan')
    # ← MISSING: users relationship for collections
```

**Fix - Add junction table in `models.py`:**
```python
# Many-to-many association table
user_recipe_collection = db.Table(
    'user_recipe_collection',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('added_at', db.DateTime, default=db.func.now())
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    # ADD THIS RELATIONSHIP
    saved_recipes = db.relationship(
        'Recipe',
        secondary=user_recipe_collection,
        backref=db.backref('saved_by_users', lazy='dynamic'),
        lazy='dynamic'
    )

class Recipe(db.Model):
    # ... existing code ...
    # Recipe already has access to users via the backref above
```

**Fix - Update `collections.py` to use correct relationship:**
```python
@collections_bp.route('/', methods=['GET'])
@login_required
def get_collections():
    saved_recipes = current_user.saved_recipes.all()  # Changed from Recipe.query.filter()
    return jsonify({'recipes': [r.to_dict() for r in saved_recipes]}), 200
```

**Add endpoint to save/unsave recipes:**
```python
@collections_bp.route('/save/<int:recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe not in current_user.saved_recipes:
        current_user.saved_recipes.append(recipe)
        db.session.commit()
    return jsonify({'message': 'Recipe saved'}), 200

@collections_bp.route('/unsave/<int:recipe_id>', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.saved_recipes:
        current_user.saved_recipes.remove(recipe)
        db.session.commit()
    return jsonify({'message': 'Recipe removed'}), 200
```

---

### 7. **Missing Input Validation**

**Severity:** MEDIUM - Security risk

**Files:** `auth.py`, `recipes.py`

**Problem:** No validation of user input before database operations.

**Example Issues:**
```python
# auth.py line 14-15
username = data.get('username')
password = data.get('password')
# ↑ No length checks, no format validation
```

**Fix - Add validation helper (new file: `validators.py`):**
```python
def validate_username(username):
    if not username or len(username) < 3 or len(username) > 80:
        return False, "Username must be 3-80 characters"
    if not username.replace('_', '').replace('-', '').isalnum():
        return False, "Username must contain only alphanumeric characters, hyphens, and underscores"
    return True, None

def validate_password(password):
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters"
    return True, None

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None
```

**Fix - Update `auth.py`:**
```python
from .validators import validate_username, validate_password, validate_email

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Validate inputs
    valid, msg = validate_username(username)
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_email(email)
    if not valid:
        return jsonify({'error': msg}), 400
    
    valid, msg = validate_password(password)
    if not valid:
        return jsonify({'error': msg}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'user': new_user.to_dict()}), 201
```

---

### 8. **Missing Recipe Fields (Schema vs Code Mismatch)**

**Severity:** HIGH - API responses incomplete

**Problem:** 
Your project design and source code report specify many recipe fields that don't exist in the model:

**Missing Fields:**
- `source_url` (should link to original recipe)
- `source_website` (AllRecipes or Food Network)
- `prep_time_minutes`
- `servings`
- `difficulty`
- `image_url`
- `created_at` / `scraped_at`

**Current Model (INCOMPLETE):**
```python
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    cuisine = db.Column(db.String(50))
    cook_time = db.Column(db.Integer)  # ← Only cook time, no prep time
    # ← Missing many fields
```

**Fix - Update `models.py`:**
```python
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    source_url = db.Column(db.String(500), nullable=True)
    source_website = db.Column(db.String(50), nullable=True)  # "AllRecipes" or "Food Network"
    prep_time_minutes = db.Column(db.Integer, nullable=True)
    cook_time_minutes = db.Column(db.Integer, nullable=True)
    total_time_minutes = db.Column(db.Integer, nullable=True)
    servings = db.Column(db.Integer, default=4)
    difficulty = db.Column(db.String(20), nullable=True)  # "Easy", "Medium", "Hard"
    cuisine = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    scraped_at = db.Column(db.DateTime, nullable=True)
    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan')
    instructions = db.relationship('Instruction', backref='recipe', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'source_url': self.source_url,
            'source_website': self.source_website,
            'prep_time_minutes': self.prep_time_minutes,
            'cook_time_minutes': self.cook_time_minutes,
            'total_time_minutes': self.total_time_minutes,
            'servings': self.servings,
            'difficulty': self.difficulty,
            'cuisine': self.cuisine,
            'image_url': self.image_url,
            'ingredients': [i.to_dict() for i in self.ingredients],
            'instructions': [inst.to_dict() for inst in self.instructions]
        }
```

**Update Ingredient and Instruction to_dict:**
```python
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(20), nullable=True)  # "cup", "tsp", etc.
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit
        }

class Instruction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_number = db.Column(db.Integer, nullable=False)
    step_text = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def to_dict(self):
        return {
            'step_number': self.step_number,
            'step_text': self.step_text
        }
```

---

### 9. **Incomplete Recipe Search/Filter Endpoint**

**Severity:** HIGH - MVP feature not implemented

**File:** `recipes.py`

**Problem:** Search and filter endpoints are stubbed but incomplete.

**Current Code (INCOMPLETE):**
```python
@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    ingredient = request.args.get('ingredient')
    cuisine = request.args.get('cuisine')
    max_time = request.args.get('maxTime', type=int)

    query = Recipe.query

    if ingredient:
        query = query.join(Ingredient).filter(Ingredient.name.ilike(f'%{ingredient}%'))
    if cuisine:
        query = query.filter(Recipe.cuisine == cuisine)
    if max_time:
        query = query.filter(Recipe.cook_time <= max_time)

    recipes = query.all()
    return jsonify({'recipes': [r.to_dict() for r in recipes]}), 200
```

**Issues:**
1. No pagination (could return 300+ recipes at once)
2. Missing error handling
3. `cook_time` should be `cook_time_minutes` (if you update models)
4. No support for combined filters correctly

**Fix - Update `recipes.py`:**
```python
from flask import Blueprint, request, jsonify
from .models import Recipe, Ingredient
from . import db

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    """Get paginated list of all recipes with optional filters"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    ingredient = request.args.get('ingredient', '').strip()
    cuisine = request.args.get('cuisine', '').strip()
    max_time = request.args.get('maxTime', type=int)

    query = Recipe.query

    if ingredient:
        query = query.join(Ingredient).filter(
            Ingredient.name.ilike(f'%{ingredient}%')
        ).distinct()
    
    if cuisine:
        query = query.filter(Recipe.cuisine.ilike(f'%{cuisine}%'))
    
    if max_time:
        query = query.filter(Recipe.cook_time_minutes <= max_time)

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'recipes': [r.to_dict() for r in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }), 200

@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    """Get single recipe with full details"""
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict()), 200

@recipes_bp.route('/search', methods=['GET'])
def search_recipes():
    """Full-text search across recipe titles and descriptions"""
    query_str = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if not query_str or len(query_str) < 2:
        return jsonify({'error': 'Search query must be at least 2 characters'}), 400

    recipes = Recipe.query.filter(
        Recipe.title.ilike(f'%{query_str}%')
    ).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'recipes': [r.to_dict() for r in recipes.items],
        'total': recipes.total,
        'pages': recipes.pages,
        'current_page': page
    }), 200
```

---

### 10. **Missing CORS Configuration**

**Severity:** HIGH - Frontend can't call API

**File:** `__init__.py` or `app.py`

**Problem:** Frontend (Vue.js on different port) will get CORS errors when calling the API.

**Fix - Add Flask-CORS:**

First, update `requirements.txt`:
```
Flask>=2.0.0
Flask-SQLAlchemy>=3.0.0
Flask-Login>=0.6.0
Flask-CORS>=4.0.0
python-dotenv
werkzeug
```

Then update `__init__.py`:
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS  # ADD THIS
from . import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, supports_credentials=True)  # ADD THIS - Allow frontend to call API

    # Register blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from .recipes import recipes_bp
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')

    from .user_collections import collections_bp  # Updated name
    app.register_blueprint(collections_bp, url_prefix='/api/collections')

    return app
```

---

### 11. **Missing Error Handlers**

**Severity:** MEDIUM - Poor error responses

**File:** `app.py`

**Problem:** No global error handling, so 404s and 500s return default Flask responses.

**Fix - Add to `app.py`:**
```python
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Bad request'}), 400
```

---

## Summary of Issues by Priority

| Priority | Issue | File | Status |
|----------|-------|------|--------|
| CRITICAL | Module naming conflict (`collections.py`) | collections.py | MUST FIX NOW |
| HIGH | Missing user loader | __init__.py | Must fix before launch |
| HIGH | Missing email field | models.py | Must fix for registration |
| HIGH | Missing M2M relationship for collections | models.py | Must fix for collections feature |
| HIGH | Incomplete recipe model | models.py | Must fix for API responses |
| HIGH | Missing CORS | __init__.py | Must fix for frontend integration |
| MEDIUM | Missing input validation | auth.py | Should fix before Sprint 2 |
| MEDIUM | Incomplete search/filter | recipes.py | Should fix before Sprint 2 |
| MEDIUM | Missing error handlers | app.py | Should fix before Sprint 2 |

---

## Recommended Action Plan

**Immediate (Next 2 Hours):**
1. Rename `collections.py` to `user_collections.py`
2. Update imports in `__init__.py`
3. Test that app starts without import errors

**This Sprint (Before Nov 4 Sprint 1 end):**
1. Add user loader function
2. Update User model with email field
3. Add M2M relationship for collections
4. Complete Recipe model with all fields
5. Add Flask-CORS configuration
6. Test registration and login workflow

**Sprint 2:**
1. Add input validation
2. Complete search/filter endpoints with pagination
3. Add error handlers
4. Integration test entire auth flow

---

## Files to Review/Update

Create corrected versions:
- [ ] Rename: `collections.py` → `user_collections.py`
- [ ] Update: `__init__.py` (imports, user_loader, CORS)
- [ ] Update: `models.py` (all fields, M2M relationship)
- [ ] Update: `auth.py` (email field, validation)
- [ ] Update: `recipes.py` (pagination, complete search)
- [ ] Update: `app.py` (error handlers)
- [ ] Create: `validators.py` (input validation)
- [ ] Create/Update: `requirements.txt` (Flask-CORS)

---

## Next Steps

1. Start with the CRITICAL issue (rename collections.py)
2. Run the app locally to verify it starts
3. Test registration/login endpoints
4. Test recipe search
5. Test collections save/load

Would you like me to create corrected versions of these files ready to use?
