"""Pytest fixtures for API testing."""

import pytest
from api.app import create_app
from api.repositories.exam_repository import ExamRepository
from api.services.exam_service import ExamService


@pytest.fixture
def sample_exams():
    """Sample exam data for testing."""
    return [
        {
            "subject": "MATH",
            "course_number": "006A",
            "section": "001",
            "crn": "35359",
            "course_name": "PRECALC: INTRO TO FUNC 1",
            "start_time": "2025-12-08T08:00:00",
            "end_time": "2025-12-08T11:00:00",
            "location": "SSC 335",
            "term_code": "202540"
        },
        {
            "subject": "MATH",
            "course_number": "009B",
            "section": "020",
            "crn": "33515",
            "course_name": "FIRST-YEAR CALCULUS",
            "start_time": "2025-12-08T08:00:00",
            "end_time": "2025-12-08T11:00:00",
            "location": "BRNHL A125",
            "term_code": "202540"
        },
        {
            "subject": "CS",
            "course_number": "010A",
            "section": "001",
            "crn": "12345",
            "course_name": "INTRO TO COMPUTER SCIENCE",
            "start_time": "2025-12-09T15:00:00",
            "end_time": "2025-12-09T18:00:00",
            "location": "SSC 235",
            "term_code": "202540"
        },
        {
            "subject": "PHYS",
            "course_number": "040A",
            "section": "001",
            "crn": "54321",
            "course_name": "GENERAL PHYSICS",
            "start_time": "2025-12-10T08:00:00",
            "end_time": "2025-12-10T11:00:00",
            "location": "HMNSS 1501",
            "term_code": "202540"
        }
    ]


class MockExamRepository(ExamRepository):
    """Mock repository that uses provided data instead of file."""
    
    def __init__(self, data: list[dict]):
        super().__init__()
        self._cache = data


@pytest.fixture
def mock_repository(sample_exams):
    """Create a mock repository with sample data."""
    return MockExamRepository(sample_exams)


@pytest.fixture
def exam_service(mock_repository):
    """Create an exam service with mock repository."""
    return ExamService(repository=mock_repository)


@pytest.fixture
def app(mock_repository, monkeypatch):
    """Create a test Flask application."""
    # Patch the global exam service to use our mock repository
    from api.routes import exams as exams_module
    from api.routes import filters as filters_module
    
    mock_service = ExamService(repository=mock_repository)
    monkeypatch.setattr(exams_module, "_exam_service", mock_service)
    monkeypatch.setattr(filters_module, "_exam_service", mock_service)
    
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()
