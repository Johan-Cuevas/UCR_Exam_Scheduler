"""UCR Final Exam Scraper - Core logic for fetching and parsing exam data."""

import datetime as dt
import html
import json
import logging
import re
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import requests

from .config import API_BASE_URL, END_DATE, OUTPUT_FILE, START_DATE

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


def _parse_event_detail(event_id: str, query_date: str, session: requests.Session) -> dict:
    """Fetch detail page to recover structured timestamps (best effort)."""

    url = API_BASE_URL.format(date=query_date) + f"&eventid={event_id}&view=event"

    response = session.get(url, timeout=30)
    response.raise_for_status()

    result: dict = {"event_id": event_id}

    title_match = re.search(r"<meta property=\"og:title\" content=\"([^\"]+)\"", response.text)
    if title_match:
        result["title"] = html.unescape(title_match.group(1)).strip()

    start_match = re.search(
        r"<meta property=\"event:start_time\" content=\"([^\"]+)\"", response.text
    )
    if start_match:
        start_utc = dt.datetime.fromisoformat(start_match.group(1).replace("Z", "+00:00"))
        result["start_time"] = start_utc.astimezone(LA_TZ).replace(tzinfo=None).isoformat()

    # Try to infer end_time from meta description like "8 - 11 a.m."
    desc_match = re.search(
        r"<meta property=\"description\" content=\"([^\"]+)\"", response.text
    )
    if result.get("start_time") and desc_match:
        desc = desc_match.group(1)
        time_range = re.search(
            r"\b(\d{1,2})(?::(\d{2}))?\s*-\s*(\d{1,2})(?::(\d{2}))?\s*(a\.m\.|p\.m\.)\b",
            desc,
        )
        if time_range:
            end_hour = int(time_range.group(3))
            end_min = int(time_range.group(4) or "0")
            end_is_pm = time_range.group(5).startswith("p")

            if end_hour == 12:
                end_hour = 0
            if end_is_pm:
                end_hour += 12

            start_local = dt.datetime.fromisoformat(result["start_time"])
            end_local = start_local.replace(hour=end_hour, minute=end_min, second=0)
            if end_local < start_local:
                end_local += dt.timedelta(days=1)
            result["end_time"] = end_local.isoformat()

    return result



def _parse_day_html(text: str, query_date: str, session: requests.Session) -> list[dict]:
    """Parse the day view HTML table into raw exam dicts."""

    rows = re.findall(
        r"<tr class=\"twSimpleTableEventRow[^\"]*\".*?</tr>",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

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
        start_time_label = (start_time_match.group(1).strip() if start_time_match else "")
        location = (html.unescape(location_match.group(1)).strip() if location_match else "")

        start_iso = ""
        end_iso = ""

        parsed_time = _parse_time_label(start_time_label)
        if parsed_time:
            hour, minute = parsed_time
            start_dt = dt.datetime.strptime(query_date, "%Y%m%d").replace(hour=hour, minute=minute)
            start_iso = start_dt.isoformat()

        # Fetch detail page for enriched times and term/course metadata when possible.
        try:
            details = _parse_event_detail(event_id=event_id, query_date=query_date, session=session)
            start_iso = details.get("start_time", start_iso)
            end_iso = details.get("end_time", end_iso)
        except Exception as e:
            logger.debug(f"Failed to fetch details for event_id={event_id} date={query_date}: {e}")
            details = {"event_id": event_id}

        exams.append(
            {
                "title": details.get("title", title),
                "location": location,
                "startDateTime": start_iso,
                "endDateTime": end_iso,
                "eventId": event_id,
                "_query_date": query_date,
            }
        )

    return exams


def _parse_xhr_response(text: str, query_date: str, session: requests.Session) -> list[dict]:
    """Parse XHR widget response.

    The endpoint often returns an HTML day view, so parse table rows.
    """

    return _parse_day_html(text, query_date=query_date, session=session)


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
            url = API_BASE_URL.format(date=date)
            logger.info(f"Fetching exams for {date}: {url}")

            try:
                response = session.get(url, timeout=30)
                response.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"Failed to fetch exams for {date}: {e}")
                raise SystemExit(1)

            try:
                raw_exams = _parse_xhr_response(response.text, query_date=date, session=session)
            except Exception as e:
                logger.error(
                    f"Failed to parse exams for {date} (status={response.status_code}): {e}"
                )
                raise SystemExit(1)

            all_exams.extend(raw_exams)

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
