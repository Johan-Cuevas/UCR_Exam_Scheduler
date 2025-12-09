# exam-scraper Specification

## Purpose
TBD - created by archiving change add-math-exam-scraper. Update Purpose after archive.
## Requirements
### Requirement: Exam Data Fetching

The system SHALL fetch final exam data from UCR's 25Live calendar API endpoint.

#### Scenario: Successful fetch with subject filter
- **WHEN** the scraper is run with subject filter "MATH"
- **THEN** the system fetches data from `https://25livepub.collegenet.com/calendars/final-exam-calendar.json?filter1=MATH`
- **AND** returns only exams matching the MATH subject code

#### Scenario: API unavailable
- **WHEN** the API endpoint is unreachable or returns an error
- **THEN** the system logs the error and exits gracefully without crashing

### Requirement: Exam Data Parsing

The system SHALL parse raw API responses and extract structured exam information.

#### Scenario: Parse exam title
- **WHEN** an exam has title "EXAM: MATH 009B 020 33515"
- **THEN** the system extracts subject="MATH", course_number="009B", section="020", crn="33515"

#### Scenario: Parse exam schedule
- **WHEN** an exam has startDateTime and endDateTime fields
- **THEN** the system preserves these as ISO 8601 formatted strings

#### Scenario: Parse exam location
- **WHEN** an exam has a location field
- **THEN** the system includes the location in the parsed output

#### Scenario: Handle missing fields
- **WHEN** an exam is missing optional fields (location, customFields)
- **THEN** the system uses null/empty values without failing

### Requirement: Exam Data Storage

The system SHALL save parsed exam data to a JSON file.

#### Scenario: Save to file
- **WHEN** exams are successfully fetched and parsed
- **THEN** the system writes the data to `backend/data/exams.json`
- **AND** the JSON is formatted with indentation for readability

#### Scenario: Output structure
- **WHEN** exams are saved
- **THEN** each exam object contains: subject, course_number, section, crn, course_name, start_time, end_time, location, term_code

