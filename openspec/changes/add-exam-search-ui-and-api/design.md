## Context

This change introduces two new capabilities: a React/Next.js frontend for searching final exams and a Flask REST API backend to serve the exam data. The exam data already exists in `backend/data/exams.json` (populated by the exam-scraper capability).

**Stakeholders:**
- Students searching for their final exam schedules
- Developers maintaining the codebase

**Constraints:**
- Must run locally without authentication
- Frontend must be responsive but mobile view not required
- Backend must be secure even for local use

## Goals / Non-Goals

### Goals
- Provide a fast, intuitive search experience for finding exams
- Support partial, case-insensitive matching on course number and name
- Allow filtering by exam date and location
- Use infinite scroll for smooth pagination experience
- Follow RESTful conventions for API design
- Maintain security best practices

### Non-Goals
- Mobile-optimized UI (responsive desktop is sufficient)
- User authentication/authorization
- Database storage (continue using JSON file)
- Multi-term support (Fall 2025 only for now)
- Advanced analytics or search history

## Decisions

### Decision 1: TanStack Query for Data Fetching
- **What**: Use TanStack Query (React Query) for API data fetching and caching
- **Why**: Provides built-in infinite scroll support, caching, background refetching, and loading states. Well-documented and widely adopted.
- **Alternatives considered**: 
  - SWR: Similar features but TanStack Query has better infinite query support
  - Plain fetch: Would require manual state management for pagination

### Decision 2: Native Scroll Event for Infinite Scroll
- **What**: Use native scroll event listener instead of react-intersection-observer
- **Why**: User explicitly requested no react-intersection-observer. Native scroll events are sufficient for this use case.
- **Trade-off**: Slightly more code but fewer dependencies

### Decision 3: Flask with Blueprints
- **What**: Organize API using Flask blueprints for modular routing
- **Why**: Matches project.md conventions and keeps code organized as we add endpoints
- **Alternatives considered**:
  - FastAPI: Would require learning curve change; Flask is specified in project.md
  - Single file: Less maintainable as endpoints grow

### Decision 4: Layered Backend Architecture
- **What**: Separate Repository (data access), Service (business logic), and API (HTTP) layers
- **Why**: Matches project.md architecture patterns, enables unit testing of each layer
- **Alternatives considered**:
  - Flat structure: Harder to test and maintain

### Decision 5: Client-Side Filtering vs Server-Side
- **What**: All filtering and searching performed server-side
- **Why**: More efficient with larger datasets, reduces client bundle, centralizes logic
- **Trade-off**: More API calls but better scalability

### Decision 6: Date and Location as Separate Filter Endpoints
- **What**: Provide `/api/filters/dates` and `/api/filters/locations` to fetch available filter options
- **Why**: Allows dynamic filter UI based on actual data, supports future expansion
- **Alternatives considered**:
  - Hardcoded filters: Inflexible if data changes

## Data Flow

```
┌─────────────┐    HTTP/JSON    ┌─────────────────┐
│   Next.js   │ ◄──────────────►│   Flask API     │
│  Frontend   │                 │                 │
└─────────────┘                 └────────┬────────┘
                                         │
                                         ▼
                                ┌─────────────────┐
                                │  ExamService    │
                                │  (search/filter)│
                                └────────┬────────┘
                                         │
                                         ▼
                                ┌─────────────────┐
                                │ ExamRepository  │
                                │ (JSON read)     │
                                └────────┬────────┘
                                         │
                                         ▼
                                ┌─────────────────┐
                                │  exams.json     │
                                └─────────────────┘
```

## API Design

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exams` | Search and list exams with pagination |
| GET | `/api/filters/dates` | Get available exam dates (cached) |
| GET | `/api/filters/locations` | Get available exam locations grouped by building (cached) |
| GET | `/api/health` | Health check endpoint |

### Search Fields
The `q` parameter searches across:
- `course_number` (e.g., "009B")
- `course_name` (e.g., "Calculus")
- `crn` (e.g., "35359")

### Query Parameters for `/api/exams`

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | Search query (partial, case-insensitive) |
| `date` | string | Filter by date (ISO format: YYYY-MM-DD) |
| `location` | string | Filter by location |
| `page` | int | Page number (default: 1) |
| `limit` | int | Items per page (default: 20, max: 100) |

### Response Format

#### Exams Response
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "hasMore": true
  }
}
```

#### Locations Response (Grouped by Building)
```json
{
  "data": [
    { "building": "SSC", "rooms": ["SSC 235", "SSC 308", "SSC 329", "SSC 335"] },
    { "building": "BRNHL", "rooms": ["BRNHL A125"] },
    { "building": "HMNSS", "rooms": ["HMNSS 1501"] }
  ]
}
```

## Frontend Component Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchBar.tsx
│   │   ├── FilterTabs.tsx
│   │   ├── ExamTable.tsx
│   │   ├── ExamRow.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── EmptyState.tsx
│   │   └── ErrorDisplay.tsx
│   ├── hooks/
│   │   └── useExams.ts          # TanStack Query hook
│   ├── lib/
│   │   └── api.ts               # API client
│   ├── types/
│   │   └── exam.ts              # TypeScript interfaces
│   └── app/
│       └── page.tsx             # Main page
```

## Table Column Formatting

| Column | Display Format | Source Fields |
|--------|---------------|---------------|
| Final Exam | "EXAM: MATH 006A 040 35359" | subject, course_number, section, crn |
| Exam Date | "Dec 8" | start_time (formatted) |
| Start Time | "8am" | start_time (formatted) |
| End Time | "10am" | end_time (formatted) |
| Classroom | "SSC 335" | location |

## Security Considerations

1. **Input Validation**: Validate and sanitize all query parameters
2. **SQL Injection**: N/A (using JSON file, not database)
3. **XSS**: React handles output encoding; ensure API doesn't return executable content
4. **Rate Limiting**: Consider adding for production (optional for local use)
5. **CORS**: Configure to allow frontend origin only
6. **Error Messages**: Don't leak internal details in error responses

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Large JSON file could slow API | Implement caching at repository layer |
| Search performance degrades | Use indexed data structure if needed |
| Frontend bundle size | Use dynamic imports for heavy components |
| Scroll performance with many rows | Implement virtual scrolling if needed |

## Resolved Decisions

1. **CRN Search**: Yes, search matches against CRN in addition to course number and name
2. **Timezone**: PST (Pacific Standard Time) - university is in California
3. **Filter Caching**: Cache filter options at the repository/service layer
4. **UI Library**: Tailwind CSS (per project conventions)
