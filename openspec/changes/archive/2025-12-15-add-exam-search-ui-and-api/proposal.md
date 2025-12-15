# Change: Add Exam Search UI and API

## Why

Students need a modern, searchable interface to quickly find their final exam schedules. The current data exists (scraped and stored as JSON) but there's no way for users to access it. We need both a frontend interface with search/filter capabilities and a backend API to serve the exam data.

## What Changes

### Frontend (New Capability)
- Add a search bar for course number and course name queries
- Add filter tabs for exam date and location
- Display results in a responsive table with infinite scroll pagination (TanStack Query)
- Table columns: Final Exam (composite), Exam Date, Start Time, End Time, Classroom
- Modern, simple design using Tailwind CSS
- Jest + React Testing Library tests

### Backend API (New Capability)
- RESTful API endpoints for exam search and filtering
- Case-insensitive partial matching for search queries
- Separate filter endpoints for date and location
- JSON response format with pagination support
- Security best practices (input validation, rate limiting considerations)
- pytest test suite

## Impact

- Affected specs: None (new capabilities)
- New specs: `frontend`, `backend-api`
- Affected code:
  - `frontend/` - New Next.js application structure
  - `backend/` - New Flask API endpoints and service layer

## Decisions (Resolved)

1. **Pagination size**: 20 items per page (confirmed)
2. **Date filter format**: Individual dates (e.g., Dec 8, Dec 9)
3. **Location filter**: Grouped by building (e.g., SSC, BRNHL, HMNSS)
4. **Error handling UI**: 
   - No results: "No results found"
   - API failure: "Something went wrong on our end. Please try again later."
5. **Loading states**: Spinners (not skeleton loaders)
6. **Term selection**: Not needed right now (Fall 2025 only)
7. **CRN in search**: Yes, search should also match CRN numbers
8. **Timezone**: PST (Pacific Standard Time) - university is in California
9. **Filter caching**: Cache filter options (dates and locations)
10. **UI Library**: Tailwind CSS (per project conventions)
