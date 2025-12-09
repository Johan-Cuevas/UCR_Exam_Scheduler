# Design: Math Exam Scraper

## Context

UCR's final exam schedule is displayed on https://registrar.ucr.edu/calendar/final-exam-live using a Trumba/CollegeNET calendar widget. Initial investigation revealed the page uses JavaScript to dynamically load content, which would typically require Selenium for scraping.

However, we discovered a direct JSON API endpoint that returns all exam data without requiring JavaScript execution.

## Goals / Non-Goals

**Goals:**
- Fetch Math department final exam data reliably
- Parse and transform data into a structured JSON format
- Store data locally for consumption by the frontend
- Keep implementation simple using only the `requests` library

**Non-Goals:**
- Scraping all departments (only Math as POC)
- Real-time sync or scheduling
- Building a full web scraping framework
- Handling authentication (API is public)

## Decisions

### Decision 1: Use Direct JSON API Instead of HTML Scraping

**What:** Use `https://25livepub.collegenet.com/calendars/final-exam-calendar.json` endpoint

**Why:**
- Returns structured JSON data directly
- No need for Selenium/browser automation
- Faster and more reliable than HTML parsing
- Supports server-side filtering with `?filter1=MATH` parameter

**Alternatives considered:**
- Selenium: Would work but overkill - slower, requires browser driver, more complex setup
- Scrapy: Designed for HTML scraping, unnecessary given JSON API exists
- BeautifulSoup: Can't execute JavaScript, wouldn't work with Trumba widget

### Decision 2: Data Transformation Strategy

**What:** Parse the API response and extract key fields into a flat JSON structure

**API Response Structure (per exam):**
```json
{
  "title": "EXAM: MATH 009B 020 33515",
  "startDateTime": "2025-03-17T08:00:00",
  "endDateTime": "2025-03-17T10:00:00",
  "location": "INTS 1113",
  "customFields": {
    "Subject Code": "MATH",
    "Course Name": "First-Year Calculus",
    "Term Code": "202520"
  }
}
```

**Transformed Output Structure:**
```json
{
  "subject": "MATH",
  "course_number": "009B",
  "section": "020",
  "crn": "33515",
  "course_name": "First-Year Calculus",
  "start_time": "2025-03-17T08:00:00",
  "end_time": "2025-03-17T10:00:00",
  "location": "INTS 1113",
  "term_code": "202520"
}
```

### Decision 3: File Structure

```
backend/
├── scraper/
│   ├── __init__.py
│   ├── exam_scraper.py    # Main scraper logic
│   └── config.py          # API URLs, filter configs
├── data/
│   └── exams.json         # Output file
└── requirements.txt       # Add 'requests' dependency
```

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| API endpoint could change | Document the discovery process; add error handling |
| Rate limiting | Add delays between requests if needed; cache results |
| API returns unexpected format | Validate response structure before parsing |
| Missing data for some exams | Handle None/missing fields gracefully |

### Decision 4: No Caching

**What:** No caching layer - fetch fresh data on each run

**Why:** This is a proof of concept; caching adds unnecessary complexity

### Decision 5: CLI Interface

**What:** Add a simple CLI entry point to run the scraper manually

**Why:** Makes it easy to test and run the scraper during development
