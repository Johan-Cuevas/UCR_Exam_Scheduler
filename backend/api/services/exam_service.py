"""Exam service for search and filter operations."""

from datetime import datetime
from functools import lru_cache
from api.repositories.exam_repository import ExamRepository


class ExamService:
    """Service class for exam search and filter operations."""
    
    def __init__(self, repository: ExamRepository | None = None):
        """Initialize the exam service.
        
        Args:
            repository: Optional exam repository instance. If not provided,
                       a default repository will be created.
        """
        self._repository = repository or ExamRepository()
    
    def search_exams(
        self,
        query: str | None = None,
        date: str | None = None,
        location: str | None = None,
        page: int = 1,
        limit: int = 20
    ) -> dict:
        """Search and filter exams with pagination.
        
        Args:
            query: Search query for course_number, course_name, or crn (case-insensitive).
            date: Filter by exam date (ISO format: YYYY-MM-DD).
            location: Filter by location (case-insensitive).
            page: Page number (1-indexed).
            limit: Number of items per page.
            
        Returns:
            Dictionary with 'data' (list of exams) and 'pagination' metadata.
        """
        exams = self._repository.get_all_exams()
        
        # Apply search filter
        if query:
            query_lower = query.lower()
            exams = [
                exam for exam in exams
                if query_lower in exam.get("course_number", "").lower()
                or query_lower in exam.get("course_name", "").lower()
                or query_lower in exam.get("crn", "").lower()
            ]
        
        # Apply date filter
        if date:
            exams = [
                exam for exam in exams
                if self._extract_date(exam.get("start_time", "")) == date
            ]
        
        # Apply location filter
        if location:
            location_lower = location.lower()
            exams = [
                exam for exam in exams
                if location_lower in exam.get("location", "").lower()
            ]
        
        # Calculate pagination
        total = len(exams)
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_exams = exams[start_index:end_index]
        has_more = end_index < total
        
        return {
            "data": paginated_exams,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "hasMore": has_more
            }
        }
    
    def get_available_dates(self) -> list[str]:
        """Get unique exam dates sorted chronologically.
        
        Returns:
            List of unique dates in ISO format (YYYY-MM-DD).
        """
        exams = self._repository.get_all_exams()
        dates = set()
        
        for exam in exams:
            date = self._extract_date(exam.get("start_time", ""))
            if date:
                dates.add(date)
        
        return sorted(dates)
    
    def get_available_locations(self) -> list[dict]:
        """Get unique exam locations grouped by building.
        
        Returns:
            List of dictionaries with 'building' and 'rooms' keys,
            sorted alphabetically by building.
        """
        exams = self._repository.get_all_exams()
        building_rooms: dict[str, set[str]] = {}
        
        for exam in exams:
            location = exam.get("location", "").strip()
            if location:
                # Extract building from location (first word)
                parts = location.split()
                building = parts[0] if parts else location
                
                if building not in building_rooms:
                    building_rooms[building] = set()
                building_rooms[building].add(location)
        
        # Convert to list format sorted by building
        result = [
            {"building": building, "rooms": sorted(rooms)}
            for building, rooms in sorted(building_rooms.items())
        ]
        
        return result
    
    @staticmethod
    def _extract_date(datetime_str: str) -> str | None:
        """Extract date from ISO datetime string.
        
        Args:
            datetime_str: ISO datetime string (e.g., "2025-12-08T08:00:00").
            
        Returns:
            Date string in YYYY-MM-DD format, or None if invalid.
        """
        if not datetime_str:
            return None
        try:
            dt = datetime.fromisoformat(datetime_str)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return None
