# Tasks: Update Scraper to Fetch All Exams

## 1. Configuration Updates
- [ ] 1.1 Remove `DEFAULT_SUBJECT_FILTER` from `backend/scraper/config.py`

## 2. Core Scraper Updates
- [ ] 2.1 Remove the `subject_filter` parameter from `fetch_exams()` in `backend/scraper/exam_scraper.py`
- [ ] 2.2 Update URL construction to use base URL without `filter1` query param
- [ ] 2.3 Update logging to indicate all exams are being fetched
- [ ] 2.4 Update `run_scraper()` to remove `subject_filter` parameter

## 3. CLI Updates
- [ ] 3.1 Remove subject argument from CLI in `backend/scraper/__main__.py`
- [ ] 3.2 Update CLI docstring and output to reflect fetching all exams

## 4. Testing & Validation
- [ ] 4.1 Run scraper and verify all department exams are fetched
- [ ] 4.2 Validate JSON output structure remains consistent
- [ ] 4.3 Verify existing API and frontend continue to work with expanded dataset
