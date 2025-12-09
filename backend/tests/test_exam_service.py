"""Unit tests for ExamService."""

import pytest
from api.services.exam_service import ExamService


class TestExamServiceSearch:
    """Tests for search functionality."""
    
    def test_search_by_course_number(self, exam_service):
        """Test searching by course number."""
        result = exam_service.search_exams(query="009B")
        
        assert len(result["data"]) == 1
        assert result["data"][0]["course_number"] == "009B"
    
    def test_search_by_course_name(self, exam_service):
        """Test searching by course name."""
        result = exam_service.search_exams(query="calculus")
        
        assert len(result["data"]) == 1
        assert "CALCULUS" in result["data"][0]["course_name"]
    
    def test_search_case_insensitive(self, exam_service):
        """Test that search is case-insensitive."""
        result_upper = exam_service.search_exams(query="CALCULUS")
        result_lower = exam_service.search_exams(query="calculus")
        result_mixed = exam_service.search_exams(query="CaLcUlUs")
        
        assert len(result_upper["data"]) == len(result_lower["data"]) == len(result_mixed["data"]) == 1
    
    def test_search_partial_match(self, exam_service):
        """Test partial matching in search."""
        result = exam_service.search_exams(query="CALC")
        
        # Should match PRECALC and CALCULUS
        assert len(result["data"]) == 2
    
    def test_search_by_crn(self, exam_service):
        """Test searching by CRN."""
        result = exam_service.search_exams(query="35359")
        
        assert len(result["data"]) == 1
        assert result["data"][0]["crn"] == "35359"
    
    def test_search_no_results(self, exam_service):
        """Test search with no matching results."""
        result = exam_service.search_exams(query="NONEXISTENT")
        
        assert len(result["data"]) == 0
        assert result["pagination"]["total"] == 0


class TestExamServiceDateFilter:
    """Tests for date filter functionality."""
    
    def test_filter_by_date(self, exam_service):
        """Test filtering by date."""
        result = exam_service.search_exams(date="2025-12-08")
        
        assert len(result["data"]) == 2
        for exam in result["data"]:
            assert exam["start_time"].startswith("2025-12-08")
    
    def test_filter_by_date_no_results(self, exam_service):
        """Test date filter with no matching results."""
        result = exam_service.search_exams(date="2025-01-01")
        
        assert len(result["data"]) == 0


class TestExamServiceLocationFilter:
    """Tests for location filter functionality."""
    
    def test_filter_by_location(self, exam_service):
        """Test filtering by location."""
        result = exam_service.search_exams(location="SSC 335")
        
        assert len(result["data"]) == 1
        assert result["data"][0]["location"] == "SSC 335"
    
    def test_filter_by_location_case_insensitive(self, exam_service):
        """Test that location filter is case-insensitive."""
        result = exam_service.search_exams(location="ssc 335")
        
        assert len(result["data"]) == 1
    
    def test_filter_by_building(self, exam_service):
        """Test filtering by building (partial match)."""
        result = exam_service.search_exams(location="SSC")
        
        assert len(result["data"]) == 2  # SSC 335 and SSC 235


class TestExamServiceCombinedFilters:
    """Tests for combined search and filters."""
    
    def test_search_with_date_filter(self, exam_service):
        """Test combining search query with date filter."""
        result = exam_service.search_exams(query="CALC", date="2025-12-08")
        
        assert len(result["data"]) == 2
        for exam in result["data"]:
            assert "CALC" in exam["course_name"].upper()
    
    def test_search_with_location_filter(self, exam_service):
        """Test combining search query with location filter."""
        result = exam_service.search_exams(query="006A", location="SSC")
        
        assert len(result["data"]) == 1
    
    def test_all_filters_combined(self, exam_service):
        """Test combining all filters."""
        result = exam_service.search_exams(
            query="PRECALC",
            date="2025-12-08",
            location="SSC"
        )
        
        assert len(result["data"]) == 1
        assert result["data"][0]["crn"] == "35359"


class TestExamServicePagination:
    """Tests for pagination functionality."""
    
    def test_default_pagination(self, exam_service):
        """Test default pagination values."""
        result = exam_service.search_exams()
        
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["limit"] == 20
        assert result["pagination"]["total"] == 4
        assert result["pagination"]["hasMore"] is False
    
    def test_custom_pagination(self, exam_service):
        """Test custom pagination values."""
        result = exam_service.search_exams(page=1, limit=2)
        
        assert len(result["data"]) == 2
        assert result["pagination"]["page"] == 1
        assert result["pagination"]["limit"] == 2
        assert result["pagination"]["total"] == 4
        assert result["pagination"]["hasMore"] is True
    
    def test_second_page(self, exam_service):
        """Test getting second page of results."""
        result = exam_service.search_exams(page=2, limit=2)
        
        assert len(result["data"]) == 2
        assert result["pagination"]["page"] == 2
        assert result["pagination"]["hasMore"] is False
    
    def test_page_beyond_results(self, exam_service):
        """Test requesting a page beyond available results."""
        result = exam_service.search_exams(page=10, limit=20)
        
        assert len(result["data"]) == 0
        assert result["pagination"]["hasMore"] is False


class TestExamServiceAvailableDates:
    """Tests for getting available dates."""
    
    def test_get_available_dates(self, exam_service):
        """Test getting available dates."""
        dates = exam_service.get_available_dates()
        
        assert len(dates) == 3
        assert dates == ["2025-12-08", "2025-12-09", "2025-12-10"]
    
    def test_dates_are_sorted(self, exam_service):
        """Test that dates are sorted chronologically."""
        dates = exam_service.get_available_dates()
        
        assert dates == sorted(dates)


class TestExamServiceAvailableLocations:
    """Tests for getting available locations."""
    
    def test_get_available_locations(self, exam_service):
        """Test getting available locations grouped by building."""
        locations = exam_service.get_available_locations()
        
        assert len(locations) == 3  # BRNHL, HMNSS, SSC
    
    def test_locations_grouped_by_building(self, exam_service):
        """Test that locations are grouped by building."""
        locations = exam_service.get_available_locations()
        
        buildings = [loc["building"] for loc in locations]
        assert "SSC" in buildings
        assert "BRNHL" in buildings
        assert "HMNSS" in buildings
    
    def test_locations_sorted_alphabetically(self, exam_service):
        """Test that buildings are sorted alphabetically."""
        locations = exam_service.get_available_locations()
        
        buildings = [loc["building"] for loc in locations]
        assert buildings == sorted(buildings)
    
    def test_rooms_within_building(self, exam_service):
        """Test that rooms are listed within each building."""
        locations = exam_service.get_available_locations()
        
        ssc = next(loc for loc in locations if loc["building"] == "SSC")
        assert "SSC 335" in ssc["rooms"]
        assert "SSC 235" in ssc["rooms"]
