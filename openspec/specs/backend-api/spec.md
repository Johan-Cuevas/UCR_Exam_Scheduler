# backend-api Specification

## Purpose
TBD - created by archiving change add-exam-search-ui-and-api. Update Purpose after archive.
## Requirements
### Requirement: Exam List Endpoint

The system SHALL provide a GET endpoint at `/api/exams` to retrieve exam data with optional search and filters.

#### Scenario: Retrieve all exams
- **WHEN** a GET request is made to `/api/exams` with no parameters
- **THEN** the system returns a paginated list of all exams
- **AND** the response includes pagination metadata

#### Scenario: Paginated response format
- **WHEN** exams are retrieved
- **THEN** the response includes `data` array and `pagination` object with `page`, `limit`, `total`, and `hasMore` fields

### Requirement: Search Query Parameter

The system SHALL support a `q` query parameter for searching exams by course number or course name.

#### Scenario: Search by course number
- **WHEN** a GET request is made to `/api/exams?q=009B`
- **THEN** the system returns exams where course_number contains "009B"

#### Scenario: Search by course name
- **WHEN** a GET request is made to `/api/exams?q=calculus`
- **THEN** the system returns exams where course_name contains "calculus"

#### Scenario: Case-insensitive search
- **WHEN** a GET request is made to `/api/exams?q=CALC`
- **THEN** the search matches "CALCULUS", "Calculus", "calculus", etc.

#### Scenario: Partial match search
- **WHEN** a GET request is made to `/api/exams?q=calc`
- **THEN** the system returns exams containing "calc" anywhere in course_number or course_name

#### Scenario: Search by CRN
- **WHEN** a GET request is made to `/api/exams?q=35359`
- **THEN** the system returns exams where crn contains "35359"

### Requirement: Date Filter Parameter

The system SHALL support a `date` query parameter for filtering exams by date.

#### Scenario: Filter by date
- **WHEN** a GET request is made to `/api/exams?date=2025-12-08`
- **THEN** the system returns only exams scheduled on December 8, 2025

#### Scenario: Invalid date format
- **WHEN** a GET request is made with an invalid date format
- **THEN** the system returns a 400 error with a descriptive message

### Requirement: Location Filter Parameter

The system SHALL support a `location` query parameter for filtering exams by location.

#### Scenario: Filter by location
- **WHEN** a GET request is made to `/api/exams?location=SSC 335`
- **THEN** the system returns only exams at location "SSC 335"

#### Scenario: Location case sensitivity
- **WHEN** a GET request is made to `/api/exams?location=ssc 335`
- **THEN** the system matches locations case-insensitively

### Requirement: Pagination Parameters

The system SHALL support `page` and `limit` query parameters for pagination.

#### Scenario: Default pagination
- **WHEN** a GET request is made without pagination parameters
- **THEN** the system returns page 1 with 20 items (default limit)

#### Scenario: Custom page and limit
- **WHEN** a GET request is made to `/api/exams?page=2&limit=10`
- **THEN** the system returns the second page with 10 items

#### Scenario: Maximum limit enforced
- **WHEN** a GET request is made with `limit=500`
- **THEN** the system caps the limit at 100 items

#### Scenario: Invalid pagination values
- **WHEN** a GET request is made with negative or non-integer pagination values
- **THEN** the system returns a 400 error with a descriptive message

### Requirement: Combined Search and Filters

The system SHALL support combining search query with filters.

#### Scenario: Search with date filter
- **WHEN** a GET request is made to `/api/exams?q=calc&date=2025-12-08`
- **THEN** the system returns exams matching "calc" AND scheduled on December 8, 2025

#### Scenario: Search with location filter
- **WHEN** a GET request is made to `/api/exams?q=math&location=SSC 335`
- **THEN** the system returns exams matching "math" AND at location "SSC 335"

#### Scenario: All filters combined
- **WHEN** a GET request is made to `/api/exams?q=calc&date=2025-12-08&location=BRNHL A125`
- **THEN** the system returns exams matching all three criteria

### Requirement: Available Dates Endpoint

The system SHALL provide a GET endpoint at `/api/filters/dates` to retrieve available exam dates.

#### Scenario: Retrieve available dates
- **WHEN** a GET request is made to `/api/filters/dates`
- **THEN** the system returns a list of unique exam dates in ISO format (YYYY-MM-DD)
- **AND** dates are sorted in chronological order

#### Scenario: Dates response cached
- **WHEN** multiple requests are made to `/api/filters/dates`
- **THEN** the response is served from cache after the first request

### Requirement: Available Locations Endpoint

The system SHALL provide a GET endpoint at `/api/filters/locations` to retrieve available exam locations grouped by building.

#### Scenario: Retrieve available locations
- **WHEN** a GET request is made to `/api/filters/locations`
- **THEN** the system returns locations grouped by building
- **AND** each building contains a list of rooms
- **AND** buildings are sorted alphabetically

#### Scenario: Locations response cached
- **WHEN** multiple requests are made to `/api/filters/locations`
- **THEN** the response is served from cache after the first request

### Requirement: Health Check Endpoint

The system SHALL provide a GET endpoint at `/api/health` for health checks.

#### Scenario: Health check success
- **WHEN** a GET request is made to `/api/health`
- **THEN** the system returns HTTP 200 with status "healthy"

### Requirement: Input Validation

The system SHALL validate and sanitize all input parameters.

#### Scenario: SQL injection prevention
- **WHEN** a request contains potentially malicious characters
- **THEN** the system sanitizes input and does not execute unintended operations

#### Scenario: Query length limit
- **WHEN** a search query exceeds 100 characters
- **THEN** the system returns a 400 error indicating the query is too long

### Requirement: CORS Configuration

The system SHALL configure CORS to allow requests from the frontend origin.

#### Scenario: Frontend origin allowed
- **WHEN** a request is made from the configured frontend origin
- **THEN** the system includes appropriate CORS headers in the response

#### Scenario: Unknown origin blocked
- **WHEN** a request is made from an unknown origin
- **THEN** the system does not include CORS headers allowing the request

### Requirement: Error Response Format

The system SHALL return consistent error responses in JSON format.

#### Scenario: Error response structure
- **WHEN** an error occurs
- **THEN** the response includes `error` and `message` fields

#### Scenario: No internal details exposed
- **WHEN** an internal server error occurs
- **THEN** the error response does not expose stack traces or internal paths

### Requirement: Backend Testing

The system SHALL have comprehensive test coverage for API endpoints and business logic.

#### Scenario: Unit tests for ExamService
- **WHEN** tests are run
- **THEN** the ExamService class has unit tests for search and filter logic

#### Scenario: Integration tests for endpoints
- **WHEN** tests are run
- **THEN** all API endpoints have integration tests using Flask test client

#### Scenario: Edge case coverage
- **WHEN** tests are run
- **THEN** tests cover edge cases like empty results, invalid inputs, and boundary conditions

