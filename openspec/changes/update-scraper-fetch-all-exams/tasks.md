# Tasks: Update Scraper to Fetch All Exams

## 1. Configuration Updates
- [ ] 1.1 Update `backend/scraper/config.py` to remove `DEFAULT_SUBJECT_FILTER`
- [ ] 1.2 Add documentation comment explaining the filter is now optional

## 2. Core Scraper Updates
- [ ] 2.1 Remove the `subject_filter` from `fetch_exams` in `backend/scraper/exam_scraper.py`
- [ ] 2.2 Modify URL construction to remove `filter1` query param as no filter is needed
- [ ] 2.3 Update logging to reflect whether filtering is applied
- [ ] 2.4 Remove the `subject_filter` from `__main__.py` in `backend/scraper/exam_scraper.py`


## 3. CLI Updates
- [ ] 3.1 Update `backend/scraper/__main__.py` to default to fetching all exams
- [ ] 3.2 Update CLI help text and docstring to reflect new behavior
- [ ] 3.3 Remove the subject argument from CLI

## 4. Testing & Validation
- [ ] 4.1 Run scraper without arguments and verify all department exams are fetched
- [ ] 4.2 Validate JSON output structure remains consistent
- [ ] 4.3 Verify existing API and frontend continue to work with expanded dataset
