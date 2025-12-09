# Tasks: Add Math Exam Scraper

## 1. Project Setup
- [x] 1.1 Create `backend/` directory structure
- [x] 1.2 Create `backend/requirements.txt` with `requests` dependency
- [x] 1.3 Create `backend/scraper/__init__.py`

## 2. Core Implementation
- [x] 2.1 Create `backend/scraper/config.py` with API URL and filter constants
- [x] 2.2 Create `backend/scraper/exam_scraper.py` with main scraper logic
- [x] 2.3 Implement `fetch_exams(subject_filter)` function to call the JSON API
- [x] 2.4 Implement `parse_exam(raw_exam)` function to transform API response
- [x] 2.5 Implement `save_exams(exams, output_path)` function to write JSON file

## 3. CLI & Data Output
- [x] 3.1 Create `backend/data/` directory
- [x] 3.2 Add CLI entry point (`__main__.py`) to run scraper from command line
- [x] 3.3 Save output to `backend/data/exams.json`

## 4. Testing & Validation
- [x] 4.1 Run scraper and verify output file is created
- [x] 4.2 Validate JSON structure matches expected format
- [x] 4.3 Verify all Math exams are captured (49 exams scraped)
