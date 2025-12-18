"""Unit tests for the 25Live exam scraper pagination and time derivation."""

from __future__ import annotations

import re

import pytest

from scraper import exam_scraper


class _FakeResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class _FakeSession:
    def __init__(self, html_by_index: dict[int, str]):
        self._html_by_index = html_by_index
        self.requested: list[int] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def get(self, url: str, timeout: int = 30):
        match = re.search(r"\bindex=(\d+)\b", url)
        assert match, f"url missing index param: {url}"
        index = int(match.group(1))
        self.requested.append(index)
        return _FakeResponse(self._html_by_index.get(index, ""))


def test_parse_day_html_derives_end_time_and_display_fields():
    html = (
        '<tr class="twSimpleTableEventRow0 ebg0">'
        '<th class="ebg0" scope="row">'
        '<span class="twDescription" role="heading" aria-level="3">'
        '<a eventid="1337687736">EXAM: CS 009A 001 34028</a>'
        "</span></th>"
        '<td class="ebg0"><span class="twStartDate">Dec 6</span></td>'
        '<td class="ebg0"><span class="twStartTime">11:30am</span></td>'
        '<td class="ebg0"><span class="twLocation">OLMH 1208</span></td>'
        "</tr>"
    )

    rows = exam_scraper._parse_day_html(html, query_date="20251206")
    assert len(rows) == 1

    row = rows[0]
    assert row["final_exam"] == "EXAM: CS 009A 001 34028"
    assert row["exam_date"] == "Dec 6"
    assert row["exam_date_iso"] == "2025-12-06"
    assert row["classroom"] == "OLMH 1208"

    # Canonical ISO datetimes
    assert row["startDateTime"] == "2025-12-06T11:30:00"
    assert row["endDateTime"] == "2025-12-06T14:30:00"

    # 12-hour clock display fields
    assert row["start_time"] == "11:30 AM"
    assert row["end_time"] == "2:30 PM"


def test_fetch_exams_stops_when_no_next_page_hint(monkeypatch):
    # Reduce the loop to a single date and a few indexes.
    monkeypatch.setattr(exam_scraper, "_iter_dates", lambda start, end: ["20251206"])
    monkeypatch.setattr(exam_scraper, "INDEX_START", 0)
    monkeypatch.setattr(exam_scraper, "INDEX_END", 50)
    monkeypatch.setattr(exam_scraper, "INDEX_STEP", 25)
    monkeypatch.setattr(exam_scraper, "REQUEST_DELAY_SECONDS", 0)

    # Page 0 includes a hint to index=25.
    page0 = (
        '<a href="s.aspx?date=20251206&index=25&spudformat=xhr">Next</a>'
        '<tr class="twSimpleTableEventRow0"><a eventid="1">EXAM: MATH 006A 001 35359</a>'
        '<span class="twStartDate">Dec 6</span><span class="twStartTime">8am</span>'
        '<span class="twLocation">SSC 335</span></tr>'
    )

    # Page 25 has rows but no hint to index=50 -> should stop after fetching index=25.
    page25 = (
        '<tr class="twSimpleTableEventRow0"><a eventid="2">EXAM: CS 010A 001 12345</a>'
        '<span class="twStartDate">Dec 6</span><span class="twStartTime">9am</span>'
        '<span class="twLocation">SSC 235</span></tr>'
    )

    fake_session = _FakeSession({0: page0, 25: page25, 50: "SHOULD NOT FETCH"})
    monkeypatch.setattr(exam_scraper.requests, "Session", lambda: fake_session)

    exams = exam_scraper.fetch_exams()

    assert fake_session.requested == [0, 25]
    assert len(exams) == 2


def test_fetch_exams_stops_when_no_rows(monkeypatch):
    monkeypatch.setattr(exam_scraper, "_iter_dates", lambda start, end: ["20251206"])
    monkeypatch.setattr(exam_scraper, "INDEX_START", 0)
    monkeypatch.setattr(exam_scraper, "INDEX_END", 50)
    monkeypatch.setattr(exam_scraper, "INDEX_STEP", 25)
    monkeypatch.setattr(exam_scraper, "REQUEST_DELAY_SECONDS", 0)

    fake_session = _FakeSession({0: "<html>No events</html>"})
    monkeypatch.setattr(exam_scraper.requests, "Session", lambda: fake_session)

    exams = exam_scraper.fetch_exams()

    assert fake_session.requested == [0]
    assert exams == []
