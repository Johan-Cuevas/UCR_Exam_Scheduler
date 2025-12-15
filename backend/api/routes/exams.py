"""Exam API routes."""

from flask import Blueprint, request, abort
from api.services.exam_service import ExamService
from api.validators import validate_pagination, validate_search_query, validate_date_format

exams_bp = Blueprint("exams", __name__)

# Initialize service
_exam_service = ExamService()


@exams_bp.route("/exams", methods=["GET"])
def get_exams():
    """Get exams with optional search and filters.
    
    Query Parameters:
        q: Search query (partial, case-insensitive match on course_number, course_name, crn)
        date: Filter by date (ISO format: YYYY-MM-DD)
        location: Filter by location (case-insensitive)
        page: Page number (default: 1)
        limit: Items per page (default: 20, max: 100)
        
    Returns:
        JSON response with exam data and pagination metadata.
    """
    # Extract and validate parameters
    search_query = request.args.get("q", "").strip()
    date_filter = request.args.get("date", "").strip()
    location_filter = request.args.get("location", "").strip()
    
    # Validate search query
    if search_query:
        error = validate_search_query(search_query)
        if error:
            abort(400, description=error)
    
    # Validate date format
    if date_filter:
        error = validate_date_format(date_filter)
        if error:
            abort(400, description=error)
    
    # Validate and parse pagination
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
    except ValueError:
        abort(400, description="Page and limit must be integers.")
    
    error = validate_pagination(page, limit)
    if error:
        abort(400, description=error)
    
    # Cap limit at 100
    limit = min(limit, 100)
    
    # Get filtered exams
    result = _exam_service.search_exams(
        query=search_query or None,
        date=date_filter or None,
        location=location_filter or None,
        page=page,
        limit=limit
    )
    
    return result
