"""Recipe routes and logic"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Recipe, Ingredient
from .validators import (
    validate_page_number, validate_per_page, validate_search_query
)

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    """Get paginated list of recipes with optional filters
    
    Query parameters:
    - page: int (default: 1)
    - per_page: int (default: 20, max: 100)
    - ingredient: str (filter by ingredient name)
    - cuisine: str (filter by cuisine type)
    - maxTime: int (filter by max cook time in minutes)
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        ingredient = request.args.get('ingredient', '').strip()
        cuisine = request.args.get('cuisine', '').strip()
        max_time = request.args.get('maxTime', type=int)

        # Validate pagination parameters
        valid, msg = validate_page_number(page)
        if not valid:
            return jsonify({'error': msg}), 400
        
        valid, msg = validate_per_page(per_page)
        if not valid:
            return jsonify({'error': msg}), 400

        query = Recipe.query

        # Filter by ingredient (joins with Ingredient table)
        if ingredient:
            query = query.join(Ingredient).filter(
                Ingredient.name.ilike(f'%{ingredient}%')
            ).distinct()
        
        # Filter by cuisine
        if cuisine:
            query = query.filter(Recipe.cuisine.ilike(f'%{cuisine}%'))
        
        # Filter by max cooking time
        if max_time:
            query = query.filter(Recipe.cook_time_minutes <= max_time)

        # Paginate results
        paginated = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return jsonify({
            'recipes': [r.to_dict(include_details=False) for r in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve recipes'}), 500


@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    """Get single recipe with full details including ingredients and instructions"""
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        return jsonify(recipe.to_dict(include_details=True)), 200
    except Exception as e:
        return jsonify({'error': 'Recipe not found'}), 404


@recipes_bp.route('/search', methods=['GET'])
def search_recipes():
    """Full-text search across recipe titles
    
    Query parameters:
    - q: str (search query, required, min 2 chars)
    - page: int (default: 1)
    - per_page: int (default: 20, max: 100)
    """
    try:
        query_str = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # Validate search query
        valid, msg = validate_search_query(query_str)
        if not valid:
            return jsonify({'error': msg}), 400

        # Validate pagination
        valid, msg = validate_page_number(page)
        if not valid:
            return jsonify({'error': msg}), 400
        
        valid, msg = validate_per_page(per_page)
        if not valid:
            return jsonify({'error': msg}), 400

        # Search recipes by title
        paginated = Recipe.query.filter(
            Recipe.title.ilike(f'%{query_str}%')
        ).paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'recipes': [r.to_dict(include_details=False) for r in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'query': query_str
        }), 200

    except Exception as e:
        return jsonify({'error': 'Search failed'}), 500


@recipes_bp.route('/by-cuisine/<cuisine>', methods=['GET'])
def get_recipes_by_cuisine(cuisine):
    """Get recipes filtered by cuisine type
    
    Path parameters:
    - cuisine: str (cuisine type, e.g., "Italian", "Thai")
    
    Query parameters:
    - page: int (default: 1)
    - per_page: int (default: 20, max: 100)
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        valid, msg = validate_page_number(page)
        if not valid:
            return jsonify({'error': msg}), 400
        
        valid, msg = validate_per_page(per_page)
        if not valid:
            return jsonify({'error': msg}), 400

        paginated = Recipe.query.filter(
            Recipe.cuisine.ilike(f'%{cuisine}%')
        ).paginate(page=page, per_page=per_page, error_out=False)

        if not paginated.items and page == 1:
            return jsonify({'error': f'No recipes found for cuisine: {cuisine}'}), 404

        return jsonify({
            'recipes': [r.to_dict(include_details=False) for r in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'cuisine': cuisine
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve recipes'}), 500


@recipes_bp.route('/quick', methods=['GET'])
def get_quick_recipes():
    """Get recipes with cooking time under 30 minutes
    
    Query parameters:
    - page: int (default: 1)
    - per_page: int (default: 20, max: 100)
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        valid, msg = validate_page_number(page)
        if not valid:
            return jsonify({'error': msg}), 400
        
        valid, msg = validate_per_page(per_page)
        if not valid:
            return jsonify({'error': msg}), 400

        paginated = Recipe.query.filter(
            Recipe.cook_time_minutes <= 30
        ).paginate(page=page, per_page=per_page, error_out=False)

        return jsonify({
            'recipes': [r.to_dict(include_details=False) for r in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page
        }), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve quick recipes'}), 500
