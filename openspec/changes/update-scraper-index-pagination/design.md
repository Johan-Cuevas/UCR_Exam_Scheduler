# Design: Index-Paginated 25Live XHR Scrape + Time Derivation

## Goals

- Fetch a complete set of final exams for dates `20251206`–`20251212`.
- Follow the 25Live widget pagination mechanism (`index` offsets).
- Extract the same table fields users see in the widget and derive a 3-hour End Time.
- Preserve compatibility with the existing backend API and frontend by keeping canonical ISO datetime fields.

## Non-Goals

- Changing frontend UX or API response shapes beyond adding optional fields.
- Introducing a new scraping framework (Scrapy/Selenium). The current HTML parsing approach is sufficient.

## Observations (Current Upstream Behavior)

- The XHR endpoint returns an HTML document containing a table with headers:
  - `Final Exam:`
  - `Exam Date:`
  - `Start Time:`
  - `Classroom:`
- Paging uses `index` offsets. The “Next Page” link in the HTML uses increments of 25 (e.g., `index=25`, `index=50`).
- At higher indexes (e.g., 300 for `20251206`), the page may still contain events but appears to omit a “next” link.

## Proposed Approach

### Fetch Strategy

- For each date in the inclusive range:
  - Request pages for `index` in `[0, 25, 50, ..., 300]`.
  - Stop early if:
    - no event rows are present, OR
    - the page does not expose a “next page” hint.
  - Cap at `index=300` to match the requested bounds.

This balances completeness with safety: it follows the requested maximum while avoiding unnecessary calls once the upstream indicates the last page.

### Parsing Strategy

- Continue parsing the HTML day table rows (`twSimpleTableEventRow*`) to extract:
  - Final Exam: the anchor text beginning with `EXAM:`
  - Exam Date: the `twStartDate` text (e.g., `Dec 6`) and a normalized ISO date (`YYYY-MM-DD`) based on the query date.
  - Start Time: the `twStartTime` label (e.g., `8am`) and a normalized ISO datetime (`YYYY-MM-DDTHH:MM:SS`) based on the query date.
  - Classroom: the `twLocation` text.

### End Time Derivation

- Interpret Start Time in `America/Los_Angeles` (PST for December 2025).
- Derive End Time as `Start Time + 3 hours`.
- Produce two representations:
  - canonical ISO datetime for backend filtering
  - a 12-hour display string (e.g., `11:00 AM`)

## Compatibility

- Keep existing fields (`start_time`, `end_time`, `location`, etc.) intact and add display-oriented fields.
- If the user prefers a simplified output schema containing only the 5 widget fields, treat that as a **breaking** change and plan corresponding API/frontend updates.
