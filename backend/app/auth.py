"""Authentication routes and logic"""
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from .validators import validate_username, validate_password, validate_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user account

    Expected JSON:
    {
        "username": "string",
        "email": "string",
        "password": "string"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
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

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user with credentials

    Expected JSON:
    {
        "username": "string",
        "password": "string"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400

        username = data.get('username', '').strip()
        password = data.get('password', '')

        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=data.get('remember', False))
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200

        return jsonify({'error': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout current user"""
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged-in user information"""
    return jsonify(current_user.to_dict()), 200


@auth_bp.route('/verify-token', methods=['GET'])
def verify_token():
    """Verify if current session is valid"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        }), 200

    return jsonify({'authenticated': False}), 401