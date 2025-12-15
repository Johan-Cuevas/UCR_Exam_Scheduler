# frontend Specification

## Purpose
TBD - created by archiving change add-exam-search-ui-and-api. Update Purpose after archive.
## Requirements
### Requirement: Exam Search Interface

The system SHALL provide a search bar that allows users to search for exams by course number or course name.

#### Scenario: Search by course number
- **WHEN** user enters "009B" in the search bar
- **THEN** the system displays all exams matching course number "009B"
- **AND** results include partial matches (e.g., "009B" matches "MATH 009B")

#### Scenario: Search by course name
- **WHEN** user enters "Calculus" in the search bar
- **THEN** the system displays all exams with "Calculus" in the course name
- **AND** search is case-insensitive

#### Scenario: Partial search match
- **WHEN** user enters "CALC" in the search bar
- **THEN** the system displays exams containing "CALC" in course number or name
- **AND** matches include "CALCULUS", "PRECALC", etc.

#### Scenario: Search by CRN
- **WHEN** user enters "35359" in the search bar
- **THEN** the system displays exams with CRN matching "35359"

#### Scenario: Empty search
- **WHEN** user clears the search bar
- **THEN** the system displays all exams (subject to active filters)

### Requirement: Date Filter

The system SHALL provide a filter tab for selecting exam dates.

#### Scenario: Filter by specific date
- **WHEN** user selects a date from the date filter tabs
- **THEN** the system displays only exams scheduled for that date

#### Scenario: Clear date filter
- **WHEN** user deselects the date filter (or selects "All")
- **THEN** the system displays exams for all dates

#### Scenario: Date options populated from data
- **WHEN** the page loads
- **THEN** the date filter options are populated from available exam dates in the data

### Requirement: Location Filter

The system SHALL provide a filter tab for selecting exam locations grouped by building.

#### Scenario: Filter by building
- **WHEN** user selects a building (e.g., "SSC") from the location filter tabs
- **THEN** the system displays only exams at locations within that building

#### Scenario: Filter by specific room
- **WHEN** user selects a specific room (e.g., "SSC 335") from the location filter
- **THEN** the system displays only exams at that specific room

#### Scenario: Clear location filter
- **WHEN** user deselects the location filter (or selects "All")
- **THEN** the system displays exams for all locations

#### Scenario: Location options grouped by building
- **WHEN** the page loads
- **THEN** the location filter options are grouped by building (e.g., SSC, BRNHL, HMNSS)

### Requirement: Exam Results Table

The system SHALL display search results in a responsive table with specific column formatting.

#### Scenario: Table columns displayed
- **WHEN** exam results are displayed
- **THEN** the table shows columns: Final Exam, Exam Date, Start Time, End Time, Classroom

#### Scenario: Final Exam column format
- **WHEN** an exam with subject="MATH", course_number="006A", section="040", crn="35359" is displayed
- **THEN** the Final Exam column shows "EXAM: MATH 006A 040 35359"

#### Scenario: Exam Date column format
- **WHEN** an exam with start_time="2025-12-08T08:00:00" is displayed
- **THEN** the Exam Date column shows "Dec 8"

#### Scenario: Start Time column format
- **WHEN** an exam with start_time="2025-12-08T08:00:00" is displayed
- **THEN** the Start Time column shows "8am"

#### Scenario: End Time column format
- **WHEN** an exam with end_time="2025-12-08T11:00:00" is displayed
- **THEN** the End Time column shows "11am"

#### Scenario: Classroom column format
- **WHEN** an exam with location="SSC 335" is displayed
- **THEN** the Classroom column shows "SSC 335"

#### Scenario: Times displayed in PST
- **WHEN** exam times are displayed
- **THEN** the times are shown in Pacific Standard Time (PST)

### Requirement: Table Title

The system SHALL display a title above the exam results table.

#### Scenario: Table title displayed
- **WHEN** the exam table is rendered
- **THEN** the title "FALL 2025 FINAL EXAMS" is displayed above the table

### Requirement: Responsive Table Layout

The system SHALL provide a responsive table that resizes with the browser window.

#### Scenario: Table resizes with window
- **WHEN** user resizes the browser window
- **THEN** the table adjusts its width to fit the available space

#### Scenario: Columns remain readable
- **WHEN** the window is resized
- **THEN** all column content remains visible and readable

### Requirement: Infinite Scroll Pagination

The system SHALL implement infinite scroll for loading additional exam results.

#### Scenario: Initial page load
- **WHEN** the page first loads
- **THEN** the first page of results is displayed (default 20 items)

#### Scenario: Scroll to load more
- **WHEN** user scrolls to the bottom of the results
- **THEN** the next page of results is automatically loaded and appended

#### Scenario: All results loaded
- **WHEN** all available results have been loaded
- **THEN** no additional API calls are made when scrolling

#### Scenario: Loading indicator
- **WHEN** additional results are being fetched
- **THEN** a loading indicator is displayed at the bottom of the table

### Requirement: Modern UI Theme

The system SHALL use a modern, clean visual design with Tailwind CSS.

#### Scenario: Consistent styling
- **WHEN** the page is displayed
- **THEN** components use consistent colors, spacing, and typography

#### Scenario: Visual simplicity
- **WHEN** users interact with the interface
- **THEN** the design emphasizes clarity and ease of use

### Requirement: Loading States

The system SHALL display spinner loading indicators during data fetching.

#### Scenario: Initial loading
- **WHEN** the page first loads and data is being fetched
- **THEN** a spinner is displayed

#### Scenario: Search loading
- **WHEN** a search query is submitted
- **THEN** a spinner is displayed while results are fetched

### Requirement: Empty State

The system SHALL display "No results found" when no results are found.

#### Scenario: No matching results
- **WHEN** a search or filter returns no results
- **THEN** the system displays "No results found"

### Requirement: Error Handling

The system SHALL gracefully handle API errors with a user-friendly message.

#### Scenario: API error
- **WHEN** the API returns an error
- **THEN** the system displays "Something went wrong on our end. Please try again later."
- **AND** does not crash

### Requirement: Frontend Testing

The system SHALL have comprehensive test coverage for components and features.

#### Scenario: Component unit tests
- **WHEN** tests are run
- **THEN** all components have unit tests covering their primary functionality

#### Scenario: Integration tests
- **WHEN** tests are run
- **THEN** the main page has integration tests with mocked API responses

