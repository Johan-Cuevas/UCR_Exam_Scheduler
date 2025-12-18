"""UCR Final Exam Scraper - Core logic for fetching and parsing exam data."""

import datetime as dt
import html
import json
import logging
import re
import time
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import requests

from .config import (
    API_BASE_URL,
    END_DATE,
    INDEX_END,
    INDEX_START,
    INDEX_STEP,
    OUTPUT_FILE,
    REQUEST_DELAY_SECONDS,
    START_DATE,
)

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def _parse_yyyymmdd(value: str) -> dt.date:
    return dt.datetime.strptime(value, "%Y%m%d").date()


def _iter_dates(start: str, end: str) -> list[str]:
    start_date = _parse_yyyymmdd(start)
    end_date = _parse_yyyymmdd(end)

    if end_date < start_date:
        raise ValueError("END_DATE must be >= START_DATE")

    current = start_date
    days: list[str] = []
    while current <= end_date:
        days.append(current.strftime("%Y%m%d"))
        current += dt.timedelta(days=1)

    return days


LA_TZ = ZoneInfo("America/Los_Angeles")


def _parse_time_label(label: str) -> Optional[tuple[int, int]]:
    """Parse widget time labels like '8am' into (hour, minute)."""

    token = label.strip().lower()
    match = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$", token)
    if not match:
        return None

    hour = int(match.group(1))
    minute = int(match.group(2) or "0")
    ampm = match.group(3)

    if hour == 12:
        hour = 0
    if ampm == "pm":
        hour += 12

    return hour, minute


def _format_time_12h(value: dt.datetime) -> str:
    hour24 = value.hour
    hour12 = hour24 % 12
    if hour12 == 0:
        hour12 = 12
    ampm = "AM" if hour24 < 12 else "PM"
    return f"{hour12}:{value.minute:02d} {ampm}"


def _extract_event_rows(text: str) -> list[str]:
    return re.findall(
        r"<tr class=\"twSimpleTableEventRow[^\"]*\".*?</tr>",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )


def _has_next_page_hint(text: str, next_index: int) -> bool:
    # Heuristic: the day view HTML includes pagination links containing the next index.
    # If the upstream stops exposing a link to index={next_index}, we treat that as end.
    return bool(re.search(rf"\bindex={next_index}\b", text))


def _parse_day_html(text: str, query_date: str) -> list[dict]:
    """Parse the day view HTML table into raw exam dicts."""

    rows = _extract_event_rows(text)

    exams: list[dict] = []
    for row in rows:
        event_match = re.search(r"\beventid=\"(\d+)\"", row)
        title_match = re.search(r">\s*(EXAM:[^<]+)<", row)
        start_date_match = re.search(r"class=\"twStartDate\">([^<]+)<", row)
        start_time_match = re.search(r"class=\"twStartTime\">([^<]+)<", row)
        location_match = re.search(r"class=\"twLocation\">([^<]*)<", row)

        if not event_match or not title_match:
            continue

        event_id = event_match.group(1)
        title = html.unescape(title_match.group(1)).strip()
        exam_date_display = (start_date_match.group(1).strip() if start_date_match else "")
        exam_date_iso = dt.datetime.strptime(query_date, "%Y%m%d").date().isoformat()
        start_time_label = (start_time_match.group(1).strip() if start_time_match else "")
        location = (html.unescape(location_match.group(1)).strip() if location_match else "")

        start_dt: Optional[dt.datetime] = None
        end_dt: Optional[dt.datetime] = None
        start_iso = ""
        end_iso = ""
        start_display = ""
        end_display = ""

        parsed_time = _parse_time_label(start_time_label)
        if parsed_time:
            hour, minute = parsed_time
            start_dt = dt.datetime.strptime(query_date, "%Y%m%d").replace(
                hour=hour, minute=minute, second=0
            )
            end_dt = start_dt + dt.timedelta(hours=3)
            start_iso = start_dt.isoformat()
            end_iso = end_dt.isoformat()
            start_display = _format_time_12h(start_dt.replace(tzinfo=LA_TZ))
            end_display = _format_time_12h(end_dt.replace(tzinfo=LA_TZ))

        exams.append(
            {
                "title": title,
                "final_exam": title,
                "location": location,
                "classroom": location,
                "startDateTime": start_iso,
                "endDateTime": end_iso,
                "exam_date": exam_date_display,
                "exam_date_iso": exam_date_iso,
                "start_time": start_display,
                "end_time": end_display,
                "eventId": event_id,
                "_query_date": query_date,
            }
        )

    return exams


def _parse_xhr_response(text: str, query_date: str) -> list[dict]:
    """Parse XHR widget response.

    The endpoint often returns an HTML day view, so parse table rows.
    """

    return _parse_day_html(text, query_date=query_date)


def fetch_exams() -> list[dict]:
    """Fetch exam data for each date in the configured range.

    Returns:
        List of raw exam dictionaries from the upstream endpoint.

    Raises:
        SystemExit: If an API request fails or parsing fails for a given date.
    """

    dates = _iter_dates(START_DATE, END_DATE)
    logger.info(f"Fetching exams for date range {START_DATE}–{END_DATE} ({len(dates)} days)")

    all_exams: list[dict] = []
    with requests.Session() as session:
        for date in dates:
            logger.info(f"Fetching exams for {date} (index {INDEX_START}..{INDEX_END} step {INDEX_STEP})")

            for index in range(INDEX_START, INDEX_END + 1, INDEX_STEP):
                url = API_BASE_URL.format(date=date, index=index)
                logger.info(f"Fetching exams for {date} index={index}: {url}")

                try:
                    response = session.get(url, timeout=30)
                    response.raise_for_status()
                except requests.RequestException as e:
                    status = getattr(getattr(e, "response", None), "status_code", None)
                    logger.error(f"Failed to fetch exams (date={date} index={index} status={status}): {e}")
                    raise SystemExit(1)

                try:
                    raw_exams = _parse_xhr_response(response.text, query_date=date)
                except Exception as e:
                    logger.error(
                        f"Failed to parse exams (date={date} index={index} status={response.status_code}): {e}"
                    )
                    raise SystemExit(1)

                # Stop early if no event rows.
                if not raw_exams:
                    logger.info(f"No event rows found; stopping pagination for date={date} at index={index}")
                    break

                all_exams.extend(raw_exams)

                # Stop early if the payload doesn't hint a next page.
                next_index = index + INDEX_STEP
                if next_index <= INDEX_END and not _has_next_page_hint(response.text, next_index=next_index):
                    logger.info(
                        f"No next page hint; stopping pagination for date={date} at index={index}"
                    )
                    break

                if REQUEST_DELAY_SECONDS > 0:
                    time.sleep(REQUEST_DELAY_SECONDS)

    logger.info(f"Fetched {len(all_exams)} raw exams before dedupe")
    return all_exams


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


def _dedupe_key(parsed_exam: dict) -> str:
    for key in ("event_id", "eventId", "id"):
        value = parsed_exam.get(key)
        if value:
            return f"id:{value}"

    return "|".join(
        [
            str(parsed_exam.get("subject", "")),
            str(parsed_exam.get("course_number", "")),
            str(parsed_exam.get("section", "")),
            str(parsed_exam.get("crn", "")),
            str(parsed_exam.get("start_time", "")),
            str(parsed_exam.get("location", "")),
        ]
    )


def parse_exam(raw_exam: dict) -> Optional[dict]:
    """Parse a raw exam dictionary into a structured record."""

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

        if title:
            logger.warning(f"Could not parse title: {title}")

    query_date = raw_exam.get("_query_date", "")

    course_name = custom_fields.get("Event Title", "").replace("EXAM: ", "")
    if not course_name and title.startswith("EXAM:"):
        course_name = title.replace("EXAM:", "").strip()

    return {
        "subject": subject,
        "course_number": course_number,
        "section": section,
        "crn": crn,
        "course_name": course_name,
        "start_time": raw_exam.get("startDateTime", ""),
        "end_time": raw_exam.get("endDateTime", ""),
        "location": raw_exam.get("location", ""),
        "term_code": custom_fields.get("SIS Term Code", ""),
        "date": query_date,
        "event_id": raw_exam.get("eventId", raw_exam.get("event_id", raw_exam.get("id", ""))),
        # Display-oriented fields from the day table.
        "final_exam": raw_exam.get("final_exam", raw_exam.get("title", "")),
        "exam_date": raw_exam.get("exam_date", ""),
        "exam_date_iso": raw_exam.get("exam_date_iso", ""),
        "start_time_display": raw_exam.get("start_time", ""),
        "end_time_display": raw_exam.get("end_time", ""),
        "classroom": raw_exam.get("classroom", raw_exam.get("location", "")),
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
    """Main entry point: fetch, parse, dedupe, and save exams."""

    raw_exams = fetch_exams()
    parsed_exams = [parse_exam(exam) for exam in raw_exams]

    # Filter out any None results from failed parsing
    parsed_exams = [e for e in parsed_exams if e is not None]

    deduped: dict[str, dict] = {}
    for exam in parsed_exams:
        key = _dedupe_key(exam)
        # Keep first occurrence; upstream duplicates should be identical.
        deduped.setdefault(key, exam)

    final_exams = list(deduped.values())
    logger.info(f"Deduped to {len(final_exams)} exams")

    save_exams(final_exams)
    return final_exams
