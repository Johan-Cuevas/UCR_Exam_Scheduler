# Tasks: Update Scraper to Fetch All Exams

## 1. Configuration Updates
- [ ] 1.1 Update `API_BASE_URL` in `backend/scraper/config.py` to use new XHR endpoint template
- [ ] 1.2 Add date range constants (`START_DATE`, `END_DATE`) for `20251206` through `20251212`
	- [ ] Confirm `START_DATE`/`END_DATE` are inclusive bounds
	- [ ] Document expected date format as `YYYYMMDD`

## 2. Core Scraper Updates
- [ ] 2.1 Update `fetch_exams()` in `backend/scraper/exam_scraper.py` to iterate over date range
- [ ] 2.2 Update URL construction to use `https://25livepub.collegenet.com/s.aspx?hosted=1&calendar=final-exam-calendar&widget=main&date={date}&spudformat=xhr`
- [ ] 2.3 Populate the `date` query parameter with each date in YYYYMMDD format
- [ ] 2.4 Update response parsing to handle XHR endpoint format
	- [ ] Treat the response as non-guaranteed JSON (e.g., HTML/XHR payload) and parse accordingly
	- [ ] If parsing fails for a given date, log context (date, status code) and exit gracefully
- [ ] 2.5 Parse and include date field in exam data
	- [ ] Add a `date` field to each parsed exam using `YYYYMMDD`
	- [ ] Define whether `date` is the query date (preferred for traceability) or derived from `start_time`
- [ ] 2.6 Update logging to indicate date range being fetched
- [ ] 2.7 Deduplicate exams if same exam appears on multiple date queries
	- [ ] Define and implement a stable dedupe key (prefer upstream event ID if available; otherwise use a composite key)

## 3. Filtering Behavior
- [ ] 3.1 Ensure no subject/department filtering is applied (fetch all departments)
	- [ ] Remove any existing subject filters in scraper logic/config (if present)

## 4. CLI Updates
- [ ] 4.1 Update CLI docstring and output to reflect date range fetching (e.g., `20251206`–`20251212`)

## 5. Testing & Validation
- [ ] 5.1 Run scraper and verify exams are fetched for all dates in range
- [ ] 5.2 Validate JSON output structure includes `date` field in `YYYYMMDD`
- [ ] 5.3 Verify scraper exits gracefully on non-200/timeout/parse failure (no crash)
- [ ] 5.4 Verify existing API and frontend continue to work with updated dataset
