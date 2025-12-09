# backend/app/recipes.py — FINAL NUCLEAR FIX (copy-paste this entire file)
from flask import Blueprint, request, jsonify
from .models import Recipe
from . import db
import sqlalchemy as sa

recipes_bp = Blueprint('recipes', __name__)

@recipes_bp.route('/', methods=['GET'])
def get_recipes():
    ingredient = request.args.get('ingredient')
    cuisine = request.args.get('cuisine')
    max_time = request.args.get('maxTime', type=int)

    query = Recipe.query.options(
        sa.orm.joinedload(Recipe.ingredients),
        sa.orm.joinedload(Recipe.instructions)
    )

    if ingredient:
        query = query.join(Recipe.ingredients).filter(
            sa.func.lower(Ingredient.name).contains(ingredient.lower())
        )
    if cuisine:
        query = query.filter(sa.func.lower(Recipe.cuisine) == cuisine.lower())
    if max_time:
        query = query.filter(Recipe.total_time_minutes <= max_time)

    recipes = query.all()

    return jsonify({
        'recipes': [r.to_dict(include_details=True) for r in recipes]
    }), 200


@recipes_bp.route('/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    recipe = Recipe.query.options(
        sa.orm.joinedload(Recipe.ingredients),
        sa.orm.joinedload(Recipe.instructions)
    ).get_or_404(id)

    return jsonify(recipe.to_dict(include_details=True)), 200