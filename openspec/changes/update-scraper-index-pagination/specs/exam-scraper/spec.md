## MODIFIED Requirements

### Requirement: Exam Data Fetching

The system SHALL fetch final exam data from UCR's 25Live calendar XHR widget endpoint for a specific date range, including all paginated results.

#### Scenario: Fetch all exams for date range using index pagination
- **WHEN** the scraper is run
- **THEN** the system fetches data from `https://25livepub.collegenet.com/s.aspx?calendar=final-exam-calendar&widget=main&date={date}&index={index}&spudformat=xhr`
- **AND** iterates through dates from `20251206` through `20251212` (inclusive)
- **AND** for each date iterates `index` from `0` through `300` (inclusive) in increments of `25`
- **AND** returns the combined set of exams from all pages for all dates

#### Scenario: Stop early when there are no more pages
- **WHEN** the scraper requests an index page for a given date
- **AND** the payload contains no exam event rows OR no “next page” pagination hint
- **THEN** the scraper stops requesting higher index values for that date

#### Scenario: API unavailable
- **WHEN** the endpoint is unreachable or returns an error
- **THEN** the system logs the error (including `date` and `index`) and exits gracefully without crashing

#### Scenario: Payload parse failure
- **WHEN** the endpoint returns a successful HTTP response but the payload cannot be parsed
- **THEN** the system logs the error context (including `date` and `index`) and exits gracefully without crashing

### Requirement: Exam Data Parsing

The system SHALL parse XHR widget HTML and extract the same fields shown in the day table.

#### Scenario: Parse table fields
- **WHEN** an exam is present in the day table
- **THEN** the system extracts:
  - Final Exam (title text)
  - Exam Date (as displayed)
  - Start Time (as displayed)
  - Classroom (location text)

#### Scenario: Derive end time (+3 hours)
- **WHEN** an exam Start Time is parsed
- **THEN** the system computes End Time as Start Time + 3 hours
- **AND** formats Start Time and End Time using a 12-hour clock for America/Los_Angeles (PST for the requested dates)

#### Scenario: Preserve canonical datetimes for API consumers
- **WHEN** Start Time is parsed
- **THEN** the system stores a canonical ISO datetime value suitable for backend filtering (e.g., `YYYY-MM-DDTHH:MM:SS`)
- **AND** the derived End Time is also stored as a canonical ISO datetime value

### Requirement: Exam Data Storage

The system SHALL save parsed exam data to a JSON file.

#### Scenario: Save to file
- **WHEN** exams are successfully fetched and parsed
- **THEN** the system writes the data to `backend/data/exams.json`
- **AND** the JSON is formatted with indentation for readability

#### Scenario: Deduplicate across page queries
- **WHEN** the same exam appears in results from multiple requested pages and/or dates
- **THEN** the system returns a single exam record for that exam in the combined output
