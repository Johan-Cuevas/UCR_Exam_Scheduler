## 1. Backend API Implementation

- [ ] 1.1 Set up Flask application structure with blueprints
- [ ] 1.2 Create ExamRepository class for JSON data access
- [ ] 1.3 Create ExamService class with search/filter logic
- [ ] 1.4 Implement `/api/exams` endpoint with pagination
- [ ] 1.5 Implement search query parameter (partial, case-insensitive matching)
- [ ] 1.6 Implement date filter parameter
- [ ] 1.7 Implement location filter parameter
- [ ] 1.8 Add `/api/filters/dates` endpoint for available dates
- [ ] 1.9 Add `/api/filters/locations` endpoint for available locations
- [ ] 1.10 Add input validation and sanitization
- [ ] 1.11 Add CORS configuration for frontend
- [ ] 1.12 Write pytest unit tests for ExamService
- [ ] 1.13 Write pytest integration tests for API endpoints
- [ ] 1.14 Update backend requirements.txt with new dependencies

## 2. Frontend Setup

- [ ] 2.1 Initialize Next.js project with TypeScript and Tailwind CSS
- [ ] 2.2 Configure ESLint and Prettier
- [ ] 2.3 Set up Jest and React Testing Library
- [ ] 2.4 Create TypeScript types for Exam data model
- [ ] 2.5 Create API client service for backend communication

## 3. Frontend Components

- [ ] 3.1 Create SearchBar component with input handling
- [ ] 3.2 Create FilterTabs component for date selection
- [ ] 3.3 Create FilterTabs component for location selection
- [ ] 3.4 Create ExamTable component with column formatting
- [ ] 3.5 Create ExamRow component for individual exam display
- [ ] 3.6 Create LoadingSpinner component
- [ ] 3.7 Create EmptyState component for no results
- [ ] 3.8 Create ErrorDisplay component

## 4. Frontend Features

- [ ] 4.1 Implement TanStack Query for data fetching
- [ ] 4.2 Implement infinite scroll pagination (without react-intersection-observer)
- [ ] 4.3 Connect search bar to API with debouncing
- [ ] 4.4 Connect filter tabs to API
- [ ] 4.5 Style components with modern Tailwind CSS theme
- [ ] 4.6 Ensure responsive table layout

## 5. Frontend Testing

- [ ] 5.1 Write unit tests for SearchBar component
- [ ] 5.2 Write unit tests for FilterTabs component
- [ ] 5.3 Write unit tests for ExamTable component
- [ ] 5.4 Write integration tests for main page with mocked API
- [ ] 5.5 Test loading and error states

## 6. Integration and Polish

- [ ] 6.1 Verify full stack integration locally
- [ ] 6.2 Add page title "FALL 2025 FINAL EXAMS"
- [ ] 6.3 Review accessibility (semantic HTML, keyboard navigation)
- [ ] 6.4 Final manual testing of search and filter combinations

## Dependencies

- Tasks 2.x and 3.x can be parallelized after 1.x backend is complete
- Task 4.x depends on components from 3.x
- Task 5.x can begin once corresponding components exist
- Task 6.x requires both frontend and backend to be complete
