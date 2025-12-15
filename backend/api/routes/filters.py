"""Filter API routes for dates and locations."""

from flask import Blueprint
from api.services.exam_service import ExamService

filters_bp = Blueprint("filters", __name__)

# Initialize service
_exam_service = ExamService()


@filters_bp.route("/dates", methods=["GET"])
def get_dates():
    """Get available exam dates.
    
    Returns:
        JSON response with list of unique exam dates in ISO format (YYYY-MM-DD),
        sorted chronologically.
    """
    dates = _exam_service.get_available_dates()
    return {"data": dates}


@filters_bp.route("/locations", methods=["GET"])
def get_locations():
    """Get available exam locations grouped by building.
    
    Returns:
        JSON response with locations grouped by building, sorted alphabetically.
    """
    locations = _exam_service.get_available_locations()
    return {"data": locations}
