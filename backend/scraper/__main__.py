"""CLI entry point for the UCR exam scraper.

Usage:
    python -m scraper

Fetches final exams for the configured date range and saves them to data/exams.json.
"""

from .config import END_DATE, START_DATE
from .exam_scraper import run_scraper


def main() -> None:
    """Main CLI entry point."""
    print("UCR Final Exam Scraper")
    print("======================")
    print(f"Fetching all department exams for {START_DATE}–{END_DATE}...")
    print()

    exams = run_scraper()

    print()
    print(f"Successfully scraped {len(exams)} exams from all departments!")


if __name__ == "__main__":
    main()
