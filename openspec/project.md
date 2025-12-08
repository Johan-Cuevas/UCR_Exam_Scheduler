# Project Context

## Purpose
- Build a modern, searchable interface for viewing university final exam schedules, initially scoped explicitly to UCR's registrar page at `https://registrar.ucr.edu/calendar/final-exam-live`.
- Replace the current static/table view with an accessible, mobile-friendly experience that lets students quickly find their exam information.
- Expose a stable backend API so the Next.js frontend (and any future tools) can consume the same exam schedule data.

## Tech Stack

- **Backend**
  - Language: Python 3.11.6 (target runtime).
  - Web framework: Flask (RESTful JSON API).
  - Scraping:
    - Primary: BeautifulSoup (for static HTML).
    - Fallback 1: Scrapy (for more complex scraping pipelines or crawl management).
    - Fallback 2: Selenium (for JavaScript-rendered pages when other approaches fail).
  - Data storage: JSON files (source-of-truth dataset for exams; potential future upgrade to a DB if needed).
  - Testing: `pytest` + Flask test client + `requests`-style HTTP testing utilities.

- **Frontend**
  - Framework: React with Next.js.
  - Language: TypeScript.
  - Styling: Tailwind CSS (modern, utility-first styling approach).
  - Version policy: use the latest stable versions of React, TypeScript, and Next.js that are mutually compatible (e.g., whatever combination is recommended by the current Next.js release).
  - Testing: Jest + React Testing Library for unit/component tests; optional Playwright/Cypress for E2E.

- **Tooling / Spec Workflow**
  - Spec-driven development using OpenSpec (`openspec/` directory).
  - Each approved change/spec is implemented on its own GitHub branch named after the `change-id` (e.g., `add-exam-search-ui`).

## Project Conventions

### Code Style

- **Backend (Python)**
  - Follow PEP 8 conventions.
  - Use type hints where practical (`mypy`-friendly style).
  - Prefer clear module and class names (no single-letter names outside small scopes).
  - Consistent formatting with tools like Black and isort (if/when added to the project).
  - Use docstrings for public functions, classes, and API endpoints.

- **Frontend (TypeScript/React)**
  - Function components with React Hooks; avoid class components.
  - Strong typing with TypeScript interfaces/types for API responses and domain models (e.g., `Exam`, `Course`).
  - File naming: kebab-case for files, PascalCase for React components.
  - Use ESLint + Prettier defaults (if configured) for formatting and linting.

### Architecture Patterns

- **Backend**
  - Layered approach:
    - Scraping layer: modules/classes responsible for fetching and parsing registrar pages (BeautifulSoup/Scrapy/Selenium).
    - Data layer: read/write JSON exam data behind a repository-style interface (e.g., `ExamRepository`).
    - Service layer: domain logic (search, filtering, deduping, schedule updates).
    - API layer: Flask blueprints that expose RESTful endpoints for the frontend and other consumers.
  - Use object-oriented abstractions where they clarify behavior (e.g., `ExamScraper`, `ExamService`).
  - Keep scraping logic decoupled from Flask so it can be run via CLI/cron as well as on demand.

- **Frontend**
  - Next.js pages/routes for top-level views (e.g., `/`, `/search`).
  - Separation of concerns:
    - `components/` for presentational and reusable UI components.
    - `features/` or `modules/` for grouped functionality (e.g., `exam-search`).
    - `lib/` or `services/` for API clients and shared utilities.
  - Fetch data via the Flask API using a thin client wrapper; keep domain types shared within the frontend.
  - Emphasis on accessibility (semantic HTML, keyboard navigation, ARIA where appropriate).

### Testing Strategy

- **Backend Testing**
  - Use `pytest` as the primary test runner.
  - Unit tests for:
    - Scraping/parsing functions (given sample HTML, produce expected exam records).
    - Service-layer logic (search/filter behavior by subject, course name, course number).
    - Data layer read/write behavior to JSON.
  - Integration tests for:
    - Flask API endpoints (search endpoints, health endpoints) using the Flask test client.
    - End-to-end scrape + load + search flow where feasible (using recorded HTML fixtures, not live HTTP).

- **Frontend Testing**
  - Jest + React Testing Library for components and pages:
    - Rendering of key screens (search page, results list, empty state).
    - User flows: typing a subject/course, triggering search, seeing correct results.
  - Optional E2E (Playwright or Cypress) once the full stack is wired:
    - Full search journey from landing page to viewing exam details.
  - Align test cases with OpenSpec scenarios to ensure each requirement has corresponding automated coverage where reasonable.

### Git Workflow

- Main/default branch reflects deployed/production-ready state.
- For any new capability or behavioral change that is not a simple bug fix/typo:
  - Create a new OpenSpec change with a unique verb-led `change-id` (e.g., `add-exam-search-api`).
  - Create a corresponding Git branch named after the `change-id` (or prefixed with `feature/` if desired, e.g., `feature/add-exam-search-api`).
  - Author `proposal.md`, `tasks.md`, and spec deltas under `openspec/changes/<change-id>/`.
  - Do not begin implementation until the proposal is reviewed and approved.
- Bug fixes or small non-behavioral changes can be implemented directly (without a new change-id) as long as they restore/align with existing specs.
- Prefer small, focused PRs that implement a single approved change.

## Domain Context

- The primary domain is university final exam scheduling, **explicitly scoped to the University of California, Riverside (UCR)** for the initial phase.
- Data is sourced from the registrar's public final exam schedule page (`https://registrar.ucr.edu/calendar/final-exam-live`). Future institutions, if added, should go through new OpenSpec changes.
- Core domain concepts include:
  - **Term** (e.g., "Fall 2025").
  - **Subject** (e.g., "CS", "MATH").
  - **Course number** (e.g., `010A`, `014`).
  - **Course name/title** (e.g., "Intro to Computer Science").
  - **Section** (e.g., `001`, `002`).
  - **Exam details**: date, start time, end time, location/room, exam group, and any notes/exceptions.
- Primary user goals:
  - Quickly find all exam details by:
    - Subject.
    - Course number.
    - Course name.
  - Optionally filter by term, day, time, or location (future enhancements).
- Search behavior and semantics:
  - Case-insensitive search across subject, course number, and course name.
  - Support loose/partial matches such that a query like `"CS 10"` matches `"CS010A"` (e.g., by normalizing whitespace and zero-padding where appropriate).
- The UI should be usable on mobile and desktop and should make it obvious when/since the data was last updated.

## Important Constraints

- **Scraping / Data Source**
  - Respect the registrar site's `robots.txt` and terms of use.
  - Avoid overloading the source site: scraping jobs should be rate-limited and typically run via scheduled tasks (e.g., daily or a few times per day) rather than on every user request.
  - Prefer parsing static HTML with BeautifulSoup; only escalate to Scrapy/Selenium when necessary.

- **Data Freshness & Reliability**
  - Store scraped data as JSON snapshots so the frontend and API do not depend on live scraping.
  - Expose "last updated" metadata so users understand how current the schedule is.
  - Handle schedule changes gracefully (e.g., overwrite/merge JSON snapshots on re-scrape).

- **Performance & UX**
  - Search should feel instant for a typical term's dataset (a few thousand courses/exams).
  - API responses should be reasonably small and paginated/limited if needed.
  - Frontend should be responsive and accessible (WCAG AA goals where practical).

- **Security & Privacy**
  - Data is public exam schedule information; no student-specific or sensitive data is handled.
  - No authentication is required initially; the app is read-only and public.

- **Deployment / Environment**
  - Assume the primary runtime environment is local development (backend and frontend running on a developer machine).
  - No specific cloud provider or production deployment target is required yet; when deployment is defined, constraints can be added via a new OpenSpec change.

## External Dependencies

- **Source systems**
  - UCR registrar final exam schedule at `https://registrar.ucr.edu/calendar/final-exam-live`.

- **Backend libraries**
  - BeautifulSoup4.
  - Scrapy (fallback for complex scraping).
  - Selenium (fallback for JavaScript-rendered pages).
  - Flask and related ecosystem libraries.
  - `pytest` and associated plugins for testing.

- **Frontend libraries/tools**
  - React, Next.js, TypeScript (latest mutually compatible stable releases).
  - Jest, React Testing Library (and possibly Playwright/Cypress later).
  - Tailwind CSS for styling.

- **Consumers**
  - Primary consumer is the Next.js frontend in this repository.
  - No mobile apps or third-party external clients are planned initially; if this changes, update specs and project context to reflect API stability/versioning guarantees.
