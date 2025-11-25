# Recipe routes and logic
from flask import Blueprint, request, jsonify
from .models import Recipe, Ingredient, Instruction
from . import db

recipes_bp = Blueprint('recipes', __name__)

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

@recipes_bp.route('/<int:id>', methods=['GET'])
def get_recipe_by_id(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify(recipe.to_dict()), 200
