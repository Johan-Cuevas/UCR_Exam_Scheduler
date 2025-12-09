"""Integration tests for API endpoints."""

import pytest


class TestHealthEndpoint:
    """Tests for the health check endpoint."""
    
    def test_health_check(self, client):
        """Test that health endpoint returns healthy status."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"


class TestExamsEndpoint:
    """Tests for the exams endpoint."""
    
    def test_get_all_exams(self, client):
        """Test getting all exams without filters."""
        response = client.get("/api/exams")
        
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert "pagination" in data
        assert len(data["data"]) == 4
    
    def test_search_by_query(self, client):
        """Test searching with query parameter."""
        response = client.get("/api/exams?q=009B")
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 1
        assert data["data"][0]["course_number"] == "009B"
    
    def test_search_case_insensitive(self, client):
        """Test case-insensitive search."""
        response = client.get("/api/exams?q=calculus")
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 1
    
    def test_search_by_crn(self, client):
        """Test searching by CRN."""
        response = client.get("/api/exams?q=35359")
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 1
        assert data["data"][0]["crn"] == "35359"
    
    def test_filter_by_date(self, client):
        """Test filtering by date."""
        response = client.get("/api/exams?date=2025-12-08")
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 2
    
    def test_filter_by_location(self, client):
        """Test filtering by location."""
        response = client.get("/api/exams?location=SSC 335")
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 1
    
    def test_combined_filters(self, client):
        """Test combining search and filters."""
        response = client.get("/api/exams?q=CALC&date=2025-12-08")
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 2
    
    def test_pagination_default(self, client):
        """Test default pagination values."""
        response = client.get("/api/exams")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["limit"] == 20
    
    def test_pagination_custom(self, client):
        """Test custom pagination values."""
        response = client.get("/api/exams?page=1&limit=2")
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["data"]) == 2
        assert data["pagination"]["page"] == 1
        assert data["pagination"]["limit"] == 2
        assert data["pagination"]["hasMore"] is True
    
    def test_pagination_max_limit(self, client):
        """Test that limit is capped at 100."""
        response = client.get("/api/exams?limit=500")
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["pagination"]["limit"] == 100
    
    def test_invalid_date_format(self, client):
        """Test error for invalid date format."""
        response = client.get("/api/exams?date=12-08-2025")
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "message" in data
    
    def test_invalid_pagination_values(self, client):
        """Test error for invalid pagination values."""
        response = client.get("/api/exams?page=-1")
        
        assert response.status_code == 400
    
    def test_invalid_pagination_type(self, client):
        """Test error for non-integer pagination values."""
        response = client.get("/api/exams?page=abc")
        
        assert response.status_code == 400
    
    def test_query_length_limit(self, client):
        """Test error for query exceeding length limit."""
        long_query = "a" * 101
        response = client.get(f"/api/exams?q={long_query}")
        
        assert response.status_code == 400


class TestFiltersEndpoints:
    """Tests for the filter endpoints."""
    
    def test_get_available_dates(self, client):
        """Test getting available dates."""
        response = client.get("/api/filters/dates")
        
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert len(data["data"]) == 3
        assert data["data"] == ["2025-12-08", "2025-12-09", "2025-12-10"]
    
    def test_get_available_locations(self, client):
        """Test getting available locations."""
        response = client.get("/api/filters/locations")
        
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert len(data["data"]) == 3
    
    def test_locations_grouped_by_building(self, client):
        """Test that locations are grouped by building."""
        response = client.get("/api/filters/locations")
        
        data = response.get_json()
        buildings = [loc["building"] for loc in data["data"]]
        assert "SSC" in buildings
        assert "BRNHL" in buildings
        assert "HMNSS" in buildings
    
    def test_locations_have_rooms(self, client):
        """Test that each building has rooms listed."""
        response = client.get("/api/filters/locations")
        
        data = response.get_json()
        for location in data["data"]:
            assert "building" in location
            assert "rooms" in location
            assert len(location["rooms"]) > 0


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_404_for_unknown_endpoint(self, client):
        """Test 404 for unknown endpoints."""
        response = client.get("/api/unknown")
        
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert "message" in data
    
    def test_error_response_format(self, client):
        """Test that error responses have consistent format."""
        response = client.get("/api/exams?date=invalid")
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "message" in data
