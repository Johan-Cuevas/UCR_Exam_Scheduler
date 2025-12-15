"""UCR Final Exam Scraper - Core logic for fetching and parsing exam data."""

import json
import logging
import re
from pathlib import Path
from typing import Optional

import requests

from .config import API_BASE_URL, OUTPUT_FILE

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def fetch_exams() -> list[dict]:
    """
    Fetch all exam data from UCR's 25Live calendar API.

    Returns:
        List of raw exam dictionaries from the API

    Raises:
        SystemExit: If the API request fails
    """
    logger.info(f"Fetching all exams from: {API_BASE_URL}")

    try:
        response = requests.get(API_BASE_URL, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch exams: {e}")
        raise SystemExit(1)

    data = response.json()

    # The API returns a list of events directly
    if isinstance(data, list):
        exams = data
    else:
        # Handle potential wrapper object
        exams = data.get("events", data.get("items", []))

    logger.info(f"Fetched {len(exams)} exams")
    return exams


def _extract_custom_fields(raw_custom_fields: list) -> dict:
    """
    Convert the customFields array into a dictionary for easier access.

    Args:
        raw_custom_fields: List of {fieldID, label, value, type} objects

    Returns:
        Dictionary mapping label to value
    """
    if not raw_custom_fields or not isinstance(raw_custom_fields, list):
        return {}

    return {field.get("label", ""): field.get("value", "") for field in raw_custom_fields}


def parse_exam(raw_exam: dict) -> Optional[dict]:
    """
    Parse a raw exam from the API into a structured format.

    Args:
        raw_exam: Raw exam dictionary from the API

    Returns:
        Parsed exam dictionary, or None if parsing fails
    """
    title = raw_exam.get("title", "")

    # Parse title format: "EXAM: MATH 009B 020 33515"
    # Pattern: EXAM: <SUBJECT> <COURSE_NUM> <SECTION> <CRN>
    match = re.match(r"EXAM:\s*(\w+)\s+(\w+)\s+(\w+)\s+(\d+)", title)

    # Convert customFields array to dict
    custom_fields = _extract_custom_fields(raw_exam.get("customFields", []))

    if match:
        subject, course_number, section, crn = match.groups()
    else:
        # Try to extract from customFields if title parsing fails
        subject = custom_fields.get("SIS Subject Code", "")
        course_number = ""
        section = ""
        crn = ""

        # Log warning for unparseable titles
        if title:
            logger.warning(f"Could not parse title: {title}")

    return {
        "subject": subject,
        "course_number": course_number,
        "section": section,
        "crn": crn,
        "course_name": custom_fields.get("Event Title", "").replace("EXAM: ", ""),
        "start_time": raw_exam.get("startDateTime", ""),
        "end_time": raw_exam.get("endDateTime", ""),
        "location": raw_exam.get("location", ""),
        "term_code": custom_fields.get("SIS Term Code", ""),
    }


def save_exams(exams: list[dict], output_path: str = OUTPUT_FILE) -> None:
    """
    Save parsed exams to a JSON file.

    Args:
        exams: List of parsed exam dictionaries
        output_path: Path to output file (relative to backend directory)
    """
    # Resolve path relative to this file's parent's parent (backend/)
    backend_dir = Path(__file__).parent.parent
    full_path = backend_dir / output_path

    # Ensure directory exists
    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(exams, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved {len(exams)} exams to {full_path}")


def run_scraper() -> list[dict]:
    """
    Main entry point: fetch, parse, and save all exams.

    Returns:
        List of parsed exam dictionaries
    """
    raw_exams = fetch_exams()
    parsed_exams = [parse_exam(exam) for exam in raw_exams]

    # Filter out any None results from failed parsing
    parsed_exams = [e for e in parsed_exams if e is not None]

    save_exams(parsed_exams)
    return parsed_exams
