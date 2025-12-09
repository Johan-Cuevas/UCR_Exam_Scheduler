# Change: Add Math Exam Scraper

## Why

UCR students need an easy way to find their final exam schedules. The current UCR registrar website uses a complex JavaScript calendar widget that is difficult to navigate. We need to scrape this data and provide it in a structured format for use in our scheduler application.

## What Changes

- Add a Python scraper that fetches Math department final exam data from UCR's 25Live calendar API
- Store exam data in structured JSON format at `backend/data/exams.json`
- Support filtering by subject code (starting with MATH as proof of concept)
- Parse exam details including course number, section, CRN, date/time, and location

## Impact

- Affected specs: `exam-scraper` (new capability)
- Affected code: `backend/scraper/` (new directory)
- Dependencies: Python `requests` library
