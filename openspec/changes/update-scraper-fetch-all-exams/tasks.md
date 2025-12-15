# Tasks: Update Scraper to Fetch All Exams

## 1. Configuration Updates
- [ ] 1.1 Update `API_BASE_URL` in `backend/scraper/config.py` to use new XHR endpoint template
- [ ] 1.2 Add date range constants (`START_DATE`, `END_DATE`) for `20251206` through `20251212`

## 2. Core Scraper Updates
- [ ] 2.1 Update `fetch_exams()` in `backend/scraper/exam_scraper.py` to iterate over date range
- [ ] 2.2 Update URL construction to use `https://25livepub.collegenet.com/s.aspx?hosted=1&calendar=final-exam-calendar&widget=main&date={date}&spudformat=xhr`
- [ ] 2.3 Populate the `date` query parameter with each date in YYYYMMDD format
- [ ] 2.4 Update response parsing to handle XHR endpoint format
- [ ] 2.5 Parse and include date field in exam data
- [ ] 2.6 Update logging to indicate date range being fetched
- [ ] 2.7 Deduplicate exams if same exam appears on multiple date queries

## 3. CLI Updates
- [ ] 3.1 Update CLI docstring and output to reflect date range fetching

## 4. Testing & Validation
- [ ] 4.1 Run scraper and verify exams are fetched for all dates in range
- [ ] 4.2 Validate JSON output structure includes date field
- [ ] 4.3 Verify existing API and frontend continue to work with updated dataset
