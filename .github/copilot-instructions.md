# Recipe Repository - AI Coding Agent Instructions

## Project Overview
This is a **Recipe Repository Capstone MVP** focused on building a web application that scrapes and manages recipes from AllRecipes and Food Network. The project follows a strict 6.5-week timeline (Oct 21 - Dec 5, 2025) with deployment to Heroku as the final deliverable.

**Current Status:** Early development phase (DataFramework branch)  
**Repository:** Recipe-Repository  
**Owner:** thomasjallen123  

## Architecture & Technology Stack

### Core Technology Stack (LOCKED - No Changes)
- **Backend:** Python 3.9+ with Flask 2.x, SQLAlchemy ORM, Flask-Login (session-based auth)
- **Frontend:** Vue.js 3 with Bootstrap 5, Vite build tool, Axios for HTTP
- **Database:** SQLite (local and production MVP)
- **Web Scraping:** Beautiful Soup 4 + Requests
- **Deployment:** Heroku with Gunicorn
- **Testing:** Pytest (backend), Jest optional (frontend)

### Expected Project Structure
```
recipe-repository/
├── backend/                    # Flask API server
│   ├── app.py                 # Main Flask application entry
│   ├── config.py              # Environment configurations
│   ├── requirements.txt       # Python dependencies
│   ├── app/
│   │   ├── models.py          # SQLAlchemy database models
│   │   ├── routes.py          # API endpoints
│   │   ├── auth.py            # Authentication logic
│   │   └── utils.py           # Helper functions
│   ├── scrapers/
│   │   ├── allrecipes.py      # AllRecipes scraper
│   │   ├── foodnetwork.py     # Food Network scraper
│   │   └── validation.py     # Data validation
│   └── tests/                 # Pytest test files
├── frontend/                   # Vue.js client application
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── views/             # Page-level components
│   │   └── services/api.js    # Centralized API client
│   └── package.json
├── docs/                      # Technical documentation
├── Procfile                   # Heroku deployment config
└── README.md                  # Project documentation
```

## Critical Development Guidelines

### Database Schema Patterns
The application uses a normalized SQLite schema with these core models:
- **users:** Authentication and user management
- **recipes:** Core recipe data with metadata (prep_time, cook_time, servings, etc.)
- **ingredients:** Related to recipes with quantity, unit, and name fields
- **instructions:** Step-by-step cooking instructions
- **user_collections:** Many-to-many relationship for saved recipes
- **dietary_tags:** Recipe categorization (Vegetarian, Vegan, etc.)

**Key Pattern:** Use cascade deletes and proper foreign key relationships:
```python
class Recipe(db.Model):
    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan')
    instructions = db.relationship('Instruction', backref='recipe', cascade='all, delete-orphan')
```

### API Endpoint Conventions
All API endpoints follow RESTful patterns under `/api/` prefix:
- **Authentication:** `/api/auth/register`, `/api/auth/login`, `/api/auth/logout`
- **Recipes:** `/api/recipes` (GET with filters), `/api/recipes/<id>` (GET), `/api/recipes/search` (GET)
- **Collections:** `/api/collections` (GET/POST), `/api/collections/<recipe_id>` (DELETE)
- **Recipe Scaling:** `/api/recipes/<id>/scale` (POST)

**Error Handling Pattern:** Always return consistent JSON error responses:
```python
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404
```

### Web Scraping Architecture
The scraping system is designed for reliability and data validation:
- **Modular scrapers:** Separate classes for AllRecipes and Food Network
- **CSS selectors over XPath:** More stable against HTML changes
- **Error handling:** Continue scraping on individual failures, log errors
- **Data validation:** Validate extracted data before database insertion
- **Rate limiting:** Add delays between requests to avoid blocking

**Scraper Pattern:**
```python
class AllRecipesScraper:
    def scrape_recipes(self, limit=100):
        recipes = []
        for page in range(1, limit // 10 + 1):
            try:
                # Scraping logic with error handling
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                # Extract and validate data
            except requests.RequestException as e:
                logger.error(f'Scraping failed: {e}')
                continue
        return recipes
```

### Vue.js Component Structure
Components follow Single File Component (SFC) pattern with Composition API:
- **Template:** Use Bootstrap 5 classes for styling
- **Script:** Use `setup()` with ref/reactive for state management
- **Error handling:** Display user-friendly error messages from API failures
- **Loading states:** Show spinners during API calls
- **Form validation:** Client-side validation with error display

**API Service Pattern:**
```javascript
// Centralized API client in services/api.js
const api = axios.create({
  baseURL: '/api',
  withCredentials: true  // For session-based auth
})

// Error interceptor for global error handling
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

### Authentication Strategy
The project uses **session-based authentication** (NOT JWT):
- Flask-Login for session management
- Secure password hashing with Werkzeug
- Session cookies with CSRF protection
- Login state persisted across browser sessions

## MVP Scope Constraints

### Must-Have Features (In Scope)
- User registration and login
- Recipe search by ingredient and filters (cuisine, cooking time)
- Recipe detail view with ingredients and instructions
- User collections (save/remove recipes)
- Recipe scaling (adjust serving sizes)
- Responsive design (mobile, tablet, desktop)
- 300-500 scraped recipes from both sites

### Phase 2 Features (Out of Scope)
- Admin dashboard or content management
- Machine learning recommendations
- Social features (ratings, comments, sharing)
- Advanced search ranking algorithms
- Nutritional analysis or dietary tracking
- Email notifications or user messaging
- Mobile native applications

## Testing Requirements
- **Backend:** 70% code coverage with Pytest, focus on API endpoints and authentication
- **Frontend:** Manual testing acceptable, Jest optional for critical components
- **Integration:** Test scraper functionality with small sample datasets
- **Performance:** API responses under 200ms, UI loads under 3 seconds

## Deployment Specifics
- **Platform:** Heroku free tier (primary) or Render (fallback)
- **Build:** Gunicorn for production WSGI server
- **Database:** SQLite file-based database (sufficient for MVP)
- **Environment:** Set Flask environment variables in Heroku dashboard
- **Assets:** Frontend built assets served by Flask for simplicity

## Development Workflow
- **Git:** Feature branches with descriptive names (`feature/recipe-scaling`)
- **Commits:** Conventional format (`feat:`, `fix:`, `docs:`, etc.)
- **Code Review:** All changes require pull request review
- **Testing:** All tests must pass before merge
- **Timeline:** Fixed deadline December 5, 2025 - scope reduction over deadline extension

## Common Implementation Patterns

### Database Queries with Pagination
```python
@api_bp.route('/recipes', methods=['GET'])
def get_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    query = Recipe.query
    if cuisine := request.args.get('cuisine'):
        query = query.filter_by(cuisine_type=cuisine)
    
    recipes = query.paginate(page=page, per_page=per_page)
    return jsonify({
        'recipes': [r.to_dict() for r in recipes.items],
        'total': recipes.total
    })
```

### Vue Component with API Integration
```vue
<script>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

export default {
  setup() {
    const recipes = ref([])
    const loading = ref(false)
    const error = ref('')
    
    const fetchRecipes = async () => {
      loading.value = true
      try {
        const response = await api.getAllRecipes()
        recipes.value = response.data.recipes
      } catch (err) {
        error.value = 'Failed to load recipes'
      } finally {
        loading.value = false
      }
    }
    
    onMounted(fetchRecipes)
    return { recipes, loading, error }
  }
}
</script>
```

## Critical File Locations
- **Database Models:** `backend/app/models.py` - Core data structure definitions
- **API Routes:** `backend/app/routes.py` - All REST endpoints
- **Scrapers:** `backend/scrapers/` - Data extraction logic
- **API Client:** `frontend/src/services/api.js` - Centralized HTTP client
- **Main Components:** `frontend/src/components/` - Reusable UI components
- **Configuration:** `backend/config.py` - Environment-specific settings

## When to Escalate
- **Scraper failures:** Blocks database population, immediate escalation needed
- **API/Database integration issues:** Affects entire backend, escalate quickly
- **Deployment problems:** Critical near deadline, requires immediate attention
- **Scope creep:** Any requests for Phase 2 features should be deferred to GitHub Issues

This project prioritizes **working software over perfect code** - focus on MVP functionality, reliable deployment, and meeting the December 5th deadline.