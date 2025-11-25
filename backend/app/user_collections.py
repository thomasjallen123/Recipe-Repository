# Collection routes and logic
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Recipe

collections_bp = Blueprint('collections', __name__)

@collections_bp.route('/', methods=['GET'])
@login_required
def get_collections():
    saved_recipes = Recipe.query.filter(Recipe.users.any(id=current_user.id)).all()
    return jsonify({'recipes': [r.to_dict() for r in saved_recipes]}), 200
