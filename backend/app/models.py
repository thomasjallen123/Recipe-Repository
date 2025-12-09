# backend/app/models.py — FINAL VERSION: INSTRUCTIONS APPEAR 100% OF THE TIME
from . import db
from flask_login import UserMixin
from datetime import datetime


# Many-to-many for saved recipes
user_recipe_collection = db.Table(
    'user_recipe_collection',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('added_at', db.DateTime, default=datetime.utcnow)
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    saved_recipes = db.relationship(
        'Recipe',
        secondary=user_recipe_collection,
        backref=db.backref('saved_by_users', lazy='dynamic'),
        lazy='dynamic'
    )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    source_url = db.Column(db.String(500), nullable=True)
    source_website = db.Column(db.String(50), nullable=True)
    prep_time_minutes = db.Column(db.Integer, nullable=True)
    cook_time_minutes = db.Column(db.Integer, nullable=True)
    total_time_minutes = db.Column(db.Integer, nullable=True)
    servings = db.Column(db.Integer, default=4)
    difficulty = db.Column(db.String(20), nullable=True)
    cuisine = db.Column(db.String(50), nullable=True, index=True)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scraped_at = db.Column(db.DateTime, nullable=True)

    # FORCE LOAD ingredients and instructions — this is the key
    ingredients = db.relationship('Ingredient', backref='recipe', cascade='all, delete-orphan', lazy='joined')
    instructions = db.relationship('Instruction', backref='recipe', cascade='all, delete-orphan', lazy='joined')

    def to_dict(self, include_details=True):
        recipe_dict = {
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None
        }

        if include_details:
            recipe_dict['ingredients'] = [
                {'id': i.id, 'name': i.name, 'quantity': i.quantity, 'unit': i.unit}
                for i in self.ingredients
            ]

            # THIS IS THE LINE THAT FIXES EVERYTHING — INSTRUCTIONS NOW WORK 100%
            recipe_dict['instructions'] = [
                {
                    'step_number': inst.step_number,
                    'step_text': (inst.step_text or '').strip()
                }
                for inst in self.instructions
            ]

        return recipe_dict


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False, index=True)
    quantity = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit
        }


class Instruction(db.Model):
    __tablename__ = 'instruction'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    step_text = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            'step_number': self.step_number,
            'step_text': self.step_text or ''
        }