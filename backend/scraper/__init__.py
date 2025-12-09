"""UCR Final Exam Scraper package."""

from .exam_scraper import fetch_exams, parse_exam, save_exams

__all__ = ["fetch_exams", "parse_exam", "save_exams"]
