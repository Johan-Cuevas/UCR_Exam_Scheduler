"""Configuration for the UCR exam scraper."""

# Base API endpoint for UCR's 25Live calendar
API_BASE_URL = "https://25livepub.collegenet.com/calendars/final-exam-calendar.json"

# Default subject filter for proof of concept
DEFAULT_SUBJECT_FILTER = "MATH"

# Output file path (relative to backend directory)
OUTPUT_FILE = "data/exams.json"
