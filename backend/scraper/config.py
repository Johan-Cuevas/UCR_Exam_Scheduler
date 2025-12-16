"""Configuration for the UCR exam scraper."""

# Base XHR endpoint template for UCR's 25Live calendar.
# The `date` parameter MUST be in YYYYMMDD format.
API_BASE_URL = (
    "https://25livepub.collegenet.com/s.aspx?hosted=1&calendar=final-exam-calendar"
    "&widget=main&date={date}&spudformat=xhr"
)

# Inclusive date range bounds for fetching final exams.
# Format: YYYYMMDD
START_DATE = "20251206"
END_DATE = "20251212"

# Output file path (relative to backend directory)
OUTPUT_FILE = "data/exams.json"
