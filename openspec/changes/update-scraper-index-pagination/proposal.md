# Change: Update Scraper to Paginate 25Live XHR by Index

## Why

The current scraper fetches only a single XHR page per day. The 25Live widget paginates results via an `index` query parameter (e.g., `index=0`, then `index=25`, ...). Without iterating these pages, the dataset may miss many exams.

This change also captures the exact table fields the widget displays (Final Exam, Exam Date, Start Time, Classroom) and derives an End Time as 3 hours after Start Time, formatted in a 12-hour clock for America/Los_Angeles (PST for the requested dates).

## What Changes

- Update scraping to iterate **both**:
  - dates from `20251206` through `20251212` (inclusive), AND
  - index pages from `0` through `300` (inclusive)
- Use the requested endpoint shape:
  - `https://25livepub.collegenet.com/s.aspx?calendar=final-exam-calendar&widget=main&date={date}&index={index}&spudformat=xhr`
- Parse the day-view HTML table to extract the displayed columns:
  - Final Exam
  - Exam Date
  - Start Time
  - Classroom
- Derive End Time as `Start Time + 3 hours` in America/Los_Angeles time and format as 12-hour clock (e.g., `8:00 AM`)
- Preserve existing canonical fields used by the API/frontend (e.g., `start_time` / `end_time` ISO strings and `location`) by **adding** the new display-oriented fields rather than replacing existing ones.

## Impact

- Affected specs: `exam-scraper` (modified capability)
- Affected code (implementation stage): `backend/scraper/config.py`, `backend/scraper/exam_scraper.py`
- Data shape: additional fields will be added to each exam record (non-breaking for consumers that ignore unknown keys)
- Scrape load: up to 13 index pages per day × 7 days = 91 requests, so the implementation should include a small delay and/or stop early when no next page is available

## Open Questions

1. End time semantics: should the scraper **always** set End Time to `Start Time + 3 hours`, or only do this when the upstream payload does not provide an end time?
Yes
2. Output schema preference: do you want the JSON output to be **only** the 5 table fields (Final Exam, Exam Date, Start Time, End Time, Classroom), or should we keep the existing fields for the API/frontend and add these as additional fields?
Yes only these fields
