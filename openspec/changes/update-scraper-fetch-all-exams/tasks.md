# Tasks: Update Scraper to Fetch All Exams

## 1. Configuration Updates
- [x] 1.1 Update `API_BASE_URL` in `backend/scraper/config.py` to use new XHR endpoint template
- [x] 1.2 Add date range constants (`START_DATE`, `END_DATE`) for `20251206` through `20251212`
	- [x] Confirm `START_DATE`/`END_DATE` are inclusive bounds
	- [x] Document expected date format as `YYYYMMDD`

## 2. Core Scraper Updates
- [x] 2.1 Update `fetch_exams()` in `backend/scraper/exam_scraper.py` to iterate over date range
- [x] 2.2 Update URL construction to use `https://25livepub.collegenet.com/s.aspx?hosted=1&calendar=final-exam-calendar&widget=main&date={date}&spudformat=xhr`

- [x] 2.3 Populate the `date` query parameter with each date in YYYYMMDD format
- [x] 2.4 Update response parsing to handle XHR endpoint format
	- [x] Treat the response as non-guaranteed JSON (e.g., HTML/XHR payload) and parse accordingly
	- [x] If parsing fails for a given date, log context (date, status code) and exit gracefully
- [x] 2.5 Parse and include date field in exam data
	- [x] Add a `date` field to each parsed exam using `YYYYMMDD`
	- [x] Define whether `date` is the query date (preferred for traceability) or derived from `start_time`
- [x] 2.6 Update logging to indicate date range being fetched
- [x] 2.7 Deduplicate exams if same exam appears on multiple date queries
	- [x] Define and implement a stable dedupe key (prefer upstream event ID if available; otherwise use a composite key)

## 3. Filtering Behavior
- [x] 3.1 Ensure no subject/department filtering is applied (fetch all departments)
	- [x] Remove any existing subject filters in scraper logic/config (if present)

## 4. CLI Updates
- [x] 4.1 Update CLI docstring and output to reflect date range fetching (e.g., `20251206`–`20251212`)

## 5. Testing & Validation
- [x] 5.1 Run scraper and verify exams are fetched for all dates in range
- [x] 5.2 Validate JSON output structure includes `date` field in `YYYYMMDD`
- [x] 5.3 Verify scraper exits gracefully on non-200/timeout/parse failure (no crash)
- [x] 5.4 Verify existing API and frontend continue to work with updated dataset
