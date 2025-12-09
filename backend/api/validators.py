"""Input validation utilities for API requests."""

import re
from datetime import datetime


def validate_search_query(query: str) -> str | None:
    """Validate search query parameter.
    
    Args:
        query: The search query string.
        
    Returns:
        Error message if validation fails, None if valid.
    """
    if len(query) > 100:
        return "Search query cannot exceed 100 characters."
    
    # Basic sanitization - allow alphanumeric, spaces, and common punctuation
    # This is defensive even though we use JSON file storage
    if not re.match(r'^[\w\s\-\.\'\"]+$', query, re.UNICODE):
        return "Search query contains invalid characters."
    
    return None


def validate_date_format(date_str: str) -> str | None:
    """Validate date format (ISO: YYYY-MM-DD).
    
    Args:
        date_str: The date string to validate.
        
    Returns:
        Error message if validation fails, None if valid.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."


def validate_pagination(page: int, limit: int) -> str | None:
    """Validate pagination parameters.
    
    Args:
        page: Page number.
        limit: Items per page.
        
    Returns:
        Error message if validation fails, None if valid.
    """
    if page < 1:
        return "Page must be a positive integer."
    
    if limit < 1:
        return "Limit must be a positive integer."
    
    return None
