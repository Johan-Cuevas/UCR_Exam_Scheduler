"""Flask application factory and configuration."""

from flask import Flask
from flask_cors import CORS

from api.routes.exams import exams_bp
from api.routes.filters import filters_bp
from api.routes.health import health_bp


def create_app(config: dict | None = None) -> Flask:
    """Create and configure the Flask application.
    
    Args:
        config: Optional configuration dictionary to override defaults.
        
    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Default configuration
    app.config.update({
        "JSON_SORT_KEYS": False,
        "CORS_ORIGINS": ["http://localhost:3000"],
    })
    
    # Override with provided config
    if config:
        app.config.update(config)
    
    # Configure CORS
    CORS(app, origins=app.config["CORS_ORIGINS"])
    
    # Register blueprints
    app.register_blueprint(exams_bp, url_prefix="/api")
    app.register_blueprint(filters_bp, url_prefix="/api/filters")
    app.register_blueprint(health_bp, url_prefix="/api")
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def register_error_handlers(app: Flask) -> None:
    """Register custom error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        return {"error": "Bad Request", "message": str(error.description)}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not Found", "message": "The requested resource was not found."}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal Server Error", "message": "An unexpected error occurred."}, 500
