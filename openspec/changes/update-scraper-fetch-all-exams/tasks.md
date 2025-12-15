# Tasks: Update Scraper to Fetch All Exams

## 1. Configuration Updates
- [ ] 1.1 Update `backend/scraper/config.py` to change `DEFAULT_SUBJECT_FILTER` from "MATH" to `None`
- [ ] 1.2 Add documentation comment explaining the filter is now optional

## 2. Core Scraper Updates
- [ ] 2.1 Update `fetch_exams()` in `backend/scraper/exam_scraper.py` to handle optional filter parameter
- [ ] 2.2 Modify URL construction to omit `filter1` query param when no filter is provided
- [ ] 2.3 Update logging to reflect whether filtering is applied

## 3. CLI Updates
- [ ] 3.1 Update `backend/scraper/__main__.py` to default to fetching all exams
- [ ] 3.2 Update CLI help text and docstring to reflect new behavior
- [ ] 3.3 Ensure passing a subject argument still applies the filter

## 4. Testing & Validation
- [ ] 4.1 Run scraper without arguments and verify all department exams are fetched
- [ ] 4.2 Run scraper with "MATH" argument and verify only Math exams are fetched
- [ ] 4.3 Validate JSON output structure remains consistent
- [ ] 4.4 Verify existing API and frontend continue to work with expanded dataset
