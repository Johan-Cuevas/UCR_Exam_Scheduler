"""CLI entry point for the UCR exam scraper.

Usage:
    python -m scraper [subject_filter]

Examples:
    python -m scraper          # Fetch MATH exams (default)
    python -m scraper PHYS     # Fetch PHYS exams
"""

import sys

from .config import DEFAULT_SUBJECT_FILTER
from .exam_scraper import run_scraper


def main() -> None:
    """Main CLI entry point."""
    # Get subject filter from command line args, or use default
    subject_filter = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SUBJECT_FILTER

    print(f"UCR Final Exam Scraper")
    print(f"======================")
    print(f"Subject filter: {subject_filter}")
    print()

    exams = run_scraper(subject_filter)

    print()
    print(f"Successfully scraped {len(exams)} exams!")


if __name__ == "__main__":
    main()
