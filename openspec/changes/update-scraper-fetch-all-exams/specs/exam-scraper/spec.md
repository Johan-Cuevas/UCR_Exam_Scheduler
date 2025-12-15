## MODIFIED Requirements

### Requirement: Exam Data Fetching

The system SHALL fetch final exam data from UCR's 25Live calendar XHR widget endpoint for a specific date range.

#### Scenario: Fetch all exams for date range
- **WHEN** the scraper is run
- **THEN** the system fetches data from `https://25livepub.collegenet.com/s.aspx?hosted=1&calendar=final-exam-calendar&widget=main&date={date}&spudformat=xhr`
- **AND** iterates through dates from `20251206` through `20251212`
- **AND** populates the `date` query parameter with each date in YYYYMMDD format
- **AND** returns all exams from all departments for the date range
- **AND** does not filter exams by subject/department

#### Scenario: API unavailable
- **WHEN** the API endpoint is unreachable or returns an error
- **THEN** the system logs the error and exits gracefully without crashing

#### Scenario: Payload parse failure
- **WHEN** the endpoint returns a successful HTTP response but the payload cannot be parsed
- **THEN** the system logs the error context (including the requested `date`) and exits gracefully without crashing

#### Scenario: Date field extraction
- **WHEN** exams are fetched for a specific date
- **THEN** the system stores a `date` field on each exam record
- **AND** the `date` field uses `YYYYMMDD` format
- **AND** the `date` field MUST represent the query date unless a stronger source of truth is available in the payload

#### Scenario: Deduplicate across date queries
- **WHEN** the same exam appears in results from multiple requested dates
- **THEN** the system returns a single exam record for that exam in the combined output
