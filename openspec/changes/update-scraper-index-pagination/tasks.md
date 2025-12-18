# Tasks: Update Scraper to Paginate 25Live XHR by Index

## 1. Config Updates
- [x] 1.1 Update `API_BASE_URL` to include `index={index}` and match the requested URL shape
- [x] 1.2 Add index pagination bounds/constants (e.g., `INDEX_START=0`, `INDEX_END=300`, `INDEX_STEP=25`)
- [x] 1.3 Confirm the date bounds remain `START_DATE=20251206`, `END_DATE=20251212` (inclusive)

## 2. Fetch Logic (Dates × Index Pages)
- [x] 2.1 Update fetch loop to request every date in range
- [x] 2.2 For each date, request pages for `index` from 0..300 (inclusive), stepping by 25
- [x] 2.3 Add a “stop early” condition when the response indicates there is no next page and/or no event rows
- [x] 2.4 Add lightweight rate limiting (small sleep) to avoid overloading the upstream site
- [x] 2.5 Ensure failures (HTTP error, timeout) log context (`date`, `index`, status) and exit gracefully

## 3. Parsing & Field Extraction
- [x] 3.1 Parse table rows (`twSimpleTableEventRow*`) and extract:
  - [x] Final Exam (raw title text, e.g., `EXAM: CS 010A 003 30920`)
  - [x] Exam Date (table date label, plus a normalized ISO date)
  - [x] Start Time (table time label, plus normalized ISO datetime)
  - [x] Classroom (table location)
- [x] 3.2 Derive End Time as Start Time + 3 hours (America/Los_Angeles) and store:
  - [x] normalized ISO datetime (for API filtering)
  - [x] a 12-hour display string (e.g., `11:00 AM`)
- [x] 3.3 Preserve existing exam fields relied on by API/frontend; add new display fields without breaking existing keys

## 4. Deduplication & Output
- [x] 4.1 Deduplicate across (date, index) pages (prefer stable upstream `event_id`)
- [x] 4.2 Save to `backend/data/exams.json` with readable formatting

## 5. Testing & Validation
- [x] 5.1 Add/extend unit tests for pagination stop conditions and time derivation (+3h)
- [x] 5.2 Verify backend API date filtering still works (depends on ISO `start_time`)
- [x] 5.3 Run `pytest` for backend tests
- [ ] 5.4 (Optional) Run scraper once locally and confirm record counts increase vs single-page fetch
