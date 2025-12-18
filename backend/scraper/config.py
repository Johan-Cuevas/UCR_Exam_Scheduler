"""Configuration for the UCR exam scraper."""

# Base XHR endpoint template for UCR's 25Live calendar.
# The `date` parameter MUST be in YYYYMMDD format.
API_BASE_URL = (
    "https://25livepub.collegenet.com/s.aspx?calendar=final-exam-calendar"
    "&widget=main&date={date}&index={index}&spudformat=xhr"
)

# Index pagination bounds (inclusive) for the XHR widget.
INDEX_START = 0
INDEX_END = 300
INDEX_STEP = 25

# Small delay between upstream requests to avoid overloading the site.
REQUEST_DELAY_SECONDS = 0.2

# Inclusive date range bounds for fetching final exams.
# Format: YYYYMMDD
START_DATE = "20251206"
END_DATE = "20251212"

# Output file path (relative to backend directory)
OUTPUT_FILE = "data/exams.json"
