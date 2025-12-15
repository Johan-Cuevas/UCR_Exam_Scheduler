# Change: Update Scraper to Fetch All Exams

## Why

The current exam scraper uses a JSON API endpoint that does not support date-based queries. To provide a complete final exam schedule for a specific date range, the scraper needs to use a different 25Live endpoint that supports date parameters. This allows fetching exams for a specific week (December 6-12, 2025) and ensures we get all exams from all departments for that period.

## What Changes

- Update API endpoint from JSON API to the XHR widget endpoint
- New base URL: `https://25livepub.collegenet.com/s.aspx?hosted=1&calendar=final-exam-calendar&widget=main&date={date}&spudformat=xhr`
- Add date iteration to fetch exams for each day from `20251206` through `20251212`
- The `date` query parameter must be populated with each date in YYYYMMDD format
- Remove subject filtering entirely (fetch all departments)
- Parse date field from exam data

## Impact

- Affected specs: `exam-scraper` (modified capability)
- Affected code: `backend/scraper/config.py`, `backend/scraper/exam_scraper.py`, `backend/scraper/__main__.py`
- API change: Different endpoint format and response structure may require parsing updates
- Data volume: Expected to fetch all exams across all departments for the specified date range
