# Change: Update Scraper to Fetch All Exams

## Why

The current exam scraper only fetches Math department exams as a proof of concept. To provide a complete final exam schedule for all UCR students, the scraper needs to fetch exams from all departments. The 25Live calendar API already supports returning all exams when no subject filter is applied.

## What Changes

- Remove subject filtering entirely from the scraper
- The scraper will always fetch all exams from all departments
- Remove the `DEFAULT_SUBJECT_FILTER` configuration and CLI subject argument

## Impact

- Affected specs: `exam-scraper` (modified capability)
- Affected code: `backend/scraper/config.py`, `backend/scraper/exam_scraper.py`, `backend/scraper/__main__.py`
- Data volume: Expected increase from ~50 MATH exams to several thousand exams across all departments
