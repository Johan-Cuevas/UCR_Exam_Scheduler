## MODIFIED Requirements

### Requirement: Exam Data Fetching

The system SHALL fetch final exam data from UCR's 25Live calendar XHR widget endpoint for a specific date range.

#### Scenario: Fetch all exams for date range
- **WHEN** the scraper is run
- **THEN** the system fetches data from `https://25livepub.collegenet.com/s.aspx?hosted=1&calendar=final-exam-calendar&widget=main&date={date}&spudformat=xhr`
- **AND** iterates through dates from `20251206` through `20251212`
- **AND** populates the `date` query parameter with each date in YYYYMMDD format
- **AND** returns all exams from all departments for the date range

#### Scenario: API unavailable
- **WHEN** the API endpoint is unreachable or returns an error
- **THEN** the system logs the error and exits gracefully without crashing

#### Scenario: Date field extraction
- **WHEN** exams are fetched for a specific date
- **THEN** the system extracts and stores the date from the exam data
