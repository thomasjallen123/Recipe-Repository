"""User recipe collections routes and logic"""
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Recipe
from . import db

collections_bp = Blueprint('collections', __name__)


@collections_bp.route('/', methods=['GET'])
@login_required
def get_user_collections():
    """Get all recipes in current user's collection"""
    try:
        saved_recipes = current_user.saved_recipes.all()
        
        return jsonify({
            'recipes': [r.to_dict(include_details=False) for r in saved_recipes],
            'total': len(saved_recipes)
        }), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve collection'}), 500


@collections_bp.route('/save/<int:recipe_id>', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    """Add recipe to user's collection
    
    Path parameters:
    - recipe_id: int (ID of recipe to save)
    """
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        
        # Check if already saved
        if recipe in current_user.saved_recipes:
            return jsonify({'message': 'Recipe already in collection'}), 200
        
        # Add to collection
        current_user.saved_recipes.append(recipe)
        db.session.commit()
        
        return jsonify({
            'message': 'Recipe saved successfully',
            'recipe': recipe.to_dict(include_details=False)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save recipe'}), 500


@collections_bp.route('/unsave/<int:recipe_id>', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    """Remove recipe from user's collection
    
    Path parameters:
    - recipe_id: int (ID of recipe to remove)
    """
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        
        # Check if in collection
        if recipe not in current_user.saved_recipes:
            return jsonify({'message': 'Recipe not in collection'}), 200
        
        # Remove from collection
        current_user.saved_recipes.remove(recipe)
        db.session.commit()
        
        return jsonify({'message': 'Recipe removed from collection'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to remove recipe'}), 500


@collections_bp.route('/is-saved/<int:recipe_id>', methods=['GET'])
@login_required
def is_recipe_saved(recipe_id):
    """Check if recipe is in user's collection
    
    Path parameters:
    - recipe_id: int (ID of recipe to check)
    """
    try:
        recipe = Recipe.query.get_or_404(recipe_id)
        is_saved = recipe in current_user.saved_recipes
        
        return jsonify({'is_saved': is_saved}), 200
    
    except Exception as e:
        return jsonify({'error': 'Failed to check recipe status'}), 500


@collections_bp.route('/add-multiple', methods=['POST'])
@login_required
def add_multiple_recipes():
    """Add multiple recipes to collection
    
    Expected JSON:
    {
        "recipe_ids": [1, 2, 3, ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'recipe_ids' not in data:
            return jsonify({'error': 'recipe_ids array is required'}), 400
        
        recipe_ids = data.get('recipe_ids', [])
        
        if not isinstance(recipe_ids, list):
            return jsonify({'error': 'recipe_ids must be an array'}), 400
        
        if len(recipe_ids) > 100:
            return jsonify({'error': 'Cannot add more than 100 recipes at once'}), 400
        
        added_count = 0
        errors = []
        
        for recipe_id in recipe_ids:
            try:
                recipe = Recipe.query.get(recipe_id)
                if recipe and recipe not in current_user.saved_recipes:
                    current_user.saved_recipes.append(recipe)
                    added_count += 1
                elif not recipe:
                    errors.append(f'Recipe {recipe_id} not found')
            except Exception as e:
                errors.append(f'Failed to add recipe {recipe_id}')
        
        db.session.commit()
        
        return jsonify({
            'message': f'Added {added_count} recipes to collection',
            'added': added_count,
            'errors': errors if errors else None
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add recipes'}), 500


@collections_bp.route('/clear', methods=['POST'])
@login_required
def clear_collection():
    """Clear all recipes from user's collection"""
    try:
        count = current_user.saved_recipes.count()
        current_user.saved_recipes.delete()
        db.session.commit()
        
        return jsonify({
            'message': f'Cleared {count} recipes from collection',
            'cleared': count
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to clear collection'}), 500
