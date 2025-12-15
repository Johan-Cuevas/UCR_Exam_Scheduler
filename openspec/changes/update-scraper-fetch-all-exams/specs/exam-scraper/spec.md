## MODIFIED Requirements

### Requirement: Exam Data Fetching

The system SHALL fetch final exam data from UCR's 25Live calendar API endpoint.

#### Scenario: Fetch all exams without filter
- **WHEN** the scraper is run without a subject filter
- **THEN** the system fetches data from `https://25livepub.collegenet.com/calendars/final-exam-calendar.json`
- **AND** returns all exams from all departments

#### Scenario: Fetch exams with optional subject filter
- **WHEN** the scraper is run with an optional subject filter (e.g., "MATH")
- **THEN** the system fetches data from `https://25livepub.collegenet.com/calendars/final-exam-calendar.json?filter1=MATH`
- **AND** returns only exams matching the specified subject code

#### Scenario: API unavailable
- **WHEN** the API endpoint is unreachable or returns an error
- **THEN** the system logs the error and exits gracefully without crashing
