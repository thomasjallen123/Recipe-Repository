"""Initialize the Flask app and database"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Enable CORS for frontend integration (supports credentials for sessions)
    CORS(app, supports_credentials=True, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # User loader callback for Flask-Login
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID from database"""
        return User.query.get(int(user_id))

    # Set login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this resource'

    # Register blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from .recipes import recipes_bp
    app.register_blueprint(recipes_bp, url_prefix='/api/recipes')

    from .user_collections import collections_bp
    app.register_blueprint(collections_bp, url_prefix='/api/collections')

    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return {'error': 'Bad request'}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 errors"""
        return {'error': 'Unauthorized'}, 401

    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors"""
        return {'error': 'Forbidden'}, 403

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return {'error': 'Internal server error'}, 500

    return app
