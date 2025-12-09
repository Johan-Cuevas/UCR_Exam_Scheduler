"""Health check API route."""

from flask import Blueprint

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint.
    
    Returns:
        JSON response with status "healthy" and HTTP 200.
    """
    return {"status": "healthy"}
