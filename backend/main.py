"""Main application entry point"""
from app import create_app, db
from flask import jsonify, send_from_directory
import os

app = create_app()


@app.route('/')
def index():
    """Root endpoint - API welcome message"""
    return jsonify({
        "message": "Welcome to the Recipe Repository API!",
        "version": "1.0",
        "endpoints": {
            "auth": "/api/auth",
            "recipes": "/api/recipes",
            "collections": "/api/collections"
        }
    }), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        "status": "healthy",
        "service": "Recipe Repository API"
    }), 200


@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    try:
        return send_from_directory(
            os.path.join(app.root_path, 'static'),
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
    except Exception:
        return '', 204


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return jsonify({
        'error': 'Bad request',
        'status': 400
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 Unauthorized errors"""
    return jsonify({
        'error': 'Unauthorized',
        'status': 401
    }), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors"""
    return jsonify({
        'error': 'Forbidden',
        'status': 403
    }), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return jsonify({
        'error': 'Resource not found',
        'status': 404
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors"""
    return jsonify({
        'error': 'Method not allowed',
        'status': 405
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    db.session.rollback()
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
