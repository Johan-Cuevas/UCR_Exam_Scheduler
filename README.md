# Final Exam Scheduler (UCR)

A modern, searchable interface for viewing University of California, Riverside (UCR) final exam schedules.

## Project Purpose

- Replace UCR's static/table-based registrar final exam schedule page with an accessible, mobile-friendly web application.
- Allow students to quickly find final exam information by subject, course number, course name, and section.
- Provide a stable backend API so the Next.js frontend (and any future tools) can consume the same exam schedule data.
- Store scraped schedule data as JSON snapshots so the UI and API are fast, reliable, and do not depend on live scraping.

## Tech Stack

### Backend

- **Language:** Python 3.11.6
- **Framework:** Flask (RESTful JSON API)
- **Scraping:**
  - BeautifulSoup (primary for static HTML parsing)
  - Scrapy (fallback for more complex scraping/crawling)
  - Selenium (fallback for JavaScript-rendered pages when needed)
- **Data Storage:** JSON files for exam schedule snapshots (with room to upgrade to a database later).
- **Testing:** `pytest` with Flask test client and HTTP-style tests.

### Frontend

- **Framework:** React with Next.js
- **Language:** TypeScript
- **Styling:** Tailwind CSS (utility-first, responsive design)
- **Testing:** Jest and React Testing Library for components/pages; optional Playwright/Cypress for end-to-end tests.

### Tooling & Workflow

- **Specs:** Spec-driven development using OpenSpec (`openspec/` directory).
- **Workflow:** Each approved change is implemented on a dedicated Git branch named after its OpenSpec `change-id`.

## Why This Project Exists

Students currently have to scan a long, static table on the registrar site to find their exam details. This project aims to:

- Make it significantly faster and easier to look up exam schedules.
- Improve accessibility and usability on both mobile and desktop devices.
- Establish a clean separation between data scraping, backend API, and frontend UI so the system is easier to maintain and extend.

## Status

This repository is under active development and uses OpenSpec specs to describe and evolve its behavior over time.
