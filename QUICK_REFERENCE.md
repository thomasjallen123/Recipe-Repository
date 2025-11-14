# Backend Quick Reference

## File Changes Summary

| File | Status | Changes |
|------|--------|---------|
| `__init__.py` | ✅ UPDATED | Added user_loader, CORS, error handlers |
| `app.py` | ✅ UPDATED | Added error handlers, health endpoint |
| `config.py` | ✅ UPDATED | Complete config for dev/test/prod |
| `models.py` | ✅ UPDATED | Complete schema, M2M relationship |
| `auth.py` | ✅ UPDATED | Email field, validation, extra endpoints |
| `recipes.py` | ✅ UPDATED | Search, filter, pagination |
| `collections.py` | ❌ DELETE | Rename to `user_collections.py` |
| `user_collections.py` | ✨ NEW | Complete collections with M2M |
| `validators.py` | ✨ NEW | Input validation functions |
| `requirements.txt` | ✅ UPDATED | Added Flask-CORS |
| `.env.example` | ✨ NEW | Environment template |

---

## Critical Changes

### 1. MUST DO: Rename File
```bash
mv collections.py user_collections.py
```
Without this, the app won't start.

### 2. MUST DO: Install New Dependency
```bash
pip install -r requirements.txt
```
Flask-CORS is required for frontend integration.

### 3. MUST DO: Reinitialize Database
```bash
rm app.db
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## API Summary

### Auth
| Method | Endpoint | Auth | Response |
|--------|----------|------|----------|
| POST | `/api/auth/register` | No | User object |
| POST | `/api/auth/login` | No | User object |
| POST | `/api/auth/logout` | Yes | Message |
| GET | `/api/auth/me` | Yes | User object |
| GET | `/api/auth/verify-token` | No | {authenticated: bool} |

### Recipes
| Method | Endpoint | Params | Auth |
|--------|----------|--------|------|
| GET | `/api/recipes` | page, per_page, ingredient, cuisine, maxTime | No |
| GET | `/api/recipes/<id>` | - | No |
| GET | `/api/recipes/search` | q, page, per_page | No |
| GET | `/api/recipes/by-cuisine/<cuisine>` | page, per_page | No |
| GET | `/api/recipes/quick` | page, per_page | No |

### Collections
| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/api/collections` | Yes |
| POST | `/api/collections/save/<id>` | Yes |
| POST | `/api/collections/unsave/<id>` | Yes |
| GET | `/api/collections/is-saved/<id>` | Yes |
| POST | `/api/collections/add-multiple` | Yes |
| POST | `/api/collections/clear` | Yes |

---

## Common Tasks

### Test Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"pass1234"}'
```

### Test Search
```bash
curl "http://localhost:5000/api/recipes/search?q=chicken&page=1&per_page=20"
```

### Test Filter by Cuisine
```bash
curl "http://localhost:5000/api/recipes/by-cuisine/Italian?page=1"
```

### Test Save Recipe (requires login)
```bash
curl -X POST http://localhost:5000/api/collections/save/1 \
  -b cookies.txt
```

---

## Database Fields

### User
```python
id, username, email, password, created_at
```

### Recipe
```python
id, title, source_url, source_website,
prep_time_minutes, cook_time_minutes, total_time_minutes,
servings, difficulty, cuisine, image_url,
created_at, scraped_at
```

### Ingredient
```python
id, recipe_id, name, quantity, unit
```

### Instruction
```python
id, recipe_id, step_number, step_text
```

---

## Response Format

### Success (200)
```json
{
  "message": "Operation successful",
  "data": {...}
}
```

### Error (400/401/500)
```json
{
  "error": "Error description",
  "status": 400
}
```

### Paginated List
```json
{
  "recipes": [...],
  "total": 100,
  "pages": 5,
  "current_page": 1,
  "per_page": 20
}
```

---

## Validation Rules

### Username
- Required, 3-80 characters
- Only alphanumeric, hyphens, underscores

### Email
- Required, valid format
- Must not exceed 120 characters

### Password
- Required, at least 8 characters
- Must not exceed 200 characters

### Search Query
- Required, at least 2 characters
- Maximum 200 characters

### Pagination
- page: min 1
- per_page: min 1, max 100

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `ImportError: cannot import 'defaultdict'` | File named `collections.py` | Rename to `user_collections.py` |
| `No module named 'flask_cors'` | Missing dependency | `pip install -r requirements.txt` |
| `No such table: recipe` | Database not initialized | Delete `app.db` and reinitialize |
| `CORS error from frontend` | Origin not allowed | Update CORS config in `__init__.py` |
| `Invalid email already exists` | Duplicate email | Register with different email |

---

## Development Checklist

Before committing code:

- [ ] Run app without errors: `python app.py`
- [ ] Test health endpoint: `curl http://localhost:5000/health`
- [ ] Test registration works
- [ ] Test login works
- [ ] Test at least one recipe endpoint
- [ ] No console errors
- [ ] No database errors
- [ ] CORS headers present in responses

---

## File to Update Last: Frontend

After all backend changes work, update frontend:

1. Change `cook_time` → `cook_time_minutes`
2. Add email field to registration form
3. Add pagination handling
4. Update response parsing for new pagination fields

---

## Deployment Notes

For production:

1. Update `SECRET_KEY` in `.env`
2. Set `FLASK_ENV=production` in `.env`
3. Use PostgreSQL instead of SQLite
4. Update CORS origins to production URL
5. Enable HTTPS (set `SESSION_COOKIE_SECURE=True`)

---

## Quick Commands

```bash
# Start app
python app.py

# Test app
curl http://localhost:5000/

# Check database
python -c "from app import db; print(db.session.query(Recipe).count())"

# Reset database
rm app.db && python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ --cov
```

---

## Links

- Full Code Review: `BACKEND_CODE_REVIEW.md`
- Setup Guide: `BACKEND_SETUP_GUIDE.md`
- Migration Guide: `MIGRATION_GUIDE.md`
- API Docs: Use Postman or Swagger

Good luck!
