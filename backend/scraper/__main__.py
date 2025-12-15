"""CLI entry point for the UCR exam scraper.

Usage:
    python -m scraper

Fetches all final exams from UCR's 25Live calendar and saves them to data/exams.json.
"""

from .exam_scraper import run_scraper


def main() -> None:
    """Main CLI entry point."""
    print("UCR Final Exam Scraper")
    print("======================")
    print("Fetching all department exams...")
    print()

    exams = run_scraper()

    print()
    print(f"Successfully scraped {len(exams)} exams from all departments!")


if __name__ == "__main__":
    main()
