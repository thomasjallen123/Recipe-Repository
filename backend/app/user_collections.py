# backend/app/user_collections.py
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Recipe
from . import db

collections_bp = Blueprint('collections', __name__)

@collections_bp.route('/', methods=['GET'])
@login_required
def get_collections():
    saved_recipes = current_user.saved_recipes.all()
    return jsonify({'recipes': [r.to_dict(include_details=True) for r in saved_recipes]}), 200

@collections_bp.route('/<int:recipe_id>/toggle', methods=['POST'])
@login_required
def toggle_save(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.saved_recipes:
        current_user.saved_recipes.remove(recipe)
        saved = False
    else:
        current_user.saved_recipes.append(recipe)
        saved = True
    db.session.commit()
    return jsonify({'saved': saved}), 200