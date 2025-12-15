# Change: Update Scraper to Fetch All Exams

## Why

The current exam scraper only fetches Math department exams as a proof of concept. To provide a complete final exam schedule for all UCR students, the scraper needs to fetch exams from all departments. The 25Live calendar API already supports returning all exams when no subject filter is applied.

## What Changes

- Update the scraper's default behavior to fetch all exams instead of only MATH
- Remove the default subject filter, allowing the API call to return all departments
- Update configuration to remove the subject filter for scraping

## Impact

- Affected specs: `exam-scraper` (modified capability)
- Affected code: `backend/scraper/config.py`, `backend/scraper/exam_scraper.py`, `backend/scraper/__main__.py`
- Data volume: Expected increase from ~50 MATH exams to several thousand exams across all departments
